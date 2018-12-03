from math import floor

class Process:

    # Creates the object
    def __init__(self, pid, size, pageTable):
        self.pid = pid
        self.size = size
        self.pageTable = pageTable
        self.cputime = 0
        self.waittime = 0

    def getRealAddress(self, vadd, pageSize, memoryPageSize):
        if not self.pageTable['pageLoaded'][floor(vadd / pageSize)]:
            raise NameError
        if self.pageTable['pageNumber'][floor(vadd / pageSize)] >= memoryPageSize * pageSize:
            raise ValueError
        return self.pageTable['pageNumber'][floor(vadd / pageSize)] | (vadd % pageSize)

    def pageLoaded(self, processPage, memoryPage):
        self.pageTable['pageLoaded'][processPage] = True
        self.pageTable['pageNumber'][processPage] = memoryPage

    def pageSwapped(self, processPage, memoryPage):
        self.pageTable['pageNumber'][processPage] = memoryPage

    def getPageNumber(self, memoryPage):
        return self.pageTable['pageNumber'].index(memoryPage)

    def getMemoryPage(self, page):
        return self.pageTable['pageNumber'][page]

    def getPageList(self, pageSize):
        pages = []
        for val, condition in zip(self.pageTable['pageNumber'], self.pageTable['pageLoaded']):
            if condition:
                pages.append(floor(val / pageSize))
        return pages

    def addressInProcess(self, add):
        return add >= self.size

    def addCPUTime(self, time):
        self.cputime = self.cputime + time

    def getCPUTime(self):
        return self.cputime

    def getTurnaround(self):
        return self.cputime + self.waittime

    def addWaitTime(self, time):
        self.waittime = self.waittime + time

    def getWaitTime(self):
        return self.waittime

    def __eq__(self, pid):
        return self.pid == pid

    def getPID(self):
        return self.pid
