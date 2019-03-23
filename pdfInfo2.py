import pdfplumber
import json
import itertools
import re


class PdfInfo2():

    def convertToJson(self, docData, fileName="data.json"):
        with open(fileName, 'w') as outfile:
            json.dump(docData, outfile)

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

    def formatCharData(self, index, char):
        for key in char:
            char[key] = self.decimalToFloat(char[key])
        return char

    def decimalToFloat(self, value):
        if str(type(value)) == "<class 'decimal.Decimal'>":
            return str(float(value))
        else:
            return str(value)

    def getCharIndices(self, positions):
        start = positions[0]
        end = positions[-1]
        diff = end - start
        return [i+start for i in range(diff)]

    def getMatchIndice(self, text, stringToMatch):
        stringMatches = [[match.start(), match.end()]
                         for match in re.finditer(stringToMatch, text)]
        return [self.getCharIndices(positions) for positions in stringMatches]

    def getPageText(self, page):
        characters = page.chars
        text = ""
        for character in characters:
            text += character["text"]
        return text

    def matchedChars(self, pageChar, pageMatch):
        affectedChars = []
        for positions in pageMatch:
            for index in positions:
                affectedChars.append(pageChar[index])
        return affectedChars

    def getMatches(self, pageText, entitiesToMask):
        matches = []
        for entity in entitiesToMask:
            matches = [*matches, *self.getMatchIndice(pageText, entity)]
        return matches

    def controller(self, path, entitiesToMask):
        pdf = self.openPdf(path)
        pages = self.getPages(pdf)
        pagesChar = [self.getChars(page) for page in pages]
        pagesText = [self.getPageText(page) for page in pages]
        pagesCharsToMask = {}
        for index, page in enumerate(pagesText):
            matches = self.getMatches(page, entitiesToMask)
            pagesCharsToMask[str(index)] = self.matchedChars(
                pagesChar[index], matches)
        return pagesCharsToMask

