
class Settings:
    def __init__(self, size, surf):
        self.size = size
        self.surf = surf
        self.screen = None

        self.f_tr = 0.93

        self.gravity_rad = 60
        self.dots_go_back = False

        self.dots = []

        self.colors = [(254, 0, 2), (216, 0, 39), (161, 1, 93),
                        (99, 0, 158), (42, 0, 213), (3, 2, 252)]


        self.test_colors = []

        self.text_size = 60
        self.text_alpha = 0

        r, g, b = 255, 40, 0

        for k in range(52):
            self.test_colors.append((r, g, b))

            r -= 5
            b += 5
