import math
import random

class SimulatedAnnealing(object):
    def __init__(self, filename, T=1, alpha=1, stopping_T=-1, max_itterations=-1):
        self.N = 0
        self.T = T
        self.initialT = self.T
        self.alpha = alpha
        if stopping_T == -1:
            self.stopping_temperature = 1e-8
        else:
            self.stopping_temperature = stopping_T
        if max_itterations == -1:
            self.max_itterations = 100000
        else:
            self.max_itterations = max_itterations
        self.iteration = 1
        self.nodes = []
        self.best_solution = None
        self.best_fitness = float("Inf")
        self.filename = filename

    def read_file(self,filename):
        coordinates = []
        lineNo = 1
        with open(filename, "r") as f:
            noCities = 0
            for line in f:
                if lineNo > 6:
                    line = line.strip('\n')
                    elements = line.split(' ')
                    if elements != ['EOF']:
                        city = int(elements[0])
                        if city > noCities:
                            noCities = city
                        x_coord = int(elements[1])
                        y_coord = int(elements[2])
                        coordinates.append([city, x_coord, y_coord])
                lineNo += 1
        return coordinates

    def initial_solution(self):
        '''
        alegem random un oras, apoi adaugam orasul cu cea mai apropiata distanta pana la el
        facem asta pentru fiecare oras nou adaugat, pana nu mai este niciun oras neadaugat
        :return:solutia, fitnesul solutiei initiale
        '''
        selected = random.choice(self.nodes)#orasul ales random
        solution = [selected] #solution va contine solutia initiala a oraselor
        unused = self.nodes.copy()
        unused.remove(selected)#scoatem orasul initial din nodurile nevizitate
        while unused:#cat timp mai avem orase nevizitate
            next_node = min(unused, key=lambda x: self.dist(selected, x))#alegem orasul cel mai apropiat de cel curent
            #actualizam variabilele
            unused.remove(next_node)
            solution.append(next_node)
            selected = next_node
        #initializam solutia initiala si fitness-ul curent
        cur_fit = self.fitness(solution)
        if cur_fit < self.best_fitness:
            self.best_fitness = cur_fit
            self.best_solution = solution
        return solution, cur_fit

    def dist(self, city1, city2):
        '''
        calculam distanta dintre doua orase
        '''
        x, y = self.coords[city1], self.coords[city2]
        return int(math.sqrt((x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2))

    def fitness(self, solution):
        '''
        calculam costul solutiei actuale,
        nu uitam sa calculam si distanta de la ultimul oras la primul!!!
        '''
        cur_fit = 0
        for i in range(self.N):
            cur_fit += self.dist(solution[i % self.N], solution[(i + 1) % self.N])
        return cur_fit

    def probability(self, current_cost):
        '''
        calculam probabilitatea de a alege un nou best_candidate
        '''
        return math.exp(-abs(current_cost - self.cur_fitness) / self.T)

    def verify(self, candidate):
        '''
        verificam daca solutia curenta este mai buna decat cea mai buna
        de pana acum
        '''
        current_cost = self.fitness(candidate)
        if current_cost < self.cur_fitness:
            self.cur_fitness, self.cur_solution = current_cost, candidate
            if current_cost < self.best_fitness:
                self.best_fitness, self.best_solution = current_cost, candidate
        else:
            if random.random() < self.probability(current_cost):
                self.cur_fitness, self.cur_solution = current_cost, candidate

    def anneal(self):
        '''
        algoritmul pentru simulated annealing, conform celui din curs
        '''
        self.cur_solution, self.cur_fitness = self.initial_solution()
        while self.T >= self.stopping_temperature and self.iteration < self.max_itterations:
            candidate = list(self.cur_solution)
            # 2-opt
            l = random.randint(2, self.N - 1)
            i = random.randint(0, self.N - l)
            candidate[i : (i + l)] = reversed(candidate[i : (i + l)])
            self.verify(candidate)
            self.T *= self.alpha
            self.iteration += 1


    def run_all(self, n):
        '''
        rulam simulated annealing de n ori
        '''
        self.coords = self.read_file(self.filename)
        self.N = len(self.coords)
        self.nodes = [i for i in range(self.N)]
        for i in range(1, n + 1):
            print(f"Rulare {i}, cea mai buna solutie este:")
            self.T = self.initialT
            self.iteration = 1
            self.cur_solution, self.cur_fitness = self.initial_solution()
            self.anneal()
            print(self.fitness(self.best_solution))
            print(f"Solutia curenta: {i}")
            print(self.cur_solution)


sa = SimulatedAnnealing("../data/eil76.tsp", max_itterations=5000,T=1,alpha=0.994)
sa.run_all(200)