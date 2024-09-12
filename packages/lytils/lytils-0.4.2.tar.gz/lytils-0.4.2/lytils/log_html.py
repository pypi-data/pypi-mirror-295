import os
from lytils.file import create_file_at_path

try:
    from airium import Airium
except ImportError:
    Airium = None


def join_styles(styles: dict):
    # Quotes need to be manually added as some styles don't require quotes
    # ex. colors, sizes, etc
    styles_list = []
    for s in styles:
        styles_list.append(f"{s}: {styles[s]};")
    return " ".join(styles_list) if styles_list else ""


def join_attrs(attrs: dict):
    attrs_list = []
    for a in attrs:
        attrs_list.append(f"{a}='{attrs[a]}'")
    return " ".join(attrs_list) if attrs_list else ""


class LogHTML:
    def __init__(self, path: str = "log.html", title: str = "", dark: bool = True):
        self.filename = path
        self.title = title if title else os.path.basename(path)
        self.dark = dark
        self.log = []
        self.paths = {}
        self.__a = Airium()
        self.__a("<!DOCTYPE html>")

    def append_divider(self):
        self.log.append("<hr>")

    def append_image(self, src: str, inline: bool = False):
        display = "inline" if inline else "block"
        self.log.append(f"<img src='{src}' style='display: {display};' />")

    def append_link(self, href: str, text: str = ""):
        text = text if text else href
        attrs = join_attrs({"href": href, "target": "_blank"})
        self.log.append(f"<a {attrs}>{text}</a>")

    def append_text(self, text: str):
        self.log.append(f"<p>{text}</p>")

    def generate_unique_path(self, path: str, name: str, ext: str):
        """
        Generate a unique file path by appending an index to the filename.

        Args:
            path (str): The directory where the file will be saved.
            name (str): The name of the file without the extension.
            ext (str): The file extension without the period.

        Returns:
            str: A unique file path with an appended index if necessary.
        """
        hash = f"{path}/{name}.{ext}"
        hash = hash.replace("//", "/")  # Account for any double slashes
        if hash not in self.paths:
            self.paths[hash] = 0
            return f"{path}/{name}_{0}.{ext}"
        else:
            self.paths[hash] += 1
            return f"{path}/{name}_{self.paths[hash]}.{ext}"

    def style_css(self):
        return """
            body.dark {
                background-color: #333333;
                color: #e0e0e0;

                a {
                    color: #66ccff
                }

                a:visited {
                    color: #bb00cc
                }
            }
            """

    def save(self):
        theme = "dark" if self.dark else "light"
        with self.__a.html(lang="en"):
            with self.__a.head():
                self.__a.meta(charset="utf-8")
                self.__a.title(_t=self.title)
                with self.__a.style():
                    self.__a(self.style_css())
            with self.__a.body(klass=theme):
                # Iterate over markup
                for item in self.log:
                    self.__a(item)

        create_file_at_path(self.filename)
        with open(self.filename, "w") as f:
            f.write(str(self.__a))
