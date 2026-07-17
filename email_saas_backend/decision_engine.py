class DecisionEngine:
    """
    Core Deliverability Engine responsible for calculating reputations
    and adjusting provider-specific limits based on health and trends.
    """

    @staticmethod
    def calculate_reputation(bounce_rate: float, complaint_rate: float, reply_rate: float, volume_sent: int) -> float:
        """
        Calculates the reputation score on a scale of 0-100.
        Reputation = Base(100) - Penalty_Bounce - Penalty_Complaint + Bonus_Reply
        """
        if volume_sent < 10:
            return None  # Not enough data, carry over previous day's reputation

        base = 100.0
        
        # Penalties (Harsh penalties for bounces and spam complaints)
        penalty_bounce = (bounce_rate / 0.5) * 5.0
        penalty_complaint = (complaint_rate / 0.1) * 10.0
        
        # Bonus (Positive signals)
        bonus_reply = (reply_rate / 1.0) * 2.0
        bonus_reply = min(bonus_reply, 15.0) # Max +15 points
        
        reputation = base - penalty_bounce - penalty_complaint + bonus_reply
        
        # Bound between 0 and 100
        return max(0.0, min(100.0, reputation))

    @staticmethod
    def calculate_daily_strategy(current_limit: int, reputation: float) -> dict:
        """
        Determines the sending strategy for a specific provider.
        Returns the new daily limit, campaign %, warmup %, and strategy name.
        """
        if reputation >= 85.0:
            strategy = "Ramp-up"
            new_limit = int(current_limit * 1.10) # 10% growth
            campaign_pct = 70.0
            warmup_pct = 30.0
        elif 70.0 <= reputation < 85.0:
            strategy = "Stabilize"
            new_limit = current_limit # Freeze growth
            campaign_pct = 50.0
            warmup_pct = 50.0
        else:
            strategy = "Recovery"
            new_limit = int(current_limit * 0.50) # Cut by half
            campaign_pct = 20.0
            warmup_pct = 80.0
            
        return {
            "strategy": strategy,
            "daily_limit": max(10, new_limit), # Minimum floor of 10
            "campaign_percent": campaign_pct,
            "warmup_percent": warmup_pct
        }

    @staticmethod
    def calculate_risk_score(recent_bounces: int, recent_complaints: int, volume_spike_pct: float) -> float:
        """
        Calculates the overall risk score of a mailbox (0-100). Lower is better.
        """
        risk = (recent_bounces * 2.0) + (recent_complaints * 5.0)
        if volume_spike_pct > 50.0:
            risk += 10.0
        
        return min(100.0, risk)
