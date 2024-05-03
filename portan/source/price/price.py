from portan.utilities.finite.positive import PositiveFinite


class Price(PositiveFinite):
    """Price of a financial instrument (e.g., 101.402).

    The price of a financial instrument is represented internally with a
    finite and strictly positive floating-point number with
    undefined precision.
    """

    pass
