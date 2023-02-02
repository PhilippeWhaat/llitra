# Place this python file in the folder_2B_OCRed where txt OCRed files should be generated, and run it.
# If not working (error on Wand Image), install package Imagemagick from 
# conda install -c conda-forge/label/cf202003 <package name>
# To avoid incompatibilities (conda will downgrade during the installation), install missing
# packages with the same method

import os
import pdfplumber
from wand.image import Image
#import pytesseract
from PIL import ImageEnhance, ImageFilter
from PIL import Image as Img
import cv2 as cv
import PyPDF2
import shutil
from spellchecker import SpellChecker
import re
import multiprocessing
from tkinter import Tk, filedialog, messagebox
import pyperclip as clipboard

Img.MAX_IMAGE_PIXELS = None

folder_2B_OCRed = os.path.dirname(__file__)
src_prefix = len(folder_2B_OCRed)
spell = SpellChecker(language="es", distance=2)
spell.word_frequency.load_words(os.path.join(folder_2B_OCRed, "dict_created.txt"))

CUR_DIR = str(os.path.dirname(__file__))

# Asking for destination folder:
# ------------------------------------
root = Tk() # pointing root to Tk() to use it as Tk() in program.
root.withdraw() # Hides small tkinter window.
root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
messagebox.showinfo("Destination folder", "Please select the destination folder for OCRed files.")
dst = filedialog.askdirectory(initialdir=CUR_DIR) # Returns opened path as str
if dst == "":
    exit()
# ------------------------------------

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

def Scanned(folder_2B_OCRed):
    equipo,nombre_pdf, raiz_pdf, count, expedientes_pdfs = [],[],[], 0, []
    for root, dirs, files in os.walk(folder_2B_OCRed):
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
                            dirpath = dst + direccion[src_prefix:]
                            expedientes_pdfs.append(direccion)
                            with open(f"{dirpath}.txt", "w",encoding="utf-8") as f:
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

    #text = pytesseract.image_to_string(Img.open(os.path.join(file_images_pdf,'auxo.jpg')), lang='spa')
    img_to_shortcut = os.path.join(file_images_pdf,'auxo.jpg')

    root = Tk()
    root.withdraw()
    root.clipboard_clear()
    # text to clipboard
    os.system(f'shortcuts run CopyText -i "{img_to_shortcut}"')

    # wU = True
    # while wU == True:
    #     if img_to_shortcut != root.clipboard_get(): #checks the condition
    #         text = root.clipboard_get()
    #         wU = False
    #     time.sleep(1) #waits 60s for preformance
    
    root.destroy()
    text = clipboard.paste()
    #text = str(os.system("pbpaste"))

    return text

def ImgToPdf(filename, file_images_pdf):
    #estableciendo resolucion a imagen
    with Image(filename=filename, resolution=400) as img:
        #estableciendo ancho y alto
        img.resize(2000, 2500)
        img.save(filename= os.path.join(file_images_pdf,"img.jpg"))

pdfs, nombre_pdf, raiz_pdf = Scanned(folder_2B_OCRed)
print(f'len pdfs: {len(pdfs)}')

for i in range(0,len(pdfs)):
#def FileProcessing(i):
    direccion = raiz_pdf[i] + "/" + nombre_pdf[i]
    
    # here dst has destination directory, root[src_prefix:] gives us relative
	# path from source directory and dirname has folder names
    dirpath = dst + direccion[src_prefix:]

    print(direccion)
    print(dirpath)
    print((i+1)/len(pdfs))

    if os.path.isfile(f"{dirpath}.txt".upper()):
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
        
        #text = Correction(text)
        
        with open(f"{dirpath}.txt", "w", encoding="utf8") as f:
            f.write(text + '\n')
            
        shutil.rmtree(file_images_pdf)

# if __name__ == "__main__":
#     # input list
#     i = range(0,len(pdfs))
  
#     # creating a pool object
#     p = multiprocessing.Pool(os.cpu_count())
  
#     # map list to target function
#     result = p.map(FileProcessing, i)