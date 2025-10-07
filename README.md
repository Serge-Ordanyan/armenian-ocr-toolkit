Armenian OCR Toolkit: Advanced Processing for Historical Texts
Repository Name: armenian-ocr-toolkit
This Python project utilizes pytesseract and Pillow to perform advanced Optical Character Recognition (OCR) on Armenian-language PDFs. It is specifically designed to handle challenging inputs such as old, scanned, or difficult-to-read historical documents where standard copy/paste or basic OCR often fails.

The core feature is the implementation of multiple, parallel preprocessing and language strategies to maximize character recognition accuracy on stylized or broken Armenian fonts.

Key Features
Multi-Method Processing: The script runs the OCR pipeline with 6 distinct preprocessing and Tesseract configuration methods simultaneously. This ensures that if one technique fails, another might succeed.
Morphological Repair (Method 0): This top-priority method uses image dilation (MaxFilter) to repair broken or faded character strokes (like thinning or gaps in the letters) common in aged prints, which is crucial for improving the recognition of tricky Armenian letters.
Combined Language Model: Explicitly uses the hye+arm Tesseract language configuration. This combines both the standard Armenian (hye) and the older Armenian (arm) training data, leading to superior recognition across various scripts.
High-Quality Input: Converts PDF pages to high-resolution (600 DPI) images to capture maximum detail before processing.
Comparative Output: Saves the results from all 6 methods into separate .txt files, allowing the user to easily compare the outputs and select the best, most accurate result for final editing.
Prerequisites
To run this script, you must have the following installed on your system:
Python 3: The script requires Python 3.
Tesseract OCR Engine: Tesseract must be installed system-wide.
macOS (via Homebrew): brew install tesseract
Poppler: Required by the pdf2image library to reliably convert PDFs to images.
macOS (via Homebrew): brew install poppler
Tesseract Armenian Language Packs: You must have both the standard and old Armenian models (hye.traineddata and arm.traineddata) installed in your Tesseract data directory.
Installation and Setup
Clone the Repository:
git clone [https://github.com/Serge-Ordanyan/armenian-ocr-toolkit.git](https://github.com/Serge-Ordanyan/armenian-ocr-toolkit.git)
cd armenian-ocr-toolkit

Install Python Dependencies:
pip install pytesseract pillow pdf2image

Configure the Script: Open ocr_processor.py and modify the three lines in the Configuration section to match your local file paths (e.g., your PDF location and Tesseract binary path):

# Example Configuration:

pdf_path = "/path/to/your/input/Anania_Shirakatsi_1979.pdf"
output_dir = "/path/to/your/output_folder"
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

Usage
Run the script from your terminal:

python3 ocr_processor.py

The script will process the PDF and save all 6 output files to the designated folder. Always check the file beginning with Method_0_HYE+ARM_Morphological.txt first, as it uses the specialized preprocessing technique optimized for difficult Armenian book fonts.
