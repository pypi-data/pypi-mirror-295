# alphonse/utilities.py

"""
Module for instantiating the logger and exception handler singleton objects used throughout the project.
"""

from functools import wraps
from inspect import BoundArguments, signature
from logging import getLogger
from typing import Any, Callable, List, NoReturn, Optional, TypeVar, Union

try:
	from src.solidipy.exceptions import ExceptionHandler
	from src.solidipy.logging_utility import BaseLogger
except ImportError:
	from solidipy.exceptions import ExceptionHandler
	from solidipy.logging_utility import BaseLogger


logger: BaseLogger = BaseLogger(getLogger("elric_logger"))
""" Logger instance for the project. """

exception_handler: ExceptionHandler = ExceptionHandler(logger)
""" Exception handler instance for the project. """

wrapped_func = TypeVar("wrapped_func", bound=Callable[..., Any])
"""
TypeVar used for a wrapped function.
"""


def validate_params() -> wrapped_func:
	"""
	This is a wrapped function to be used as a decorator on db_manager
	methods to ensure that all parameters are populated and not empty.
	"""

	def inspect_params(func: wrapped_func) -> wrapped_func:
		"""
		This is a wrapped function to be returned by the decorator.

		:param func: The wrapped function.
		:return: The wrapped function.
		"""

		sig = signature(func)
		params = sig.parameters

		@wraps(func)
		def wrapped(*args, **kwargs):
			"""
			A wrapped function that houses the validation logic.

			:return: Args and Kwargs for the wrapped function.
			"""

			bound: BoundArguments = sig.bind_partial(*args, **kwargs)
			missing: list = [
				name for name, param in params.items()
				if name not in bound.arguments and param.default is param.empty
			]
			empty: list = [
				name for name, value in bound.arguments.items()
				if not value and name in params and params[name].default is params[name].empty
			]
			try:
				if missing:
					if len(missing) == 1:
						raise AttributeError(
							f"The argument `{missing[0]}` supplied to `{func.__name__}()` is missing."
						)
					if len(missing) == 2:
						raise ValueError(
							f"The arguments `{missing[0]}` and `{missing[-1]}` supplied to `{func.__name__}()` are missing."
						)
					else:
						raise AttributeError(
							f"The arguments `{', '.join(missing[:-1])}`, and `{missing[-1]}` supplied to `{func.__name__}()` are missing."
						)
				if empty:
					if len(empty) == 1:
						raise ValueError(
							f"The argument `{empty[0]}` supplied to `{func.__name__}()` cannot be empty."
						)
					if len(empty) == 2:
						raise ValueError(
							f"The arguments `{empty[0]}` and `{empty[1]}` supplied to `{func.__name__}()` cannot be empty."
						)
					else:
						raise ValueError(
							f"The arguments `{', '.join(empty[:-1])}`, and `{empty[-1]}` supplied to `{func.__name__}()` cannot be empty."
						)
			except (AttributeError, ValueError) as exc:
				print(exc)
				exception_handler.get_exception_log(exc)
				return None

			# Combine args and kwargs into a single dictionary
			combined_kwargs = {**kwargs, **dict(zip(sig.parameters, args))}

			# Reassign kwargs to the combined dictionary
			kwargs = combined_kwargs

			return func(**kwargs)

		return wrapped

	return inspect_params


def validate_joins_params() -> wrapped_func:
	"""
	This is a wrapped function to be used as a decorator on db_manager.joined_read()
	to ensure that all parameters are populated and not empty.
	"""

	def inspect_params(func: wrapped_func) -> wrapped_func:
		"""
		This is a wrapped function to be returned by the decorator.

		:param func: The wrapped function.
		:return: The wrapped function.
		"""

		def validate_single_table_params(single_table_params: dict) -> NoReturn:
			"""
			Validates the single dict of search parameters supplied to the `joined_read()` method.

			:param single_table_params: Single dict of search parameters to validate.
			"""

			for key, value in single_table_params.items():
				if value is not None and not value:
					raise AttributeError(
						f"Empty value supplied for key `{key}` in the `search_params` dictionary.  Use `None` to indicate an null value."
					)

		def validate_search_params(search_params: Union[dict, List[dict]]) -> Union[dict, List[dict]]:
			"""
			Validates all search parameters supplied to the `joined_read()` method.

			:param search_params: List of search parameters to validate.
			:return: Validated search parameters.
			"""

			if type(search_params) is list:
				for single_table_params in search_params:
					validate_single_table_params(single_table_params)

			if type(search_params) is dict:
				validate_single_table_params(search_params)
				search_params = [search_params]

			return search_params

		def validate_select_params(select_params: Union[dict, List[dict], None]) -> Optional[List[list]]:
			"""
			Validates the search parameters supplied to the `joined_read()` method.

			:param select_params: List of search parameters to validate.
			:return: Validated search parameters.
			"""

			if select_params is None:
				return None

			if type(select_params[0]) is not list:
				# If a 2D list of search params is supplied, house it in a list for consistency.
				select_params = [select_params]

			for single_table_params_list in select_params:
				for param in single_table_params_list:
					if type(param) is not str or not param:
						raise AttributeError(
							"Only non-empty strings are valid within the `search_params` listed supplied to the `joined_read()` method."
						)

			return select_params

		@wraps(func)
		def wrapped(**kwargs) -> NoReturn:
			"""
			A wrapped function that houses the validation logic.

			:return: Kwargs for the wrapped function.
			"""

			try:
				kwargs["search_params"]: Union[dict, List[dict]] = validate_search_params(kwargs.get("search_params"))
				kwargs["select_params"]: Optional[List[list]] = validate_select_params(
					kwargs.get("select_params", None)
					)

			except AttributeError as exc:
				exception_handler.get_exception_log(exc)
				return None
			return func(**kwargs)

		return wrapped

	return inspect_params
