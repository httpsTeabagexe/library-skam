import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed
import fitz
import time
from PIL import Image

# Create a folder to save the downloaded photos
folder_path = 'photos'
os.makedirs(folder_path, exist_ok=True)

# Log file to keep track of converted photos
log_file = 'converted_photos.log'

# Function to download a photo given its URL
def download_photo(url, filename):
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    file_path = os.path.join(folder_path, filename)
    if os.path.exists(file_path):
        return True, f'Photo {filename} already exists'

    try:
        response = session.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return True, f'Downloaded photo {filename}'
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {filename}: {e}")
        return False, f'Failed to download {filename}'

# Cache for storing download results (True for success, False for failure)
page_cache = {} 

# Predict the number of pages using an enhanced binary search
def predict_number_of_pages(base_url):
    """Predicts the number of pages using a cached binary search."""

    def is_page_available(page_num):
        """Checks if a page is available, with caching and retries."""
        if page_num in page_cache:
            return page_cache[page_num]

        url = base_url.format(str(page_num).zfill(6))
        filename = f'photo_{str(page_num).zfill(3)}.png'
        success, _ = download_photo(url, filename)
        time.sleep(0.1)  # Small delay 

        page_cache[page_num] = success  # Cache the result
        return success

    low = 1
    high = 1000  # Initial high guess, adjust if needed

    while low <= high:
        mid = (low + high) // 2
        if is_page_available(mid):
            low = mid + 1
        else:
            high = mid - 1

    return low  

# Base URL for the photos
base_url = 'https://elibrary.mai.ru/ProtectedView/Content/tmp/df93ea3f83f94279998e496925c936cf{}.png'

# Predict the number of pages
num_pages = predict_number_of_pages(base_url)
print(f'Predicted number of pages: {num_pages}')

# List of URLs to download
urls = [base_url.format(str(i).zfill(6)) for i in range(1, num_pages + 1)]

# Download the photos in parallel and store download statuses
download_statuses = {}
with ThreadPoolExecutor() as executor:
    futures = {executor.submit(download_photo, url, f'photo_{str(i).zfill(3)}.png'): i for i, url in enumerate(urls, 1)}
    for future in as_completed(futures):
        page_num = futures[future]
        download_statuses[page_num] = future.result()

# Print download statuses in order
for i in range(1, num_pages + 1):
    success, message = download_statuses[i]
    print(message)

# Read the log file to get the list of already converted photos
if os.path.exists(log_file):
    with open(log_file, 'r') as log:
        converted_photos = set(log.read().splitlines())
else:
    converted_photos = set()

# Combine the downloaded photos into a PDF
pdf_path = 'output.pdf'
doc = fitz.open()

for filename in sorted(os.listdir(folder_path)):
    if filename.endswith('.png') and filename not in converted_photos:
        image_path = os.path.join(folder_path, filename)
        img = Image.open(image_path).convert('RGB')
        img.save(image_path, 'PNG')
        imgdoc = fitz.open(image_path)
        pdfbytes = imgdoc.convert_to_pdf()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insert_pdf(imgpdf)
        # Log the converted photo
        with open(log_file, 'a') as log:
            log.write(filename + '\n')

# Check if the document has pages before saving
if len(doc) > 0:
    # Save the combined PDF
    doc.save(pdf_path)
    doc.close()
    print('All photos downloaded, combined into a PDF.')
else:
    print('No pages were added to the PDF. Please check the downloaded images.')

# Check if the PDF was created successfully
if not os.path.exists(pdf_path):
    print(f'Error: The PDF file {pdf_path} was not created.')
else:
    # Ask user if they want to delete the photos
    delete_photos = input('Do you want to delete the downloaded photos? (yes/no): ').strip().lower()
    if delete_photos == 'yes':
        for filename in os.listdir(folder_path):
            if filename.endswith('.png'):
                os.remove(os.path.join(folder_path, filename))
        print('Downloaded photos deleted successfully.')

    # Ask user if they want to remove the watermark
    remove_watermark = input('Would you like to remove the watermark from the PDF? (yes/no): ').strip().lower()
    if remove_watermark == 'yes':
        watermark_text = input('Please enter the watermark text to remove: ').strip()

        # Function to remove clustered rotated watermarks from a PDF
        def remove_watermark_from_pdf(pdf_path, watermark_text):
            """Removes clustered rotated watermarks from a PDF file.

            Args:
                pdf_path (str): The path to the PDF file.
                watermark_text (str): The text of the watermark to remove.
            """
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)

                watermark_instances = []
                for text in page.get_text("words"):
                    if text[4] == watermark_text and round(text[5]) != 0:
                        watermark_instances.append(text)

                if watermark_instances:
                    # 1. Create clusters of nearby watermarks:
                    clusters = []
                    threshold_distance = 50  # Adjust based on typical spacing

                    for instance in watermark_instances:
                        added_to_cluster = False
                        for cluster in clusters:
                            for other in cluster:
                                distance = ((instance[0] - other[0])**2 + (instance[1] - other[1])**2)**0.5 
                                if distance < threshold_distance:
                                    cluster.append(instance)
                                    added_to_cluster = True
                                    break
                            if added_to_cluster:
                                break

                        if not added_to_cluster:
                            clusters.append([instance]) 

                    # 2. Redact watermarks within clusters:
                    for cluster in clusters:
                        for text in cluster:
                            x0, y0, x1, y1 = text[0] - 5, text[1] - 5, text[2] + 5, text[3] + 5
                            redact_area = fitz.Rect(x0, y0, x1, y1)
                            page.add_redact_annot(redact_area, fill=(1, 1, 1)) 

                # Detect and redact colorful watermarks
                for image_index in range(page.get_image_count()):
                    xref = page.get_image_xref(image_index)
                    image = doc.extract_image(xref)
                    pix = fitz.Pixmap(doc, xref)
                    if pix.colorspace.n == 3:  # Check if the image is in RGB
                        if pix.samples[0] == 255 and pix.samples[1] == 0 and pix.samples[2] == 0:  # Red watermark
                            page.add_redact_annot(pix.rect, fill=(1, 1, 1))
                        elif pix.samples[0] == 0 and pix.samples[1] == 0 and pix.samples[2] == 255:  # Blue watermark
                            page.add_redact_annot(pix.rect, fill=(1, 1, 1))

                page.apply_redactions()

            output_path = os.path.splitext(pdf_path)[0] + "_no_watermark.pdf"
            doc.save(output_path)
            doc.close()

            print(f"Watermark removed. Saved to: {output_path}")

        # Remove watermark from the PDF
        remove_watermark_from_pdf(pdf_path, watermark_text)