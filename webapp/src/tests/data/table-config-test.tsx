export const SIMPLE_CONFIGS: any[] = [
  {
    annotations: [],
    columns: [
      {
        column_type: "INT",
        name: "n_nationkey",
      },
      {
        column_type: "STRING",
        name: "n_name",
      },
      {
        column_type: "INT",
        name: "n_regionkey",
      },
      {
        column_type: "STRING",
        name: "n_comment",
      },
    ],
    data_paths: [
      "/Users/qiweili/Desktop/Project_1/SECYAN-GEN/data_dir/nation.tbl",
    ],
    data_sizes: [25],
    table_name: "nation",
  },
  {
    annotations: [],
    columns: [
      {
        column_type: "INT",
        name: "r_regionkey",
      },
      {
        column_type: "STRING",
        name: "r_name",
      },
      {
        column_type: "STRING",
        name: "r_comment",
      },
    ],
    data_paths: [
      "/Users/qiweili/Desktop/Project_1/SECYAN-GEN/data_dir/region.tbl",
    ],
    data_sizes: [10],
    table_name: "region",
  },
  {
    annotations: [],
    columns: [
      {
        column_type: "INT",
        name: "p_partkey",
      },
      {
        column_type: "STRING",
        name: "p_name",
      },
      {
        column_type: "STRING",
        name: "p_mfgr",
      },
      {
        column_type: "STRING",
        name: "p_brand",
      },
      {
        column_type: "STRING",
        name: "p_type",
      },
      {
        column_type: "INT",
        name: "p_size",
      },
      {
        column_type: "STRING",
        name: "p_container",
      },
      {
        column_type: "DECIMAL",
        name: "p_retailprice",
      },
      {
        column_type: "STRING",
        name: "p_comment",
      },
    ],
    data_paths: [
      "/Users/qiweili/Desktop/Project_1/SECYAN-GEN/data_dir/part.tbl",
    ],
    data_sizes: [40000],
    table_name: "part",
  },
  {
    annotations: [],
    columns: [
      {
        column_type: "INT",
        name: "s_suppkey",
      },
      {
        column_type: "STRING",
        name: "s_name",
      },
      {
        column_type: "STRING",
        name: "s_address",
      },
      {
        column_type: "INT",
        name: "s_nationkey",
      },
      {
        column_type: "STRING",
        name: "s_phone",
      },
      {
        column_type: "DECIMAL",
        name: "s_acctbal",
      },
      {
        column_type: "STRING",
        name: "s_comment",
      },
    ],
    data_paths: [
      "/Users/qiweili/Desktop/Project_1/SECYAN-GEN/data_dir/supplier.tbl",
    ],
    data_sizes: [2000],
    table_name: "supplier",
  },
  {
    annotations: [],
    columns: [
      {
        column_type: "INT",
        name: "ps_partkey",
      },
      {
        column_type: "INT",
        name: "ps_suppkey",
      },
      {
        column_type: "INT",
        name: "ps_availqty",
      },
      {
        column_type: "DECIMAL",
        name: "ps_supplycost",
      },
      {
        column_type: "STRING",
        name: "ps_comment",
      },
    ],
    data_paths: [
      "/Users/qiweili/Desktop/Project_1/SECYAN-GEN/data_dir/partsupp.tbl",
    ],
    data_sizes: [160000],
    table_name: "partsupp",
  },
  {
    annotations: ["CAST(c_mktsegment = 'AUTOMOBILE' AS int)"],
    columns: [
      {
        column_type: "INT",
        name: "c_custkey",
      },
      {
        column_type: "STRING",
        name: "c_name",
      },
      {
        column_type: "STRING",
        name: "c_address",
      },
      {
        column_type: "INT",
        name: "c_nationkey",
      },
      {
        column_type: "STRING",
        name: "c_phone",
      },
      {
        column_type: "DECIMAL",
        name: "c_acctbal",
      },
      {
        column_type: "STRING",
        name: "c_mktsegment",
      },
      {
        column_type: "STRING",
        name: "c_comment",
      },
    ],
    data_paths: [
      "/Users/qiweili/Desktop/Project_1/SECYAN-GEN/data_dir/customer.tbl",
    ],
    data_sizes: [30000],
    table_name: "customer",
  },
  {
    annotations: ["CAST(o_orderdate < date '1995-03-13' AS int)"],
    columns: [
      {
        column_type: "INT",
        name: "o_orderkey",
      },
      {
        column_type: "INT",
        name: "o_custkey",
      },
      {
        column_type: "STRING",
        name: "o_orderstatus",
      },
      {
        column_type: "DECIMAL",
        name: "o_totalprice",
      },
      {
        column_type: "DATE",
        name: "o_orderdate",
      },
      {
        column_type: "STRING",
        name: "o_orderpriority",
      },
      {
        column_type: "STRING",
        name: "o_clerk",
      },
      {
        column_type: "INT",
        name: "o_shippriority",
      },
      {
        column_type: "STRING",
        name: "o_comment",
      },
    ],
    data_paths: [
      "/Users/qiweili/Desktop/Project_1/SECYAN-GEN/data_dir/orders.tbl",
    ],
    data_sizes: [300000],
    table_name: "orders",
  },
  {
    annotations: [
      "CAST(l_shipdate > date '1995-03-13' AS int)*CAST(l_extendedprice * (1 - l_discount) AS int)",
    ],
    columns: [
      {
        column_type: "INT",
        name: "l_orderkey",
      },
      {
        column_type: "INT",
        name: "l_partkey",
      },
      {
        column_type: "INT",
        name: "l_suppkey",
      },
      {
        column_type: "INT",
        name: "l_linenumber",
      },
      {
        column_type: "DECIMAL",
        name: "l_quantity",
      },
      {
        column_type: "DECIMAL",
        name: "l_extendedprice",
      },
      {
        column_type: "DECIMAL",
        name: "l_discount",
      },
      {
        column_type: "DECIMAL",
        name: "l_tax",
      },
      {
        column_type: "STRING",
        name: "l_returnflag",
      },
      {
        column_type: "STRING",
        name: "l_linestatus",
      },
      {
        column_type: "DATE",
        name: "l_shipdate",
      },
      {
        column_type: "DATE",
        name: "l_commitdate",
      },
      {
        column_type: "DATE",
        name: "l_receiptdate",
      },
      {
        column_type: "STRING",
        name: "l_shipinstruct",
      },
      {
        column_type: "STRING",
        name: "l_shipmode",
      },
      {
        column_type: "STRING",
        name: "l_comment",
      },
    ],
    data_paths: [
      "/Users/qiweili/Desktop/Project_1/SECYAN-GEN/data_dir/lineitem.tbl",
    ],
    data_sizes: [600572],
    table_name: "lineitem",
  },
];
