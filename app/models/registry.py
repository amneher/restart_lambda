"""
Registry:
 user (owner)
 create_date
 updated
 invitees
 private/public
 items

WP 'restart-registry' custom post type:
{
    "restart-registry": {
        "name": "restart-registry",
        "label": "Registries",
        "singular_label": "Registry",
        "description": "Consists of a user\\'s story, info, and list of items they wished for.",
        "public": "true",
        "publicly_queryable": "true",
        "show_ui": "true",
        "show_in_nav_menus": "true",
        "delete_with_user": "false",
        "show_in_rest": "true",
        "rest_base": "restart-registry",
        "rest_controller_class": "",
        "rest_namespace": "",
        "has_archive": "false",
        "has_archive_string": "",
        "exclude_from_search": "false",
        "capability_type": "post",
        "hierarchical": "false",
        "can_export": "false",
        "rewrite": "true",
        "rewrite_slug": "",
        "rewrite_withfront": "true",
        "query_var": "true",
        "query_var_slug": "",
        "menu_position": "",
        "show_in_menu": "true",
        "show_in_menu_string": "",
        "menu_icon": null,
        "register_meta_box_cb": null,
        "supports": [
            "title",
            "editor",
            "thumbnail",
            "excerpt",
            "trackbacks",
            "custom-fields",
            "comments",
            "revisions",
            "author",
            "page-attributes",
            "post-formats",
        ],
        "taxonomies": ["category", "post_tag"],
        "labels": {
            "menu_name": "Restart Registry",
            "all_items": "All Registries",
            "add_new": "Create a Registry",
            "add_new_item": "Add Item to Registry",
            "edit_item": "Edit Registry",
            "new_item": "New Registry",
            "view_item": "View Registry",
            "view_items": "View Registry Items",
            "search_items": "Search Ites",
            "not_found": "No Registries Found",
            "featured_image": "Your beautiful mug",
            "set_featured_image": "Set Mugshot",
            "remove_featured_image": "Remove Mugshot",
            "use_featured_image": "Use as your glam pic",
            "archives": "Registry Archives",
            "not_found_in_trash": "",
            "parent_item_colon": "",
            "insert_into_item": "",
            "uploaded_to_this_item": "",
            "filter_items_list": "",
            "items_list_navigation": "",
            "items_list": "",
            "attributes": "",
            "name_admin_bar": "",
            "item_published": "",
            "item_published_privately": "",
            "item_reverted_to_draft": "",
            "item_trashed": "",
            "item_scheduled": "",
            "item_updated": "",
            "template_name": "",
        },
        "custom_supports": "",
        "enter_title_here": "My Headline",
    }
    'restart-registry': PostType(name='Registries', slug='restart-registry', description="Consists of a user's story, info, and list of items they wished for.", hierarchical=False, has_archive=False, rest_base='restart-registry', rest_namespace='wp/v2', taxonomies=['category', 'post_tag'], capabilities={}, labels={}, supports={}, icon=None, viewable=True, visibility={}),
}


"""

from pydantic import BaseModel, ConfigDict, Field


class RegistryBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)


class RegistryCreate(RegistryBase):
    pass


class RegistryUpdate(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)


class Registry(RegistryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
