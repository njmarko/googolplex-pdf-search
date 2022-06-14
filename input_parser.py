"""
Author: Marko Njegomir sw-38-2018
"""



def parse_input():
    unos = input("Search googolplex($ at the end for autocomplete): ")
    if not unos:
        print("You have to type in something. Please try again.")
        any_input_to_continue()
        return
    unos = unos.strip()
    if not unos:
        print("You have to type in something. Please try again.")
        any_input_to_continue()
        return

    if unos == ":q" or unos == ":wq" or unos == ":q!" or unos == ":x" or unos == ":qa":
        return ("exit", unos)

    if unos[0] == "\"":
        unos = unos.replace("\"", "")
        unos = unos.strip()

        print("You entered a phrase {}".format(unos))
        return ("phrase", unos)

    lista_reci = unos.lower().split(" ")
    if "and" in lista_reci or "or" in lista_reci or "not" in lista_reci:
        for i in range(len(lista_reci)):
            lista_reci[i] = lista_reci[i].strip()
        return ("logical", unos)

    if lista_reci[-1]:
        if lista_reci[-1][-1] == "$":
            return ("autocomplete", unos)
    return ("regular", unos)


def next_page_input():

    unos = input("Press n for next, and b for back <pdf to export><x to search again>")
    if not unos.strip():
        return 1
    if unos.lower().strip() == "x":
        return 0
    if unos.lower().strip() == "b":
        return -1
    if unos.lower().strip() == "pdf":
        return 2
    return 1

def any_input_to_continue():
    input("Press any key to continue.")
