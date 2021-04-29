import os
import random

from combat_actions import player_attack, choose_pokemon, enemy_attack, raffle_of_objects, assign_experience
from player_pokemon_information import any_player_pokemon_lives, get_pokemon_info


def capture_pokemon(enemy_pokemon, player_profile):
    if player_profile["pokeballs"] > 0:
        if enemy_pokemon["current_health"] < 40:
            capture_ratio = random.randint(1, 2)
            if capture_ratio == 1:
                player_profile["pokemon_inventory"].append(enemy_pokemon)
                print("Has capturado a {}".format(enemy_pokemon["name"]))
                return True
        elif 40 < enemy_pokemon["current_health"] < 80:
            capture_ratio = random.randint(1, 3)
            if capture_ratio == 1:
                player_profile["pokemon_inventory"].append(enemy_pokemon)
                print("Has capturado a {}".format(enemy_pokemon["name"]))
                return True
        elif enemy_pokemon["current_health"] > 80:
            capture_ratio = random.randint(1, 5)
            if capture_ratio == 1:
                player_profile["pokemon_inventory"].append(enemy_pokemon)
                print("Has capturado a {}".format(enemy_pokemon["name"]))
                return True
        player_profile["pokeballs"] -= 1
        print("El pokemon se ha escapado")
    else:
        print("No tienes pokeballs.")
    return False


def cure_pokemon(player_profile, player_pokemon):
    if player_profile["health_potion"] > 0:
        player_pokemon["current_health"] += 50
        if player_pokemon["current_health"] > player_pokemon["base_health"]:
            player_pokemon["current_health"] = player_pokemon["base_health"]
        print("{} se ha curado, su vida actual es {}.".format(player_pokemon["name"], player_pokemon["current_health"]))
        player_profile["health_potion"] -= 1
    print("No tienes pociones")


def menu(player_profile, player_pokemon, enemy_pokemon, capture, attack_history=None):
    action = None
    while action not in ["A", "P", "V", "C"]:
        action = input("¿Que deseas hacer?: [A]tacar, [P]okeball, Pocion de [V]ida, [C]ambiar")

    if action == "A":
        player_attack(player_pokemon, enemy_pokemon)
        attack_history.append(player_pokemon)
    elif action == "P":
        capture = capture_pokemon(enemy_pokemon, player_profile)
    elif action == "V":
        cure_pokemon(player_profile, player_pokemon)
        pass
    elif action == "C":
        player_pokemon = choose_pokemon(player_profile)
    os.system("cls")

    if enemy_pokemon["current_health"] > 0 and not capture:
        enemy_attack(enemy_pokemon, player_pokemon)

    if player_pokemon["current_health"] == 0 and any_player_pokemon_lives(player_profile):
        player_pokemon = choose_pokemon(player_profile)

    return capture, player_pokemon


def fight(player_profile, enemy_pokemon):
    print("--- EMPIEZA EL COMBATE ---")

    capture = False
    attack_history = []
    player_pokemon = choose_pokemon(player_profile)
    print("Contincantes: {} vs {}".format(get_pokemon_info(player_pokemon),
                                          get_pokemon_info(enemy_pokemon)))

    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0 and not capture:
        capture, player_pokemon = menu(player_profile, player_pokemon, enemy_pokemon, capture, attack_history)
        os.system("cls")

    os.system("cls")
    if any_player_pokemon_lives(player_profile):
        print("Has ganado el combate.")
        raffle_of_objects(player_profile)
        assign_experience(attack_history)

    print("--- FIN DEL COMBATE ---")
    input("Presiona ENTER para continuar...")
