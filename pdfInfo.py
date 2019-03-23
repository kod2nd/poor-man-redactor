import pdfplumber
import json
import itertools
import re


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

    def collateLines(self, pageNum, docData):
        page = docData[pageNum]
        lineCount = 0
        lines = {}
        charTop = ""
        temp = []
        for char in page:
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
        formattedLines = [self.char2Words(lineNum, lines) for lineNum in lines]
        wordsOnPage = list(itertools.chain(*formattedLines))
        self.wordsOnPage = wordsOnPage
        return wordsOnPage

    def char2Words(self, lineNum, lines):
        line = lines[lineNum]
        indexOfSpaces = []
        for index, char in enumerate(line):
            if char["text"] == " ":
                indexOfSpaces.append(index)
        currentIndex = 0
        words = []
        for spaceIndex in indexOfSpaces:
            if spaceIndex < len(line):
                words.append(line[currentIndex:spaceIndex])
                currentIndex = spaceIndex + 1
            else:
                if line[spaceIndex+1::]:
                    words.append(line[spaceIndex+1::])
        joinedWords = [self.joinWord(word) for word in words]
        return joinedWords

    def isNotAlphaNumeric(self,char):
        if re.search('[a-zA-Z0-9]',char):
            return False
        else:
            return True

    def joinWord(self, word):
        firstChar = word[0]
        lastChar = word[-1]
        if self.isNotAlphaNumeric(firstChar["text"]):
            if len(word) > 1:
                firstChar = word[1]
        if self.isNotAlphaNumeric(lastChar["text"]):
            if len(word) > 1:
                lastChar = word[-2]
        joinedWord = {
            "x0": firstChar["x0"],
            "y0": firstChar["y0"],
            "x1": lastChar["x1"],
            "y1": lastChar["y1"],
            "page": firstChar["page_number"],
            "text": ""
        }
        for char in word:
            joinedWord["text"] += char["text"]
        return joinedWord

    def getWordCoords(self, path):
        pdf = self.openPdf(path)
        pages = self.getPages(pdf)
        docData = {}
        for count, page in enumerate(pages):
            docData[str(count+1)] = self.getChars(page)
        docWords = [self.collateLines(page, docData) for page in docData]
        self.convertToJson(docWords)
        return docWords


instance1 = PdfInfo()

# a = instance1.getWordCoords("article.pdf")
# a = instance1.collateLines()
# instance1.char2Words()
