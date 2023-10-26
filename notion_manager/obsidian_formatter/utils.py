import os
import re


def get_files_in_subfolders(root_folder):
    files = []
    for root, dirs, filenames in os.walk(root_folder):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


def read_md_file(file_path):
    """
    Read a markdown file and return its name and content

    :param file_path: path to the markdown file
    :return: name of the file, content of the file
    """
    with open(file_path, "r") as f:
        return file_path.split("/")[-1], f.read()


def write_md_file(file_path, md_file):
    with open(file_path, "w") as f:
        f.write(md_file)


def retrieve_date_from_file_name_if_exists(file_name):
    # Use regular expressions to extract the date
    date_match = re.search(r"\d{4}-\d{2}-\d{2}", file_name)

    if date_match:
        date = date_match.group()
        return date
    return None


def clean_metadata(metadata):
    """
    Clean the metadata
    """
    metadata = metadata.replace(" |-", "").replace("-|", "")
    metadata = metadata.replace(" - ", "")
    return metadata.strip()
