#Chunking

from typing import List
import logfire

def chunk_text(text: str, chunk_size: int = 1500) -> List[str]:
    """
    Simple semantic-ish chunker that splits by paragraphs.
    Ensures chunks do not exceed the specified size.
    """

    with logfire.span("Text Chunking", text_lenght = len(text)):
        if not text.strip():
            return []

        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""

        for p in paragraphs:
            if len(current_chunk) + len(p) < chunk_size:
                chunks.append(current_chunk.strip())
            current_chunk += p +  "\n\n"

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks      