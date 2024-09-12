# /tests/test_crud.py

""" TestCRUD class implementation """

import copy
from typing import NoReturn, Optional
from unittest import TestCase
from unittest.mock import patch

from sqlalchemy.engine import Result
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

try:
	from src.alphonse.crud import Crud
except ImportError:
	from alphonse.crud import Crud

from tests.testing_values.testing_singleton_values import table_list


class TestCrud(TestCase):
	""" Test Crud class implementation """

	def setUp(self) -> NoReturn:
		"""TestCRUD setUp method"""

		# Create a new instance of the Crud class
		self.__crud: Optional[Crud] = Crud(None, table_list)

		# Mock the `Session.rollback()` method.
		self.__rollback_mock = patch.object(
			Session, "rollback", return_value=None
		).start()

		# Mock the `Session.expire_all()` method.
		self.__expire_all_mock = patch.object(
			Session, "expire_all", return_value=None
		).start()

		# Mock the `Session.add()` method.
		self.__add_row_mock = patch.object(
			Session, "add", return_value=None
		).start()

		# Mock the `Session..commit()` method.
		self.__session_commit_mock = patch.object(
			Session, "commit", return_value=None
		).start()

		# Mock the `Session.execute()` method.
		self.__session_execute_mock = patch.object(
			Session, "execute", return_value=Result("_metadata")  # noqa
		).start()

		# Mock the `Session..delete()` method.
		self.__session_delete_mock = patch.object(
			Session, "delete", return_value=None
		).start()

		# Mock the `Result.all()` method.
		self.__cursor_all_mock = patch.object(
			Result, "all", return_value=[]
		).start()

		# Mock the `Result.fetchall()` method.
		self.__cursor_fetchall_mock = patch.object(
			Result, "fetchall", return_value=[]
		).start()

	def tearDown(self) -> NoReturn:
		"""TestCRUD tearDown method"""

		self.__cursor_fetchall_mock.stop()
		self.__cursor_all_mock.stop()
		self.__session_delete_mock.stop()
		self.__session_execute_mock.stop()
		self.__session_commit_mock.stop()
		self.__add_row_mock.stop()
		self.__expire_all_mock.stop()
		self.__rollback_mock.stop()
		self.__crud = None

	# ------------------- CREATE -------------------

	def test_create_success_with_model_that_has_map_method(self) -> NoReturn:
		"""
		Test for the `Crud.create()` method where the operation is
		successful and the model has a `map()` method.
		"""

		result = self.__crud.create(
			"User",
			{
				"name": "test_user",
				"email": "test_user@test.com"
			}
		)
		self.assertTrue(result)

		self.__add_row_mock.assert_called_once()
		self.__session_commit_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_create_success_with_blind_model_mapping(self) -> NoReturn:
		"""
		Test for the `Crud.create()` method where the operation is
		successful and the model does not have a `map()` method.
		"""

		result = self.__crud.create(
			"Post",
			{
				"title": "post_title",
				"content": "lorem ipsum dolor sit amet ...",
				"likes": None,
				"user_id": 1,
			}
		)
		self.assertTrue(result)

		self.__add_row_mock.assert_called_once()
		self.__session_commit_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_create_failure_model_cannot_be_blind_mapped_due_to_missing_value(self) -> NoReturn:
		"""
		Test for the `Crud.create()` method where the operation
		fails because the model can't be mapped.
		"""

		result = self.__crud.create(
			"Post",
			{
				"title": "post_title",
				"content": "lorem ipsum dolor sit amet ...",
				"likes": None,
				"user_id": "1",
			}
		)
		self.assertFalse(result)

		self.__add_row_mock.assert_not_called()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_create_failure_model_cannot_be_blind_mapped_due_to_mistyped_value(self) -> NoReturn:
		"""
		Test for the `Crud.create()` method where the operation
		fails because the model can't be mapped.
		"""

		result = self.__crud.create(
			"Post",
			{
				"content": "lorem ipsum dolor sit amet ...",
				"user_id": 1,
				"likes": 0
			}
		)
		self.assertFalse(result)

		self.__add_row_mock.assert_not_called()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_create_failure_model_cannot_be_mapped_due_to_unexpected_null_value(self) -> NoReturn:
		"""
		Test for the `Crud.create()` method where the operation fails
		because the model can't be mapped due to an unexpected null value.
		"""

		result = self.__crud.create(
			"Post",
			{"content": "lorem ipsum dolor sit amet ...", "user_id": None, "likes": 0}
		)
		self.assertFalse(result)

		self.__add_row_mock.assert_not_called()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_create_failure_exception_occurs_in_bespoke_map_method(self) -> NoReturn:
		"""
		Test for the `Crud.create()` method where the operation
		fails because an exception occurs within the model's `map()` method.
		"""

		user = copy.deepcopy(self.__crud.schema_index["User"])
		with patch.object(
			user, "map", side_effect=AttributeError
		)as map_mock:
			result: bool = self.__crud.create(
				"User",
				{
					"name": "test_user",
					"email": "test_user@test.com"
				}
			)
			self.assertFalse(result)

			map_mock.assert_called_once()
		self.__add_row_mock.assert_not_called()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_create_failure_database_exception_occurs(self) -> NoReturn:
		"""
		Test for the `Crud.create()` method where the operation
		fails because ane exception occurs with the database connection.
		"""

		result: bool
		self.__add_row_mock.side_effect = DatabaseError(
			"Database error", {}, None  # noqa
		)
		result = self.__crud.create(
			"Post",
			{
				"title": "post_title",
				"content": "lorem ipsum dolor sit amet ...",
				"likes": 0,
				"user_id": 1
			}
		)
		self.assertFalse(result)

		self.__add_row_mock.assert_called_once()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_called_once()

	def test_create_failure_database_exception_occurs_and_rollback_fails(self) -> NoReturn:
		"""
		Test for the `Crud.create()` method where the operation
		fails because ane exception occurs with the database connection.
		"""

		result: bool
		self.__add_row_mock.side_effect = DatabaseError(
			"Database error", {}, None  # noqa
		)
		self.__rollback_mock.side_effect = DatabaseError(
			"Database error", {}, None  # noqa
		)
		result = self.__crud.create(
			"Post",
			{
				"title": "post_title",
				"content": "lorem ipsum dolor sit amet ...",
				"likes": 0,
				"user_id": 1
			}
		)
		self.assertFalse(result)

		self.__add_row_mock.assert_called_once()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_called_once()
		self.__expire_all_mock.assert_called_once()

	# ------------------- CREATE AND FETCH -------------------

	def test_create_and_fetch_success_with_model_that_has_map_method(self) -> NoReturn:
		"""
		Test for the `Crud.create_and_fetch()` method where the operation is
		successful and the model has a `map()` method.
		"""
		model = copy.deepcopy(self.__crud.schema_index["User"])
		mock_user = model(id=1, name='test_user', email='test@test.org')
		mock_result: tuple = (mock_user,)
		self.__cursor_all_mock.return_value = [mock_result]

		req_payload: dict = {
				"name": "test_user",
				"email": "test_user@test.com",
		}

		result = self.__crud.create_and_fetch("User", req_payload)

		self.assertEqual(
			result,
			{
				'email': 'test_user@test.com',
				'favorite_dishes': [],
				'id': None,
				'is_verified_user': False,
				'name': 'test_user'}
		)

		self.__add_row_mock.assert_called_once()
		self.__session_commit_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_create_and_fetch_success_with_blind_model_mapping(self) -> NoReturn:
		"""
		Test for the `Crud.create_and_fetch()` method where the operation is
		successful and the model does not have a `map()` method.
		"""

		model = copy.deepcopy(self.__crud.schema_index["User"])
		mock_user = model(id=1, name='test_user', email='test@test.org')
		mock_result: tuple = (mock_user,)
		self.__cursor_all_mock.return_value = [mock_result]

		req_payload: dict = {
				"is_active": True,
				"title": "post_title",
				"content": "lorem ipsum dolor sit amet ...",
				"likes": None,
				"user_id": 1,
		}

		result = self.__crud.create_and_fetch(
			"Post", req_payload
		)
		self.assertEqual(
			result,
			{
				'content': 'lorem ipsum dolor sit amet ...',
				'id': None,
				'is_active': True,
				'likes': None,
				'title': 'post_title',
				'user_id': 1
			}
		)

		self.__add_row_mock.assert_called_once()
		self.__session_commit_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_create_and_fetch_failure_model_cannot_be_blind_mapped_due_to_mistyped_value(self) -> NoReturn:
		"""
		Test for the `Crud.create_and_fetch()` method where the operation
		fails because the model can't be mapped.
		"""
		req_payload: dict = {
				"content": "lorem ipsum dolor sit amet ...",
				"user_id": 1,
				"likes": 0
		}

		result = self.__crud.create_and_fetch("Post", req_payload)
		self.assertEqual(result, {})

		self.__add_row_mock.assert_not_called()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_create_and_fetch_failure_model_cannot_be_mapped_due_to_unexpected_null_value(self) -> NoReturn:
		"""
		Test for the `Crud.create_and_fetch()` method where the operation fails
		because the model can't be mapped due to an unexpected null value.
		"""

		req_payload: dict = {
			"content": "lorem ipsum dolor sit amet ...",
			"user_id": None,
			"likes": 0
		}


		result = self.__crud.create_and_fetch("Post", req_payload)
		self.assertEqual(result, {})

		self.__add_row_mock.assert_not_called()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_create_and_fetch_failure_exception_occurs_in_bespoke_map_method(self) -> NoReturn:
		"""
		Test for the `Crud.create_and_fetch()` method where the operation
		fails because an exception occurs within the model's `map()` method.
		"""

		req_payload: dict = {
			"name": "test_user",
			"email": "test_user@test.com"
		}

		user = copy.deepcopy(self.__crud.schema_index["User"])
		with patch.object(
			user, "map", side_effect=AttributeError
		)as map_mock:

			result = self.__crud.create_and_fetch("User", req_payload)
			self.assertEqual(result, {})

			map_mock.assert_called_once()
		self.__add_row_mock.assert_not_called()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_create_and_fetch_failure_database_exception_occurs(self) -> NoReturn:
		"""
		Test for the `Crud.create_and_fetch()` method where the operation
		fails because ane exception occurs with the database connection.
		"""

		req_payload: dict = {
				"title": "post_title",
				"content": "lorem ipsum dolor sit amet ...",
				"likes": 0,
				"user_id": 1
		}

		result: dict
		self.__add_row_mock.side_effect = DatabaseError(
			"Database error", {}, None  # noqa
		)
		result = self.__crud.create_and_fetch("Post", req_payload)
		self.assertEqual(result, {})

		self.__add_row_mock.assert_called_once()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_called_once()

	def test_create_and_fetch_failure_database_exception_occurs_and_rollback_fails(self) -> NoReturn:
		"""
		Test for the `Crud.create_and_fetch()` method where the operation
		fails because ane exception occurs with the database connection.
		"""

		req_payload: dict = {
			"title": "post_title",
			"content": "lorem ipsum dolor sit amet ...",
			"likes": 0,
			"user_id": 1
		}

		result: dict
		self.__add_row_mock.side_effect = DatabaseError(
			"Database error", {}, None  # noqa
		)
		self.__rollback_mock.side_effect = DatabaseError(
			"Database error", {}, None  # noqa
		)
		result = self.__crud.create_and_fetch("Post", req_payload)
		self.assertEqual(result, {})

		self.__add_row_mock.assert_called_once()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_called_once()
		self.__expire_all_mock.assert_called_once()

	# ------------------- READ -------------------

	def test_read_success_single_result_no_select_params(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is successful
		in returning a single row with no select params supplied.
		"""

		mock_user = copy.deepcopy(
			self.__crud.schema_index["User"]
		)(id=1, name='test_user', email='test@test.org')
		mock_result: tuple = (mock_user,)
		self.__cursor_all_mock.return_value = [mock_result]

		result: dict = self.__crud.read(
			"User", {"id": 1}, None
		)
		self.assertEqual(
			result, {"id": 1, "name": "test_user", "email": "test@test.org"}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_read_success_single_result_no_select_params_search_param_is_unnecessarily_nested(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is successful
		in returning a single row with no select params supplied and a search param is unnecessarily nested.
		"""

		mock_user = copy.deepcopy(
			self.__crud.schema_index["User"]
		)(id=1, name='test_user', email='test@test.org')
		mock_result: tuple = (mock_user,)
		self.__cursor_all_mock.return_value = [mock_result]

		result: dict = self.__crud.read(
			"User", {"id": [1]}, None
		)
		self.assertEqual(
			result, {"id": 1, "name": "test_user", "email": "test@test.org"}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_read_success_multiple_result_no_select_params(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is successful
		in returning multiple rows with no select params supplied.
		"""

		mock_post_1 = copy.deepcopy(
			self.__crud.schema_index["Post"]
		)(id=1, title="Everything Wrong With The World", content="lorem ipip", likes=1, is_active=None)
		mock_post_2 = copy.deepcopy(
			self.__crud.schema_index["Post"]
		)(id=2, title="How To Make Botson Cream Pie", content="pippipcherio", likes=1, is_active=None)
		self.__cursor_all_mock.return_value = [(mock_post_1,), (mock_post_2,)]

		result: dict = self.__crud.read(
			"Post", {"likes": 1, "is_active": None}, None
		)
		self.assertEqual(
			result,
			{
				"result": [
					{"id": 1, "title": "Everything Wrong With The World", "content": "lorem ipip", "likes": 1, "is_active": None},
					{"id": 2, "title": "How To Make Botson Cream Pie", "content": "pippipcherio", "likes": 1, "is_active": None}
				]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_read_success_multiple_result_no_select_params_multiple_search_params_for_one_field(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is successful
		in returning multiple rows with no select params supplied and
		multiple option supplied for a `search_param`
		"""

		mock_post_1 = copy.deepcopy(
			self.__crud.schema_index["Post"]
		)(id=1, title="Everything Wrong With The World", content="lorem ipip", likes=1)
		mock_post_2 = copy.deepcopy(
			self.__crud.schema_index["Post"]
		)(id=2, title="How To Make Botson Cream Pie", content="pippipcherio", likes=100)
		self.__cursor_all_mock.return_value = [(mock_post_1,), (mock_post_2,)]

		result: dict = self.__crud.read(
			"Post", {"likes": [1, 100]}, None
		)
		self.assertEqual(
			result,
			{
				"result": [
					{"id": 1, "title": "Everything Wrong With The World", "content": "lorem ipip", "likes": 1},
					{"id": 2, "title": "How To Make Botson Cream Pie", "content": "pippipcherio", "likes": 100}
				]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_read_success_multiple_result_no_select_params_and_ne_equality_is_used_on_search_params(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is successful
		in returning multiple rows with no select params supplied and
		multiple option supplied for a `search_param`
		"""

		mock_post_1 = copy.deepcopy(
			self.__crud.schema_index["Post"]
		)(id=1, title="Everything Wrong With The World", content="lorem ipip", likes=1)
		mock_post_2 = copy.deepcopy(
			self.__crud.schema_index["Post"]
		)(id=2, title="How To Make Botson Cream Pie", content="pippipcherio", likes=100)
		self.__cursor_all_mock.return_value = [(mock_post_1,), (mock_post_2,)]

		result: dict = self.__crud.read(
			"Post", {"id<=": 10000, "likes>=": 1, "title!=": ["Bad title", "Even worse title"]}, None
		)
		self.assertEqual(
			result,
			{
				"result": [
					{"id": 1, "title": "Everything Wrong With The World", "content": "lorem ipip", "likes": 1},
					{"id": 2, "title": "How To Make Botson Cream Pie", "content": "pippipcherio", "likes": 100}
				]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_read_success_multiple_result_no_select_params_and_equality_is_used_on_search_params(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is successful
		in returning multiple rows with no select params supplied and
		multiple option supplied for a `search_param`
		"""

		mock_post_1 = copy.deepcopy(
			self.__crud.schema_index["Post"]
		)(id=1, title="Everything Wrong With The World", content="lorem ipip", likes=1)
		mock_post_2 = copy.deepcopy(
			self.__crud.schema_index["Post"]
		)(id=2, title="How To Make Botson Cream Pie", content="pippipcherio", likes=100)
		self.__cursor_all_mock.return_value = [(mock_post_1,), (mock_post_2,)]

		result: dict = self.__crud.read(
			"Post", {"id<=": 10000, "likes>=": 1, "title==": ["Everything Wrong With The World", "How To Make Botson Cream Pie"]}, None
		)
		self.assertEqual(
			result,
			{
				"result": [
					{"id": 1, "title": "Everything Wrong With The World", "content": "lorem ipip", "likes": 1},
					{"id": 2, "title": "How To Make Botson Cream Pie", "content": "pippipcherio", "likes": 100}
				]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_read_success_single_result_with_select_params(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is successful
		in returning a single row with select params supplied.
		"""

		self.__cursor_all_mock.return_value = [(1,)]

		result: dict = self.__crud.read(
			"User", {"id": 1}, ["id"]
		)
		self.assertEqual(result, {"id": 1})

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_read_success_single_result_with_distinct_select_params(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is successful
		in returning a single row with distinct select params supplied.
		"""

		self.__cursor_all_mock.return_value = [(1,)]

		result: dict = self.__crud.read(
			"User", {"id": 1}, ["id%"]
		)
		self.assertEqual(result, {"id": 1})

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_read_success_multiple_result_with_select_params(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is successful
		in returning multiple rows with select params supplied.
		"""

		self.__cursor_all_mock.return_value = [
			(1, "Everything Wrong With The World",),
			(2, "How To Make Botson Cream Pie")
		]

		result: dict = self.__crud.read(
			"Post", {"likes": 1}, ["id", "title"]
		)
		self.assertEqual(
			result,
			{
				"result": [
					{"id": 1, "title": "Everything Wrong With The World"},
					{"id": 2, "title": "How To Make Botson Cream Pie"}
				]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_read_success_multiple_results_with_distinct_select_params(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is successful
		in returning one of multiple rows with distinct select params supplied.
		"""

		self.__cursor_all_mock.return_value = [
			(1, "Everything Wrong With The World",),
		]

		result: dict = self.__crud.read(
			"Post", {"likes": 1}, ["id%", "title"]
		)
		self.assertEqual(result, {"id": 1, "title": "Everything Wrong With The World"},)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_read_failure_no_result_found(self) -> NoReturn:
		""" Test for the `Crud.read()` method where the operation finds no result. """

		self.__cursor_all_mock.return_value = []

		result: dict = self.__crud.read(
			"User", {"id": 1}, ["id"]
		)
		self.assertEqual(result, {})
		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_read_failure_database_model_not_found(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation
		fails because the supplied model is not in the schema_index.
		"""

		result: Optional[dict] = self.__crud.read(
			"users", {"id": 1}, ["id"]
		)
		self.assertEqual(result, None)
		self.__session_execute_mock.assert_not_called()
		self.__cursor_all_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_read_failure_database_exception_occurs(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation
		fails because ane exception occurs with the database connection.
		"""

		self.__session_execute_mock.side_effect = DatabaseError(
			"Database error", {}, None  # noqa
		)

		result: Optional[dict] = self.__crud.read(
			"User", {"id": 1}, ["id"]
		)
		self.assertIsNone(result)
		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_not_called()
		self.__rollback_mock.assert_called_once()

	def test_read_failure_improperly_formatted_select_param(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation
		fails because the `select_parameters` have the distinct
		operator applied at the front of a value.
		"""

		result: dict = self.__crud.read(
			"User",
			{"id": 1},
			["%id", "email",]
		)
		self.assertIsNone(result)
		self.__session_execute_mock.assert_not_called()
		self.__cursor_all_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_read_failure_select_param_does_not_exist(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation fails because
		one of the `select_parameters` doesn't exist on the table.
		"""

		result: dict = self.__crud.read(
			"User",
			{"id": 1},
			["rizz", "email",]
		)
		self.assertIsNone(result)
		self.__session_execute_mock.assert_not_called()
		self.__cursor_all_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_read_failure_search_param_does_not_exist(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation fails because
		one of the `search_parameters` doesn't exist on the table.
		"""

		result: dict = self.__crud.read(
			"User",
			{"id": 1, "height": 77},
			["id", "email",]
		)
		self.assertIsNone(result)
		self.__session_execute_mock.assert_not_called()
		self.__cursor_all_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_read_failure_search_param_is_wrong_type(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation fails
		because one of the `search_parameters` is of the wrong type.
		"""

		result: dict = self.__crud.read(
			"User",
			{"id": "1"},
			["id", "email",]
		)
		self.assertIsNone(result)
		self.__session_execute_mock.assert_not_called()
		self.__cursor_all_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_read_failure_search_param_none_on_non_nullable_column(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation fails
		because one of the `search_parameters` is None for a non-nullable column.
		"""

		result: dict = self.__crud.read(
			"User",
			{"id": None},
			["id", "email",]
		)
		self.assertIsNone(result)
		self.__session_execute_mock.assert_not_called()
		self.__cursor_all_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_read_failure_equality_operator_not_on_correct_side_of_search_param(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is a failure because
		the operator is on the incorrect side of the `search_param's` key
		"""

		result: dict = self.__crud.read(
			"User", {">=id": 1}, None
		)
		self.assertIsNone(result)

		self.__session_execute_mock.assert_not_called()
		self.__cursor_all_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_read_failure_equality_operator_supplied_instead_of_search_param(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is a failure because
		the operator is supplied a `search_param` with no param attached.
		"""

		result: dict = self.__crud.read(
			"User", {">=": 1}, None
		)
		self.assertIsNone(result)

		self.__session_execute_mock.assert_not_called()
		self.__cursor_all_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_read_failure__invalid_equality_operator_supplied_for_search_param(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is a failure because
		an invalid operator is supplied for the `search_param`.
		"""

		result: dict = self.__crud.read(
			"User", {"id=!": 1}, None
		)
		self.assertIsNone(result)

		self.__session_execute_mock.assert_not_called()
		self.__cursor_all_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_read_failure_multiple_result_no_select_params_and_ne_equality_is_used_on_search_params(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is a failure
		because an invalid list of `search_params` are supplied.
		"""

		result: dict = self.__crud.read(
			"Post", {"is_active": [True, False, None]}, None
		)
		self.assertIsNone(result)

		self.__session_execute_mock.assert_not_called()
		self.__cursor_all_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_read_failure_multiple_result_no_select_params_and_equality_is_used_on_search_params(self) -> NoReturn:
		"""
		Test for the `Crud.read()` method where the operation is a failure
		because an invalid list of `search_params` are supplied.
		"""

		result: dict = self.__crud.read(
			"Post",
			{"is_active!=": [True, False, None]},
			None
		)

		self.assertIsNone(result)

		self.__session_execute_mock.assert_not_called()
		self.__cursor_all_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	# ------------------ UPDATE ------------------

	def test_update_success(self) -> NoReturn:
		""" Test for the `Crud.update()` method where the operation is successful. """

		mock_user = copy.deepcopy(
			self.__crud.schema_index["User"]
		)(id=1, name='test_user', email='test@test.org')
		mock_result: tuple = (mock_user,)
		self.__cursor_all_mock.return_value = [mock_result]

		result: bool = self.__crud.update(
			"User", {"id": 1}, {"email": "abc@test.net"}
		)
		self.assertTrue(result)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__session_commit_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_update_failure_no_result_found(self) -> NoReturn:
		""" Test for the `Crud.update()` method where the operation finds no result. """

		self.__cursor_all_mock.return_value = []

		result: bool = self.__crud.update(
			"User", {"id": 1}, {"email": "abc@test.net"}
		)
		self.assertFalse(result)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_update_failure_database_model_not_found(self) -> NoReturn:
		"""
		Test for the `Crud.update()` method where the operation
		fails because the supplied model is not in the schema_index.
		"""

		result: bool = self.__crud.update(
			"user",
			{"id": 1},
			{"email": "abc@test.net"}
		)
		self.assertFalse(result)

		self.__session_execute_mock.assert_not_called()
		self.__cursor_all_mock.assert_not_called()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_update_failure_database_exception_occurs(self) -> NoReturn:
		"""
		Test for the `Crud.update()` method where the operation
		fails because ane exception occurs with the database connection.
		"""

		self.__session_execute_mock.side_effect = DatabaseError(
			"Database error", {}, None  # noqa
		)

		result: bool = self.__crud.update(
			"User", {"id": 1}, {"email": "abc@test.net"}
		)
		self.assertFalse(result)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_not_called()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_called_once()

	# ------------------ DELETE ------------------

	def test_delete_success(self) -> NoReturn:
		"""
		Test for the `Crud.delete()` method where the operation is successful.
		"""

		mock_user = copy.deepcopy(
			self.__crud.schema_index["User"]
		)(id=1, name='test_user', email='test@test.org')
		mock_result: tuple = (mock_user,)
		self.__cursor_all_mock.return_value = [mock_result]

		result: bool = self.__crud.delete("User", {"id": 1})
		self.assertTrue(result)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__session_delete_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_delete_failure_no_result_found(self) -> NoReturn:
		""" Test for the `Crud.delete()` method where the operation finds no result. """

		self.__cursor_all_mock.return_value = []

		result: bool = self.__crud.delete(
			"User", {"id": 1}
		)
		self.assertFalse(result)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_delete_failure_database_model_not_found(self) -> NoReturn:
		"""
		Test for the `Crud.delete()` method where the operation
		fails because the supplied model is not in the schema_index.
		"""

		result: bool = self.__crud.delete(
			"users", {"id": 1},
		)
		self.assertFalse(result)

		self.__session_execute_mock.assert_not_called()
		self.__cursor_all_mock.assert_not_called()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_delete_failure_database_exception_occurs(self) -> NoReturn:
		"""
		Test for the `Crud.delete()` method where the operation
		fails because ane exception occurs with the database connection.
		"""

		self.__session_execute_mock.side_effect = DatabaseError(
			"Database error", {}, None  # noqa
		)

		result: bool = self.__crud.delete(
			"User", {"id": 1}
		)
		self.assertFalse(result)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_not_called()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_called_once()

# --------------- JOINED_READ ----------------

	def test_joined_read_success_with_single_search_params_and_no_select_params(
		self
	) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation is successful.
		A single `search_parameter` is supplied and no `select_parameters` are supplied.
		"""

		mock_user = copy.deepcopy(
			self.__crud.schema_index["User"]
		)(id=1, name='test_user', email='test@test.org')

		mock_post = copy.deepcopy(
			self.__crud.schema_index["Post"]
		)(id=1, title="Everything Wrong With The World", content="lorem ipip", likes=1, user_id=1)

		self.__cursor_fetchall_mock.return_value = [(mock_user, mock_post)]

		result: dict = self.__crud.joined_read(
			"User", "Post", [{"id": 1}]
		)
		self.assertEqual(
			result,
			{
				"User": [{"id": 1, "name": "test_user", "email": "test@test.org"}],
				"Post": [{"id": 1, "title": "Everything Wrong With The World", "content": "lorem ipip", "likes": 1, "user_id": 1}]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_fetchall_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_success_with_single_search_params_and_no_select_params_returns_multiple_rows_for_a_single_table(
		self
	) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation is successful.
		A single `search_parameter` is supplied and no `select_parameters` are supplied.
		Multiple results are returned for a single table.
		"""

		mock_user = copy.deepcopy(
			self.__crud.schema_index["User"]
		)(id=1, name='test_user', email='test@test.org')
		mock_post_1 = copy.deepcopy(
			self.__crud.schema_index["Post"]
		)(id=1, title="Everything Wrong With The World", content="lorem ipip", likes=1, user_id=1)
		mock_post_2 = copy.deepcopy(
			self.__crud.schema_index["Post"]
		)(id=47, title="This is another post", content="bleep blorp", likes=200, user_id=1)
		self.__cursor_fetchall_mock.return_value = [(mock_user, mock_post_1), (mock_user, mock_post_2)]

		result: dict = self.__crud.joined_read(
			"User", "Post", [{"id": 1}]
		)
		self.assertEqual(
			result,
			{
				"User": [
					{"id": 1, "name": "test_user", "email": "test@test.org"}
				],
				"Post": [
					{"id": 1, "title": "Everything Wrong With The World", "content": "lorem ipip", "likes": 1, "user_id": 1},
					{"id": 47, "title": "This is another post", "content": "bleep blorp", "likes": 200, "user_id": 1}
				]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_fetchall_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_success_with_multi_search_params_and_no_select_params(
		self
	) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation is successful.
		`search_parameters` are supplied for multiple tables and no `select_parameters` are supplied.
		"""

		mock_user = copy.deepcopy(
			self.__crud.schema_index["User"]
		)(id=1, name='test_user', email='test@test.org')

		mock_post = copy.deepcopy(
			self.__crud.schema_index["Post"]
		)(id=42, title="Everything Wrong With The World", content="lorem ipip", likes=7000, user_id=1)

		self.__cursor_fetchall_mock.return_value = [(mock_user, mock_post)]

		result: dict = self.__crud.joined_read(
			"User",
			"Post",
			[{"id": 1}, {"id": 42}],
		)
		self.assertEqual(
			result,
			{
				"User": [{"id": 1, "name": "test_user", "email": "test@test.org"}],
				"Post": [{"id": 42, "title": "Everything Wrong With The World", "content": "lorem ipip", "likes": 7000, "user_id": 1}]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_fetchall_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_success_with_single_search_params_and_single_select_params(
		self
	) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation is successful.
		A single `search_parameter` is supplied, and `select_parameters` are supplied for the first table only.
		"""

		mock_post = copy.deepcopy(
			self.__crud.schema_index["Post"]
		)(id=1, title="Everything Wrong With The World", content="lorem ipip", likes=1, user_id=1)

		self.__cursor_fetchall_mock.return_value = [(1, 'test_user', 'test@test.org', mock_post)]

		result: dict = self.__crud.joined_read(
			"User",
			"Post",
			[{"id": 1}],
			[["id", "name", "email"]]
		)
		self.assertEqual(
			result,
			{
				"User": [{"id": 1, "name": "test_user", "email": "test@test.org"}],
				"Post": [{"id": 1, "title": "Everything Wrong With The World", "content": "lorem ipip", "likes": 1, "user_id": 1}]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_fetchall_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_success_with_single_search_params_and_single_distinct_select_params(
		self
	) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation is successful.
		A single `search_parameter` is supplied,
		and `select_parameters` are supplied for the first table only with one distinct column.
		"""

		mock_post = copy.deepcopy(
			self.__crud.schema_index["Post"]
		)(id=1, title="Everything Wrong With The World", content="lorem ipip", likes=1, user_id=1)

		self.__cursor_fetchall_mock.return_value = [(1, 'test_user', 'test@test.org', mock_post)]

		result: dict = self.__crud.joined_read(
			"User",
			"Post",
			[{"id": 1}],
			[["id%", "name", "email"]]
		)
		self.assertEqual(
			result,
			{
				"User": [{"id": 1, "name": "test_user", "email": "test@test.org"}],
				"Post": [{"id": 1, "title": "Everything Wrong With The World", "content": "lorem ipip", "likes": 1, "user_id": 1}]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_fetchall_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_success_with_single_search_params_and_single_select_params_for_end_table_only(
		self
	) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation is successful.
		A single `search_parameter` is supplied, and `select_parameters` are supplied for the first table only.
		"""

		mock_user = copy.deepcopy(self.__crud.schema_index["User"])(
			id=1, name='test_user', email='test@test.org',
		)

		self.__cursor_fetchall_mock.return_value = [(mock_user, 42, 7000)]

		result: dict = self.__crud.joined_read(
			"User",
			"Post",
			[{"id": 1}],
			[[], ["id", "likes"]]
		)
		self.assertEqual(
			result,
			{
				"User": [{"id": 1, "name": "test_user", "email": "test@test.org"}],
				"Post": [{"id": 42, "likes": 7000}]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_fetchall_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_success_with_single_search_params_and_multi_select_params(
		self
	) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation is successful.
		A single `search_parameter` is supplied, and `select_parameters` are supplied for multiple tables.
		"""

		self.__cursor_fetchall_mock.return_value = [(1, 'test_user', 42, 7000)]

		result: dict = self.__crud.joined_read(
			"User",
			"Post",
			[{"id": 1}],
			[["id", "name"], ["id", "likes"]]
		)
		self.assertEqual(
			result,
			{
				"User": [{"id": 1, "name": "test_user"}],
				"Post": [{"id": 42, "likes": 7000}]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_fetchall_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_success_with_single_search_params_and_more_multi_select_params_then_tables_traversed(
		self
	) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation is successful.
		A single `search_parameter` is supplied, and `select_parameters` are
		supplied for more tables than will be traversed.
		"""

		self.__cursor_fetchall_mock.return_value = [(1, 'test_user', 42, 7000)]

		result: dict = self.__crud.joined_read(
			"User",
			"Post",
			[{"id": 1}],
			[["id", "name"], ["id", "likes"], []]
		)
		self.assertEqual(
			result,
			{
				"User": [{"id": 1, "name": "test_user"}],
				"Post": [{"id": 42, "likes": 7000}]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_fetchall_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_success_with_single_search_params_and_multi_distinct_select_params(
		self
	) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation is successful.
		A single `search_parameter` is supplied, and `select_parameters` are supplied for multiple tables
		with distinct parameters.
		"""

		self.__cursor_fetchall_mock.return_value = [(1, 'test_user', 42, 7000)]

		result: dict = self.__crud.joined_read(
			"User",
			"Post",
			[{"id": 1}],
			[["id%", "name"], ["id%", "likes"]]
		)
		self.assertEqual(
			result,
			{
				"User": [{"id": 1, "name": "test_user"}],
				"Post": [{"id": 42, "likes": 7000}]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_fetchall_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_success_with_multi_search_params_and_multi_select_params(
		self
	) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation is successful.
		A multiple `search_parameters` are supplied, and `select_parameters` are supplied for multiple tables.
		"""

		self.__cursor_fetchall_mock.return_value = [(1, 'test_user', 42, 7000)]

		result: dict = self.__crud.joined_read(
			"User",
			"Post",
			[{"id": 1}, {"id": 42}],
			[["id", "name"], ["id", "likes"]]
		)
		self.assertEqual(
			result,
			{
				"User": [{"id": 1, "name": "test_user"}],
				"Post": [{"id": 42, "likes": 7000}]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_fetchall_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_success_with_multi_search_params_and_multi_select_params_return_multiple_rows(
		self
	) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation is successful.
		A multiple `search_parameters` are supplied, and `select_parameters` are supplied for multiple tables.
		Multiple tables are returned and multiple rows are returned for certain tables.
		"""

		self.__cursor_fetchall_mock.return_value = [(1, 'test_user', 1, 1), (1, 'test_user', 47, 200)]

		result: dict = self.__crud.joined_read(
			"User",
			"Post",
			[{"id": 1}, {"user_id": 1}],
			[["id", "name"], ["id", "likes"]]
		)
		self.assertEqual(
			result,
			{
				"User": [{"id": 1, "name": "test_user"}],
				"Post": [{"id": 1, "likes": 1}, {"id": 47, "likes": 200}]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_fetchall_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_success_across_joins_table(
		self
	) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation is successful while traversing a JOINS table.
		"""
		mock_joins_table_1 = copy.deepcopy(
			self.__crud.schema_index["AssignedAsset"]
		)(user_id=1, art_asset_id=1)
		mock_joins_table_2 = copy.deepcopy(
			self.__crud.schema_index["AssignedAsset"]
		)(user_id=1, art_asset_id=42)

		self.__cursor_fetchall_mock.return_value = [
			(1, 'test_user', mock_joins_table_1, "standard_asset", "The Standard asset for all users"),
			(1, 'test_user', mock_joins_table_2, "special_asset", "A special asset for certain users")
		]

		result: dict = self.__crud.joined_read(
			"User",
			"ArtAsset",
			[{"id": 1}, {}, {}],
			[["id", "name"], [], ["name", "description"]]
		)
		self.assertEqual(
			result,
			{
				"User": [{"id": 1, "name": "test_user"}],
				"AssignedAsset": [
					{"user_id": 1, "art_asset_id": 1},
					{"user_id": 1, "art_asset_id": 42}
				],
				"ArtAsset": [
					{"name": "standard_asset", "description": "The Standard asset for all users"},
					{"name": "special_asset", "description": "A special asset for certain users"}
				]
			}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_fetchall_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_failure_no_results_found(self) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the
		operation fails because no db results are found.
		"""

		self.__cursor_fetchall_mock.return_value = []

		result: dict = self.__crud.joined_read(
			"User", "Post", [{"id": 1}],
		)
		self.assertEqual(result, {})

		self.__session_execute_mock.assert_called_once()
		self.__cursor_fetchall_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_failure_database_model_not_found(self) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation
		fails because the supplied model is not in the schema_index.
		"""

		result: dict = self.__crud.joined_read(
			"User", "Toast", [{"id": 1}],
		)
		self.assertIsNone(result)

		self.__session_execute_mock.assert_not_called()
		self.__cursor_fetchall_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_failure_sql_statement_cant_be_constructed_due_to_bad_search_param(self) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation fails because
		the `search_params` supplied can't be used to construct a SQL statement.
		"""

		result: dict = self.__crud.joined_read(
			"User", "Post", [{"bad_param": "idk"}],
		)
		self.assertIsNone(result)

		self.__session_execute_mock.assert_not_called()
		self.__cursor_fetchall_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_joined_read_failure_db_error(self) -> NoReturn:
		""" Test for the `Crud.joined_read()` method where the operation fails because a database error occurs. """

		self.__session_execute_mock.side_effect = DatabaseError(
			"Database error", {}, None   # noqa
		)

		result: dict = self.__crud.joined_read(
			"User", "Post", [{"id": 1}],
		)
		self.assertIsNone(result)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_fetchall_mock.assert_not_called()
		self.__rollback_mock.assert_called_once()

	def test_joined_read_failure_no_path_found_between_tables(
		self
	) -> NoReturn:
		"""
		Test for the `Crud.joined_read()` method where the operation is successful.
		A single `search_parameter` is supplied and no `select_parameters` are supplied.
		"""

		result: dict = self.__crud.joined_read(
			"User", "Disconnected", [{"id": 1}],
		)
		self.assertIsNone(result)

		self.__session_execute_mock.assert_not_called()
		self.__cursor_fetchall_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	# ------------------ COUNT -------------------
	def test_count_success(self) -> NoReturn:
		"""
		Test for the `Crud.count()` method where the operation is successful.
		"""

		mock_user = copy.deepcopy(
			self.__crud.schema_index["User"]
		)(id=1, name='test_user', email='test@test.org')
		mock_result: tuple = (mock_user,)
		self.__cursor_all_mock.return_value = [mock_result]

		result: dict = self.__crud.count("User", {"id": 1})
		self.assertEqual(
			result, {"count": 1}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_count_failure_no_result_found(self) -> NoReturn:
		""" Test for the `Crud.count()` method where the operation finds no result. """

		self.__cursor_all_mock.return_value = []

		result: Optional[dict] = self.__crud.count(
			"User", {"id": 1}
		)
		self.assertEqual(
			result, {"count": 0}
		)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_called_once()
		self.__rollback_mock.assert_not_called()

	def test_count_failure_database_model_not_found(self) -> NoReturn:
		"""
		Test for the `Crud.count()` method where the operation
		fails because the supplied model is not in the schema_index.
		"""

		result: Optional[dict] = self.__crud.count(
			"user",
			{"id": 1},
		)
		self.assertIsNone(result)

		self.__session_execute_mock.assert_not_called()
		self.__cursor_all_mock.assert_not_called()
		self.__rollback_mock.assert_not_called()

	def test_count_failure_database_exception_occurs(self) -> NoReturn:
		"""
		Test for the `Crud.count()` method where the operation
		fails because ane exception occurs with the database connection.
		"""

		self.__session_execute_mock.side_effect = DatabaseError(
			"Database error", {}, None   # noqa
		)

		result: Optional[dict] = self.__crud.count(
			"User", {"id": 1}
		)
		self.assertIsNone(result)

		self.__session_execute_mock.assert_called_once()
		self.__cursor_all_mock.assert_not_called()
		self.__session_commit_mock.assert_not_called()
		self.__rollback_mock.assert_called_once()
