__version__ = "1.0.0"
__maintainer__ = "Fabia Miorelli"
__birthdate__ = "04.09.2023"
__status__ = "dev"  # options are: dev, test, prod
__license__ = "BSD-3-Clause"

import pytest

import pandas as pd

from ...vencopy.core.profileaggregators import Aggregator

# NOT TESTED: __basic_aggregation(), 