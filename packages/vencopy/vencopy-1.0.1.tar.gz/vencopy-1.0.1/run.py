__maintainer__ = "Niklas Wulff, Fabia Miorelli"
__license__ = "BSD-3-Clause"


import time
import warnings
import logging

from pathlib import Path

from vencopy.core.dataparsers import parse_data
from vencopy.core.gridmodellers import GridModeller
from vencopy.core.flexestimators import FlexEstimator
from vencopy.core.diarybuilders import DiaryBuilder
from vencopy.core.profileaggregators import ProfileAggregator
from vencopy.core.postprocessors import PostProcessor
from vencopy.utils.utils import load_configs, create_output_folders

warnings.simplefilter(action='ignore', category=FutureWarning)
logging.basicConfig(level=logging.INFO, filename='vencopy.log', filemode='w', format="{%(filename)s: %(lineno)d} %(message)s")

if __name__ == "__main__":
    start_time = time.time()

    base_path = Path(__file__).parent / "vencopy"
    configs = load_configs(base_path=base_path)
    create_output_folders(configs=configs)

    data = parse_data(configs=configs)
    data.process()

    grid = GridModeller(configs=configs, data=data.data)
    grid.assign_grid()

    flex = FlexEstimator(configs=configs, data=grid.data)
    flex.estimate_technical_flexibility_through_iteration()

    diary = DiaryBuilder(configs=configs, data=flex.data)
    diary.create_diaries()

    profiles = ProfileAggregator(configs=configs, data=diary.data, profiles=diary)
    profiles.aggregate_profiles()

    post = PostProcessor(configs=configs, profiles=profiles, data=diary.data)
    post.normalise_profiles()
    post.create_annual_profiles()
    post.generate_fleet_profiles()

    elapsed_time = time.time() - start_time
    logging.info(f"Elapsed time: {elapsed_time}.")
