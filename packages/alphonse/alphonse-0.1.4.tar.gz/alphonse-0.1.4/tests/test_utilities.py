# /tests/test_utilities.py

""" TestUtilities class implementation """

from typing import NoReturn, Optional
from unittest import TestCase
from unittest.mock import patch

from src.alphonse.db_manager import DbManager
from src.alphonse.crud import Crud
from src.alphonse.utilities import exception_handler


class TestUtilities(TestCase):
	""" TestUtilities class implementation """

	def setUp(self) -> NoReturn:
		"""TestUtilities setUp method"""

		self._db_manager: Optional[DbManager] = DbManager(
			None, None
		)

		self.__read_mock = patch.object(
			Crud, "joined_read", return_value=None
		)
		self.__read_patch = self.__read_mock.start()

		# Mock log_error method for the logger.
		self.__exc_handler_mock = patch.object(exception_handler, "get_exception_log")
		self.__exc_handler_patch = self.__exc_handler_mock.start()

	def tearDown(self) -> NoReturn:
		"""TestTestUtilities tearDown method"""

		self.__read_patch.stop()
		self.__read_mock = None

		self.__exc_handler_patch.stop()
		self.__exc_handler_mock = None

		self._db_manager = None

	def test_validate_params_success(self) -> NoReturn:
		""" Test the validate_params decorator with a successful validation. """

		self.__read_patch.return_value = {}

		res = self._db_manager.joined_read(
			start_table="User",
			end_table="Credential",
			search_params={"search_params": "value"}
		)
		self.assertEqual(res, {})
		self.__exc_handler_patch.assert_not_called()

	def test_validate_params_missing_first_param(self) -> NoReturn:
		""" Scenario where the first parameter is missing from the decorated function. """

		res = self._db_manager.joined_read(
			end_table="Credential",
			search_params={"search_params": "value"},
			select_params=["id", "name"]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual("The argument `start_table` supplied to `joined_read()` is missing.", error_message)

	def test_validate_params_missing_second_param(self) -> NoReturn:
		""" Scenario where the second parameter is missing from the decorated function. """

		res = self._db_manager.joined_read(
			start_table="User",
			search_params={"search_params": "value"},
			select_params=["id", "name"]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"The argument `end_table` supplied to `joined_read()` is missing.",
			error_message
		)

	def test_validate_params_missing_third_param(self) -> NoReturn:
		""" Scenario where the third parameter is missing from the decorated function. """

		res = self._db_manager.joined_read(
			start_table="User",
			end_table="Credential",
			select_params=["id", "name"]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual("The argument `search_params` supplied to `joined_read()` is missing.", error_message)

	def test_validate_params_missing_two_params(self) -> NoReturn:
		""" Scenario where the two parameters are missing from the decorated function. """

		res = self._db_manager.joined_read(
			end_table="Credential",
			select_params=["id", "name"]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"The arguments `start_table` and `search_params` supplied to `joined_read()` are missing.",
			error_message
		)

	def test_validate_params_missing_three_params(self) -> NoReturn:
		""" Scenario where the three+ parameters are missing from the decorated function. """
		res = self._db_manager.joined_read(select_params=["id", "name"])
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"The arguments `start_table, end_table`, and `search_params` supplied to `joined_read()` are missing.",
			error_message
		)

	def test_validate_params_empty_first_param(self) -> NoReturn:
		""" Scenario where the first parameter is empty from the decorated function. """

		res = self._db_manager.joined_read(
			start_table="",
			end_table="Credential",
			search_params={"search_params": "value"},
			select_params=["id", "name"]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"The argument `start_table` supplied to `joined_read()` cannot be empty.",
			error_message
		)

	def test_validate_params_empty_second_param(self) -> NoReturn:
		""" Scenario where the second parameter is empty from the decorated function. """

		res = self._db_manager.joined_read(
			start_table="User",
			end_table="",
			search_params={"search_params": "value"},
			select_params=["id", "name"]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"The argument `end_table` supplied to `joined_read()` cannot be empty.",
			error_message
		)

	def test_validate_params_empty_third_param(self) -> NoReturn:
		""" Scenario where the third parameter is empty from the decorated function. """

		res = self._db_manager.joined_read(
			start_table="User",
			end_table="Credential",
			search_params={},
			select_params=["id", "name"]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"The argument `search_params` supplied to `joined_read()` cannot be empty.",
			error_message
		)

	def test_validate_params_two_empty_params(self) -> NoReturn:
		""" Scenario where the two parameters are empty from the decorated function. """

		res = self._db_manager.joined_read(
			start_table="",
			end_table="Credential",
			search_params={},
			select_params=["id", "name"]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"The arguments `start_table` and `search_params` supplied to `joined_read()` cannot be empty.",
			error_message
		)

	def test_validate_params_three_empty_params(self) -> NoReturn:
		""" Scenario where the three parameters are empty from the decorated function. """

		res = self._db_manager.joined_read(
			start_table="",
			end_table="",
			search_params={},
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"The arguments `start_table, end_table`, and `search_params` supplied to `joined_read()` cannot be empty.",
			error_message
		)

# ------------------------------ End validate_params tests ------------------------------

	def test_validate_joins_params_success(self) -> NoReturn:
		""" Test the validate_joins_params decorator with a successful validation. """

		self.__read_patch.return_value = {}

		res = self._db_manager.joined_read(
			start_table="User",
			end_table="Credential",
			search_params={"search_params": "value"},
			select_params=["id", "name"]
		)
		self.assertEqual(res, {})
		self.__exc_handler_patch.assert_not_called()

	def test_validate_joins_params_failure_empty_single_search_param(
		self
	) -> NoReturn:
		""" Scenario where a search param's value is empty within a single dict. """

		res = self._db_manager.joined_read(
			start_table="User",
			end_table="Credential",
			search_params={"thing": "stuff", "missing_param": "", "other_thing": "other_stuff"},
			select_params=["id", "name"]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"Empty value supplied for key `missing_param` in the `search_params` dictionary.  Use `None` to indicate an null value.",
			error_message
		)

	def test_validate_joins_params_failure_empty_nested_search_param(
		self
	) -> NoReturn:
		""" Scenario where a search param's value is an empty string within a dict within a list. """

		res = self._db_manager.joined_read(
			start_table="User",
			end_table="Credential",
			search_params=[
				{"id": 1, "name": "John Doe"},
				{"thing": "stuff", "missing_param": "", "other_thing": "other_stuff"}
			],
			select_params=["id", "name"]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"Empty value supplied for key `missing_param` in the `search_params` dictionary.  Use `None` to indicate an null value.",
			error_message
		)

	def test_validate_joins_params_failure_empty_select_params(
		self
	) -> NoReturn:
		""" Scenario where a select param's value is an empty string. """

		res = self._db_manager.joined_read(
			start_table="User",
			end_table="Credential",
			search_params=[
				{"id": 1, "name": "John Doe"},
				{"thing": "stuff", "other_thing": "other_stuff"}
			],
			select_params=["id", ""]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"Only non-empty strings are valid within the `search_params` listed supplied to the `joined_read()` method.",
			error_message
		)

	def test_validate_joins_params_failure_non_string_select_param(
		self
	) -> NoReturn:
		""" Scenario where a select param's type is not a strinr within a dict within a list. """

		res = self._db_manager.joined_read(
			start_table="User",
			end_table="Credential",
			search_params=[
				{"id": 1, "name": "John Doe"},
				{"thing": "stuff", "other_thing": "other_stuff"}
			],
			select_params=["id", False]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"Only non-empty strings are valid within the `search_params` listed supplied to the `joined_read()` method.",
			error_message
		)

	def test_validate_joins_params_failure_empty_nested_select_params(
		self
	) -> NoReturn:
		""" Scenario where a select param's value is an empty string within a nested list. """

		res = self._db_manager.joined_read(
			start_table="User",
			end_table="Credential",
			search_params=[
				{"id": 1, "name": "John Doe"},
				{"thing": "stuff", "other_thing": "other_stuff"}
			],
			select_params=[["id", "name"], ["id", ""]]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"Only non-empty strings are valid within the `search_params` listed supplied to the `joined_read()` method.",
			error_message
		)

	def test_validate_joins_params_failure_non_string_select_params(
		self
	) -> NoReturn:
		""" Scenario where a select param's type is not a string. """

		res = self._db_manager.joined_read(
			start_table="User",
			end_table="Credential",
			search_params=[
				{"id": 1, "name": "John Doe"},
				{"thing": "stuff", "other_thing": "other_stuff"}
			],
			select_params=["id", 7]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"Only non-empty strings are valid within the `search_params` listed supplied to the `joined_read()` method.",
			error_message
		)

	def test_validate_joins_params_failure_non_string_nested_select_params(
		self
	) -> NoReturn:
		""" Scenario where a select param's type is not a string within a nested list. """

		res = self._db_manager.joined_read(
			start_table="User",
			end_table="Credential",
			search_params=[
				{"id": 1, "name": "John Doe"},
				{"thing": "stuff", "other_thing": "other_stuff"}
			],
			select_params=[["id", "name"], [9, "id"]]
		)
		self.assertIsNone(res)

		self.__exc_handler_patch.assert_called()
		error_message: str = self.__exc_handler_patch.call_args[0][0].args[0]
		self.assertEqual(
			"Only non-empty strings are valid within the `search_params` listed supplied to the `joined_read()` method.",
			error_message
		)
