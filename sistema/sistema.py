from time import time
from collections import deque
from .memory import Memory
from .proceso import Process
from math import ceil

class System:

    # Creates our system with the values sent from the client
    def __init__(self, s: str, mm: str, q: float, rm: int, sm: int, p: int):
        self.scheduling = s
        self.memory = mm
        self.quantum = q
        self.pageSize = p
        self.pid = 'A'
        self.process = deque()
        self.startTime = time()
        self.memory = Memory(rm, sm, self.pageSize)

    # Creates process, s is the process size in bytes
    def createProcess(self, s: int):
        pages = ceil(s / self.pageSize)
        pageNumber = [0] * pages
        pageLoaded = [False] * pages
        pageTable = {'pageLoaded': pageLoaded, 'pageNumber': pageNumber}
        try:
            process = Process(self.pid, s, pageTable)
            self.memory.storeProcess(process, 0)
            self.process.append(process)
            self.pid = chr(ord(self.pid) + 1)
            return 'Process created'
        except NameError:
            return 'Not enough memory'

    @staticmethod
    def getProcess(pid):
        try:
            i = self.process.index(pid)
            return self.process[i]
        except ValueError:
            return None


    # Returns virtual address of process pid at v
    def getAddress(self, pid, v):
        pass

    # Adds quantum to current process
    def quantum(self):
        pass

    # Kills pid
    def fin(self, pid):
        pass

    # Ends simulation
    def end(self):
        pass

    def printMemory(self):
        self.memory.printMemory()


if __name__ == "__main__":
    s = System('rr', 'mru', 1, 4096, 2048, 1024)
    s.createProcess(2048)
    s.createProcess(1024)
    s.printMemory()
