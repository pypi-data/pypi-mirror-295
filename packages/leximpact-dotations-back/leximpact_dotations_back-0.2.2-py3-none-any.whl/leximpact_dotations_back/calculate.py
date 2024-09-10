import logging

from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france_dotations_locales import (
    CountryTaxBenefitSystem as OpenFiscaFranceDotationsLocales,
)


CURRENT_YEAR = 2024
model = OpenFiscaFranceDotationsLocales()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_simulation_with_data(model, period, data):
    sb = SimulationBuilder()
    sb.create_entities(model)
    sb.declare_person_entity("commune", data.index)

    etat_instance = sb.declare_entity("etat", ["france"])
    nombre_communes = len(data.index)
    etat_communes = ["france"] * nombre_communes
    communes_etats_roles = [None] * nombre_communes  # no roles in our model
    sb.join_with_persons(etat_instance, etat_communes, communes_etats_roles)

    simulation = sb.build(model)
    # TODO vérifier nécessité : simulation.max_spiral_loops = 10

    return simulation
