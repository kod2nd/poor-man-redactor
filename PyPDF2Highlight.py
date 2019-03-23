from PyPDF2.generic import (
    DictionaryObject,
    NumberObject,
    FloatObject,
    NameObject,
    TextStringObject,
    ArrayObject
)

# x0, y0 starts in bottom left corner
def createHighlight(x0, y0, x1, y1, color = [0, 0, 0]):
    newHighlight = DictionaryObject()

    newHighlight.update({
        NameObject("/F"): NumberObject(4),
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Highlight"),

        NameObject("/C"): ArrayObject([FloatObject(c) for c in color]),
        NameObject("/Rect"): ArrayObject([
            FloatObject(x0),
            FloatObject(y0),
            FloatObject(x1),
            FloatObject(y1)
        ]),
        NameObject("/QuadPoints"): ArrayObject([
            FloatObject(x0),
            FloatObject(y1),
            FloatObject(x1),
            FloatObject(y1),
            FloatObject(x0),
            FloatObject(y0),
            FloatObject(x1),
            FloatObject(y0)
        ]),
    })

    return newHighlight

def addHighlightToPage(highlight, page, output):
    highlight_ref = output._addObject(highlight)

    if "/Annots" in page:
        page[NameObject("/Annots")].append(highlight_ref)
    else:
        page[NameObject("/Annots")] = ArrayObject([highlight_ref])