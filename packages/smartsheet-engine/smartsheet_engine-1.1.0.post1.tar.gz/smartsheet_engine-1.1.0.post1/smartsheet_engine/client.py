"""client.py

Provides an abstraction for working with the SmartsheetAPI.

Classes
-------
- SmartsheetTokenError (exception)
- SmartsheetAPIClient

Dependencies
------------
- pandas
- smartsheet-python-sdk
"""

import os
import time
import logging
from enum import Enum
from datetime import datetime, date
from typing import Union, List, Callable, Dict
from functools import wraps
import pandas as pd
import smartsheet
from smartsheet import models
from smartsheet_engine.grids import SmartsheetGrid, METADATA_FIELDS
logger = logging.getLogger(__name__)


DEFAULT_SMARTSHEET_RETRIES = 3
DEFAULT_SMARTSHEET_WAIT_TIME = 15
SHARE_ACCESS_LEVELS = [
	"ADMIN",
	"COMMENTER",
	"EDITOR",
	"EDITOR_SHARE",
	"OWNER",
	"VIEWER",
]


def smartsheet_retry(
	retries: int = DEFAULT_SMARTSHEET_RETRIES,
	wait_time: int = DEFAULT_SMARTSHEET_WAIT_TIME,
	exception: Exception = Exception
) -> Callable:
	"""Try running the decorated function again after sleeping if an exception is caught
	
	The main purpose for this decorator is to retry some requests to the Smartsheet API. The API
	can occasionally fail due to internal server errors, and there's a bug where the SDK will
	occasionally raise an exception when this happens.

	:param retries: How many times to retry the request if an Exception is raised (default: 3)
	:param wait_time: How long to wait/sleep between retries, in seconds (default: 60 seconds)
	:param exception: Which Exception to catch (default: Exception)
	"""

	def decorator(func: Callable):
		@wraps(func)
		def wrapper(*args, **kwargs):
			for i in range(1, retries+1):
				try:
					func_return_value = func(*args, **kwargs)
				except exception as err:
					logger.warning(f'Retry {i} of {retries}: The Smartsheet API returned an {exception}: {err} error. Waiting {wait_time} seconds and trying again.')
					time.sleep(wait_time)
				else:
					if isinstance(func_return_value, dict):
						status_code = func_return_value.get('response').get('statusCode')
						reason = func_return_value.get('response').get('reason')
						if status_code == 500:
							logger.warning(f'Retry {i} of {retries}: The Smartsheet API returned an error: {status_code}, {reason}')
							time.sleep(wait_time)
					else:
						return func_return_value
		return wrapper
	return decorator


class SmartsheetTokenError(Exception):
	"""Raise an Exception when there's an issue with the user's Smartsheet API token

	The exception that will be raised if the user doesn't have a Smartsheet API
	key stored in the "SMARTSHEET_ACCESS_TOKEN" environment variable, or an API
	key isn't provided when initializing an instance of SmartsheetEngine.
	"""

	default_msg = ('A Smartsheet API access token is required to use this method. '
				   'Please get an API token and make sure it\'s assigned to the '
				   '"SMARTSHEET_ACCESS_TOKEN" environment variable, or provided to '
				   'the api_key parameter when initializing a SmartsheetEngine.')

	def __init__(
		self,
		msg=default_msg,
		*args,
		**kwargs
	):
		super().__init__(msg, *args, **kwargs)


class SmartsheetAPIClient:
	"""A high-level abstraction for making Smartsheet API requests

	Public Methods
	--------------
	- smartsheet_get_sheet(sheet_id)
	- smartsheet_update_rows(sheet_id, rows)
	- smartsheet_add_rows(sheet_id, rows)
	- smartsheet_delete_rows(sheet_id, row_ids)
	- smartsheet_add_columns(sheet_id, columns)
	- smartsheet_update_column(sheet_id, column_id, columns)
	- gen_rows_to_append(grid, df)
	- gen_rows_to_update(grid, df)
	- gen_rows_to_delete(grid, df)
	"""

	def __init__(self, api_key: str = None):
		"""Initialize an instance of SmartsheetEngine

		The Smartsheet SDK automatically looks for an API key in the SMARTSHEET_ACCESS_TOKEN
		environment variable. If the user passes an API key, that will be used instead. If an
		API key isn't passed by the user, and there's no API key in the environment variable,
		then an exception will be raised.

		:param api_key: Authenticate with the Smartsheet API using this key
		:raises SmartsheetTokenError: If an API key wasn't provided or found in the environment
		"""

		if api_key:
			logger.info(f'Initializing Smartsheet API with user-provided key')
			self.smart = smartsheet.Smartsheet(api_key)
		else:
			try:
				if os.environ['SMARTSHEET_ACCESS_TOKEN']:
					pass
				else:
					raise SmartsheetTokenError()
			except KeyError:
				raise SmartsheetTokenError()

			self.smart = smartsheet.Smartsheet()
		logger.info(f'Initialized Smartsheet API with key in environment')
		self.smart.errors_as_exceptions(True)

	@smartsheet_retry()
	def smartsheet_get_sheet(self, sheet_id: int) -> models.Sheet:
		return self.smart.Sheets.get_sheet(sheet_id)
	
	@smartsheet_retry()
	def smartsheet_share_sheet(
		self,
		sheet_id: int,
		share_settings: models.Share,
		send_email: bool = False
	) -> models.Sheet:
		return self.smart.Sheets.share_sheet(sheet_id, share_settings, send_email=send_email)
	
	@smartsheet_retry()
	def smartsheet_update_rows(self, sheet_id: int, rows: List[models.Row]):
		return self.smart.Sheets.update_rows(sheet_id, rows)
	
	@smartsheet_retry()
	def smartsheet_add_rows(self, sheet_id: int, rows: List[models.Row]):
		return self.smart.Sheets.add_rows(sheet_id, rows)

	@smartsheet_retry()
	def smartsheet_delete_rows(self, sheet_id: int, row_ids: List[int]):
		return self.smart.Sheets.delete_rows(sheet_id, row_ids)

	@smartsheet_retry()
	def smartsheet_add_columns(self, sheet_id: int, columns: Union[models.Column, List[models.Column]]):
		return self.smart.Sheets.add_columns(sheet_id, columns)

	@smartsheet_retry()
	def smartsheet_update_column(
		self,
		sheet_id: int,
		column_id: int,
		columns: Union[models.Column, List[models.Column]]
	):
		return self.smart.Sheets.update_column(sheet_id, column_id, columns)
	 
	def gen_rows_to_append(
		self,
		grid: SmartsheetGrid,
		df: pd.DataFrame,
		include_cols: list = None,
		exclude_cols: list = None
	) -> Union[List[models.Row], None]:
		"""Generate a list of Smartsheet SDK Row objects that will be appended to a Sheet

		:param grid: Append Rows to the Sheet represented by this SmartsheetGrid
		:param df: Generate a Row object for each series in this dataframe
		:param include_cols: Only append the values in these columns (default: whatever fields exist in both df and grid.sheet_df)
		:param exclude_cols: Don't append the values from any of these columns
		:returns: A list of Smartsheet Row objects
		"""

		if not df.empty:
			available_cols = set(df.columns) & set(grid.sheet_df.columns)
			if include_cols:
				include_cols = available_cols & set(include_cols)
			else:
				include_cols = available_cols
			if not include_cols:
				raise ValueError(f'No columns in the dataframe are present in the Smartsheet')

			rows_to_append = []
			records = df.to_dict('records')
			for record in records:
				new_row = models.Row()
				new_row.to_bottom = True
				for key, value in record.items():
					if key in METADATA_FIELDS:
						continue
					if include_cols and key not in include_cols:
						continue
					if exclude_cols and key in exclude_cols:
						continue
					if isinstance(value, datetime) or isinstance(value, date):
						value = value.isoformat()
					if value:
						new_row.cells.append({
							'column_id':    grid.column_map[key],
							'value':        value})
				rows_to_append.append(new_row)
				logger.info(f'{grid.sheet_name} ({grid.sheet_id}): Created {len(rows_to_append)} Row objects to append')
			return rows_to_append
		return None

	def gen_rows_to_update(
		self,
		grid: SmartsheetGrid,
		df: pd.DataFrame,
		include_cols: list = None,
		exclude_cols: list = None
	) -> Union[List[models.Row], None]:
		"""Generate a list of Smartsheet SDK Row objects that will be updated on a Sheet
		
		:param grid: Update Rows on the Sheet represented by this SmartsheetGrid
		:param df: Generate a Row object for updating each series in this dataframe
		:param include_cols: Only update the values in these columns (default: whatever fields exist in both df and grid.sheet_df)
		:param exclude_cols: Don't update the values from any of these columns
		:returns: A list of Smartsheet Row objects
		"""

		if not df.empty:
			available_cols = set(df.columns) & set(grid.sheet_df.columns)
			if include_cols:
				include_cols = available_cols & set(include_cols)
			else:
				include_cols = available_cols
			if not include_cols:
				raise ValueError(f'No columns in the dataframe are present in the Smartsheet')

			rows_to_update = []
			records = df.to_dict('records')
			for record in records:
				row_id = int(record.get('_ss_row_id', 0))
				if row_id:
					new_row = models.Row()
					new_row.id = row_id
					for key, value in record.items():
						if key in METADATA_FIELDS:
							continue
						if include_cols and key not in include_cols:
							continue
						if exclude_cols and key in exclude_cols:
							continue
						if isinstance(value, datetime) or isinstance(value, date):
							value = value.isoformat()
						if not value:
							value = ''
						new_cell = models.Cell()
						new_cell.column_id = grid.column_map[key]
						new_cell.value = value
						new_row.cells.append(new_cell)
					rows_to_update.append(new_row)
			logger.info(f'{grid.sheet_name} ({grid.sheet_id}): Created {len(rows_to_update)} Row objects to update')
			return rows_to_update
	
	def gen_rows_to_delete(
		self,
		grid: SmartsheetGrid,
		df: pd.DataFrame
	) -> Union[List[int], None]:
		"""Generate a list of Smartsheet Row IDs to delete from a Sheet
		
		:param grid: Delete Rows from the Sheet represented by this SmartsheetGrid
		:param df: Get the list of Row IDs from this dataframe
		:returns: A list of Row IDs
		"""

		if not df.empty:
			rows_to_remove = []
			records = df.to_dict('records')
			for record in records:
				row_id = int(record.get('_ss_row_id', 0))
				if row_id:
					rows_to_remove.append(row_id)
			logger.info(f'{grid.sheet_name} ({grid.sheet_id}): Created a list of {len(rows_to_remove)} Row IDs to delete')
			return rows_to_remove
