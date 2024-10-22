from helper import get_pdf_document, find_next_section_page, find_section_page

def find_section_pages(pdf_path, section_title):
    try:
        doc = get_pdf_document(pdf_path)
        toc = doc.get_toc()

        start_page = find_section_page(toc, section_title)
        next_section_page = find_next_section_page(toc, section_title)

        if start_page is not None:
            end_page = next_section_page - 1 if next_section_page is not None else len(doc)
            print(f"The '{section_title}' section starts on page {start_page} and ends on page {end_page}.\n")
            return start_page, end_page
        else:
            print(f"The section titled '{section_title}' was not found in the document.")
            return None, None

    except FileNotFoundError:
        print(f"Error: The file at path '{pdf_path}' was not found. Please check the file path and try again.")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred while processing the document: {e}")
        return None, None

def check_consortium_doc(start_page, end_page, doc):
    for i in range(start_page, end_page + 1):
        page = doc.load_page(i)
        text = page.get_text('text')
        if "8. Consortium/Contractual Arrangements" in text:
            lines = text.split('\n')
            for j, line in enumerate(lines):
                if "8. Consortium/Contractual Arrangements" in line:
                    if j + 1 < len(lines) and lines[j + 1].strip().endswith(".pdf"):
                        print(f"Found consortium document: {lines[j + 1].strip()}")
                        return lines[j + 1].strip()
    return "Error: Consortium document not found in the specified section."

def validate_consortium_arrangement():
    pdf_path = "../Docs/Application/EyeSonix_Application_Preview 1.pdf"

    subward_budget_pages = find_section_pages(pdf_path, "Subaward Budget 1")
    if subward_budget_pages[0] is not None:
        phs398_pages = find_section_pages(pdf_path, "PHS Research Plan")
        if phs398_pages[0] is not None:
            doc = get_pdf_document(pdf_path)
            error = check_consortium_doc(phs398_pages[0] - 1, phs398_pages[1] - 1, doc)
            if error:
                print(error)

def main():
    validate_consortium_arrangement()

if __name__ == "__main__":
    main()
