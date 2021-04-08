from typing import List, Optional, Tuple
import sqlparse
from sqlparse.sql import Comment, Identifier, Statement, Where, Token, IdentifierList, Comparison
from .node import SelectNode, GroupByNode, FromNode, JoinNode, OrderByNode, WhereNode, BaseNode
from .table import Table, FreeConnexTable
from jinja2 import Template
from . import templates

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources


class Parser:
    """
    This a parser class. This parser will parse the sql statement and generate a sql syntax tree.
    The syntax tree contains two different types object.
    1. SQL Table. This parse need these tables' data to perform some operations such as join.
    2. SQL Syntax tree node. This object will do the operation based on the data it has.

    Usage:

    ```python
    parser = Parser(sql=sql, tables=tables)
    parser.parse()

    # Generate string output
    parser.to_output()
    ```
    """

    def __init__(self, sql: str, tables: List[Table]):
        self.sql = sql
        self.tokens: List[Token] = sqlparse.parse(sql)[0].tokens
        self.root = BaseNode(tables=[])
        self.tables: List[Table] = tables

    @property
    def root_table(self) -> Optional[Table]:
        joined = [t for t in self.tables if t.used_in_join]

        if len(joined) > 0:
            return joined[0].get_root()

        joined = [t for t in self.tables if t.used]

        return joined[0].get_root()

    def get_output_attributes(self) -> List[str]:
        """
        Get a list of output attributes. This will be useful for telling if a join tree is a free connex join tree.
        :return: List of output attributes
        """
        node = self.root
        while node:
            if type(node) == SelectNode:
                return [str(i) for i in node.identifier_list]
            else:
                node = node.next
        return []

    def get_non_output_attributes(self, output_attrs: List[str]) -> List[str]:
        """
        Get list of non output attributes. This will be useful for telling if a join tree is a free connex join tree.
        :param output_attrs: List of non output attributes
        :return:
        """
        attrs = []
        tables = [t for t in self.tables if t.used]
        for table in tables:
            for col in table.original_column_names:
                for a in output_attrs:
                    if not col.equals_name(a):
                        if col.name not in attrs:
                            attrs.append(col.name)

        return attrs

    def parse(self):
        for token in self.tokens:
            if not token.is_whitespace:
                if type(token) == Token:
                    if token.normalized == "SELECT":
                        self.__parse_select__()
                    elif token.normalized == "GROUP BY":
                        self.__parse_group_by__()
                    elif token.normalized == "FROM":
                        self.__parse_from__()
                    elif token.normalized == "ORDER BY":
                        self.__parse_order_by__()
                elif type(token) == Where:
                    token: Where
                    self.__parse_where__(token)
                elif type(token) == Identifier:
                    token: Identifier
                    self.__parse_identifier__(token)
                elif type(token) == IdentifierList:
                    token: IdentifierList
                    self.__parse_identifier_list__(token)

        self.__do_merge__()
        self.check_valid()
        return self

    def __do_merge__(self):
        """
        Merge data.

        This function will perform merge operation on the SQL Syntax tree.
        :return:
        """
        cur = self.root
        while cur:
            cur.merge()
            cur = cur.next

    def check_valid(self, raise_error=True) -> bool:
        n = 0
        roots = []
        for table in self.tables:
            if table.parent is None and table.used_in_join:
                n += 1
                roots.append(table)

        if n > 1:
            if raise_error:
                raise RuntimeError(
                    f"Join tree has {n} root. Check your join statement. Roots: {[r.variable_table_name for r in roots]}")
            else:
                return False

        return True

    def __to_code__(self) -> List[str]:
        """
        Generate a list of code
        :return: A list of code
        """
        code = []
        cur = self.root
        while cur:
            c = cur.to_code(root=self.root_table)
            if c:
                code += c
            cur = cur.next

        return code

    def to_file(self, file_name: str):
        """
        Generate code and save it to the file with file_name
        :param file_name:
        :return:
        """
        template = Template(pkg_resources.read_text(templates, "template.j2"))
        with open(file_name, 'w') as f:
            lines = self.__to_code__()
            generated = template.render(function_lines=lines)
            f.write(generated)

    def to_output(self, function_name="run_Demo") -> str:
        """
        Generate code and return
        :return: generated code
        """
        template = Template(pkg_resources.read_text(templates, "template.j2"))
        lines = self.__to_code__()
        generated = template.render(function_lines=lines, function_name=function_name)
        return generated

    def __parse_from__(self):
        last = self.root.get_last_node()
        last.next = FromNode(tables=self.tables)
        last.next.prev = last

    def __parse_where__(self, token: Where):
        last = self.root.get_last_node()
        comparison_list: List[Comparison] = []
        for t in token.tokens:
            if type(t) == Comparison:
                comparison_list.append(t)
        last.next = WhereNode(comparison_list=comparison_list, tables=self.tables)
        last.next.prev = last

    def __parse_group_by__(self):
        last = self.root.get_last_node()
        last.next = GroupByNode(tables=self.tables)
        last.next.prev = last

    def __parse_order_by__(self):
        last = self.root.get_last_node()
        last.next = OrderByNode(tables=self.tables)
        last.next.prev = last

    def __parse_select__(self):
        last = self.root.get_last_node()
        last.next = SelectNode(tables=self.tables)
        last.next.prev = last

    def __parse_identifier__(self, token: Identifier):
        last = self.root.get_last_node()
        last.set_identifier_list([token])

    def __parse_identifier_list__(self, token: IdentifierList):
        last = self.root.get_last_node()
        tokens = [t for t in token.get_identifiers()]
        last.set_identifier_list(tokens)
