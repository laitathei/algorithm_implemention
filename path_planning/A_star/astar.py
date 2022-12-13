import pygame
import math
import numpy as np
from pygame.locals import *

pygame.init()
actual_screen = pygame.display.set_mode((800, 480))
simulation_screen_array = np.full((640,480), 0)
#simulation_screen = pygame.Surface((640, 480))
simulation_screen = pygame.surfarray.make_surface(simulation_screen_array)
interface_screen = pygame.Surface((200, 480))
pygame.display.set_caption("A star demo")

obstacle_list = []
open_list = []
close_list = []
path = []
loop = 0
mouse_count = 0
start_point = None
end_point = None
start = False
draw_obstacle = False
start_drag = False
length = 10

class maze:
    def __init__(self,x,y,obstacle,start_point,end_point,path,close_list,open_list):
        self.x, self.y = x*length,y*length
        self.length = length
        self.draw_point(obstacle,start_point,end_point,path,close_list,open_list)

    def draw_point(self,obstacle,start_point,end_point,path,close_list,open_list):
        cell = pygame.Rect(self.x,self.y,self.length,self.length)
        if obstacle == True:
            pygame.draw.rect(simulation_screen, pygame.Color('gray'), cell)
        elif start_point == True:
            pygame.draw.rect(simulation_screen, pygame.Color('purple'), cell)
        elif end_point == True:
            pygame.draw.rect(simulation_screen, pygame.Color('blue'), cell)
        elif path == True:
            pygame.draw.rect(simulation_screen, pygame.Color('green'), cell)
        elif close_list == True:
            pygame.draw.rect(simulation_screen, pygame.Color('blue'), cell)
        elif open_list == True:
            pygame.draw.rect(simulation_screen, pygame.Color('red'), cell)
        pygame.draw.line(simulation_screen, pygame.Color('white'), (self.x, self.y), (self.x+self.length, self.y), 2)
        pygame.draw.line(simulation_screen, pygame.Color('white'), (self.x+self.length, self.y), (self.x+self.length, self.y+self.length), 2)
        pygame.draw.line(simulation_screen, pygame.Color('white'), (self.x+self.length, self.y+self.length), (self.x, self.y+self.length), 2)
        pygame.draw.line(simulation_screen, pygame.Color('white'), (self.x, self.y+self.length), (self.x, self.y), 2)

def astar(maze, start, end):
    open_list = [] # store unchecked point
    close_list = [] # store checked point
    open_list.append([[[None,None,None],[None,None]],[[0,0,0],[start[0], start[1]]]])
    end = [[[None,None,None],[None,None]],[[0,0,0],[end[0], end[1]]]]
    step = 0
    while len(open_list) > 0:
        print("A * step: {}".format(step))
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item[1][0][0] < current_node[1][0][0]:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        close_list.append(current_node)

        # Found the goal
        if current_node[1][1] == end[1][1]:
            path = []
            while current_node[1][1] != close_list[0][1][1]:
                for i in range (len(close_list)):
                    if close_list[i][1] == current_node[1]:
                        path.append(close_list[i][1][1])
                        current_node = close_list[i][0]
                        for j in range (len(close_list)):
                            if close_list[j][1] == current_node:
                                current_node = close_list[j]
            if current_node[1][1] == close_list[0][1][1]:
                path.append(close_list[0][1][1])
                path = path[::-1]
                #print("path: {}".format(path))
            return path,open_list,close_list

        # Generate children
        children = []
        adjacent_squares_list = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        #adjacent_squares_list = [[-1,0],[0,-1],[0,1],[1,0]]
        #print("                   ")
        for i in range (len(adjacent_squares_list)): # Adjacent squares
            not_add = False
            # Get node position
            children_node = [current_node[1][1][0] + adjacent_squares_list[i][0], current_node[1][1][1] + adjacent_squares_list[i][1]]

            # Make sure within range
            if children_node[0] > (len(maze) - 1) or children_node[0] < 0 or children_node[1] > (len(maze[len(maze)-1]) -1) or children_node[1] < 0:
                not_add = True

            # Make sure walkable terrain
            if maze[children_node[0]][children_node[1]] != 0:
                not_add = True
            
            if not_add == False:
                # Append children to list [current_node,children_node]
                children.append([[[current_node[1][0][0],current_node[1][0][1],current_node[1][0][2]],[current_node[1][1][0],current_node[1][1][1]]], [[0,0,0],[children_node[0],children_node[1]]]])
        
        # Loop through children
        for i in range (len(children)):
            not_add = False
            # Create the f, g, and h values
            # [f,g,h]
            children[i][1][0][1] = children[i][0][0][1] + 1
            children[i][1][0][2] = abs(children[i][1][1][0] - end[1][1][0]) + abs(children[i][1][1][1] - end[1][1][1])
            children[i][1][0][0] = children[i][1][0][1] + children[i][1][0][2]

            # Child is on the closed list
            for j in range (len(close_list)):
                if children[i][1][1] == close_list[j][1][1]:
                    not_add = True

            # Child is already in the open list
            for k in range (len(open_list)):
                if children[i][1][1] == open_list[k][1][1]:
                    not_add = True

            if not_add == False:
                # Add the child to the open list
                open_list.append(children[i])
        step += 1

while True:
    mouse = pygame.mouse.get_pos()
    interface_screen.fill("gray")
    smallfont = pygame.font.SysFont('Corbel',20)
    actual_screen.blit(simulation_screen, (0, 0))
    actual_screen.blit(interface_screen, (640, 0))

    draw_obstacle_button = pygame.Rect(0,0,160,40)
    draw_obstacle_button.center = (720,40)
    draw_obstacle_text = smallfont.render('Draw obstacle' , True , (0,0,0))
    pygame.draw.rect(actual_screen, (255,255,255), draw_obstacle_button)
    actual_screen.blit(draw_obstacle_text , (640,40))

    start_button = pygame.Rect(0,0,160,40)
    start_button.center = (720,100)
    start_button_text = smallfont.render('Start A* calculation' , True , (0,0,0))
    pygame.draw.rect(actual_screen, (255,255,255), start_button)
    actual_screen.blit(start_button_text , (640,100))

    restart_button = pygame.Rect(0,0,160,40)
    restart_button.center = (720,160)
    restart_button_text = smallfont.render('Restart' , True , (0,0,0))
    pygame.draw.rect(actual_screen, (255,255,255), restart_button)
    actual_screen.blit(restart_button_text , (640,160))

    for i in range (len(obstacle_list)):
        maze(obstacle_list[i][0],obstacle_list[i][1],True,False,False,False,False,False)

    if start_point != None:
        maze(start_point[0],start_point[1],False,True,False,False,False,False)
    if end_point != None:
        maze(end_point[0],end_point[1],False,False,True,False,False,False)

    for i in range (len(close_list)):
        maze(close_list[i][0],close_list[i][1],False,False,False,False,True,False)

    for i in range (len(open_list)):
        maze(open_list[i][0],open_list[i][1],False,False,False,False,False,True)

    for i in range (len(path)):
        maze(path[i][0],path[i][1],False,False,False,True,False,False)

    if loop == 0:
        simulation_screen_array = np.full((int(simulation_screen_array.shape[0]/10),int(simulation_screen_array.shape[1]/10)), 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if mouse_count == 2 and start == True:
            tmp = []
            path, tmp, tmp2 = astar(simulation_screen_array,start_point,end_point)
            for i in range (len(tmp)):
                open_list.append([tmp[i][1][1][0], tmp[i][1][1][1]])
            for i in range (len(tmp2)):
                close_list.append([tmp2[i][1][1][0], tmp2[i][1][1][1]])
            mouse_count = 0

        # get start point and end point, then start a* algo
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_count <=1 and start == True :
            if event.button == 1:
                if mouse_count == 0:
                    start_x,start_y = pygame.mouse.get_pos()
                    start_point = [math.ceil(start_x/length),math.ceil(start_y/length)]
                    print("start point: {}".format(start_point))
                if mouse_count == 1:
                    end_x,end_y = pygame.mouse.get_pos()
                    end_point = [math.ceil(end_x/length),math.ceil(end_y/length)]
                    print("end point: {}".format(end_point))
                    for i in range (len(obstacle_list)):
                        simulation_screen_array[obstacle_list[i][0]][obstacle_list[i][1]] = 1
                mouse_count += 1
            
        if event.type == pygame.MOUSEBUTTONDOWN and draw_obstacle == True:
            if event.button == 1:
                if start_drag%2 == 0:
                    start_drag = True
                else:
                    start_drag = False
                    mouse_count += 1

        if start_drag == True:
            if event.type == pygame.MOUSEMOTION:
                x,y = pygame.mouse.get_pos()
                if obstacle_list == []:
                    obstacle_list.append([math.ceil(x/length),math.ceil(y/length)])
                for i in range (len(obstacle_list)):
                    if [math.ceil(x/length),math.ceil(y/length)] not in obstacle_list[i]:
                        obstacle_list.append([math.ceil(x/length),math.ceil(y/length)])
                obstacle_list = [i for n, i in enumerate(obstacle_list) if i not in obstacle_list[:n]]

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 640 <= mouse[0] <= 800 and 20 <= mouse[1] <= 60:
                draw_obstacle = True
                mouse_count = 0
                start = False
            elif 640 <= mouse[0] <= 800 and 80 <= mouse[1] <= 120:
                draw_obstacle = False
                start = True
                mouse_count = 0
                start_drag = False
                print("hover on start button")
            elif 640 <= mouse[0] <= 800 and 140 <= mouse[1] <= 180:
                obstacle_list = []
                close_list = []
                open_list = []
                path = []
                loop = -1
                mouse_count = 0
                start_point = None
                end_point = None
                start = False
                draw_obstacle = False
                start_drag = False
                actual_screen = pygame.display.set_mode((800, 480))
                simulation_screen_array = np.full((640,480), 0)
                simulation_screen = pygame.surfarray.make_surface(simulation_screen_array)
                interface_screen = pygame.Surface((200, 480))
                pygame.display.set_caption("A star demo")
                print("hover on restart button")

    loop += 1
    pygame.display.update()
