import time

import pygame
from src.algorithms.Genetics import *
import copy
from src.algorithms.BFSearch import *
from src.maze.Maze import Maze
from src.visuals.Visuals import Visual

def visual_search():
    print('\n-------------\nPROGRAM KEYS:\n-------------')
    print('[B] BFS Algorithm (Toggle to Pause)\n[N] BFS Original Path and Maze\n[M] BFS Best Path and Maze Found')
    print('[G] Genetic Algorithm (Toggle to Pause)\n[I] Instance Visual (Toggle)')

    maze_size = 10
    maze_walk_att = maze_size * 3
    maze_moves = maze_size * maze_size
    maze_fake_goal = 20
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
    distance_maze = copy.deepcopy(maze)
    distance_mat = distance_matrix(distance_maze)

    visual_maze = copy.deepcopy(maze)
    visual = Visual(40)
    visual.set_maze(visual_maze)
    instant_visual = False

    running = True
    while running and visual:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_i:
                    instant_visual = not instant_visual
                    print_toggle(instant_visual, 'Instant Visual')

                if event.key == pygame.K_b:
                    Gen_Search = False
                    BFS_Search = not BFS_Search
                    print_toggle(BFS_Search, 'Breadth-first search algorithm')

                if event.key == pygame.K_n:
                    if first_bfs is not None:
                        print('Original Breadth-first search path')
                        BFS_Search = False
                        visual_maze = copy.deepcopy(maze)
                        draw_path(visual, visual_maze, first_bfs, -6)
                    else:
                        print('ERROR N: BFS has not been executed first ([B] Key)')

                if event.key == pygame.K_m:
                    if best_bfs is not None:
                        print('Best Breadth-first search path and maze distribution')
                        BFS_Search = False
                        best_bfs_maze.unsearch_matrix()
                        visual_maze = copy.deepcopy(best_bfs_maze)
                        draw_path(visual, visual_maze, best_bfs, -6)
                    else:
                        print('ERROR M: BFS has not been executed first ([B] Key)')

                if event.key == pygame.K_g:
                    BFS_Search = False
                    Gen_Search = not Gen_Search
                    print_toggle(Gen_Search, 'Genetic algorithm')

                if event.key == pygame.K_d:
                    print('Distance Matrix from Goal:')
                    for x in range(maze.size):
                        for y in range(maze.size):
                            print(f"{int(distance_mat[x][y]):02d}", end=" ")
                        print('')
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
            elif best_bfs is None or len(search) < len(best_bfs):
                best_bfs = copy.deepcopy(search)
                best_bfs_maze = copy.deepcopy(bfs_maze)
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
            print('Calculating Path...')
            history, move_matrix = geneticAlgorithm(gen_maze, distance_mat, maze_size*maze_size*2, not instant_visual, maze_probability,10, False)
            goal_x, goal_y = maze.get_end()
            if history[-1] == (int(goal_x), int(goal_y)):
                print(f"Steps to find the goal: {len(history)}")
            else:
                #print(f"ended at {history[-1]} goal was at {int(goal_x), int(goal_y)}")
                print(f"Couldn't find goal, total steps: {len(history)}")
            for i in range(len(history)):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_g:
                            Gen_Search = False
                            print_toggle(Gen_Search, 'Genetic algorithm')
                x, y = history[i]
                if not instant_visual:
                    visual_maze.set_movable_values(move_matrix[i])
                aux = visual_maze.get_cell(x, y)
                visual_maze.set_cell(x, y, -6)
                if not instant_visual:
                    visual.draw()
                    time.sleep(0.5)
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

def print_toggle(toggle, name):
    if toggle:
        print(name, '[Activated]')
    else:
        print(name, '[Deactivate]')

def delete_fake_goal_path(maze):
    bfs_maze = copy.deepcopy(maze)
    search, history = breadthFirstSearch(bfs_maze)
    for i in range(len(search)):
        if maze.get_cell(search[i][0], search[i][1]) == -2:
            maze.set_cell(search[i][0], search[i][1], 0)


def test_time():
    mazes = int(input("Number of Mazes: "))
    cycles = int(input("Number of Cycles per Maze: "))
    iterations = int(input("Number of Iterations per Cycle: "))

    test_start = time.perf_counter()

    for i in range(mazes):
        maze_size = 10
        maze = Maze(maze_size, maze_size, maze_size * maze_size, 20, 5)
        delete_fake_goal_path(maze)

        distance_maze = copy.deepcopy(maze)
        distance_mat = distance_matrix(distance_maze)
        maze_size = maze.get_size()

        with open("MazeSearch"+str(i+1)+".csv", "w") as file:

            success_cycle = []
            probability = [0, 0]
            write_header(file, "BFS Time: ; Probability; ", "Iteration ", iterations)
            for j in range(cycles):
                file.write("Cycle "+str(j+1)+"; 1/" + str(probability[0]) + " | 1/" + str(probability[1]) + "; ")
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
            write_header(file, "\n\nGenetic Time: ; Probability; ", "Iteration ", iterations)
            for j in range(cycles):
                file.write("Cycle "+str(j+1)+"; 1/" + str(probability[0]) + " | 1/" + str(probability[1]) + "; ")
                success_iter = []
                for k in range(iterations):
                    success = "No"
                    start = time.perf_counter()
                    history, move_matrix = geneticAlgorithm(maze, distance_mat, maze_size*maze_size*2, False, probability,10, True)
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
    case = 1
    if case == 1:
        test_time()
    else:
        visual_search()

if __name__ =="__main__":
    main()