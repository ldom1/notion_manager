import re


def get_tags_from_md_file(md_file):
    """
    Extract the tags from a markdown file

    :param md_file: content of the markdown file
    :return: list of tags
    """
    # Extract the hashtags from the template
    hashtag_match = re.search(r"#(.*?)$", md_file, re.MULTILINE)
    if hashtag_match:
        hashtags = hashtag_match.group(1).strip().split(" #")
    return hashtags


def remove_tags_from_md_file(md_file):
    """
    Remove the tags from a markdown file

    :param md_file: content of the markdown file

    :return: markdown file without tags
    """
    return re.sub(r"#(.*?)$", "", md_file, flags=re.MULTILINE)
