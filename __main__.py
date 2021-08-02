import math as m
import numpy as np
from multiprocessing import Pool
import os
import time

Scene = 'Objects2.txt'

##Classes :

# points : np.array([x, y, z], dtype='float')
# colors : np.array([r, g, b], dtype='float')

class vec:
    def __init__(self, A, B):
        self.co = B - A
        self.norm = m.sqrt(PS(self, self))
        return None


class ray:
    def __init__(self, origin, goal):
        self.o = origin
        self.dir = unit(vec(origin, goal))
        return None

    def pt(self, t):
        return self.o + t * self.dir.co


class sphere:
    def __init__(self, center, radius, Kd):
        self.C = center
        self.r = radius
        self.kd = Kd
        return None


class source:
    def __init__(self, point, color):
        self.pt = point
        self.c = color
        return None


##Functions :

def unit(v):
    return vec(O, v.co / v.norm)


def PS(u, v):
    return u.co[0] * v.co[0] + u.co[1] * v.co[1] + u.co[2] * v.co[2]


def intersect(sp, ra):
    u, r = ra.dir, sp.r
    CS = vec(sp.C, ra.o)
    a, b = 0, -PS(u, CS)

    def f(t):
        return t ** 2 + 2 * t * PS(u, CS) + CS.norm ** 2 - r ** 2

    if f(b) >= 0 or CS.norm <= r or b <= 0:
        return None
    dt = b / 100
    while f(a) > -f(b) / 100:
        a -= f(a) * dt / (f(a + dt) - f(a))
    return a


def overH(sp, P, src):
    CP = vec(sp.C, P)
    return PS(CP, vec(src.pt, P)) < 0


def visible(listSp, j, P, src):
    sp, ra = listSp[j], ray(src.pt, P)
    if not overH(sp, P, src):
        return False
    for i in range(len(listSp)):
        if i != j:
            interi = intersect(listSp[i], ra)
            interj = intersect(sp, ra)
            if inter is not None and interj is not None:
                if inter < interj :
                    return False
    return True


def diffuse(sp, P, src):
    ra, N = ray(src.pt, P), unit(vec(sp.C, P))
    costheta = -PS(ra.dir, N)
    return sp.kd * src.c * costheta


def intersectAll(ra, listSp):
    closer = None
    distClose = np.inf
    for i in range(len(listSp)):
        inter = intersect(listSp[i], ra)
        if inter is not None:
            inter
            if inter < distClose:
                closer = i
                distClose = inter
    if closer is None:
        return None
    return ra.pt(distClose), closer


def diffuseAll(listSp, j, P, listSrc):
    color = black
    for src in listSrc:
        if visible(listSp, j, P, src):
            color = color + diffuse(listSp[j], P, src)
    return color


def rayScreen(Ω, Screen, i, j):
    width, height, pxlSz = Screen
    E = np.array([0, (i - width / 2 + 0.5), (height / 2 - j - 0.5)]) * pxlSz
    return ray(Ω, E)


#Multicore processing made by Loïc

def RTX_pixel(arg):
    i, j, pos, BG, listSp, listSrc, Screen = arg
    p = BG
    rayij = rayScreen(pos, Screen, j, i)
    inter = intersectAll(rayij, listSp)
    if inter:
        point, k = inter
        p = diffuseAll(listSp, k, point, listSrc)
    return p


def RTX(pos, BG, listSp, listSrc, Screen):
    width, height, pxlSz = Screen
    args = [(k//width, k % width, pos, BG, listSp, listSrc, Screen) for k in range(width * height)]
    with Pool(processes=os.cpu_count() - 1) as pool:
        image = pool.map(func=RTX_pixel, iterable=args)
    return np.array(image).reshape(height, width, 3)


def PrintSettings():
    window.fill((192, 192, 192))

    window.blit(sphereText, (239, -3))
    for i in range(len(Spheres)):
        sp = Spheres[i]
        window.blit(spSlider, (0, 20 + i * 90))

        window.blit(cursor, (36 + sp.C[0] * 10, 20 + 26 + i * 90))
        window.blit(cursor, (66 + sp.C[1] * 5, 20 + 45 + i * 90))
        window.blit(cursor, (66 + sp.C[2] * 5, 20 + 64 + i * 90))

        window.blit(cursor, (143 + sp.r * 20, 20 + 45 + i * 90))

        window.blit(cursor, (290 + sp.kd[0] * 100, 20 + 26 + i * 90))
        window.blit(cursor, (290 + sp.kd[1] * 100, 20 + 45 + i * 90))
        window.blit(cursor, (290 + sp.kd[2] * 100, 20 + 64 + i * 90))

        color = np.array([[tuple(255 * sp.kd) for i in range(78)] for j in range(78)])
        colSurf = pygame.Surface((78, 78))
        pygame.surfarray.blit_array(colSurf, color)
        window.blit(colSurf, (422, 20 + 6 + i * 90))

    if len(Spheres) == 0:
        window.blit(add, (246, 31))

    window.blit(sourceText, (670, -3))
    for i in range(len(Sources)):
        src = Sources[i]
        window.blit(srcSlider, (520, 20 + i * 90))

        window.blit(cursor, (520 + 66 + src.pt[0] * 5, 20 + 26 + i * 90))
        window.blit(cursor, (520 + 66 + src.pt[1] * 5, 20 + 45 + i * 90))
        window.blit(cursor, (520 + 66 + src.pt[2] * 5, 20 + 64 + i * 90))

        window.blit(cursor, (520 + 153 + src.c[0] * 100, 20 + 26 + i * 90))
        window.blit(cursor, (520 + 153 + src.c[1] * 100, 20 + 45 + i * 90))
        window.blit(cursor, (520 + 153 + src.c[2] * 100, 20 + 64 + i * 90))

        color = np.array([[tuple(255 * src.c) for i in range(78)] for j in range(78)])
        colSurf = pygame.Surface((78, 78))
        pygame.surfarray.blit_array(colSurf, color)
        window.blit(colSurf, (520 + 285, 20 + 6 + i * 90))

    if len(Sources) == 0:
        window.blit(add, (520 + 178, 31))

    rendSurf = pygame.Surface(Render.shape[:2])
    pygame.surfarray.blit_array(rendSurf, Render)
    window.blit(rendSurf, (520 + 383 + 5, 360 - h // 2))

    window.blit(smallR, (520 + 383 + 5 + w // 2 - 83, 360 - h // 2 - 36))
    window.blit(bigR, (520 + 383 + 5 + w // 2 - 83, 360 + h // 2 + 5))

    pygame.display.flip()


##Objects :

O = np.array([0, 0, 0])
white, black = np.array([1., 1., 1.]), np.array([0., 0., 0.])
w, h = 400, 280  # number of pixels of the render in width and height
ẟ = 0.05  # size of a pixel in the space
nbmax = 8  # maximum of objects of a type (sphere or source)

##Objects importation :

Spheres, Sources = [], []
File = open(Scene)
Data = File.read()
File.close()
Data = Data.split('\n')
for i in range(len(Data)):
    rawObj = Data[i].split(',')
    if rawObj[-1] == 'Sp':
        coords = np.array(rawObj[:3], dtype='float')
        radius = float(rawObj[3])
        Kd = np.array(rawObj[4:7], dtype='float')
        Spheres.append(sphere(coords, radius, Kd))
    elif rawObj[-1] == 'Src':
        coords = np.array(rawObj[:3], dtype='float')
        color = np.array(rawObj[3:6], dtype='float')
        Sources.append(source(coords, color))



# main loop
if __name__ == "__main__":
    
    import pygame
    eyePos = np.array([-15, 0, 0])
    background = np.array([0.44, 0.72, 0.96])
    
    ##Pygame integration :

    pygame.init()
    window = pygame.display.set_mode((520 + 383 + 10 + w, 740))
    clock = pygame.time.Clock()

    # image ressources
    spSlider = pygame.image.load('images\spSliders.png')
    srcSlider = pygame.image.load('images\srcSliders.png')
    cursor = pygame.image.load('images\cursor.png')
    add = pygame.image.load('images\\addButton.png')
    smallR = pygame.image.load('images\SmRender.png')
    bigR = pygame.image.load('images\BgRender.png')

    # text support
    all_fonts = pygame.font.get_fonts()
    if "comicsansms" in all_fonts:
        font = pygame.font.SysFont('Times New Roman', 17)
    else:
        font = pygame.font.Font(None, 40)

    sphereText = font.render("Spheres", True, (0, 0, 0))
    sourceText = font.render("Sources", True, (0, 0, 0))

    # path variables
    done = False
    big = False
    firstLoop = True
    Render = np.array([[tuple(background) for i in range(h)] for j in range(w)])
    while not done:
        
        if not big:
            firstLoop = True
            for event in pygame.event.get():

                nbSp = len(Spheres)
                nbSrc = len(Sources)
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos

                    # Add  objects
                    if 246 <= x <= 254 and 31 <= y - 90 * nbSp <= 39:
                        Spheres.append(sphere(np.array([0., 0., 0.]), 1, np.array([0.5, 0.5, 0.5])))
                    elif 520 + 178 <= x <= 520 + 186 and 31 <= y - 90 * nbSrc <= 39:
                        Sources.append(source(np.array([0., 0., 0.]), np.array([0., 0., 0.])))

                    # Render image
                    elif 520 + 383 + 5 + w // 2 - 83 <= x <= 520 + 383 + 5 + w // 2 + 83 and 360 - h // 2 - 36 <= y <= 360 - h // 2 - 5:
                        print("Rendering...")
                        started_time = time.time()
                        Render = RTX(eyePos, background, Spheres, Sources, (w, h, ẟ))
                        # tupling, rotate and mirror rendered image for pygame
                        Render = np.array([[tuple(255 * Render[i, j]) for i in range(h)] for j in range(w)])
                        print("Rendering done in : " + str(time.time() - started_time) + " seconds")

                    elif 520 + 383 + 5 + w // 2 - 83 <= x <= 520 + 383 + 5 + w // 2 + 83 and 360 + h // 2 + 5 <= y <= 360 + h // 2 + 36:
                        big = True

                    # Remove objects
                    else:
                        for i in range(nbSp):
                            if 510 <= x <= 518 and 21 <= y - 90 * i <= 29:
                                Spheres.pop(i)
                        for i in range(nbSrc):
                            if 520 + 373 <= x <= 520 + 381 and 21 <= y - 90 * i <= 29:
                                Sources.pop(i)

                # Moving cursors
                elif event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        x, y = event.pos

                        # Sphere cursors
                        for i in range(nbSp):
                            sp = Spheres[i]
                            # coordinates
                            if 17 <= x <= 117 and 47 <= y - 90 * i <= 52:
                                sp.C[0] = (x - 37) / 10
                            elif 17 <= x <= 117 and 65 <= y - 90 * i <= 70:
                                sp.C[1] = (x - 67) / 5
                            elif 17 <= x <= 117 and 84 <= y - 90 * i <= 89:
                                sp.C[2] = (x - 67) / 5
                            # size
                            elif 154 <= x <= 254 and 65 <= y - 90 * i <= 70:
                                sp.r = (x - 144) / 20
                            # color
                            elif 291 <= x <= 391 and 47 <= y - 90 * i <= 52:
                                sp.kd[0] = (x - 291) / 100
                            elif 291 <= x <= 391 and 65 <= y - 90 * i <= 70:
                                sp.kd[1] = (x - 291) / 100
                            elif 291 <= x <= 391 and 84 <= y - 90 * i <= 89:
                                sp.kd[2] = (x - 291) / 100

                        for i in range(nbSrc):
                            src = Sources[i]
                            # coordinates
                            if 520 + 17 <= x <= 520 + 117 and 47 <= y - 90 * i <= 52:
                                src.pt[0] = (x - 520 - 67) / 5
                            elif 520 + 17 <= x <= 520 + 117 and 65 <= y - 90 * i <= 70:
                                src.pt[1] = (x - 520 - 67) / 5
                            elif 520 + 17 <= x <= 520 + 117 and 84 <= y - 90 * i <= 89:
                                src.pt[2] = (x - 520 - 67) / 5
                            # color
                            elif 520 + 154 <= x <= 520 + 254 and 47 <= y - 90 * i <= 52:
                                src.c[0] = (x - 520 - 154) / 100
                            elif 520 + 154 <= x <= 520 + 254 and 65 <= y - 90 * i <= 70:
                                src.c[1] = (x - 520 - 154) / 100
                            elif 520 + 154 <= x <= 520 + 254 and 84 <= y - 90 * i <= 89:
                                src.c[2] = (x - 520 - 154) / 100

            PrintSettings()

        else:
            w, h = 520 + 383 + 10 + w, 740
            ẟ = 0.02
            if firstLoop:
                print("Rendering...")
                started_time = time.time()
                Render = RTX(eyePos, background, Spheres, Sources, (w, h, ẟ))
                # tupling, rotate and mirror rendered image for pygame
                Render = np.array([[tuple(255 * Render[i, j]) for i in range(h)] for j in range(w)])
                print("Rendering done in : " + str(time.time()-started_time) + " seconds")
                rendSurf = pygame.Surface(Render.shape[:2])
                pygame.surfarray.blit_array(rendSurf, Render)
                window.blit(rendSurf, (0, 0))
                pygame.display.flip()
                firstLoop = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    big = False
                    w, h = 400, 280  # number of pixels of the render in width and height   
                    ẟ = 0.05
                    Render = np.array([[tuple(background) for i in range(h)] for j in range(w)])

        clock.tick(30)

    pygame.quit()
