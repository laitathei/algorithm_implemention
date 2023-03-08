import math
import numpy as np

def astar(maze, start, end):
    open_list = [] # store unchecked point
    close_list = [] # store checked point
    open_list.append([[[None,None,None],[None,None]],[[0,0,0],[start[0], start[1]]]])
    end = [[[None,None,None],[None,None]],[[0,0,0],[end[0], end[1]]]]
    step = 0
    while len(open_list) > 0:
        print("step: {}".format(step))
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item[1][0][0] < current_node[1][0][0]:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        print(current_index)
        print(open_list[current_index])
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
                print("path: {}".format(path))
                print("close list: {}".format(np.array(close_list)))
                print("len(close_list): {}".format(len(close_list)))
                print("len(open_list): {}".format(len(open_list)))
                print("len(path): {}".format(len(path)))
                print("step: {}".format(step))
            return path, open_list, close_list

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
        
        print("open_list: {}".format(open_list))
        print("len(children): {}".format(len(children)))

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

def main():
    # maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # [(0, 0), (1, 1), (2, 2), (3, 3), (4, 3), (5, 4), (6, 5), (7, 6)]
    # [(2, 0), (2, 1), (2, 2), (1, 3), (0, 4), (1, 5), (2, 6), (2, 7), (2, 8)]
    # start = [4, 2]
    # end = [2, 5]
    start = [1, 1]
    end = [7, 7]
    path,tmp,tmp2 = astar(maze,start,end)
    open_list = []
    close_list = []
    for i in range (len(tmp)):
        open_list.append([tmp[i][1][1][0], tmp[i][1][1][1]])
    for i in range (len(tmp2)):
        close_list.append([tmp2[i][1][1][0], tmp2[i][1][1][1]])

    print("open_list: {}".format(open_list))
    print("close_list: {}".format(close_list))
                
    for i in range (0,len(maze)):
        for j in range (0,len(maze[0])):
            if [i,j] in path:
                print("*, ", end='')
            elif [i,j] in open_list:
                print("!, ", end='')
            elif [i,j] in close_list:
                print("/, ", end='')
            else:
                print(str(maze[i][j])+", ",end='')
        print()

if __name__ == '__main__':
    main()