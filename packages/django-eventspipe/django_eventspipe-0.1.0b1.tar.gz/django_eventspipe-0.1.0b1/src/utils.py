import json

from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

def get_sentinel_user() -> User:
    """
    Prevent pipeline removal when deleting an user
    """
    return get_user_model().objects.get_or_create(username="deleted")[0]

# https://stackoverflow.com/a/53092940
def linkify(field_name: str) -> str:
    """
    Converts a foreign key value into clickable links.
    
    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change
    """
    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return '-'
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = field_name  # Sets column name
    return _linkify

# https://stackoverflow.com/a/72256767
class PrettyJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, indent: int, sort_keys: bool, **kwargs):
        super().__init__(*args, indent=2, sort_keys=True, **kwargs)
