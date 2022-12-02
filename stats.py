class Stats:
    '''Track statistics for Ships Ahoy'''
    def __init__(self, sa_game):
        '''initialize statistics'''
        self.settings = sa_game.settings
        self.reset_stats()
        self.game_active = False
        self.level = 0
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.ship2s_left = self.settings.ship2_limit