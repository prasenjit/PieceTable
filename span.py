FILE_TYPE_ORIGINAL = 1
FILE_TYPE_ADD = 2

class Buffer:
    def __init__(self, string):
        self.string = string
    
    def printBuffer(self):
        print(self.string)

    def length(self):
        return len(self.string)

    def append(self, substring):
        self.string += substring

class Piece:
    def __init__(self, filetype, buffStartPos, length, calculatedStartPos):
        self.filetype = filetype
        self.buffStartPos = buffStartPos
        self.length = length 
        self.calculatedStartPos = calculatedStartPos


class PieceTable:
    def __init__(self, initialFileContent):
        self.entries = []
        self.fileBuff = Buffer(initialFileContent)
        self.addBuff = Buffer('')
        initPiece = Piece(FILE_TYPE_ORIGINAL, 0, self.fileBuff.length(), 0)
        self.entries.append(initPiece)

    def removeText(self, buffStartPos, endPos):
        if (buffStartPos == 0):
            ...
        elif (endPos == self.fileBuff.length()):
            ...
        else:
            ...

    def addPiece(self, substring, position):
        if position < self.entries[-1].buffStartPos + self.entries[-1].length:
            i = 0
            while i < len(self.entries) and self.entries[i].buffStartPos < position:
                i += 1
            # i -= 1
            oldLen = self.entries[i].length
            self.entries[i].length = position - self.entries[i].buffStartPos
            remainLen = oldLen - self.entries[i].length
            remaining = Piece(self.entries[i].filetype, position, remainLen, 0)
            newentry = Piece(FILE_TYPE_ADD, self.addBuff.length(), len(substring), 0)
            self.addBuff.append(substring)
            self.entries.insert(i + 1, newentry)
            self.entries.insert(i + 2, remaining)

        else:
            newentry = Piece(FILE_TYPE_ADD, self.addBuff.length(), len(substring), 0)
            self.entries.append(newentry)
            self.addBuff.append(substring)

    def getFinalContent(self):
        final = ''
        for piece in self.entries:
            if (piece.filetype == FILE_TYPE_ORIGINAL):
                final += self.fileBuff.string[piece.buffStartPos : piece.buffStartPos + piece.length]
            if (piece.filetype == FILE_TYPE_ADD):
                final += self.addBuff.string[piece.buffStartPos : piece.buffStartPos + piece.length]
        return final

    def printPieceTable(self):
        print("===== PIECE TABLE =====")
        print("File: ", self.fileBuff.string, "\nAdd: ", self.addBuff.string)
        for entry in self.entries:
            print(entry.filetype, entry.buffStartPos, entry.length)
        print("=======================")


if __name__ == '__main__':
    temp = PieceTable("hello my name is terry")
    temp.printPieceTable()
    temp.addPiece("big  ", 23)
    temp.printPieceTable()
    print("final: ", temp.getFinalContent())
    temp.addPiece("very", 17)
    temp.printPieceTable()
    print("final: ", temp.getFinalContent())
    temp.addPiece("oi, ", 0)
    temp.printPieceTable()
    print("final: ", temp.getFinalContent())