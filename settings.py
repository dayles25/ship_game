class Settings:
    '''Stores all settings for Alien Invasion'''

    def __init__(self):
        '''Initialize the game's settings'''
        self.screen_width = 1280
        self.screen_height = 640
        self.ship_speed = 1.5
        self.ship_limit = 3
        self.cannonball_speed = 1.5
        self.ship2_limit = 3
        self.cannonball_frequency = .005
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''initialize the setting that change throughout the game'''
        self.cannonball_frequency = .005

    def increase_speed(self):
        '''increase speed settings'''
        self.cannonball_frequency *= self.speedup_scale


