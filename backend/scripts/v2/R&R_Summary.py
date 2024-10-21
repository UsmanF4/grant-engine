from helper import (
    get_pdf_document,
    find_section_page,
    find_next_section_page,
    extract_section_content,
)


def count_summary_length(content):
    doc_text = [
        line
        for line in content[0].split("\n")
        if line.strip()
        and not any(
            line.lstrip().startswith(prefix)
            for prefix in [
                "PROJECT SUMMARY:",
                "Contact PD/PI:",
                "Project Summary/Abstract",
                "Page",
            ]
        )
    ]

    num_lines = len(doc_text)

    if num_lines <= 30:
        return "Exceeding line limit"


def main():
    pdf_path = "../Docs/Application/Amalgent_Sept4_FT_Application_Submitted.pdf"
    section_title = "PROJECT SUMMARY"
    doc = get_pdf_document(pdf_path)

    toc = doc.get_toc()
    start_page = find_section_page(toc, section_title)
    next_section_page = find_next_section_page(toc, section_title)

    if start_page is not None:
        end_page = next_section_page - 1 if next_section_page is not None else len(doc)
        print(
            f"The '{section_title}' section starts on page {start_page} and ends on page {end_page}."
        )

    Content = extract_section_content(doc, section_title)
    Error = count_summary_length(Content)
    print(Error)


if __name__ == "__main__":
    main()
