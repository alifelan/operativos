from math import ceil


class Memory:
    def __init__(self, realMemorySize, swapMemorySize, pageSize):
        self.realMemory = RealMemory(realMemorySize, pageSize)
        self.swapMemory = SwapMemory(swapMemorySize, pageSize, self.realMemory.getPages())
        self.pageSize = pageSize

    def storeProcess(self, process, processPage):
        if self.realMemory.freePages():
            self.realMemory.setPage(process, self.swapMemory, processPage, self.pageSize)
        else:
            raise ValueError(self.realMemory.getMRUPID())

    def storeAndSwapProcess(self, process1, processPage, process2):
        if self.swapMemory.freePages():
            self.realMemory.setAndSwapPage(process1, self.swapMemory, processPage, self.pageSize, process2)
        else:
            raise NameError

    def printMemory(self):
        self.realMemory.printMemory()
        self.swapMemory.printMemory()


class SwapMemory:
    def __init__(self, memorySize, pageSize, pageLen):
        self.pages = ceil(memorySize / pageSize) * [0]
        self.pageLen = pageLen

    def storePage(self, process, processPage, pageSize):
        i = self.pages.index(0)
        self.pages[i] = str(i) + ":" + str(process.getPID()) + "." + str(processPage)
        process.pageSwapped(process.getPageNumber(processPage), (self.pageLen + i) * pageSize)

    def freePages(self):
        for page in self.pages:
            if page == 0: return True
        return False

    def printMemory(self):
        print("Swap memory")
        for val in self.pages:
            print(val)


class RealMemory:
    def __init__(self, memorySize, pageSize):
        self.pages = ceil(memorySize / pageSize) * [0]
        self.mfu = [0] * ceil(memorySize / pageSize)

    def setPage(self, process, swap, processPage, pageSize):
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

    def getPages(self):
        return len(self.pages)

    def printMemory(self):
        print("Real memory")
        for i, val in enumerate(self.pages):
            if val == 0:
                print(str(i) + ":L")
            else:
                print(str(i) + ":" + str(val))
