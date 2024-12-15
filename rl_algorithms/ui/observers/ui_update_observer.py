from .base_observer import UIObserver

class UIUpdateObserver(UIObserver):
    """
    Observer class responsible for updating the UI based on events.

    Attributes
    ----------
    visualization : object
        The visualization object containing various UI sections.

    Methods
    -------
    update(event_type: str, data: dict)
        Handles the event and calls the appropriate update method.
    _update_algorithm_ui(algorithm)
        Updates the UI for the algorithm section.
    _update_visualization_ui(viz_type, state)
        Updates the UI for visualization toggles.
    _update_evaluation_ui(eval_data)
        Updates the UI based on policy evaluation data.
    _update_agent_ui(agent_data)
        Updates the UI for the agent's movement.
    """
    def __init__(self, visualization):
        """
        Initializes the UIUpdateObserver with the given visualization object.

        Parameters
        ----------
        visualization : object
            The visualization object containing various UI sections.
        """
        self.visualization = visualization
        
    def update(self, event_type: str, data: dict):
        """
        Handles the event and calls the appropriate update method.

        Parameters
        ----------
        event_type : str
            The type of the event being handled (e.g., 'algorithm_changed').
        data : dict
            Additional data associated with the event.
        """
        if event_type == 'algorithm_changed':
            self._update_algorithm_ui(data['algorithm'])
        elif event_type == 'visualization_changed':
            self._update_visualization_ui(data['type'], data['state'])
        elif event_type == 'policy_evaluation':
            self._update_evaluation_ui(data)
        elif event_type == 'agent_moved':
            self._update_agent_ui(data)
            
    def _update_algorithm_ui(self, algorithm):
        """
        Updates the UI for the algorithm section.

        Parameters
        ----------
        algorithm : object
            The algorithm object to be updated in the UI.
        """
        self.visualization.current_alg = algorithm
        self.visualization.control_section.update_algorithm(algorithm)
        
    def _update_visualization_ui(self, viz_type, state):
        """
        Updates the UI for visualization toggles.

        Parameters
        ----------
        viz_type : str
            The type of visualization (e.g., 'Toggle Rewards').
        state : bool
            The state of the visualization (True/False).
        """
        self.visualization.visualization_section.update_visualization(viz_type, state)
        
    def _update_evaluation_ui(self, eval_data):
        """
        Updates the UI based on policy evaluation data.

        Parameters
        ----------
        eval_data : dict
            Data related to the policy evaluation (e.g., steps, delta, convergence status).
        """
        self.visualization.control_section.update_evaluation(eval_data)
        
    def _update_agent_ui(self, agent_data):
        """
        Updates the UI for the agent's movement.

        Parameters
        ----------
        agent_data : dict
            Data related to the agent's movement (e.g., action, state, terminal status).
        """
        self.visualization.grid.update_agent(agent_data)