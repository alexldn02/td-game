#Generic Scene class, all game scenes will be children of this class
class Scene:
    def __init__(self, game_state):

        self.game_state = game_state
