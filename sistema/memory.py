from math import ceil

class Memory:
    def __init__(self, realMemorySize, swapMemorySize, pageSize):
        self.realMemory = RealMemory(realMemorySize, pageSize)
        self.swapMemory = SwapMemory(swapMemorySize, pageSize, self.realMemory.getPages())
        self.pageSize = pageSize

    def storeProcess(self, process, processPage):
        if self.realMemory.freePages() or self.swapMemory.freePages():
            self.realMemory.setPage(process, self.swapMemory, processPage, self.pageSize)
        else:
            raise NameError('NotEnoughMemory')

    def printMemory(self):
        self.realMemory.printMemory()
        self.swapMemory.printMemory()


class SwapMemory:
    def __init__(self, memorySize, pageSize, pageLen):
        self.pages = ceil(memorySize / pageSize) * [0]
        self.pageLen = pageLen

    def storePage(self, process, processPage, pageSize):
        try:
            i = self.pages.index(0)
            self.pages[i] = process.getPID()
            process.pageSwapped(process.getPageNumber(processPage), (self.pageLen + i) * pageSize)
        except ValueError:
            pass

    def freePages(self):
        try:
            self.pages.index(0)
            return True
        except ValueError:
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
        try:
            i = self.pages.index(0)
            self.pages[i] = process.getPID()
            process.pageLoaded(processPage, i * pageSize)
        except ValueError:
            i = self.mfu.index(max(mfu))
            swap.storePage(System.getProcess(pages[i]), i, pageSize)
            self.pages[i] = process.getPID()
            self.mfu[i] = 0
            process.pageLoaded(processPage, i * pageSize)

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
        for val in self.pages:
            print(val)
