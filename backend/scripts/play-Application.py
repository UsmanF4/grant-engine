import fitz
import re


def get_pdf_document(file_path):
    return fitz.open(file_path)


def find_section_page(toc, section_title):
    for entry in toc:
        level, title, page_number = entry
        if section_title.lower() in title.lower():
            return page_number
    return None


def find_next_section_page(toc, current_section_title):
    found_current = False
    for entry in toc:
        level, title, page_number = entry
        if found_current:
            return page_number
        if current_section_title.lower() in title.lower():
            found_current = True
    return None


def section_exists(doc, section_title):
    toc = doc.get_toc()
    page_number = find_section_page(toc, section_title)
    return page_number is not None


def check_figure_sequence_in_section(doc, start_page, end_page):
    errors = []
    figure_pattern = re.compile(r"Figure\s+(\d+)\.\s")
    last_figure_number = 0
    print(f"Checking figures from page {start_page} to {end_page}")

    for page_num in range(start_page - 1, end_page):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        images = page.get_images(full=True)

        if images:
            last_image_index = images[-1][0]  # Get the index of the last image
            text_after_last_image = text.split(images[-1][7])[
                -1
            ]  # Get text after the last image
        else:
            text_after_last_image = text

        figures = figure_pattern.findall(text_after_last_image)
        print(f"Page {page_num + 1} has figures: {figures}")

        for figure in figures:
            figure_number = int(figure)
            if figure_number != last_figure_number + 1:
                errors.append(
                    f"Figure number is out of sequence on page {page_num + 1} for figure {figure_number}."
                )
            last_figure_number = figure_number

    return errors


def main():
    pdf_path = "Docs/LightSeed_Application_Preview 1.pdf"
    section_title = "Research strategy"
    doc = get_pdf_document(pdf_path)

    # Verify if the section exists
    toc = doc.get_toc()
    start_page = find_section_page(toc, section_title)
    next_section_page = find_next_section_page(toc, section_title)

    if start_page is not None:
        if next_section_page is not None:
            end_page = next_section_page - 1
        else:
            end_page = len(doc)
        print(
            f"The '{section_title}' section starts on page {start_page} and ends on page {end_page}."
        )

        # Check the sequence of figures in the section
        errors = check_figure_sequence_in_section(doc, start_page, end_page)
        if errors:
            for error in errors:
                print(error)
        else:
            print("All figures in the section are in correct sequence.")
    else:
        print(f"The '{section_title}' section was not found in the Table of Contents.")


if __name__ == "__main__":
    main()
