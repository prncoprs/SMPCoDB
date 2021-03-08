import sqlparse
from codegen.codegen import Parser
from codegen.table.column import TypeEnum
from codegen.table.table import Table, Column
import json

sql = """
select
   n_name
from
   CUSTOMER,
   ORDERS,
   LINEITEM,
   SUPPLIER
where
   c_custkey = o_custkey
   and l_orderkey = o_orderkey
   and l_suppkey = s_suppkey 
   and c_nationkey = s_nationkey
"""

# CUSTOMER_TABLE = Table(table_name="CUSTOMER",
#                        columns=[
#                            Column(name="c_custkey", column_type=TypeEnum.int),
#                            Column(name="c_nationkey", column_type=TypeEnum.int)
#                        ])
# ORDERS_TABLE = Table(table_name="ORDERS",
#                      columns=[
#                          Column(name="o_custkey", column_type=TypeEnum.int),
#                          Column(name="o_orderkey", column_type=TypeEnum.int),
#                          Column(name="o_shippriority", column_type=TypeEnum.int)
#                      ])
# LINEITEM_TABLE = Table(table_name="LINEITEM",
#                        columns=[
#                            Column(name="l_orderkey", column_type=TypeEnum.int)
#                        ])
#
# SUPPLIER_TABLE = Table(table_name="SUPPLIER",
#                        columns=[
#                            Column(name="s_suppkey", column_type=TypeEnum.int),
#                            Column(name="s_nationkey", column_type=TypeEnum.int)
#                        ])
#
# NATION_TABLE = Table(table_name="NATION",
#                        columns=[
#                            Column(name="s_suppkey", column_type=TypeEnum.int),
#                            Column(name="s_nationkey", column_type=TypeEnum.int)
#                        ])

with open("examples/table_config.json", 'r') as f:
    tables = [Table.load_from_json(t) for t in json.load(f)]
    parser = Parser(sql=sql, tables=tables)
    parser.parse().to_file("examples/test.cpp")
