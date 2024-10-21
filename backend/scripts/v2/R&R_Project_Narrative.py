from helper import (
    get_pdf_document,
    find_section_page,
    find_next_section_page,
    extract_section_content,
)


def count_narrative_length(content):
    if not content:
        print("No content provided.")
        return

    doc_text = content[0].split(".")
    filtered_text = [
        line.strip()
        for line in doc_text
        if line.strip() and not any(
            line.lstrip().startswith(prefix)
            for prefix in [
                "Contact PD/PI:",
                "Project Summary/Abstract",
                "Page",
            ]
        )
    ]
    cleaned_text = [
        line.replace("PROJECT NARRATIVE:", "").replace("NARRATIVE", "")
        for line in filtered_text
    ]
    if len(cleaned_text) < 3:
        return "Exceeding Sentence limit"
    return None


def main():
    pdf_path = "../Docs/Application/Amalgent_Sept4_FT_Application_Submitted.pdf"
    section_title = "PROJECT NARRATIVE"
    doc = get_pdf_document(pdf_path)

    toc = doc.get_toc()
    start_page = find_section_page(toc, section_title)
    next_section_page = find_next_section_page(toc, section_title)

    if start_page is not None:
        end_page = next_section_page - 1 if next_section_page is not None else len(doc)
        print(
            f"The '{section_title}' section starts on page {start_page} and ends on page {end_page}."
        )

    content = extract_section_content(doc, section_title)
    error = count_narrative_length(content)
    if error:
        print(error)


if __name__ == "__main__":
    main()
