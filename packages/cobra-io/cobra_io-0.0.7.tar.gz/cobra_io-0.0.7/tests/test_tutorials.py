import os
from pathlib import Path
import re
import sys

import nbconvert
import nbformat
import pytest

from cobra.user.user import login


sys.path.append(str(Path(__file__).parent.parent.joinpath('tutorials')))  # for local imports in tutorials

excluded_notebooks = {  # Notebooks that are not runnable automatically
    'Tolerated_Poses.ipynb'
}
notebooks_with_upload = {  # Notebooks that need login information
    '0_CoBRA_Introduction.ipynb',
    '1_CoBRA_Timor_Interaction.ipynb',
}


normal_notebooks = tuple(p for p in Path(__file__).parent.parent.glob('tutorials/*.ipynb')
                         if p.name not in excluded_notebooks | notebooks_with_upload)
notebooks_with_upload = tuple(p for p in Path(__file__).parent.parent.glob('tutorials/*.ipynb')
                              if p.name not in excluded_notebooks and p.name in notebooks_with_upload)
nb2script = nbconvert.ScriptExporter()


def _generate_script(nb):
    notebook = nbformat.read(nb.open("r"), as_version=4)
    script, _ = nb2script.from_notebook_node(notebook)
    script = re.sub(r'get_ipython\(\).*$\n', '', script, flags=re.MULTILINE)  # Remove ! commands
    script = re.sub(r'^.*condacolab.*$\n', '', script, flags=re.MULTILINE)  # Remove conda magic
    script = re.sub(r'^.*delete_solution.*$\n', '', script, flags=re.MULTILINE)  # Remove delete calls
    return script


def _exec_script(script):
    """Execute script in a clean context."""
    exec(script)


@pytest.mark.parametrize("nb", normal_notebooks)
def test_all_runable(nb: Path):
    # Make notebook into script
    script = _generate_script(nb)
    # Run script
    _exec_script(script)  # To keep local context clean


@pytest.mark.parametrize("nb", notebooks_with_upload)
def test_notebook_with_upload(
        nb: Path,
        test_user=os.environ.get("TEST_USER", 'cobra@cps.cit.tum.de'),
        test_password=os.environ.get("TEST_USER_PASSWORD", '!2345678')):
    """Test if notebook with upload works."""
    script = _generate_script(nb)
    script = script.replace('your-name', 'nb_test')
    script = script.replace('your-email', test_user)
    script = script.replace('your-affiliation', 'unit_test')
    login(test_user, test_password)  # Make sure user token already set
    _exec_script(script)
