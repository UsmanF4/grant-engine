import re
from helper import get_pdf_document, find_section_page, find_next_section_page


def extract_sbc_control_id(content, search_text):
    start_index = content.find(search_text)
    end_index = content.find("\n", start_index)
    next_line_start = end_index + 1
    next_line_end = content.find("\n", next_line_start)
    return content[next_line_start:next_line_end].strip()


def validate_sbc_control_id(document, start_page, end_page):
    search_text = "SBC Control ID:*"
    for page_number in range(start_page - 1, end_page):
        page = document.load_page(page_number)
        page_content = page.get_text("text")
        if search_text in page_content:
            sbc_control_id = extract_sbc_control_id(page_content, search_text)
            if re.match(r"^\d{9}$", sbc_control_id):
                print("SBC Control ID:", sbc_control_id)
                return
            else:
                return f"Page {page_number + 1} - 'SBC Control ID' should be a 9-digit number."
        else:
            return f"Page {page_number + 1} - Text not found"


def main():
    pdf_path = "../Docs/LightSeed_Application_Preview 1.pdf"
    section_title = "SBIR STTR Information"
    document = get_pdf_document(pdf_path)

    table_of_contents = document.get_toc()
    start_page = find_section_page(table_of_contents, section_title)
    next_section_page = find_next_section_page(table_of_contents, section_title)

    if start_page is not None:
        end_page = next_section_page - 1 if next_section_page is not None else len(document)
        print(
            f"The '{section_title}' section starts on page {start_page} and ends on page {end_page}.\n"
        )

        validation_result = validate_sbc_control_id(document, start_page, end_page)
        if validation_result:
            print(validation_result)


if __name__ == "__main__":
    main()
