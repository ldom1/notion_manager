import os

from notion_manager.obsidian_formatter.config import OBSIDIAN_VAULT_PATH
from notion_manager.obsidian_formatter.metadata import (
    add_metadata_to_md_file,
    generate_md_file_metadata,
)
from notion_manager.obsidian_formatter.tags import (
    get_tags_from_md_file,
    remove_tags_from_md_file,
)
from notion_manager.obsidian_formatter.utils import (
    read_md_file,
    retrieve_date_from_file_name_if_exists,
    write_md_file,
)

folder_of_interest = "3 - RESOURCES/Exposition"
list_of_files = [
    y
    for y in os.listdir(os.path.join(OBSIDIAN_VAULT_PATH, folder_of_interest))
    if ".md" in y
]

for filename in list_of_files:
    name, md_file = read_md_file(
        os.path.join(OBSIDIAN_VAULT_PATH, folder_of_interest, filename)
    )
    tags = get_tags_from_md_file(md_file=md_file)
    date = retrieve_date_from_file_name_if_exists(file_name=filename)

    metadata = generate_md_file_metadata(name.split("-")[0], tags, date)
    new_md_file = add_metadata_to_md_file(md_file, metadata)
    new_md_file = remove_tags_from_md_file(new_md_file)

    write_md_file(
        os.path.join(OBSIDIAN_VAULT_PATH, folder_of_interest, filename), new_md_file
    )
