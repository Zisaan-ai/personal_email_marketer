import json

class WorkflowExecutor:
    """
    Executes the Visual Builder Workflows based on a Directed Acyclic Graph (DAG) 
    JSON structure.
    """

    @staticmethod
    def process_event(workflow_dag: dict, current_node_id: str, event_data: dict) -> dict:
        """
        Traverses to the next node in the workflow based on the event (e.g. email opened, replied).
        """
        nodes = {n['id']: n for n in workflow_dag.get('nodes', [])}
        edges = workflow_dag.get('edges', [])
        
        current_node = nodes.get(current_node_id)
        if not current_node:
            return {"status": "error", "message": "Node not found."}
            
        print(f"Current State: Contact is at {current_node['type']} ({current_node['id']})")
        
        # Find the outgoing edges from the current node
        outgoing_edges = [e for e in edges if e['source'] == current_node_id]
        
        if not outgoing_edges:
            return {"status": "completed", "message": "End of workflow reached."}
            
        # Example: Branching logic based on Event
        # If the node is a Condition (e.g. "If Replied")
        if current_node['type'] == 'condition_replied':
            has_replied = event_data.get('replied', False)
            target_handle = "yes" if has_replied else "no"
            
            # Find the specific edge matching the condition output
            next_edge = next((e for e in outgoing_edges if e.get('sourceHandle') == target_handle), None)
            
            if next_edge:
                next_node_id = next_edge['target']
                return {
                    "status": "moved",
                    "next_node": nodes[next_node_id],
                    "action": f"Moved to {nodes[next_node_id]['type']} due to condition {target_handle}"
                }
            else:
                return {"status": "completed", "message": "No connecting path."}
        
        # Linear progression (e.g. Delay -> Action)
        next_node_id = outgoing_edges[0]['target']
        return {
            "status": "moved",
            "next_node": nodes[next_node_id],
            "action": f"Moved to {nodes[next_node_id]['type']} sequentially."
        }
