# Poor Man's PDF Redactor

Mask/Redact words in a pdf document

## Installation

Python 3

- pip install PyPDF2
- pip install pdfplumber
  
You man need to install ImageMagick [Installation instructions here](http://docs.wand-py.org/en/latest/guide/install.html#install-imagemagick-debian)

Special thanks to [agentcooper](https://gist.github.com/agentcooper)
## Usage

1. import and instantiatie RedactPdf
2. call pdfRedact method

```python
from redactPDF.py import RedactPdf

redactor = RedactPdf()
redactor.pdfRedact(input, output, wordList)
```


### instance.pdfRedact(input,output,wordList)

##### Input

Path to input pdf

- Type(String)

##### Output

Path to output pdf

- Type(String)

##### wordList

List of words to redact or mask

- Type(List)

## Example

Using artcle.pdf(in project root) as input pdf. Should give you output.pdf with masked out "SINGAPORE" and "Street 61"

```python
from redactPDF.py import RedactPdf

wordsToMasks = ["SINGAPORE","Street 61"]
redactor = RedactPdf()
redactor.pdfRedact("article.pdf", "output.pdf", wordList)
```

