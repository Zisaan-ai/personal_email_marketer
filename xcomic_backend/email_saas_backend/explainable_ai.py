class ExplainableAI:
    """
    Generates human-readable explanations (NLG) for automatic decisions 
    made by the Deliverability Engine.
    """

    @staticmethod
    def generate_explanation(old_health: float, new_health: float, provider: str, metrics_delta: dict, strategy_result: dict) -> dict:
        """
        metrics_delta expects keys like 'bounce_rate', 'reply_rate', 'volume'
        with positive/negative float values representing the change.
        """
        summary_parts = []
        
        # Determine the primary reason for a health drop
        if new_health < old_health:
            summary_parts.append(f"Health dropped from {old_health:.1f} to {new_health:.1f}")
            
            # Find the worst offending metric
            if metrics_delta.get('bounce_rate', 0) > 0:
                summary_parts.append(f"because {provider} Bounce Rate increased by {metrics_delta['bounce_rate']:.1f}%")
            elif metrics_delta.get('complaint_rate', 0) > 0:
                summary_parts.append(f"because {provider} Spam Complaints increased by {metrics_delta['complaint_rate']:.2f}%")
            elif metrics_delta.get('reply_rate', 0) < 0:
                summary_parts.append(f"because {provider} Reply Rate decreased by {abs(metrics_delta['reply_rate']):.1f}%")
        elif new_health > old_health:
            summary_parts.append(f"Health improved from {old_health:.1f} to {new_health:.1f}")
            if metrics_delta.get('reply_rate', 0) > 0:
                summary_parts.append(f"due to {provider} Reply Rate increasing by {metrics_delta['reply_rate']:.1f}%")
        else:
            summary_parts.append(f"Health remained stable at {new_health:.1f}")
            
        summary = " ".join(summary_parts) + "."
        
        # Formulate Recommendation based on the Strategy
        recommendation = ""
        strategy = strategy_result['strategy']
        
        if strategy == "Recovery":
            recommendation = f"Apply Recovery Strategy: Reduced {provider} campaign volume by 50% and increased warmup traffic to 80%. Expected recovery: 5–7 days."
        elif strategy == "Stabilize":
            recommendation = f"Stabilize Strategy: Frozen {provider} daily limits to prevent further reputation damage. Split traffic 50/50 between warmup and campaigns."
        elif strategy == "Ramp-up":
            recommendation = f"Ramp-up Strategy: Safely increasing {provider} daily limit by 10% to {strategy_result['daily_limit']}."

        return {
            "summary": summary,
            "recommendation": recommendation,
            "action_taken": strategy
        }
