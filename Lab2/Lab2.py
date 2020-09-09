"""
Program: This program is to solve a travel-planning problem, which gives user best
arrive time from the start city to destination city.
The program implementation based on modified version of Dijkstra's Algorithm.
"""

import sys


"""Function use to read txt file then return integer type list"""
def read_data():
    new_data = []
    try:
        file = open("2019_Lab_2_flights_real_data.txt", "r")
        data_line = file.readline()
        while len(data_line) > 0:
            new_data.append([int(num) for num in data_line.split("\t")])
            data_line = file.readline()
        return new_data
    except OSError as error:
        print(error),sys.exit()
    except ValueError as error:
        print(error),sys.exit()


"""Function use to make data become adjacency matrix, put all possible time into list"""
def graph_matrix(num_vertices, graph):
    make_matrix = [[0 for column in range(num_vertices)] for row in range(num_vertices)] # make a matrix by number of vertices
    for time in graph:
        for column in range(len(make_matrix)):
            for row in range(len(make_matrix)):
                if time[0] == column and time[1] == row and make_matrix[column][row] == 0:
                    make_matrix[column][row] = [(time[2], time[3])]
                elif time[0] == column and time[1] == row and make_matrix[column][row] != 0:
                    make_matrix[column][row].append((time[2], time[3]))
    for column in range(len(make_matrix)):
        for row in range(len(make_matrix)):
            try:
                make_matrix[column][row] = sorted(make_matrix[column][row], key=lambda x: x[0])  # sorted the time by departure time
            except TypeError:
                pass
    return make_matrix


"""Function use to Dijkstra's to find the best path between the
    start city and destination city"""
def dijkstra(num_vertices, graph, source, destination):
    arrival_time = [sys.maxsize] * num_vertices
    use_vertex = [i for i in range(num_vertices)]
    list_path = [-1] * num_vertices
    arrival_time[source] = 0
    min_size = sys.maxsize   # make the size become the infinite
    min_index = -1

    while use_vertex:
        for i in range(num_vertices):
            if arrival_time[i] < min_size and i in use_vertex:
                min_size = arrival_time[i]
                min_index = i
                
        try:  # try to remove the use vertex,
            use_vertex.remove(min_index)  
        except ValueError:  # error is for already find the best path or city can not reach
            break
        
        for i in range(num_vertices):
            if graph[min_index][i] and i in use_vertex:
                for time in range(len(graph[min_index][i])):  # First, compare the departure is the earliest(small) time
                    if arrival_time[i] > graph[min_index][i][time][1] and arrival_time[min_index] < \
                            graph[min_index][i][time][0]: # Second,compare the time between departure time and arrival time
                        arrival_time[i] = graph[min_index][i][time][1]  # if the time is not conflict
                        list_path[i] = min_index                 # then update the time(earliest one) and the city path
        min_size = sys.maxsize
        min_index = -1

    arrival_path(arrival_time, list_path, source, destination)


"""Function use to print the path result and final arrival time"""
def arrival_path(arrival_time, list_path, source, destination):
    if arrival_time[destination] != sys.maxsize:
        path_list = []
        path = destination
        print("\nOptimal route from", source, "to", destination, "\n")
        while path != -1:
            path_list.append(path)  # get the path list back
            path = list_path[path]
        path_list.reverse()
        for i in range(len(path_list)):
            try:
                print("Fly from", path_list[i], "to", path_list[i + 1])
            except IndexError:
                break
        print("\nArrive at", destination, "at time", arrival_time[destination])
    else:
        print("There is no route from the specified start city to the specified end city")  # if city cannot reach


if __name__ == '__main__':
    data = read_data()
    vertices, flight_data = data[0][0], data[1:]
    matrix = graph_matrix(vertices, flight_data)
    dijkstra(vertices, matrix, source=87, destination=57)  
