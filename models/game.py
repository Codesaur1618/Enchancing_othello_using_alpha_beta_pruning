from abc import ABC, abstractmethod

class Game(ABC):
    """Abstract class, it defines the methods of a game.""" 

    @abstractmethod
    def actions(self, state, player):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    @abstractmethod
    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    @abstractmethod
    def terminal_state(self, state):
        """Return True if this is a final state for the game."""
        raise NotImplementedError