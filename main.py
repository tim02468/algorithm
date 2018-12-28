class node():
    def __init__(self, stage, res, prof, prev):
        self.stage = stage
        self.res = res
        self.prof = prof
        self.prev = prev


class multiStageGraph():
    def __init__(self, numStage, resource):
        self.resource = resource
        self.numStage = numStage
        self.previousList = [0 for i in range(resource)]
        self.currentList = [0 for i in range(resource)]
        self.root = node(0, 0, 0, 0)
        self.endNode = node(self.numStage, self.resource, 0, 0)
    def buildGraph(self, classes):
        # stage 1 speical case
        for i in range(len(classes[0])):
            newNode = node(1, i+1, classes[0][i], self.root)
            self.previousList[i] = newNode
        
        # stage 2 etc
        for i in range(2, self.numStage):
            self.currentList = [0 for i in range(self.resource)]
            for j in range(i, self.resource):
                newNode = node(i, j, 0, 0)
                self.currentList[j-i] = newNode
                for k in range(j-i+1):
                    pastNode = self.previousList[k]
                    if pastNode == 0 or newNode.res - pastNode.res > 4:
                        continue
                    prof = classes[i-1][newNode.res - pastNode.res - 1]
                    cumProf = prof + pastNode.prof
                    if (cumProf >= newNode.prof):
                        newNode.prof = cumProf
                        newNode.prev = pastNode
            self.previousList = self.currentList.copy()
            
        
        # end node
        for i in self.previousList:
            if i == 0:
                continue
            prof = 0 if self.resource - i.res == 0 else classes[self.numStage-1][self.resource - i.res - 1]
            cumProf = i.prof + prof
            if cumProf >= self.endNode.prof:
                self.endNode.prof = cumProf
                self.endNode.prev = i


# input data
with open("input.txt") as f:
    inputFile = f.read().splitlines()

table = []

for index in range(len(inputFile)):
    line = inputFile[index]
    line = line.split(' ')
    
    # table
    if len(line) > 1:
        table.append([int(l) for l in line])
    
    if line[0] == '':
        if len(inputFile[index+1]) == 1 and type(int(inputFile[index+1][0])) == int:
            classes = list(map(list, zip(*table)))
            stage = len(classes)
            graph = multiStageGraph(stage, int(inputFile[index+1][0]))
            graph.buildGraph(classes)
            print(graph.endNode.prof)
        else:
            table = []
            del classes

            