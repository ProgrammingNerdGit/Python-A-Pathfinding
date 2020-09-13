import sys
import time

searchNodeWorkers = []
ammOfWorkers = 0


def tupleAdd(a,b):
    return (a[0] + b[0],a[1]+b[1])

class ASGrid:
    def __init__(self,size):
        self.final = False
        self.finished = False
        self.size = size+1
        self.grid = {}
        self.rw = reverseWorker(self,(1,1))
    def setStart(self,pos):
        searchNodeWorkers.append(searchNode(self,pos,0,"start")) 
    def setEnd(self,pos):
        self.addValue(pos,"end")
        self.rw = reverseWorker(self,pos)
    def addBlocker(self,pos):
        self.addValue(pos,"block")
    def addValue(self,pos,type_,num=None,**kwargs):
        if("text" in kwargs.keys()):
            self.grid[pos] = (type_,num,kwargs.get("text"))
        else:
            self.grid[pos] = (type_,num)
    def path(self):
        return self.rw.path
    def getValue(self,pos):
        return self.grid.get(pos)
    def changeValue(self,pos,type_,num=None,**kwargs):
        if("text" in kwargs.keys()):
            self.grid[pos] = (type_,num,kwargs.get("text"))
        else:
            self.grid[pos] = (type_,num)
    def getNearTiles(self,tilePos):
        return [tupleAdd(tilePos,(1,0)),tupleAdd(tilePos,(0,1)),tupleAdd(tilePos,(-1,0)),tupleAdd(tilePos,(0,-1))]

    def run(self):
        running = True
        while running:
            
            if(not self.finished):
                for a in range(len(searchNodeWorkers)):
                    searchNodeWorkers[a].iterate()
            if(self.finished and not self.final):
                
                self.rw.iterate()
            if(self.final):
                
                running = False


class searchNode:
    def __init__(self,ASGrid,pos,value,type="node"):
        self.ASGrid = ASGrid
        self.pos = pos
        self.value = value
        self.type = type
        self.finished = False
        
    def getdata(self,pos):
        for j in searchNodeWorkers:
            if(pos == j.pos):
                return (j.value,j.type,j)
    def iterate(self):
        global ammOfWorkers
        ammOfWorkers += 1
        if(not self.finished):
            near = self.ASGrid.getNearTiles(self.pos)

            self.ASGrid.addValue(self.pos,self.type,self.value)
            for i in near:
                if(self.ASGrid.getValue(i) == None and i[0] >= 0 and i[1] >= 0 and i[0] <= self.ASGrid.size-1 and i[1] <= self.ASGrid.size-1):
                    poses = []
                    workerPoses = []
                    for j in searchNodeWorkers:
                        workerPoses.append(j.pos)
                    #checkIfDuplicates_1(j.pos)
                    if(i not in workerPoses):
                        poses.append(i)
                    for s in poses:
                        #print(self.ASGrid.getValue(i),i)
                        searchNodeWorkers.append(searchNode(self.ASGrid,s,self.value+1))
                elif(self.ASGrid.getValue(i) != None and self.ASGrid.getValue(i)[0] == "end"):
                    self.ASGrid.finished = True
            self.finished = True
            ammOfWorkers -= 1
        
class reverseWorker(searchNode):
    def __init__(self,ASGrid,pos):
        self.pos = pos
        self.ASGrid = ASGrid
        self.nextPos = pos
        self.path = []
    def iterate(self):
        
        near = self.ASGrid.getNearTiles(self.nextPos)
        vals = {}
        for i in near:
            if(self.ASGrid.getValue(i) != None and (self.ASGrid.getValue(i)[0] == "node" or self.ASGrid.getValue(i)[0] == "start" )):
                vals[i] = self.ASGrid.getValue(i)
        low = (sys.maxsize,(0,0))
        for i in vals.keys():
            #print(low[0],vals.get(i)[1])
            if(vals.get(i)[1] == 0):
                self.ASGrid.final = True
            if(low[0] >= vals.get(i)[1] and self.getdata(i) != None):
                low = (vals.get(i)[1],self.getdata(i)[2].pos)
        self.nextPos = low[1]
        self.ASGrid.changeValue(low[1],"path",0)
        self.path.append(low[1])
        
        if(self.ASGrid.final == True):
            self.path.reverse()  
            self.path.append(self.ASGrid.rw.pos)




if __name__ == "__main__":
    def run():
        grid = ASGrid(10)
        grid.addBlocker((1,0))
        grid.setStart((0,0))
        grid.setEnd((10,10))

        startTime = time.time()

        grid.run()

        print(time.time()-startTime)

        print(grid.path())

    run()
