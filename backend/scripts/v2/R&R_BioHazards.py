from helper import (
    get_pdf_document,
    extract_section_content,
    find_next_section_page,
    find_section_page,
)


def extract_style(doc, start_page, end_page, specific_text):
    found = False

    # Load the specified page
    for page_number in range(start_page, end_page):
        page = doc.load_page(page_number)
        if page is None:
            print(f"Failed to load page {page_number + 1}")
            continue

        text_dict = page.get_text("dict")

        if text_dict is None:
            print(f"Failed to extract text from page {page_number + 1}")
            continue

        # Iterate through each block of text
        for block in text_dict["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        if specific_text in text:
                            font = span["font"]
                            if "Bold" in font:
                                # print(f"Page {page_number + 1} - Text: {text}")
                                # print(f"Font: {font}")
                                found = True
                                break
                    if found:
                        break
                if found:
                    break
            if found:
                break

    if not found:
        return("Biohazards handling and disposal missing")


def main():
    pdf_path = "../Docs/Application/SparkMolecular_Sept24_PhI_Application_submitted.pdf"
    section_title = "Facilities & Other Resources"
    doc = get_pdf_document(pdf_path)

    toc = doc.get_toc()

    start_page = find_section_page(toc, section_title)
    next_section_page = find_next_section_page(toc, section_title)

    if start_page is not None:
        end_page = next_section_page - 1 if next_section_page is not None else len(doc)
        print(
            f"The '{section_title}' section starts on page {start_page} and ends on page {end_page}."
            + "\n"
        )

        Error = extract_style(doc, start_page-1, end_page, "Biohazard")
        if Error is not None:
            print(Error)
        else:
            print("No error found!")


if __name__ == "__main__":
    main()
