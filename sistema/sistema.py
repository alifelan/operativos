from collections import deque
from .memory import Memory
from .proceso import Process
from math import ceil, floor
from time import time
from tabulate import tabulate

class System:

    # Creates our system with the values sent from the client
    def __init__(self, s: str, mm: str, q: float, rm: int, sm: int, p: int):
        self.scheduling = s
        self.memoryType = mm
        self.quantumSize = q
        self.pageSize = p
        self.pid = 1
        self.quantumVal = 0
        self.process = deque()
        self.memory = Memory(rm, sm, self.pageSize)
        self.table = [["Comando", "Timestamp", "Dir real", "Cola listos", "CPU", "Memoria", "Swap", "Terminados"]]
        self.terminados = []
        self.timestamp = time()
        self.timer = 0
        self.pageFaults = 0
        self.pageVisits = 0

    def getCPU(self):
        if len(self.process) < 1: return ''
        return self.process[0].getPID()

    def getReady(self):
        if len(self.process) < 1: return ''
        return ','.join(str(i.getPID()) for i in list(self.process)[1:])

    def getTimestamp(self):
        return self.quantumSize * self.quantumVal + self.timer * self.quantumSize / 25

    def getTerminados(self):
        if len(self.terminados) < 1: return ''
        return ','.join(str(i.getPID()) for i in self.terminados)

    # Creates process, s is the process size in bytes
    def createProcess(self, s: int):
        self.timer = self.timer + 1
        pages = ceil(s / self.pageSize)
        pageNumber = [0] * pages
        pageLoaded = [False] * pages
        pageTable = {'pageLoaded': pageLoaded, 'pageNumber': pageNumber}
        process = Process(self.pid, s, pageTable)
        try:
            self.memory.loadProcessPage(process, 0)
            self.process.append(process)
            self.pid = self.pid + 1
        except ValueError as err:
            try:
                self.memory.swapAndLoadPage(process, 0, self.process[self.process.index(int(float(err.args[0])))])
                self.process.append(process)
                self.pid = self.pid + 1
            except:
                self.table.append(['create {}'.format(s), str(self.getTimestamp()), '', self.getReady(), self.getCPU(), self.memory.getRealString(), self.memory.getSwapString(), self.getTerminados()])
                self.pid = self.pid + 1
                return "<{}> Process {} not created".format(self.getTimestamp(), self.pid)
        self.table.append(['create {}'.format(s), str(self.getTimestamp()), '', self.getReady(), self.getCPU(), self.memory.getRealString(), self.memory.getSwapString(), self.getTerminados()])
        return "<{}> Process {} created with size {}".format(self.getTimestamp(), self.pid - 1, s)

    def getProcess(self, pid):
        try:
            i = self.process.index(pid)
            return self.process[i]
        except ValueError:
            return None

    # Returns real address of process pid at v
    def getAddress(self, pid, v):
        self.pageVisits = self.pageVisits + 1
        self.timer = self.timer + 1
        try:
            process = self.process[self.process.index(pid)]
        except:
            self.table.append(['Address {} {}'.format(pid, v), str(self.getTimestamp()), 'None', self.getReady(), self.getCPU(), self.memory.getRealString(), self.memory.getSwapString(), self.getTerminados()])
            return "<{}> {} not executing".format(self.getTimestamp(), pid)
        if process.addressInProcess(v):
            self.table.append(['Address {} {}'.format(pid, v), str(self.getTimestamp()), 'Page Fault', self.getReady(), self.getCPU(), self.memory.getRealString(), self.memory.getSwapString(), self.getTerminados()])
            self.pageFaults = self.pageFaults + 1
            return "<{}> Address {} outside of process {}".format(self.getTimestamp(), v, pid)
        try:
            add = process.getRealAddress(v, self.pageSize, self.memory.getRealMemorySize())
        except NameError:
            self.pageFaults = self.pageFaults + 1
            try:
                self.memory.loadProcessPage(process, floor(v / self.pageSize))
            except ValueError as err:
                try:
                    self.memory.swapAndLoadPage(process, floor(v / self.pageSize),
                                            self.process[self.process.index(int(float(err.args[0])))])
                except NameError:
                    self.table.append(['Address {} {}'.format(pid, v), str(self.getTimestamp()), 'None', self.getReady(), self.getCPU(), self.memory.getRealString(), self.memory.getSwapString(), self.getTerminados()])
                    return "<{}> Not enough memory".format(self.getTimestamp())
            add = process.getRealAddress(v, self.pageSize, self.memory.getRealMemorySize())
        except ValueError:
            self.pageFaults = self.pageFaults + 1
            self.memory.swapPages(process, floor(v / self.pageSize),
                                  self.process[self.process.index(self.memory.getMRUPID())])
            add = process.getRealAddress(v, self.pageSize, self.memory.getRealMemorySize())
        self.memory.accessedPage(ceil(process.getMemoryPage(floor(v / self.pageSize)) / self.pageSize))
        self.table.append(['Address {} {}'.format(pid, v), str(self.getTimestamp()), str(add), self.getReady(), self.getCPU(), self.memory.getRealString(), self.memory.getSwapString(), self.getTerminados()])
        return "<{}> Real address: {}".format(self.getTimestamp(), add)

    # Adds quantum to current process
    def quantum(self):
        self.timer = self.timer + 1
        if len(self.process) > 0:
            self.process[0].addCPUTime(self.quantumSize)
            for p in list(self.process)[1:]:
                p.addWaitTime(self.quantumSize)
            x = self.process.popleft()
            self.process.append(x)
        self.table.append(['Quantum', str(self.getTimestamp()), '', self.getReady(), self.getCPU(), self.memory.getRealString(), self.memory.getSwapString(), self.getTerminados()])
        self.quantumVal = self.quantumVal + 1
        self.timer = 0
        return "<{}> Quantum end".format(self.getTimestamp())

    # Kills pid
    def fin(self, pid):
        self.timer = self.timer + 1
        try:
            self.memory.clearPages(self.process[self.process.index(pid)].getPageList(self.pageSize))
            self.terminados.append(self.process[self.process.index(pid)])
            self.process.remove(pid)
        except ValueError:
            return "<{}> Process {} not running".format(self.getTimestamp(), pid)
            pass
        self.table.append(['Fin {}'.format(pid), str(self.getTimestamp()), '', self.getReady(), self.getCPU(), self.memory.getRealString(), self.memory.getSwapString(), self.getTerminados()])
        return "<{}> Process {} ended".format(self.getTimestamp(), pid)

    def getMetricas(self):
        output = [['Process', 'CPU time', 'Wait time', 'Turnaround']]
        for p in self.terminados:
            output.append([str(p.getPID()), str(p.getCPUTime()), str(p.getWaitTime()), str(p.getTurnaround())])
        return output

    def getRendimiento(self):
        return [['Visitas', 'Page faults', '% Page faults'], [str(self.pageVisits), str(self.pageFaults), str(self.pageFaults / self.pageVisits * 100)]]

    # Ends simulation
    def end(self):
        for p in self.process:
            fin(p.getPID())
        self.table.append(['End', str(self.getTimestamp()), '', self.getReady(), self.getCPU(), self.memory.getRealString(), self.memory.getSwapString(), self.getTerminados()])
        print(tabulate(self.table, tablefmt='fancy_grid'))
        print(tabulate(self.getMetricas(), tablefmt='fancy_grid'))
        print(tabulate(self.getRendimiento(), tablefmt='fancy_grid'))

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
