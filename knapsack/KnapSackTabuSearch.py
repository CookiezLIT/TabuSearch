from knapsack.KnapSackDataGenerator import KnapSackDataGenerator
from tabusearch.TabuSearch import TabuSearch
import random

class KnapSackTabuSearch(TabuSearch):
    def __init__(self, max_iterations, max_memory ,file, filename):
        super().__init__()
        self.best_value = 0
        self.best_weight = 0
        self.best_solution = []
        self.memory = [] #tabu solutions will be stored here|as list of lists
        self.memory_size = 0
        self.max_memory = max_memory
        self.iteration_count = 0
        self.max_iterations = max_iterations
        self.max_weight = 0
        self.data = [] #value/weight
        self.file = file
        self.fileName = filename

    def load_data(self):
        generator = KnapSackDataGenerator(self.file,self.fileName)
        (self.max_weight, self.data) = generator.getData()


    def initial_solution(self):#we generate a random valid solution to start with
        self.load_data()
        counter = 0
        self.current_solution = []
        self.best_weight = 0
        self.best_value= 0
        for i in self.data:
            current_choice = int(random.random() * 10) % 2 #we choose randomly if we select an object or not
            #current_choice = 0
            self.best_value = self.best_value + i[0] * current_choice
            self.best_weight = self.best_weight + i[1] * current_choice
            self.current_solution.append(current_choice)
            counter +=1

        if (self.best_weight > self.max_weight):
            self.initial_solution()
        else:
            print("Initial solution generated: " + str(self.current_solution))
            print("Initial solutiuon's weight " + str(self.best_weight))
            print("Initial solutions's value " + str(self.best_value))
            self.best_solution = self.current_solution
            self.best_value = self.calculate_cost(self.best_solution)
            return self.best_solution

    def init_memory(self):
        self.memory.append(self.best_solution)
        self.memory_size = 1


    def update_memory(self, solution):
        if self.memory_size < self.max_memory:
            self.memory.append(solution)
            self.memory_size += 1
        elif self.memory_size == self.max_memory:
            self.memory.pop(0)
            self.memory.append(solution)


    def getBestNeighbours(self, solution):
        all_solutions = []
        i = 0
        for i in range(len(solution)):
            best_aux = solution.copy()
            best_aux[i] = 1 - best_aux[i]
            all_solutions.append(best_aux)
        return all_solutions


    def update_best(self, solution):
        self.best_solution = solution
        self.best_value = self.calculate_cost(solution)
        self.best_weight = 0
        i = 0
        for i in range(len(solution)):
            self.best_weight += self.data[i][1] * solution[i]


    def calculate_cost(self, solution):
        value = 0
        sweight = 0
        i = 0
        for i in range(len(solution)):
            value = value + self.data[i][0] * solution[i]
            sweight = sweight + self.data[i][1] * solution[i]
        if sweight > self.max_weight:
            return 0
        else:
            return value



    def run_all(self):
        self.initial_solution()
        self.init_memory()
        self.iteration_count = 0
        best_candidate = self.best_solution
        while(self.iteration_count < self.max_iterations):
            neighbours = self.getBestNeighbours(best_candidate)
            ok = True
            while neighbours and ok == True:
                best_candidate = neighbours[0]
                for candidate in neighbours:
                    #print(self.calculate_cost(candidate))
                    if self.calculate_cost(candidate) >= self.calculate_cost(best_candidate):
                        if candidate not in self.memory:
                            best_candidate = candidate
                            ok = False
                        else:
                            #print(best_candidate)
                            best_candidate = candidate
                            neighbours.remove(best_candidate)

            if self.calculate_cost(best_candidate) > self.calculate_cost(self.best_solution):
                self.update_best(best_candidate)
                #print(self.calculate_cost(best_candidate))
            #print(best_candidate)
            self.update_memory(best_candidate)
            self.iteration_count += 1

        return (self.best_solution, self.best_value, self.best_weight)


x = KnapSackTabuSearch(1000,50,True,'../data/rucsac-200.txt')
(solution, value, weight) = x.run_all()

print()
print()

print('Final solution ' + str(solution))
print('Final weight ' + str(weight))
print('Final value: ' + str(value))