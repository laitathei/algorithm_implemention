import pygame
import numpy as np
from pygame.locals import *
from KalmenFilter import kf

pygame.init()
actual_screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption("Mouse Tracking demo")
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
clock = pygame.time.Clock()
fps = 60
KF = kf(4, 2, 2, 1/fps, 10, 0.5, 0.5, 0.01)
x = y = 0
while True:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if (event.type == pygame.MOUSEMOTION) and (clock.get_fps() != 0):
            actual_screen.fill((0,0,0))
            dt = 1/clock.get_fps()
            x = event.pos[0]
            y = event.pos[1]
            (estimate_x, estimate_y) = KF.update(np.array([[x],[y]]))
            estimate_x = int(estimate_x)
            estimate_y = int(estimate_y)
            (predict_x, predict_y) = KF.predict(np.array([[0],[0]]))
            predict_x = int(predict_x)
            predict_y = int(predict_y)
            print("_______________")
            print("measure n: ", x, y)
            print("estimate n: ", estimate_x,estimate_y)
            print("predict n+t: ", predict_x, predict_y)
            pygame.draw.line(actual_screen, (0, 255, 0), (int(estimate_x-10), int(estimate_y)), (int(estimate_x+10), int(estimate_y)))
            pygame.draw.line(actual_screen, (0, 255, 0), (int(estimate_x), int(estimate_y-10)), (int(estimate_x), int(estimate_y+10)))
            pygame.draw.line(actual_screen, (255, 0, 0), (int(predict_x-10), int(predict_y)), (int(predict_x+10), int(predict_y)))
            pygame.draw.line(actual_screen, (255, 0, 0), (int(predict_x), int(predict_y-10)), (int(predict_x), int(predict_y+10)))
            #pygame.draw.circle(actual_screen, (255, 0, 0), [predict_x, predict_y], 10)
            #pygame.draw.circle(actual_screen, (0, 0, 255), [estimate_x, estimate_y], 10)
            pygame.display.update()
