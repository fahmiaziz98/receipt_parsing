import io
import pytesseract
import numpy as np
from abc import ABC, abstractmethod
from pdf2image import convert_from_bytes
from PIL import Image
from pypdf import PdfReader

DEFAULT_DPI = 50

class FileBytesToImage(ABC):

    @staticmethod
    @abstractmethod
    def convert_bytes_to_jpeg(file_bytes):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def convert_bytes_to_text(file_bytes):
        raise NotImplementedError


class PDFBytesToImage(FileBytesToImage):

    @staticmethod
    def convert_bytes_to_jpeg(file_bytes, dpi=DEFAULT_DPI, return_array=False):
        jpeg_data = convert_from_bytes(file_bytes, fmt="jpeg", dpi=dpi)[0]
        if return_array:
            jpeg_data = np.asarray(jpeg_data)
        return jpeg_data

    @staticmethod
    def convert_bytes_to_text(file_bytes):
        pdf_data = PdfReader(
            stream=io.BytesIO(initial_bytes=file_bytes) 
        )
        # receipt data should only have one page
        page = pdf_data.pages[0]
        return page.extract_text()


class JpegBytesToImage(FileBytesToImage):

    @staticmethod
    def convert_bytes_to_jpeg(file_bytes, dpi=DEFAULT_DPI, return_array=False):
        jpeg_data = Image.open(io.BytesIO(file_bytes))
        if return_array:
            jpeg_data = np.array(jpeg_data)
        return jpeg_data

    @staticmethod
    def convert_bytes_to_text(file_bytes):
        jpeg_data = Image.open(io.BytesIO(file_bytes))
        text_data = pytesseract.image_to_string(image=jpeg_data, nice=1)
        return text_data

 
if __name__ == "__main__":
    # Example usage
    # Assuming you have a PDF or JPEG file in bytes

    # Read a PDF file as bytes
    with open("Get Paid Now Confirmation.pdf", "rb") as f:
        pdf_bytes = f.read()

    # # Read a JPEG file as bytes
    # with open("example.jpeg", "rb") as f:
    #     jpeg_bytes = f.read()

    # Convert PDF bytes to JPEG and extract text
    pdf_to_image = PDFBytesToImage()
    pdf_jpeg = pdf_to_image.convert_bytes_to_jpeg(pdf_bytes)
    pdf_text = pdf_to_image.convert_bytes_to_text(pdf_bytes)

    print("Extracted text from PDF:")
    print(pdf_text)