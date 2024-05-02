import os
import glob
import shutil
import uuid
from typing import Any, List, Optional
import hashlib
from server import common
from fastapi import UploadFile
from llama_index.core import Document

MEMORY_FOLDER = "memories"
TMP_FOLDER = "tmp"
TMP_DOCUMENT_PATH = common.app_path(os.path.join(MEMORY_FOLDER, TMP_FOLDER))
PARSED_FOLDER = "parsed"
PARSED_DOCUMENT_PATH = common.app_path(os.path.join(MEMORY_FOLDER, PARSED_FOLDER))

# @TODO Add funcs to convert any original file's contents to text format and save to .md file.


def create_checksum(file_path: str):
    BUF_SIZE = 65536
    try:
        sha1 = hashlib.sha1()
        with open(file_path, "rb") as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha1.update(data)
        digest = sha1.hexdigest()
        print(f"{common.PRNT_EMBED} SHA1: {digest}", flush=True)
        return digest
    except Exception as err:
        print(f"{common.PRNT_EMBED} Failed to hash as file {err}", flush=True)
        return ""


def create_file_name(id: str, input_file_name: str):
    file_extension = input_file_name.rsplit(".", 1)[1]
    file_name = f"{id}.{file_extension}"
    return file_name


# Create a filename for a parsed markdown document
def create_parsed_id(collection_name: str):
    id = str(uuid.uuid4()).replace("-", "")
    # return f"{collection_name}--{id}"
    return id


def get_file_type_from_path(path: str):
    file_extension = path.rsplit(".", 1)[1]
    return file_extension


def check_is_url_file(path_ext: str):
    file_extension = get_file_type_from_path(path_ext)
    supported_ext = (
        "txt",
        "md",
        "mdx",
        "doc",
        "docx",
        "pdf",
        "rtf",
        "csv",
        "json",
        "xml",
        "xls",
    )
    is_supported_file = file_extension.lower().endswith(supported_ext)
    print(f"{common.PRNT_EMBED} Check is url a file: {file_extension}", flush=True)
    return is_supported_file


def check_file_support(file_ext: str):
    # Check supported file types
    file_extension = get_file_type_from_path(file_ext)
    supported_ext = (
        "txt",
        "md",
        "mdx",
        "doc",
        "docx",
        "pdf",
        "rtf",
        "csv",
        "json",
        "xml",
        "xls",
        "pptx",
        "jpg",
        "jpeg",
        "png",
        "gif",
        "mp3",
        "mp4",
        # "html",
        # "htm",
        # "orc",
    )
    is_supported = file_extension.lower().endswith(supported_ext)
    print(f"{common.PRNT_EMBED} Check extension: {file_extension}", flush=True)
    return is_supported


# Define a dynamic document parser to convert basic text contents to markdown format
# @TODO This will be CPU intensive and should be done in thread (if performed locally)
def process_documents(nodes: List[Document]) -> List[Document]:
    try:
        # Loop thru parsed document contents
        # ...
        # @TODO Copied text should be parsed and edited to include markdown syntax to describe important bits (headings, attribution, links)
        # @TODO Copied contents may include things like images/graphs that need special parsing to generate an effective text description
        # @TODO Ai Generate name, descr, tags if not present based on parsed text content ...
        print(f"{common.PRNT_EMBED} Successfully processed {nodes}", flush=True)
        return nodes
    except (Exception, ValueError, TypeError, KeyError) as error:
        print(f"{common.PRNT_EMBED} Document processing failed: {error}", flush=True)


async def copy_file_to_disk(
    app: Any,
    url_path: str,  # web, could be a file or html
    text_input: str,  # text from client
    file: UploadFile,  # file from client
    id: str,
    file_path: Optional[str] = "",  # local path on server
) -> dict:
    try:
        file_name = ""
        tmp_input_file_path = ""
        tmp_folder = TMP_DOCUMENT_PATH
        # Save temp files to disk first
        if url_path:
            ext = get_file_type_from_path(url_path)
            if not check_file_support(ext):
                raise Exception("Unsupported file format.")
            if not os.path.exists(tmp_folder):
                os.makedirs(tmp_folder)
            # Download asset from url or use external service for websites
            file_name = create_file_name(id=id, input_file_name=url_path)
            if check_is_url_file(ext):
                print(
                    f"{common.PRNT_API} Downloading file from url {url_path} to {tmp_input_file_path}"
                )
                # Download the file and save to disk
                tmp_input_file_path = os.path.join(tmp_folder, file_name)
                await common.get_file_from_url(url_path, tmp_input_file_path, app)
            else:
                print(
                    f"{common.PRNT_API} Cannot save website to disk. Will use loader instead: {url_path}"
                )
                tmp_input_file_path = url_path
        elif text_input:
            print(f"{common.PRNT_API} Saving raw text to file...\n{text_input}")
            # @TODO Do input sanitation here...
            if not os.path.exists(tmp_folder):
                os.makedirs(tmp_folder)
            # Write to file
            file_name = create_file_name(id=id, input_file_name="content.txt")
            tmp_input_file_path = os.path.join(tmp_folder, file_name)
            with open(tmp_input_file_path, "w") as f:
                f.write(text_input)
        elif file_path:
            # Read file from local path
            print(f"{common.PRNT_API} Reading local file from disk...{file_path}")
            ext = get_file_type_from_path(file_path)
            if not os.path.exists(file_path):
                raise Exception("File does not exist.")
            if not check_file_support(ext):
                raise Exception("Unsupported file format.")
            # Copy the file to the destination folder
            file_name = create_file_name(id=id, input_file_name=file_path)
            tmp_input_file_path = os.path.join(tmp_folder, file_name)
            if not os.path.exists(tmp_folder):
                os.makedirs(tmp_folder)
            shutil.copyfile(file_path, tmp_input_file_path)
        elif file:
            print(f"{common.PRNT_API} Saving uploaded file to disk...")
            ext = get_file_type_from_path(file.filename)
            if not os.path.exists(tmp_folder):
                os.makedirs(tmp_folder)
            if not check_file_support(ext):
                raise Exception("Unsupported file format.")
            # Read the uploaded file in chunks of 1mb
            file_name = create_file_name(id=id, input_file_name=file.filename)
            tmp_input_file_path = os.path.join(tmp_folder, file_name)
            with open(tmp_input_file_path, "wb") as f:
                while contents := file.file.read(1024 * 1024):
                    f.write(contents)
            file.file.close()
        else:
            raise Exception("Please supply a file path or url.")
        return {
            "document_id": file_name,
            "file_name": file_name,
            "path_to_file": tmp_input_file_path,
            "checksum": create_checksum(tmp_input_file_path),
        }
    except Exception as err:
        print(f"{common.PRNT_EMBED} Failed to copy to disk: {err}")


# Wipe all parsed files
def delete_all_files():
    if os.path.exists(TMP_DOCUMENT_PATH):
        files = glob.glob(f"{TMP_DOCUMENT_PATH}/*")
        for f in files:
            os.remove(f)  # del files
        os.rmdir(TMP_DOCUMENT_PATH)  # del folder
    if os.path.exists(PARSED_DOCUMENT_PATH):
        files = glob.glob(f"{PARSED_DOCUMENT_PATH}/*.md")
        for f in files:
            os.remove(f)  # del all .md files
        os.rmdir(PARSED_DOCUMENT_PATH)  # del folder
