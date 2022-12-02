class Settings:
    '''Stores all settings for Alien Invasion'''

    def __init__(self):
        '''Initialize the game's settings'''
        self.screen_width = 1280
        self.screen_height = 640
        self.ship_speed = 1.5
        self.obstacle_amount = 3
        self.cannonball_speed = 1.5
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (5, 250, 9)
        self.bullets_allowed = 3
        self.alien_speed = 1.0
        self.ship_limit = 3
        self.cannonball_frequency = .05

