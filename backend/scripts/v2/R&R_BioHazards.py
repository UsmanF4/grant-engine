from helper import get_pdf_document, find_next_section_page, find_section_page

texts = ["Biohazard", "Intellectual Property"]

def extract_style(doc, start_page, end_page, specific_text):
    for page_number in range(start_page, end_page):
        page = doc.load_page(page_number)
        if page is None:
            print(f"Failed to load page {page_number + 1}")
            continue

        text_dict = page.get_text("dict")
        if text_dict is None:
            print(f"Failed to extract text from page {page_number + 1}")
            continue

        for block in text_dict.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "")
                    if specific_text in text and "Bold" in span.get("font", ""):
                        # print(f"Page {page_number + 1} - Text: {text}")
                        # print(f"Font: {span['font']}")
                        return None

    return f"{specific_text} missing"

def main():
    pdf_path = "../Docs/Application/SparkMolecular_Sept24_PhI_Application_submitted.pdf"
    section_title = "Facilities & Other Resources"
    doc = get_pdf_document(pdf_path)

    toc = doc.get_toc()
    start_page = find_section_page(toc, section_title)
    next_section_page = find_next_section_page(toc, section_title)

    if start_page is not None:
        end_page = next_section_page - 1 if next_section_page is not None else len(doc)
        print(f"The '{section_title}' section starts on page {start_page} and ends on page {end_page}.\n")

        for specific_text in texts:
            error = extract_style(doc, start_page - 1, end_page, specific_text)
            if error:
                print(f"Error for '{specific_text}': {error}")
            else:
                print(f"No error found for '{specific_text}'!")

if __name__ == "__main__":
    main()
