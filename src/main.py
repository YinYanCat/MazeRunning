import time

import pygame
from src.algorithms.Genetics import *
import copy
from src.algorithms.BFSearch import *
from src.maze.Maze import Maze
from src.visuals.Visuals import Visual


def visual_search():
    print('\n-------------------\nVISUAL SEARCH KEYS:\n-------------------')
    print('[B] BFS Algorithm\n[N] BFS Original path and maze\n[M] BFS Best path and maze found')
    print('[G] Genetic Algorithm\n[H] Genetic Algorithm - Path Only')
    print('[Q] Quit current search\n[R] Generate New Maze')

    maze_size = 20
    maze_walk_att = maze_size
    maze_moves = maze_size * maze_size
    maze_fake_goal = 10
    maze_move_wall = 5
    maze_probability = [4,1]

    maze = Maze(maze_size,maze_walk_att,maze_moves,maze_fake_goal,maze_move_wall)
    delete_fake_goal_path(maze)

    bfs_maze = copy.deepcopy(maze)
    BFS_Search = False
    first_bfs = None
    best_bfs = None
    best_bfs_maze = None

    gen_maze = copy.deepcopy(maze)
    Gen_Search = False
    Gen_Path = True
    distance_maze = copy.deepcopy(maze)
    distance_mat = distance_matrix(distance_maze)

    visual_maze = copy.deepcopy(maze)
    visual = Visual(30)
    visual.set_maze(visual_maze)

    running = True
    while running and visual:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    maze = Maze(maze_size, maze_walk_att, maze_moves, maze_fake_goal, maze_move_wall)
                    delete_fake_goal_path(maze)
                    bfs_maze = copy.deepcopy(maze)
                    gen_maze = copy.deepcopy(maze)
                    Gen_Search = False
                    BFS_Search = False
                    first_bfs = None
                    best_bfs = None
                    best_bfs_maze = None
                    distance_maze = copy.deepcopy(maze)
                    distance_mat = distance_matrix(distance_maze)
                    visual_maze = copy.deepcopy(maze)
                    visual.set_maze(visual_maze)

                if event.key == pygame.K_b:
                    if not BFS_Search:
                        Gen_Search = False
                        BFS_Search = True
                        print('B: Breadth-first search Algorithm Active!')

                if event.key == pygame.K_n:
                    if first_bfs is not None:
                        print('N: Original Breadth-first search path')
                        BFS_Search = False
                        visual_maze = copy.deepcopy(maze)
                        draw_path(visual, visual_maze, first_bfs, -6)
                    else:
                        print('ERROR N: BFS has not been executed first ([B] Key)')

                if event.key == pygame.K_m:
                    if best_bfs is not None:
                        print('M: Best Breadth-first search path and maze distribution')
                        BFS_Search = False
                        best_bfs_maze.unsearch_matrix()
                        visual_maze = copy.deepcopy(best_bfs_maze)
                        draw_path(visual, visual_maze, best_bfs, -6)
                    else:
                        print('ERROR M: BFS has not been executed first ([B] Key)')

                if event.key == pygame.K_g:
                    if not Gen_Search:
                        BFS_Search = False
                        Gen_Search = True
                        Gen_Path = True
                        print('G: Genetic Algorithm Active!')

                if event.key == pygame.K_h:
                    if not Gen_Search:
                        BFS_Search = False
                        Gen_Search = True
                        Gen_Path = False
                        print('G: Instant Genetic Algorithm Active!')

                if event.key == pygame.K_q:
                    BFS_Search = False
                    Gen_Search = False
                    print('Q: Quitting search...')

        visual.draw()

        if BFS_Search:
            visual_maze = copy.deepcopy(bfs_maze)
            visual.set_maze(visual_maze)
            search, history = breadthFirstSearch(bfs_maze)
            toview = search
            value = -6
            if len(search) == 0:
                toview = history
                value = -7
                print(f"BFS: Exit NOT Found - Total Cells Reached: {len(history)}")
            elif best_bfs is None or len(search) < len(best_bfs):
                best_bfs = copy.deepcopy(search)
                best_bfs_maze = copy.deepcopy(bfs_maze)
                print(f"BFS: Exit Found!!! [NEW Short Path] - Path Length: {len(search)}")
            else:
                print(f"BFS: Exit Found!!! - Path Length: {len(search)}")
            if first_bfs is None:
                first_bfs = copy.deepcopy(search)

            draw_path(visual, visual_maze, toview, value)
            time.sleep(1)
            bfs_maze.unsearch_matrix()
            bfs_maze.switch_walls(maze_probability[0], maze_probability[1])

        elif Gen_Search:
            visual_maze = copy.deepcopy(gen_maze)
            visual.set_maze(visual_maze)
            visual.draw()
            print('Gen: Calculating Path...')
            history, move_matrix = geneticAlgorithm(gen_maze, distance_mat, maze_size*maze_size*2, Gen_Path, maze_probability,10, False)
            goal_x, goal_y = maze.get_end()
            if history[-1] == (int(goal_x), int(goal_y)):
                print(f"Gen: Exit Found!!! - Total Steps: {len(history)}")
            else:
                print(f"Gen: Exit NOT Found - Total Steps: {len(history)}")
            for i in range(len(history)):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            BFS_Search = False
                            Gen_Search = False
                            print('Q: Quitting search...')
                x, y = history[i]
                if Gen_Path and 0 <= i < len(move_matrix):
                    visual_maze.set_movable_values(move_matrix[i])
                aux = visual_maze.get_cell(x, y)
                visual_maze.set_cell(x, y, -6)
                if Gen_Path:
                    visual.draw()
                    time.sleep(0.2)
                    visual_maze.set_cell(x, y, aux)
                visual.draw()
                if not Gen_Search:
                    break
            time.sleep(1)

    pygame.quit()

def draw_path(visual, maze, path, color):
    visual.set_maze(maze)
    for i in range(len(path)):
        x, y = path[i]
        if i != 0:
            maze.set_cell(x, y, color)
        visual.draw()

def delete_fake_goal_path(maze):
    bfs_maze = copy.deepcopy(maze)
    search, history = breadthFirstSearch(bfs_maze)
    for i in range(len(search)):
        if maze.get_cell(search[i][0], search[i][1]) == -2:
            maze.set_cell(search[i][0], search[i][1], 0)

def test_time():
    print('\n--------------------------\n      TIME RESULTS\nEXPERIMENTS CONFIGURATION:\n--------------------------')
    mazes = int(input("Number of Mazes: "))
    cycles = int(input("Number of Cycles per Maze: "))
    iterations = int(input("Number of Iterations per Cycle: "))

    test_start = time.perf_counter()

    for i in range(mazes):
        maze_size = 10
        maze = Maze(size=maze_size, walkback_attempts=maze_size, moves=maze_size * maze_size, fake_goal=20, move_walls=5)
        delete_fake_goal_path(maze)

        distance_maze = copy.deepcopy(maze)
        distance_mat = distance_matrix(distance_maze)
        maze_size = maze.get_size()

        with open("MazeSearch"+str(i+1)+".csv", "w") as file:

            success_cycle = []
            probability = [0, 0]
            write_header(file, "BFS Time: ; ", "Iteration ", iterations)
            for j in range(cycles):
                file.write("Cycle "+str(j+1)+" 1/" + str(probability[0]) + " | 1/" + str(probability[1]) + "; ")
                success_iter = []
                for k in range(iterations):
                    success = "Yes"
                    start = time.perf_counter()
                    search, history = breadthFirstSearch(maze)
                    end = time.perf_counter()
                    maze.unsearch_matrix()
                    maze.switch_walls(probability[0], probability[1])
                    if len(search) == 0:
                        success = "No"
                    file.write(str(end-start)+"; ")
                    success_iter.append(success)
                success_cycle.append(success_iter)
                file.write("\n")
                probability = [probability[0] + 2, probability[1] + 1]
            print(f"BFS Maze {i + 1} ends")

            write_header(file, "\nBFS Success: ; ", "Iteration ", iterations)
            write_success(file, success_cycle, cycles, iterations)

            success_cycle = []
            probability = [0, 0]
            write_header(file, "\n\nGenetic Time: ; ", "Iteration ", iterations)
            for j in range(cycles):
                file.write("Cycle "+str(j+1)+" 1/" + str(probability[0]) + " | 1/" + str(probability[1]) + "; ")
                success_iter = []
                for k in range(iterations):
                    success = "No"
                    start = time.perf_counter()
                    history, move_matrix = geneticAlgorithm(maze, distance_mat, maze_size*maze_size*2, False, probability,10, False)
                    end = time.perf_counter()
                    goal_x, goal_y = maze.get_end()
                    if history[-1] == (int(goal_x), int(goal_y)):
                        success = "Yes"
                    file.write(str(end - start) + "; ")
                    success_iter.append(success)
                    print("Genetic iteration ends")
                success_cycle.append(success_iter)
                print("Genetic Cycle ends")
                file.write("\n")
                probability = [probability[0] + 2, probability[1] + 1]
            print(f"Genetic Maze {i + 1} ends")

            write_header(file, "\nGenetic Success: ; ", "Iteration ", iterations)
            write_success(file, success_cycle, cycles, iterations)
            file.close()

    test_end = time.perf_counter()
    print(f"Test finished after: {test_end-test_start}")

def write_header(file, title, name, iterations):
    file.write(title)
    for i in range(iterations):
        file.write(name + str(i + 1) + "; ")
    file.write("\n")

def write_success(file, success, cycles, iterations):
    for a in range(cycles):
        file.write("Cycle " + str(a + 1) + "; ")
        for b in range(iterations):
            file.write(success[a][b] + "; ")
        file.write("\n")



def main():
    print('\n--------------------\nMAZE SEARCH PROGRAM:\n--------------------')
    print('-VISUAL SEARCH: The main form where you can see the mazes and agents')
    print('-TIME RESULTS: Quick search form where only the times are delivered in a CSV file (No visuals)\n')

    case = input("Visual search (Y/N): ")
    while case!='Y' and case!='y' and case!='N' and case!='n':
        case = input("[[ERROR!]] Visual search (Y/N): ")
    if case == 'Y' or case == 'y':
        visual_search()
    else:
        test_time()

if __name__ =="__main__":
    main()