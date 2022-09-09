import sys
import fitz


class PDFdocument:

    def __init__(self):
        self.scale_of_PyMuPDF_to_Adobe = 0.75

    def load(self, import_pdf=False, import_jpg=False):
        """
        method for loading document into object, opening first page and rendering it
        :return: 0. page object, 1. height, 2. width, 3. DPI
        """
        print("Hello Jakob!\n\n1. Your file should be named '1pdf.pdf' and"
              "\n2. should be stored in same folder as this python script."
              "\n3. decimals should be writen with . Ex.: 0.8 or 0.65"
              "\n\nPlease proceed :)"
              "\n")

        file_name = input("What is the name of the file? (WITHOUT file extensions, ex.: 123pdf): ")

        if import_pdf:
            doc = fitz.open(f"{file_name}.pdf")
            return doc

        if import_jpg:
            # fname = sys.argv[1]
            doc = fitz.open()
            img = fitz.open(f"{file_name}.jpg")
            rect = img[0].rect
            pdfbytes = img.convert_to_pdf()
            img.close()
            img_pdf = fitz.open("pdf", pdfbytes)
            page = doc.new_page(width=rect.width,
                                height=rect.height)
            page.show_pdf_page(rect, img_pdf, 0)
            return doc

    def render(self, page):
        """
        method for rendering pages and getting info about their height, width and DPI
        :param page: Data of one page of document
        :return: Data about page: 0. height, 1. width, 2. DPI
        """
        # render page
        pix = page.get_pixmap()

        # info about page
        page_height = pix.height
        page_width = pix.width
        dpi_of_image = pix.xres

        return page_height, page_width, dpi_of_image

    def inch_to_pixels(self, dpi_of_image ,inch):
        """
        calculate inches to pixels
        :param dpi_of_image:
        :param inch:
        :return: value of pixels in passed inch
        """
        px = (dpi_of_image * inch) * self.scale_of_PyMuPDF_to_Adobe
        return px

    def trim(self, page_data):
        """

        :param page_data: passed data from "load" method.
        :return: values for triming: 0.left, 1.top, 2.right, 3.bottom
        """

        from_left = float(input("How much to crop LEFT side of document (in INCH, ex.: 0.8 ): "))
        from_top = float(input("How much to crop TOP side of document (in INCH, ex.: 0.8 ): "))
        from_right = float(input("How much to crop RIGHT side of document (in INCH, ex.: 0.8 ): "))
        from_bottom = float(input("How much to crop BOTTOM side of document (in INCH, ex.: 0.8 ): "))

        width = page_data[0]
        height = page_data[1]
        dpi = page_data[2]

        left = self.inch_to_pixels(dpi, from_left)
        top = self.inch_to_pixels(dpi, from_top)
        right = width - self.inch_to_pixels(dpi, from_right)
        bottom = height - self.inch_to_pixels(dpi, from_bottom)

        return left, top, bottom, right

    def crop(self,
             import_pdf=False,
             import_jpg=False,
             export_as_pdf=False,
             export_as_jpg=False):
        """
        MAIN method which:
        1. loads PDF document or JPG image

        2. calculate inches to px, then crop document

        3. exports document in PDF document or JPG image
        (makes multiple images if ex. PDF has multiple pages).

        :param import_pdf: True if you are importing PDF
        :param import_jpg: True if you are importing JPG
        :param export_as_pdf: True if you want PDF
        :param export_as_jpg: True if you want JPG
        :return: None
        """
        doc = self.load(import_pdf, import_jpg)

        get_user_trim_wishes = True
        for page in doc:

            #get info about each page
            page_info = self.render(page)

            if get_user_trim_wishes:
                trim = self.trim(page_info)
                get_user_trim_wishes = False

            # cropping each page
            page.set_cropbox(fitz.Rect(trim[0],
                                       trim[1],
                                       trim[2],
                                       trim[3]))

        name_of_the_file = input("What will be the name of the file: ")

        if export_as_pdf:
            doc.save(f"{name_of_the_file}.pdf")

        if export_as_jpg:
            for page in doc:
                pix = page.get_pixmap()
                pix.save(f"{name_of_the_file}-{page.number + 1}.jpg")

        print("Done.")


