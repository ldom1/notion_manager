import re
from typing import Tuple


def extract_values_from_people_file(md_file: str) -> Tuple[str, str, str]:
    """
    Extract data from a markdown file
    The metadata of the markdown file should be formatted as follows:
    ...
    [
        ...,
        ***linkedin profile:*** [linkedin profile],
        ***email pro:*** [email pro],
        ***email perso:*** [email perso],
        ...
    ]

    :param md_file: The markdown file to extract the values from
    :return: linkedin_profile, email_pro, email_perso
    """
    md_file_lines = md_file.split("\n")

    # Extract the metadata from the template
    linkedin_profile = None
    email_pro = None
    email_perso = None

    for line in md_file_lines:
        if line.strip():
            if "***linkedin profile:***" in line:
                line = line.replace("***", "")
                linkedin_profile = "".join(line.split(":")[1:]).strip()
            elif "***email pro:***" in line:
                line = line.replace("***", "")
                email_pro = line.split(":")[1].strip()
            elif "***email perso:***" in line:
                line = line.replace("***", "")
                email_perso = line.split(":")[1].strip()

    return linkedin_profile, email_pro, email_perso
