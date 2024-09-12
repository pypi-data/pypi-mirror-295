import pandas as pd
import langchain_text_splitters as lcs
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.schema import Document
from docx2python import docx2python


def split_Docx_Recursive(path: str, separators=["\n\nTable_Start\n", "\n\n\n", "\n\n", "\n", " ", ""], chunk_size=1024, chunk_overlap=750) -> list[dict]:
    """
    Reads a docx file (i.e., a Word document) and splits it recursively on the specified separators.

    NOTE: Since the docx parser can separate text- and table-sections, these get separated by a '\\n\\nTable_Start\\n' and a\
        subsequent '\\n\\n\\n' from the text blocks. In order to keep a table together as a block when splitting the parsed text, \
        the list of separators should have those expressions as highest priority, since otherwise a lot of context can get lost.\
        This is the default, but when overriding the separators, this must be done manually.

    Args:
        path (str): The file path of the docx file. Can be absolute ('C:/foo/bar.docx') or relative ('./foo/bar.docx').
        separators (list): List of separators to split at. Priority: Left: High -> Right: Low.
        chunk_size (int): The maximum number of characters in split chunks.
        chunk_overlap (int): How far the individual chunks can overlap. Larger values mean more context for the individual chunks, but also more duplication between them.

    Returns:
        chunks (list[dict]): A list of dictionaries, which include the components 'page_content', 'properties', and 'name'. The latter describes the file name as specified in the path.
    """
    documentText = ""
    chunks = []
    try:
        doc = docx2python(path)
        text_splitter = lcs.RecursiveCharacterTextSplitter(separators=separators, chunk_size = chunk_size, chunk_overlap = chunk_overlap)

        """
        NOTE for future developers:
        The 'doc.body' part is divided into sections. These sections distinguish between text and tables;
        For example: If the Word document has a text with ONE table in between, the doc.body consists of a list with
        3 elements:
            doc.body[0] is the section with the text BEFORE the table
            doc.body[1] is the section WITH the table (and ONLY the table)
            doc.body[2] is the section with the text AFTER the table.
        Tables themselves are further divided into nested lists, which can be beautified with the Pandas module:
            pd.DataFrame(data=doc.body[X][1:], columns=[val[0] for val in doc.body[X][0]])
            (X for the Xth table section.)
        The text sections themselves are also nested: If you want to print each line individually with a for loop,
        you need to use doc.body[x][0][0] (X for the Xth text section).
        """
        
        for section in doc.body:
            # If the read block can be converted into a table, beautify it with Pandas...
            if not pd.DataFrame(section[1:]).empty:
                section = pd.DataFrame(data=section[1:], columns=[val[0] for val in section[0]])
                documentText += "\n\nTable_Start\n" + section.to_string() + "\n\n\n"
            # ... Otherwise, treat it like a normal text block.
            else:
                for row in section[0][0]:
                    documentText += row + "\n"

        splitted_chunks = text_splitter.split_text(documentText)
        for chunk in splitted_chunks:
            chunks.append({"page_content": chunk, "properties": doc.core_properties, "name": path.split('/')[-1]})

    except FileNotFoundError as e:
        raise FileNotFoundError(f"The document at path '{path}' does not exist / The path is invalid. Is the path spelled correctly in its entirety? Error: {e}")
    except PermissionError as e:
        raise PermissionError(f"The document at path '{path}' could not be opened. This usually occurs when the file is already opened by another program, or the file needs special access rights. Error: {e}")
    except:
        raise
    return chunks


def split_Pdf_Recursive(path, separators=["\n\n", "\n", " ", ""], chunk_size=1024, chunk_overlap=750) -> list[Document]:
    """
    Reads a PDF file and splits it recursively on the specified separators.

    Args:
    path (str): The file path of the PDF file. Can be absolute ('C:/foo/bar.pdf') or relative ('./foo/bar.pdf').
    separators (list): List of separators to split at. Priority: Left: High -> Right: Low.
    chunk_size (int): The maximum number of characters in split chunks.
    chunk_overlap (int): How far the individual chunks can overlap. Larger values mean more context for the individual chunks, but also more duplication between them.

    Returns:
        chunks (list[Document]): A list of dictionaries of type Document, including the components 'page_content' and 'metadata'. The latter describes properties of the PDF file such as title, etc.
    """
    try:
        loader = PyMuPDFLoader(path)
        chunks = loader.load_and_split(lcs.RecursiveCharacterTextSplitter(separators=separators, chunk_size=chunk_size, chunk_overlap=chunk_overlap))
    except AssertionError as e:
        raise AssertionError(f"The PDF splitter could not process the file. Does it have the correct format (.pdf)? Error: {e}")
    except ValueError as e:
        raise ValueError(f"The document at path '{path}' does not exist / The path is invalid. Is the path complete and correctly spelled? Error: {e}")
    except:
        raise

    return chunks


def split_Txt_Recursive(path, encoding="utf-8", separators=["\n\n", "\n", " ", ""], chunk_size = 1024, chunk_overlap = 750) -> list[str]:
    """
    Recursively splits a string on the specified separators.

    Args:
        path (str): The path to the text file to be split. Can be absolute ('C:/foo/bar.txt') or relative ('./foo/bar.txt').
        encoding (str): The encoding of the text file. Defaults to utf-8.
        separators (list): List of separators to split at. Priority: Left: High -> Right: Low.
        chunk_size (int): The maximum number of characters in split chunks.
        chunk_overlap (int): How far the individual chunks can overlap. Larger values mean more context for the individual chunks, but also more duplication between them.

    Returns:
        chunks (list[str]): The split chunks.
    """
    text_splitter = lcs.RecursiveCharacterTextSplitter(separators=separators, chunk_size = chunk_size, chunk_overlap = chunk_overlap)

    try:
        with open(path, mode="r", encoding=encoding) as doc:
            text = doc.read()
            chunks = text_splitter.split_text(text)
        doc.close()
    except LookupError as e:
        raise LookupError(f"The specified encoder '{encoding}' is not supported by Python. To get a list of supported encoders, refer to Python's 'encodings' module. A few popular examples are: 'ascii', 'utf-8', 'utf-16', 'latin-1'. Error: {e}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The specified path '{path}' does not contain the mentioned file. Is the path spelled correctly and does the file exist? Error: {e}")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"The text splitter could not decode a certain byte. This usually happens when the file does not have the correct format - Are you sure the specified file is a .txt file and is encoded with {encoding}? Error: {e}")
    except:
        raise

    return chunks
