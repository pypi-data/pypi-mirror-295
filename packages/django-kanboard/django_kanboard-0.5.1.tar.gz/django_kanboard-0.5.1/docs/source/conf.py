"""
Configuration for docs generation on django_kanboard application.

:creationdate: 29/06/2021 16:44
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: conf
"""
# -- Path setup --------------------------------------------------------------
import sys
from pathlib import Path

import sphinx_rtd_theme

# -- Project information -----------------------------------------------------
DEBUG = True
DEBUG and print("DEBUG::conf.py Current directory = ", Path(__file__).parent)  # noqa: T201
PROJECT_ROOT = Path(__file__).parents[3]
DEBUG and print("DEBUG::conf.py PROJECT_ROOT = ", PROJECT_ROOT)  # noqa: T201
PROJECT_SRC = PROJECT_ROOT
DEBUG and print("DEBUG::conf.py BASE_DIR = ", PROJECT_SRC)  # noqa: T201
sys.path.insert(0, str(PROJECT_SRC))
DEBUG and print("DEBUG::conf.py sys.path = ", sys.path)  # noqa: T201

project = "django-kanboard"
copyright = "2021, François GUÉRIN <fguerin@ville-tourcoing.fr>"  # noqa
author = "François GUÉRIN <fguerin@ville-tourcoing.fr>"

# The full version, including alpha/beta/rc tags
version = "0.5"
release = "0.5.1"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions: list[str] = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]

# Add any paths that contain templates here, relative to this directory.
templates_path: list[str] = [
    "_templates",
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: list[str] = [
    "./tmp",
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Options for intersphinx extension ---------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    # Django
    "django": (
        "https://docs.djangoproject.com/en/3.0/",
        "https://docs.djangoproject.com/en/3.0/_objects/",
    ),
    # Other packages
    "kanboard": (
        "https://docs.kanboard.org/en/latest/",
        None,
    ),
}
