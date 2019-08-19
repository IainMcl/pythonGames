class Platform(object):
    def __init__(self, game_width, game_height):
        self.width = game_width
        self.height = game_height
        self.x = self.width // 2
        self.y = self.height // 100
        self.platform_width = self.width // 20
        self.platform_height = self.height // 100
        self.speed = 1

    def move(self, direction):
        # Direction = 1 move right; -1 move left
        self.x += self.speed * direction
        if self.x + self.platform_width >= self.width:
            self.x = self.width - self.platform_width
        if self.x <= 0:
            self.x = 0
        