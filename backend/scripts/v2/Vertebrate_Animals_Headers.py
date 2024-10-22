import fitz
from helper import get_pdf_document, find_section_page, find_next_section_page

HEADERS = [
    "1. Description of Procedures",
    "2. Justification for the conduct of the studies described and the use of animals",
    "3. Minimization of Pain and Distress",
    "4. Methods of Euthanasia",
]


def check_vertebrate_animals_headers(doc, start_page, end_page):
    errors = []
    headers_found = {header: False for header in HEADERS}

    for page_num in range(start_page - 1, end_page):
        page = doc[page_num]
        text = page.get_text("text")

        for line in text.split("\n"):
            for header in HEADERS:
                if line.startswith(header):
                    headers_found[header] = True

    for header, found in headers_found.items():
        if not found:
            errors.append(
                f"Header '{header}' not found in the section from page {start_page} to {end_page}"
            )

    return errors


def validate_headers_in_section(doc, section_title):
    toc = doc.get_toc()
    start_page = find_section_page(toc, section_title)
    next_section_page = find_next_section_page(toc, section_title)

    if start_page is not None:
        end_page = next_section_page - 1 if next_section_page is not None else len(doc)
        print(
            f"The '{section_title}' section starts on page {start_page} and ends on page {end_page}.\n"
        )

        errors = check_vertebrate_animals_headers(doc, start_page, end_page)
        if errors:
            for error in errors:
                print(error)
        else:
            print("All headers found!")
    else:
        print(f"Section '{section_title}' not found in the document.")


def main():
    pdf_path = "../Docs/LightSeed_Application_Preview 1.pdf"
    section_title = "Vertebrate Animals"
    doc = get_pdf_document(pdf_path)

    validate_headers_in_section(doc, section_title)


if __name__ == "__main__":
    main()
