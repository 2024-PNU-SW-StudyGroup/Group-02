from .base_observer import UIObserver

class UIUpdateObserver(UIObserver):
    def __init__(self, visualization):
        self.visualization = visualization
        
    def update(self, event_type: str, data: dict):
        if event_type == 'algorithm_changed':
            self._update_algorithm_ui(data['algorithm'])
        elif event_type == 'visualization_changed':
            self._update_visualization_ui(data['type'], data['state'])
        elif event_type == 'policy_evaluation':
            self._update_evaluation_ui(data)
        elif event_type == 'agent_moved':
            self._update_agent_ui(data)
            
    def _update_algorithm_ui(self, algorithm):
        self.visualization.current_alg = algorithm
        self.visualization.control_section.update_algorithm(algorithm)
        
    def _update_visualization_ui(self, viz_type, state):
        self.visualization.visualization_section.update_visualization(viz_type, state)
        
    def _update_evaluation_ui(self, eval_data):
        self.visualization.control_section.update_evaluation(eval_data)
        
    def _update_agent_ui(self, agent_data):
        self.visualization.grid.update_agent(agent_data)