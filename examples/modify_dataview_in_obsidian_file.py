import os

from notion_manager.obsidian_formatter.config import OBSIDIAN_VAULT_PATH
from notion_manager.obsidian_formatter.dataview import (
    get_data_view_from_md_file,
    modify_data_view,
    modify_multiple_data_view_in_md_file,
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
    if ".md" in y
]

"""
for filename in list_of_files:

    name, md_file = read_md_file(os.path.join(OBSIDIAN_VAULT_PATH, folder_of_interest, filename))

    data_view = get_data_view_from_md_file(md_file=md_file)

    mapping_old_view_new_data_view = {

        view: modify_data_view(view, element_to_replace='contains(tags,"project")', new_element='contains(type,"project")') if 'contains(tags,"project")' in view else modify_data_view(view, element_to_replace='contains(tags,"meeting")', new_element='contains(type,"meeting")') for view in data_view
    }

    new_md_file = modify_multiple_data_view_in_md_file(md_file=md_file, mapping_old_new_data_view=mapping_old_view_new_data_view)
    write_md_file(os.path.join(OBSIDIAN_VAULT_PATH, folder_of_interest, filename), new_md_file)

"""

for filename in list_of_files:
    name, md_file = read_md_file(
        os.path.join(OBSIDIAN_VAULT_PATH, folder_of_interest, filename)
    )

    data_view = get_data_view_from_md_file(md_file=md_file)

    mapping_old_view_new_data_view = {
        view: modify_data_view(
            view,
            element_to_replace=f'TABLE project_name as "Project Name", creation_date as "Creation Date", priority as "Priority"\nFROM [[{name.replace(".md", "")}]]\nWHERE contains(type,"meeting")',
            new_element=f'TABLE object as "Meeting object", date as "Date", related_project_name as "Related Project"\nFROM [[{name.replace(".md", "")}]]\nWHERE contains(type,"meeting")',
        )
        for view in data_view
        if "meeting" in view
    }

    new_md_file = modify_multiple_data_view_in_md_file(
        md_file=md_file, mapping_old_new_data_view=mapping_old_view_new_data_view
    )

    write_md_file(
        os.path.join(OBSIDIAN_VAULT_PATH, folder_of_interest, filename), new_md_file
    )
