from django.templatetags.static import static
from django.contrib.staticfiles.finders import find
from typing import TypedDict, Literal
from django.utils.html import format_html
from django import template
from django.conf import settings
import os

__all__ = ["vite_asset"]


class Settings(TypedDict):
    DEBUG: bool
    HOST: str
    PORT: int
    BASE: str


register = template.Library()


@register.simple_tag
def vite_asset(file: str, **attributes):
    app_settings = get_app_settings()

    debug = app_settings.get("DEBUG", False)
    host = app_settings.get("HOST", "localhost")
    port = app_settings.get("PORT", 5173)
    base = app_settings.get("BASE", "")
    filetype = parseFile(file)

    # TODO This can return List[str] or str or None (Handle Those Cases)
    file_abs = find(file.lstrip("/"))
    print(file_abs)
    static_url = os.path.relpath(file_abs, settings.BASE_DIR)

    # Generating Response Body
    response = None
    if debug:
        if filetype:
            response = format_html(
                '<script src="http://{}:{}{}/{}" type="module"',
                host,
                port,
                base.removeprefix("/"),
                static_url.removeprefix("/"),
            )
    else:
        if filetype == "StyleSheet":
            response = format_html('<link rel="stylesheet" href="{}"', static(file))

        elif filetype == "JavaScript":
            response = format_html('<script src="{}"', static(file))

    # Adding User's Attribute
    if filetype:
        for key, value in attributes.items():
            response += format_html(' {}="{}"', key, value)

    # Closing Tag
    if filetype == "StyleSheet" and not debug:
        response += format_html(">")
    elif filetype == "JavaScript":
        response += format_html("></script>")
    elif debug:
        response += format_html("></script>")

    return response


def get_app_settings() -> Settings:
    return getattr(
        settings,
        "DJANGO_VITE",
        {
            "DEBUG": getattr(settings, "DEBUG", False),
            "HOST": "localhost",
            "PORT": 5173,
            "BASE": "",
        },
    )


def parseFile(file: str) -> Literal["JavaScript", "StyleSheet", None]:
    _, ext = os.path.splitext(file)
    if ext == ".js":
        return "JavaScript"
    elif ext == ".css":
        return "StyleSheet"
    else:
        return None
