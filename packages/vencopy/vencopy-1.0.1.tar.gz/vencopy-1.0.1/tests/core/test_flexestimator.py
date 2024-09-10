__version__ = "1.0.0"
__maintainer__ = "Fabia Miorelli"
__birthdate__ = "04.09.2023"
__status__ = "dev"  # options are: dev, test, prod
__license__ = "BSD-3-Clause"


import pytest

import pandas as pd
from pathlib import Path
from dateutil import parser
from ...vencopy.core.flexestimators import FlexEstimator

@pytest.fixture
def sample_data_frame_other_filters():
    data = {
        "unique_id": [1, 1, 2, 2, 3],
        "timestamp_start": ["2023-09-01 08:00", "2023-09-01 08:45", "2023-09-01 10:00", "2023-09-01 10:30", "2023-09-01 11:00"],
        "timestamp_end": ["2023-09-01 09:00", "2023-09-01 09:30", "2023-09-01 10:15", "2023-09-01 11:15", "2023-09-01 11:30"],
        "trip_distance": [60.0, 15.0, 10.0, 10.0, 10.0],
        "travel_time": [60, 45, 90, 90, 90],
        "season": ["summer", "winter", "spring", "summer", "summer"]
    }
    data["timestamp_start"] = [parser.parse(x) for x in data["timestamp_start"]]
    data["timestamp_end"] = [parser.parse(x) for x in data["timestamp_end"]]
    return pd.DataFrame(data)

def _test_drain():

        df = sample_data_frame_other_filters()

        def _calculate_drain_by_season(x, y):
            if x == "spring" or x == "fall":
                x_new = y * 18 / 100
                return x_new
            elif x == "summer":
                x_new = (y * 18 / 100)*1.033
                return x_new
            elif x == "winter":
                x_new = (y * 18 / 100)*1.3
                return x_new
        # print(x_new)
    
        df["drain"] = df.apply(lambda row: _calculate_drain_by_season(row['season'],
                                                row['trip_distance']), axis=1)
        print(df)
        
