import json
import logging
import os
import re
import shutil

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.nav import Page, Section

logger = logging.getLogger(__name__)

class MarkdownParser():
    """
    Class to parse markdown and convert them 
    to mkdocs format.
    """
    HEADING_RE = r'^#+\s'
    CODE_BLOCK_RE = r'^\s*```'

    def __init__(self):
        self._code_block_start = False

    def _heading_parse(self, line: str) -> str:
        return '#' + line

    def _code_block_parse(self, line: str) -> str:
        # Each time a code block delimiter is found
        # toggle code block start flag
        new_line = line
        self._code_block_start = not self._code_block_start
        if self._code_block_start:
            # Check for code block start and end if we want more updates
            # on code block
            if 'ln:false' in line:
                new_line = line.replace('ln:false', '')
            else:
                new_line = line + ' linenums="1"'
        return new_line

    def parse(self, markdown: str) -> str:
        """
        Takes a markdown file input returns a version
        with converted syntax
        """
        # Convert markdown line by line, then return it
        new_markdown = []
        for line in markdown.splitlines():
            if re.search(self.CODE_BLOCK_RE, line):
                new_line = self._code_block_parse(line)
            elif re.search(self.HEADING_RE, line):
                new_line = self._heading_parse(line)
            else:
                new_line = line
            new_markdown.append(new_line)
        return '\n'.join(new_markdown)

class ObsidianIconsImport():
    """
    Class to import Obsidian icons to mkdocs.
    """
    PACKS_MAP = {
        'Bo':   'boxicons',
        'Co':   'coolicons',
        'Fi':   'feather-icons',
        'Fab':  'font-awesome-brands',
        'Far':  'font-awesome-regular',
        'Fas':  'font-awesome-solid',
        'Ib':   'icon-brew',
        'Li':   'lucide-icons',
        'Oc':   'octicons',
        'Ri':   'remix-icons',
        'Ra':   'rpg-awesome',
        'Si':   'simple-icons',
        'Ti':   'tabler-icons'
    }

    def __init__(self, config: MkDocsConfig):
        self._config = config
        self._icons_path = os.path.join(
            self._config['docs_dir'],
            '.obsidian',
            'icons'
        )
        icons_data = os.path.join(
            self._config['docs_dir'],
            '.obsidian',
            'plugins',
            'obsidian-icon-folder',
            'data.json'
        )
        with open(icons_data, 'r', encoding='utf-8') as fd:
            self._icons_map = json.load(fd)
        self._section_chain = []

    
    def _get_svg(self, title:str):
        icon_name = self._icons_map.get(title)
        if not icon_name:
            # Hack: Mkdocs capitilize section first letter, try to match title
            # by force using all lowercase
            logger.warning(
                '[ObsidianIconsImport] "%s" Icon Not Found, search by FORCE',
                title
            )
            for key in self._icons_map:
                if key.lower() == title.lower():
                    icon_name = self._icons_map.get(key)
                    break
            else:
                logger.warning('[ObsidianIconsImport] "%s" FORCE search FAIL', title)
                return None
        
        for key, value in self.PACKS_MAP.items():
            if icon_name.startswith(key):
                svg_name = icon_name.removeprefix(key) + '.svg'
                svg_path = os.path.join(self._icons_path, value, svg_name)
                break
        else:
            logger.warning('[ObsidianIconsImport] "%s" Pack Not Found', title)
            return None

        with open(svg_path, "r", encoding="utf-8") as fd:
            svg = fd.read()

        # Check if the SVG contains fill="none"
        if 'fill="none"' in svg:
            svg_class = "stroke-icon"
        else:
            svg_class = "fill-icon"

        # Inject class into the <svg> tag
        svg = svg.replace("<svg", f'<svg class="{svg_class}"', 1)
        return svg


    def apply_icon(self, item):
        # Handle Page (single note)
        if isinstance(item, Page):
            md_name = item.file.src_path.removesuffix(self._config['docs_dir'])
            page_name = os.path.splitext(os.path.basename(md_name))[0]
            svg = self._get_svg(md_name)
            if svg:
                item.title = f'<span class="nav-icon">{svg}</span> {page_name}'

        # Handle Section (folder)
        elif isinstance(item, Section):
            self._section_chain.append(item.title)
            md_name = os.path.join(*self._section_chain)
            svg = self._get_svg(md_name)
            if svg:
                item.title = f'<span class="nav-icon">{svg}</span> {item.title}'
            
            for child in item.children or []:
                self.apply_icon(child)
            self._section_chain.pop()



