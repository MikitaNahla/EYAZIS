import PyPDF2


class PDFReader:
    def __init__(self, url):
        print(url)
        self.url = url
        self.text = ''

    def get_information(self):
        with open(self.url, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)

            for page_number in range(num_pages):
                page = reader.pages[page_number]
                self.text += page.extract_text()

        return self.text
