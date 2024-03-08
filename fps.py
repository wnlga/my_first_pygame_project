class FPSCounter:
    def __init__(self, surface, font, clock, health):
        self.surface = surface
        self.font = font
        self.clock = clock
        self.color = (255, 255, 255)
        self.health = self.font.render('HEALTH:' + str(3 - health), True, (255, 0, 0))
        self.health_rect = self.health.get_rect(center=(900, 12))
        self.fps_text = self.font.render(str(int(self.clock.get_fps())) + "FPS", False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(40, 12))
        
    def reheal(self, health):
        self.health = self.font.render('HEALTH:' + str(10 - health), True, (255, 0, 0))
        
    def render(self):
        self.surface.blit(self.fps_text, self.fps_text_rect)
        self.surface.blit(self.health, self.health_rect)

    def update(self):
        text = f"{self.clock.get_fps():2.0f} FPS"
        self.fps_text = self.font.render(text, False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(40, 12))


