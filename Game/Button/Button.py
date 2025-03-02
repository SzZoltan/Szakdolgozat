import pygame


# Egy Gomb osztály ami egy x,y koordinátát, a gomb képét és egy scale értéket, hogy mekkorára szeretnénk növelni a képet
class Button:
    """
    Egy Gomb osztály amivel definiáljuk a Gomb objektumokat
    """
    def __init__(self, x, y, img, scale):
        """
        :param x: egész szám, a Gomb x koordinátája
        :param y: egész szám, a Gomb y koordinátája
        :param img: pygame.SurfaceType, a Gomb képe amit fel rajzol
        :param scale: egész szám, a képet mennivel skáláza
        """
        self.width = img.get_width()
        self.height = img.get_height()
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(img, (int( self.width*scale), int(self.height*scale)))
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

# Megszerzi az egér pozicióját és megnézi hogy megnyomták-e rá a bal egérgombot, visszaadja hogy megnyomták-e vagy nem
    def draw(self, win):
        """
        Felrajzolja a gombot a képernyőre és lekezeli, hogyha rákattintanak-e
        :param win: pygame.SurfaceType, az ablak amire felrajzolja majd a gombot
        :return: logikai változó, megnyomták-e a gombot
        """
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        win.blit(self.img, (self.rect.x, self.rect.y))

        return action
