import pygame
import math

pygame.init()


DEADZONERAD = 70
LASTRADCHANGE = 0
LASTMOUSEMOTION = 0
CIRCLZ = False
ANGLE = 0
WIDTH = 1200
HEIGHT = 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
STATE = True
RAD = 2
BESTSCR = 0

class Circle:
    def __init__(self, x, y, rad):
        self.x = x
        self.y = y
        self.center = (x, y)
        self.radius = rad

    def drawing(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), 5)


paintsurf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
paintsurf.set_colorkey((0, 0, 0))
img = pygame.image.load('bgg.jpg')
SCREEN.blit(img, (0, 0))
pygame.draw.circle(SCREEN, (255, 255, 255), (WIDTH // 2, HEIGHT // 2), 5)
centre = Circle(WIDTH // 2, HEIGHT // 2, 5)
scoresurf = pygame.Surface((900, 450), pygame.SRCALPHA)
scoresurf.set_colorkey((0, 0, 0))



font = pygame.font.SysFont("Arial", 60)
smallfont = pygame.font.SysFont("Arial", 40)
smallfontzz = pygame.font.SysFont("Arial", 30)
wrongway = smallfontzz.render("Wrong way", True, (255, 0, 0))
tooclose = smallfontzz.render("Too close to dot", True, (255, 0, 0))
tinyfont = pygame.font.SysFont("PublicPixel.ttf", 20)
newbs = smallfontzz.render("New best score", True, (0, 255, 0))
fullcirc = smallfontzz.render("Draw full circle", True, (255, 0, 0))
slow = smallfontzz.render("Too slow", True, (255, 0, 0))



def leave_refresh():
    global score
    global scrx
    global tsc
    disx = action.pos[0] - prev_pos[0]
    disy = action.pos[1] - prev_pos[1]
    dis = max(abs(disx), abs(disy))
    for i in range(dis):
        cenx = prev_pos[0] + int(float(i) / dis * disx)
        ceny = prev_pos[1] + int(float(i) / dis * disy)
        diam = math.sqrt((cenx - WIDTH // 2) ** 2 + (ceny - HEIGHT // 2) ** 2)
        distance = abs(r - diam)
        if distance >= 51:
            red = 255
            green = 0
        else:
            red = 5 * distance
            green = 255 - 5 * distance
        score += green + red
        scrx += green
        pygame.draw.circle(paintsurf, (red, green, 0), (cenx, ceny), RAD)
    SCREEN.blit(paintsurf, (0, 0))
    tsc = scrx / score * 100

    refresh(tsc)



def refresh(ts):
    scoresurf.fill((0, 0, 0))
    if ts < 10:
        scoresurf.blit(font.render(f"{int(ts)}", True, colr_percentage(int(ts) / 100)), (50, 0))
    else:
        scoresurf.blit(font.render(f"{int(ts)}", True, colr_percentage(int(ts) / 100)),(270, 100))
    scoresurf.blit(smallfont.render(f"{int((round(ts, 1) - int(round(ts, 1))) * 10)}%", True, colr_percentage(int(ts) / 100)), (340, 117))
    SCREEN.blit(scoresurf, (270, 350))

def angles(directionz, anglez, previous):
    global ANGLE
    if abs(anglez - previous) > 100:
        if directionz == "clockwise":
            ANGLE += anglez
        else:
            ANGLE += 360 - anglez
        anglez += 360
        return False
    else:
        ANGLE += abs(anglez - previous)
    if directionz == "clockwise":
        if anglez < previous:
            return True
    elif directionz == "counter_clockwise":
        if anglez > previous:
            return True
    return False



def colr_percentage(percentage):
    if percentage <= 0.75:
        return 255, 0, 0
    if (1 - percentage) * 100 < 12.5:
        green = 255
        red = int(2060 * (1 - percentage))
    else:
        red = 255
        green = int(255 - 816 * (1 - percentage))
    return red, green, 0


def errtext(text):
    SCREEN.blit(img, (0, 0))
    scoresurf.fill((0, 0, 0))
    SCREEN.blit(paintsurf, (0, 0))
    SCREEN.blit(scoresurf, (600, 350))
    SCREEN.blit(text, (600, 430))
    global CIRCLZ
    CIRCLZ = True

def lvbs():
    global BESTSCR
    global CIRCLZ
    if ANGLE >= 360:
        if tsc > BESTSCR:
            BESTSCR = tsc
            SCREEN.blit(newbs, (500, 520))
        else:
            SCREEN.blit(smallfont.render(f"{int(BESTSCR)}.{int((round(BESTSCR, 1) - int(round(BESTSCR, 1))) * 10)}%", True, (255, 255, 255)), (570, 520))
            bstext = smallfontzz.render(f"Best:", True, (255, 255, 255))
            SCREEN.blit(bstext, (500, 520))
        CIRCLZ = True





def mouse_in_circle(x, y, radi):
    position = pygame.mouse.get_pos()
    distance = math.sqrt((position[0] - x) ** 2 + (position[1] - y) ** 2)
    return distance <= radi





def timetodraw(drawingtime, current, inception):
    if current - inception > drawingtime:
        errtext(slow)



while STATE:
    MSSTATE = pygame.mouse.get_pressed()
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            pygame.quit()

        if action.type == pygame.KEYDOWN:
            if action.key == pygame.K_SPACE:
                pygame.quit()
        if action.type == pygame.MOUSEBUTTONUP and CIRCLZ == False:
            errtext(fullcirc)

        if action.type == pygame.MOUSEBUTTONDOWN:
            SCREEN.blit(img, (0, 0))
            paintsurf.fill((0, 0, 0))
            centre.drawing(paintsurf)
            centre.drawing(SCREEN)
            prev_pos = None
            LASTMOUSEMOTION = 0
            LASTRADCHANGE = 0
            CIRCLZ = False
            start_angle = None
            direction = None
            ANGLE = 0
            score = 0
            scrx = 0
            tsc = 0
            RAD = 2
            start_time = pygame.time.get_ticks()
            if mouse_in_circle(WIDTH // 2, HEIGHT // 2, DEADZONERAD):
                errtext(tooclose)

        if action.type == pygame.MOUSEMOTION and MSSTATE[0] == True and CIRCLZ == False:
            SCREEN.blit(img, (0, 0))
            angle = math.degrees(math.atan2(action.pos[1] - HEIGHT // 2, action.pos[0] - WIDTH // 2))
            if angle < 0:
                angle += 360

            if start_angle == None:
                start_angle = angle
            elif direction == None:
                if angle > start_angle:
                    direction = "clockwise"
                else:
                    direction = "counter_clockwise"

            DEADZONERAD = 25
            if prev_pos is not None:
                leave_refresh()

                if angles(direction, angle, prev_angle):
                    errtext(wrongway)

                lvbs()

            if prev_pos is None:
                r = math.sqrt((action.pos[0] - WIDTH // 2) ** 2 + (action.pos[1] - HEIGHT // 2) ** 2)
            prev_pos = action.pos
            prev_angle = angle
            LASTMOUSEMOTION = pygame.time.get_ticks()
            if mouse_in_circle(WIDTH // 2, HEIGHT // 2, DEADZONERAD):
                errtext(tooclose)
            timetodraw(7000, pygame.time.get_ticks(), start_time)

    if pygame.time.get_ticks() - LASTRADCHANGE > 80:
        elapsed_time = pygame.time.get_ticks() - LASTMOUSEMOTION
        if elapsed_time > 10 and RAD <= 10:
            RAD += 1
        elif elapsed_time < 10 and RAD >= 3:
            RAD -= 1
        LASTRADCHANGE = pygame.time.get_ticks()
    pygame.display.update()
