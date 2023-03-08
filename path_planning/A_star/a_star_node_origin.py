class Node():
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position
        self.f = 0
        self.g = 0
        self.h = 0

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
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path
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



def main():
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]
    start = [1, 1]
    end = [2, 5]

    path = astar(maze, start, end)
    print(path)
    for i in range (0,len(maze)):
        for j in range (0,len(maze[0])):
            if [i,j] in path:
                print("*, ", end='')
            else:
                print(str(maze[i][j])+", ",end='')
        print()
if __name__ == '__main__':
    main()