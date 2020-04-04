from bst.node import Node

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Tree:
    root = None
    nodes = {}

    @staticmethod
    def build_from_data(data):
        tree = Tree()
        tree.nodes = {index: Node(v[0], v[1], v[2]) for index, v in data.items()}

        # tworzenie połączeń, nadawanie keyów
        for index, node in tree.nodes.items():
            node.key = index
            if node.left is not None:
                node.left = tree.nodes[node.left]
                node.left.parent = node

            if node.right is not None:
                node.right = tree.nodes[node.right]
                node.right.parent = node

        return tree

    def __str__(self):
        if len(self.nodes) == 0:
            return ''
        current = self.nodes[0]
        visited_nodes = []
        depth = 0
        output = []

        def reverse_in_order(node, level=0, side=None):
            if node:
                #prawy
                reverse_in_order(node.right, level +1, 'right')
                visited_nodes.append(node.key)

                # printowanie
                string = ''
                if side:
                    arc = '┌─' if side == 'right' else '└─'
                    string = '  ' * (level - 1) + arc
                else:
                    string = ' ' * 2 *level
                string += '{}{}{} [{}{}{}]'.format(
                    bcolors.OKGREEN, node.value, bcolors.ENDC,
                    bcolors.OKBLUE, node.key, bcolors.ENDC
                )
                output.append(string)
                # lewy
                reverse_in_order(node.left, level + 1, 'left')

        reverse_in_order(self.nodes[0])

        # napraw pionowe linie w schemacie
        def fix_schema(schema, char):
            matrix = [0] * max(map(len, schema))
            for line_index, line in enumerate(schema):
                line = list(line)
                for char_index, flag in enumerate(matrix):
                    if char_index < len(line):
                        if flag:
                            if line[char_index] == ' ':
                                line[char_index] = '|'
                            else:
                                matrix[char_index] = 0  # wyłącz wstawianie pionowych linii
                        else:
                            if line[char_index] == char:
                                matrix[char_index] = 1

                schema[line_index] = ''.join(line)
            return schema

        output = fix_schema(output, '┌')
        output = fix_schema(output[::-1], '└')[::-1]
        return '\n'.join(output)

    def add(self, value):
        node = Node(value)
        if len(self.nodes):
            current = self.nodes[0]  # root
            # przeszukaj drzewo w poszukiwaniu ścieżki do ostatniego pasującego liścia
            while current.value > value and current.left is not None or current.value <= value and current.right is not None:
                if current.value > value:
                    if current.left:
                        current = current.left
                else:
                    if current.right:
                        current = current.right
            # przy ostatnim pasującym liściu zdecyduj która strona
            if current.value > value:
                current.left = node
                node.parent = current
                node.key = node.parent.key * 2 + 1
            else:
                current.right = node
                node.parent = current
                node.key = node.parent.key * 2 + 2

        else:
            node.key = 0
            self.nodes[0] = node
        self.nodes[node.key] = node

    @staticmethod
    def build_random(n, min=0, max=64):
        import random
        tree = Tree()
        for i in range(n):
            tree.add(random.randint(min, max))
        return tree

    def find_min(self):
        current = self.nodes[0]
        path = []
        while current.left:
            path.append(current.value)
            current = current.left
        return {
            'path': path,
            'min': current.value
        }

    def find_max(self):
        current = self.nodes[0]
        path = []
        while current.right:
            path.append(current.value)
            current = current.right
        return {
            'path': path,
            'min': current.value
        }

    def get_successor(self, node):
        # wezel posiada prawego syna
        if node.right:
            current = node.right
            while current.left:
                current = current.left
            return current
        else:
            current = node
            while current.get_parent_side() != 'left':
                if current.parent:
                    current = current.parent
                else:
                    return None
            return current.parent

    def delete_node(self, key):
        if key not in self.nodes:
            return False

        node = self.nodes[key]
        # bezdzietny węzeł
        if not node.left and not node.right:
            print('bezdzietny')
            node_id = id(node)
            if id(node.parent.left) == node_id:
                node.parent.left = None
            else:
                node.parent.right = None
                del self.nodes[key]
                print(self.nodes)
        elif bool(node.left) ^ bool(node.right):  # xor
            print('jednodziecko')
            parent = node.parent
            if parent.left == node:
                if node.right:
                    parent.left = node.right
                else:
                    parent.left = node.left
            else:
                if node.right:
                    parent.right = node.right
                else:
                    parent.right = node.left
            del self.nodes[key]
        else: # ma wszystkie dzieci
            print('oba dzieciory')
            successor = self.get_successor(node)
            print(successor)
            node.value = successor.value
            node.key = successor.key
            self.delete_node(successor)