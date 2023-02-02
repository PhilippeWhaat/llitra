# Place this python file in the folder where txt OCRed files should be generated, and run it.

import os
import pdfplumber
from wand.image import Image
import pytesseract
from PIL import ImageEnhance, ImageFilter
from PIL import Image as Img
import cv2 as cv
import PyPDF2
import shutil
from spellchecker import SpellChecker
import re
import multiprocessing
Img.MAX_IMAGE_PIXELS = None

folder = os.path.dirname(__file__)
spell = SpellChecker(language="es", distance=2)
spell.word_frequency.load_words(os.path.join(folder, "dict_created.txt"))

def Correction(completeDoc):
    completeDocListLines = completeDoc.split("\n")
    completeDocListLinesWords = []

    for frase in completeDocListLines:
        x = re.search("[A-Z]|[a-z]", frase)
        if frase != "" and x is not None:
            completeDocListLinesWords.append(frase.split(" "))

    correctedListLineWord = []
    correctedListLine = []
    for line in completeDocListLinesWords:
        for mot in line:
            i = spell.correction(mot)
            if i != mot:
                correctedListLineWord.append(i)
            else:
                correctedListLineWord.append(mot)
        correctedListLine.append(correctedListLineWord)
        correctedListLineWord = []

    finalListCorrected = []
    for line in correctedListLine:
        finalListCorrected.append(" ".join(line))

    finalListCorrected = "\n".join(finalListCorrected)
    return finalListCorrected

def Scanned(folder):
    equipo,nombre_pdf, raiz_pdf, count, expedientes_pdfs = [],[],[], 0, []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".pdf"):
                count += 1
                flag = 0
                with pdfplumber.open(os.path.join(root, file)) as pdf:

                    for w in range(len(pdf.pages)):
                        current_page = pdf.pages[w]

                        if current_page.extract_text() == None or str(current_page.extract_text()).find('Scann') != -1:
                            flag = 1
                            break
                        else:
                            flag = 0
                            pdf_s = ''
                            for pdfs in range(len(pdf.pages)):
                                pagina = pdf.pages[pdfs]
                                pdf_s = pdf_s + str(pagina.extract_text())
                            direccion = os.path.join(root, file)[:-4]
                            print(direccion)
                            expedientes_pdfs.append(direccion)
                            with open(f"{direccion}.txt", "w",encoding="utf-8") as f:
                                f.write(pdf_s+ '\n')
                            break

                    if flag == 1:
                        equipo.append(os.path.join(root, file))
                        nombre_pdf.append(file[:-4])
                        raiz_pdf.append(root)

    return equipo, nombre_pdf, raiz_pdf

def OCR(imagen, file_images_pdf):
    img = cv.imread(imagen)
    img = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
    adaptive = cv.adaptiveThreshold(img,255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 107,11) #57,4
    cv.imwrite(os.path.join(file_images_pdf,'auxo.jpg'), adaptive)
    im = Img.open(os.path.join(file_images_pdf,'auxo.jpg'))
    im = im.filter(ImageFilter.MedianFilter())

    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(15)
    im = im.convert('1')
    im.save(os.path.join(file_images_pdf,'auxo.jpg'))

    text = pytesseract.image_to_string(Img.open(os.path.join(file_images_pdf,'auxo.jpg')), lang='spa')
    return text

def ImgToPdf(filename, file_images_pdf):
    #estableciendo resolucion a imagen
    with Image(filename=filename, resolution=400) as img:
        #estableciendo ancho y alto
        img.resize(2000, 2500)
        img.save(filename= os.path.join(file_images_pdf,"img.jpg"))

pdfs, nombre_pdf, raiz_pdf = Scanned(folder)
print(f'len pdfs: {len(pdfs)}')

for i in range(0,len(pdfs)):
#def FileProcessing(i):
    direccion = raiz_pdf[i] + "/" + nombre_pdf[i]
    print(direccion)
    print((i+1)/len(pdfs))

    if os.path.isfile(f"{direccion}.txt"):
        print("File exists")

    else:
        
        pdf_filename = pdfs[i]

        file_images_pdf = pdf_filename[:-4]
        os.makedirs(file_images_pdf, exist_ok=True)

        text = ''
        pdfFileObj = open(pdf_filename, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj,strict=False)
        count = pdfReader.numPages

        if count == 1:
            ImgToPdf(pdf_filename, file_images_pdf)
            list_files = []
            text = 'HOJA 1\n' + OCR(os.path.join(file_images_pdf,'img.jpg'), file_images_pdf)
        else:
            
            ImgToPdf(pdf_filename, file_images_pdf)
            list_files = []
            for i in range(count):
                list_files.append(os.path.join(file_images_pdf,'img-' + str(i) + '.jpg'))

            u = 0
            for k in list_files:
                text = text + f'HOJA {u+1}\n' + OCR(k, file_images_pdf)
                u+=1
        
        text = Correction(text)
        
        with open(f"{direccion}.txt", "w", encoding="cp1252") as f:
            f.write(text + '\n')
            
        shutil.rmtree(file_images_pdf)

# if __name__ == "__main__":
#     # input list
#     i = range(0,len(pdfs))
  
#     # creating a pool object
#     p = multiprocessing.Pool(os.cpu_count())
  
#     # map list to target function
#     result = p.map(FileProcessing, i)