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
close_list = []
open_list = []
path = []
loop = 0
mouse_count = 0
start_point = None
end_point = None
start = False
draw_obstacle = False
start_drag = False
length = 10

class Node():
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position
        self.f = 0
        self.g = 0
        self.h = 0

class maze:
    def __init__(self,x,y,obstacle,start_point,end_point,path,open_list,close_list):
        self.x, self.y = x*length,y*length
        self.length = length
        self.draw_point(obstacle,start_point,end_point,path,open_list,close_list)

    def draw_point(self,obstacle,start_point,end_point,path,open_list,close_list):
        cell = pygame.Rect(self.x,self.y,self.length,self.length)
        if obstacle == True:
            pygame.draw.rect(simulation_screen, pygame.Color('gray'), cell)
        elif start_point == True:
            pygame.draw.rect(simulation_screen, pygame.Color('purple'), cell)
        elif end_point == True:
            pygame.draw.rect(simulation_screen, pygame.Color('blue'), cell)
        elif path == True:
            pygame.draw.rect(simulation_screen, pygame.Color('green'), cell)
        elif open_list == True:
            pygame.draw.rect(simulation_screen, pygame.Color('red'), cell)
        elif close_list == True:
            pygame.draw.rect(simulation_screen, pygame.Color('yellow'), cell)
        pygame.draw.line(simulation_screen, pygame.Color('white'), (self.x, self.y), (self.x+self.length, self.y), 2)
        pygame.draw.line(simulation_screen, pygame.Color('white'), (self.x+self.length, self.y), (self.x+self.length, self.y+self.length), 2)
        pygame.draw.line(simulation_screen, pygame.Color('white'), (self.x+self.length, self.y+self.length), (self.x, self.y+self.length), 2)
        pygame.draw.line(simulation_screen, pygame.Color('white'), (self.x, self.y+self.length), (self.x, self.y), 2)

def find_duplicate(item, list):
    ans = False
    for i in list:
        if item.position == i.position:
            ans = True
            return True
        else:
            ans = False
    return ans

def astar(maze, start, end):
    start_node = Node(None, start)
    end_node = Node(None, end)
    open_list = []
    close_list = []
    open_list.append(start_node)
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        close_list.append(current_node)
        # Found the goal
        if current_node.position == end_node.position:
            path = []
            open_list_pos = []
            close_list_pos = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            for i in open_list:
                open_list_pos.append(i.position)
            for i in close_list:
                close_list_pos.append(i.position)
            return path[::-1],open_list_pos,close_list_pos # Return reversed path
        # Generate children
        children = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                if current_node.position[0] + i < 0 or current_node.position[0] + i > (len(maze) - 1):
                    continue
                if current_node.position[1] + j < 0 or current_node.position[1] + j > (len(maze[len(maze)-1]) -1):
                    continue
                node_position = [current_node.position[0] + i, current_node.position[1] + j]
                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] != 0:
                    continue
                new_node = Node(current_node, node_position)
                children.append(new_node)
                #print(new_node.position)
        # Loop through children
        for child in children:
            # Child is on the closed list
            ans = find_duplicate(child,close_list)

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            child.f = child.g + child.h

            # Child is already in the open list
            ans2 = find_duplicate(child,open_list)

            if ans == True:
                continue
            if ans2 == True:
                continue
            # Add the child to the open list
            open_list.append(child)

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

    for i in range (len(open_list)):
        maze(open_list[i][0],open_list[i][1],False,False,False,False,True,False)

    for i in range (len(close_list)):
        maze(close_list[i][0],close_list[i][1],False,False,False,False,False,True)

    for i in range (len(path)):
        maze(path[i][0],path[i][1],False,False,False,True,False,False)

    if loop == 0:
        simulation_screen_array = np.full((int(simulation_screen_array.shape[0]/10),int(simulation_screen_array.shape[1]/10)), 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if mouse_count == 2 and start == True:
            path, open_list, close_list = astar(simulation_screen_array,start_point,end_point)
            mouse_count = 0

        # get start point and end point, then start a* algo
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_count <=1 and start == True :
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
                actual_screen = pygame.display.set_mode((800, 480))
                simulation_screen_array = np.full((640,480), 0)
                simulation_screen = pygame.surfarray.make_surface(simulation_screen_array)
                interface_screen = pygame.Surface((200, 480))
                pygame.display.set_caption("A star demo")
                print("hover on restart button")

    loop += 1
    pygame.display.update()