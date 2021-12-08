from enum import Enum, auto
from anytree import Node

from IO.file_IO import TokenType
from parser_sup.non_terminal import first_dictionary, follow_dictionary, NonTerminal


#
# class NonTerminal:
#     def __init__(self, name, first, follow) -> None:
#         self.name = name
#         self.first = first
#         self.follow = follow

class Terminal:
    def __init__(self, lexeme) -> None:
        self.lexeme = lexeme


class Link:
    def __init__(self, parameter, father, child) -> None:
        self.parameter = parameter
        self.father = father
        self.child = child

    def is_terminal(self):
        if isinstance(self.parameter, Terminal):
            return True
        return False


# class Node:
#     def __init__(self, father_NT, out_links, number) -> None:
#         self.father_NT = father_NT
#         self.out_links = out_links
#         self.number = number

class ErrorType(Enum):
    NOT_IN_FOLLOW = auto()
    IN_FOLLOW = auto()
    TERMINALS_NOT_MATCH = auto()


class Parser:
    def __init__(self, scanner) -> None:
        # initialize all terminal, nonterminals, nodes, and links
        # keep nodes in a dict
        self.nodes = {}
        self.current_node = 0
        self.scanner = scanner
        self.lookahead = scanner.get_next_token()
        pass

    def move(self, token):
        node = self.nodes[self.current_node]
        for link in node.out_links:
            if link.is_terminal():
                pass
            else:
                pass

    def handle_error(self, error_type):
        pass

    def program(self):
        children = []
        parent = Node(NonTerminal.PROGRAM.value)
        while self.current_node != 2:
            if self.current_node == 0:
                if self._is_nt_edge_valid(NonTerminal.DECLARATION_LIST):
                    self.current_node = 3
                    children.append(self.declaration_list())
                    self.current_node = 1
                if self._is_in_follow_set(NonTerminal.PROGRAM):
                    self._handle_missing_non_term(NonTerminal.PROGRAM.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.program()
            elif self.current_node == 1:
                if self.lookahead[1] is TokenType.END:
                    self._add_leaf_to_tree(children, parent, 2)
                else:
                    self._handle_missing_token("$", 2)
        return self._make_tree(parent, children)

    def declaration_list(self):
        children = []
        parent = Node(NonTerminal.DECLARATION_LIST.value)
        while self.current_node != 5:
            if self.current_node == 3:
                if self._is_nt_edge_valid(NonTerminal.DECLARATION):
                    self.current_node = 6
                    children.append(self.declaration())
                    self.current_node = 4
                if self._is_epsilon_move_valid(NonTerminal.DECLARATION_LIST):
                    return None
                if self._is_in_follow_set(NonTerminal.DECLARATION_LIST):
                    self._handle_missing_non_term(NonTerminal.DECLARATION_LIST.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.declaration_list()
            elif self.current_node == 4:
                self.current_node = 3
                children.append(self.declaration_list())
                self.current_node = 5
        return self._make_tree(parent, children)

    def declaration(self):
        parent = Node(NonTerminal.DECLARATION.value)
        children = []
        while self.current_node != 8:
            if self.current_node == 6:
                if self._is_nt_edge_valid(NonTerminal.DECLARATION_INITIAL):
                    self.current_node = 9
                    children.append(self.declaration_initial())
                    self.current_node = 7
                elif self._is_in_follow_set(NonTerminal.DECLARATION):
                    self._handle_missing_non_term(NonTerminal.DECLARATION.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.declaration()
            if self.current_node == 7:
                self.current_node = 12
                children.append(self.declaration_prime())
                self.current_node = 9
        return self._make_tree(parent, children)

    def declaration_initial(self):
        parent = Node(NonTerminal.DECLARATION_INITIAL.value)
        children = []
        while self.lookahead != 11:
            if self.current_node == 9:
                if self._is_nt_edge_valid(NonTerminal.TYPE_SPECIFIER):
                    self.current_node = 25
                    children.append(self.type_specifier())
                    self.current_node = 10
                elif self._is_in_follow_set(NonTerminal.DECLARATION):
                    self._handle_missing_non_term(NonTerminal.DECLARATION_INITIAL.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.declaration_initial()
            if self.current_node == 10:
                self._move_terminal_edge(children, parent, TokenType.ID, 11)
        return self._make_tree(parent, children)

    def declaration_prime(self):
        parent = Node(NonTerminal.DECLARATION_PRIME.value)
        children = []
        while self.current_node != 13:
            if self._is_nt_edge_valid(NonTerminal.FUN_DECLARATION_PRIME):
                self.current_node = 20
                children.append(self.fun_declaration_prime())
                self.current_node = 13
            elif self._is_nt_edge_valid(NonTerminal.VAR_DECLARATION_PRIME):
                self.current_node = 14
                children.append(self.var_declaration_prime())
                self.current_node = 13
            elif self._is_in_follow_set(NonTerminal.DECLARATION_PRIME):
                self._handle_missing_non_term(NonTerminal.DECLARATION_PRIME.value)
                return None
            else:
                self._handle_invalid_input()
                return self.declaration_prime()
        return self._make_tree(parent, children)

    def var_declaration_prime(self):
        parent = Node(NonTerminal.VAR_DECLARATION_PRIME.value)
        children = []
        while self.current_node != 19:
            if self.current_node == 14:
                if self.lookahead[0] == '[':
                    self._add_leaf_to_tree(children, parent, 15)
                elif self.lookahead[0] == ';':
                    self._add_leaf_to_tree(children, parent, 19)
                else:
                    # which edge ??!
                    self._handle_missing_token('[', 15)
            elif self.current_node == 15:
                self._move_terminal_edge(children, parent, TokenType.NUM, 17)
            elif self.current_node == 17:
                self._move_terminal_edge(children, parent, ']', 18)
            elif self.current_node == 18:
                if self.lookahead[0] == ';':
                    self._move_terminal_edge(children, parent, ';', 19)
        return self._make_tree(parent, children)

    def fun_declaration_prime(self):
        parent = Node(NonTerminal.FUN_DECLARATION_PRIME.value)
        children = []
        while self.current_node != 24:
            if self.current_node == 20:
                self._move_terminal_edge(children, parent, '(', 21)
            elif self.current_node == 21:
                self.current_node = 27
                children.append(self.params())
                self.current_node = 22
            elif self.current_node == 22:
                self._move_terminal_edge(children, parent, ')', 23)
            elif self.current_node == 23:
                self.current_node = 42
                children.append(self.compound_stmt())
                self.current_node = 24
        return self._make_tree(parent, children)

    def type_specifier(self):
        parent = Node(NonTerminal.TYPE_SPECIFIER.value)
        children = []
        while self.current_node != 26:
            if self.current_node == 25:
                if self.lookahead[0] == 'int':
                    self._add_leaf_to_tree(children, parent, 26)
                elif self.lookahead[0] == 'void':
                    self._add_leaf_to_tree(children, parent, 26)

    def params(self):
        parent = Node(NonTerminal.PARAMS.value)
        children = []
        while self.current_node != 31:
            if self.current_node == 27:
                if self.lookahead[0] == 'int':
                    self._add_leaf_to_tree(children, parent, 28)
                elif self.lookahead[0] == 'void':
                    self._add_leaf_to_tree(children, parent, 31)
            elif self.current_node == 28:
                self._move_terminal_edge(children, parent, TokenType.ID, 29)
            elif self.current_node == 29:
                self.current_node = 39
                children.append(self.param_prime())
                self.current_node = 30
            elif self.current_node == 30:
                self.current_node = 32
                self.param_list()
                self.current_node = 31
        return self._make_tree(parent, children)

    def param_list(self):
        parent = Node(NonTerminal.PARAM_LIST.value)
        children = []
        while self.current_node != 35:
            if self.current_node == 32:
                if self.lookahead[0] == ',':
                    self._add_leaf_to_tree(children, parent, 33)
                if self._is_epsilon_move_valid(NonTerminal.PARAM_LIST):
                    return None
                if not self._is_in_follow_set(NonTerminal.PARAM_LIST):
                    self._handle_invalid_input()
                    return self.param_list()
            elif self.current_node == 33:
                self.current_node = 36
                children.append(self.param())
                self.current_node = 34
            elif self.current_node == 34:
                self.current_node = 32
                children.append(self.param_list())
                self.current_node = 35
        return self._make_tree(parent, children)

    def param(self):
        parent = Node(NonTerminal.PARAM.value)
        children = []
        while self.current_node != 38:
            if self.current_node == 36:
                if self._is_nt_edge_valid(NonTerminal.DECLARATION_INITIAL):
                    self.current_node = 9
                    children.append(self.declaration_initial())
                    self.current_node = 37
                if self._is_in_follow_set(NonTerminal.DECLARATION_INITIAL):
                    self._handle_missing_non_term(NonTerminal.PARAM.value)
                    return None
                else:
                    self._handle_invalid_input()
                    return self.param()
            elif self.current_node == 37:
                self.current_node = 39
                children.append(self.param_prime())
                self.current_node = 38
        return self._make_tree(parent, children)

    def param_prime(self):
        pass

    def compound_stmt(self):
        pass

    def statement_list(self):
        pass

    def statement(self):
        pass

    def expression_stmt(self):
        pass

    def selection_stmt(self):
        pass

    def else_stmt(self):
        pass

    def iteration_stmt(self):
        pass

    def return_stmt(self):
        pass

    def return_stmt_prime(self):
        pass

    def expression(self):
        pass

    def b(self):
        pass

    def h(self):
        pass

    def simple_expression_zegond(self):
        pass

    def simple_expression_prime(self):
        pass

    def c(self):
        pass

    def relop(self):
        pass

    def additive_expression(self):
        pass

    def additive_expression_prime(self):
        pass

    def additive_expression_zegond(self):
        pass

    def d(self):
        pass

    def addop(self):
        pass

    def term(self):
        pass

    def term_prime(self):
        pass

    def term_zegond(self):
        pass

    def g(self):
        pass

    def factor(self):
        pass

    def var_call_prime(self):
        pass

    def var_prime(self):
        pass

    def factor_prime(self):
        pass

    def factor_zegond(self):
        pass

    def args(self):
        pass

    def arg_list(self):
        pass

    def arg_list_prime(self):
        pass

    def _is_nt_edge_valid(self, non_term):
        """
        Return True if we can move with the 'non_term' edge
        """
        token = self.lookahead[0]
        if token in first_dictionary.get(non_term):
            return True
        if '' in first_dictionary.get(non_term) and token in follow_dictionary.get(token):
            return True
        return False

    @staticmethod
    def _make_tree(parent, children):
        """
        :param parent:  Node
        :param children: list of Nodes
        :return: A tree with 'parent' as root and 'children' as its children
        """
        for child in children:
            if child is not None:
                child.parent = parent
        return parent

    def _is_epsilon_move_valid(self, non_term):
        return self.lookahead[0] in follow_dictionary.get(non_term)

    def _move_lookahead(self):
        self.lookahead = self.scanner.get_next_token()

    def _is_in_follow_set(self, non_term):
        return self.lookahead[0] in follow_dictionary(non_term)

    def _get_leaf_node(self, parent):
        return Node(str((self.lookahead[0], self.lookahead[1])), parent)

    def _handle_missing_non_term(self, non_term: str):
        # TODO: write error
        pass

    def _handle_invalid_input(self):
        # TODO: write invalid input
        self._move_lookahead()

    def _handle_missing_token(self, missed, next_state):
        # TODO: handle missing token
        self.current_node = next_state

    def _add_leaf_to_tree(self, children, parent, next):
        children.append(self._get_leaf_node(parent))
        self._move_lookahead()
        self.current_node = next

    def _move_terminal_edge(self, children, parent, expected, next):
        """
        This method makes move on terminal edges. If there is a mismatch, it will handle the error
        It also adds a leaf node to 'children list"
        ATTENTION: TRY NOT TO USE THIS FUNCTION FOR INITIAL STATES.
        :param children:
        :param parent:
        :param expected: the expected token (on the edge). It can be a string or a token TokenType(like: TokenType.ID)
        :param next: the next state that we should go
        :return:
        """
        if type(expected) == str:
            if self.lookahead[0] == expected:
                self._add_leaf_to_tree(children, parent, next)
            else:
                self._handle_missing_token(expected, next)
        else:
            if self.lookahead[1] is expected:
                self._add_leaf_to_tree(children, parent, next)
            else:
                self._handle_missing_token(expected.value, next)
