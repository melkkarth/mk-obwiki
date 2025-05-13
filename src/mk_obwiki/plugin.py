from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

from mk_obwiki.utils import ObWikiParser

class ObWikiPlugin(BasePlugin):
    """
    Obsidian Wiki Plugin
    """
    config_scheme = {}

    def on_page_markdown(self, markdown: str, /, *, page, config, files) -> str | None:
        parser = ObWikiParser()
        return parser.parse(markdown)
