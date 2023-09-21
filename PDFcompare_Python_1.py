import aspose.words as aw
from datetime import date

File1 = "file1.pdf"
File2 = "file2.pdf"

# Load PDF files
PDF1 = aw.Document(File1)
PDF2 = aw.Document(File2)

# Convert PDF files to Word format
PDF1.save(File1, aw.SaveFormat.DOCX)
PDF2.save(File2, aw.SaveFormat.DOCX)

# Load converted Word documents 
DOC1 = aw.Document(File1)
DOC2 = aw.Document(File2)

# Set comparison options
options = aw.comparing.CompareOptions()            
options.ignore_formatting = True
options.ignore_headers_and_footers = True
options.ignore_case_changes = True
options.ignore_tables = True
options.ignore_fields = True
options.ignore_comments = True
options.ignore_textboxes = True
options.ignore_footnotes = True

# DOC1 will contain changes as revisions after comparison
DOC1.compare(DOC2, "user", date.today(), options)

if (DOC1.revisions.count > 0):
    # Save resultant file as PDF
    DOC1.save("compared.pdf", aw.SaveFormat.PDF)
    print("Documents are NOT equal")
else:
    print("Documents ARE equal")