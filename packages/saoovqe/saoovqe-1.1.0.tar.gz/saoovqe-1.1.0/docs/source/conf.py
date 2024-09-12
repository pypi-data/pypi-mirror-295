# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project
# -information

import os
import sys

# Location of Sphinx files
sys.path.insert(0, os.path.abspath('./../..'))

project = 'SA-OO-VQE'
copyright = '2023, Martin Beseda, Silvie Illésová, Saad Yalouz, Bruno Senjean'
author = 'Martin Beseda, Silvie Illésová, Saad Yalouz, Bruno Senjean'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general
# -configuration

extensions = [
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'myst_parser',
    'nbsphinx',
    'nbsphinx_link',
    'sphinx.ext.autodoc'
]

autodoc_mock_imports = ['qiskit_nature', 'qiskit', 'sympy', 'psi4', 'scipy',
                        'mendeleev', 'deprecated']

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for
# -html-output

html_theme = 'alabaster'
# html_static_path = ['_static']
