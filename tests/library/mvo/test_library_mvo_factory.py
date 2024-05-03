import pytest

from portan.library.mvo.factory import IMVOProgramFactory, MVOProgramFactory
from portan.library.optimisation.constraint import (
    LinearConstraints,
    LinearEqualities,
    LinearInequalities,
)
from portan.library.optimisation.objective import QuadraticCoefficients
from portan.library.optimisation.quadratic import QuadraticProgram
from portan.library.rate import Rate
from portan.library.rate.matrix import RateMatrix
from portan.library.rate.sequence import RateSequence


class TestIMVOProgramFactoryRaises:
    def test(self):
        factory = IMVOProgramFactory()
        with pytest.raises(NotImplementedError):
            factory.get(RateMatrix([]), Rate(0.0))


class TestMVOProgramFactoryGet:
    @pytest.fixture(scope="class")
    def minimum(self) -> Rate:
        return Rate(0.05)

    @pytest.fixture(scope="class")
    def factory(self) -> MVOProgramFactory:
        return MVOProgramFactory()

    def test_when_empty(
        self,
        factory: MVOProgramFactory,
        minimum: Rate,
    ):
        rates = RateMatrix([])
        result = factory.get(rates, minimum)
        expected = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[[]],
                    bounds=[1.0],
                ),
                LinearInequalities.from_float(
                    coefficients=[[]],
                    bounds=[
                        -float(minimum),
                    ],
                ),
            ),
        )
        assert result == expected

    def test_when_one_and_empty(
        self,
        factory: MVOProgramFactory,
        minimum: Rate,
    ):
        rates = RateMatrix(
            [
                RateSequence.from_float([]),
            ]
        )
        result = factory.get(rates, minimum)
        expected = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float([[0.0]]),
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[[1.0]],
                    bounds=[1.0],
                ),
                LinearInequalities.from_float(
                    coefficients=[[1.0], [-1.0], [-0.0]],
                    bounds=[1.0, -0.0, -float(minimum)],
                ),
            ),
        )
        assert result == expected

    def test_when_one_and_one(
        self,
        factory: MVOProgramFactory,
        minimum: Rate,
    ):
        rates = RateMatrix(
            [
                RateSequence.from_float([5.0]),
            ]
        )
        result = factory.get(rates, minimum)
        expected = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float([[0.0]]),
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[[1.0]],
                    bounds=[1.0],
                ),
                LinearInequalities.from_float(
                    coefficients=[[1.0], [-1.0], [-5.0]],
                    bounds=[1.0, -0.0, -float(minimum)],
                ),
            ),
        )
        assert result == expected

    def test_when_one_and_multiple(
        self,
        factory: MVOProgramFactory,
        minimum: Rate,
    ):
        values = RateSequence.from_float([5.0, 6.0])
        rates = RateMatrix([values])
        result = factory.get(rates, minimum)
        expected = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(rates.covariances()),
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[[1.0]],
                    bounds=[1.0],
                ),
                LinearInequalities.from_float(
                    coefficients=[[1.0], [-1.0], [-float(values.mean())]],
                    bounds=[1.0, -0.0, -float(minimum)],
                ),
            ),
        )
        assert result == expected

    def test_when_multiple_and_empty(
        self,
        factory: MVOProgramFactory,
        minimum: Rate,
    ):
        rates = RateMatrix(
            [
                RateSequence.from_float([]),
                RateSequence.from_float([]),
            ]
        )
        result = factory.get(rates, minimum)
        expected = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(
                [
                    [0.0, 0.0],
                    [0.0, 0.0],
                ]
            ),
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[[1.0, 1.0]],
                    bounds=[1.0],
                ),
                LinearInequalities.from_float(
                    coefficients=[
                        [1.0, 0.0],
                        [0.0, 1.0],
                        [-1.0, -0.0],
                        [-0.0, -1.0],
                        [-0.0, -0.0],
                    ],
                    bounds=[1.0, 1.0, -0.0, -0.0, -float(minimum)],
                ),
            ),
        )
        assert result == expected

    def test_when_multiple_and_one(
        self,
        factory: MVOProgramFactory,
        minimum: Rate,
    ):
        rates = RateMatrix(
            [
                RateSequence.from_float([2.0]),
                RateSequence.from_float([3.0]),
            ]
        )
        result = factory.get(rates, minimum)
        expected = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(
                [
                    [0.0, 0.0],
                    [0.0, 0.0],
                ]
            ),
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[[1.0, 1.0]],
                    bounds=[1.0],
                ),
                LinearInequalities.from_float(
                    coefficients=[
                        [1.0, 0.0],
                        [0.0, 1.0],
                        [-1.0, -0.0],
                        [-0.0, -1.0],
                        [-2.0, -3.0],
                    ],
                    bounds=[1.0, 1.0, -0.0, -0.0, -float(minimum)],
                ),
            ),
        )
        assert result == expected

    def test_when_multiple_and_multiple(
        self,
        factory: MVOProgramFactory,
        minimum: Rate,
    ):
        values = [
            RateSequence.from_float([2.0, 4.0]),
            RateSequence.from_float([3.0, 5.0]),
        ]
        rates = RateMatrix(values)
        result = factory.get(rates, minimum)
        expected = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(rates.covariances()),
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[[1.0, 1.0]],
                    bounds=[1.0],
                ),
                LinearInequalities.from_float(
                    coefficients=[
                        [1.0, 0.0],
                        [0.0, 1.0],
                        [-1.0, -0.0],
                        [-0.0, -1.0],
                        [-float(values[0].mean()), -float(values[1].mean())],
                    ],
                    bounds=[1.0, 1.0, -0.0, -0.0, -float(minimum)],
                ),
            ),
        )
        assert result == expected
