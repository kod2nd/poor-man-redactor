import pdfplumber
import json


class PdfInfo():

    def openPdf(self, path):
        self.pdf = pdfplumber.open(path)
        return self.pdf

    def getPages(self, pdf):
        self.pages = pdf.pages
        return pdf.pages

    def getChars(self, page):
        charsOnPage = [self.formatCharData(
            index, char) for index, char in enumerate(page.chars)]
        return charsOnPage

    def convertToJson(self, docData, fileName="data.json"):
        with open(fileName, 'w') as outfile:
            json.dump(docData, outfile)

    def formatCharData(self, index, char):
        for key in char:
            char[key] = self.decimalToFloat(char[key])
        return char

    def decimalToFloat(self, value):
        if str(type(value)) == "<class 'decimal.Decimal'>":
            return str(float(value))
        else:
            return str(value)

    def controller(self, path):
        pdf = self.openPdf(path)
        pages = self.getPages(pdf)
        docData = {}
        for count, page in enumerate(pages):
            docData[str(count+1)] = self.getChars(page)
        self.convertToJson(docData)
        self.docData = docData
        return docData

    def collateLines(self):
        page1 = self.docData["1"]
        lineCount = 0
        lines = {}
        charTop = ""
        temp = []
        for char in page1:
            if char["top"] == charTop:
                temp.append(char)
            elif charTop == "":
                temp.append(char)
                charTop = char["top"]
            else:
                lines[str(lineCount)] = temp
                lineCount += 1
                temp = []
                temp.append(char)
                charTop = char["top"]
        self.convertToJson(lines, "lines.json")
        self.lines = lines
        return lines
    
    def char2Words(self):
        firstLine = self.lines["0"]
        indexOfSpaces = []
        for index,char in enumerate(firstLine):
            if char["text"] == " ":
                indexOfSpaces.append(index)
        print(indexOfSpaces)
        currentIndex = 0
        words = []
        for spaceIndex in indexOfSpaces:
            if spaceIndex < len(firstLine):
                print("HERE", currentIndex, spaceIndex)
                words.append(firstLine[currentIndex:spaceIndex])
                currentIndex = spaceIndex + 1
            else:
                if firstLine[spaceIndex+1::]:
                    words.append(firstLine[spaceIndex+1::])
        # print(len(firstLine),firstLine[56:62])
        print(words)


instance1 = PdfInfo()

instance1.controller("article.pdf")
instance1.collateLines()
instance1.char2Words()