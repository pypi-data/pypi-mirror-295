# Configuration file for the Sphinx documentation builder.
# Documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Setup root --------------------------------------------------------------
import os
import time

from dvttestkit import confluence_handler


def get_version():
    with open('version.txt', 'r') as f:
        current_version = f.read().strip()
    return current_version


project = 'dvtTestKit'
author = 'Dan Edens'
release = get_version()

master_doc = 'DvtKit_index'
todo_include_todos = False
# pygments_style = 'classic'
source_suffix = {'.rst': 'restructuredtext'}
exclude_patterns = ['build/*']
html_theme = "classic"
extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.coverage',
        'sphinxcontrib.confluencebuilder',
        'sphinx.ext.napoleon',
        'sphinx.ext.viewcode',
        ]

confluence_default_alignment = 'center'
# confluence_header_file = 'assets/header.tpl'
# confluence_footer_file = 'assets/footer.tpl'
# confluence_disable_ssl_validation = False
confluence_publish_debug = True

confluence_publish_onlynew = True


# confluence_publish_denylist = [
#     'index',
#     'foo/bar',
# ]

def generate_sphinx_config(theme='alabaster', pdf=False):
    """
    Generates a Sphinx configuration dictionary with the given theme.

    Args:
        theme (str): The name of the theme to use for HTML and HTML Help pages.
            Defaults to 'alabaster'.
        pdf (bool): Whether to generate settings for PDF output. Defaults to False.

    Returns:
        A dictionary containing the Sphinx configuration.
    """
    config = {
            'htmlhelp_basename':    'DVT Test Kit',
            'html_theme':           theme,
            'html_static_path':     [],
            'html_show_sourcelink': False,
            'html_show_sphinx':     False,
            'html_show_copyright':  False
            }

    if pdf:
        config['latex_engine'] = 'xelatex'
        config['latex_elements'] = {
                'papersize':    'letterpaper',
                'pointsize':    '10pt',
                'classoptions': ',oneside',
                'babel':        '\\usepackage[english]{babel}',
                'fontpkg':      '\\usepackage{fontspec}',
                'fncychap':     '\\usepackage[Bjornstrup]{fncychap}',
                'preamble':     '\\usepackage{unicode-math}\n\\setmathfont{XITS Math}\n\\setmainfont{XITS}\n'
                }

    return config


def publish_dvttestkit_to_confluence(pages):
    """
    Publishes files to Confluence pages and returns a string of return codes.

    :param pages: A list of tuples containing file names and corresponding page IDs. :type pages: List[Tuple[str, int]]
    :returns: A string containing return codes separated by newlines. :rtype: str
    :raises Exception: Raises an exception if update_confluence_page fails.

    >>> publish_dvttestkit_to_confluence([("file1", 123), ("file2", 456)])  
    "Return code for file1: 0\nReturn code for file2: 1\n"
    """
    result = ""
    for file_name, page_id in pages:
        try:
            return_code = confluence_handler.update_confluence_page(
                conf_file_path=file_name,
                page_id=page_id
            )
            result += f"Return code for {file_name}:{page_id}: {return_code}\n"
        except Exception as e:
            raise Exception(f"Failed to update {file_name}:{page_id} on Confluence: {e}")
    return result.strip()

        


def update_all_confluence_pages(root_page_id='15976006035'):
    """
    Updates all Confluence pages with the latest documentation.
    """
    pages = []
    for each in (confluence_handler.get_child_page_ids(root_page_id)):
        # print(confluence_handler.get_confluence_page_title(each))
        pages.append((confluence_handler.get_confluence_page_title(each), each))
    print(f"pre-publish_dvttestkit: {pages}")
    publish_dvttestkit_to_confluence(pages)

if __name__ == '__main__':
    docs_dir = os.path.abspath('docs')
    os.system(f"cd {docs_dir}")
    os.system("source ~/.zshenv")
    confluence_command = 'make build-doc'

    # Run the "make confluence" command
    os.system(confluence_command)

    # Update all Confluence pages
    update_all_confluence_pages()
    # print("post-publish_dvttestkit")
    
    
    
