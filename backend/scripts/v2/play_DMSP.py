import fitz
from helper import get_pdf_document, extract_text_from_doc

ELEMENTS = [
    "Element 1: Data Type",
    "Element 2: Related Tools, Software and/or Code",
    "Element 3: Standards",
    "Element 4: Data Preservation, Access, and Associated Timelines",
    "Element 5: Access, Distribution, or Reuse Considerations",
    "Element 6: Oversight of Data Management and Sharing",
]

CONDITIONS = {
    "Element 1:": "Element A found",
    "Element 4:": "Element A found",
    "Element 5:": "Element A found",
    "Element 2:": "Error: Element A found",
    "Element 3:": "Error: Element A found",
    "Element 6:": "Error: Element A found",
}


def check_elements(doc, exact_match=False):
    element_set = set(ELEMENTS)
    found_elements = set()
    text = extract_text_from_doc(doc)
    for line in text.split("\n"):
        for element in element_set:
            if (exact_match and line.strip() == element) or (
                not exact_match and line.startswith(element)
            ):
                found_elements.add(element)

    missing_elements = list(element_set - found_elements)
    return (
        [f"{element} is missing" for element in missing_elements]
        if missing_elements
        else "All elements are present" if not exact_match else "No error found"
    )


def find_sub_elements(doc):
    sub_elements = []
    element_set = set(ELEMENTS)
    text = extract_text_from_doc(doc)
    for line in text:
        for element in element_set:
            if line.startswith(element):
                start = text.find(line)
                end = len(text)
                for next_element in element_set:
                    next_start = text.find(next_element, start + 1)
                    if next_start != -1 and next_start < end:
                        end = next_start
                sub_element = text[start:end]
                sub_elements.append(sub_element)
    return sub_elements


def check_conditions_on_sub_elements(sub_elements):
    errors = []

    for sub_element in sub_elements:
        element_number = sub_element.split(":")[0]
        found = {"A": False, "B": False, "C": False}

        for element, message in CONDITIONS.items():
            if sub_element.startswith(element):
                sub_lines = sub_element.split("\n")
                found.update(
                    {
                        key: any(
                            sub_line.startswith(f"{key}.") for sub_line in sub_lines
                        )
                        for key in found
                    }
                )

                if element in ["Element 1:", "Element 4:", "Element 5:"]:
                    errors.extend(
                        f"{element_number} - Error: Element {key} not found"
                        for key, is_found in found.items()
                        if not is_found
                    )
                else:
                    errors.extend(
                        f"{element_number} - {message.replace('A', key)}"
                        for key, is_found in found.items()
                        if is_found
                    )

    return errors


def validate_DMSP(doc):
    errors = []
    element_errors = check_elements(doc, exact_match=False)
    if element_errors != "All elements are present":
        errors.extend(element_errors)
    sub_elements = find_sub_elements(doc)
    sub_element_errors = check_conditions_on_sub_elements(sub_elements)
    errors.extend(sub_element_errors)
    if not errors:
        errors.append("No errors found")
    return errors


def main():
    file_path = "../Docs/DMSP/Maipl_DMSP_Preview 1.pdf"
    doc = get_pdf_document(file_path)
    errors = validate_DMSP(doc)
    print(errors)


if __name__ == "__main__":
    main()
