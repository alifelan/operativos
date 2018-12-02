from collections import deque
from .memory import Memory
from .proceso import Process
from math import ceil, floor

class System:

    # Creates our system with the values sent from the client
    def __init__(self, s: str, mm: str, q: float, rm: int, sm: int, p: int):
        self.scheduling = s
        self.memoryType = mm
        self.quantum = q
        self.pageSize = p
        self.pid = 1
        self.quantumVal = 0
        self.process = deque()
        self.memory = Memory(rm, sm, self.pageSize)

    # Creates process, s is the process size in bytes
    def createProcess(self, s: int):
        pages = ceil(s / self.pageSize)
        pageNumber = [0] * pages
        pageLoaded = [False] * pages
        pageTable = {'pageLoaded': pageLoaded, 'pageNumber': pageNumber}
        process = Process(self.pid, s, pageTable)
        try:
            self.memory.loadProcessPage(process, 0)
            self.process.append(process)
            self.pid = self.pid + 1
            print('Process created')
        except ValueError as err:
            try:
                self.memory.swapAndLoadPage(process, 0, self.process[self.process.index(int(float(err.args[0])))])
                self.process.append(process)
                self.pid = self.pid + 1
                print('Process created')
            except:
                print('Not enough memory')
                return "Process {} not created".format(self.pid)
        return "Process {} created with size {}".format(self.pid - 1, s)

    def getProcess(self, pid):
        try:
            i = self.process.index(pid)
            return self.process[i]
        except ValueError:
            return None

    # Returns real address of process pid at v
    def getAddress(self, pid, v):
        try:
            process = self.process[self.process.index(pid)]
        except:
            return "{} not executing".format(pid)
        if process.addressInProcess(v):
            return "Address {} outside of process {}".format(v, pid)
        try:
            add = process.getRealAddress(v, self.pageSize, self.memory.getRealMemorySize())
        except NameError:
            try:
                self.memory.loadProcessPage(process, floor(v / self.pageSize))
            except ValueError as err:
                self.memory.swapAndLoadPage(process, floor(v / self.pageSize), self.process[self.process.index(int(float(err.args[0])))])
            add = process.getRealAddress(v, self.pageSize, self.memory.getRealMemorySize())
        except ValueError:
            self.memory.swapPages(process, floor(v / self.pageSize), self.process[self.process.index(self.memory.getMRUPID())])
            add = process.getRealAddress(v, self.pageSize, self.memory.getRealMemorySize())
        self.memory.accessedPage(ceil(process.getMemoryPage(floor(v / self.pageSize)) / self.pageSize))
        return "Real address: {}".format(add)


    # Adds quantum to current process
    def quantum(self):
        p = self.process.popleft()
        self.process.append(p)
        return "Quantum end"

    # Kills pid
    def fin(self, pid):
        self.memory.clearPages(self.process[self.process.index(pid)].getPageList(self.pageSize))
        print("Process {} ended".format(pid))

    # Ends simulation
    def end(self):
        pass

    def printMemory(self):
        self.memory.printMemory()


if __name__ == "__main__":
    s = System('rr', 'mru', 1, 4096, 2048, 1024)
    s.createProcess(2048)
    s.getAddress(1, 1045)
    s.printMemory()
    s.createProcess(1024)
    s.getAddress(2, 1023)
    s.createProcess(2048)
    s.printMemory()
    s.createProcess(2048)
    s.createProcess(2048)
    s.printMemory()
    s.fin(1)
    s.printMemory()
    s.createProcess(2048)
    s.createProcess(2048)
    s.printMemory()
