import fitz


def get_pdf_document(file_path):
    return fitz.open(file_path)


def count_elements(doc):
    element_count = 0
    for i in range(doc.page_count):
        page = doc[i]
        text = page.get_text("text")
        for line in text.split("\n"):
            if line.startswith("Element"):
                element_count += 1
    return element_count


def find_sub_elements(doc):
    sub_elements = []
    for i in range(doc.page_count):
        page = doc[i]
        text = page.get_text("text")
        for line in text.split("\n"):
            if line.startswith("Element"):
                start = text.find(line)
                end = text.find("Element", start + 1)
                if end == -1:
                    end = text.find("End of Element", start + 1)
                sub_element = text[start:end]
                sub_elements.append(sub_element)
    return sub_elements


def check_conditions_on_sub_elements(sub_elements):
    for sub_element in sub_elements:
        element_number = sub_element.split(":")[0]
        if (
            (sub_element.startswith("Element 1:"))
            or (sub_element.startswith("Element 4:"))
            or (sub_element.startswith("Element 5:"))
        ):
            for sub_line in sub_element.split("\n"):
                if sub_line.startswith("A."):
                    print(f"{element_number} - Element A found")
                if sub_line.startswith("B."):
                    print(f"{element_number} - Element B found")
                if sub_line.startswith("C."):
                    print(f"{element_number} - Element C found")


def main():
    file_path = "Docs/AG DMSP 20240102.pdf"
    doc = get_pdf_document(file_path)

    print("Number of pages: ", doc.page_count)

    element_count = count_elements(doc)
    if element_count != 6:
        print("Error: Number of elements: ", element_count)

    sub_elements = find_sub_elements(doc)
    check_conditions_on_sub_elements(sub_elements)


if __name__ == "__main__":
    main()
