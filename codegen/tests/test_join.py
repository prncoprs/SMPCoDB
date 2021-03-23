import unittest

from codegen.table.column import Column, TypeEnum
from codegen.table.table import Table
from codegen.table.free_connex_table import FreeConnexTable


class JoinTest(unittest.TestCase):
    """
    Test join on tables
    """

    def setUp(self):
        self.a_table = Table(table_name="a",
                             columns=[Column(name="name", column_type=TypeEnum.string),
                                      Column(name="id", column_type=TypeEnum.int)])
        self.b_table = Table(table_name="b", columns=[Column(name="name", column_type=TypeEnum.string),
                                                      Column(name="id", column_type=TypeEnum.int)])

        self.c_table = Table(table_name="c", columns=[
            Column(name="name", column_type=TypeEnum.string),
            Column(name="id", column_type=TypeEnum.int),
            Column(name="address", column_type=TypeEnum.string)
        ])

    def test_simple_join(self):
        self.a_table.join(self.b_table, "id", "id")
        self.assertEqual(len(self.a_table.children), 1)
        column_names = self.a_table.column_names
        self.assertEqual(len(column_names), 3)

    def test_simple_join_2(self):
        self.b_table.join(self.c_table, "id", "id")
        column_names = self.b_table.column_names
        self.assertEqual(len(column_names), 4)
        expected_names = ["c.name", "b.id", "c.address", "b.name"]
        for c in column_names:
            self.assertTrue(c.name_with_table in expected_names)

    def test_simple_join_3(self):
        self.a_table.join(self.b_table, "id", "id")
        self.b_table.join(self.c_table, "id", "id")
        column_names = self.a_table.column_names
        self.assertEqual(len(column_names), 5)
        expected_names = ["a.name", "a.id", "b.name", "c.name", "c.address"]
        for c in column_names:
            self.assertTrue(c.name_with_table in expected_names)

    def test_get_aggregate_columns(self):
        table_a = Table(table_name="A", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="b", column_type=TypeEnum.int),
            Column(name="c", column_type=TypeEnum.int)
        ])

        table_b = Table(table_name="B", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="e", column_type=TypeEnum.int)
        ])

        table_c = Table(table_name="C", columns=[
            Column(name="e", column_type=TypeEnum.int),
            Column(name="f", column_type=TypeEnum.int)
        ])

        table_a.join(table_b, "a", "a")
        table_c.join(table_a, "e", "e")

        column_names = table_a.column_names
        self.assertEqual(len(column_names), 4)

        agg = table_b.get_aggregate_columns()
        self.assertEqual(2, len(agg))
        self.assertEqual(agg[0].name, "a")
        self.assertEqual(agg[1].name, "e")

        agg = table_a.get_aggregate_columns()
        self.assertEqual(1, len(agg))
        self.assertEqual(agg[0].name, "e")

        agg = table_c.get_aggregate_columns()
        self.assertEqual(0, len(agg))

    def test_get_aggregate_columns2(self):
        table_a = Table(table_name="A", columns=[
            Column(name="aa", column_type=TypeEnum.int),
            Column(name="b", column_type=TypeEnum.int),
            Column(name="c", column_type=TypeEnum.int)
        ])

        table_b = Table(table_name="B", columns=[
            Column(name="ba", column_type=TypeEnum.int),
            Column(name="e", column_type=TypeEnum.int)
        ])

        table_a.join(to_table=table_b, from_table_key="aa", to_table_key="ba")

        column_names = table_a.column_names
        self.assertEqual(len(column_names), 4)

        agg = table_b.get_aggregate_columns()
        self.assertEqual(1, len(agg))
        self.assertEqual(agg[0].name, "ba")

    def test_get_aggregate_columns3(self):
        table_a = Table(table_name="A", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="b", column_type=TypeEnum.int),
        ])

        table_b = Table(table_name="B", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="c", column_type=TypeEnum.int)
        ])

        table_c = Table(table_name="C", columns=[
            Column(name="b", column_type=TypeEnum.int),
            Column(name="d", column_type=TypeEnum.int)
        ])

        table_a.join(table_b, 'a', 'a')
        table_a.join(table_c, 'b', 'b')

        agg = table_b.get_aggregate_columns()
        self.assertEqual(1, len(agg))
        self.assertEqual(agg[0].name, 'a')

        agg = table_c.get_aggregate_columns()
        self.assertEqual(1, len(agg))
        self.assertEqual(agg[0].name, "b")


class FreeConnexJoin(unittest.TestCase):

    def setUp(self) -> None:
        self.table_1 = FreeConnexTable(table_name="1", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="b", column_type=TypeEnum.int),
        ])

        self.table_2 = FreeConnexTable(table_name="2", columns=[
            Column(name="a", column_type=TypeEnum.int),
            Column(name="c", column_type=TypeEnum.int)
        ])

        self.table_3 = FreeConnexTable(table_name="3", columns=[
            Column(name="b", column_type=TypeEnum.int),
            Column(name="d", column_type=TypeEnum.int)
        ])

        self.table_4 = FreeConnexTable(table_name="4", columns=[
            Column(name="d", column_type=TypeEnum.int),
            Column(name="f", column_type=TypeEnum.int),
            Column(name="g", column_type=TypeEnum.int),
        ])

        self.table_5 = FreeConnexTable(table_name="5", columns=[
            Column(name="b", column_type=TypeEnum.int),
            Column(name="e", column_type=TypeEnum.int)
        ])

    def test_is_free_connex_join(self):
        """
        See exaample/join_tree.drawio tree A
        :return:
        """

        self.table_1.join(self.table_2, "a", "a")
        self.table_1.join(self.table_3, "b", "b")
        self.table_3.join(self.table_4, "d", "d")
        self.table_3.join(self.table_5, "b", "b")

        output_attrs = ["b", "d", "e", "f"]
        non_output_attrs = ["a", "c", "g"]

        height_of_tree = self.table_1.get_height()

        table, height = self.table_1.get_highest_with_attr("a", height_of_tree)
        self.assertEqual(table, self.table_1)
        self.assertEqual(height, 2)

        table, height = self.table_1.get_highest_with_attr("d", height_of_tree)
        self.assertEqual(table, self.table_3)
        self.assertEqual(height, 1)

        table, height = self.table_1.get_highest_with_attr("c", height_of_tree)
        self.assertEqual(table, self.table_2)
        self.assertEqual(height, 1)

        is_free_connex, output_tables = self.table_1.is_free_connex(output_attrs=output_attrs,
                                                                    non_output_attrs=non_output_attrs,
                                                                    height=height_of_tree)
        self.assertFalse(is_free_connex)
        self.assertEqual(output_tables[0], self.table_3)

    def test_is_free_connex_join2(self):
        """
        See exaample/join_tree.drawio tree B
        :return:
        """

        self.table_5.join(self.table_3, "b", "b")
        self.table_3.join(self.table_1, "b", "b")
        self.table_1.join(self.table_2, "a", "a")
        self.table_3.join(self.table_4, "d", "d")

        output_attrs = ["b", "d", "e", "f"]
        non_output_attrs = ["a", "c", "g"]

        height_of_tree = self.table_5.get_height()

        table, height = self.table_5.get_highest_with_attr("a", height_of_tree)
        self.assertEqual(table, self.table_1)
        self.assertEqual(height, 1)

        table, height = self.table_5.get_highest_with_attr("d", height_of_tree)
        self.assertEqual(table, self.table_3)
        self.assertEqual(height, 2)

        table, height = self.table_5.get_highest_with_attr("c", height_of_tree)
        self.assertEqual(table, self.table_2)
        self.assertEqual(height, 0)

        is_free_connex, _ = self.table_5.is_free_connex(output_attrs=output_attrs,
                                                        non_output_attrs=non_output_attrs,
                                                        height=height_of_tree)
        self.assertTrue(is_free_connex)

    def test_is_free_connex_join3(self):
        """
        See exaample/join_tree.drawio tree A
        :return:
        """

        self.table_1.join(self.table_2, "a", "a")
        self.table_1.join(self.table_3, "b", "b")
        self.table_3.join(self.table_4, "d", "d")
        self.table_3.join(self.table_5, "b", "b")

        output_attrs = ["b", "d", "e", "f"]
        non_output_attrs = ["a", "c", "g", "sum"]

        height_of_tree = self.table_1.get_height()

        is_free_connex, output_tables = self.table_1.is_free_connex(output_attrs=output_attrs,
                                                                    non_output_attrs=non_output_attrs,
                                                                    height=height_of_tree)
        self.assertFalse(is_free_connex)
        self.assertEqual(output_tables[0], self.table_3)

    def test_swap(self):
        self.table_1.join(self.table_2, "a", "a")
        self.table_1.join(self.table_3, "b", "b")
        self.table_3.join(self.table_4, "d", "d")
        self.table_3.join(self.table_5, "b", "b")

        # self.table_3.swap()
        # self.assertEqual(self.table_5.parent, None)
        # self.assertEqual(self.table_5.children, [self.table_3])
