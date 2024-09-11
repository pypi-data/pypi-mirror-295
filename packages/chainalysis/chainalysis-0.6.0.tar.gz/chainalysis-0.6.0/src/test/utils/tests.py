import datetime
import unittest

from chainalysis.data_solutions import DataSolutionsClient
from chainalysis.util_functions.exceptions import BadRequest

ds = DataSolutionsClient(
    api_key="",
)


class utils(unittest.TestCase):
    """
    Unit tests for various utility functions in the DataSolutions API.

    This test suite covers stringifying lists and datetime objects,
    as well as validating the correct execution of SQL queries using these utilities.
    """

    def test_list_stringify(self):
        """
        Test that a list of integers is correctly stringified.

        Verifies that a list of integers is converted to a string format
        that can be used in an SQL query.
        """

        blocks = [1, 2]
        stringified_blocks = ds.utils.stringify.lists(
            blocks,
        )
        assert stringified_blocks == "(1, 2)"

    def test_list_stringified_string(self):
        """
        Test that a list of strings (block hashes) is correctly stringified.

        Ensures that a list of block hashes is formatted into a string suitable
        for use in an SQL query.
        """

        block_hashes = [
            "000000000000057d13a731f556c24a1318bcbb4df7d537ef07c8c813c0dc1b37",
            "00000000000005b71bc4c0cf24a6f00e04980c627e9409266983bd37acbe14d3",
        ]

        stringified_block_hashes = (
            ds.utils.stringify.lists(
                block_hashes,
            ),
        )

        assert stringified_block_hashes == (
            "('000000000000057d13a731f556c24a1318bcbb4df7d537ef07c8c813c0dc1b37', '00000000000005b71bc4c0cf24a6f00e04980c627e9409266983bd37acbe14d3')",
        )

    def test_datetime_stringify(self):
        """
        Test that a datetime object is correctly stringified.

        Ensures that a datetime object is formatted into a string suitable
        for use in an SQL query.
        """

        timestamp = "2011-08-25T22:07:41Z"
        dt_object = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

        stringified_timestamp = ds.utils.stringify.datetimes(
            dt_object,
        )
        assert stringified_timestamp == "'2011-08-25T22:07:41Z'"

    def test_incorrect_datetime(self):
        """
        Test that an incorrect type raises the correct exception for datetime stringification.

        Ensures that passing a non-datetime object to the datetime stringification utility
        raises a BadRequest exception with the expected message.
        """

        with self.assertRaises(BadRequest) as context:
            ds.utils.stringify.datetimes(3)
        self.assertEqual(
            str(context.exception),
            "Incorrect type. Supply a datetime.datetime object.",
        )

    def test_incorrect_list(self):
        """
        Test that a list containing multiple types raises an exception.

        Ensures that a list with different data types raises an exception
        with the expected error message.
        """

        list_with_multiple_types = [1, "hello"]

        with self.assertRaises(Exception) as context:
            ds.utils.stringify.lists(list_with_multiple_types)
        self.assertEqual(
            str(context.exception),
            "The list contains multiple types: {<class 'int'>, <class 'str'>}. Enter a list with only numbers, strings, or bools.",
        )

    def test_empty_list(self):
        """
        Test that an empty list raises an exception.

        Ensures that a list with different data types raises an exception
        with the expected error message.
        """

        empty_list = []

        with self.assertRaises(ValueError):
            ds.utils.stringify.lists(empty_list)

    def test_correct_columns(self):
        """
        Test that an column list is correctly converted.

        Ensures that a list with different data types raises an exception
        with the expected error message.
        """

        columns = ["column1", "column2"]

        stringified_columns = ds.utils.stringify.columns(columns)

        assert stringified_columns == "column1, column2"

    def test_incorrect_type_columns(self):
        """
        Test that an empty column list raises an exception.

        Ensures that a list with different data types raises an exception
        with the expected error message.
        """

        columns = [1, 2]

        with self.assertRaises(BadRequest):
            ds.utils.stringify.columns(columns)

    def test_incorrect_list_type(self):
        """
        Test that a non-list input raises the correct exception for list stringification.

        Ensures that passing a non-list object to the list stringification utility
        raises an exception with the expected message.
        """

        not_a_list = 1

        with self.assertRaises(Exception) as context:
            ds.utils.stringify.lists(not_a_list)
        self.assertEqual(
            str(context.exception),
            "Incorrect type. Supply a list.",
        )


if __name__ == "__main__":
    unittest.main()
