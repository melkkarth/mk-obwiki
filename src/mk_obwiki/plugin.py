import logging
import os
import shutil

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

from mk_obwiki.utils import ObsidianIconsImport
from mk_obwiki.utils import MarkdownParser

logger = logging.getLogger(__name__)

class ObWikiPlugin(BasePlugin):
    """
    Obsidian Wiki Plugin
    """
    config_scheme = {}

    def _assets_path(self, path):
        return os.path.join(os.path.dirname(__file__), path)

    def on_config(self, config):
        # Inject custom CSS
        config['extra_css'].append(f'stylesheets/extra.css')

        # Inject template override path (partials)
        override_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if os.path.isdir(override_dir):
            config['theme'].dirs.insert(0, override_dir)

        return config

    def on_page_markdown(self, markdown: str, page, config, files):
        parser = MarkdownParser()
        return parser.parse(markdown)

    def on_nav(self, nav, config, files):
        icons = ObsidianIconsImport(config)
        for item in nav.items:
            icons.apply_icon(item)
        return nav

    def on_post_build(self, config):
        # Copy static files (CSS)
        css_path = os.path.join(os.path.dirname(__file__), 'stylesheets', 'extra.css')
        dest_dir = os.path.join(config['site_dir'], 'stylesheets')
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy(css_path, os.path.join(dest_dir, 'extra.css'))

