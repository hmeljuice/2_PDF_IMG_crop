from croppdf import PDFdocument


document = PDFdocument()
document.crop(import_pdf=True, export_as_pdf=True)

