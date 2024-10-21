import fitz
from helper import extract_text_between_markers, count_non_empty_entries, get_pdf_document

def extract_awarding_components(doc):
    count_awards = 0
    for page in doc:
        text = page.get_text("text")
        awarding_components_text = extract_text_between_markers(
            text,
            "Suggested Awarding Components:",
            "Study Section Assignment Suggestions (optional)",
        )
        if awarding_components_text:
            print(awarding_components_text)
            count_awards += count_non_empty_entries(awarding_components_text)
    print("Number of Awarding Components: ", count_awards)
    return count_awards

def extract_study_sections(doc):
    count_sections = 0
    for page in doc:
        text = page.get_text("text")
        study_sections_text = extract_text_between_markers(
            text,
            "Suggested Study Sections:",
            "Rationale for assignment suggestions (optional)",
        )
        # Exclude the "Each entry is limited to 20 characters" part
        study_sections_text = study_sections_text.replace(
            "Each entry is limited to 20 characters", ""
        ).strip()
        if study_sections_text:
            print(study_sections_text)
            count_sections += count_non_empty_entries(study_sections_text)
    print("Number of Count Sections: ", count_sections)
    return count_sections

def validate_DMSP(doc):
    count_awards = extract_awarding_components(doc)
    count_study_sections = extract_study_sections(doc)
    errors = []

    if count_awards < 2:
        errors.append("Less than 2 awards found")
    if count_study_sections < 1:
        errors.append("Less than 1 study section found")
    if not errors:
        errors.append("No errors found")

    return errors

def main():
    doc = get_pdf_document("../Docs/Assigments/Dare_Sept24_PhII_Assignment_Submitted.pdf")
    errors = validate_DMSP(doc)
    print(errors)
    doc.close()

if __name__ == "__main__":
    main()
