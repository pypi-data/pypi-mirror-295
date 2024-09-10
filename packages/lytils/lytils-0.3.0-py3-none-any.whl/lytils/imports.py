import ast
import inspect
import importlib
from lytils import ctext


class MissingImportsException(Exception):
    # Raise this when undetected_chromedriver is not installed
    def __init__(self, message: str):
        self.message = ctext(f"<y>{message}")
        super().__init__(self.message)


def get_imports(filename):
    with open(filename, "r") as file:
        code = file.read()

    tree = ast.parse(code)
    imports = [
        node.module if isinstance(node, ast.ImportFrom) else node.names[0].name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
    ]
    return imports


def raise_missing_imports(missing_imports, method: str = "poetry"):
    """
    Raise an exception if there are missing imports.

    Args:
        method (str, optional): The method to install missing imports. Defaults to "poetry". Can also pass "pip".
    """
    if missing_imports:
        prefix = ""
        if method == "poetry":
            prefix = "poetry add "
        elif method == "pip":
            prefix = "pip install "
        message = 'Try running "' + prefix + " ".join(missing_imports) + '"'
        raise MissingImportsException(message)


def verify_imports(filename: str = "main.py", method: str = "poetry"):
    """
    Verify that all imports are installed.

    Args:
        filename (str, optional): The filename to verify imports. Defaults to "main.py".
        method (str, optional): The method to install missing imports. Defaults to "poetry". Can also pass "pip".
    """
    imports = get_imports(filename)
    missing_imports = []
    for module in imports:
        try:
            importlib.import_module(module)
        except ImportError:
            missing_imports.append(module)

    raise_missing_imports(missing_imports, method)
