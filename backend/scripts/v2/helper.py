import fitz

def get_pdf_document(file_path):
    """Open the PDF document."""
    return fitz.open(file_path)

def extract_text_between_markers(text, start_marker, end_marker):
    """Extract text between two markers."""
    start_index = text.find(start_marker) + len(start_marker)
    end_index = text.find(end_marker)
    if start_index != -1 and end_index != -1:
        return text[start_index:end_index].strip()
    return ""

def count_non_empty_entries(text):
    """Count non-empty entries in text."""
    return len([entry for entry in text.split("\n") if entry.strip()])

def find_section_page(toc, section_title):
    """Find the start page of the specified section."""
    for level, title, page_number in toc:
        if section_title.lower() in title.lower():
            return page_number
    return None

def find_next_section_page(toc, current_section_title):
    """Find the start page of the next section."""
    found_current = False
    for level, title, page_number in toc:
        if found_current:
            return page_number
        if current_section_title.lower() in title.lower():
            found_current = True
    return None

def extract_section_content(doc, section_title):
    """Extract text from the specified section."""
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

def check_assurance_number(page_text, page_num, start_text, end_text):
    """Verify assurance number for subjects."""
    assurance_number = extract_text_between_markers(page_text, start_text, end_text)
    if assurance_number and assurance_number.lower() not in ["none"]:
        return f"False! Correct {start_text} required at page {page_num}."
    return None

def extract_text_from_doc(doc):
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text