from math import floor

class Process:

    # Creates the object
    def __init__(self, pid, size, pageTable):
        self.pid = pid # process id
        self.size = size # process size
        self.pageTable = pageTable # Page table, a dict that has  pageLoaded and pageNumber
        self.cputime = 0 # Process time on the cpu
        self.waittime = 0 # Process time waiting

    # Returns real address of virtual address. Raises error if the page is not loaded or not in the process
    def getRealAddress(self, vadd, pageSize, memoryPageSize):
        if not self.pageTable['pageLoaded'][floor(vadd / pageSize)]:
            raise NameError
        if self.pageTable['pageNumber'][floor(vadd / pageSize)] >= memoryPageSize * pageSize:
            raise ValueError
        return self.pageTable['pageNumber'][floor(vadd / pageSize)] | (vadd % pageSize)

    # Updates page table if the page is loaded
    def pageLoaded(self, processPage, memoryPage):
        self.pageTable['pageLoaded'][processPage] = True
        self.pageTable['pageNumber'][processPage] = memoryPage

    # Updates the table if the page is swapped
    def pageSwapped(self, processPage, memoryPage):
        self.pageTable['pageNumber'][processPage] = memoryPage

    # Returns process page number by checking the memory page its in
    def getPageNumber(self, memoryPage):
        return self.pageTable['pageNumber'].index(memoryPage)

    # Returns memory page by process page
    def getMemoryPage(self, page):
        return self.pageTable['pageNumber'][page]

    # Returns a list of pages used by the process
    def getPageList(self, pageSize):
        pages = []
        for val, condition in zip(self.pageTable['pageNumber'], self.pageTable['pageLoaded']):
            if condition:
                pages.append(floor(val / pageSize))
        return pages

    # Checks if the address is in the process
    def addressInProcess(self, add):
        return add >= self.size

    # Adds cpu time to the process
    def addCPUTime(self, time):
        self.cputime = self.cputime + time

    # Returns cpu time of the process
    def getCPUTime(self):
        return self.cputime

    # Returns turnaround time of the process
    def getTurnaround(self):
        return self.cputime + self.waittime

    # Adds waittime to the process
    def addWaitTime(self, time):
        self.waittime = self.waittime + time

    # Returns wait time of the process
    def getWaitTime(self):
        return self.waittime

    # Updates the equal function, to just check the process id
    def __eq__(self, pid):
        return self.pid == pid

    # Returns its process id
    def getPID(self):
        return self.pid
