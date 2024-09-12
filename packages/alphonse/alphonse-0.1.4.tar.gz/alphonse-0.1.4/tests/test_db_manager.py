# /tests/test_db_manager.py

""" TestDBManager class implementation """

from typing import Any, Dict, List, NoReturn, Optional
from unittest import TestCase
from unittest.mock import patch

from src.alphonse.db_manager import DbManager
from src.alphonse.crud import Crud
from tests.testing_values.testing_singleton_values import table_list


class TestDBManager(TestCase):
	""" Test DBManager class implementation """

	def setUp(self) -> NoReturn:
		"""TestDBManager setUp method"""

		# Create a new instance of the DbManager class
		self.__db_manager: Optional[DbManager] = DbManager(
			None, table_list
		)

	def tearDown(self) -> NoReturn:
		"""TestDBManager tearDown method"""

		self.__db_manager = None

	def test_create_success(self) -> NoReturn:
		"""Test for the `create()` method where the operation is successful."""

		with patch.object(Crud, "create", return_value=True) as mock_create:
			res: bool = self.__db_manager.create(
				"User", {"username": "test_user", "password": "test_password"}
			)
			self.assertTrue(res)
			mock_create.assert_called_once()

	def test_create_quiet_failure(self) -> NoReturn:
		"""Test for the `create()` method where the operation fails."""

		with patch.object(Crud, "create", return_value=False) as mock_create:
			res: bool = self.__db_manager.create(
				"User", {"username": "test_user", "password": "test_password"}
			)
			self.assertFalse(res)
			mock_create.assert_called_once()

	def test_create_and_fetch_success(self) -> NoReturn:
		"""Test for the `create_and_fetch()` method where the operation is successful."""

		with patch.object(Crud, "create_and_fetch", return_value={"username": "test_user", "password": "test_password"}) as mock_create_and_fetch:
			res: dict = self.__db_manager.create_and_fetch(
				"User", {"username": "test_user", "password": "test_password"}
			)
			self.assertEqual(res, {"username": "test_user", "password": "test_password"})
			mock_create_and_fetch.assert_called_once()

	def test_create_and_fetch_quiet_failure(self) -> NoReturn:
		"""Test for the `create_and_fetch()` method where the operation fails."""

		with patch.object(Crud, "create_and_fetch", return_value={}) as mock_create_and_fetch:
			res: dict = self.__db_manager.create_and_fetch(
				"User", {"username": "test_user", "password": "test_password"}
			)
			self.assertEqual(res, {})
			mock_create_and_fetch.assert_called_once()

	def test_read_success(self) -> NoReturn:
		"""Test for the `read()` method where the operation is successful."""

		with patch.object(Crud, "read", return_value=True) as mock_read:
			res: Optional[dict] = self.__db_manager.read(
				"User", {"username": "test_user", "password": "test_password"}
			)
			self.assertTrue(res)
			mock_read.assert_called_once()

	def test_read_quiet_failure(self) -> NoReturn:
		"""Test for the `read()` method where the operation fails quietly."""

		with patch.object(Crud, "read", return_value=False) as mock_read:
			res: Optional[dict] = self.__db_manager.read(
				"User", {"username": "test_user", "password": "test_password"}
			)
			self.assertFalse(res)
			mock_read.assert_called_once()

	def test_read_hard_failure(self) -> NoReturn:
		"""Test for the `read()` method where the operation fails quietly."""

		with patch.object(Crud, "read", return_value=None) as mock_read:
			res: Optional[dict] = self.__db_manager.read(
				"User", {"username": "test_user", "password": "test_password"}
			)
			self.assertIsNone(res)
			mock_read.assert_called_once()

	def test_update_success(self) -> NoReturn:
		"""Test for the `update()` method where the operation is successful."""

		with patch.object(Crud, "update", return_value=True) as mock_update:
			res: bool = self.__db_manager.update(
				"User", {"id": 43}, {"status": "active"}
			)
			self.assertTrue(res)
			mock_update.assert_called_once()

	def test_update_quiet_failure(self) -> NoReturn:
		"""Test for the `update()` method where the operation fails."""

		with patch.object(Crud, "update", return_value=False) as mock_update:
			res: bool = self.__db_manager.update(
				"User", {"id": 43}, {"status": "active"}
			)
			self.assertFalse(res)
			mock_update.assert_called_once()

	def test_delete_success(self) -> NoReturn:
		"""Test for the `delete()` method where the operation is successful."""

		with patch.object(Crud, "delete", return_value=True) as mock_delete:
			res: bool = self.__db_manager.delete(
				"User", {"id": 43}
			)
			self.assertTrue(res)
			mock_delete.assert_called_once()

	def test_delete_quiet_failure(self) -> NoReturn:
		"""Test for the `delete()` method where the operation fails quietly."""

		with patch.object(Crud, "delete", return_value=False) as mock_delete:
			res: bool = self.__db_manager.delete(
				"User", {"id": -1}
			)
			self.assertFalse(res)
			mock_delete.assert_called_once()

	def test_joined_read_success_no_optional_parameters(self) -> NoReturn:
		""" Success case for joined read where no optional parameters are provided """

		mock_query_res: Dict[str, List[dict[str, Any]]] = {
				"User": [{"id": 1, "username": "test_user"}],
				"Credential": [{"id": 1, "user_id": 1, "password": "test_password"}]
			}
		with patch.object(
			Crud, "joined_read", return_value=mock_query_res
		) as mock_joined_read:
			res = self.__db_manager.joined_read(
				start_table="User",
				end_table="Credential",
				search_params={"id": 1}
			)
			self.assertEqual(res, mock_query_res)
			mock_joined_read.assert_called_once()

	def test_joined_read_success_with_optional_parameters(self) -> NoReturn:
		""" Success case for joined read where no optional parameters are provided """

		mock_query_res: Dict[str, List[dict[str, Any]]] = {
				"User": [{"id": 1}],
				"Credential": [{"id": 1}]
			}
		with patch.object(
			Crud, "joined_read", return_value=mock_query_res
		) as mock_joined_read:
			res = self.__db_manager.joined_read(
				start_table="User",
				end_table="Credential",
				search_params={"id": 1},
				select_params=[["id"], ["id"]]
			)
			self.assertEqual(res, mock_query_res)
			mock_joined_read.assert_called_once()

	def test_joined_read_quiet_failure(self) -> NoReturn:
		""" Failure case for the `joined_read()` where no row is found. """

		with patch.object(
			Crud, "joined_read", return_value={}
		) as mock_joined_read:
			res = self.__db_manager.joined_read(
				start_table="User",
				end_table="Credential",
				search_params={"id": 1},
				select_params=[["id"], ["id"]]
			)
			self.assertEqual(res, {})
			mock_joined_read.assert_called_once()

	def test_joined_read_hard_failure(self) -> NoReturn:
		""" Failure case for the `joined_read()` where no row is found. """

		with patch.object(
			Crud, "joined_read", return_value=None
		) as mock_joined_read:
			res = self.__db_manager.joined_read(
				start_table="User",
				end_table="Credential",
				search_params={"id": 1},
				select_params=[["id"], ["id"]]
			)
			self.assertIsNone(res)
			mock_joined_read.assert_called_once()

	def test_count_success(self) -> NoReturn:
		"""Test for the `count()` method where the operation is successful."""

		mock_query_result = {"count": 2}
		with patch.object(
			Crud, "count", return_value=mock_query_result
		) as mock_count:
			res: Optional[dict] = self.__db_manager.count(
				"User", {"password": "12345password"}
			)
			self.assertEqual(res, mock_query_result)
			mock_count.assert_called_once()

	def test_count_quiet_failure(self) -> NoReturn:
		"""Test for the `count()` method where now rows are found."""

		mock_query_result = {"count": 0}
		with patch.object(
			Crud, "count", return_value=mock_query_result
		) as mock_count:
			res: Optional[dict] = self.__db_manager.count(
				"User", {"password": "12345password"}
			)
			self.assertEqual(res, mock_query_result)
			mock_count.assert_called_once()

	def test_count_hard_failure(self) -> NoReturn:
		"""Test for the `count()` method where an exception occurs."""

		with patch.object(
			Crud, "count", return_value=None
		) as mock_count:
			res: Optional[dict] = self.__db_manager.count(
				"User", {"password": "12345password"}
			)
			self.assertIsNone(res)
			mock_count.assert_called_once()
