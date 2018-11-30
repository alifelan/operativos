from time import time

class System:

    # Creates our system with the values sent from the client
    def __init__(self, s, mm, q, rm, sm, p):
        self.scheduling = s
        self.memory = mm
        self.quantum = q
        self.realMemory = rm
        self.swapMemory = sm
        self.pageSize = p
        self.pid = 1
        self.process = {}
        self.startTime = time()

    # Creates process, s is the process size in bytes
    def createProcess(self, s):
        pass

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
