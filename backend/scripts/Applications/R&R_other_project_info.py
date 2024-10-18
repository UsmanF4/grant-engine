import fitz

# Store constants for animal and human subjects
CONSTANTS = {
    "animal": {
        "yes_text": """2. Are Vertebrate Animals Used?*
●Yes
❍No""",
        "no_text": """2. Are Vertebrate Animals Used?*
❍Yes
●No""",
        "assurance_start": "Animal Welfare Assurance Number",
        "assurance_end": "3. Is proprietary/privileged information included in the application?*",
        "no_info_text": """2. Are Vertebrate Animals Used?*
❍Yes
●No
2.a. If YES to Vertebrate Animals
Is the IACUC review Pending?
❍Yes ❍No
IACUC Approval Date:
Animal Welfare Assurance Number"""
    },
    "human": {
        "yes_text": """1. Are Human Subjects Involved?*
●Yes
❍No""",
        "no_text": """1. Are Human Subjects Involved?*
❍Yes
●No""",
        "assurance_start": "Human Subject Assurance Number",
        "assurance_end": "2. Are Vertebrate Animals Used?*",
        "no_info_text": """1. Are Human Subjects Involved?*
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
    }
}

def get_pdf_document(file_path):
    return fitz.open(file_path)

def find_section_page(toc, section_title):
    """Finds the start page of the specified section."""
    for level, title, page_number in toc:
        if section_title.lower() in title.lower():
            return page_number
    return None

def find_next_section_page(toc, current_section_title):
    """Finds the start page of the next section."""
    found_current = False
    for level, title, page_number in toc:
        if found_current:
            return page_number
        if current_section_title.lower() in title.lower():
            found_current = True
    return None

def extract_section_content(doc, section_title):
    """Extracts text content from the section."""
    toc = doc.get_toc()
    start_page = find_section_page(toc, section_title)
    end_page = find_next_section_page(toc, section_title)
    if start_page is not None:
        section_text = ""
        pages_info = []
        for page_num in range(start_page - 1, (end_page or len(doc)) - 1):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            section_text += text
            pages_info.append((page_num + 1, text))
        return section_text, pages_info
    return None, []

def find_subject_involved(section_text, pages_info, subject_type):
    """Finds whether the subject (human/animal) is involved."""
    constants = CONSTANTS[subject_type]
    yes_text = constants["yes_text"]
    no_text = constants["no_text"]

    for page_num, page_text in pages_info:
        if yes_text in page_text or no_text in page_text:
            return are_subject_involved(page_text, page_num, subject_type)
    return None

def are_subject_involved(page_text, page_num, subject_type):
    """Checks if the subject is involved and processes accordingly."""
    constants = CONSTANTS[subject_type]
    yes_text = constants["yes_text"]
    no_text = constants["no_text"]

    if yes_text in page_text:
        return check_assurance_number(page_text, page_num, constants["assurance_start"], constants["assurance_end"])
    elif no_text in page_text:
        return check_no_1a_information_added(page_text, page_num, subject_type)
    return None

def check_assurance_number(page_text, page_num, start_text, end_text):
    """Verifies the assurance number for the subject."""
    start_index = page_text.find(start_text)
    end_index = page_text.find(end_text)
    if start_index != -1 and end_index != -1:
        assurance_number = page_text[start_index + len(start_text):end_index].strip()
        if assurance_number.lower() not in ["none"]:
            return f"False! Correct {start_text} required at page {page_num}."
    return None

def check_no_1a_information_added(page_text, page_num, subject_type):
    """Validates that no additional information is required for the subject."""
    constants = CONSTANTS[subject_type]
    no_info_text = constants["no_info_text"]

    if no_info_text not in page_text:
        return f"False! Information not required at page {page_num}."
    return None

def validate_subject_involvement(section_text, pages_info, subject_type):
    """Validates involvement of human or animal subjects."""
    errors = []
    error = find_subject_involved(section_text, pages_info, subject_type)
    if error:
        errors.append(error)
    return errors

def main():
    pdf_path = "../Docs/Application"
    section_title = "R&R Other Project Information"
    doc = get_pdf_document(pdf_path)

    toc = doc.get_toc()
    start_page = find_section_page(toc, section_title)
    next_section_page = find_next_section_page(toc, section_title)

    if start_page is not None:
        end_page = next_section_page - 1 if next_section_page is not None else len(doc)
        print(f"The '{section_title}' section starts on page {start_page} and ends on page {end_page}.")

        section_text, pages_info = extract_section_content(doc, section_title)

        # Validate animal subjects
        animal_errors = validate_subject_involvement(section_text, pages_info, "animal")
        if animal_errors:
            print("Animal Subject Errors:", animal_errors)

        # Validate human subjects
        human_errors = validate_subject_involvement(section_text, pages_info, "human")
        if human_errors:
            print("Human Subject Errors:", human_errors)

if __name__ == "__main__":
    main()
