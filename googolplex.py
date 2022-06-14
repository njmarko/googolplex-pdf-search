"""
Author: Marko Njegomir sw-38-2018
"""


from page_graph import Graph
import re
from stack import Stack
from Heap import MaxHeap, Heap_node
from didyoumean import didyoumean


class Bojanka:
    ZELENA = '\u001b[32m'
    CRVENA = '\u001b[31m'
    CIJAN = '\u001b[36m'
    CRNA = '\u001b[30;1m'
    BELA = '\u001b[37;1m'
    SVETLO_PLAVA = '\u001b[34;1m'
    PLAVA = '\u001b[34m'
    BG_PLAVA = '\u001b[44;1m'
    BG_BELA = '\u001b[47;1m'
    BG_ROZA = '\u001b[45m'
    BG_SVETLO_ZUTA = '\u001b[43;1m'
    KRAJ = '\033[0m'


class LogicalOperators(object):
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    ALL_OPERATORS = ('AND', 'OR', 'NOT')


class Node(object):

    def __init__(self):
        self._children = {}
        self._isEnd = False
        self._page_and_position = set()
        self._next_words = {}

    def get_children(self):
        return self._children

    def set_children(self, new_children):
        self._children = new_children

    def get_pages_and_positions(self):
        return self._page_and_position

    def add_page(self, page_vertex):
        if page_vertex not in self._page_and_position:
            self._page_and_position.add(page_vertex)

    def add_next_word(self, word, page):
        if word not in self._next_words:
            self._next_words[word] = [page]
        else:
            self._next_words[word].append(page)

    def get_next_word(self, word):
        if word in self._next_words:
            return self._next_words[word]

    def is_end(self):
        return self._isEnd

    def set_is_end(self, bool):
        self._isEnd = bool

    def __str__(self):
        return "this is Trie node"


class Trie(object):

    def __init__(self, page_graph):
        self._root = Node()
        self._words = []
        self._page_graph = page_graph
        self._all_words_in_document = set()

    def insert(self, word, page_vertex, position):

        current = self._root

        for letter in list(word):
            if current.get_children().get(letter) is None:
                current.get_children()[letter] = Node()
            current = current.get_children()[letter]

        current.set_is_end(True)
        page_vertex.add_word_position(word, position)
        page_vertex.set_word_rank(word, 0)
        current.add_page(page_vertex)
        self._all_words_in_document.add(word)
        return current

    def createTrieFromPage(self, page_vertex):
        # prvo isecem sve reci iz sadrzaja
        content = page_vertex.get_content()
        start = 0
        end = 0
        word = ""
        previous_node = None
        for i in range(len(content)):
            if not content[i].isalnum():
                position = (start, end)
                current_node = self.insert(word, page_vertex, position)
                if not previous_node:
                    previous_node = current_node
                else:
                    previous_node.add_next_word(word, page_vertex)
                    previous_node = current_node
                start += len(word) + 1
                end = start
                word = ""
                continue
            word += content[i].lower()
            end += 1

    def build_regex(self, words):
        if not words:
            return
        regex = r"" + words[0] + " \s*"
        i = 1
        while i < len(words):
            regex += words[i] + " \s*"
            i += 1
        return regex

    def find_phrase(self, phrase, graph):
        if not phrase:
            return
        words = phrase.strip().split(" ")
        regex = self.build_regex(words)
        ret_val = []
        # print(regex)
        word = words[0]
        node = self.search(word)
        found_on_pages = None
        if node and node[1] and node[2]:
            found_on_pages = node[0].get_pages_and_positions()
        if not found_on_pages:
            return ret_val
        for page in found_on_pages:
            content = page.get_content()
            # print(page.get_page_num())
            match = re.finditer(regex, content, re.IGNORECASE)
            # print(match)
            if match:
                ret_val.append((page, match))
        return ret_val

    def search(self, word):
        current = self._root
        score = True

        for letter in list(word):
            if current.get_children().get(letter) is None:
                score = False
                break
            current = current.get_children()[letter]
        ret_val = current, current.is_end(), score
        return ret_val

    def get_all_results(self, word):
        node = self.search(word)
        if not node[1] or not node[2]:
            # print("No {} in text".format(word))
            return set()
        return node[0].get_pages_and_positions()

    def evaluate_page_rank(self, word, graph, page):
        word_count = page.get_word_positions(word)
        if word_count:
            num_words_in_page = len(word_count)
        else:
            num_words_in_page = 0
        in_edges = graph.incident_edges(page, False)
        num_words_in_edges = 0
        for edge in in_edges:
            source_page = edge.get_source()
            if source_page.get_word_positions(word):
                words_in_source = len(source_page.get_word_positions(word))
            else:
                words_in_source = 0
            num_words_in_edges += words_in_source
        rank = num_words_in_page * 2 + len(in_edges) * 10000 + num_words_in_edges
        page.set_word_rank(word, rank)
        return page

    def get_top_results_one_word(self, word, graph):
        all_hits = self.get_all_results(word)
        ranked_pages = set()
        for page in all_hits:
            ranked_pages.add(self.evaluate_page_rank(word, graph, page))
        return ranked_pages

    def get_pages_from_expression(self, expression, graph):
        words = expression.strip().split(" ")
        logic_que = []
        results_que = []
        for word in words:
            if word in LogicalOperators.ALL_OPERATORS:
                logic_que.append(word)
                continue
            pages = self.get_top_results_one_word(word, graph)
            results_que.append(pages)
        final_result = None
        if results_que:
            final_result = results_que.pop(0)
        while results_que:
            operator = logic_que.pop(0)
            if operator == LogicalOperators.AND:
                final_result = final_result.intersection(results_que.pop(0))
            elif operator == LogicalOperators.OR:
                final_result = final_result.union(results_que.pop(0))
            elif operator == LogicalOperators.NOT:
                final_result = final_result.difference(results_que.pop(0))
        return final_result

    def clean_word(self, expression):
        if not expression:
            return ""
        expression = expression.replace("AND", "")
        expression = expression.replace("OR", "")
        expression = expression.replace("NOT", "")
        expression = expression.replace("(", " ")
        expression = expression.replace(")", " ")
        expression = expression.strip()
        return expression

    def convert_to_postfix(self, expression):

        prioritet = {'AND': 2, 'OR': 2, "NOT": 2, "(": 1}

        postfix = []
        operators = Stack()

        words = expression.strip().split(" ")

        consequtive_words = False

        for word in words:
            word = word.strip()
            if word == "":
                continue
            if consequtive_words:
                clean_word = self.clean_word(word)
                if clean_word:
                    while not operators.is_empty() and prioritet[operators.top()] >= prioritet["OR"]:
                        postfix.append(operators.pop())
                    operators.push("OR")
                    consequtive_words = False

            if word[0] == "(":
                word = word.replace("(", "")
                operators.push("(")

            if word == "":
                continue
            if word != "AND" and word != "OR" and word != "NOT" and word != "(" and word != ")":
                if word[-1] == ")":
                    try:
                        word = word.replace(")", "")
                        if word in prioritet:
                            while not operators.is_empty() and prioritet[operators.top()] >= prioritet[word]:
                                postfix.append(operators.pop())
                            operators.push(word)
                        else:
                            word = word.lower()
                            postfix.append(word)
                            top = operators.pop()
                            consequtive_words = True
                            while top != '(':
                                postfix.append(top)
                                top = operators.pop()
                    except:
                        return ""
                    continue
                word = word.lower()
                postfix.append(word)
                consequtive_words = True
            elif word == '(':
                operators.push(word)
            elif word == ')':
                try:
                    top = operators.pop()
                    while top != '(':
                        postfix.append(top)
                        top = operators.pop()
                except:
                    return ""
            else:
                consequtive_words = False
                while not operators.is_empty() and prioritet[operators.top()] >= prioritet[word]:
                    postfix.append(operators.pop())
                operators.push(word)
        while not operators.is_empty():
            if operators.top() == "(":
                operators.pop()
                continue
            postfix.append(operators.pop())

        return " ".join(postfix)

    def evaluate_postfix(self, postfix_expression, page_graph):

        operators = Stack()

        words = postfix_expression.split()

        for word in words:
            if word != "AND" and word != "OR" and word != "NOT" and word != "(" and word != ")":
                operators.push(word)

            else:
                word = word.replace("(", "")
                word = word.replace(")", "")
                try:
                    druga_rec = operators.pop()
                    prva_rec = operators.pop()
                except:
                    return

                result = self.calculate_logical_expression(word, prva_rec, druga_rec, page_graph)
                operators.push(result)
        ret_val = operators.pop()
        if isinstance(ret_val, set):
            return ret_val
        else:
            return self.get_top_results_one_word(ret_val, page_graph)

    def calculate_logical_expression(self, operacija, prva_rec, druga_rec, page_graph):

        if not isinstance(prva_rec, set):
            prva_rec_pages = self.get_top_results_one_word(prva_rec, page_graph)
        else:
            prva_rec_pages = prva_rec

        if not isinstance(druga_rec, set):
            druga_rec_pages = self.get_top_results_one_word(druga_rec, page_graph)
        else:
            druga_rec_pages = druga_rec

        final_result = set()
        if operacija == LogicalOperators.AND:
            final_result = prva_rec_pages.intersection(druga_rec_pages)
        elif operacija == LogicalOperators.OR:
            final_result = prva_rec_pages.union(druga_rec_pages)
        elif operacija == LogicalOperators.NOT:
            final_result = prva_rec_pages.difference(druga_rec_pages)

        return final_result

    def create_ranked_node(self, page, expression, graph):

        expression = expression.replace("AND", "")
        expression = expression.replace("OR", "")
        expression = expression.replace("NOT", "")
        expression = expression.replace("(", "")
        expression = expression.replace(")", "")
        words = expression.split(" ")

        found_words_num = 0

        total_rank = 0

        for word in words:
            word.strip()
            if not word:
                continue
            self.evaluate_page_rank(word, graph, page)
            if word in page.get_word_ranks():
                word_rank = page.get_word_rank(word)
                if word_rank > 0:
                    total_rank += word_rank
                    found_words_num += 1000  # stranica na kojoj se pojavljuju sve reci imace vecu vrednost

        key = total_rank + found_words_num
        # print(str(key) + " key value")
        heap_node = Heap_node(key, page)
        return heap_node

    def get_sorted_ranked_pages_logical(self, expression, graph):
        postfix_expression = self.convert_to_postfix(expression)
        if postfix_expression == "":
            return None
        page_results = self.evaluate_postfix(postfix_expression, graph)
        if not page_results:
            return self.auto_suggest(postfix_expression), postfix_expression

        ranked_pages = []

        for page in page_results:
            heap_node = self.create_ranked_node(page, expression, graph)
            if not heap_node:
                continue
            ranked_pages.append(heap_node)

        max_sorted_heap = MaxHeap(ranked_pages)
        max_sorted_heap.sort()

        if len(page_results) < 5:
            return max_sorted_heap, self.auto_suggest(postfix_expression), postfix_expression  # 3 povratne vrednosti
        else:
            return max_sorted_heap  # 1 povratna vrednost

    def print_autocorrect_suggestions(self, suggestions, expression):
        expression = self.clean_word(expression)
        words = expression.split()

        same_words = True
        for i in range(len(suggestions)):
            if suggestions[i] != words[i]:
                same_words = False
                break
        if same_words:
            return

        print("Did you mean: ", end=" ")
        for i in range(len(suggestions)):
            if not suggestions[i]:
                print(words[i].strip(), end=" ")
                continue
            if suggestions[i] != words[i]:
                print(Bojanka.PLAVA + Bojanka.BG_BELA + suggestions[i] + Bojanka.KRAJ, end=" ")
            else:
                print(words[i].strip(), end=" ")
        print(Bojanka.KRAJ + "\n")

    def auto_suggest(self, expression):
        expression = self.clean_word(expression)
        words = expression.split()

        suggestions = []
        for word in words:
            word = word.strip()
            sug_word = didyoumean.didYouMean(word, self._all_words_in_document)
            suggestions.append(sug_word)
        return suggestions

    def suggestions_autocomplete(self, node, word):

        if node.is_end():
            self._words.append(word)
        for w, node in node.get_children().items():
            self.suggestions_autocomplete(node, word + w)

    def print_suggestions_autocomplete(self, prefix):

        current = self._root
        score = False
        word = ""

        for letter in list(prefix):
            if current.get_children().get(letter) is None:
                score = True
                break

            word += letter
            current = current.get_children()[letter]

        if score:
            return 0
        elif current.is_end() and current.get_children() is None:
            return -1
        self.suggestions_autocomplete(current, word)

        counter = 0
        total = 0
        print(Bojanka.CIJAN + "Autocomplete suggestions: " + Bojanka.KRAJ, end=" ")
        for found in self._words:
            if counter >= 10:
                print()
                counter = 0
            if counter == 0:
                print(Bojanka.ZELENA + found + Bojanka.KRAJ, end=" ")
            else:
                print(Bojanka.ZELENA + ", " + found + Bojanka.KRAJ, end=" ")
            counter += 1
            total += 1
            if total == 20:
                break
        self._words = []
        print()
        return 1
