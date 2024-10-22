import fitz
from helper import get_pdf_document

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


def extract_text_from_doc(doc):
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text


def check_elements(doc, exact_match=False):
    element_set = set(ELEMENTS)
    found_elements = set()
    text = extract_text_from_doc(doc)
    element_count = {element: 0 for element in ELEMENTS}
    other_elements_found = False

    for line in text.split("\n"):
        for element in element_set:
            if (exact_match and line.strip() == element) or (
                not exact_match and line.startswith(element)
            ):
                found_elements.add(element)
                element_count[element] += 1

        if line.lower().startswith("element") and not any(
            line.startswith(element) for element in element_set
        ):
            other_elements_found = True

    missing_elements = list(element_set - found_elements)
    duplicate_elements = [element for element, count in element_count.items() if count > 1]

    errors = []
    if missing_elements:
        errors.extend([f"{element} is missing" for element in missing_elements])
    if duplicate_elements:
        errors.extend([f"{element} exists more than once" for element in duplicate_elements])
    if other_elements_found:
        errors.append("Other elements found that are not in the predefined list")
    if len(found_elements) != len(ELEMENTS):
        errors.append(f"Total elements found are not equal to {len(ELEMENTS)}")

    return errors if errors else "All elements are present"


def find_sub_elements(doc):
    sub_elements = []
    element_set = set(ELEMENTS)
    text = extract_text_from_doc(doc)

    for line in text.split("\n"):
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
    file_path = "../test/DMSP2 2.pdf"
    doc = get_pdf_document(file_path)
    errors = validate_DMSP(doc)
    print(errors)


if __name__ == "__main__":
    main()
