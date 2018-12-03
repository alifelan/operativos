from math import ceil

class Memory:
    # Creates memory, having the real memory size, swap memory size and page size
    def __init__(self, realMemorySize, swapMemorySize, pageSize):
        self.realMemory = RealMemory(realMemorySize, pageSize) # Real memory object
        self.swapMemory = SwapMemory(swapMemorySize, pageSize, self.realMemory.getPages()) # Swap memory object
        self.pageSize = pageSize # Page size

    # Tries to load a page on real memory, if it cant it raises ValueError to get process with the MFUPID
    def loadProcessPage(self, process, processPage):
        if self.realMemory.freePages():
            self.realMemory.setPage(process, processPage, self.pageSize)
        else:
            raise ValueError(self.realMemory.getMFUPID())

    # Tries to swap page from real memory and load received page. Raises NameError if theres not enough memory
    def swapAndLoadPage(self, process1, processPage, process2):
        if self.swapMemory.freePages():
            self.realMemory.setAndSwapPage(process1, self.swapMemory, processPage, self.pageSize, process2)
        else:
            raise NameError("Not enough memory")

    # Calls print on each memory
    def printMemory(self):
        self.realMemory.printMemory()
        self.swapMemory.printMemory()

    # Returns real memory state as a string
    def getRealString(self):
        return self.realMemory.getString()

    # Returns swap memory state as a string
    def getSwapString(self):
        return self.swapMemory.getString()

    # Returns both strings
    def getString(self):
        return [self.realMemory.getString(), self.swapMemory.getString()]

    # Returns ammount of pages on real memory
    def getRealMemorySize(self):
        return self.realMemory.getPages()

    # Swaps pages between real and swap memory
    def swapPages(self, process1, processPage, process2):
        self.realMemory.swapPages(process1, self.swapMemory, processPage, self.pageSize, process2)

    # Adds one to the counter of the accessed page
    def accessedPage(self, pageNumber):
        self.realMemory.accessedPage(pageNumber)

    # Returns the process id of the most frequently used page
    def getMFUPID(self):
        return self.realMemory.getMFUPID()

    # Clears pages that are in the received list
    def clearPages(self, pageList):
        for page in pageList:
            if page < self.realMemory.getPages():
                self.realMemory.clear(page)
            else:
                self.swapMemory.clear(page - self.realMemory.getPages())


class SwapMemory:
    # Starts swap memory with its size, page size and lenght of real memory
    def __init__(self, memorySize, pageSize, pageLen):
        self.pages = ceil(memorySize / pageSize) * [0] # Pages of swap
        self.pageLen = pageLen # Size of real memory, swap memory pages starts after real

    # Store page on swap
    def storePage(self, process, processPage, pageSize):
        i = self.pages.index(0)
        self.pages[i] = str(process.getPID()) + "." + str(processPage)
        process.pageSwapped(processPage, (self.pageLen + i) * pageSize)

    # Swaps a process page with another process
    def storePageOnNumber(self, process, processPage, pageSize, swapPage, realSize):
        self.pages[swapPage - realSize] = str(process.getPID()) + "." + str(processPage)
        process.pageSwapped(process.getPageNumber(processPage), (swapPage) * pageSize)

    # Returns true if there are free pages
    def freePages(self):
        for page in self.pages:
            if page == 0: return True
        return False

    # Clears a page
    def clear(self, page):
        self.pages[page] = 0

    # Prints memory state
    def printMemory(self):
        print("Swap memory")
        for i, val in enumerate(self.pages):
            if val == 0:
                print(str(i) + ":L")
            else:
                print(str(i) + ":" + str(val))

    # Returns memory state as a string
    def getString(self):
        s = ""
        for i, val in enumerate(self.pages):
            if val == 0:
                s = s + str(i) + ":L; "
            else:
                s = s + str(i) + ":" + str(val) + "; "
        return s[:-1]


class RealMemory:
    # Starts real memory
    def __init__(self, memorySize, pageSize):
        self.pages = ceil(memorySize / pageSize) * [0] # Starts pages
        self.mfu = [0] * ceil(memorySize / pageSize) # Starts mfu
        self.memorySize = ceil(memorySize / pageSize) # Sets its size in pages

    # Sets a free page with received page
    def setPage(self, process, processPage, pageSize):
        i = self.pages.index(0)
        self.pages[i] = str(process.getPID()) + "." + str(processPage)
        process.pageLoaded(processPage, i * pageSize)

    # Moves the most frequently used page to swap, and stores what it received in real memory
    def setAndSwapPage(self, process1, swap, processPage, pageSize, process2):
        i = self.mfu.index(max(self.mfu))
        s = self.pages[i]
        swap.storePage(process2, int(s[s.index(".")+1:]), pageSize)
        self.pages[i] = str(process1.getPID()) + "." + str(processPage)
        self.mfu[i] = 0
        process1.pageLoaded(processPage, i * pageSize)

    # Returns most frequently used process id
    def getMFUPID(self):
        return self.pages[self.mfu.index(max(self.mfu))]

    # Checks if there are free pages on real memory
    def freePages(self):
        try:
            self.pages.index(0)
            return True
        except ValueError:
            return False

    # Clears received page
    def clear(self, page):
        self.pages[page] = 0

    # Returns lenght of real memory in pages
    def getPages(self):
        return len(self.pages)

    # Swaps pages with swap memory
    def swapPages(self, process1, swap, processPage, pageSize, process2):
        i = self.mfu.index(max(self.mfu))
        s = self.pages[i]
        swap.storePageOnNumber(process2, int(s[s.index(".")+1:]), pageSize, process1.getMemoryPage(), self.memoryPage)
        self.pages[i] = str(process1.getPID()) + "." + str(processPage)
        self.mfu[i] = 0
        process1.pageLoaded(processPage, i * pageSize)

    # Adds one to the counter of the accessed page
    def accessedPage(self, pageNumber):
        self.mfu[pageNumber] = self.mfu[pageNumber] + 1

    # Prints its state
    def printMemory(self):
        print("Real memory")
        for i, val in enumerate(self.pages):
            if val == 0:
                print(str(i) + ":L")
            else:
                print(str(i) + ":" + str(val))

    # Returns state as a string
    def getString(self):
        s = ""
        for i, val in enumerate(self.pages):
            if val == 0:
                s = s + str(i) + ":L; "
            else:
                s = s + str(i) + ":" + str(val) + "; "
        return s[:-1]
