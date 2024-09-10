"""
DeepArchiveParser class t5est
"""
import pytest
import sys
from archive_ops.DeepArchiveParser import DeepArchiveParser

# Write pytests for the DeepArchive
def test_deep_archive_incremental_true_when_not_given():
    """
    Test the DeepArchiveParser class
    """

    sys.argv = ["DipLogParserTest.py", '--input-file', 'dontcare']
    dap = DeepArchiveParser("usage", "desc")
    test_ns = dap.parsedArgs
    assert test_ns is not None
    assert test_ns.incremental is True
    assert test_ns.complete is False

# parameterize test_deep_archive_incremental_true_when_given
@pytest.mark.parametrize("form", ['-I', '--incremental'])
def test_deep_archive_incremental_true_when_given(form):
    """
    Test the DeepArchiveParser class
    """
    sys.argv = ["DipLogParserTest.py", '--input-file', 'dontcare', form]
    dap = DeepArchiveParser("usage", "desc")
    test_ns = dap.parsedArgs
    assert test_ns is not None
    assert test_ns.incremental is True
    assert test_ns.complete is False

@pytest.mark.parametrize("form", ['-C', '--complete'])
def test_deep_archive_complete_true_when_given(form):
    """
    Test the DeepArchiveParser class
    """
    sys.argv = ["DipLogParserTest.py", '--input-file', 'dontcare', form]
    dap = DeepArchiveParser("usage", "desc")
    test_ns = dap.parsedArgs
    assert test_ns is not None
    assert test_ns.incremental is False
    assert test_ns.complete is True



