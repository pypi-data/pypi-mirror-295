from typing import TYPE_CHECKING, Any, Callable

from bs4 import BeautifulSoup

from .component import Component, weba_html_context
from .env import env
from .tag.context_manager import TagContextManager

if TYPE_CHECKING:
    from bs4 import Tag


class UIFactory:
    """
    A factory class for creating UI elements dynamically based on tag names.
    """

    def __getattr__(self, tag_name: str) -> Callable[..., TagContextManager]:
        def create_tag(*args: Any, **kwargs: Any) -> TagContextManager:
            html_context = weba_html_context.get(None)
            is_first = False

            if not html_context or html_context and str(html_context) == "None" or not callable(html_context.new_tag):
                html_context = Component()
                is_first = True

            if tag_name == "text":
                tag: Tag = html_context.new_string(str(args[0]))  # type: ignore
            elif tag_name == "raw":
                html = str(args[0])
                parser = env.xml_parser if html.startswith("<?xml") else env.html_parser
                tag: Tag = BeautifulSoup(html, parser)
            else:
                tag: Tag = html_context.new_tag(tag_name, **kwargs)  # type: ignore
                if args:
                    tag.string = str(args[0])

            if not isinstance(tag, TagContextManager):
                tag = TagContextManager(tag, html_context)  # type: ignore

            html_context._append_to_context(tag._tag)  # type:ignore

            if not is_first:
                html_context._last_component = tag  # type: ignore

            return tag

        return create_tag


ui = UIFactory()
