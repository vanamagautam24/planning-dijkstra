import time
import pygame
import sys
import copy

class Node:
    def __init__(self, state, parent, cost, distance):
        self.state = state              
        self.parent = parent                   
        self.cost = cost
        self.distance = distance 

    def __repr__(self):
        return str(self.state)
    
    def switch_(self, fn):
        registry = dict()
        registry['default'] = fn

        def register(case):
            def inner(fn):
                registry[case] = fn
                return fn
            return inner
        
        def decorator(case):
            fn = registry.get(case, registry['default'])
            return fn()
        
        decorator.register = register
        return decorator

    def check_obstacle_space(self, potential_node):
        x, y = potential_node[0], potential_node[1]
        if (x < 0) or (x > 400) or (y < 0) or (y > 250):
            return True
        if ((x - 300) ** 2 + (y - 185) ** 2 - 45 * 45) <= 0:
            return True
        elif ((0.316 * x + 178.608 - y) >= 0 and (0.857 * x + 106.429 - y) <= 0 and (-0.114 * x + 189.091 - y) <= 0) or ((-3.2 * x + 450 - y) >= 0 and (-1.232 * x + 220.348 - y) <= 0 and not (-0.114 * x + 189.091 - y) <= 0):
            return True
        elif (-0.575 * x + 169 - y) <= 0 and (160 - x) <= 0 and (0.575 * x + 31 - y) >= 0 and (-0.575 * x + 261 - y) >= 0and (240 - x) >= 0 and (0.575 * x - 61 - y) <= 0:
            return True
        else:
            return False

    def common_move(self, potential_node, direction_val, direction):
        if not self.check_obstacle_space(potential_node):
            move_node = Node(copy.deepcopy(self.state), Node(self.state, self.parent, self.cost, self.distance), self.cost + direction_val, direction_val)
            if direction == 'up':
                move_node.state[1] = move_node.state[1] + 1
            elif direction == 'down':
                move_node.state[1] = move_node.state[1] - 1
            elif direction == 'left':
                move_node.state[0] = move_node.state[0] - 1
            elif direction == 'right':
                move_node.state[0] = move_node.state[0] + 1
            elif direction == 'up_left':
                move_node.state[0], move_node.state[1]  = move_node.state[0] - 1, move_node.state[1] + 1
            elif direction == 'up_right':
                move_node.state[0], move_node.state[1]  = move_node.state[0] + 1, move_node.state[1] + 1
            elif direction == 'down_left':
                move_node.state[0], move_node.state[1]  = move_node.state[0] - 1, move_node.state[1] - 1
            elif direction == 'down_right':
                move_node.state[0], move_node.state[1]  = move_node.state[0] - 1, move_node.state[1] - 1
            return move_node
        return None

    def up(self):
        potential_node = (self.state[0], self.state[1] + 1)
        up_node = self.common_move(potential_node, 1, "up")
        return up_node

    def down(self):
        potential_node = (self.state[0], self.state[1] - 1)
        down_node = self.common_move(potential_node, 1, "down")
        return down_node

    def left(self):
        potential_node = (self.state[0] - 1, self.state[1])
        left_node = self.common_move(potential_node, 1, "left")
        return left_node

    def right(self):
        potential_node = (self.state[0] + 1, self.state[1])
        right_node = self.common_move(potential_node, 1, "right")
        return right_node
    
    def up_left(self):
        potential_node = (self.state[0] - 1, self.state[1] + 1)
        up_left = self.common_move(potential_node, 1.414, "up_left")
        return up_left
    
    def up_right(self):
        potential_node = (self.state[0] + 1, self.state[1] + 1)
        up_right = self.common_move(potential_node, 1.414, "up_right")
        return up_right

    def down_left(self):
        potential_node = (self.state[0] - 1, self.state[1] - 1)
        down_left = self.common_move(potential_node, 1.414, "down_left")
        return down_left

    def down_right(self):
        potential_node = (self.state[0] + 1, self.state[1] - 1)
        down_right = self.common_move(potential_node, 1.414, "down_right")
        return down_right

    def generate_children(self):
        children = []
        @self.switch_
        def move():
            return "Invalid move"
        
        move.register("up")(lambda: children.append(self.up()))
        move.register("down")(lambda: children.append(self.down()))
        move.register("left")(lambda: children.append(self.left()))
        move.register("right")(lambda: children.append(self.right()))  
        move.register("up_left")(lambda: children.append(self.up_left()))       
        move.register("up_right")(lambda: children.append(self.up_right()))       
        move.register("down_left")(lambda: children.append(self.down_left()))       
        move.register("down_right")(lambda: children.append(self.down_right()))  

        if self.up():
            move("up")
        if self.down():
            move("down")
        if self.left():
            move("left")
        if self.right():
            move("right")
        if self.up_left():
            move("up_left")
        if self.up_right():
            move("up_right")
        if self.down_left():
            move("down_left")
        if self.down_right():
            move("down_right")
        
        return children
    

if __name__== "__main__":
    while(1):
        x1, y1 = map(int, input("Please input the X and Y coordinates of the start node!\n").split())
        input_node = Node([x1, y1], None, 0, 0)
        
        x2, y2 = map(int, input("Please input the X and Y coordinates of the goal node!\n").split())
        goal_node = Node([x2, y2], None, 1000000, 0)
        
        if goal_node.check_obstacle_space(goal_node.state) or input_node.check_obstacle_space(input_node.state):
            print("Input Coordinates are in obstacle space!")
        else:
            break    

    queue = []                  
    queue.append(input_node)

    visited_states = []
    t = time.time()

    while(1):
        queue.sort(key = lambda x: x.cost)
        current_node = queue.pop(0)
        print(current_node, end = '\n')
        if current_node.state == [x2, y2]:
            print("Goal Found\n")
            print("Shortest path:\n")
            print(current_node.state)
    
            path = []
            while(current_node.state != [x1, y1]):
                current_node = current_node.parent
                path.append(current_node.state)
                print(current_node)
            break

        if current_node.state not in visited_states:
            visited_states.append(current_node.state)
            children = current_node.generate_children() 

            for child in children:
                queue.append(child)
        else:     
            parent_node = current_node.parent     
            if current_node.cost > parent_node.cost + current_node.distance:
                current_node.cost = parent_node.cost + current_node.distance
    print("Execution time", time.time()-t)
    
    print("Running pygame animation..................")
    pygame.init()
    screen = pygame.display.set_mode((400, 250))
    counter = 0
    
    while True:
        screen.fill((0,0,0))
        pygame.draw.circle(screen, (0,0, 255), (300, 65), 40)
        pygame.draw.polygon(screen, (0,0, 255), [[200, 109], [234, 129], [234, 170], [200, 190], [165, 170], [165, 129]])
        pygame.draw.polygon(screen, (0,0, 255), [[36, 65], [115, 40], [80, 70], [105, 150]])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if counter ==0:
            for state in visited_states:
                print(state)        
                pygame.draw.circle(screen, (255,255,255), (state[0], 250-state[1]), 1) 
                pygame.display.update()
            for state in path:
                pygame.draw.circle(screen, (0,0,255), (state[0], 250-state[1]), 1)
            pygame.display.update()
        counter +=1    
