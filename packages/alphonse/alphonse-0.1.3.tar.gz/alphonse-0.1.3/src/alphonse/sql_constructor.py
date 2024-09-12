# alphonse/sql_constructor.py

""" SQLConstructor definition. """

import operator
from typing import Any, List, NoReturn, Optional, Tuple, Union

from solidipy.exceptions import MASTER_EXCEPTION_TUPLE
from sqlalchemy import Column, lambda_stmt, or_
from sqlalchemy.future import select
from sqlalchemy.orm import Mapper, class_mapper
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql import StatementLambdaElement, null

try:
	from src.alphonse.utilities import exception_handler
except ImportError:
	from alphonse.utilities import exception_handler


class SQLConstructor:
	""" Class for generating dynamic SQL statements to be executed in a db session. """

	literal_operator_dict: dict = {
		"==": operator.eq,
		"!=": operator.ne,
		"<": operator.lt,
		"<=": operator.le,
		">": operator.gt,
		">=": operator.ge,
	}
	""" Dictionary of equality operators used in the construction of WHERE clauses. """

	def __init__(self) -> NoReturn:
		""" SQLConstructor initializer. """

	def get_single_table_query_stmt(
		self, table, search_params: dict, select_params: Optional[list]
	) -> StatementLambdaElement:
		"""
		Method for constructing query statements in SQLAlchemy to be executed by the Crud class.

		:param table: Instance of a database table model.
		:param search_params: Dictionary of keys corresponding to columns to search and values
		corresponding to the column values to search for.
		:param select_params: List of columns to select.
		Returns all table columns if the list is empty.
		:return resulting_query: A SQLAlchemy query object or None if an exception occurs.
		"""

		# Generate an initial SELECT statement to build the rest of the `SQL statement` off of.
		stmt, distinct_cols = self.__get_select(
			table, select_params
		)
		if stmt is not None:
			# If the statement is not None, accumulate a `WHERE clause` for each key in the `query_params` dictionary.
			stmt = self.__get_single_table_where_clause(
				table, search_params, stmt
			)
		# Order results by the primary key of the table (if the table has one)
		# & return the accumulated StatementLambdaElement SQL statement.
		if stmt is not None and hasattr(table, "id") and not distinct_cols:
			stmt += lambda s: s.order_by(table.id)
		return stmt

	def __get_select(
		self, table, select_params: Optional[list[str]]
	) -> tuple[StatementLambdaElement, list[InstrumentedAttribute]]:
		"""
		Method that constructs and returns a dynamic 'SELECT' portion of a 'SQL statement'.

		:param table: Instance of a database table model.
		:param select_params: Optional parameter used to specify if specific table columns should
		be selected.
		If it is not provided, all table columns are selected.
		:return: A StatementLambdaElement object that represents the `SELECT` of a SQL statement.
		"""

		# Instantiate a list to store the columns that will be selected distinctly.
		distinct_columns_list: list = []
		# If there are no `select_params` it means the whole table row should be selected.
		if not select_params:
			# Generate a `SELECT` statement that selects all columns from the table.
			stmt: StatementLambdaElement = lambda_stmt(lambda: select(table))
			# Return the `SELECT` statement and an empty list of distinct columns.
			return stmt, distinct_columns_list
		# If there are `select_params`, then the columns must be verified and
		# enumerated into two lists: normal columns and distinct columns.
		column_list, distinct_columns_list = self.__map_select_columns(
			table, select_params
		)
		if distinct_columns_list:
			# If there are distinct columns, generate a `SELECT` statement that selects them.
			select_stmt = select(*distinct_columns_list).select_from(table)
			for column in distinct_columns_list:
				select_stmt = select_stmt.distinct(column)
			# If there are normal columns, add them to the `SELECT` statement.
			if column_list:
				select_stmt = select_stmt.add_columns(*column_list)
			# Return the `SELECT` statement and the list of distinct columns.
			return lambda_stmt(lambda: select_stmt), distinct_columns_list
		else:
			# If there are no distinct columns, generate a `SELECT` statement that selects the normal columns only.
			# If `select_params` is empty at this point, it means they were invalid, so the whole table will be selected.
			return (
				(
					lambda_stmt(lambda: select(*column_list).select_from(table)),
					column_list,
				)
				if column_list
				else (lambda_stmt(lambda: select(table)), distinct_columns_list)
			)

	@classmethod
	def __map_select_columns(cls, table, select_params: list) -> tuple[list, list]:
		"""
		Method that dynamically maps a list of column names to an SQLAlchemy ORM database model.

		:param table: An uninstantiated instance of a SQLAlchemy ORM database model.
		:param select_params: A list of strings representing column names on the table.
		:return: A formatted list of strings that will be used to produce a more specific dynamic
		SELECT statement in the parent method.
		"""

		mapped_column_list: list = []
		distinct_columns_list: list = []
		valid_select_params: list = []
		# Iterate over the `select_params` list and map the column names to the table.
		for i, column_name in enumerate(select_params):
			# If the column name starts with a '%' character, it is invalid.
			if column_name and column_name[0] == "%":
				raise AttributeError(
					f"The select param `{column_name}` is invalid because the '%' operator must be at the end of the key.  "
					)
			# If the column name ends with a '%' character, it is a distinct column.
			if column_name.endswith("%"):
				# Remove the '%' character from the column name.
				column_name = column_name[:-1]
				# Append the column name to the list of distinct columns.
				select_params[i] = column_name
				# Append the column to the list of distinct columns.
				distinct_columns_list.append(getattr(table, column_name))
			# If the column name is invalid, raise an AttributeError.
			if not hasattr(table, column_name):
				raise AttributeError(f"'The `{table.__name__}` table has no column called `{column_name}'.")
			# Append the column to the list of mapped columns.
			mapped_column_list.append(getattr(table, column_name))
			# Append the column name to the list of valid select params.
			valid_select_params.append(column_name)
		# Clear the `select_params` list and append the valid select params to it.
		select_params.clear()
		select_params.extend(valid_select_params)
		# Return the list of mapped columns and the list of distinct columns.
		return mapped_column_list, distinct_columns_list

	def __get_single_table_where_clause(
		self, table, search_params: Union[dict, List[dict]], stmt: StatementLambdaElement
	):
		"""
		Method that add WHERE clauses to an existing StatementLambdaElement object SQL statement
		and returns the statement.

		:param table: An uninstantiated instance of a SQLAlchemy ORM database mode that the clause
		will be applied to.
		:param search_params: Mapped dictionary of filter parameters.
		:param stmt:  A StatementLambdaElement SQL statement that is in progress.
		:return: A StatementLambdaElement SQL statement with an added WHERE clause.
		"""

		# Iterate over the `search_params` dictionary.
		for i, (attr, val) in enumerate(search_params.items()):
			try:
				# Determine the equality operator, attribute, and value
				# to be used in the construction of the WHERE clause.
				equality_operator, attribute = self.__determine_equality_type(attr)
				# Add a WHERE clause to the SQL statement.
				stmt = self.__get_where_clause(
					table,
					attribute,
					equality_operator,
					val,
					stmt,
				)
			except MASTER_EXCEPTION_TUPLE as exception:
				# If an exception occurs, log it and return None to halt the construction of the SQL statement.
				exception_handler.get_exception_log(exception)
				return None
		# Return the `SQL statement` with the added `WHERE clause`.
		return stmt

	@classmethod
	def __validate_column_and_value(
		cls, column: str, value, table
	) -> InstrumentedAttribute:
		"""
		Method that validates a column's existence on a db table and its datatype, then returns an
		InstrumentedAttribute to be used in the construction of a WHERE clause.

		:param column: String representation of a database table's column.
		:param table: An uninstantiated instance of a SQLAlchemy ORM database model that the clause
		will be applied to.
		:return: InstrumentedAttribute to be used in the construction of a WHERE clause.
		"""

		error_msg: str = ""
		# Get the mapper for the table and validate the column and value.
		mapper: Mapper = class_mapper(table)
		attribute: InstrumentedAttribute
		# If the column is in the mapper's columns, validate the column and value.
		if column in mapper.columns:
			# Get the column and value from the mapper.
			mapper_column: Column = mapper.columns[column]
			# Get the column's datatype.
			python_type: type = mapper_column.type.python_type
			# Get the column's nullable status.
			is_nullable: bool = mapper_column.nullable
			# If the value is None and the column is not nullable, add to the error message.
			if value is None and not is_nullable:
				error_msg += f"The value supplied to the '{column}' column on the table `{table.__tablename__.capitalize()}` cannot be null."
			# If the value's type is not the column's type, add to the error message.
			if value is not None and type(value) is not python_type:
				error_msg += f"The value supplied to the '{column}' column on the table `{table.__tablename__}` should be a type of `{python_type.__name__}`, but {value} was supplied."
			if error_msg:
				# If there is an error message, raise a TypeError.
				raise TypeError(error_msg)
		else:
			# If the value is not in the mapper's columns, add to the error message.
			error_msg += (
				f"Db table '{table.__name__}' has no colum called '{column}'."
			)
			# If the first character of the column is not a letter, add to the error message.
			if not column[0].isalpha():
				error_msg += "  Equality operators must be appended to the -1 index of the key to be valid."
		if error_msg:
			# If there is an error message, raise an AttributeError.
			raise AttributeError(error_msg)
		# If there are no errors, return the column's attribute.
		attribute = getattr(table, column)
		return attribute

	def __determine_equality_type(self, column_name: str) -> tuple[str, str]:
		"""
		Method that determines if a column name has an equality operator concatenated into it.

		:param column_name: String representation of a database table's column.
		:return: The appropriate equality operator depends on the input string.
		"""

		equality_operator: str = ""

		# If the last character of the column name is a letter,
		# then no equality operator was supplied.
		# Use the '==' operator.
		if column_name[-1].isalpha():
			equality_operator = "=="
		else:
			# If the last character of the column name is not a letter, iterate over the string in reverse.
			for i in range(len(column_name) - 1, -1, -1):
				# Check if the next character is a letter.
				next_char: str = column_name[i - 1]
				if next_char.isalpha():
					# If the next character is a letter, the equality operator is
					# the substring from the next character to the end of the string.
					equality_operator = column_name[i:]
					column_name = column_name[: -len(equality_operator)]
					# End the loop if the equality operator is found.
					break
				# If the next character is the first character of the string, the equality operator is the whole string.
				if column_name.index(next_char) == 0:
					equality_operator = column_name
		# If an equality operator was found, but isn't in the `literal_operator_dict` raise an AttributeError.
		if equality_operator and (equality_operator not in self.literal_operator_dict):
			raise AttributeError(f"'{equality_operator}' operator supplied to the '{column_name}' column is invalid.")
		# Return the equality operator and the column name.
		return equality_operator, column_name

	def __get_where_clause(
		self,
		table,
		attribute: str,
		str_operator: str,
		column_value: Optional[Any],
		stmt: StatementLambdaElement,
	):
		"""
		Method that concatenates new WHERE clauses on to a supplied StatementLambdaElement.

		:param table: An uninstantiated instance of a SQLAlchemy ORM database model that the clause
		will be applied to.
		:param attribute: Column of the table that the WHERE clause will be applied to.
		:param str_operator: String of an equality operator used in the WHERE clause.
		:param column_value: Value of the column in question.
		:param stmt:  A StatementLambdaElement SQL statement that is in progress.
		:return: StatementLambdaElement with added WHERE clause.
		"""

		col: InstrumentedAttribute
		# Get the appropriate equality operator for the column and value.
		literal_operator: operator = self.literal_operator_dict.get(str_operator)
		# If the column value is a list and the column is not a list, and the list has one element, parse the element.
		if (
			isinstance(column_value, list)
			and not table.__table__.columns[attribute].type == list
			and len(column_value) == 1
		):
			column_value = column_value[0]
		# If the column value is a list and the column is not a list,
		# and the list has more than one element, parse the list of values.
		if (
			isinstance(column_value, list) and
			not table.__table__.columns[attribute].type == list
		):
			# If they have given a list of values for the attribute, parse the whole list:
			return self.__parse_multiple_attributes_for_a_single_column(
				table,
				attribute,
				literal_operator,
				column_value,
				stmt,
			)
		# If the column value is a single value, validate the value.
		col: Optional[InstrumentedAttribute] = self.__validate_column_and_value(
			attribute, column_value, table
		)
		# If the column value is None, set it to `null` so the PostgresSQL database can handle it.
		if column_value is None:
			column_value = null()
		# Concatenate the literal operator and the column value to a partial `WHERE clause`.
		literal_operator = literal_operator(col, column_value)
		# Concatenate the partial `WHERE clause` into a full `WHERE cause` and append it to the `SQL statement`.
		stmt += lambda s=stmt, op=literal_operator: s.where(op)
		# Return the `SQL statement` with the added `WHERE clause`.
		return stmt

	def __parse_multiple_attributes_for_a_single_column(
		self,
		table,
		attribute: str,
		literal_operator: operator,
		val: list,
		stmt: StatementLambdaElement,
	) -> Optional[StatementLambdaElement]:
		"""
		Method that concatenates new WHERE clauses on to a supplied StatementLambdaElement when a
		single table column needs to have multiple values evaluated.

		:param table: An uninstantiated instance of a SQLAlchemy ORM database model that the clause
		will be applied to.
		:param attribute: Column of the table that the WHERE clauses will apply to.
		:param literal_operator: A python equality operator used in the WHERE clause.
		:param val: List of values that will be compared to the column in question.
		:param stmt:  A StatementLambdaElement SQL statement that is in progress.
		:return: StatementLambdaElement with added WHERE clause.
		"""

		# Get the name of the table.
		current_table: str = table.__tablename__
		if literal_operator == operator.eq:
			# If the equality operator is '==', validate the list of values.
			self.__validate_eq_in_where_list(val, current_table)
			# If the list of values is valid, concatenate an `or WHERE clause` for each value.
			or_list = [
				literal_operator(
					self.__validate_column_and_value(attribute, list_item, table),
					null() if list_item is None else list_item,
				)
				for list_item in val
			]
			# Concatenate all `or WHERE clauses` into a full `WHERE cause` and append it to the `SQL statement`.
			stmt += lambda s=stmt: s.where(or_(*or_list))
		else:
			# If the equality operator is '!=', validate the list of values.
			self.__validate_ne_in_where_list(current_table, val)
			# If the list of values is valid, concatenate an `and WHERE clause` for each value.
			and_list: list = [
				literal_operator(
					self.__validate_column_and_value(attribute, list_item, table),
					null() if list_item is None else list_item,
				)
				for list_item in val
			]
			# Concatenate all `and WHERE clauses` into a full `WHERE cause` and append it to the `SQL statement`.
			stmt += lambda s=stmt: s.where(*and_list)
		# Return the `SQL statement` with the added `WHERE clause(s)`.
		return stmt

	@classmethod
	def __validate_eq_in_where_list(
		cls,
		val: list,
		current_table: str,
	):
		"""
		Helper method for evaluating equality in a 'WHERE' SQL clause.

		:param val: List of values associated with a singed table column / attribute.
		:param: current_table: String used in error handling and logging.
		:param: current_statement: String used in error handling and logging.
		:return: None if the supplied list is valid.
		Returns the statement if the clause should be skipped.
		"""

		# If the list of values is a set of True, False, and None, raise a ValueError.
		if set(val) == {True, False, None}:
			raise ValueError(f"Bad search params: {current_table} != {val}")

	@classmethod
	def __validate_ne_in_where_list(cls, table: str, val: list):
		"""
		Helper method for evaluating inequality in a 'WHERE' SQL clause.

		:param table: The name of the table.
		:param val: List of values associated with a singed table column / attribute.
		:return: None if the supplied list is valid.
		Returns the statement if the clause should be skipped.
		"""

		# If the list of values is a set of True, False, and None, raise a ValueError.
		if set(val) == {True, False, None} or set(val) == {True, False}:
			raise ValueError(f"Bad search params: {table} != {val}")

	def construct_join_stmt(
		self,
		relationship_tuple: tuple[list, list],
		search_params: List[dict],
		select_params: Optional[List[list]]
	) -> StatementLambdaElement:
		"""
		Method that conducts the construction of a dynamic JOINS statements and returns them to be
		executed.

		:param relationship_tuple: A tuple of two lists containing the relationships between the tables.
		:param search_params: Either a single dictionary of query parameters and their associated
		values, These values are associated with the starting_table or a list of these dictionaries
		each corresponding to a specific table traversed in the construction of the JOINS statement.
		:param select_params: Optional list of lists each containing strings representing columns
		to select.
		There must be one per table traversed.
		:return: A 'JOINS' statement represented as a StatementLambdaElement object.
		"""

		__ID: str = "id"

		relationship_list: list = relationship_tuple[0]
		#  If there are `select_params`, verify that the length of the list is equal to the length of the `relationship_list`.
		if select_params is not None and len(select_params) != len(relationship_list):
			# If the select_params are longer than the relationship_list, remove the extra elements.
			while len(select_params) > len(relationship_list):
				select_params.pop()
			# If the select_params are shorter than the relationship_list, append empty lists to the select_params list.
			while len(select_params) < len(relationship_list):
				select_params.append([])
		# Generate a `SELECT` statement to build the rest of the `SQL statement` off of.
		select_stmt, distinct_cols = self.__get_joins_select_stmt(
			relationship_list, select_params
		)
		# Attempt to generate and add a `WHERE clause` for the `SQL statement`.
		stmt: StatementLambdaElement = self.__get_joins_where_statement(
			relationship_list, search_params, select_stmt
		)

		if stmt is None:
			# If the `WHERE clause` could not be generated, raise a ValueError.
			raise ValueError("Couldn't create a `WHERE` clause for SQL statement.")

		# If the `WHERE clause` was generated, add the `JOINS` clauses to the `SQL statement`.
		stmt = self.__add_joins(relationship_tuple, stmt)

		# Order results by the primary key of the table (if the table has one) or the distinct columns if there are any.
		return (
			stmt.order_by(__ID) if not distinct_cols else stmt.order_by(*distinct_cols)
		)

	def __get_joins_select_stmt(
		self, relationships: list, select_params: Optional[list]
	) -> tuple:
		"""
		TODO
		:param relationships:
		:param select_params:
		:return:
		"""

		# If there are no `select_params`, generate a `SELECT` statement that selects all columns from the table.
		if select_params is None:
			return lambda_stmt(lambda relations=relationships: select(*relations)), []  # noqa

		column_list: list = []
		distinct_column_list: list = []
		# Iterate over the relationships and select_params lists.
		for i in range(len(relationships)):
			relationship = relationships[i]
			current_select_params = select_params[i]
			# If the currently selected list of `select_params` has value
			if current_select_params:
				# Map the columns to the table and append them to the column list and distinct column list.
				mapped_column_list, distinct_cols = self.__map_select_columns(
					relationship, current_select_params
				)
				column_list = [*column_list, *mapped_column_list]
				distinct_column_list = [*distinct_column_list, *distinct_cols]
			else:
				# If the currently selected list of `select_params` has no value, append the table to the column list.
				column_list = [*column_list, relationship]

		if distinct_column_list:
			# If there are distinct columns, generate a `SELECT` statement that selects them.
			select_stmt = select(*distinct_column_list).select_from(*relationships)
			for column in distinct_column_list:
				# Add a `DISTINCT clause` to the `SELECT statement` for each distinct column.
				select_stmt = select_stmt.distinct(column)
			select_stmt = select_stmt.add_columns(*column_list)
			return lambda_stmt(lambda: select_stmt), distinct_column_list

		# If the column list is populated, it means that there are multiple tables to select from.
		# Generate a `SELECT` statement that selects the validated columns.
		if column_list:
			return (
				lambda_stmt(
					lambda relations=relationships, col_list=column_list: select(*col_list).select_from(*relations)
					# noqa
				),
				distinct_column_list,
			)

	def __get_joins_where_statement(
		self,
		relationship_list: list,
		search_param_list: list[dict],
		stmt: StatementLambdaElement,
	):
		"""
		Method that adds multiple WHERE clauses to an existing StatementLambdaElement object SQL
		statement and returns the statement.

		:param relationship_list: A list of uninstantiated instances of a SQLAlchemy ORM database
		models that WHERE clauses will be applied to.
		:param search_param_list: A list of mapped dictionary of filter parameters.
		:param stmt:  A StatementLambdaElement SQL statement that is in progress.
		:return: A StatementLambdaElement SQL statement with an added WHERE clause.
		"""

		# Iterate over the `relationship_list` and `search_param_list` lists.
		for i in range(len(relationship_list)):
			# If the current index is equal to the length of the `search_param_list`, break the loop.
			if i == len(search_param_list):
				break
			current_param_dict: dict = search_param_list[i]
			# If no `search_params` were supplied for the current table,
			# continue to the next iteration and used foreign keys to find the table to join.
			if not current_param_dict:
				continue
			# Add a `WHERE clause` to the `SQL statement` for the current table.
			stmt: StatementLambdaElement = self.__get_single_table_where_clause(
				relationship_list[i], current_param_dict, stmt
			)
			# If the `WHERE clause` could not be generated, return None to halt the construction of the SQL statement.
			if stmt is None:
				break
		# Return the `SQL statement` with the added `WHERE clause`.
		return stmt

	@classmethod
	def __add_joins(
		cls, relationship_tuple: tuple[list, list], stmt: StatementLambdaElement
	):
		"""
		Method that iterates over a list of relationships and concatenates JOINS clauses onto an
		in progress SQL statement.

		:param relationship_tuple: A tuple of two lists.
		The first is an ordered list of db models.
		The second is an ordered list of relationships between the tables in the first list,
		in the same order.
		:param stmt: A StatementLambdaElement SQL statement that is in progress.
		:return: StatementLambdaElement SQL statement with SELECT, WHERE, and JOINS clauses.
		"""

		# List of tables
		relationship_list: list = relationship_tuple[0]
		# List of table foreign keys
		primary_joins_list: list = relationship_tuple[1]
		# Iterate over the `relationship_list` and `primary_joins_list` lists.
		for i in range(len(relationship_list) - 1):
			next_table = relationship_list[i + 1]
			primary_join = primary_joins_list[i]
			# Concatenate a `JOIN clause` to the `SQL statement` for the current table and the next table.
			stmt = stmt.join(next_table, primary_join)
		# Return the `SQL statement` with the added `JOINS clauses`.
		return stmt

	def get_relationship_path(
		self, starting_table, ending_table
	) -> Optional[Tuple[list, list]]:
		"""
		Method that takes in a starting and ending table and dynamically traverses a series of
		relational db tables by foreign key.

		:param starting_table: The table where the traversal will begin.
		:param ending_table: The destination table of the traversal.
		:return: A tuple of two lists.
		The first is an ordered list of db models.
		The second is an ordered list of relationships between the tables in the first list,
		in the same order.
		"""
		try:
			# Establish the current model as the starting table.
			current_model = starting_table
			# Create a list to store the path of relationships between the starting and ending tables.
			path: list = [current_model]
			# Create a list to store the primary joins (foreign keys) between the current table and the next.
			primary_joins: list = []
			# Create a set to store the visited tables.
			visited: set = {current_model}
			# While the path list has length, iterate over the relationships of the current model.
			while path:
				# Get the current model from the path list.
				current_model = path[-1]
				# If the current model is the ending table, return the path and primary joins.
				if current_model == ending_table:
					return path, primary_joins
				# Iterate over the relationships of the current model.
				for rel in class_mapper(current_model).relationships:
					# Establish the related model for reference.
					related_model = rel.mapper.class_
					# If the related model is not in the `visited` set
					if related_model not in visited:
						# Use the local and remote columns to find the primary join between the current table and the next model to check.
						primary_join = self.__get_local_remote_cols(
							current_model, related_model
						)
						if primary_join is not None:
							# If the primary join exists, append it to the primary joins list.
							primary_joins.append(primary_join)
							# Append the related model to the path list and to the visited set.
							path.append(related_model)
							visited.add(related_model)
							# Break the loop to check the next table.
							break
				else:
					# If the `current_model` is not the `ending_table`,
					# pop the current model from the path list to check the next table.
					path.pop()
					# If there are no primary joins, raise a ValueError.
					if not primary_joins:
						raise ValueError(
							f"No relationship path found between {current_model.__name__} and {path[-1].__name__}."
						)
					# If there are primary joins, pop the last primary join from the primary joins list to check the next table.
					primary_joins.pop()
		except MASTER_EXCEPTION_TUPLE as exc:
			exception_handler.get_exception_log(exc)
			return None

	@classmethod
	def __get_local_remote_cols(cls, current_table, next_table):
		"""
		Method that gets the local and remote columns between the current and next db table used
		to concatenate a JOIN statement.

		:param current_table: The currently inspected database table.
		:param next_table: The next table to be traversed.
		:return: SQLAlchemy RelationshipProperty object.
		"""

		# Get the mapper for the current table.
		current_mapper = class_mapper(current_table)
		# Iterate over the relationships of the current table.
		for relation in current_mapper.relationships:
			if relation.mapper.class_ == next_table:
				# If the related model is the next table, check for the primary join.
				relationship: RelationshipProperty = relation
				if hasattr(relationship, "primaryjoin"):
					# If the primary join exists, return it.
					return relationship.primaryjoin
