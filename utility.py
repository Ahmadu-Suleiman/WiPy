import io
import magic
import os
from os.path import isfile, join
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


class Section:
    def __init__(self, name, item_list) -> None:
        self.name = name
        self.item_list = item_list

    def append_item(self, item):
        self.item_list.append(item)

    def extend_list(self, item_list):
        self.item_list.extend(item_list)

    def __repr__(self):
        return ','.join(self.item_list)


Files = []
PATH = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop', 'Container')
mime = magic.Magic(mime=True)

for (path, folder, files) in os.walk(PATH):
    paths = [join(path, file) for file in files if isfile(join(path, file))]
    Files.extend(paths)

Files = sorted(Files, key=lambda i: os.path.splitext(os.path.basename(i)))

Sections = [Section('Images', [image for image in Files if mime.from_file(image).find('image') != -1]),
            Section('Videos', [video for video in Files if mime.from_file(
                video).find('video') != -1]),
            Section('Audios', [audio for audio in Files if mime.from_file(
                audio).find('audio') != -1]),
            Section('Texts', [text for text in Files if mime.from_file(
                text).find('text') != -1]),
            Section('PDFs', [text for text in Files if mime.from_file(
                text).find('pdf') != -1]),
            Section('Others', [text for text in Files if mime.from_file(text).find('application') != -1 and
                               mime.from_file(text).find('pdf') == -1])]


def get_text(item):
    file = open(item, 'r')
    text = file.read()
    return text


def get_text_pdf(item):
    file = open(item, 'rb')
    res_mgr = PDFResourceManager()
    ret_data = io.StringIO()
    txt_converter = TextConverter(res_mgr, ret_data, laparams=LAParams())
    interpreter = PDFPageInterpreter(res_mgr, txt_converter)

    for page in PDFPage.get_pages(file):
        interpreter.process_page(page)
    return ret_data.getvalue()
