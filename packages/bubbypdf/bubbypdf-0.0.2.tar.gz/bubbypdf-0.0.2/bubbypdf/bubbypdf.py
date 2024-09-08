import os
from pdfrw import PdfReader, PdfWriter


def merge_pdfs(files, out):
    writer = PdfWriter()
    for input_file in files:
        writer.addpages(PdfReader(input_file).pages)
    writer.write(out)


def main():
    path = os.getcwd()
    outfile = os.path.join(path, "merged.pdf")
    pdf_files = [
        os.path.join(path, filename) for filename in os.listdir(path) if filename.endswith(".pdf")
    ]
    merge_pdfs(files=pdf_files, out=outfile)


if __name__ == '__main__':
    main()
