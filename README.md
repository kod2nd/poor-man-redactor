# Poor Man's PDF Redactor

Mask out words in a pdf document

## Installation

Python 3

- pip install PyPDF2
- pip install pdfplumber
  You man need to install ImageMagick [Installation instructions here](http://docs.wand-py.org/en/latest/guide/install.html#install-imagemagick-debian)

## Usage

1. import and instantiatie RedactPdf
2. call pdfRedact method

```python
from redactPDF.py import RedactPdf

redactor = RedactPdf()
redactor.pdfRedact(input, output, wordList)
```


#### instance.pdfRedact(input,output,wordList)

##### Input

Path to input pdf

- Type(String)

##### Output

Path to output pdf

- Type(String)

##### wordList

List of words to redact or mask

- Type(List)

