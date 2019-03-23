from PyPDF2 import PdfFileWriter, PdfFileReader
from pdfInfo2 import PdfInfo2
from PyPDF2Highlight import createHighlight, addHighlightToPage

inputPdf = "article.pdf"
# wordsToMask = ["SINGAPORE","Greenview", "Greenweave", "Tampines"]

pdfInfoRead = PdfInfo2()
charCoords = pdfInfoRead.controller(inputPdf)


def getMatchingWords(words, wordToMatch):
    matchingWords = [word for word in words if word["text"] == wordToMask]
    return matchingWords


def maskChars(chars, page, pdfOutput):
    for char in chars:
        highlight = createHighlight(
            char["x0"], char["y0"], char["x1"], char["y1"])
        addHighlightToPage(highlight, page, pdfOutput)
    return


pdfInput = PdfFileReader(open(inputPdf, "rb"))
pdfOutput = PdfFileWriter()

# 0 is the first page
page1 = pdfInput.getPage(0)

maskChars(charCoords,page1,pdfOutput)
# for wordToMask in wordsToMask:
#     matchingWords = getMatchingWords(wordsCoords[0], wordToMask)
#     maskWords(matchingWords, page1, pdfOutput)


# highlight = createHighlight(50, 400, 400, 500)

# addHighlightToPage(highlight, page1, pdfOutput)

pdfOutput.addPage(page1)

outputStream = open("output.pdf", "wb")
pdfOutput.write(outputStream)
