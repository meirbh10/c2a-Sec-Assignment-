import filecmp

def compare_pdfs(pdf_file1, pdf_file2):
    return filecmp.cmp(pdf_file1, pdf_file2)

if __name__ == "__main__":
    pdf_file1 = "file1.pdf"
    pdf_file2 = "file2.pdf"

    are_pdfs_equal = compare_pdfs(pdf_file1, pdf_file2)

    if are_pdfs_equal:
        print("The PDFs ARE equal.")
    else:
        print("The PDFs are NOT equal.")
