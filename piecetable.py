__author__ = "Prasenjit Kumar Shaw"
__copyright__ = "Copyright 2019, Prasenjit Kumar Shaw"
__license__ = "MIT"
__email__ = "shawprasenjit7@gmail.com"

class PieceTable:
    def __init__(self, originalContent):
        self.origBuff = originalContent
        self.addBuff = ''
        self.table = [{
                "add": False, # false means it points to origBuff, true means addBuff
                "startpos": 0,
                "length": len(self.origBuff)
            }]
        self.recivedCommands = []
        self.undoStack = []
        self.redoStack = []

    def resetBuffers(self):
        self.origBuff = self.getOutputText()
        self.addBuff = ''
        self.table = [{
                "add": False, # false means it points to origBuff, true means addBuff
                "startpos": 0,
                "length": len(self.origBuff)
            }]
        self.undoStack = []
        self.redoStack = []

    def undo(self):
        print("XXXXX Command Recieved: undo()")
        if len(self.undoStack):
            command = self.undoStack.pop()
            self.redoStack.append(command)
            self.table = command["initialTable"]
            
    def redo(self):
        print("XXXXX Command Recieved: redo()")
        if len(self.redoStack):
            command = self.redoStack.pop()
            self.undoStack.append(command)
            self.table = command["finalTable"]

    def __getPieceIndex(self, startpos):  # return piece index and offset within this piece
        offset = startpos
        for piece in self.table:
            if offset <= piece["length"]:
                return self.table.index(piece), piece["startpos"] + offset
            offset -= piece["length"]
        return 0, 0

    def insert(self, string, startpos):
        print("XXXXX Command Recieved: insert({0}, {1})".format(string, startpos))

        initialTable = []
        for piece in self.table:
            initialTable.append(piece)

        if len(string) == 0:
            return
        addBuffOffset = len(self.addBuff)
        self.addBuff += string
        pieceIndex, buffOffset = self.__getPieceIndex(startpos)
        piece = self.table[pieceIndex]
        if piece["add"] and buffOffset == (piece["startpos"] + piece["length"]) and addBuffOffset == (piece["startpos"] + piece["length"]):
            self.table[pieceIndex]["length"] += len(string)
            return
        
        piece1 = {
            "add": piece["add"],
            "startpos": piece["startpos"],
            "length": buffOffset - piece["startpos"]
        }
        piece2 = {
            "add": True,
            "startpos": addBuffOffset,
            "length": len(string)
        }
        piece3 = {
            "add": piece["add"],
            "startpos": buffOffset,
            "length": piece["length"] - (buffOffset - piece["startpos"])
        }

        self.table.pop(pieceIndex)
        if piece3["length"] > 0:
            self.table.insert(pieceIndex, piece3)
        if piece2["length"] > 0:
            self.table.insert(pieceIndex, piece2)
        if piece1["length"] > 0:
            self.table.insert(pieceIndex, piece1)

        finalTable = []
        for piece in self.table:
            finalTable.append(piece)

        command = {
            "type": "insert",
            "initialTable": initialTable,
            "finalTable": finalTable
        }

        self.undoStack.append(command)

    def delete(self, startpos, n_chars):
        if n_chars == 0:
            return
        if startpos < 0:
            return
        if n_chars < 0:
            return self.delete(startpos + n_chars, -n_chars)

        print("XXXXX Command Recieved: delete({0}, {1})".format(startpos, n_chars))

        initialTable = []
        for piece in self.table:
            initialTable.append(piece)

        initPieceIndex, initBuffOffset = self.__getPieceIndex(startpos)
        finalPieceIndex, finalBuffOffset = self.__getPieceIndex(startpos + n_chars)
        print("init index: {0}\t\tfinal index: {1}\t\t for deletion".format(initPieceIndex, finalPieceIndex))
        if initPieceIndex == finalPieceIndex:
            if initBuffOffset == self.table[initPieceIndex]["startpos"]:
                print("Deletion towards start of index {0}".format(initPieceIndex))
                self.table[initPieceIndex]["startpos"] += n_chars
                self.table[initPieceIndex]["length"] -= n_chars
                return
            elif finalBuffOffset == (self.table[initPieceIndex]["startpos"] + self.table[initPieceIndex]["length"]):
                print("Deletion towards end of index {0}".format(finalPieceIndex))
                self.table[initPieceIndex]["length"] -= n_chars
                return
        
        piece1 = {
            "add": self.table[initPieceIndex]["add"],
            "startpos": self.table[initPieceIndex]["startpos"],
            "length": initBuffOffset - self.table[initPieceIndex]["startpos"]
        }
        piece2 = {
            "add": self.table[finalPieceIndex]["add"],
            "startpos": finalBuffOffset,
            "length": self.table[finalPieceIndex]["startpos"] + self.table[finalPieceIndex]["length"] - finalBuffOffset
        }

        for i in range(initPieceIndex, finalPieceIndex + 1):
            self.table.pop(initPieceIndex)
        if piece2["length"] > 0:
            self.table.insert(initPieceIndex, piece2)
        if piece1["length"] > 0:
            self.table.insert(initPieceIndex, piece1)

        finalTable = []
        for piece in self.table:
            finalTable.append(piece)

        command = {
            "type": "delete",
            "initialTable": initialTable,
            "finalTable": finalTable
        }

        self.undoStack.append(command)

    
    def getOutputText(self):
        finalText = ''
        for piece in self.table:
            if piece["add"]:
                finalText += self.addBuff[piece["startpos"] : piece["startpos"] + piece["length"]]
            else:
                finalText += self.origBuff[piece["startpos"] : piece["startpos"] + piece["length"]]
        return finalText

    def printPieceTable(self):
        print("====PIECE  TABLE====")
        print("FileContent: {0}".format(self.origBuff))
        print("AddBufferContent: {0}".format(self.addBuff))
        print()
        for piece in self.table:
            print("AddBuff: {0}\t\tStartPos: {1}\t\tLength: {2}".format(
                piece["add"], piece["startpos"], piece["length"]
            ))

        print("::: Undo Stack :::")
        for command in self.undoStack:
            print("\t{0}".format(command["type"]))

        print("::: Redo Stack :::")
        for command in self.redoStack:
            print("\t{0}".format(command["type"]))
        print("====================")



def example1():
    initString = "Hey, this is a program implementing Piece Table Method."

    print("Initialising...")
    table = PieceTable(initString)
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")
    
    print("Adding text...")
    table.insert(" for text editors", len(initString) - 1)
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

    print("Adding text...")
    table.insert(" you", 3)
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

    print("\n\nTo be deleted: {0}".format(table.getOutputText()[3:3+4]))
    print("Deleting text...")
    table.delete(3, 4)
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

    print("\n\nTo be deleted: {0}".format(table.getOutputText()[15-4:15]))
    print("Deleting text...")
    table.delete(15, -4)
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

    print("\n\nResetting Buffers...")
    table.resetBuffers()
    table.printPieceTable()
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

    print("Adding text...")
    table.insert(" for text editors", len(initString) - 1)
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

    print("Adding text...")
    table.insert(" you", 3)
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

    print("\n\nTo be deleted: {0}".format(table.getOutputText()[3:3+4]))
    print("Deleting text...")
    table.delete(3, 4)
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")


    print("\n\nTo be deleted: {0}".format(table.getOutputText()[15-4:15]))
    print("Deleting text...")
    table.delete(15, -4)
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")
    
    print("\n\nResetting Buffers...")
    table.resetBuffers()
    table.printPieceTable()
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

def example2():
    initString = 'ABCDEFGH'
    table = PieceTable(initString)
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

    table.insert("IJKL", len(initString))
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

    table.undo()
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

    table.redo()
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

    table.delete(3, 2)
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

    table.undo()
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

    table.redo()
    table.printPieceTable()
    print("Final Text: {0}".format(table.getOutputText()))
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")

    print("\n\nResetting Buffers...")
    table.resetBuffers()
    table.printPieceTable()
    print("=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=.=")


if __name__ == '__main__':
    # example1()
    example2()
