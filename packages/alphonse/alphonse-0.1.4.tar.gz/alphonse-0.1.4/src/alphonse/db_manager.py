# alphonse/db_manager.py

""" Database manager class. """

from typing import List, NoReturn, Optional, Union

from sqlalchemy.engine.base import Engine

try:
	from src.alphonse.crud import Crud
	from src.alphonse.utilities import validate_joins_params, validate_params
except ImportError:
	from alphonse.crud import Crud
	from alphonse.utilities import validate_joins_params, validate_params


class DbManager:
	""" Base database manager class. """

	def __init__(
		self, db_engine: Optional[Engine], table_list: Optional[list]
	) -> NoReturn:
		"""
		Initialization of the DbManager.

		:param db_engine: SQLAlchemy base engine object.
		:param table_list: List of SQLAlchemy table model objects.
		"""

		self.__crud: Crud = Crud(db_engine, table_list)

	@validate_params()
	def create(self, table_key: str, req_payload: dict) -> bool:
		"""
		Database interface method for creating new table rows.

		:param table_key: String key constant of the table that has a new row to be added.
		:param req_payload: Mapped dictionary of the table row to be created.
		:return: Tuple of a boolean indicating operation success.
		"""

		return self.__crud.create(table_key, req_payload)

	@validate_params()
	def create_and_fetch(self, table_key: str, req_payload: dict) -> dict:
		"""
		Database interface method for creating new table rows and returning
		that entity as confirmation that it was created.

		:param table_key: String key constant of the table that has a new row to be added.
		:param req_payload: Mapped dictionary of the table row to be created.
		:return: Tuple of a boolean indicating operation success.
		"""

		return self.__crud.create_and_fetch(table_key, req_payload)

	@validate_params()
	def read(
		self,
		table_key: str,
		search_params: dict,
		select_params: Optional[list] = None,
	) -> Optional[dict]:
		"""
		Database interface method for returning full or partial rows from a single database table.

		:param table_key: String key constant of the table to query.
		:param search_params: Mapped dictionary of parameters pertinent to specifying the query.
		:param select_params: List of columns to select and returns all table columns if the list is empty.
		:return: A dictionary representation of the requested db table row if a single row is found,
		if multiple rows were found, a dictionary containing a list of dictionary representations of
		the requested rows, an empty dictionary if no results are found, or None if an exception occurred.
		"""

		return self.__crud.read(table_key, search_params, select_params)

	@validate_params()
	def update(
		self, table_key: str, search_params: dict, insert_params: dict
	) -> bool:
		"""
		Database interface method for updating column values of database table rows.

		:param table_key: String key constant of the table to be updated.
		:param search_params: Mapped dictionary of parameters pertinent to specifying the query.
		:param insert_params: Mapped dictionary of key/value pairs corresponding to db
		columns to be updated.
		:return: Boolean indicating operation success.
		"""

		return self.__crud.update(table_key, search_params, insert_params)

	@validate_params()
	def delete(self, table_key: str, search_params: dict) -> bool:
		"""
		Database interface method for deleting database table rows.

		:param table_key: String key constant of the table to be updated.
		:param search_params: Mapped dictionary of parameters pertinent to specifying the query.
		:return: Boolean indicating operation success.
		"""

		return self.__crud.delete(table_key, search_params)

	@validate_params()
	@validate_joins_params()
	def joined_read(
		self,
		start_table: str,
		end_table: str,
		search_params: Union[dict, List[dict]],
		select_params: Union[List[str], List[list], None] = None,
	) -> Optional[dict]:
		"""
		Database interface method for constructing and executing a query that traverses multiple database tables.

		:param start_table: A string key of the table applies the 'search_params' to and begins the query.
		:param end_table: String key of the table on which the query should stop traversing tables.
		:param search_params: Mapped dictionary of parameters pertinent to specifying the query
		for the start_table.
		:param select_params: Optional list of lists each containing strings representing columns
		to select.
		There must be one per table traversed.
		:return: Dictionary mapping containing query results from multiple database rows,
		an empty dict if no matching rows are found, or None if an exception occurred.
		"""

		# select_params = select_params if
		return self.__crud.joined_read(
			start_table,
			end_table,
			search_params,
			select_params
		)

	@validate_params()
	def count(self, table_key: str, search_params: dict) -> Optional[dict]:
		"""
		Database interface method that returns a count of rows that match the supplied parameters.

		:param table_key: String key constant of the table to query.
		:param search_params: Mapped dictionary of parameters pertinent to specifying the query.
		:return: A dictionary containing the count of rows that meet the criteria of the provided
		parameters or an empty dictionary if an error occurs.
		"""

		return self.__crud.count(table_key, search_params)
