# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# stevedore documentation build configuration file

# make openstackdocstheme an optional dependency. stevedore is a
# low level lib
# that is used outside of OpenStack. Not having something OpenStack specific
# as build requirement is a good thing.
try:
    import openstackdocstheme  # noqa
except ImportError:
    has_openstackdocstheme = False
else:
    has_openstackdocstheme = True


# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.graphviz',
    'sphinx.ext.extlinks',
    'stevedore.sphinxext',
]
if has_openstackdocstheme:
    extensions.append('openstackdocstheme')

# openstackdocstheme options
openstackdocs_repo_name = 'openstack/stevedore'
openstackdocs_auto_name = False
openstackdocs_bug_project = 'python-stevedore'
openstackdocs_bug_tag = ''

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'stevedore'
copyright = '2016, DreamHost'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'native'


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
if has_openstackdocstheme:
    html_theme = 'openstackdocs'


# -- Options for LaTeX output ---------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author,
# documentclass [howto/manual]).
latex_documents = [
    (
        'index',
        'stevedore.tex',
        'stevedore Documentation',
        'DreamHost',
        'manual'
    ),
]


# -- Options for extlinks extension ---------------------------------------

extlinks = {
    'issue': ('https://github.com/dreamhost/stevedore/issues/%s', 'issue '),
}


# -- Options for autodoc extension ----------------------------------------

autodoc_default_options = {
    'members': None,
    'special-members': None,
    'show-inheritance': None
}
