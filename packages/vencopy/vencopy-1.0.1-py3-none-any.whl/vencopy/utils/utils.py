__maintainer__ = "Niklas Wulff, Fabia Miorelli"
__license__ = "BSD-3-Clause"

import logging
import os
import yaml

from pathlib import Path

import pandas as pd

# Constants that define Seasons
winter_start = pd.to_datetime("12-21", format="%m-%d").dayofyear
spring_start = pd.to_datetime("03-20", format="%m-%d").dayofyear
summer_start = pd.to_datetime("06-21", format="%m-%d").dayofyear
fall_start = pd.to_datetime("09-23", format="%m-%d").dayofyear


def load_configs(base_path: Path) -> dict:
    """
    Generic function to load and open yaml config files.
    Uses pathlib syntax for windows, max, linux compatibility,
    see https://realpython.com/python-pathlib/ for an introduction.

    Args:
        base_path (Path): _description_

    Returns:
        configs (dict): Dictionary with opened yaml config files
    """
    config_names = ("user_config", "dev_config")
    config_path = Path(base_path) / "config"
    configs = {}
    for config_name in config_names:
        file_path = (config_path / config_name).with_suffix(".yaml")
        with open(file_path) as ipf:
            configs[config_name] = yaml.load(ipf, Loader=yaml.SafeLoader)
    return configs


def return_lowest_level_dict_keys(dictionary: dict, lst: list = None) -> list:
    """
    Returns the lowest level keys of dictionary and returns all of them
    as a list. The parameter lst is used as
    interface between recursion levels.

    Args:
        dictionary (dict): Dictionary of variables
        lst (list, optional): List used as interface between recursion levels. Defaults to None.

    Returns:
        list: list with all the bottom level dictionary keys
    """
    if lst is None:
        lst = []
    for i_key, i_value in dictionary.items():
        if isinstance(i_value, dict):
            lst = return_lowest_level_dict_keys(i_value, lst)
        elif i_value is not None:
            lst.append(i_key)
    return lst


def return_lowest_level_dict_values(dictionary: dict, lst: list = None) -> list:
    """
    Returns a list of all dictionary values of the last dictionary level
    (the bottom) of dictionary. The parameter
    lst is used as an interface between recursion levels.

    Args:
        dictionary (dict): Dictionary of variables
        lst (list, optional): List used as interface to next recursion. Defaults to None.

    Returns:
        list: List with all the bottom dictionary values
    """
    if lst is None:
        lst = []
    for _, i_value in dictionary.items():
        if isinstance(i_value, dict):
            lst = return_lowest_level_dict_values(i_value, lst)
        elif i_value is not None:
            lst.append(i_value)
    return lst


def replace_vec(
    series, year=None, month=None, day=None, hour=None, minute=None, second=None
) -> pd.Series:
    """
    _summary_

    Args:
        series (_type_): _description_
        year (_type_, optional): _description_. Defaults to None.
        month (_type_, optional): _description_. Defaults to None.
        day (_type_, optional): _description_. Defaults to None.
        hour (_type_, optional): _description_. Defaults to None.
        minute (_type_, optional): _description_. Defaults to None.
        second (_type_, optional): _description_. Defaults to None.

    Returns:
        pd.Series: _description_
    """
    replacement = pd.to_datetime(
        {
            "year": (
                series.dt.year if year is None else [year for i in range(len(series))]
            ),
            "month": (
                series.dt.month
                if month is None
                else [month for i in range(len(series))]
            ),
            "day": series.dt.day if day is None else [day for i in range(len(series))],
            "hour": (
                series.dt.hour if hour is None else [hour for i in range(len(series))]
            ),
            "minute": (
                series.dt.minute
                if minute is None
                else [minute for i in range(len(series))]
            ),
            "second": (
                series.dt.second
                if second is None
                else [second for i in range(len(series))]
            ),
        }
    )
    return replacement


def create_output_folders(configs: dict):
    """
    Function to crete vencopy output folder and subfolders

    Args:
        configs (dict): _description_
    """
    root = Path(configs["user_config"]["global"]["absolute_path"]["vencopy_root"])
    main_dir = "output"
    if not os.path.exists(Path(root / main_dir)):
        os.mkdir(Path(root / main_dir))
    sub_dirs = (
        "dataparser",
        "diarybuilder",
        "gridmodeller",
        "flexestimator",
        "profileaggregator",
        "postprocessor",
    )
    for sub_dir in sub_dirs:
        if not os.path.exists(Path(root / main_dir / sub_dir)):
            os.mkdir(Path(root / main_dir / sub_dir))


def create_file_name(dev_config: dict, user_config: dict, file_name_id: str, dataset: str, suffix: str = "csv") -> str:
    """
    Generic method used for fileString compilation throughout the venco.py framework. This method does not write any
    files but just creates the file name including the filetype suffix.

    Args:
        dev_config (dict): _description_
        user_config (dict): _description_
        file_name_id (str): ID of respective data file as specified in global config
        dataset (str): Dataset
        manual_label (str, optional):  Optional manual label to add to file_name. Defaults to "".
        suffix (str, optional): _description_. Defaults to "csv".

    Returns:
        str: Full name of file to be written.
    """
    additional_label = dev_config['global']['additional_label']
    run_label = user_config['global']['run_label']
    if len(run_label) == 0:
        return f"{dev_config['global']['disk_file_names'][file_name_id]}_{dataset}.{suffix}"
    if dataset is None:
        return f"{dev_config['global']['disk_file_names'][file_name_id]}_{additional_label}_{run_label}.{suffix}"
    if len(additional_label) == 0:
        return f"{dev_config['global']['disk_file_names'][file_name_id]}_{dataset}_{run_label}.{suffix}"
    return f"{dev_config['global']['disk_file_names'][file_name_id]}_{additional_label}_{dataset}_{run_label}.{suffix}"


def write_out(data: pd.DataFrame, path: Path):
    """
    Utility function to write the DataFrame given in data to the location given in path.

    Args:
        data (pd.DataFrame): Any DataFrame to write to disk
        path (Path): Location on the disk
    """
    data.to_csv(path, header=True)
    logging.info(f"Dataset written to {path}.")


def calculate_shortest_hourly_distance(start_hour, end_hour):
    """
    Function to calculate the shortest hourly distance between to hours
    within a 24 hour cycle

    Args:
        start_hour (float): First hour value
        end_hour (float): Second hour value

    Returns:
        float: Distance in hours
    """
    # Calculate the absolute difference between the hours
    hour_difference = abs(end_hour - start_hour)

    # Calculate the shortest distance considering a 24-hour cycle
    shortest_distance = min(hour_difference, 24 - hour_difference)

    return shortest_distance


def calculate_longest_hourly_distance(start_hour, end_hour):
    """
    Function to calculate the longest hourly distance between to hours
    within a 24 hour cycle

    Args:
        start_hour (float): First hour value
        end_hour (float): Second hour value

    Returns:
        float: Distance in hours
    """
    # Calculate the absolute difference between the hours
    hour_difference = abs(end_hour - start_hour)

    # Calculate the longest distance considering a 24-hour cycle
    longest_distance = max(hour_difference, 24 - hour_difference)

    return longest_distance


def adjust_factor_range_by_temperature_range(user_config, category, season):
    """
    This function calculates the changing factor of the seasonal factor
    based to the Hour_of_the_day.
    The season with the maximum temperature range within a day is used to
    be a reference between min and may consumption
    Seasons with lower temperature ranges are adapted to the maximum range
    (based on the logic that consumption factors change more within a day
    if the temperature range is very high)
    Args:
        season (string): The season of the activitiy

    Returns:
        season_min_factor: The factor for the season at the minimum
        consumption hour of a day
        season_max_factor: The factor for the season at the maximum
        consumption hour of a day
        season_neutral_factor: The factor for the season the hour
        between min and max
    """
    seasons_max_range = max(
        user_config[
            "global"][
            "consider_temperature_cycle_dependency"][
            "day_night_factors"][
            season][
            'temperature_range'] for season in ["winter",
                                                "spring",
                                                "summer",
                                                "fall"]
        )
    season_range = user_config[
        "global"][
        "consider_temperature_cycle_dependency"][
        "day_night_factors"][
        season][
        "temperature_range"]
    season_neutral_factor = category[season+"_factor"]
    season_min_factor = season_neutral_factor * (
        1 - season_range / seasons_max_range)
    season_max_factor = season_neutral_factor * (
        1 + season_range / seasons_max_range)

    return season_min_factor, season_max_factor, season_neutral_factor


def calculate_daily_seasonal_factor(user_config,
                                    season,
                                    category,
                                    hour_of_trip):
    """
    This function calulates the hours of neutral consumption as well as
    the range between the extremes and neutrals
    This is then used to calculate weigthing of the daily factors

    Args:
        season (string): The season of the activitiy
        hour_of_trip (double): Hour of the trip based on data timestamp

    Returns:
        factor: daily consumption factor that is added to seasonal
        consumption
        """

    season_min_factor, season_max_factor, season_neutral_factor = adjust_factor_range_by_temperature_range(user_config, category, season)

    max_hour = user_config["global"]["consider_temperature_cycle_dependency"][
        "day_night_factors"][season]["highest_temperature_hour"]
    min_hour = user_config["global"]["consider_temperature_cycle_dependency"][
        "day_night_factors"][season]["lowest_temperature_hour"]

    range_within = calculate_shortest_hourly_distance(max_hour, min_hour)
    range_outside = calculate_longest_hourly_distance(max_hour, min_hour)

    hour_range_min_hod = float(calculate_shortest_hourly_distance(
        hour_of_trip, min(max_hour, min_hour)))
    hour_range_max_hod = float(calculate_shortest_hourly_distance(
        hour_of_trip, max(max_hour, min_hour)))

    if hour_of_trip >= max(max_hour, min_hour):
        if hour_range_max_hod < hour_range_min_hod:
            if user_config["global"]["consider_temperature_cycle_dependency"][
                "day_night_factors"][season][
                    'consumption_at_highest_hour'] == 'max':
                max_factor = season_max_factor
                factor = max_factor - (
                    abs(max_factor - season_min_factor)
                    / range_outside
                    ) * hour_range_max_hod
            else:
                max_factor = season_min_factor
                factor = max_factor + (
                    abs(max_factor - season_max_factor)
                    / range_outside
                    ) * hour_range_max_hod
        else:
            if user_config["global"]["consider_temperature_cycle_dependency"][
                "day_night_factors"][season][
                    'consumption_at_highest_hour'] == 'max':
                min_factor = season_max_factor
                factor = min_factor - (
                    abs(min_factor - season_min_factor)
                    / range_outside
                    ) * hour_range_min_hod
            else:
                min_factor = season_min_factor
                factor = min_factor + (
                    abs(min_factor - season_min_factor)
                    / range_outside
                    ) * hour_range_min_hod

    elif hour_of_trip <= min_hour:

        if hour_range_max_hod < hour_range_min_hod:
            if user_config["global"]["consider_temperature_cycle_dependency"][
                "day_night_factors"][season][
                    'consumption_at_highest_hour'] == "max":
                max_factor = season_max_factor
                factor = max_factor - (
                    abs(max_factor - season_min_factor)
                    / range_outside
                    ) * hour_range_max_hod
            else:
                max_factor = season_min_factor
                factor = max_factor + (
                    abs(max_factor - season_max_factor)
                    / range_outside
                    ) * hour_range_max_hod
        else:
            if user_config["global"]["consider_temperature_cycle_dependency"][
                "day_night_factors"][season][
                    'consumption_at_highest_hour'] == "max":
                min_factor = season_max_factor
                factor = min_factor - (
                    abs(min_factor - season_min_factor)
                    / range_outside
                    ) * hour_range_min_hod
            else:
                min_factor = season_min_factor
                factor = min_factor + (
                    abs(min_factor - season_max_factor)
                    / range_outside
                    ) * hour_range_min_hod
    else:
        if hour_range_max_hod < hour_range_min_hod:
            if user_config["global"]["consider_temperature_cycle_dependency"][
                "day_night_factors"][season][
                    'consumption_at_highest_hour'] == "max":
                max_factor = season_max_factor
                factor = max_factor - (
                    abs(max_factor - season_min_factor)
                    / range_within
                    ) * hour_range_max_hod
            else:
                max_factor = season_min_factor
                factor = max_factor + (
                    abs(max_factor - season_max_factor)
                    / range_within
                    ) * hour_range_max_hod

        elif hour_range_max_hod > hour_range_min_hod:
            if user_config["global"]["consider_temperature_cycle_dependency"][
                "day_night_factors"][season][
                    'consumption_at_highest_hour'] == "max":
                min_factor = season_max_factor
                factor = min_factor - (
                    abs(min_factor - season_min_factor)
                    / range_within
                    ) * hour_range_max_hod
            else:
                min_factor = season_min_factor
                factor = min_factor + (
                    abs(min_factor - season_max_factor)
                    / range_within
                    ) * hour_range_max_hod
        else:
            factor = season_neutral_factor

    return factor
