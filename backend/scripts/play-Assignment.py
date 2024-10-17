import fitz


def extract_text_between_markers(text, start_marker, end_marker):
    start_index = text.find(start_marker) + len(start_marker)
    end_index = text.find(end_marker)
    if start_index != -1 and end_index != -1:
        return text[start_index:end_index].strip()
    return ""


def count_non_empty_entries(text):
    return len([entry for entry in text.split("\n") if entry.strip()])


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
    return count_sections


def main():
    doc = fitz.open("Docs/Dare_Sept24_PhII_Assignment_Submitted.pdf")
    count_awards = extract_awarding_components(doc)
    print("Count of awards:", count_awards)
    count_study_sections = extract_study_sections(doc)
    print("Count of study sections:", count_study_sections)
    doc.close()


if __name__ == "__main__":
    main()
