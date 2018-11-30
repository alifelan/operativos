class Process:

    # Creates the object
    def __init__(self, pid, size, pageTable):
        self.pid = pid
        self.size = size
        self.pageTable = pageTable

    def getRealAddress(self, vadd, pageSize):
        return self.pageTable['pageNumber'][vadd / pageSize] | (vadd % pageSize)

    def pageLoaded(self, processPage, memoryPage):
        self.pageTable['pageLoaded'][processPage] = True
        self.pageTable['pageNumber'][processPage] = memoryPage

    def pageSwapped(self, processPage, memoryPage):
        self.pageTable['pageLoaded'][processPage] = False
        self.pageTable['pageNumber'][processPage] = memoryPage

    def getPageNumber(self, memoryPage):
        return self.pageTable['pageNumber'].index(memoryPage)

    def __eq__(self, pid):
        return self.pid == pid

    def getPID(self):
        return self.pid
