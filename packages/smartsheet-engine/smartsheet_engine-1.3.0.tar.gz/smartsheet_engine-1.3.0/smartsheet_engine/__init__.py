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
from typing import Union, List
from datetime import datetime
import pandas as pd
from smartsheet import models
from .client import SmartsheetAPIClient, SHARE_ACCESS_LEVELS
from .grids import SmartsheetGrid, GridRepository, METADATA_FIELDS
logging.basicConfig(format='%(asctime)s : %(levelname)-8s : %(name)s : %(funcName)s : %(message)s',
					datefmt='%Y-%m-%d %I:%M%p',
					level=logging.INFO)
logger = logging.getLogger(__name__)


# DEBUGGING: Write logs to file
log_format = logging.Formatter('%(asctime)s : %(levelname)-8s : %(name)s : %(funcName)s : %(message)s')
file_handler = logging.FileHandler('smartsheet_engine_test_run.log')
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)


class SmartsheetEngine:
	"""An abstraction that implements high-level Smartsheet operations"""

	def __init__(self, api_key: str = None):
		self.api = SmartsheetAPIClient(api_key=api_key)
		self.repo = GridRepository()
		self.get_home_contents()

	def get_home_contents(self):
		"""Get a listing of all Smartsheets available to the user and save the metadata for each Sheet to the GridRepository
		"""

		home = self.api.smartsheet_get_home()
		if home is None:
			logger.warning(f'No Smartsheets are available to the user')
			return None
		else:
			self.home_contents = home.to_dict()
		
		# Get Sheets in user's Sheets folder
		for sheet in self.home_contents['sheets']:
			sheet_grid = SmartsheetGrid(sheet_id=sheet['id'],
										sheet_name=sheet['name'],
										access_level=sheet['accessLevel'],
										created_at=datetime.strptime(sheet['createdAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
										modified_at=datetime.strptime(sheet['modifiedAt'], '%Y-%m-%dT%H:%M:%S%zZ'))
			if self.repo.get_grid_by_id(sheet_grid.sheet_id):
				self.repo.update_grid(sheet_grid)
			else:
				self.repo.add_grid(sheet_grid)

		# Get Sheets in Folders
		self._find_sheets_in_folders(self.home_contents['folders'])

		# Get Sheets in Workspaces
		for workspace in self.home_contents['workspaces']:
			#logger.debug(f'Found workspace: {workspace["name"]}: keys={workspace.keys()}')
			if 'sheets' in workspace:
				for sheet in workspace['sheets']:
					sheet_grid = SmartsheetGrid(sheet_id=sheet['id'],
												sheet_name=sheet['name'],
												access_level=sheet['accessLevel'],
												created_at=datetime.strptime(sheet['createdAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
												modified_at=datetime.strptime(sheet['modifiedAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
												workspace_id=workspace['id'],
												workspace_name=workspace['name'],
												is_in_workspace=True)
					if self.repo.get_grid_by_id(sheet_grid.sheet_id):
						self.repo.update_grid(sheet_grid)
					else:
						self.repo.add_grid(sheet_grid)

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
								sheet_grid = SmartsheetGrid(sheet_id=sheet['id'],
															sheet_name=sheet['name'],
															access_level=sheet['accessLevel'],
															created_at=datetime.strptime(sheet['createdAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
															modified_at=datetime.strptime(sheet['modifiedAt'], '%Y-%m-%dT%H:%M:%S%zZ'),
															folder_id=folder['id'],
															folder_name=folder['name'],
															workspace_id=workspace_id,
															workspace_name=workspace_name,
															is_in_folder=True,
															is_in_workspace=any([workspace_id, workspace_name]))
								if self.repo.get_grid_by_id(sheet_grid.sheet_id):
									self.repo.update_grid(sheet_grid)
								else:
									self.repo.add_grid(sheet_grid)
					self._find_sheets_in_folders(v)

	def get_sheet(
		self,
		sheet_name: str,
		include_sheet_id: bool = False,
	) -> Union[SmartsheetGrid, None]:
		"""Get all the data from the API for the given Sheet, and save it as a SmartsheetGrid object
		
		:param sheet_name: Get the contents of this Smartsheet
		:param include_sheet_id: Include the Sheet ID of this Smartsheet in optional `_ss_sheet_id` metadata column
		:returns: A SmartsheetGrid object that contains the data and metadata for the given Smartsheet, or None if the Sheet doesn't exist
		"""

		grid = self.repo.get_grid_by_name(sheet_name)
		if not grid or (grid.sheet_df is not None and len(grid.sheet_df.index)) == 0:
			self.get_home_contents()
			grid = self.repo.get_grid_by_name(sheet_name)
			if not grid:
				logger.error(f'Smartsheet not found: {sheet_name}')
				return
		
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
			row_record = {}
			row_record['_ss_row_id'] = row.id
			if include_sheet_id:
				row_record['_ss_sheet_id'] = grid.sheet_id
			for col in grid.column_map.keys():
				row_record.update({col: row.get_column(grid.column_map[col]).value})
			sheet_records.append(row_record)
		return pd.DataFrame.from_dict(sheet_records)

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

		grid = self.get_sheet(sheet_name)
		rows = self.api.gen_rows_to_append(grid, df, include_cols, exclude_cols)
		resp = self.api.smartsheet_add_rows(grid.sheet_id, rows)
		if resp:
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

		grid = self.get_sheet(sheet_name)
		rows = self.api.gen_rows_to_update(grid, df, include_cols, exclude_cols)
		resp = self.api.smartsheet_update_rows(grid.sheet_id, rows)
		if resp:
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

		grid = self.get_sheet(sheet_name)
		rows = self.api.gen_rows_to_delete(grid, df)
		resp = self.api.smartsheet_delete_rows(grid.sheet_id, rows)
		if resp:
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
		
		grid = self.get_sheet(sheet_name)
		resp = self._set_column_property(grid, column_name, {'formula': formula})
		if resp:
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

		grid = self.get_sheet(sheet_name)
		resp = self._set_column_property(grid, column_name, {'type': 'PICKLIST', 'options': dropdown_options})
		if resp:
			logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Set the dropdown values to {dropdown_options}')

	def lock_column(self, sheet_name: str, column_name: str):
		"""Lock a column in a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to lock
		"""

		grid = self.get_sheet(sheet_name)
		resp = self._set_column_property(grid, column_name, {'locked': True})
		if resp:
			logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Locked column')

	def hide_column(self, sheet_name: str, column_name: str):
		"""Hide a column in a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to hide
		"""

		grid = self.get_sheet(sheet_name)
		resp = self._set_column_property(grid, column_name, {'hidden': True})
		if resp:
			logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Hid column')

	def unlock_column(self, sheet_name: str, column_name: str):
		"""Unlock a column in a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to lock
		"""

		grid = self.get_sheet(sheet_name)
		resp = self._set_column_property(grid, column_name, {'locked': False})
		if resp:
			logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Unlocked column')

	def unhide_column(self, sheet_name: str, column_name: str):
		"""Unhide a column in a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to unhide
		"""

		grid = self.get_sheet(sheet_name)
		resp = self._set_column_property(grid, column_name, {'hidden': False})
		if resp:
			logger.info(f'{grid.sheet_name} ({grid.sheet_id}): {column_name}: Unhid column')

	def _set_column_property(
		self,
		grid: SmartsheetGrid,
		column_name: str,
		setting: dict
	) -> Union[models.result.Result, None]:
		"""Update a Smartsheet Column property
		
		:param grid: Update the column on the Smartsheet that's represented by this SmartsheetGrid object
		:param column_name: Update the property of this column
		:param setting: A dictionary where the key is the name of the Column property, and the value is the new setting for the property
		"""

		if not grid:
			logger.error(f'A SmartsheetGrid must be provided to _set_column_property')
			return
		
		if column_name not in grid.column_map:
			logger.error(f'Column "{column_name}" does not exist in the "{grid.sheet_name}" Smartsheet')
			return

		resp = self.api.smartsheet_update_column(grid.sheet_id,
										  		 grid.column_map[column_name],
										  		 self.api.smart.models.Column(setting))
		return resp

	def create_sheet(
		self,
		sheet_name: str,
		column_spec: List[dict],
		create_in: str = 'home',
		folder_id: int = None,
		workspace_id: int = None
	):
		"""Create a new Smartsheet
		
		:param sheet_name: The name of the Smartsheet to create
		:param column_spec: A list of dictionaries, each containing a Smartsheet column specification
		:param create_in: Where to create the Smartsheet (either "home", "folder", or "workspace")
		:param folder_id: The ID of the Folder to save the Smartsheet in (required if create_in is "folder")
		:param workspace_id: The ID of the Workspace to save the Smartsheet in (required if create_in is "workspace")
		"""

		if not sheet_name:
			logger.error(f'Sheet name required to create a new Smartsheet, but none was provided')
			return
		
		sheet_spec = models.Sheet({'name': sheet_name, 'columns': column_spec})

		if create_in == 'home':
			resp = self.api.smartsheet_create_sheet_in_home(sheet_spec)
	
		elif create_in == 'folder':
			if folder_id:
				resp = self.api.smartsheet_create_sheet_in_folder(sheet_spec, folder_id)
			else:
				logger.error(f'A folder ID must be provided when choosing to create a Smartsheet in a Folder, but none was provided')
				return				

		elif create_in == 'workspace':
			if workspace_id:
				resp = self.api.smartsheet_create_sheet_in_workspace(sheet_spec, workspace_id)
			else:
				logger.error(f'A workspace ID must be provided when choosing to create a Smartsheet in a Workspace, but none was provided')
				return

		if resp:
			sheet_id = resp.result.id
			permalink = resp.result.permalink
			logger.info(f'{sheet_name} ({sheet_id}): Created new Smartsheet at {permalink}')

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
			logger.error(f'Access level must be provided as a string, and it must be a valid option ({", ".join(SHARE_ACCESS_LEVELS)})')
			return
		else:
			access_level = access_level.upper()
			if access_level not in SHARE_ACCESS_LEVELS:
				logger.error(f'Invalid access level provided ({access_level}). Please specify a valid option ({", ".join(SHARE_ACCESS_LEVELS)})')
				return
		
		if isinstance(share_with, str):
			if ';' in share_with:
				share_with = [email.strip() for email in share_with.split(';')]
			else:
				share_with = [share_with.strip()]
		elif isinstance(share_with, list):
			share_with = [email.strip() for email in share_with]
		else:
			logger.error(f'Share email addresses must be provided as either a string or a list of strings. If providing multiple emails in a string, the string must be comma-delimited.')
			return
		
		if send_email:
			email_notification_str = 'sending notification email'
		else:
			email_notification_str = 'not sending notification email'
		
		grid = self.get_sheet(sheet_name)
		for email in share_with:
			share_settings = models.Share({'access_level': access_level, 'email': email})
			resp = self.api.smartsheet_share_sheet(grid.sheet_id, share_settings, send_email=send_email)
			if resp:
				logger.info(f'{grid.sheet_name} ({grid.sheet_id}): Shared sheet with {email} ({access_level}), {email_notification_str}')
