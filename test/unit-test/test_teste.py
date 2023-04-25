import os
import sys
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# @mock.patch("src.blueprint.google.soma")
# def test_soma(mock_soma):
#     mock_soma.return_value = 5
#     assert mock_soma(2, 3) == 5
#     mock_soma.assert_called_once_with(2, 3)
