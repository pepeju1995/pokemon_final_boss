import pickle

from requests_html import HTMLSession


pokemon_base = {
    "name": "",
    "current_health": 100,
    "base_health": 100,
    "level": 1,
    "type": None,
    "current_exp": 0
}

URL_BASE = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="


def get_pokemon(index):
    url = "{}{}".format(URL_BASE, index)
    session = HTMLSession()

    new_pokemon = pokemon_base.copy()
    pokemon_page = session.get(url)

    new_pokemon["name"] = pokemon_page.html.find(".mini", first=True).text

    new_pokemon["type"] = []
    for img in pokemon_page.html.find(".pkmain", first=True).find(".bordeambos", first=True).find("img"):
        new_pokemon["type"].append(img.attrs["alt"])

    new_pokemon["attacks"] = []
    attacks_element = pokemon_page.html.find(".pkmain")[-1]
    for atkk in attacks_element.find(".check3"):
        if atkk.find(".center")[0].find("span", first=True).text != "":
            attack = {
                "name": atkk.find(".nav6c", first=True).text,
                "type": atkk.find(".center")[2].find("img", first=True).attrs["alt"],
                "level": int(atkk.find(".center")[0].find("span", first=True).text),
                "damage": int(atkk.find(".center")[4].text.replace("--", "0"))
            }
            new_pokemon["attacks"].append(attack)

    return new_pokemon


def get_all_pokemons():
    try:
        with open("pokefile.pkl", "rb") as pokefile:
            print("Archivo encontrado, vamos a cargarlo!")
            all_pokemons = pickle.load(pokefile)
    except FileNotFoundError:
        print("No hemos encontrado ningun archivo, vamos a crearlo!")
        all_pokemons = []
        for p in range(151):
            all_pokemons.append(get_pokemon(p + 1))
            print(p, end="")
        print("Todos los pokemon han sido descargados!")
        with open("pokefile.pkl", "wb") as pokefile:
            pickle.dump(all_pokemons, pokefile)

    return all_pokemons
