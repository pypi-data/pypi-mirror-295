# alphonse/crud.py

""" Crud class definition. """

from copy import copy
from typing import List, NoReturn, Optional

from solidipy.exceptions import MASTER_EXCEPTION_TUPLE
from sqlalchemy.engine import Result, Row
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, class_mapper, sessionmaker
from sqlalchemy.sql import StatementLambdaElement

try:
	from src.alphonse.sql_constructor import SQLConstructor
	from src.alphonse.utilities import exception_handler, logger
except ImportError:
	from alphonse.sql_constructor import SQLConstructor
	from alphonse.utilities import exception_handler, logger


class Crud:
	"""
	Class used to map SqlAlchemy table objects, execute SQL statements, and control the db session.
	"""

	def __init__(self, engine: Optional[Engine], table_list: Optional[list]) -> NoReturn:
		"""
		Crud Initialization.

		:param engine: Instance of a SQLAlchemy db engine that contains db connection information.
		:param table_list: list of SQLAlchemy table model objects.
		"""

		self.engine: Optional[Engine] = engine if engine else None
		self.schema_index: dict = {cls.__name__: cls for cls in table_list} if table_list else {}
		self.sql_constructor: SQLConstructor = SQLConstructor()

	def create(self, table_key: str, req_payload: dict) -> bool:
		"""
		Base method for creating a new entity or row in the database.

		:param table_key: String key constant of the table that has a new row to be added.
		:param req_payload: A request object containing the payload of values used to create a new
		row in a database table.
		:return: Flag indicating if the operation was a success.
		"""

		# Get a shallow copy of the specified db table model and map the request payload to it.
		mapped_table_model = self.__get_mapped_model(
			table_key, req_payload
		)

		row_was_created: bool = False

		# If the table model is mapped successfully, start a session with the db and attempt to add the new row.
		if mapped_table_model is not None:
			with sessionmaker(bind=self.engine)() as session:
				try:
					session.add(mapped_table_model)
					session.commit()
					row_was_created = True

				except MASTER_EXCEPTION_TUPLE as exception:
					self.__rollback_session(session, exception)

		return row_was_created

	def create_and_fetch(self, table_key: str, req_payload: dict) -> dict:
		"""
		Method for creating a new entity or row in the database and returning
		that entity as confirmation that it was created.

		:param table_key: String key constant of the table that has a new row to
		be added.
		:param req_payload: A request object containing the payload of values
		used to create a new row in a database table.
		:return: Dictionary representation of the newly created row or an empty
		dictionary if the insert failed.
		"""

		# Get a shallow copy of the specified db table model and map the request
		# payload to it.  If the table model is mapped successfully, start a session
		# with the db & attempt to add the new row.
		if (mapped_table_model := self.__get_mapped_model(table_key, req_payload)) is None:
			return {}

		inserted_row: dict = {}
		with sessionmaker(bind=self.engine)() as session:
			try:
				session.add(mapped_table_model)
				session.flush()  # Push the changes to the DB without committing
				# Access the primary key or other fields after flush
				inserted_row = self.__model_to_dict(mapped_table_model)
			except MASTER_EXCEPTION_TUPLE as exception:
				logger.log_error("Could not insert db row.")
				self.__rollback_session(session, exception)
				return {}

			# Commit the session after fetching the inserted row
			session.commit()

		return inserted_row


	def read(
		self, table_key: str, search_params: dict, select_params: Optional[list]
	) -> Optional[dict]:
		"""
		Base method for returning an instance or row from the database.

		:param table_key: String key constant of the table to query.
		:param search_params: A dictionary of query parameters and their associated values.
		:param select_params: Optional list of db columns to return partial db rows to the service.
		:return: Dictionary of db row instance or an empty dictionary if the query returns nothing.
		"""

		# Get a 'SQL query' statement based on the supplied table_key and search_params dictionary and select_params list.
		stmt: Optional[StatementLambdaElement] = self.__get_stmt(
			table_key, search_params, select_params
		)
		# If the statement could not be made for any reason, return None and don't start a session with the db.
		if stmt is None:
			return None

		status_dictionary: dict = {}
		query_res: Optional[list[Row]] = None  # noqa

		with sessionmaker(bind=self.engine)() as session:
			try:
				# Attempt to execute the stmt and get the query result(s).
				cursor: Result = session.execute(stmt)
				query_res = cursor.all()   # noqa
			except MASTER_EXCEPTION_TUPLE as exception:
				return self.__rollback_session(session, exception)

		# If an exception did not occur, but the query result is empty, then no db rows were found.
		if not query_res:
			logger.log_info("No db rows found.")
			return status_dictionary

		# If the select_params list is empty, it means that the whole table row was selected
		# and the column name keys have been returned with the query result values.
		# If the 'select_params' list is not empty, it means that the database has
		# returned a tuple of values that have no key in the order of the 'select_params' list.
		# Use the `select_params` to map key value pairs.
		return (
			self.__format_results(query_res)
			if not select_params
			else self.__format_filtered_results(query_res, select_params)
		)

	def update(self, table_key, query_params: dict, insert_params: dict) -> bool:
		"""
		Base method for updating table rows in the database.  If the query has found multiple
		results / rows, the session will attempt to update all found db rows.

		:param table_key: String key constant of the table to query.
		:param query_params: A dictionary of parameters pertinent to specifying the query.
		:param insert_params: A dictionary of key/value pairs corresponding to db columns to be updated.
		:return: Flag indicating if the operation was a success.
		"""

		# Get a 'SQL query' statement based on the supplied table_key and search_params dictionary and select_params list.
		stmt: Optional[StatementLambdaElement] = self.__get_stmt(
			table_key, query_params, None
		)
		# If the statement could not be made for any reason, return None and don't start a session with the db.
		if stmt is None:
			return False

		is_successful_update: bool = False
		with sessionmaker(bind=self.engine)() as session:
			try:
				# Attempt to execute the stmt and find the row(s) to be updated.
				cursor: Result = session.execute(stmt)
				query_res: list[Row] = cursor.all()  # noqa
				if bool(query_res):
					# If the query has found results, map the insertion parameters to the db rows and commit the session.
					self.__map_updated_columns(query_res, insert_params)
					session.commit()
					is_successful_update = True
				else:
					# If an exception did not occur, but the query result is empty, then no db rows were found.
					logger.log_error("No db row found to update.")
			except MASTER_EXCEPTION_TUPLE as exception:
				self.__rollback_session(session, exception)

		return is_successful_update

	def delete(self, table_key, query_params: dict) -> bool:
		"""
		Base method for removing rows on a table in the database.

		:param table_key: String key constant of the table to query.
		:param query_params: A dictionary of parameters pertinent to specifying the query.
		:return: A flag indicating if the operation was a success.
		"""

		# Get a 'SQL query' statement based on the supplied table_key and search_params dictionary and select_params list.
		stmt: Optional[StatementLambdaElement] = self.__get_stmt(
			table_key, query_params, None
		)
		# If the statement could not be made for any reason, return None and don't start a session with the db.
		if stmt is None:
			return False

		is_successful_delete: bool = False

		with sessionmaker(bind=self.engine)() as session:
			try:
				# Attempt to execute the stmt and find the row(s) to be deleted.
				cursor: Result = session.execute(stmt)
				query_res: list[Row] = cursor.all()  # noqa
				if query_res:
					# If the query has found results, delete the db rows and commit the session.
					list(map(lambda res_tuple: session.delete(res_tuple[0]), query_res))
					session.commit()
					is_successful_delete = True
				else:
					# If an exception did not occur, but the query result is empty, then no db rows were found.
					logger.log_warning("No db row found to delete.")

			except MASTER_EXCEPTION_TUPLE as exception:
				self.__rollback_session(session, exception)

		return is_successful_delete

	def joined_read(
		self,
		start_table: str,
		end_table: str,
		search_params: List[dict],
		select_params: Optional[List[list]] = None
	) -> Optional[dict]:
		"""
		Method for dynamically concatenating JOINS statements between tables and executing them.

		:param start_table: String key representing the table where the JOINS statement should begin.
		:param end_table: String key representing the destination table of the JOINS statement.
		:param search_params: A dictionary of query parameters and their associated values. These
		values are associated with the start_table.
		:param select_params: Optional list of lists each containing strings representing columns
		to select.  There must be one per table traversed.
		:return: Dictionary of multiple db row instances or an empty dictionary if the query
		finds nothing.
		"""

		try:
			# Get shallow copies of the starting table and the ending (or destination) table.
			starting_table = self.__get_model_copy(start_table)
			ending_table = self.__get_model_copy(end_table)
			# Inspect the models and ensure that a relationship path exists between them.
			relationship_tuple: tuple[list, list] = self.sql_constructor.get_relationship_path(
				starting_table, ending_table
			)
			# attempt to construct a 'JOINS' statement based on the relationship path, search_params, and select_params.
			stmt = self.sql_constructor.construct_join_stmt(
				relationship_tuple, search_params, select_params
			)
		except MASTER_EXCEPTION_TUPLE as exception:
			exception_handler.get_exception_log(exception)
			return None

		with sessionmaker(bind=self.engine)() as session:
			try:
				# Attempt to execute the stmt and find the row(s) on all tables in the relationship path.
				cursor: Result = session.execute(stmt)
				query: list[Row] = cursor.fetchall()  # noqa
			except MASTER_EXCEPTION_TUPLE as exception:
				return self.__rollback_session(session, exception)
		if not bool(query):
			# If an exception did not occur, but the query result is empty, then no db rows were found.
			logger.log_info("No db rows found.")
			return {}
		# Format the results of the JOINS query so that there is no duplicate data
		# and every result is organized into a dictionary of lists of dictionary representations of each found db row.
		# If select_params are supplied for a row, use them as keys to map the query result values.
		return (
			self.__format_joins_results(query)
			if not select_params
			else self.__format_filtered_joins_results(
				query, relationship_tuple[0], select_params
			)
		)

	def count(self, table_key, query_params: dict) -> Optional[dict]:
		"""
		Base method for counting database rows based on provided query parameters.

		:param table_key: String key constant of the table to query.
		:param query_params: A dictionary of query parameters and their associated values.
		:return: A dictionary containing the count of rows that meet the criteria of the provided
		parameters or an empty dictionary if an error occurs.
		"""

		# Get a 'SQL query' statement based on the supplied table_key and search_params dictionary and select_params list.
		stmt: Optional[StatementLambdaElement] = self.__get_stmt(
			table_key, query_params, None
		)
		# If the statement could not be made for any reason, return None and don't start a session with the db.
		if stmt is None:
			return None
		# Instantiate a dictionary to hold the count of rows that meet the criteria of the provided parameters.
		count_object: dict = {
			"count": 0
		}

		with sessionmaker(bind=self.engine)() as session:
			try:
				# Attempt to execute the stmt and find the row(s) to be counted.
				cursor: Result = session.execute(stmt)
				query_res: list[Row] = cursor.all()  # noqa
				if not query_res:
					# If an exception did not occur, but the query result is empty, then no db rows were found.
					logger.log_info("No db rows found.")
				else:
					# If the query has found results, count the db rows and return the count.
					count_object["count"] += len(query_res)
			except MASTER_EXCEPTION_TUPLE as exception:
				return self.__rollback_session(session, exception)
		return count_object

	@classmethod
	def __rollback_session(
		cls, session: Session, exception: Exception = SQLAlchemyError
	) -> None:
		"""
		Convenience method for rolling back a session and
		logging the exception that caused the rollback.

		:param session: Instance of a database connection session.
		:param exception: Exception that is prompting the rollback.
		"""

		try:
			# Log the exception that prompted the imminent the rollback.
			exception_handler.get_exception_log(exception)
			# Attempt the rollback.
			session.rollback()
		except MASTER_EXCEPTION_TUPLE as rollback_exception:
			# If the rollback fails, log the exception that caused the rollback to fail.
			exception_handler.get_exception_log(rollback_exception)
			# Expire all objects in the session to prevent the bad session from being used again.
			session.expire_all()
		return None

	def __get_model_copy(self, table_key: str):
		"""
		Convenience method for retrieving and making shallow copies of orm database models from the
		Crud schema_index table.

		:param table_key: String key constant of the table to query.
		:return: A shallow copy of an orm database model or None if an invalid key was supplied.
		"""

		# Get a shallow copy of the specified db table model from the schema_index.
		current_table = self.schema_index.get(table_key)
		if current_table is None:
			# If the table can't be found, log a warning and raise a LookupError with suggestions.
			plural_hint: str = (
				"Table name might be singular."
				if table_key.lower().endswith("s")
				else "Table name might be plural."
			)
			capital_hint: str = (
				"Table name might be capitalized."
				if table_key[0].islower()
				else ""
			)
			raise LookupError(
				f"Table '{table_key}' was not found.  Suggestions: {capital_hint} {plural_hint}"
			)
		# Return a shallow copy of the specified db table model.
		return copy(current_table)

	def __get_mapped_model(self, table_key: str, req_payload: dict):
		"""
		Method for mapping a request payload to a shallow copy the specified database table model.

		:param table_key: String key constant of the table that has a new row to be added.
		:param req_payload: Dictionary of values to be mapped to the shallow copied instance of
		the specified database table model
		:return: Mapped orm database model or None if an error occurred.
		"""

		try:
			# Get a shallow copy of the specified db table model.
			new_model_instance = self.__get_model_copy(table_key)
			# Attempt to map the request payload to the model instance.
			# If the model instance has a map method, use it to map the request payload to the model instance.
			# If the model instance does not have a map method,
			# use the __blind_map method to map the request payload to the model instance using the attribute names.
			return (
				new_model_instance.map(req_payload)
				if hasattr(new_model_instance, "map")
				else self.__blind_map(new_model_instance, req_payload)
			)
		except MASTER_EXCEPTION_TUPLE as exception:
			exception_handler.get_exception_log(exception)
			return None

	@classmethod
	def __model_to_dict(cls, model) -> dict:
		"""Converts a SQLAlchemy model instance to a dictionary."""

		return {
			column.key: getattr(model, column.key)
			for column in class_mapper(model.__class__).mapped_table.c
		}

	@classmethod
	def __blind_map(cls, model_instance, req_payload: dict):
		"""
		Method for mapping a request payload to a shallow copy the specified database table model
		when that model has no defined map method.

		:param model_instance: Shallow copy of the specified db table model.
		:param req_payload: Dictionary of values to be mapped to the shallow copied instance of
		the specified database table model
		:return: Mapped orm database model or None if an error occurred.
		"""

		try:
			# Iterate through the columns of the table and check if the request payload contains.
			for column in model_instance.__table__.columns:
				# If the column is an "autoincrement primary key", skip to the next column.
				if column.primary_key and column.autoincrement:
					continue
				attribute_name: str = column.name
				# If the column is not in the request payload and is not nullable on the model, raise an AttributeError.
				if attribute_name not in req_payload and not column.nullable:
					raise AttributeError(
						f"The `{model_instance.__name__}` table requires the a value for the '{attribute_name}' column to create a new row."
					)
				# If the column is in the request payload, check if the value is of the correct type.
				if attribute_name in req_payload:
					if req_payload[attribute_name] is None and column.nullable:
						continue
					if not isinstance(req_payload[attribute_name], column.type.python_type):
						raise TypeError(
							f"Attribute '{column.name}' must be of type '{type(column.type)}'."
						)
			# If the request payload contains all the required values, map the request payload to the model instance.
			mapped_model = model_instance(**req_payload)
			return mapped_model

		except MASTER_EXCEPTION_TUPLE as exception:
			exception_handler.get_exception_log(exception)
			return None

	def __get_stmt(
		self, table_key: str, query_params: dict, select_params: Optional[list]
	) -> Optional[StatementLambdaElement]:
		"""
		Convenience method for getting a 'SQL query' statement based
		on the supplied table_key and query_params dictionary.

		:param table_key: String key constant of the table to query.
		:param query_params: A dictionary of query parameters and their associated values.
		:param select_params: Optional list of db columns to return partial db rows to the service.
		:return: A SQL query statement or None if an error occurred.
		"""

		stmt: Optional[StatementLambdaElement] = None

		try:
			# Get a shallow copy of the specified db table model.
			table = self.__get_model_copy(table_key)
			# Attempt to get a 'SQL query' statement based on the supplied table model,
			# `query_params` dictionary and `select_params` list.
			stmt = self.sql_constructor.get_single_table_query_stmt(
				table, query_params, select_params
			)
		except MASTER_EXCEPTION_TUPLE as exception:
			exception_handler.get_exception_log(exception)
		# Return the 'SQL query' statement or None if an error occurred.
		return stmt

	def __format_results(self, query_res: list[Row]) -> dict:
		"""
		Method for type-casting SQLAlchemy objects into more usable dictionary objects.

		:param query_res: A list of SQLAlchemy query result object(s).
		:return: Dictionary representation of a SQLAlchemy query result object with unnecessary
		fields stripped out, or a dictionary of lists each containing dictionary representations of SQLAlchemy
		query result objects if the db returned multiple rows.
		"""

		result_rows_list: list = []
		# Iterate through the list of Rows.
		for res_tuple in query_res:
			# Iterate through the list of `Result Tuple` objects.
			for res in res_tuple:
				# Cast the `Result Tuple` object to a dictionary and remove metadata fields.
				res_dict = self.__remove_sqlalchemy_metadata(res.__dict__)
				# If the db returned only one row, return the dictionary representation of the row.
				if len(query_res) == 1:
					# Return the dictionary representation of the row.
					return res_dict
				# If more than one row was returned, append the dictionary representation of the row to a list.
				result_rows_list.append(res_dict)
		# Return the list of dictionary representations of the rows.
		return {"result": result_rows_list}

	@classmethod
	def __format_filtered_results(cls, query_res: list, select_params: list) -> dict:
		"""
		Convenience method for type-casting SQLAlchemy objects into dictionaries to be consumed
		throughout the application.

		:param query_res: A list of SQLAlchemy query result object(s).
		:return: Dictionary representation of a SQLAlchemy query result object with unnecessary
		fields stripped out.
		"""

		formatted_results: list = []
		# Iterate over the list of `Result Tuple` objects.
		for query_res_tuple in query_res:
			# Use the select_params list to map the query result values to the correct keys.
			single_formatted_result: dict = {
				key: value for key, value in zip(select_params, query_res_tuple)
				if key not in ("_sa_instance_state", "sa_instance_state")
			}
			# If the db returned only one row, return the dictionary representation of the row.
			if len(query_res) == 1:
				return single_formatted_result
			# If more than one row was returned, append the dictionary representation of the row to a list.
			formatted_results.append(single_formatted_result)
		# Return the list of dictionary representations of the rows.
		return {"result": formatted_results}

	@classmethod
	def __map_updated_columns(cls, query_res: List[Row], insert_params: dict):
		"""
		Convenience method that maps insertion parameters per table row and column to be committed by the Session.

		:param query_res: A SQLAlchemy result object from the db.
		:param insert_params: A mapped dictionary of parameters to update within the db.
		"""

		# Iterate through the list of Rows to be updated.
		for (current_db_row,) in query_res:
			# Create a memo to keep track of the attributes that have been updated.
			attribute_memo: set = set()
			# Iterate through the insert_params dictionary.
			for key, value in insert_params.items():
				# Don't perform the update unless the current attribute's new value
				# is different from the old value, and it has not yet been updated.
				if (
					hasattr(current_db_row, key)
					and getattr(current_db_row, key) != value
					and key not in attribute_memo
				):
					setattr(current_db_row, key, value)
				# Add the attribute to the memo to prevent it from being updated again.
				attribute_memo.add(key)

	@classmethod
	def __format_joins_results(cls, query_res: list) -> dict:
		"""
		Method that formats results of a 'JOINS query' so that there is no duplicate data and every
		result is organized into a dictionary of lists of dictionary representations of each found
		db row.

		:param query_res: List of tuples that each contain SQLAlchemy result objects.
		:return: Normalized dictionary of lists containing no duplicate data.
		"""

		table_dict: dict = {}
		memo: set = set()
		# Iterate through the list of `Result Tuple` objects.
		for row_res in query_res:
			# Iterate through the list of `Result` objects.
			for model in row_res:
				table_name = type(model).__name__
				# Check if the table has already been encountered on a previous iteration.
				if table_name not in table_dict:
					# If the table has not been encountered, add it to the
					# `table_dict` create an empty list as its value.
					table_dict[table_name] = []
				# If the table has not been encountered, add it to the set of encountered tables.
				if model not in memo:
					memo.add(model)
					# Append the dictionary representation of the row to the list of the table in the `table_dict`.
					table_dict[table_name].append(
						{
							k: v
							for k, v in model.__dict__.items()
							if k != ("_sa_instance_state" or "sa_instance_state")
						}
					)
		# Return the `table_dict` dictionary of lists containing no duplicate data.
		return table_dict

	def __format_filtered_joins_results(
		self, query_res: list, relationship_list: list, select_params: list
	):
		"""
		Method that formats results of a 'JOINS query'.
		Ensure there is no duplicate data and every result is organized into a dictionary
		of lists of dictionary representations of each found db row when a filter has been applied to any table.

		:param query_res: List of tuples that each contain SQLAlchemy result objects and values returned from columns.
		:param relationship_list: List of SQLAlchemy table model objects that are related to each other.
		:param select_params: List of lists each containing strings representing columns to select.
		:return: Normalized dictionary of lists containing no duplicate data.
		"""

		formatted_results: dict = {}
		# Iterate through the list of `Result Tuple` objects.
		for joined_query_result in query_res:
			# Iterate through the list of `Result` objects.
			for i, param_list in enumerate(select_params):
				# Check if the result is a full table select or a filtered select.
				is_full_table_select: bool = len(param_list) < 1
				# Get the name of the table that the current `Result` object is from.
				current_table: str = relationship_list[i].__name__
				# Get the attributes of the current `Result` object or values returned from columns.
				current_table_attributes = (
					(joined_query_result[: len(param_list)])
					if not is_full_table_select
					else (joined_query_result[0])
				)
				# Format the `Results object` into a dictionary and remove unnecessary metadata.
				formatted_result_dict: dict = (
					self.__format_filtered_results(
						[current_table_attributes], param_list
					)
					if not is_full_table_select
					else self.__remove_sqlalchemy_metadata(current_table_attributes.__dict__)
				)
				# Check if the table has already been encountered on a previous iteration.
				if current_table not in formatted_results:
					# If the table has not been encountered, add it to the `formatted_results` dictionary
					formatted_results[current_table] = [formatted_result_dict]
				# If the table has been encountered, append the dictionary representation
				# of the row to the list of the table if the row is not a duplicate.
				elif (
					current_table in formatted_results and
					formatted_result_dict not in formatted_results[current_table]
				):
					formatted_results[current_table].append(formatted_result_dict)
				# Mutate the `joined_query_result` to remove the values that have already been mapped.
				joined_query_result = (
					(joined_query_result[len(param_list):])
					if not is_full_table_select else (joined_query_result[1:])
				)
		return formatted_results

	@classmethod
	def __remove_sqlalchemy_metadata(cls, result_dict: dict) -> dict:
		"""
		Method for removing unnecessary SQLAlchemy metadata from a dictionary, so it isn't returned to the service.

		:param result_dict: Dictionary representation of a SQLAlchemy query result object.
		:return: Sanitized dictionary representation of a SQLAlchemy query result object.
		"""
		# Remove the metadata fields from the dictionary.
		result_dict.pop("_sa_instance_state", None)
		result_dict.pop("sa_instance_state", None)
		# Return the sanitized dictionary representation of a SQLAlchemy query result object.
		return result_dict
