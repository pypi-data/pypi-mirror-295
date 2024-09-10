from os import listdir, getcwd
from os.path import join
from pandas import DataFrame, read_csv
from pathlib import Path

from leximpact_dotations_back import logger
from leximpact_dotations_back.mapping.criteres_dgcl_2024 import CODE_INSEE, CODE_INSEE_DTYPE, DECIMAL_SEPARATOR
from leximpact_dotations_back.data_building.adapt_dotations_criteres import adapt_criteres


CRITERES_FILENAME_PREFIX = "criteres_repartition_"
CRITERES_FILENAME_EXTENSION = ".csv"
DATA_DIRECTORY = join(getcwd(), "data")


def get_criteres_file_path(data_dirpath: str, year: int) -> str:
    '''
    Build DGCL critères file path from reference data_dirpath directory, dotations year and filename constraints (prefix and suffix).
    '''
    path = join(data_dirpath, CRITERES_FILENAME_PREFIX + str(year) + CRITERES_FILENAME_EXTENSION)
    logger.debug(f"Building {year} criteres path '{path}'...")
    return path


def load_dgcl_csv(csv_path: str) -> DataFrame:
    try:
        logger.info(f"Loading {Path(csv_path).resolve()}...")
        dgcl_data = read_csv(csv_path, decimal=DECIMAL_SEPARATOR, dtype={CODE_INSEE: CODE_INSEE_DTYPE})

    except FileNotFoundError:
        logger.fatal(f"Following file was not found: {csv_path}")
        logger.debug("Directory content:", listdir("."))
        logger.debug("Working directory:", getcwd())
        raise
    return dgcl_data


def load_criteres(data_dirpath: str, year: int) -> DataFrame:
    '''
    Get a DataFrame of DGCL critères data from a file in reference data_dirpath directory and for a specific year of dotations.
    '''
    criteres_file_path = get_criteres_file_path(data_dirpath, year)
    criteres = load_dgcl_csv(criteres_file_path)
    logger.debug(criteres)
    return criteres


# TODO def insert_dsu_garanties(adapted_criteres, year):
#     return adapted_criteres_to_dsu
#
# https://fr.wikipedia.org/wiki/Liste_des_communes_nouvelles_créées_en_2024
# TODO def insert_dsr_garanties_communes_nouvelles(adapted_criteres_to_dsu, year):
#     return adapted_criteres_to_dsu_and_dsr


def build_data(year):
    data_criteres = load_criteres(DATA_DIRECTORY, year)
    adapted_criteres = adapt_criteres(data_criteres, year)

    # TODO adapted_criteres_to_dsu = insert_dsu_garanties(adapted_criteres, year)
    # TODO adapted_criteres_to_dsu_and_dsr = insert_dsr_garanties_communes_nouvelles(adapted_criteres_to_dsu, year)
    # TODO merge with previous years data

    return adapted_criteres  # TODO do not forget to update with latest dataframe
