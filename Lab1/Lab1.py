""" Lab 1  Dijkstra's Algortithm """


import sys

def read_data():
    graph = []
    try:
        file = open("Dijkstra_Data_6.txt", "r")
        data = file.readline()
        size = int(data)
        while len(data) > 0:
            if "\t" in data:
                data = data.split("\t")[0:-1]
            else:
                data = data.split(" ")[0:-1]
            graph.append([int(num) for num in data])
            data = file.readline()

    except OSError as error:
        print(error)
        exit()
    except ValueError as error:
        print(error)
        exit()

    return size, graph[1:]


def dijkstra(vertices, graph, source):

    distlist = [sys.maxsize] * vertices

    useV = [False] * vertices

    distlist[source] = 0            # min_index = 0, 0

    mim_size = sys.maxsize

    for i in range(vertices):

        for v in range(vertices):
            if distlist[v] < mim_size and useV[v] == False:
                mim_size = distlist[v]
                mim_index = v
                # print(mim_index)

        print(distlist)
        print(mim_index)

        useV[mim_index] = True
        mim_size = sys.maxsize



        for v in range(vertices):
            if graph[mim_index][v] > 0 and useV[v] == False and distlist[v] > distlist[mim_index] + graph[mim_index][v]:
                distlist[v] = distlist[mim_index] + graph[mim_index][v]



    for i in range(vertices):
        print("From", source, "to", i, "is", distlist[i])



def main():
    vertices, graph = read_data()
    dijkstra(vertices, graph, 0)



if __name__ == '__main__':
    print()
    main()
