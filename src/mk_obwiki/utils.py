import re

class ObWikiParser():
    """
    Class to parse markdown and convert them 
    to mkdocs format.
    """
    HEADING_RE = r'^#+\s'
    CODE_BLOCK_RE = r'^\s*```'

    def __init__(self):
        pass

    def _heading(self, line: str) -> str:
        return '#' + line

    def _code_block(self, line: str) -> str:
        # Check for code block start and end if we want more updates
        # on code block
        return line.replace('ln:false', '')

    def parse(self, markdown: str) -> str:
        """
        Takes a markdown file input returns a version
        with converted syntax
        """
        # Convert markdown line by line, then return it
        new_markdown = []
        for line in markdown.split():
            if re.search(self.CODE_BLOCK_RE, line):
                new_line = self._code_block(line)
            elif re.search(self.HEADING_RE, line):
                new_line = self._heading(line)
            else:
                new_line = line
            new_markdown.append(new_line)
        return '\n'.join(new_markdown)
