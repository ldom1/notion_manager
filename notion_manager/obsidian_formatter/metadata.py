import datetime
import re
import textwrap

import yaml


def generate_md_file_metadata(name, tags, content_type, date=None):
    """
    Generate the metadata for a markdown file

    :param name: name of the file
    :param tags: list of tags
    :param date: date of the file

    :return: metadata
    """

    if content_type == "exposition":
        content = "exposition"
        type_ = "art"

    metadata = f"""
    ---
    name: {name}
    content: {content}
    type: {type_}
    tags: {', '.join(tags)}
    date: {date if date else datetime.datetime.now().strftime("%Y-%m-%d")}
    ---\n
    """
    return textwrap.dedent(metadata)


def add_metadata_to_md_file(md_file, metadata):
    """
    Add metadata to a markdown file

    :param md_file: content of the markdown file
    :param metadata: metadata to add to the markdown file

    :return: markdown file with metadata
    """
    return f"{metadata}{md_file}"


def get_metadata_from_md_file(md_file):
    """
    Extract the metadata from a markdown file

    :param md_file: content of the markdown file

    :return: metadata
    """
    # Extract the metadata from the template
    metadata_match = re.search(r"---(.*?)---", md_file, re.MULTILINE | re.DOTALL)
    if metadata_match:
        metadata = metadata_match.group(1).strip()
        return metadata
    else:
        raise Exception(
            f"""
            No metadata found in the markdown file:
            {md_file}
            """
        )


def parse_metadata(metadata):
    """
    Parse the metadata of a markdown file

    :param metadata: metadata of the markdown file

    :return: parsed metadata
    """
    # Parse the metadata
    return yaml.safe_load(metadata)


def modify_metadata(
    metadata,
    element_to_remove: list,
    element_to_modify: dict,
    element_to_add: list,
    element_to_rename: dict,
):
    """
    Modify the metadata of a markdown file

    :param metadata: metadata of the markdown file
    :return: modified metadata

    Example:
    metadata =
    ---
    name: test
    content: exposition
    type: art
    tags: test, test2
    date: 2021-06-01
    element_to_rename: test
    ---
    element_to_remove = ["name"]
    element_to_modify = {"tags": "test, test3"}
    element_to_add = ["creation_date: 2021-06-01: 12:00:00"]
    element_to_rename = {"element_to_rename": "element_renamed"}

    modified_metadata =
    ---
    content: exposition
    type: art
    tags: test, test3
    date: 2021-06-01
    creation_date: 2021-06-01: 12:00:00
    element_renamed: test
    ---
    """
    modified_metadata = metadata

    # Remove the elements from the metadata
    for element in element_to_remove:
        modified_metadata = _remove_one_element_in_metadata(
            metadata=modified_metadata, element=element
        )

    # Rename the keys of the elements in the metadata
    for old_key, new_key in element_to_rename.items():
        modified_metadata = _rename_key_of_one_element_in_metadata(
            metadata=modified_metadata, old_key=old_key, new_key=new_key
        )

    # Modify the elements in the metadata
    for element, new_value in element_to_modify.items():
        modified_metadata = _modify_one_element_in_metadata(
            metadata=modified_metadata, element=element, new_value=new_value
        )

    # Add the elements to the metadata
    for element in element_to_add:
        modified_metadata = _add_one_element_in_metadata(
            metadata=modified_metadata, element=element
        )

    return modified_metadata


def _remove_one_element_in_metadata(metadata, element):
    """
    Remove one element from the metadata

    :param metadata: metadata of the markdown file
    :param element: element to remove from the metadata

    :return: modified metadata
    """

    transformed_metadata = re.sub(rf"{element}:.*?\n", "", metadata)
    return transformed_metadata


def _modify_one_element_in_metadata(metadata, element, new_value):
    """
    Modify one element from the metadata

    :param metadata: metadata of the markdown file
    :param element: element to modify from the metadata
    :param new_value: new value of the element

    :return: modified metadata
    """

    transformed_metadata = re.sub(
        rf"{element}:(.*?)\n", f"{element}: {new_value}\n", metadata
    )
    return transformed_metadata


def _add_one_element_in_metadata(metadata, element: str):
    """
    Add one element in the metadata

    :param metadata: metadata of the markdown file
    :param element: element to add in the metadata

    :return: modified metadata
    """
    # Use regex to find the location where the new element should be added
    pattern = r"\ntags:(.*?)$"
    match = re.search(pattern, metadata, re.MULTILINE | re.DOTALL)

    if match:
        # Insert the new element after the "tags" line
        insertion_index = match.end()
        transformed_metadata = (
            metadata[:insertion_index]
            + "\n"
            + element
            + "\n"
            + metadata[insertion_index:]
        )
        return transformed_metadata
    else:
        raise ValueError(
            f"The metadata does not contain a 'tags' line, for metadata: {metadata}"
        )


def _rename_key_of_one_element_in_metadata(metadata, old_key, new_key):
    """
    Rename one element from the metadata

    :param metadata: metadata of the markdown file
    :param old_key: element to rename from the metadata
    :param new_key: new name of the element

    :return: modified metadata
    """
    transformed_metadata = metadata.replace(old_key, new_key)
    return transformed_metadata


def modify_metadata_in_md_file(md_file, old_metadata, new_metadata):
    """
    Modify the metadata of a markdown file

    :param md_file: content of the markdown file
    :param old_metadata: metadata to replace
    :param new_metadata: new metadata

    :return: modified markdown file
    """
    # Replace the metadata in the markdown file
    modified_md_file = md_file.replace(old_metadata, new_metadata)
    return modified_md_file
