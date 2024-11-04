import os

from notion_manager.obsidian_formatter.config import OBSIDIAN_VAULT_PATH
from notion_manager.obsidian_formatter.metadata import (
    get_metadata_from_md_file,
    modify_metadata,
    modify_metadata_in_md_file,
)
from notion_manager.obsidian_formatter.utils import (
    get_files_in_subfolders,
    read_md_file,
    write_md_file,
)

folder_of_interest = "3 - RESOURCES/People"
list_of_files = [
    y
    for y in get_files_in_subfolders(
        root_folder=os.path.join(OBSIDIAN_VAULT_PATH, folder_of_interest)
    )
    if "attachments" not in y
]


for filename in list_of_files:
    name, md_file = read_md_file(
        os.path.join(OBSIDIAN_VAULT_PATH, folder_of_interest, filename)
    )

    metadata = get_metadata_from_md_file(md_file=md_file)

    new_metadata = modify_metadata(
        metadata,
        element_to_remove=[],
        element_to_modify={},
        element_to_add=[],
        element_to_rename={"creation date": "creation_date"},
    )

    new_md_file = modify_metadata_in_md_file(
        md_file=md_file, old_metadata=metadata, new_metadata=new_metadata
    )

    write_md_file(
        os.path.join(OBSIDIAN_VAULT_PATH, folder_of_interest, filename), new_md_file
    )
