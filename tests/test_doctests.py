"""Guard that the package's docstring examples actually get checked.

``doodad``'s behavioural coverage lives almost entirely in docstring examples.
Those are only collected by ``pytest --doctest-modules``, and only for paths
pytest is pointed at -- so a narrow ``testpaths`` silently disables all of
them, locally and in CI alike, while the suite stays green.

There is a second, subtler trap: the CI runner forces
``-o doctest_optionflags='ELLIPSIS IGNORE_EXCEPTION_DETAIL'``, which *replaces*
the ``pyproject.toml`` setting and therefore drops ``NORMALIZE_WHITESPACE``.
A whitespace-sensitive example can pass a plain local run and still fail CI.

Running the examples from here -- ``tests/``, the one directory this repo has
always collected -- with exactly the CI flag set closes both gaps at once.
"""

import doctest
import importlib
import pkgutil

import pytest

import doodad

#: The flag set the CI runner forces, replacing the ``pyproject.toml`` value.
#: Notably *without* ``NORMALIZE_WHITESPACE``, so whitespace-sensitive examples
#: fail here the same way they would fail CI.
CI_DOCTEST_OPTIONFLAGS = doctest.ELLIPSIS | doctest.IGNORE_EXCEPTION_DETAIL


def _doodad_module_names():
    """Yield the importable module names of the ``doodad`` package."""
    yield doodad.__name__
    prefix = f"{doodad.__name__}."
    for module_info in pkgutil.walk_packages(doodad.__path__, prefix):
        yield module_info.name


@pytest.mark.parametrize("module_name", sorted(_doodad_module_names()))
def test_module_doctests(module_name):
    """Every docstring example in ``module_name`` runs and matches its output."""
    module = importlib.import_module(module_name)
    results = doctest.testmod(module, optionflags=CI_DOCTEST_OPTIONFLAGS, verbose=False)
    assert results.failed == 0, (
        f"{results.failed} of {results.attempted} doctest examples failed in "
        f"{module_name} (see the doctest report in the captured output above)"
    )
