# Portan: Mean-Variance Analysis for Python

Portan helps you perform a mean-variance analysis on financial instruments.
It supports Python 3.9.

## Installation

Portan is not yet available on PyPI, and must be installed from source.

## Quick Start

### Instrument

The instrument class allows for the computation of the mean and volatility
of a single instrument.

```python
from portan import Instrument, Source

instrument = Instrument(
    "AAPL",
    ("2021-09-27", "2021-10-01"),
    source=Source.YAHOO,
)
instrument.fetch()
instrument.mean()
instrument.volatility()
```

An instrument is defined by a **unique identifier** (i.e., ticker), a
**range of dates** delimiting the prices to include in the computation
of the analytics and a **source** from which to fetch prices.

_Note: Both sides of the range of dates are inclusive, and the unique identifier
must be valid in combination with the source._

### Portfolio

The portfolio class allows for the computation of the mean, volatility
and correlation matrix of a weighted collection of instruments (i.e.,
financial portfolio).

```python
from portan import Portfolio, Source

portfolio = Portfolio(
    {"AAPL": 60, "SQ": 40},
    ("2021-09-27", "2021-10-01"),
    source=Source.YAHOO,
)
portfolio.fetch()
portfolio.mean()
portfolio.volatility()
portfolio.correlations()
```

A portfolio is defined by a **mapping** of unique identifier (i.e., ticker)
to weight, a **range of dates** delimiting the prices to include in the
computation of the analytics and a **source** from which to fetch prices.

_Note: Both sides of the range of dates are inclusive, the unique
identifiers must be valid in combination with the source, the
weights represent percentage values (i.e., 25 is equivalent to an
allocation of 25%), and the sum of the weights must be equal to one
hundred (i.e., 100)._

### MVO

The MVO class allows for the mean-variance optimisation of a weighted
collection of instruments (i.e., financial portfolio). The optimisation
finds the optimal allocation amongst the instruments that minimizes
volatility while achieving a specified minimum expected rate of return.

```python
from portan import MVO, Source

optimiser = MVO()
optimiser.optimise(
    ("AAPL", "SQ"),
    ("2021-07-30", "2021-08-31"),
    minimum=0.05,
    source=Source.YAHOO
)
```

The `optimise` method of the MVO class takes several arguments; an **iterable**
of unique identifiers (i.e., tickers), a **range of dates** delimiting the
prices to include in the optimisation, a **minimum** expected
rate of return, and a **source** from which to fetch prices.

_Note: Both sides of the range of dates are inclusive, the unique
identifiers must be valid in combination with the source,
the minimum is an annual continuous rate of return, and
the minimum expected rate of return must be selected carefully otherwise
the optimisation problem might be infeasible._

The MVO class returns a mapping of the instruments identifiers to
the optimal weights (i.e., an allocation).

> WARNING: The MVO class does not guarantee that the weights in the
> optimal allocation will sum to 100.

_Note: The weights are returned as integers, and those integers represent
percentage values (i.e., 25 is equivalent to an allocation of 25%)._

> DISCLAIMER: The MVO class uses historical prices to determine
> the expected returns of the financial instruments. Since past returns
> are not a guarantee of future returns, there's no guarantee that the
> minimum expected rate of return will be achieved in practice.
