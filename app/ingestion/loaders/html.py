from bs4 import Tag
from bs4 import BeautifulSoup
import logfire

def parse_html(file_path: str):
    """
    Parses HTML content using BeautifulSoup.
    Cleans scripts, styles and extracts readable text for RAG.
    """
    with logfire.span("HTML Parsing", filename = file_path):
        try:
            with open(file_path, 'r', encoding = 'utf-8', errors = 'ignore') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')

            # 1. Remove Junk (Scripts, styles, Metadata)
            for script in soup[Tag](["script", "style", "meta","noscript"]):
                script.decompose()

            # 2. Extract the text output
            text = soup.get_text(separator = "\n")

            # 3. Clean whitespace (collapse multiple newLines)
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split(""))
            text_clean = "\n".join(chunk for chunk in chunks if chunk)

            return text_clean

        except Exception as e:
            logfire.error(f"HTML Parse Failed: {e}")
            raise e    

            
                