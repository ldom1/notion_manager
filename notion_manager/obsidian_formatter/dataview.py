import re


def get_data_view_from_md_file(md_file):
    """
    Extract the dataview from a markdown file

    :param md_file: content of the markdown file
    :return: dataview
    """

    metadata_match = re.findall(
        r"```dataview(.*?)```", md_file, re.MULTILINE | re.DOTALL
    )

    if metadata_match:
        return metadata_match

    else:
        raise Exception(
            f"""
            No dataview found in the markdown file:
            {md_file}
            """
        )


def modify_data_view(data_view, element_to_replace, new_element):
    """
    Modify a dataview

    :param data_view: dataview
    :param element_to_replace: element to replace
    :param new_element: new element

    :return: modified dataview
    """
    return data_view.replace(element_to_replace, new_element)


def modify_data_view_in_md_file(md_file, old_data_view, new_data_view):
    """
    Modify a dataview in a markdown file

    :param md_file: content of the markdown file
    :param old_data_view: old dataview
    :param new_data_view: new dataview

    :return: modified markdown file
    """
    return md_file.replace(old_data_view, new_data_view)


def modify_multiple_data_view_in_md_file(md_file, mapping_old_new_data_view):
    """
    Modify multiple dataviews in a markdown file

    :param md_file: content of the markdown file
    :param mapping_old_new_data_view: mapping of old dataviews to new dataviews

    :return: modified markdown file
    """
    for old_data_view, new_data_view in mapping_old_new_data_view.items():
        md_file = modify_data_view_in_md_file(md_file, old_data_view, new_data_view)
    return md_file
