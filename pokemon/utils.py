from typing import List, Tuple
import logging
from pokemon.models import Pokemon

logger = logging.getLogger(__name__)


class PokemonUtils:

    @classmethod
    def get_pokemon(cls, pokemon_id: int = None, pokemon: Pokemon = None) -> Pokemon:
        return pokemon or Pokemon.objects.filter(pk=pokemon_id).first()


    @classmethod
    def create_update_pokemon(
            cls, pokemon_id: int = None, pokemon: Pokemon = None, name: str = None, species: str = None,
            height: float = None, weight: float = None, growth_rate: str = None, type: List[str] = None,
            abilities: List[str] = None, egg_groups: List[str] = None, ev_yield: List[str] = None) -> Tuple[bool, Pokemon or None, str]:

        pokemon: Pokemon = cls.get_pokemon(pokemon_id=pokemon_id, pokemon=pokemon) or Pokemon()
        logger.info("")
        if name is not None:
            pokemon.name = name
        if species is not None:
            pokemon.species = species
        if height is not None:
            pokemon.height = height
        if weight is not None:
            pokemon.weight = weight
        if growth_rate is not None:
            pokemon.growth_rate = growth_rate

        pokemon.save()
        if type is not None and type.__class__ == list:
            pokemon.type.set(type)
        if abilities is not None and abilities.__class__ == list:
            pokemon.abilities.set(type)
        if egg_groups is not None and egg_groups.__class__ == list:
            pokemon.egg_groups.set(egg_groups)
        if ev_yield is not None and ev_yield.__class__ == list:
            pokemon.ev_yield.set(ev_yield)

        logger.info("")
        return True, pokemon, "Created / Updated Successfully"

