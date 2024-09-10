"""__init__.py

The entry-point for smartsheet_engine when it's imported as a library.

Classes
-------
- SmartsheetEngine

Dependencies
------------
- pandas
- smartsheet-python-sdk
"""


import logging
from typing import Union
from datetime import datetime
import pandas as pd
from smartsheet import models
from .client import SmartsheetAPIClient, SHARE_ACCESS_LEVELS
from .grids import SmartsheetGrid, GridRepository, METADATA_FIELDS
logging.basicConfig(format='%(asctime)s : %(levelname)-8s : %(name)s : %(message)s',
					datefmt='%Y-%m-%d %I:%M%p',
					level=logging.INFO)
logger = logging.getLogger(__name__)


class SmartsheetEngine:
	"""An abstraction that implements high-level Smartsheet operations

	Public Methods
	--------------
	- get_home_contents()
	- get_sheet(sheet_name)
	- append_sheet_rows(sheet_name, df)
	- update_sheet_rows(sheet_name, df)
	- delete_sheet_rows(sheet_name, df)
	- set_column_formula(sheet_name, column_name, formula)
	- set_column_dropdown(sheet_name, column_name, dropdown_options)
	- lock_column(sheet_name, column_name)
	- hide_column(sheet_name, column_name)
	- unlock_column(sheet_name, column_name)
	- unhide_column(sheet_name, column_name)
	- share_sheet(sheet_name, share_with, access_level, send_email)
	"""

	def __init__(self, api_key: str = None):
		self.api = SmartsheetAPIClient(api_key=api_key)
		self.repo = GridRepository()
		self.get_home_contents()

	def get_home_contents(self):
		"""Get a listing of the user's Smartsheet Home contents via the API, and build SmartsheetGrid objects to represent each one
		"""

		self.home_contents = self.api.smart.Home.list_all_contents(include='source').to_dict()

		# Get Sheets in user's Sheets folder
		for sheet in self.home_contents['sheets']:
			self.repo.add_grid(SmartsheetGrid(sheet_id=sheet['id'],
											  sheet_name=sheet['name'],
											  access_level=sheet['accessLevel'],
											  created_at=datetime.strptime(sheet['createdAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
											  modified_at=datetime.strptime(sheet['modifiedAt'], '%Y-%m-%dT%H:%M:%S%zZ')))

		# Get Sheets in Folders
		self._find_sheets_in_folders(self.home_contents['folders'])

		# Get Sheets in Workspaces
		for workspace in self.home_contents['workspaces']:
			#logger.debug(f'Found workspace: {workspace["name"]}: keys={workspace.keys()}')
			if 'sheets' in workspace:
				for sheet in workspace['sheets']:
					self.repo.add_grid(SmartsheetGrid(sheet_id=sheet['id'],
													  sheet_name=sheet['name'],
													  access_level=sheet['accessLevel'],
													  created_at=datetime.strptime(sheet['createdAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
													  modified_at=datetime.strptime(sheet['modifiedAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
													  workspace_id=workspace['id'],
													  workspace_name=workspace['name'],
													  is_in_workspace=True))

			if 'folders' in workspace:
				self._find_sheets_in_folders(workspace,
											 workspace_id=workspace['id'],
											 workspace_name=workspace['name'])

		logger.info(f'Built an index of {len(self.repo.grids)} available Sheets')

	def _find_sheets_in_folders(
		self,
		folders: dict,
		workspace_id: int = None,
		workspace_name: str = None
	) -> dict:
		"""Get all sheets in the user's Smartsheet Folder(s), recursively

		:param folders: The dictionary to traverse recursively, looking for folders
		:param workspace_id: The workspace ID to include in the SmartsheetGrid object, if the folders are in a workspace 
		:param workspace_name: The workspace Name to include in the SmartsheetGrid object, if the folders are in a workspace
		:returns: A Smartsheet API response dictionary that may contain a list of folders
		"""

		if isinstance(folders, dict):
			for k, v in folders.items():
				if k == 'folders':
					for folder in v:
						if 'sheets' in folder:
							for sheet in folder['sheets']:
								self.repo.add_grid(SmartsheetGrid(sheet_id=sheet['id'],
																  sheet_name=sheet['name'],
																  access_level=sheet['accessLevel'],
																  created_at=datetime.strptime(sheet['createdAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
																  modified_at=datetime.strptime(sheet['modifiedAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
																  folder_id=folder['id'],
																  folder_name=folder['name'],
																  workspace_id=workspace_id,
																  workspace_name=workspace_name,
																  is_in_folder=True,
																  is_in_workspace=any([workspace_id, workspace_name])))
					self._find_sheets_in_folders(v)

	def get_sheet(
		self,
		sheet_name: str,
		include_sheet_id: bool = False
	) -> SmartsheetGrid:
		"""Get all the data from the API for the given Sheet, and save it as a SmartsheetGrid object
		
		:param sheet_name: Get the contents of this Smartsheet
		:param include_sheet_id: Include the Sheet ID of this Smartsheet in optional `_ss_sheet_id` metadata column
		:returns: A SmartsheetGrid object that contains the data and metadata for the given Smartsheet
		"""

		grid = self.repo.get_grid_by_name(sheet_name)
		grid.sheet_obj = self.api.smartsheet_get_sheet(grid.sheet_id)
		grid.column_map = {col.title: col.id for col in grid.sheet_obj.columns}
		grid.sheet_df = self._build_dataframe(sheet_name, include_sheet_id)
		self.repo.update_grid(grid)
		logger.info(f'{sheet_name} ({grid.sheet_id}): Got Sheet with {len(grid.sheet_df.index)} rows')
		return grid

	def _build_dataframe(
		self,
		sheet_name: str,
		include_sheet_id: bool = False
	) -> pd.DataFrame:
		"""Convert a Sheet object to a DataFrame and return it
		
		:param sheet_name: Build a dataframe for this Smartsheet
		:returns: The Sheet object as a dataframe
		"""
		
		grid = self.repo.get_grid_by_name(sheet_name)
		sheet_records = []
		for row in grid.sheet_obj.rows:
			# These fields prefixed with _ss are metadata needed for processing when
			# updating, adding, or removing rows
			row_record = {field:None for field in METADATA_FIELDS}
			row_record['_ss_row_id'] = row.id
			if include_sheet_id:
				row_record['_ss_sheet_id'] = grid.sheet_id
			for col in grid.column_map.keys():
				row_record.update({col: row.get_column(grid.column_map[col]).value})
			sheet_records.append(row_record)
		return pd.DataFrame.from_dict(sheet_records)

	def _get_grid(
		self,
		sheet_name: str,
		force_refresh: bool = False
	):
		"""Get a SmartsheetGrid from the repository and download the Sheet data and metadata
		
		:param sheet_name: Get the grid for the Smartsheet with this name
		:param force_refresh: Download the most current Sheet data/metadata, even if it already exists in the repo
		"""
		
		grid = self.repo.get_grid_by_name(sheet_name)
		if force_refresh or not grid.column_map:
			grid = self.get_sheet(grid.sheet_name)
		return grid
	
	def append_sheet_rows(
		self,
		sheet_name: str,
		df: pd.DataFrame,
		include_cols: list = None,
		exclude_cols: list = None
	):
		"""Append dataframe rows to a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to append rows to
		:param df: Append the rows in this dataframe to the Sheet
		:param include_cols: Only append the values in these columns (default: whatever fields exist in both df and grid.sheet_df)
		:param exclude_cols: Don't append the values from any of these columns
		"""

		grid = self._get_grid(sheet_name)
		rows = self.api.gen_rows_to_append(grid, df, include_cols, exclude_cols)
		self.api.smartsheet_add_rows(grid.sheet_id, rows)
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): Added {len(rows)} rows')

	def update_sheet_rows(
		self,
		sheet_name: str,
		df: pd.DataFrame,
		include_cols: list = None,
		exclude_cols: list = None
	):
		"""Update Rows in a Smartsheet

		:param sheet_name: The name of the Smartsheet to update rows on
		:param df: Update the Sheet with this dataframe
		:param include_cols: Only update the values in these columns (default: whatever fields exist in both df and grid.sheet_df)
		:param exclude_cols: Don't update the values from any of these columns
		"""

		grid = self._get_grid(sheet_name)
		rows = self.api.gen_rows_to_update(grid, df, include_cols, exclude_cols)
		self.api.smartsheet_update_rows(grid.sheet_id, rows)
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): Updated {len(rows)} rows')

	def delete_sheet_rows(
		self,
		sheet_name: str,
		df: pd.DataFrame
	):
		"""Delete Rows in a Smartsheet

		:param sheet_name: The name of the Smartsheet to delete rows from
		:param df: Get the list of Row IDs to delete from this dataframe
		:returns: A list of Row IDs
		"""

		grid = self._get_grid(sheet_name)
		rows = self.api.gen_rows_to_delete(grid, df)
		self.api.smartsheet_delete_rows(grid.sheet_id, rows)
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): Deleted {len(rows)} rows')

	def set_column_formula(
		self,
		sheet_name: str,
		column_name: str,
		formula: str
	):
		"""Set the column formula for a column in a Smartsheet

		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to set the dropdown on
		:param dropdown_options: The new values for the column dropdown
		"""
		
		grid = self._get_grid(sheet_name)
		self._set_column_property(grid, column_name, {'formula': formula})
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Set the column formula to {formula}')

	def set_column_dropdown(
		self,
		sheet_name: str,
		column_name: str,
		dropdown_options: list
	):
		"""Set the dropdown options for a column in a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to set the dropdown on
		:param dropdown_options: The new values for the column dropdown
		"""

		grid = self._get_grid(sheet_name)
		self._set_column_property(grid, column_name, {'type': 'PICKLIST', 'options': dropdown_options})
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Set the dropdown values to {dropdown_options}')

	def lock_column(self, sheet_name: str, column_name: str):
		"""Lock a column in a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to lock
		"""

		grid = self._get_grid(sheet_name)
		self._set_column_property(grid, column_name, {'locked': True})
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Locked column')

	def hide_column(self, sheet_name: str, column_name: str):
		"""Hide a column in a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to hide
		"""

		grid = self._get_grid(sheet_name)
		self._set_column_property(grid, column_name, {'hidden': True})
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Hid column')

	def unlock_column(self, sheet_name: str, column_name: str):
		"""Unlock a column in a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to lock
		"""

		grid = self._get_grid(sheet_name)
		self._set_column_property(grid, column_name, {'locked': False})
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Unlocked column')

	def unhide_column(self, sheet_name: str, column_name: str):
		"""Unhide a column in a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to unhide
		"""

		grid = self._get_grid(sheet_name)
		self._set_column_property(grid, column_name, {'hidden': False})
		logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Unhid column')

	def _set_column_property(
		self,
		grid: SmartsheetGrid,
		column_name: str,
		setting: dict
	):
		"""Update a Smartsheet Column property
		
		:param grid: Update the column on the Smartsheet that's represented by this SmartsheetGrid object
		:param column_name: Update the property of this column
		:param setting: A dictionary where the key is the name of the Column property, and the value is the new setting for the property
		"""

		if not grid:
			raise ValueError(f'A SmartsheetGrid must be provided to _set_column_property')
		if column_name not in grid.column_map:
			raise ValueError(f'Column "{column_name}" does not exist in the "{grid.sheet_name}" Smartsheet')
		
		self.api.smartsheet_update_column(grid.sheet_id,
										  grid.column_map[column_name],
										  self.api.smart.models.Column(setting))

	def share_sheet(
		self,
		sheet_name: str,
		share_with: Union[list, str],
		access_level: str = 'VIEWER',
		send_email: bool = False
	):
		"""Share a Smartsheet with one or more users with a given access level

		:param sheet_name: The name of the Smartsheet to share
		:param share_with: A list or semicolon-delimited string of email address(es) to share the Sheet with
		:param access_level: The access level that the given email address(es) should have (options: ADMIN,
			COMMENTER, EDITOR, EDITOR_SHARE, OWNER, VIEWER
		:param send_email: Notify the given user(s) by email that the sheet has been shared with them (default: Don't send email)
		"""
		
		if not isinstance(access_level, str):
			raise ValueError(f'Access level must be provided as a string, and it must be a valid option ({", ".join(SHARE_ACCESS_LEVELS)})')
		else:
			access_level = access_level.upper()
			if access_level not in SHARE_ACCESS_LEVELS:
				raise ValueError(f'Invalid access level provided ({access_level}). Please specify a valid option ({", ".join(SHARE_ACCESS_LEVELS)})')
		
		if isinstance(share_with, str):
			if ';' in share_with:
				share_with = [email.strip() for email in share_with.split(';')]
			else:
				share_with = [share_with.strip()]
		elif isinstance(share_with, list):
			share_with = [email.strip() for email in share_with]
		else:
			raise ValueError(f'Share email addresses must be provided as either a string or a list of strings. If providing multiple emails in a string, the string must be comma-delimited.')

		if send_email:
			email_notification_str = 'sending notification email'
		else:
			email_notification_str = 'not sending notification email'
		
		grid = self._get_grid(sheet_name)
		for email in share_with:
			share_settings = models.Share({'access_level': access_level, 'email': email})
			self.api.smartsheet_share_sheet(grid.sheet_id, share_settings, send_email=send_email)
			logger.info(f'{grid.sheet_name} ({grid.sheet_id}): Shared sheet with {email} ({access_level}), {email_notification_str}')
