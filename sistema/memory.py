from math import ceil

class Memory:
    def __init__(self, realMemorySize, swapMemorySize, pageSize):
        self.realMemory = RealMemory(realMemorySize, pageSize)
        self.swapMemory = SwapMemory(swapMemorySize, pageSize, self.realMemory.getPages())
        self.pageSize = pageSize

    def loadProcessPage(self, process, processPage):
        if self.realMemory.freePages():
            self.realMemory.setPage(process, processPage, self.pageSize)
        else:
            raise ValueError(self.realMemory.getMRUPID())

    def swapAndLoadPage(self, process1, processPage, process2):
        if self.swapMemory.freePages():
            self.realMemory.setAndSwapPage(process1, self.swapMemory, processPage, self.pageSize, process2)
        else:
            raise NameError("Not enough memory")

    def printMemory(self):
        self.realMemory.printMemory()
        self.swapMemory.printMemory()

    def getRealString(self):
        return self.realMemory.getString()

    def getSwapString(self):
        return self.swapMemory.getString()

    def getString(self):
        return [self.realMemory.getString(), self.swapMemory.getString()]

    def getRealMemorySize(self):
        return self.realMemory.getPages()

    def swapPages(self, process1, processPage, process2):
        self.realMemory.swapPages(process1, self.swapMemory, processPage, self.pageSize, process2)

    def accessedPage(self, pageNumber):
        self.realMemory.accessedPage(pageNumber)

    def getMRUPID(self):
        return self.realMemory.getMRUPID()

    def clearPages(self, pageList):
        for page in pageList:
            if page < self.realMemory.getPages():
                self.realMemory.clear(page)
            else:
                self.swapMemory.clear(page - self.realMemory.getPages())


class SwapMemory:
    def __init__(self, memorySize, pageSize, pageLen):
        self.pages = ceil(memorySize / pageSize) * [0]
        self.pageLen = pageLen

    def storePage(self, process, processPage, pageSize):
        i = self.pages.index(0)
        self.pages[i] = str(process.getPID()) + "." + str(processPage)
        process.pageSwapped(processPage, (self.pageLen + i) * pageSize)

    def storePageOnNumber(self, process, processPage, pageSize, swapPage, realSize):
        self.pages[swapPage - realSize] = str(process.getPID()) + "." + str(processPage)
        process.pageSwapped(process.getPageNumber(processPage), (swapPage) * pageSize)

    def freePages(self):
        for page in self.pages:
            if page == 0: return True
        return False

    def clear(self, page):
        self.pages[page] = 0

    def printMemory(self):
        print("Swap memory")
        for i, val in enumerate(self.pages):
            if val == 0:
                print(str(i) + ":L")
            else:
                print(str(i) + ":" + str(val))

    def getString(self):
        s = ""
        for i, val in enumerate(self.pages):
            if val == 0:
                s = s + str(i) + ":L; "
            else:
                s = s + str(i) + ":" + str(val) + "; "
        return s[:-1]


class RealMemory:
    def __init__(self, memorySize, pageSize, ):
        self.pages = ceil(memorySize / pageSize) * [0]
        self.mfu = [0] * ceil(memorySize / pageSize)
        self.memorySize = ceil(memorySize / pageSize)

    def setPage(self, process, processPage, pageSize):
        i = self.pages.index(0)
        self.pages[i] = str(process.getPID()) + "." + str(processPage)
        process.pageLoaded(processPage, i * pageSize)

    def setAndSwapPage(self, process1, swap, processPage, pageSize, process2):
        i = self.mfu.index(max(self.mfu))
        s = self.pages[i]
        swap.storePage(process2, int(s[s.index(".")+1:]), pageSize)
        self.pages[i] = str(process1.getPID()) + "." + str(processPage)
        self.mfu[i] = 0
        process1.pageLoaded(processPage, i * pageSize)

    def getMRUPID(self):
        return self.pages[self.mfu.index(max(self.mfu))]

    def freePages(self):
        try:
            self.pages.index(0)
            return True
        except ValueError:
            return False

    def clear(self, page):
        self.pages[page] = 0

    def getPages(self):
        return len(self.pages)

    def swapPages(self, process1, swap, processPage, pageSize, process2):
        i = self.mfu.index(max(self.mfu))
        s = self.pages[i]
        swap.storePageOnNumber(process2, int(s[s.index(".")+1:]), pageSize, process1.getMemoryPage(), self.memoryPage)
        self.pages[i] = str(process1.getPID()) + "." + str(processPage)
        self.mfu[i] = 0
        process1.pageLoaded(processPage, i * pageSize)

    def accessedPage(self, pageNumber):
        self.mfu[pageNumber] = self.mfu[pageNumber] + 1

    def printMemory(self):
        print("Real memory")
        for i, val in enumerate(self.pages):
            if val == 0:
                print(str(i) + ":L")
            else:
                print(str(i) + ":" + str(val))

    def getString(self):
        s = ""
        for i, val in enumerate(self.pages):
            if val == 0:
                s = s + str(i) + ":L; "
            else:
                s = s + str(i) + ":" + str(val) + "; "
        return s[:-1]
