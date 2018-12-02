from math import floor

class Process:

    # Creates the object
    def __init__(self, pid, size, pageTable):
        self.pid = pid
        self.size = size
        self.pageTable = pageTable

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
        for val in self.pageTable['pageNumber']:
            if self.pageTable['pageLoaded']:
                pages.append(floor(val / pageSize))
        return pages

    def __eq__(self, pid):
        return self.pid == pid

    def getPID(self):
        return self.pid
