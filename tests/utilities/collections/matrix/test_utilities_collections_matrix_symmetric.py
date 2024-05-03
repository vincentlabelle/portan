from typing import Tuple

import pytest

from portan.utilities.collections import Sequence, SymmetricMatrix


class TestSymmetricMatrixInvariants:
    @pytest.mark.parametrize(
        "values",
        [
            (),
            (Sequence([0.01]),),
            (
                Sequence([0.01, 0.02]),
                Sequence([0.02, 0.04]),
            ),
        ],
    )
    def test_when_symmetrical(self, values: Tuple[Sequence, ...]):
        SymmetricMatrix(values)  # does not raise

    @pytest.mark.parametrize(
        "values",
        [
            (
                Sequence([0.01, 0.02]),
                Sequence([0.03, 0.04]),
            ),
            (
                Sequence([0.01, 0.02, 0.03]),
                Sequence([0.03, 0.04, 0.05]),
                Sequence([0.03, 0.06, 0.08]),
            ),
        ],
    )
    def test_when_asymmetrical(self, values: Tuple[Sequence, ...]):
        with pytest.raises(ValueError, match="symmetric"):
            SymmetricMatrix(values)
