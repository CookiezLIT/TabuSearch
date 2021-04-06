#no iterations
#tabu[i,j]

class TabuSearch():
    def __init__(self):
        self.current_solution = None
        self.best_solution = None
        self.memory = [] #tabu solutions will be stored here
        self.memory_size = 0
        self.iteration_count = 0
        self.max_iterations = 0

    def initial_solution(self):
        pass

    def init_memory(self):
        pass

    def update_memory(self, solution):
        pass

    def getBestNeighbours(self, solution):
        pass

    def update_best(self, solution):
        pass

    def calculate_cost(self, solution):
        pass

    def run_all(self):
        pass