// In order to run the Script need to run the command "node PDFcompare_JavaScript.js"

const fs = require('fs');

// Function to compare two PDF files
function comparePDFs(pdfPath1, pdfPath2) {
  try {
    // Read the contents of the PDF files as binary buffers
    const pdfBuffer1 = fs.readFileSync(pdfPath1);
    const pdfBuffer2 = fs.readFileSync(pdfPath2);

    // Compare the byte streams of the two PDFs
    if (pdfBuffer1.equals(pdfBuffer2)) {
      return true; // PDFs are equal
    } else {
      return false; // PDFs are not equal
    }
  } catch (error) {
    console.error('Error:', error);
    return false; // An error occurred, or one of the files doesn't exist
  }
}

const pdfFile1 = 'file1.pdf';
const pdfFile2 = 'file2.pdf';

const arePDFsEqual = comparePDFs(pdfFile1, pdfFile2);

if (arePDFsEqual) {
  console.log('The PDFs ARE equal.');
} else {
  console.log('The PDFs are NOT equal.');
}
