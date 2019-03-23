from PyPDF2 import PdfFileWriter, PdfFileReader
from pdfInfo2 import PdfInfo2
from PyPDF2Highlight import createHighlight, addHighlightToPage

inputPdf = "article.pdf"
wordsToMask = ["SINGAPORE","Greenview", "Greenweave", "Tampines"]

pdfInfoRead = PdfInfo2()
pagesCharCoords = pdfInfoRead.controller(inputPdf,wordsToMask)


def maskChars(chars, page, pdfOutput):
    for char in chars:
        highlight = createHighlight(
            char["x0"], char["y0"], char["x1"], char["y1"])
        addHighlightToPage(highlight, page, pdfOutput)
    return


pdfInput = PdfFileReader(open(inputPdf, "rb"))
pdfOutput = PdfFileWriter()


def setPageToMask(page):
    return pdfInput.getPage(int(page))


for page in pagesCharCoords:
    maskChars(pagesCharCoords[page], setPageToMask(page), pdfOutput)
    pdfOutput.addPage(setPageToMask(page))


outputStream = open("output.pdf", "wb")
pdfOutput.write(outputStream)
