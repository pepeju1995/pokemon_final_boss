from combat_actions import enemy_pokemon_choice
from combat_menu import fight
from player_pokemon_information import get_player_profile, any_player_pokemon_lives
from pokeload import get_all_pokemons


def main():
    pokemon_list = get_all_pokemons()
    player_profile = get_player_profile(pokemon_list)

    while any_player_pokemon_lives(player_profile):
        fight(player_profile, enemy_pokemon_choice(pokemon_list))

    print("Has perdido en el combate numero {}.".format(player_profile["combats"]))


if __name__ == '__main__':
    main()