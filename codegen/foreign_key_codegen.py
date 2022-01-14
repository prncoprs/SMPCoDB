from typing import Tuple, List, Optional

from sqlparse.sql import Where, Comparison

from codegen.codegen import Parser
from codegen.node.cpp_nodes.WhereNode import FreeConnexWhereNode
from codegen.table import Table, FreeConnexTable

import sqlparse
import sql_metadata
import networkx as nx


class ForeignKeyParser(Parser):
    """
    Construct a Foreign Key SQL Query parser.
    This will try to construct a free connex join tree instead of the regular join tree
    which the base class "Parser" will generate by default.
    """

    def __init__(self, sql: str, tables: List[Table]):
        super(ForeignKeyParser, self).__init__(sql, tables, "")
        self.sql = sqlparse.format(self.sql, strip_comments=True, reindent=True, identifier_case="lower")
        self.DG = nx.DiGraph()
        self.SDG = nx.DiGraph()
        self.load_tpch_schema()

    def load_tpch_schema(self):
        self.DG.add_nodes_from(["lineitem", "partsupp", "orders", "part", "supplier", "customer", "nation", "region"])
        self.DG.add_edges_from(
            [("lineitem", "partsupp"), ("lineitem", "orders"), ("partsupp", "part"), ("partsupp", "supplier"),
             ("orders", "customer"), ("supplier", "nation"), ("customer", "nation"), ("nation", "region")])

    def is_foreign_key_acyclic(self) -> bool:
        query_tables = self.get_query_tables()
        self.SDG = self.DG.subgraph(query_tables)
        print(query_tables)
        print(self.SDG)
        return nx.is_directed_acyclic_graph(self.SDG)

    def get_query_tables(self) -> List[str]:
        return sql_metadata.get_query_tables(self.sql)



    # def __parse_where__(self, token: Where):
    #     last = self.root.get_last_node()
    #     comparison_list: List[Comparison] = []
    #     for t in token.tokens:
    #         if type(t) == Comparison:
    #             comparison_list.append(t)
    #     last.next = FreeConnexWhereNode(comparison_list=comparison_list, tables=self.tables,
    #                                     is_free_connex_table=self.is_free_connex)
    #     last.next.prev = last


