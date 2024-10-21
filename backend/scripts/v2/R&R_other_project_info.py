import fitz
from helper import get_pdf_document, find_section_page, find_next_section_page, extract_section_content, check_assurance_number

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
    pdf_path = "../Docs/Application/Amalgent_Sept4_FT_Application_Submitted.pdf"
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
