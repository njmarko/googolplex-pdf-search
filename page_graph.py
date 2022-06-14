"""
Author: Marko Njegomir sw-38-2018
"""


class Vertex(object):

    def __init__(self, index, page_num, content):
        self._index = index
        self._page_num = page_num
        self._content = content
        self._word_positions = {}
        self._word_ranks = {}

    def get_index(self):
        return self._index

    def get_page_num(self):
        return self._page_num

    def get_content(self):
        return self._content

    def get_word_ranks(self):
        return self._word_ranks

    def set_word_rank(self, word, value):
        self._word_ranks[word] = value

    def get_word_rank(self, word):
        if word in self._word_ranks:
            return self._word_ranks[word]

    def set_word_ranks(self, new_rank):
        self._word_ranks = new_rank

    def add_word_position(self, word, position):
        if word in self._word_positions:
            self._word_positions[word].append(position)
            return
        self._word_positions[word] = [position]

    def get_all_word_positions(self):
        return self._word_positions

    def get_word_positions(self, word):
        if word in self._word_positions:
            return self._word_positions[word]

    def __str__(self):
        return "Page with index " + str(self._index)

    def __hash__(self):
        return hash(self._index)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._index == other.get_index()


class Edge(object):
    def __init__(self, dest, sorc, value=None):
        self._value = value
        self._destination = dest
        self._source = sorc

    def get_source(self):
        return self._source

    def get_destination(self):
        return self._destination

    def get_value(self):
        return self._value

    def __str__(self):
        return str((str(self._source), str(self._destination)))


class Graph(object):
    def __init__(self, directed=False):
        self._out = {}
        self._in = {}
        self._directed = directed

    def get_out(self):
        return self._out

    def get_in(self):
        return self._in

    def insert_vertex(self, index, page_num, content):
        v = Vertex(index, page_num, content)
        self._out[v] = []
        self._in[v] = []
        return v

    def insert_edge(self, source, dest, elem=None):
        edge = Edge(source, dest, elem)
        oposite = Edge(dest, source, elem)
        if self._directed:
            self._out[source].append(edge)
            self._in[dest].append(edge)
        else:
            self._out[source].append(edge)
            self._out[dest].append(oposite)
            self._in[source].append(oposite)
            self._in[dest].append(edge)

    def vertex_count(self):
        return len(self._in)

    def vertices(self):
        if self._directed:
            vertices = {}
            for vertex in self._out.keys():
                vertices[vertex] = vertex
            for vertex in self._in.keys():
                vertices[vertex] = vertex
            return vertices
        else:
            return self._out.keys()

    def get_vertex(self, vertex_index):
        vertices = self.vertices()
        if vertex_index in vertices:
            return vertices[vertex_index]

    def get_vertex_by_page_num(self, page_num):
        vertices = self.vertices()
        for vertex in vertices:
            if vertices[vertex].get_page_num() == page_num:
                return vertices[vertex]

    def edges(self):
        ret_val = []
        for veze in self._out.values():
            ret_val.extend(veze)
        return ret_val

    def degree(self, vertex, out=True):
        if out:
            return len(self._out[vertex])
        return len(self._in[vertex])

    def incident_edges(self, vertex, out=True):
        if out:
            return self._out[vertex]
        return self._in[vertex]

    def remove_vertex(self, vertex):
        izlazne = self._out[vertex]
        self._out.pop(vertex)
        ulazne = self._in[vertex]
        self._in.pop(vertex)
        for veza in izlazne:
            self._in[veza[1]].pop(veza)
        for veza in ulazne:
            self._out[veza[1]].pop(veza)

    def remove_edge(self, edge):
        self._out[edge.get_source()].pop(edge)
        self._in[edge.get_destination()].pop(edge)

    def get_edge(self, source, destination):
        lista_veza = self._out[source]
        for edge in lista_veza:
            if edge.get_destination == destination:
                return edge
        return None
