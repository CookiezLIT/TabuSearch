class KnapSackDataGenerator:
    '''
    primeste ca si argument file,
    daca este False, se vor folosi datele din program
    daca este True, in fileName se va specifica calea spre fisierul de unde se vor citi datele
    metoda getData returneaza datele, de ori unde ar fi ele citite
    '''
    def __init__(self,file,fileName=False):
        self.file = file
        self.fileName = fileName
        self.data = [[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[8,9],[9,10]] #date in memorie


    def getData(self):
        maxWeight = 20
        if self.file == False: #daca nu citim din fisier
            return maxWeight,self.data
        if self.file == True:#datele in fisier sunt de forma valoare' 'greutate, despartite pe linii diferite
            f = open(self.fileName,'r')
            aux = []#vectorul in care vom insera valorile si greutatile citite
            count = 1
            totalItems = 0
            maxWeight = 0
            for x in f:
                if count == 1: #daca citim prima linie
                    totalItems = int(x)
                    count = count + 1
                elif count == totalItems+2:#daca suntem pe ultima linie
                    maxWeight = int(x)
                else:
                    count = count + 1
                    numbers = x.split() #despartimim linia dupa spatii
                    number1 = int(numbers[1])#fitness
                    number2 = int(numbers[2])#weight
                    aux.append([number1,number2])#cand inseram, respectam forma declarata
            self.data = aux
            return maxWeight,self.data

