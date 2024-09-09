```markdown
# Photo Downloader and PDF Combiner

## Description
This script downloads photos from a specified URL pattern, combines them into a PDF, and optionally removes watermarks from the PDF.

## Prerequisites
Ensure you have the following libraries installed:
- `requests`
- `Pillow`
- `fitz` (PyMuPDF)
- `concurrent.futures`

You can install them using pip:
```bash
pip install requests Pillow PyMuPDF
```

## Usage
1. **Download Photos**: The script will predict the number of pages and download photos from the specified base URL.
2. **Combine into PDF**: The downloaded photos will be combined into a single PDF file.
3. **Optional Deletion**: You will be prompted to delete the downloaded photos after combining them into a PDF.
4. **Optional Watermark Removal**: You will be prompted to remove watermarks from the PDF.

Run the script:
```bash
python main.py
```

## Configuration
- **Base URL**: Modify the [`base_url`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FC%3A%2FUsers%2Ftimur%2FDownloads%2F%D0%BF%D1%80%D0%B8%D1%86%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%20%D0%BA%D0%BD%D0%B8%D0%B6%D0%BA%D0%B0%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A40%2C%22character%22%3A28%7D%7D%5D%2C%224e27ec37-5d7a-431f-971f-77f219e11336%22%5D "Go to definition") variable to match the URL pattern of the photos you want to download.
- **Folder Path**: Change the [`folder_path`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FC%3A%2FUsers%2Ftimur%2FDownloads%2F%D0%BF%D1%80%D0%B8%D1%86%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%20%D0%BA%D0%BD%D0%B8%D0%B6%D0%BA%D0%B0%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A10%2C%22character%22%3A0%7D%7D%5D%2C%224e27ec37-5d7a-431f-971f-77f219e11336%22%5D "Go to definition") variable if you want to save the photos in a different directory.
- **Log File**: The [`log_file`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FC%3A%2FUsers%2Ftimur%2FDownloads%2F%D0%BF%D1%80%D0%B8%D1%86%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%20%D0%BA%D0%BD%D0%B8%D0%B6%D0%BA%D0%B0%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A14%2C%22character%22%3A0%7D%7D%5D%2C%224e27ec37-5d7a-431f-971f-77f219e11336%22%5D "Go to definition") variable specifies the file to log converted photos.

## Output
- **PDF File**: The combined PDF will be saved as `output.pdf`.
- **Log File**: A log file [`converted_photos.log`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FC%3A%2FUsers%2Ftimur%2FDownloads%2F%D0%BF%D1%80%D0%B8%D1%86%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%20%D0%BA%D0%BD%D0%B8%D0%B6%D0%BA%D0%B0%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A94%2C%22character%22%3A8%7D%7D%5D%2C%224e27ec37-5d7a-431f-971f-77f219e11336%22%5D "Go to definition") will keep track of the photos that have been converted to PDF.

## License
This project is licensed under the MIT License.
```

This README file provides a clear and concise guide on how to use the script, including prerequisites, usage instructions, and configuration options.
