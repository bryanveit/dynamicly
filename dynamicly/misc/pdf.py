import PyPDF2

def merge_pdfs(pdf_list, savepath):
    merger = PyPDF2.PdfFileMerger()
    for filename in pdf_list:
        merger.append(PyPDF2.PdfFileReader(filename))
    merger.write(savepath)
