from anki.hooks import wrap
from anki.lang import _
from aqt.editor import *
from aqt.editor import Editor, _html

from .config import getUserOption
from .from_file import add_style_in_web, str_from_file_name


def setBrowserResizeImage(self):
    js = ["js", "jquery-ui"]
    css = ["jquery-ui"]
    self.web.eval("var limit_height = null;")
    self.web.eval("var limit_width = null;")
    if getUserOption("apply maximum height when not resizing", False):
        max_height = getUserOption("max-height", "200px")
        add_style_in_web(self, f"""#fields img {{max-height: {max_height} }}""")
        self.web.eval(f"""limit_height = "{max_height}";""")
    if getUserOption("apply maximum width when not resizing", False):
        max_width = getUserOption("max-width", "200px")
        add_style_in_web(self, f"""#fields img {{max-width: {max_width} }}""")
        self.web.eval(f"""limit_width = "{max_width}";""")
    css = "\n".join(str_from_file_name(f"{file}.css") for file in css)
    js = "\n".join(str_from_file_name(f"{file}.js") for file in js)
    add_style_in_web(self, css)
    self.web.eval(js)


Editor.setupWeb = wrap(Editor.setupWeb, setBrowserResizeImage)
