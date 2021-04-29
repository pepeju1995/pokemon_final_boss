import random


def get_player_profile(pokemon_list):
    return {
        "player_name": input("¿Cual es tu nombre?"),
        "pokemon_inventory": [random.choice(pokemon_list) for _ in range(3)],
        "combats": 0,
        "pokeballs": 0,
        "health_potion": 0
    }


def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0


def get_pokemon_info(pokemon):
    return "{} | lvl {} | hp {}/{}".format(pokemon["name"],
                                           pokemon["level"],
                                           pokemon["current_health"],
                                           pokemon["base_health"])


def get_attack_info(attack):
    return "{} | hp {} | type {}".format(attack["name"],
                                         attack["damage"],
                                         attack["type"])
