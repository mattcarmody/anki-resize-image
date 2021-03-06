import json

from anki.hooks import wrap
from anki.lang import _
from aqt import gui_hooks, mw
from aqt.editor import Editor

from .config import getUserOption


def setBrowserResizeImage(web_content, context):
    if not isinstance(context, Editor):
        return
    addon_package = mw.addonManager.addonFromModule(__name__)
    web_content.css.append(f"/_addons/{addon_package}/web/jquery-ui.css")
    web_content.js.append(f"/_addons/{addon_package}/web/js.js")
    web_content.js.append(f"jquery-ui.js")

    style = getUserOption("resizable-style", "border:1px dashed black;")
    css = []
    js = []
    if style:
        css.append(f".ui-wrapper {{   {style} }}\n")
    for m, default, suffix in [
            ("min", 10, ""),
            ("max", 200, " when not resizing")
    ]:
        for direction in ["width", "height"]:
            if getUserOption(f"apply {m}imum {direction}{suffix}", False):
                limit = getUserOption(f"{m}-{direction}", default)
                css.append(f""".field img {{{m}-{direction}: {limit}px}}""")
                js.append(f"""{m}_{direction} = "{limit}";""")
            else:
                js.append(f"""{m}_{direction} = null;""")
    image_classes = getUserOption("image-classes", {})
    image_classes = json.dumps(image_classes)
    js.append(f"""image_classes = {image_classes};""")
    js.append(
        f"""preserve_ratio={json.dumps(getUserOption("preserve ratio while resizing", "current"))}""")
    web_content.head += (f"""
<style>""" + "\n".join(css) + """</style>
<script>""" + "\n".join(js) + """</script>""")


mw.addonManager.setWebExports(__name__, r"web/.*(css|js)")
gui_hooks.webview_will_set_content.append(setBrowserResizeImage)
