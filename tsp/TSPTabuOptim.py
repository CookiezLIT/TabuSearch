import random

from tabusearch.TabuSearch import TabuSearch
from math import sqrt
from operator import itemgetter


class TSPTabuOptim(TabuSearch):
    def __init__(self, maxItterations, maxTabu):
        super().__init__()
        self.coordinates = []
        self.data = []
        self.noCities = 0
        self.cities = []
        self.memory = []
        self.itterations_count = 0
        self.tabu_count = 0
        self.maxTabu = maxTabu
        self.max_iterations = maxItterations
        self.best_fitness = float("Inf")

    def read_data(self):
        lineNo = 1
        f = open('../data/eil76.tsp')
        for line in f:
            if lineNo > 6:
                line = line.strip('\n')
                elements = line.split(' ')
                if elements != ['EOF']:
                    city = int(elements[0])
                    if city > self.noCities:
                        self.noCities = city
                    x_coord = int(elements[1])
                    y_coord = int(elements[2])
                    self.coordinates.append([city,x_coord,y_coord])
            lineNo += 1
        #coordinates conaints a list of triples: city, x_coord, y_coord

    def calculate_distances(self):
        for i in self.coordinates:
            for j in self.coordinates:
                if i != j:
                    distance = int(sqrt((i[1]-j[1])**2 + (i[2]-j[2])**2))
                    self.data.append([i[0],j[0],distance])
                    #euclidian distance for 2d points
                    #self.data contains list of [city1, city2, distance] and the reverse edges
        i = 1
        for i in range(self.noCities):
            self.data.append([i,i,150000])


    def initial_solution(self):
        """
        Greedy algorithm to get an initial solution (closest-neighbour).
        """
        self.cities = [i + 1 for i in range(self.noCities)]
        cur_node = random.choice(self.cities)  # start from a random node
        solution = [cur_node]

        free_nodes = set(self.cities)
        free_nodes.remove(cur_node)
        while free_nodes:
            next_node = min(free_nodes, key=lambda x: self.find_edge(cur_node,x))  # nearest neighbour
            free_nodes.remove(next_node)
            solution.append(next_node)
            cur_node = next_node

        cur_fit = self.calculate_cost(solution)
        if cur_fit < self.best_fitness:  # If best found so far, update best fitness
            self.best_fitness = cur_fit
            self.best_solution = solution

    def find_edge(self,c1,c2):
        for i in self.data:
            if i[0] == c1 and i[1] == c2:
                return i

    def init_memory(self):
        pass


    def update_memory(self, solution):
        pass


    def getBestNeighbours(self, solution):
        neighbours = []
        i = 2
        for i in range(len(self.cities)-2):
            j = i + 1
            for j in range(len(self.cities)-1):
                aux = self.cities.copy()
                aux[i] = self.cities[j]
                aux[j] = self.cities[i]
                if self.calculate_cost(aux) < self.calculate_cost(self.cities):
                    neighbours.append(aux)
        return neighbours

    def update_best(self, solution):
        pass


    def calculate_cost(self, solution):
        #print(solution)
        cost = 0
        i = 2
        for i in range(len(solution)):
            cost = cost + self.find_edge(solution[i-1],solution[i])[2]
        cost = cost + self.find_edge(solution[len(solution)-1],1)[2]
        return cost


    def run_all(self):
        self.read_data()
        self.calculate_distances()
        self.initial_solution()
        print(self.calculate_cost(self.cities))
        while self.itterations_count < self.max_iterations:
            neighbours = self.getBestNeighbours("")
            best_neighbour = neighbours[0]
            neighbour = 0
            for neighbour in range(len(neighbours)):
                #print(neighbour)
                if self.calculate_cost(neighbours[neighbour]) < self.calculate_cost(best_neighbour):
                    best_neighbour = neighbours[neighbour]
            if best_neighbour not in self.memory:
                if self.calculate_cost(best_neighbour) < self.calculate_cost(self.cities):
                    self.cities = best_neighbour
                    if self.tabu_count < self.maxTabu:
                        self.memory.append(best_neighbour)
                    else:
                        self.memory.pop(0)
                        self.memory.append(best_neighbour)
            self.itterations_count+=1
            #print(self.itterations_count)
            print(self.calculate_cost(self.cities))

x = TSPTabuOptim(100,4)
x.run_all()