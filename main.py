"""
Author: Marko Njegomir sw-38-2018
"""



from googolplex import Trie
from parse_txt_files import read_results_from_files
from page_graph import Graph
import re
from input_parser import parse_input, next_page_input, any_input_to_continue
import os
from Heap import MaxHeap, Heap_node
from copy import deepcopy
from fitz import fitz  # pip install pymupdf
import time, sys, random
from parse_pdf import get_pdf_content


class Bojanka:
    ZELENA = '\u001b[32m'
    CRVENA = '\u001b[31m'
    CIJAN = '\u001b[36m'
    TAMNO_CRNA = '\u001b[30;1m'
    CRNA = '\u001b[30m'
    BELA = '\u001b[37;1m'
    SVETLO_PLAVA = '\u001b[34;1m'
    BG_PLAVA = '\u001b[44;1m'
    BG_BELA = '\u001b[47;1m'
    BG_ROZA = '\u001b[45m'
    BG_SVETLO_ZUTA = '\u001b[43;1m'
    BG_ZUTA = '\u001b[43m'
    KRAJ = '\033[0m'


def print_googolplex_logo():
    print(Bojanka.CIJAN)
    print("""  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$  /$$       /$$$$$$$  /$$       /$$$$$$$$ /$$   /$$
 /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$| $$      | $$__  $$| $$      | $$_____/| $$  / $$
| $$  \__/| $$  \ $$| $$  \ $$| $$  \__/| $$  \ $$| $$      | $$  \ $$| $$      | $$      |  $$/ $$/
| $$ /$$$$| $$  | $$| $$  | $$| $$ /$$$$| $$  | $$| $$      | $$$$$$$/| $$      | $$$$$    \  $$$$/ 
| $$|_  $$| $$  | $$| $$  | $$| $$|_  $$| $$  | $$| $$      | $$____/ | $$      | $$__/     >$$  $$ 
| $$  \ $$| $$  | $$| $$  | $$| $$  \ $$| $$  | $$| $$      | $$      | $$      | $$       /$$/\  $$
|  $$$$$$/|  $$$$$$/|  $$$$$$/|  $$$$$$/|  $$$$$$/| $$$$$$$$| $$      | $$$$$$$$| $$$$$$$$| $$  \ $$
 \______/  \______/  \______/  \______/  \______/ |________/|__/      |________/|________/|__/  |__/
                                                                                                    
                                                                                                    
                                                                                                    """ + Bojanka.KRAJ)


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_preview(page, expression, results_counter):
    expression = expression.replace("AND", "")
    expression = expression.replace("OR", "")
    expression = expression.replace("NOT", "")
    expression = expression.replace("(", "")
    expression = expression.replace(")", "")
    expression = expression.strip().lower()
    words = expression.split(" ")

    content = page.get_content()

    # print(words)
    word_positions = []
    for word in words:
        if word != "":
            found = page.get_word_positions(word.strip())
            if found:
                word_positions.extend(found)

    word_positions.sort()
    # print(word_positions)
    position = None

    first_position = word_positions[0]
    i = first_position[0]
    if i < 10:
        i = 0
    else:
        i -= 10
    end_counter = len(content) - i
    if end_counter < 100:
        if i < 50:
            i = 0
        else:
            i -= 50
    brojac = 0

    page_num = page.get_page_num()

    first_row = content.split("\n")[0]
    first_row_words = first_row.split(" ")
    header = ''
    for word in first_row_words:
        word = word.strip()
        if word == "" or str.isdigit(word):
            continue
        header += word + " "

    print(Bojanka.CIJAN + str(results_counter + 1) + ") PAGE NUMBER: " + str(
        page_num) + "   Title: " + header + Bojanka.KRAJ)

    number_of_lines = 0
    print("...", end="")
    while i < len(content):
        if not position:
            position = word_positions.pop(0)
        if i == position[0]:
            print(Bojanka.BG_SVETLO_ZUTA, end="")
        if i == position[1]:
            print(Bojanka.KRAJ, end="")
            if word_positions:
                position = word_positions.pop(0)
        if content[i] == "\n":
            number_of_lines += 1
        if brojac >= 200 or number_of_lines >= 2:
            print(Bojanka.KRAJ + "...\n")
            break
        print(content[i], end="")
        i += 1
        brojac += 1


def print_phrase_preview(page, results_counter, matched_positions):
    content = page.get_content()

    matched_positions.sort()
    matched_positions = deepcopy(matched_positions)
    # print(word_positions)
    position = None

    first_position = matched_positions[0]
    i = first_position[0]
    if i < 10:
        i = 0
    else:
        i -= 10
    end_counter = len(content) - i
    if end_counter < 100:
        if i < 50:
            i = 0
        else:
            i -= 50
    brojac = 0

    page_num = page.get_page_num()

    first_row = content.split("\n")[0]
    first_row_words = first_row.split(" ")
    header = ''
    for word in first_row_words:
        word = word.strip()
        if word == "" or str.isdigit(word):
            continue
        header += word + " "

    print(Bojanka.CIJAN + str(results_counter + 1) + ") PAGE NUMBER: " + str(
        page_num) + "   Title: " + header + Bojanka.KRAJ)

    number_of_lines = 0
    print("...", end="")
    end_line = False
    while i < len(content):
        if not position:
            position = matched_positions.pop(0)
        if position[0] <= i < position[1] and not end_line:
            print(Bojanka.BG_SVETLO_ZUTA, end="")
        if i == position[1]:
            print(Bojanka.KRAJ, end="")
            if matched_positions:
                position = matched_positions.pop(0)
        if content[i] == "\n":
            number_of_lines += 1
        if brojac >= 200 or number_of_lines >= 2:
            print(Bojanka.KRAJ + "...\n")
            break
        if i < len(content) - 1:
            if content[i + 1] == "\n" or content[i + 1] == "\t" or content[i] == "\n" or content[i] == "\t" \
                    or content[i + 1] == " ":
                print(Bojanka.KRAJ + content[i], end="")
                end_line = True
            else:
                print(content[i], end="")
                end_line = False
        else:
            end_line = False
            print(content[i], end="")
        i += 1
        brojac += 1


def get_phrase_positions_for_pages(results, graph):
    list_for_sorting = []

    for package in results:
        page = package[0]
        iterator = package[1]
        if not iterator:
            continue
        pozicije = []
        for matchNum, match in enumerate(iterator, start=1):

            # print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
            #                                                                     end=match.end(), match=match.group()))

            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1

                # print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                #                                                                 start=match.start(groupNum),
                #                                                                 end=match.end(groupNum),
                #                                                                 group=match.group(groupNum)))
                print(match.group(groupNum))
            pozicije.append((match.start(), match.end()))
        if not pozicije or len(pozicije) == 0:
            continue
        key = len(pozicije) * 2 + len(graph.incident_edges(page, False)) * 10000
        value = (page, pozicije)
        node = Heap_node(key, value)
        list_for_sorting.append(node)

    if not list_for_sorting:
        return
    heap = MaxHeap(list_for_sorting)
    heap.sort()
    return heap.get_data()


def show_paginated_results_phrase(results, search_query, graph):
    if not results:
        print("\nGoogolplex did not find any results for: {}".format(search_query))
        any_input_to_continue()
        return
    # print(results)

    heap_nodes = get_phrase_positions_for_pages(results, graph)

    if not heap_nodes:
        print("\nGoogolplex did not find any results for: {}".format(search_query))
        any_input_to_continue()
        return
    node_total_number = len(heap_nodes)
    pagination = 10
    page = 0
    while True:
        clear_console()
        print_googolplex_logo()
        print(Bojanka.ZELENA + "Showing results for: {}".format(search_query) + Bojanka.KRAJ)

        brojac = 0
        while (page * 10 + brojac) < node_total_number:
            node = heap_nodes[page * 10 + brojac]
            # print(node.get_value())
            print_phrase_preview(node.get_value()[0], page * 10 + brojac, node.get_value()[1])
            brojac += 1
            if brojac >= pagination:
                break
        print_page_position(page, node_total_number)
        input = next_page_input()
        if input == 0:
            return
        elif input == 1:
            if (page + 1) * 10 > node_total_number:
                formula = node_total_number // ((page + 1) * 10)
                if 0 < formula < 10:
                    page += 1
            else:
                page += 1
        elif input == -1:
            if page > 0:
                page -= 1
        elif input == 2:
            if node_total_number == 0:
                continue
            pdf_pages = []
            if node_total_number > 10:
                pdf_counter = 10
            else:
                pdf_counter = node_total_number
            for j in range(pdf_counter):
                node = heap_nodes[j]
                pdf_pages.append(node.get_value()[0])

            save_as_pdf(pdf_pages, search_query, True)


def find_page_connections(page_content):
    regex = r"see\s*page\s*(\d+)|see\s*pages\s*(\d+)\s*and\s*(\d+)|on\s*page\s*(\d+)"
    matches = re.finditer(regex, page_content, re.IGNORECASE)
    grupe = []
    for matchNum, match in enumerate(matches, start=1):

        # print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
        #                                                                     end=match.end(), match=match.group()))

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1

            # print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
            #                                                                 start=match.start(groupNum),
            #                                                                 end=match.end(groupNum),
            #                                                                 group=match.group(groupNum)))
            # print(match.group(groupNum))
        grupe.append(match.groups())
    return grupe  # primer povratne vrednosti [(None, None, None, '123'), (None, None, None, '125')]


def connect_all_pages(all_connections, graph):
    brojac = 0
    for page in all_connections:
        current_connections = all_connections[page]
        for con in current_connections:
            for i in range(0, 4):
                page_number = con[i]
                if page_number:
                    brojac += 1
                    destination = graph.get_vertex_by_page_num(int(page_number))
                    graph.insert_edge(page, destination)
    # print("Brojac = " + str(brojac))


def load_text_from_files(tri, page_graph):
    out_path = 'Data Structures and Algorithms in Python'
    pdf_path = 'Data Structures and Algorithms in Python.pdf'
    results = read_results_from_files(out_path)
    # results = get_pdf_content(pdf_path)
    """
    Results su sve stranice kojima je index kljuc u recniku
    'index'
    'page_number'
    'content'
    """

    pages_and_conections = {}

    clear_console()
    print(Bojanka.ZELENA + "\nLoading GOOGOLPLEX...")
    increment = 100/len(results)
    i = 0
    for key in results:
        sirina = int((i + 1) / 4)
        bar = "\r[" + "#" * sirina + " " * (25 - sirina) + "]"
        sys.stdout.write(bar)
        sys.stdout.flush()

        page = results[key]

        page_index = page.get("index")
        page_num = page.get("page_number")
        content = page.get("content")
        page_vertex = page_graph.insert_vertex(page_index, page_num, content)
        connections = find_page_connections(page_vertex.get_content())
        pages_and_conections[page_vertex] = connections
        tri.createTrieFromPage(page_vertex)
        i += increment
    print(Bojanka.KRAJ)
    connect_all_pages(pages_and_conections, page_graph)


def clean_word(expression):
    if not expression:
        return ""
    expression = expression.replace("AND", "")
    expression = expression.replace("OR", "")
    expression = expression.replace("NOT", "")
    expression = expression.replace("(", " ")
    expression = expression.replace(")", " ")
    expression = expression.strip()
    return expression


def save_as_pdf(pages, search_query, phrase=False):
    exists = False
    try:
        doc = fitz.open("topResults.pdf")
        exists = True
    except:
        doc = fitz.open()
    doc.deletePageRange(0, -1)
    try:
        p = fitz.Point(50, 70)
        search_query = clean_word(search_query)
        highlight_words = search_query.split()
        for page in pages:
            pdf_page = doc.newPage()
            pdf_page.insertText(p,  # bottom-left of 1st char
                                page.get_content(),  # the text (honors '\n')
                                fontname="helv",  # the default font
                                fontsize=11,  # the default font size
                                rotate=0,  # also available: 90, 180, 270
                                )
            if not phrase:
                for word in highlight_words:
                    word = word.strip()
                    text_instances = pdf_page.searchFor(word)
                    for instance in text_instances:
                        pdf_page.addHighlightAnnot(instance)
            else:
                text_instances = pdf_page.searchFor(search_query)
                for instance in text_instances:
                    pdf_page.addHighlightAnnot(instance)

        if exists:
            doc.save("topResults.pdf", incremental=1)
        else:
            doc.save("topResults.pdf", garbage=4, deflate=True, clean=True)
        doc.close()
    except:
        print("Saving to pdf failed!")
        return


def show_paginated_results(heap, search_query, tri):
    if not heap:
        print("\nGoogolplex did not find any results for: {}".format(search_query))
        return

    autocorrect = None
    if not isinstance(heap, MaxHeap):
        if len(heap) == 2:
            print(Bojanka.ZELENA + "Showing results for: {}".format(search_query) + Bojanka.KRAJ)
            tri.print_autocorrect_suggestions(heap[0], heap[1])
            print("\nGoogolplex did not find any results for: {}".format(search_query))
            any_input_to_continue()
            return
        if len(heap) == 3:
            print("Showing results for: {}".format(search_query))
            autocorrect = heap[1], heap[2]
            tri.print_autocorrect_suggestions(heap[1], heap[2])
            heap = heap[0]
    heap_nodes = heap.get_data()
    node_total_number = len(heap_nodes)
    # print(node_total_number)
    pagination = 10
    page = 0
    while True:
        clear_console()
        print_googolplex_logo()
        print(Bojanka.ZELENA + "Showing results for: {}".format(search_query) + Bojanka.KRAJ)
        if autocorrect:
            tri.print_autocorrect_suggestions(autocorrect[0], autocorrect[1])
        brojac = 0
        while (page * 10 + brojac) < node_total_number:
            node = heap_nodes[page * 10 + brojac]
            print_preview(node.get_value(), search_query, page * 10 + brojac)
            brojac += 1
            if brojac >= pagination:
                break
        print_page_position(page, node_total_number)
        input = next_page_input()
        if input == 0:
            return
        elif input == 1:
            if (page + 1) * 10 > node_total_number:
                formula = node_total_number // ((page + 1) * 10)
                if 0 < formula < 10:
                    # print("next page ")
                    page += 1
            else:
                page += 1
        elif input == -1:
            if page > 0:
                page -= 1
                # print("previous page")
        elif input == 2:
            if node_total_number == 0:
                continue
            pdf_pages = []
            if node_total_number > 10:
                pdf_counter = 10
            else:
                pdf_counter = node_total_number
            for j in range(pdf_counter):
                node = heap_nodes[j]
                pdf_pages.append(node.get_value())

            save_as_pdf(pdf_pages, search_query)


def print_page_position(page_num, total_pages):
    print(Bojanka.CIJAN + "G " + Bojanka.KRAJ, end="")
    i = 0
    while i < total_pages:
        if i >= 10:
            break
        if i % 10 == page_num % 10:
            print(Bojanka.BG_ROZA + "O" + Bojanka.KRAJ, end=" ")
        else:
            print(Bojanka.CIJAN + "O " + Bojanka.KRAJ, end="")
        i += 1

    if total_pages < 2:
        print(Bojanka.CIJAN + "O G O L P L E X" + Bojanka.KRAJ)
    else:
        print(Bojanka.CIJAN + "G O L P L E X" + Bojanka.KRAJ)


def print_autocomplete_suggestions(tri, expression):
    expression = expression.strip()
    words = expression.split()
    prefix = words[-1]
    clean = ""
    for i in range(len(prefix)):
        if str.isalnum(prefix[i]):
            clean += prefix[i]
    print(clean)
    tri.print_suggestions_autocomplete(clean)
    any_input_to_continue()


def loading():
    clear_console()
    print(Bojanka.ZELENA + "\nLoading GOOGOLPLEX...")

    for i in range(0, 100):
        sirina = int((i + 1) / 4)
        bar = "\r[" + "#" * sirina + " " * (25 - sirina) + "]"
        time.sleep(0.05)
        sys.stdout.write(bar)
        sys.stdout.flush()
    print(Bojanka.KRAJ)


def main():
    # loading()
    page_graph = Graph(True)
    tri = Trie(page_graph)
    load_text_from_files(tri, page_graph)

    while True:
        clear_console()
        print_googolplex_logo()
        search_query = parse_input()
        if not search_query:
            continue
        if search_query[0] == "phrase":
            results = tri.find_phrase(search_query[1], page_graph)
            show_paginated_results_phrase(results, search_query[1], page_graph)
        elif search_query[0] == "logical":
            results = tri.get_sorted_ranked_pages_logical(search_query[1], page_graph)
            show_paginated_results(results, search_query[1], tri)
        elif search_query[0] == "regular":
            results = tri.get_sorted_ranked_pages_logical(search_query[1], page_graph)
            show_paginated_results(results, search_query[1], tri)
        elif search_query[0] == "autocomplete":
            print_autocomplete_suggestions(tri, search_query[1])
        elif search_query[0] == "exit":
            break
    clear_console()


if __name__ == '__main__':
    main()
