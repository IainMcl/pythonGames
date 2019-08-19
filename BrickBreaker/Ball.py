class Ball(object):
    def __init__(self, game_width, game_height):
        self.width = game_width
        self.height = game_height
        self.x = self.width // 2
        self.y = self.height // 2
        self.vx = 0
        self.vy = -1

    def draw(self):
        pass
    
    def move(self, dt=1):
        if self.x <= 0 or self.x >= self.width:
            self.vx *= -1
        if self.y <= 0:
            return 0
        if self.y >= self.height:
            self.vy *= -1
        
        self.x += self.vx * dt
        self.x += self.vy * dt
        return (self.x, self.y)

    def platformCollide(self, platform):
        if self.y <= platform.platform_height + platform.y:
            if self.x >= platform.x and self.x <= platform.x + platform.platform_width:
                self.xy *= -1
