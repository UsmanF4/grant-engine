import fitz

def get_pdf_document(file_path):
    return fitz.open(file_path)

def find_section_page(toc, section_title):
    for level, title, page_number in toc:
        if section_title.lower() in title.lower():
            return page_number
    return None

def find_next_section_page(toc, current_section_title):
    found_current = False
    for level, title, page_number in toc:
        if found_current:
            return page_number
        if current_section_title.lower() in title.lower():
            found_current = True
    return None

def section_exists(doc, section_title):
    toc = doc.get_toc()
    return find_section_page(toc, section_title) is not None

def extract_section_content(doc, section_title):
    toc = doc.get_toc()
    start_page = find_section_page(toc, section_title)
    end_page = find_next_section_page(toc, section_title)
    if start_page is not None:
        section_text = ""
        pages_info = []
        for page_num in range(start_page - 1, (end_page or len(doc)) - 1):
            page = doc.load_page(page_num)
            section_text += page.get_text("text")
            pages_info.append((page_num + 1, page.get_text("text")))  # Keep track of page numbers
        return section_text, pages_info
    return None, []

def find_human_subject_involved(section_text, pages_info):
    text_yes = """1. Are Human Subjects Involved?*
●Yes
❍No"""
    text_no = """1. Are Human Subjects Involved?*
❍Yes
●No"""

    for page_num, page_text in pages_info:
        if text_yes in page_text or text_no in page_text:
            return are_human_involved(page_text, page_num)
    return None

def are_human_involved(page_text, page_num):
    text_yes = """1. Are Human Subjects Involved?*
●Yes
❍No"""
    text_no = """1. Are Human Subjects Involved?*
❍Yes
●No"""

    if text_yes in page_text:
        return check_human_assurance_number(page_text, page_num)
    if text_no in page_text:
        return check_no_1a_information_added(page_text, page_num)
    return None

def check_human_assurance_number(page_text, page_num):
    start_text = "Human Subject Assurance Number"
    end_text = "2. Are Vertebrate Animals Used?*"
    start_index = page_text.find(start_text)
    end_index = page_text.find(end_text)
    if start_index != -1 and end_index != -1:
        human_assurance_number = page_text[
            start_index + len(start_text) : end_index
        ].strip()
        if human_assurance_number not in ["None", "none", "NONE"]:
            return f"False! Correct Human Assurance Number required at page {page_num}."
    return None

def check_no_1a_information_added(page_text, page_num):
    text = """1. Are Human Subjects Involved?*
❍Yes
●No
1.a. If YES to Human Subjects
 
Is the Project Exempt from Federal regulations?
❍Yes
❍No
 
If YES, check appropriate exemption number:
1
2
3
4
5
6
7
8
 
If NO, is the IRB review Pending?
❍Yes
❍No
 
IRB Approval Date:
 
Human Subject Assurance Number"""

    if text not in page_text:
        return f"False! Information not required at page {page_num}."
    return None

def validate_human_subject_involved(section_text, pages_info):
    errors = []
    error = find_human_subject_involved(section_text, pages_info)
    if error:
        errors.append(error)
    print(errors)

def main():
    pdf_path = "../Docs/Application/SparkMolecular_Sept24_PhI_Application_submitted.pdf"
    section_title = "R&R Other Project Information"
    doc = get_pdf_document(pdf_path)

    toc = doc.get_toc()
    start_page = find_section_page(toc, section_title)
    next_section_page = find_next_section_page(toc, section_title)

    if start_page is not None:
        end_page = next_section_page - 1 if next_section_page is not None else len(doc)
        print(
            f"The '{section_title}' section starts on page {start_page} and ends on page {end_page}."
        )

        section_text, pages_info = extract_section_content(doc, section_title)
        validate_human_subject_involved(section_text, pages_info)

if __name__ == "__main__":
    main()
