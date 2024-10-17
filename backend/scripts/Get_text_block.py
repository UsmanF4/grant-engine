import fitz  # PyMuPDF

# Open the PDF document
doc = fitz.open("Docs/AG DMSP 20240102.pdf")

# Define the specific text you are looking for
specific_text = "A."

# Iterate through each page
for page_number in range(doc.page_count):
    page = doc.load_page(page_number)
    text_dict = page.get_text("dict")

    # Iterate through each block of text
    for block in text_dict["blocks"]:
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"]
                if specific_text in text:
                    font = span["font"]
                    font_size = span["size"]
                    font_color = span["color"]

                    print(f"Page {page_number + 1} - Text: {text}")
                    print(f"Font: {font}")
                    print(f"Font size: {font_size}")
                    print(f"Font color: {font_color}")
                    print(f"font style:", span["flags"])


doc.close()
