import pytest

from portan.library.brownian import IArithmeticBrownian


class TestIArithmeticBrownian:
    @pytest.fixture(scope="class")
    def brownian(self) -> IArithmeticBrownian:
        return IArithmeticBrownian()

    def test_mean(self, brownian: IArithmeticBrownian):
        with pytest.raises(NotImplementedError):
            brownian.mean()

    def test_dispersion(self, brownian):
        with pytest.raises(NotImplementedError):
            brownian.dispersion()
