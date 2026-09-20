import logfire
from unstructured.partition.auto import partition


def parse_office(file_path: str):
    """
    Parses office documents (.docx, .pptx) using the unstructured library.
    Unlike PDFs, these formats are structured and lightweight, so they are processed locally.
    """

    with logfire.span("Office Parsing", filename = file_path):
        try:
            # Unstructred  automatically detects if it's docx or pptx
            elements = partition(filename = file_path)
            full_text = "\n".join([str(el) for el in elements])

            if not full_text.strip():
                logfire.warning(f" Unstructured returned emtpy text for {file_path}")
            else:
                logfire.info(f"Succesfully parsed {len(full_text)} characters")

            return full_text

        except Exception as e:
            logfire.error(f"Office Parse failed: {e}")
            raise e
