from .soccer import SoccerPitch
from .basketball import BasketballPitch
from .tennis import TennisPitch
from .handball import HandballPitch


class Pitch:
    def __init__(self, sport="soccer", **kwargs):
        pitch_classes = {
            "soccer": SoccerPitch,
            "basketball": BasketballPitch,
            "tennis": TennisPitch,
            "handball": HandballPitch,
        }

        pitch_class = pitch_classes.get(sport.lower())
        if pitch_class:
            self.pitch = pitch_class(**kwargs)
        else:
            raise NotImplementedError(f"Sport '{sport}' is not implemented yet.")

    def __getattr__(self, name):
        return getattr(self.pitch, name)
