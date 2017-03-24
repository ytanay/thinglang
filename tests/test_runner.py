import pytest

from thinglang import utils
from thinglang.runner import run


@pytest.mark.skip
def test_external_file(source):
    utils.print_header('Expected output', source.expected_output)
    assert run(source.source).output == source.expected_output