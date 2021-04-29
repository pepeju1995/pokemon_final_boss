import random

from player_pokemon_information import get_pokemon_info, get_attack_info

TYPES = ("normal", "fuego", "agua", "planta", "electrico", "hielo", "lucha", "veneno", "tierra", "volador", "psiquico",
         "bicho", "roca", "fantasma", "dragon", "siniestro", "acero", "hada")

WEAK_TYPES = (("lucha",), ("agua", "tierra", "roca"), ("planta", "electrico"),
              ("fuego", "hielo", "veneno", "volador", "bicho"), ("tierra",), ("fuego", "lucha", "roca", "acero"),
              ("volador", "psiquico", "hada"), ("tierra", "psiquico"), ("agua", "planta", "hielo"),
              ("electrico", "hielo", "roca"), ("bicho", "fantasma", "siniestro"), ("volador", "roca", "fuego"),
              ("agua", "planta", "lucha", "tierra", "acero"), ("fantasma", "siniestro"), ("hielo", "dragon", "hada"),
              ("lucha", "bicho", "hada"), ("fuego", "lucha", "tierra"), ("veneno", "acero"))


def enemy_pokemon_choice(pokemon_list):
    election = random.choice(pokemon_list)
    election["level"] = random.randint(election["attacks"][1]["level"], election["attacks"][-1]["level"])
    attacks = attacks_disponibility(election)
    while len(attacks) == 0:
        enemy_pokemon_choice(pokemon_list)
    return election


def choose_pokemon(player_profile):
    pokemon_player = None
    pokemon_diponibility = []
    for poke in player_profile["pokemon_inventory"]:
        if poke["current_health"] > 0:
            pokemon_diponibility.append(poke)

    while pokemon_player is None:
        print("\nEstos son los pokemon que puedes elegir:")
        for index in range(len(pokemon_diponibility)):
            print("{} - {}".format(index, get_pokemon_info(pokemon_diponibility[index])))

        try:
            election = int(input("¿Que pokemon eliges?: "))
            return player_profile["pokemon_inventory"][player_profile["pokemon_inventory"].index(pokemon_diponibility[election])]
        except (ValueError, IndexError):
            print("Opcion no valida.")

    return pokemon_player


def attacks_disponibility(pokemon):
    attacks = []
    for a in pokemon["attacks"]:
        if a["level"] <= pokemon["level"]:
            attacks.append(a)
    return attacks


def choose_attack(pokemon):
    attack = None
    attacks = attacks_disponibility(pokemon)
    while attack is None:
        for index in range(len(attacks)):
            print("{} - {}".format(index, get_attack_info(attacks[index])))

        try:
            return attacks[int(input("¿Que ataque utilizas?: "))]
        except (ValueError, IndexError):
            print("Opcion no valida.")


def current_health_combat(player_pokemon, enemy_pokemon):
    return "Vida acutal de {}: {}\n" \
           "Vida acutal de {}: {}".format(player_pokemon["name"], player_pokemon["current_health"],
                                          enemy_pokemon["name"], enemy_pokemon["current_health"])


def player_attack(player_pokemon, enemy_pokemon):
    print("Es turno de {}, ¿que ataque deseas utilizar?:".format(player_pokemon["name"]))
    attack = choose_attack(player_pokemon)
    print("{} uso {}".format(player_pokemon["name"], attack["name"]))
    bonification = False
    enemy_type = enemy_pokemon["type"]

    if attack["type"] in WEAK_TYPES[TYPES.index(enemy_type[0])]:
        bonification = True

        if len(enemy_type) == 2 and not bonification:
            if attack["type"] in WEAK_TYPES[TYPES.index(enemy_type[1])]:
                bonification = True

    if bonification:
        enemy_pokemon["current_health"] -= 1.5 * attack["damage"]
    else:
        enemy_pokemon["current_health"] -= attack["damage"]

    if enemy_pokemon["current_health"] < 0:
        enemy_pokemon["current_health"] = 0
    print(current_health_combat(player_pokemon, enemy_pokemon))
    input("Presiona ENTER para continuar...")


def enemy_attack(enemy_pokemon, player_pokemon):
    print("Es turno de {}, ¿que ataque deseas utilizar?:".format(enemy_pokemon["name"]))
    attacks = attacks_disponibility(enemy_pokemon)
    attack = random.choice(attacks)
    print("{} uso {}".format(enemy_pokemon["name"], attack["name"]))
    bonification = False
    player_type = player_pokemon["type"]

    if attack["type"] in WEAK_TYPES[TYPES.index(player_type[0])]:
        bonification = True

        if len(player_type) == 2 and not bonification:
            if attack["type"] in WEAK_TYPES[TYPES.index(player_type[1])]:
                bonification = True

    if bonification:
        player_pokemon["current_health"] -= 1.25 * attack["damage"]
    else:
        player_pokemon["current_health"] -= attack["damage"]

    if player_pokemon["current_health"] < 0:
        player_pokemon["current_health"] = 0
    print(current_health_combat(player_pokemon, enemy_pokemon))
    input("Presiona ENTER para continuar...")


def assign_experience(attack_history):
    for pokemon in attack_history:
        points = random.randint(1, 5)
        pokemon["current_exp"] += points

        while pokemon["current_exp"] > 20:
            pokemon["current_exp"] -= 20
            pokemon["level"] += 1
            pokemon["base_health"] += 5
            pokemon["current_health"] = pokemon["base_health"]
            print("Tu pokemon ha  subido de nivel: {}".format(get_pokemon_info(pokemon)))


def raffle_of_objects(player_profile):
    amount = random.randint(1, 5)
    reward = random.randint(1, 2)

    if reward == 1:
        player_profile["pokeballs"] += amount
        print("Has conseguido {} pokeballs.".format(amount))
    else:
        player_profile["health_potion"] += amount
        print("Has conseguido {} pociones.".format(amount))
