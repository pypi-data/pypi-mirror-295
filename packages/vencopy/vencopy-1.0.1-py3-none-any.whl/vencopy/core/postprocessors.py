__maintainer__ = "Niklas Wulff, Fabia Miorelli"
__license__ = "BSD-3-Clause"

import logging

from pathlib import Path

import numpy as np
import pandas as pd

from ..core.profileaggregators import ProfileAggregator
from ..utils.metadata import read_metadata_config, write_out_metadata
from ..utils.utils import create_file_name, write_out


class PostProcessor:
    def __init__(self, configs: dict, profiles: ProfileAggregator, data: dict):
        """
        This class contains functions to post-process aggregated venco.py profiles for cloning weekly profiles
        to year and normalizing it with different normalization bases.

        In the PostProcessor, two steps happen. First, the aggregated weekly timeseries for the fleet are translated
        into annual timeseries by cloning e.g. a week by around 52 times to span a full year. The second purpose is to
        normalize the aggregated fleet profiles in order to provide profiles independent of the specific input and to be
        able to scale the venco.py output in a consecutive stept with feet scenarios or annual energy demands. For the
        flow profiles, two normalization bases are applied: The drain and uncontrolled charging profiles are normalized
        to the annual energy volume of the profiles to be scaled with an annual energy demand. The charging power
        profile is normalized by the number of vehicles to retrieve a rated charging power per representative vehicle.
        The two state profiles - minimum and maximum battery level profiles - are normalized using the battery capacity
        given in the flexestimaros part of the user_config.


        Args:
            configs (dict): Dictionary holding a user_config and a dev_config dictionary
            profiles (ProfileAggregator): An instance of class ProfileAggregator
        """
        self.user_config = configs["user_config"]
        self.dev_config = configs["dev_config"]
        self.dataset = self.user_config["global"]["dataset"]
        self.upscaling_base = self.user_config["postprocessor"]["upscaling_base"]
        self.time_resolution = self.user_config["diarybuilders"]["time_resolution"]
        self.time_delta = pd.timedelta_range(
            start="00:00:00", end="24:00:00", freq=f"{self.time_resolution}T"
        )
        self.time_index = list(self.time_delta)
        self.data = data
        self.vehicle_numbers = data['vehicles_number']
        self.activities = profiles.activities
        self.seasons = ["winter", "spring", "summer", "fall"]
        self.season = self.user_config["global"]["consider_temperature_cycle_dependency"]["season"] 
        self.profile_names = (
            "drain",
            "uncontrolled_charging",
            "charging_power",
            "max_battery_level",
            "min_battery_level",
        )

        self.drain = profiles.drain_weekly
        self.charging_power = profiles.charging_power_weekly
        self.uncontrolled_charging = profiles.uncontrolled_charging_weekly
        self.max_battery_level = profiles.max_battery_level_weekly
        self.min_battery_level = profiles.min_battery_level_weekly

        self.drain_normalised = pd.DataFrame()
        self.charging_power_normalised = pd.DataFrame()
        self.uncontrolled_charging_normalised = pd.DataFrame()
        self.max_battery_level_normalised = pd.DataFrame()
        self.min_battery_level_normalised = pd.DataFrame()

        self.drain_normalised_annual = pd.DataFrame()
        self.charging_power_normalised_annual = pd.DataFrame()
        self.uncontrolled_charging_normalised_annual = pd.DataFrame()
        self.max_battery_level_normalised_annual = pd.DataFrame()
        self.min_battery_level_normalised_annual = pd.DataFrame()

        self.drain_fleet = pd.DataFrame()
        self.uncontrolled_charging_fleet = pd.DataFrame()
        self.charging_power_fleet = pd.DataFrame()
        self.max_battery_level_fleet = pd.DataFrame()
        self.min_battery_level_fleet = pd.DataFrame()

        self.annual_profiles = {}
        self.normalised_profiles = {}
        self.fleet_profiles = {}

    def __week_to_annual_profile(self, profile: pd.Series) -> pd.Series:
        """
        This function clones a profile with a given temporal resolution from a weekly profile to the full year.
        Overreaching time intervals are being truncated at the year border (December, 31st). Currently, gap years are
        not considered.

        Args:
            profile (pd.Series): Any profile spanning one week in variable resolution

        Returns:
            pd.Series: Annual profile in the same temporal resolution as the input profile
        """
        start_weekday = self.user_config["postprocessor"]["start_weekday"]  # (1: Monday, 7: Sunday)
        n_timeslots_per_day = len(list(self.time_index))
        if self.user_config["global"][
            "consider_temperature_cycle_dependency"]["annual"] and self.user_config["global"]["consider_temperature_cycle_dependency"]["season"] != 'None':
            annual = profile.iloc[((start_weekday - 1) * (n_timeslots_per_day - 1)):]
            seasonal = pd.DataFrame()
            for season in self.seasons:
                annual_season = annual[season]
                annual_season = pd.concat([annual_season] * 13, ignore_index = True)
                seasonal = pd.concat([seasonal, annual_season], ignore_index=True)
            # add a few bins of winter to match a whole year
            missing_bins = (n_timeslots_per_day - 1) * 365 - len(seasonal)
            annual_season = annual['winter'].head(missing_bins)
            seasonal = pd.concat([seasonal, annual_season], ignore_index = True)
            annual = pd.DataFrame(seasonal)

        else:
            # Shift input profiles to the right weekday and start with first bin of chosen weekday
            annual = profile.iloc[((start_weekday - 1) * (n_timeslots_per_day - 1)) :]
            annual = pd.DataFrame(annual.iloc[:, 0].to_list() * 53)
            annual.drop(annual.tail(len(annual) - (n_timeslots_per_day - 1) * 365).index)
        return annual

    @staticmethod
    def __normalise_flows(profile: pd.Series) -> pd.Series:
        """
        Function to normalise a timeseries according to its annual sum. Used in venco.py for normalisation of
        uncontrolled charging and drain profiles.

        Args:
            profile (pd.Series): Weekly profile to be normalised

        Returns:
            pd.Series: Normalized timeseries
        """
        return profile / (profile.sum() / 7 * 365)

    @staticmethod
    def __normalise_states(profile: pd.Series, base: int) -> pd.Series:
        """
        Function to normalise a state profile according to a baseline value. Used in venco.py for normalisation of the
        minimum and maximum battery level profiles based on the vehicle battery capacity assumed in the flexestimator
        config.

        Args:
            profile (pd.Series): State profile to be normalised
            base (int): normalisation basis, e.g. battery capacity in kWh

        Returns:
            pd.Series: Normalized battery level between 0 and 1
        """
        return profile / base

    @staticmethod
    def __normalise_based_on_vehicle_numbers(
        profile: pd.Series, base: int, time_delta
    ) -> pd.Series:
        """
        Function to normalise a timeseries according to a baseline value for each weekday. Used in venco.py for
        normalisation of profiles based on the number of vehicles for each weekday.

        Args:
            profile (pd.Series): Profile to be normalised
            base (int): normalisation basis, e.g. number of vehicles
            time_delta (pd.timedelta_range): Temporal resolution of the run

        Returns:
            pd.Series: Charging power profile of the fleet normalized to the number of vehicles of the fleet
        """
        profile_normalised = []
        for day in range(1, 8):
            start = day * len(time_delta)
            end = start + len(time_delta)
            profile_day = profile[start:end] / (base[day])
            if profile_normalised == []:
                profile_normalised = profile_day.to_list()
            else:
                profile_normalised.extend(profile_day.to_list())
        profile = pd.Series(profile_normalised)
        return profile

    def __write_output(self, profile_name: str, profile: pd.Series, filename_id: str):
        """
        Write out the profile given in profile adding the profile_name and a filename_id (overarching file label) to the
        written file.

        Args:
            profile_name (str): A string describing the name of a profile to write
            profile (pd.Series): A profile to write to disk
            filename_id (str): An additional overarching label provided to the file written to disk
        """
        root = Path(self.user_config["global"]["absolute_path"]["vencopy_root"])
        folder = self.dev_config["global"]["relative_path"]["processor_output"]
        self.dev_config["global"]["additional_label"] = profile_name
        file_name = create_file_name(
            dev_config=self.dev_config,
            user_config=self.user_config,
            file_name_id=filename_id,
            dataset=self.dataset,
        )
        write_out(data=profile, path=root / folder / file_name)

    def create_fleet_data_structure(self):
        nuts_resolution = self.user_config["postprocessor"]["spatial"]["nuts_level"]
        spatial_resolution = self.user_config["postprocessor"]["spatial"]["country"]
        temporal_resolution = self.user_config["postprocessor"]["temporal"]
        time_resolution = self.user_config["diarybuilders"]["time_resolution"]
        eurostat_pop_file = (
            Path(self.user_config["global"]["absolute_path"]["vencopy_root"])
            / Path(self.dev_config["global"]["relative_path"]["eurostat_population"])
            / self.dev_config["global"]["files"]["eurostat_population"]
        )
        eurostat_nuts3_population = self._read_in_eurostat_data_nodes(
            eurostat_pop_file=eurostat_pop_file
        )
        data_nodes = self._keep_population_model_scope(
            eurostat_nuts3_population=eurostat_nuts3_population,
            spatial_resolution=spatial_resolution,
            temporal_resolution=temporal_resolution,
        )
        population_shares = self._calculate_population_share(
            data_nodes=data_nodes,
            nuts_resolution=nuts_resolution,
            temporal_resolution=temporal_resolution,
        )
        fleet_data = self._adjust_fleet_data_structure(
            time_resolution=time_resolution, population_shares=population_shares
        )
        return fleet_data

    @staticmethod
    def _scale_up_fleet_size(
        fleet_size: dict,
        fleet_data_structure: pd.DataFrame,
        normalised_profile: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        _summary_

        Args:
            fleet_size (dict): _description_
            fleet_data_structure (pd.DataFrame): _description_
            normalised_profile (pd.DataFrame): _description_

        Returns:
            pd.DataFrame: _description_
        """
        normalised_profile.index.name = "timestep"
        fleet_data = fleet_data_structure.groupby(level=[0], group_keys=False).apply(
            lambda x: x.mul(normalised_profile[0], axis=0)
        )
        fleet_size = pd.DataFrame.from_dict(fleet_size)
        for year in fleet_size.columns:
            fleet_data = fleet_data.groupby(level=[0], group_keys=False).apply(
                lambda x: x * fleet_size[year].values[0]
            )
        return fleet_data

    @staticmethod
    def _scale_up_annual_demand(
        annual_demand: dict,
        fleet_data_structure: pd.DataFrame,
        normalised_profile: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        _summary_

        Args:
            fleet_size (dict): _description_
            fleet_data_structure (pd.DataFrame): _description_
            normalised_profile (pd.DataFrame): _description_

        Returns:
            pd.DataFrame: _description_
        """
        normalised_profile.index.name = "timestep"
        fleet_data = fleet_data_structure.groupby(level=[0], group_keys=False).apply(
            lambda x: x.mul(normalised_profile[0], axis=0)
        )
        annual_demand = pd.DataFrame.from_dict(annual_demand)
        for year in annual_demand.columns:
            fleet_data = fleet_data.groupby(level=[0], group_keys=False).apply(
                lambda x: x * annual_demand[year].values[0]
            )
        return fleet_data

    @staticmethod
    def _read_in_eurostat_data_nodes(eurostat_pop_file: Path) -> pd.DataFrame:
        """
        Read-in eurostat population file. Updated file can be downloaded at:
        https://ec.europa.eu/eurostat/web/population-demography/population-projections/database

        Args:
            eurostat_pop_file (Path): path to the venco.py input folder containing the eurostat population

        Returns:
            pd.DataFrame: _description_
        """
        eurostat_nuts3_population = pd.read_csv(eurostat_pop_file, sep="\t")
        eurostat_nuts3_population = eurostat_nuts3_population.rename(
            columns=lambda x: x.strip()
        )
        headers = eurostat_nuts3_population[
            "projection,age,sex,unit,geo\\time"
        ].str.split(",", expand=True)
        headers = headers.rename(
            columns={0: "projection", 1: "age", 2: "sex", 3: "unit", 4: "nuts_3"}
        )
        eurostat_nuts3_population = pd.concat(
            [headers, eurostat_nuts3_population], axis=1
        )
        eurostat_nuts3_population.drop(
            "projection,age,sex,unit,geo\\time", axis=1, inplace=True
        )
        eurostat_nuts3_population = eurostat_nuts3_population.loc[
            (eurostat_nuts3_population["age"] == "TOTAL")
            & (eurostat_nuts3_population["sex"] == "T")
            & (eurostat_nuts3_population["projection"] == "NIRMIGR")
        ]
        eurostat_nuts3_population.drop(
            ["projection", "age", "sex", "unit"], axis=1, inplace=True
        )
        return eurostat_nuts3_population.reset_index(drop=True)

    @staticmethod
    def _keep_population_model_scope(
        eurostat_nuts3_population: pd.DataFrame,
        spatial_resolution: str,
        temporal_resolution: list,
    ) -> pd.DataFrame:
        """
        Subsets the eurostat dataframe containing the population for the required spatial and temporal resolution.

        Args:
            eurostat_nuts3_population (pd.DataFrame): _description_
            spatial_resolution (str): _description_
            temporal_resolution (list): _description_

        Returns:
            pd.DataFrame: _description_
        """
        data_nodes = eurostat_nuts3_population[["nuts_3"] + temporal_resolution]
        data_nodes = data_nodes[data_nodes["nuts_3"].str.contains(spatial_resolution)]
        return data_nodes.reset_index(drop=True)

    @staticmethod
    def _calculate_population_share(
        data_nodes: pd.DataFrame, nuts_resolution: str, temporal_resolution: list
    ) -> pd.DataFrame:
        """
        Calculate the population share based on the given NUTS and temporal resolution.

        Args:
            data_nodes (pd.DataFrame): dataframe containing columns with absolute population number for the specified country and NUTS level
            nuts_resolution (str): NUTS level of interest
            temporal_resolution (list): list of modelling years to be considered

        Returns:
            pd.DataFrame: dataframe with share of population for the specified modelling years and NUTS level
        """
        total_population = data_nodes[
            temporal_resolution
        ].sum()  # note: option of multiple countries not possible -> another model run
        if nuts_resolution == "nuts_0":
            data_nodes["nuts_0"] = data_nodes["nuts_3"].str.slice(0, 2)
            data_nodes.drop("nuts_3", axis=1, inplace=True)
            data_nodes = data_nodes.groupby(by="nuts_0").sum()
            population_shares = data_nodes / total_population * 100
        elif nuts_resolution == "nuts_1":
            data_nodes["nuts_1"] = data_nodes["nuts_3"].str.slice(0, 3)
            data_nodes.drop("nuts_3", axis=1, inplace=True)
            data_nodes = data_nodes.groupby(by="nuts_1").sum()
            population_shares = data_nodes / total_population * 100
        elif nuts_resolution == "nuts_2":
            data_nodes["nuts_2"] = data_nodes["nuts_3"].str.slice(0, 4)
            data_nodes.drop("nuts_3", axis=1, inplace=True)
            data_nodes = data_nodes.groupby(by="nuts_2").sum()
            population_shares = data_nodes / total_population * 100
        elif nuts_resolution == "nuts_3":
            data_nodes = data_nodes.groupby(by="nuts_3").sum()
            population_shares = data_nodes / total_population * 100
        return population_shares

    @staticmethod
    def _adjust_fleet_data_structure(time_resolution, population_shares):
        """
        Creates dataframe structure in which the profiles are stored for the predefined NUTS resolution and for the specified modelling years.

        Args:
            time_resolution (int): venco.py time resolution for timeseries
            population_shares (pd.DataFrame): Eurostat population share for the predefined temporal and geographical resolution
        """
        fleet = population_shares.transpose()
        fleet.index.name = "year"
        fleet.index = fleet.index.astype(int)
        fleet = fleet.reset_index()
        fleet = pd.DataFrame(
            np.repeat(fleet.values, int(24 * 365 * 60 / time_resolution), axis=0),
            columns=fleet.columns,
        )
        df_years_list = []
        for year in fleet["year"].unique():
            df_year = fleet[fleet["year"] == int(year)].copy()
            df_year.reset_index(inplace=True)
            df_year.drop(["index"], axis=1, inplace=True)
            df_year.index.name = "timestep"
            multi_idx = pd.MultiIndex.from_arrays([df_year["year"], df_year.index])
            df_year.index = multi_idx
            df_year.drop(["year"], axis=1, inplace=True)
            df_years_list.append(df_year)
        fleet = pd.concat(df_years_list)
        return fleet

    def generate_metadata(self, metadata_config: dict, file_name: str) -> dict:
        """
        _summary_

        Args:
            metadata_config (dict): _description_
            file_name (str): _description_

        Returns:
            dict: _description_
        """
        metadata_config["name"] = file_name
        if "normalised" in file_name:
            metadata_config["title"] = (
                "Annual normalised timeseries with venco.py output profiles"
            )
            metadata_config["description"] = "Annual normalised timeseries."
        elif "annual" in file_name:
            metadata_config["title"] = (
                "Annual timeseries with venco.py output profiles at fleet level"
            )
            metadata_config["description"] = "Annual timeseries at fleet level."
        metadata_config["sources"] = [
            f for f in metadata_config["sources"] if f["title"] in self.dataset
        ]
        reference_resource = metadata_config["resources"][0]
        this_resource = reference_resource.copy()
        this_resource["name"] = file_name.rstrip(".metadata.yaml")
        this_resource["path"] = file_name
        if "normalised" in file_name:
            these_fields = [
                f
                for f in reference_resource["schema"][self.dataset]["fields"][
                    "postprocessors"
                ]["normalised"]
            ]
        elif "annual" in file_name:
            these_fields = [
                f
                for f in reference_resource["schema"][self.dataset]["fields"][
                    "postprocessors"
                ]["annual"]
            ]
        this_resource["schema"] = {"fields": these_fields}
        metadata_config["resources"].pop()
        metadata_config["resources"].append(this_resource)
        return metadata_config

    def _write_metadata(self, file_name: str):
        """
        _summary_

        Args:
            file_name (str): _description_
        """
        metadata_config = read_metadata_config()
        class_metadata = self.generate_metadata(
            metadata_config=metadata_config, file_name=file_name.name
        )
        write_out_metadata(metadata_yaml=class_metadata, file_name=file_name)

    def create_annual_profiles(self):
        """
        Wrapper function to clone the five main venco.py profiles from weekly profiles to annual
        profiles and write them to disk. This function is meant to be called in the run.py.
        """
        if self.user_config["profileaggregators"]["aggregation_timespan"] == "daily":
            logging.info(
                "The annual profiles cannot be generated as the aggregation was performed over a single day."
            )
        elif (self.user_config["global"]["consider_temperature_cycle_dependency"]["season"] in self.seasons) & self.user_config["global"]["consider_temperature_cycle_dependency"]["annual"]:
            logging.info(
                "The annual profiles cannot be generated as only a specific season was selected."
            )
        else:

            self.drain_normalised_annual["drain"] = self.__week_to_annual_profile(profile=self.drain_normalised)
            self.uncontrolled_charging_normalised_annual["uncontrolled_charging"] = self.__week_to_annual_profile(profile=self.uncontrolled_charging_normalised)
            self.charging_power_normalised_annual["charging_power"] = self.__week_to_annual_profile(profile=self.charging_power_normalised)
            self.max_battery_level_normalised_annual["max_battery_level"] = self.__week_to_annual_profile(profile=self.max_battery_level_normalised)
            self.min_battery_level_normalised_annual["min_battery_level"] = self.__week_to_annual_profile(profile=self.min_battery_level_normalised)
        self.annual_profiles = (
            self.drain_normalised_annual,
            self.uncontrolled_charging_normalised_annual,
            self.charging_power_normalised_annual,
            self.max_battery_level_normalised_annual,
            self.min_battery_level_normalised_annual,
        )
        profile_names = self.profile_names
        if self.user_config["global"]["write_output_to_disk"]["processor_output"][
            "normalised_annual_profiles"
        ]:
            for profile_name, profile in zip(profile_names, self.annual_profiles):
                self.__write_output(
                    profile_name=profile_name,
                    profile=profile,
                    filename_id="output_postprocessor_annual",
                )
        root = Path(self.user_config["global"]["absolute_path"]["vencopy_root"])
        folder = self.dev_config["global"]["relative_path"]["processor_output"]
        file_name = (
            "vencopy_output_postprocessor_annual_normalised_"
            + self.dataset
            + ".metadata.yaml"
        )
        self._write_metadata(file_name=root / folder / file_name)

    def normalise_profiles(self):
        """
        Wrapper function to normalise the five venco.py profiles to default normalisation bases. These are
        the year-sum of the profiles for drain and uncontrolled charging, the vehicle fleet for charging power and the
        battery capacity for min and max battery level profiles.
        This profile is supposed to be called in the venco.py workflow after PostProcessor instantiation.
        """
        if self.user_config["profileaggregators"]["aggregation_timespan"] == "daily":
            raise ValueError(
                "The annual profiles cannot be normalised as the aggregation was performed over a single day."
            )
        else:
            if self.user_config["global"]["consider_temperature_cycle_dependency"]["annual"] & (self.season != 'None'):
                for season in self.seasons:
                    self.drain_normalised[season] = self.__normalise_based_on_vehicle_numbers(profile=self.drain[season], base=self.vehicle_numbers[season]["total_amount_vehicle"], time_delta=self.time_delta)
                    self.uncontrolled_charging_normalised[season] = self.__normalise_based_on_vehicle_numbers(profile=self.uncontrolled_charging[season], base=self.vehicle_numbers[season]["total_amount_vehicle"], time_delta=self.time_delta)
                    self.charging_power_normalised[season] = self.__normalise_based_on_vehicle_numbers(profile=self.charging_power[season], base=self.vehicle_numbers[season]["total_amount_vehicle"], time_delta=self.time_delta)
                    self.max_battery_level_normalised[season] = self.__normalise_states(profile=self.max_battery_level[season], base=1)
                    self.min_battery_level_normalised[season] = self.__normalise_states(profile=self.min_battery_level[season], base=1)
            elif self.upscaling_base == "fleet_size":
                self.drain_normalised["drain"] = self.__normalise_based_on_vehicle_numbers(profile=self.drain["drain"], base=self.vehicle_numbers["total_amount_vehicle"], time_delta=self.time_delta)
                self.uncontrolled_charging_normalised["uncontrolled_charging"] = self.__normalise_based_on_vehicle_numbers(profile=self.uncontrolled_charging["uncontrolled_charging"], base=self.vehicle_numbers["total_amount_vehicle"], time_delta=self.time_delta)
                self.charging_power_normalised["charging_power"] = self.__normalise_based_on_vehicle_numbers(profile=self.charging_power["charging_power"], base=self.vehicle_numbers["total_amount_vehicle"], time_delta=self.time_delta)
                self.max_battery_level_normalised["max_battery_level"] = self.__normalise_states(profile=self.max_battery_level["max_battery_level"], base=1)
                self.min_battery_level_normalised["min_battery_level"] = self.__normalise_states(profile=self.min_battery_level["min_battery_level"], base=1)
            elif self.upscaling_base == "annual_demand":
                self.drain_normalised["drain"] = self.__normalise_flows(profile=self.drain["drain"])
                self.uncontrolled_charging_normalised["uncontrolled_charging"] = self.__normalise_flows(profile=self.uncontrolled_charging["uncontrolled_charging"])
                self.charging_power_normalised["charging_power"] = self.__normalise_based_on_vehicle_numbers(profile=self.charging_power["charging_power"], base=self.vehicle_numbers["total_amount_vehicle"], time_delta=self.time_delta)
                self.max_battery_level_normalised["max_battery_level"] = self.__normalise_states(profile=self.max_battery_level["max_battery_level"], base=1)
                self.min_battery_level_normalised["min_battery_level"] = self.__normalise_states(profile=self.min_battery_level["min_battery_level"], base=1)
            else:
                NotImplementedError(
                    "The normalisation can either be based on the number of vehicles in the fleet or on the annual demand."
                )
            self.normalised_profiles = (
                self.drain_normalised,
                self.uncontrolled_charging_normalised,
                self.charging_power_normalised,
                self.max_battery_level_normalised,
                self.min_battery_level_normalised,
            )
            profile_names = self.profile_names
            if self.user_config["global"]["write_output_to_disk"]["processor_output"][
                "normalised_weekly_profiles"
            ]:
                for profile_name, profile in zip(
                    profile_names, self.normalised_profiles
                ):
                    self.__write_output(
                        profile_name=profile_name,
                        profile=profile,
                        filename_id="output_postprocessor_normalised",
                    )
            root = Path(self.user_config["global"]["absolute_path"]["vencopy_root"])
            folder = self.dev_config["global"]["relative_path"]["processor_output"]
            file_name = (
                "vencopy_output_postprocessor_weekly_normalised_"
                + self.dataset
                + ".metadata.yaml"
            )
            self._write_metadata(file_name=root / folder / file_name)

    def generate_fleet_profiles(self):
        """
        Wrapper function to scale up the five main venco.py profiles from weekly profiles to fleet
        level and write them to disk. This function is meant to be called in the run.py.
        """
        if self.user_config["profileaggregators"]["aggregation_timespan"] == "daily" or self.user_config["global"]["consider_temperature_cycle_dependency"]["season"] != "all":
            logging.info(
                "The fleet profiles cannot be generated as the aggregation was performed over a single day or only one season was selected."
            )
        else:
            fleet_data_structure = self.create_fleet_data_structure()
            if self.upscaling_base == "fleet_size":
                fleet_size = self.user_config["postprocessor"]["fleet_size_nuts_0"]
                self.drain_fleet = self._scale_up_fleet_size(normalised_profile=self.drain_normalised_annual["drain"], fleet_size=fleet_size, fleet_data_structure=fleet_data_structure)
                self.uncontrolled_charging_fleet = self._scale_up_fleet_size(normalised_profile=self.uncontrolled_charging_normalised_annual["uncontrolled_charging"], fleet_size=fleet_size, fleet_data_structure=fleet_data_structure)
                self.charging_power_fleet = self._scale_up_fleet_size(normalised_profile=self.charging_power_normalised_annual["charging_power"], fleet_size=fleet_size, fleet_data_structure=fleet_data_structure)
                self.max_battery_level_fleet = self._scale_up_fleet_size(normalised_profile=self.max_battery_level_normalised_annual["max_battery_level"], fleet_size=fleet_size, fleet_data_structure=fleet_data_structure)
                self.min_battery_level_fleet = self._scale_up_fleet_size(normalised_profile=self.min_battery_level_normalised_annual["min_battery_level"], fleet_size=fleet_size, fleet_data_structure=fleet_data_structure)
            elif self.upscaling_base == "annual_demand":
                annual_demand = self.user_config["postprocessor"]["annual_demand_nuts_0"][0] # in TWh
                vehicle_specific_consumption = self.user_config["flexestimators"]["electric_consumption"]["general"] / 100 / 1e9  # consumption from kWh/100 km to kWh/km to TWh/km
                vehicle_yearly_mileage = self.user_config["postprocessor"]["yearly_mileage"]  # km/year/vehicle
                fleet_size = annual_demand / vehicle_specific_consumption / vehicle_yearly_mileage
                self.drain_fleet = self._scale_up_annual_demand(normalised_profile=self.drain_normalised_annual["drain"], annual_demand=annual_demand, fleet_data_structure=fleet_data_structure)
                self.uncontrolled_charging_fleet = self._scale_up_annual_demand(normalised_profile=self.uncontrolled_charging_normalised_annual["uncontrolled_charging"], annual_demand=annual_demand, fleet_data_structure=fleet_data_structure)
                self.charging_power_fleet = self._scale_up_fleet_size(normalised_profile=self.charging_power_normalised["charging_power"], fleet_size=fleet_size, fleet_data_structure=fleet_data_structure)
                self.max_battery_level_fleet = self._scale_up_fleet_size(normalised_profile=self.max_battery_level_normalised_annual["max_battery_level"], fleet_size=fleet_size, fleet_data_structure=fleet_data_structure)
                self.min_battery_level_fleet = self._scale_up_fleet_size(normalised_profile=self.min_battery_level_normalised_annual["min_battery_level"], fleet_size=fleet_size, fleet_data_structure=fleet_data_structure)
            self.fleet_profiles = (
                self.drain_fleet,
                self.uncontrolled_charging_fleet,
                self.charging_power_fleet,
                self.max_battery_level_fleet,
                self.min_battery_level_fleet,
            )
            profile_names = self.profile_names
            if self.user_config["global"]["write_output_to_disk"]["processor_output"][
                "fleet_annual_profiles"
            ]:
                for profile_name, profile in zip(profile_names, self.fleet_profiles):
                    self.__write_output(
                        profile_name=profile_name,
                        profile=profile,
                        filename_id="output_postprocessor_fleet",
                    )
            root = Path(self.user_config["global"]["absolute_path"]["vencopy_root"])
            folder = self.dev_config["global"]["relative_path"]["processor_output"]
            file_name = (
                "vencopy_output_postprocessor_annual_fleet_"
                + self.dataset
                + ".metadata.yaml"
            )
            self._write_metadata(file_name=root / folder / file_name)
