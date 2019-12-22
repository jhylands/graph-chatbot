class NoIndexLinkError(Exception):
    def __init__(self, message):
        super(NoIndexLinkError).__init__(message)

class Node:
    def __init__(self, node_list, name="", data=None):
        self.outgoing = []
        self.incoming = []
        self.edges = []
        self.name = name
        self.data = data
        self.add_global_link(node_list)

    def add_global_link(self, node_list):
        self.global_ref = node_list
        try:
            self.index = node_list.index(self)
        except ValueError:
            node_list.append(self)
            self.index = node_list.index(self)

    def get_index(self):
        if self.global_ref:
            return self.index
        raise NoIndexLinkError(self.name)

    def outgoing(self):
        return self.outgoing

    def incoming(self):
        return self.incoming

    def __repr__(self):
        return "{}:{}".format(self.get_index(), self.name)

class Edge:
    def __init__(self, start, style, end):
        self.start = start
        start.outgoing.append(self)
        self.style = style
        style.edges.append(self)
        self.end = end
        end.incoming.append(self)

    def remove(self):
        # remove self from start
        self.start.outgoing.remove(self)
        # remove self from style
        self.style.edges.remove(self)
        # remove self from end
        self.end.incoming.remove(self)

    def __repr__(self):
        return "({})-[{}]->({})".format(self.start , self.style, self.end)
