from PyPDF2 import PdfFileWriter, PdfFileReader
from pdfInfo2 import PdfInfo2
from PyPDF2Highlight import createHighlight, addHighlightToPage


class RedactPdf():

    def maskChars(self, chars, page, pdfOutput):
        for char in chars:
            highlight = createHighlight(
                char["x0"], char["y0"], char["x1"], char["y1"])
            addHighlightToPage(highlight, page, pdfOutput)
        return

    def setPageToMask(self, page):
        return self.pdfInput.getPage(int(page))

    def getPdfInfo(self, inputPdfPath, wordsToMasks):
        pdfInfoRead = PdfInfo2()
        return pdfInfoRead.controller(inputPdfPath, wordsToMasks)

    def addMasksToPages(self, pagesCharCoords, pdfOutput, outputPath):
        for page in pagesCharCoords:
            pageToMask = self.setPageToMask(page)
            self.maskChars(pagesCharCoords[page], pageToMask, pdfOutput)
            pdfOutput.addPage(pageToMask)
        outputStream = open(outputPath, "wb")
        pdfOutput.write(outputStream)

    def pdfRedact(self, inputPdfPath, outputPath, wordsToMask):
        pagesCharCoords = self.getPdfInfo(inputPdfPath, wordsToMask)
        pdfInput = PdfFileReader(open(inputPdfPath, "rb"))
        self.pdfInput = pdfInput
        pdfOutput = PdfFileWriter()
        self.addMasksToPages(pagesCharCoords, pdfOutput, outputPath)
        return

# wordsToMasks = ["SINGAPORE","Street 61"]
# instance1 = RedactPdf()
# instance1.pdfRedact("article.pdf","output.pdf",wordsToMasks)