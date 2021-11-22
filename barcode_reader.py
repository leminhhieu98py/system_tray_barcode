# Importing library
import cv2
# from pdf2image import convert_from_path
from PIL import Image
from pyzbar.pyzbar import decode
import os


# Make one method to decode the barcode
def BarcodeReader(image):
    print("Scanning")
    img = cv2.imread(image)
    detectedBarcodes = decode(img)
    barcode_values = ''
    if not detectedBarcodes:
        return False
    else:
        for barcode in detectedBarcodes:
            if barcode_values == "":
                if barcode.data != "" and barcode.type != 'QRCODE':
                    barcode_values += barcode.data.decode("utf-8")
            else:
                return False
    return barcode_values


def img_to_pdf(path, filename, target_directory):
    print("converting")
    image = Image.open(path)
    pdf_from_image = image.convert('RGB')

    move_to_target_directory(path, filename, pdf_from_image, target_directory)
    

def move_to_target_directory(path, filename, pdf_from_image, target_directory):
    # remove image from root folder
    os.remove(path)

    # Save to target folder
    file_name_without_ext = filename[:-4]
    pdf_from_image.save(target_directory + "/" + file_name_without_ext + '.pdf')
    print("success")


def rename_to_barcode(barcode_result, ext, directory, filepath):
    new_file_name = barcode_result + ext[len(ext) - 1]
    new_file_path = os.path.join(directory, new_file_name)
    os.rename(filepath, new_file_path)

def scan_engine(directory, target_directory):
    print("Opening files...")
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            filepath = os.path.join(directory, filename)
            barcode_result = BarcodeReader(filepath)
            ext = os.path.splitext(filepath)
            # name_file = ''
            if barcode_result and barcode_result != '':
                rename_to_barcode(barcode_result, ext, directory, filepath)

                img_to_pdf(filepath, barcode_result, target_directory)
            else:
                print("can not scan this file:" + filename)
        else:
            continue