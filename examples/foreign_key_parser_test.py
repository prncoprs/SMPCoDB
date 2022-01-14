import sys
sys.path.append(".")

import sqlparse
from codegen.codegen import Parser
from codegen.table.free_connex_table import FreeConnexTable
from codegen.foreign_key_codegen import ForeignKeyParser
import json

sql = """
select
   l_orderkey,
   sum(l_extendedprice * (1 - l_discount)) as revenue,
   o_orderdate,
   o_shippriority
from
   CUSTOMER,
   ORDERS,
   LINEITEM
where
   c_mktsegment = 'AUTOMOBILE'
   and c_custkey = o_custkey
   and l_orderkey = o_orderkey
   and o_orderdate < date '1995-03-13'
   and l_shipdate > date '1995-03-13'
group by
   l_orderkey,
   o_orderdate,
   o_shippriority
order by
   revenue desc,
   o_orderdate
limit
   10;

"""

sql2 = """
select
   c_custkey,
   c_name,
   sum(l_extendedprice * (1 - l_discount)) as revenue,
   c_nationkey
 from
   CUSTOMER,
   ORDERS,
   LINEITEM
where
   c_custkey = o_custkey
   and l_orderkey = o_orderkey
   and o_orderdate >= date '1993-08-01'
   and o_orderdate < date '1993-08-01' + interval '3' month
   and l_returnflag = 'R'
 group by
   c_custkey,
   c_name
order by
   revenue desc
limit
   20;

"""

sql3 = """
select
    n_name,
    sum(l_extendedprice * (1 - l_discount)) as revenue
from
    CUSTOMER,
    ORDERS,
    LINEITEM,
    SUPPLIER,
    NATION,
    REGION
where
     o_custkey=c_custkey
    and l_orderkey = o_orderkey
    and s_suppkey= l_suppkey
    and r_name = 'MIDDLE EAST'
    and o_orderdate >= date '1994-01-01'
    and o_orderdate < date '1994-01-01' + interval '1' year
group by
    n_name
order by
    revenue desc;
"""

with open("examples/table_config.json", 'r') as f:
    tables = [FreeConnexTable.load_from_json(t) for t in json.load(f)]
    # parser = Parser(sql=sql3, tables=tables, annotation_name="")
    fk_parser = ForeignKeyParser(sql=sql3, tables=tables)

    fk_parser.parse()

    print(fk_parser)
    print(fk_parser.parse().is_foreign_key_acyclic())
    print()

    # parser.root.print_graph()

    # o = parser.root_table.to_json(parser.get_output_attributes())
    # print(o)
    # parser.to_file("examples/test.cpp")
