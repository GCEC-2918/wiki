# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GCEC Wiki'
copyright = '2023, GCEC Wiki Authors. GCEC Griffin © Copyright Gary Fern'
author = 'GCEC Members'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_rtd_theme',
    'sphinx-favicon'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'monokai'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_style = 'css/custom-theme.css'
html_logo = 'logo.png'

html_theme_options = {
    'style_nav_header_background': '#ff9100'
}

favicons = [
    {"href": "_static/favicon/android-chrome-192x192.png"},
    {"href": "_static/favicon/android-chrome-512x512.png"},
    {"href": "_static/favicon/favicon-16x16.png"},
    {"href": "_static/favicon/favicon-32x32.png"},
    {"href": "_static/favicon/favicon.ico"},
    {
        "rel": "apple-touch-icon",
        "href": "_static/favicon/apple-touch-icon.png",
    }
]
