from PyPDF2 import PdfFileWriter, PdfFileReader
from pdfInfo import PdfInfo
from PyPDF2Highlight import createHighlight, addHighlightToPage

inputPdf = "article.pdf"
wordsToMask = ["SINGAPORE","Greenview", "Greenweave.", "Tampines"]

pdfInfoRead = PdfInfo()
wordsCoords = pdfInfoRead.getWordCoords(inputPdf)


def getMatchingWords(words, wordToMatch):
    matchingWords = [word for word in words if word["text"] == wordToMask]
    return matchingWords


def maskWords(words, page, pdfOutput):
    for word in words:
        highlight = createHighlight(
            word["x0"], word["y0"], word["x1"], word["y1"])
        addHighlightToPage(highlight, page, pdfOutput)
    return


pdfInput = PdfFileReader(open(inputPdf, "rb"))
pdfOutput = PdfFileWriter()

# 0 is the first page
page1 = pdfInput.getPage(0)

for wordToMask in wordsToMask:
    matchingWords = getMatchingWords(wordsCoords[0], wordToMask)
    maskWords(matchingWords, page1, pdfOutput)

# highlight = createHighlight(50, 400, 400, 500)

# addHighlightToPage(highlight, page1, pdfOutput)

pdfOutput.addPage(page1)

outputStream = open("output.pdf", "wb")
pdfOutput.write(outputStream)
