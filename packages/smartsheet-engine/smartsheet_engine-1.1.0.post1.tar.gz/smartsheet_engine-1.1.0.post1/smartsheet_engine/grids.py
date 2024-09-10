"""grids.py

Provides an abstraction for representing, storing, and retrieving Smartsheets
and their associated metadata.

Classes
-------
- SmartsheetGrid (dataclass)
- GridRepository

Dependencies
------------
- pandas
- smartsheet-python-sdk
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Union, Dict, List
import pandas as pd
from smartsheet import models
logger = logging.getLogger(__name__)


# These fields are added to each dataframe that's created by SmartsheetEngine and are used to 
# track Sheet and Row IDs.
METADATA_FIELDS = [
	'_ss_row_id',
	'_ss_sheet_id', # optional -- only added if explicitly requested by the user
]


@dataclass
class SmartsheetGrid:
	"""A Smartsheet SDK Sheet object and associated metadata"""
	sheet_id: int
	sheet_name: str
	access_level: str
	column_map: dict = None
	sheet_obj: models.sheet.Sheet = None
	sheet_df: pd.DataFrame = None
	created_at: datetime = None
	modified_at: datetime = None
	workspace_id: int = None
	workspace_name: str = None
	folder_id: int = None
	folder_name: str = None
	is_in_folder: bool = False
	is_in_workspace: bool = False


class GridRepository:
	"""An in-memory repository for SmartsheetGrid objects
	
	Public Methods
	--------------
	- add_grid(grid)
	- update_grid(grid)
	- get_all_grids()
	- get_grid_by_id(sheet_id)
	- get_grid_by_name(sheet_name)
	"""

	def __init__(self):
		self.grids = []
	
	def add_grid(self, grid: SmartsheetGrid) -> bool:
		try:
			self.grids.append(grid)
			return True
		except:
			return False
	
	def update_grid(self, grid: SmartsheetGrid) -> bool:
		index = next((i for i, g in enumerate(self.grids) if g.sheet_id == grid.sheet_id), None)
		if index is not None:
			self.grids[index] = grid
			return True
		return False
	
	def get_all_grids(self) -> list:
		return self.grids
	
	def get_grid_by_id(self, id: int) -> Union[models.sheet.Sheet, None]:
		grid = next((grid for grid in self.grids if grid.sheet_id == id), None)
		if not grid:
			raise ValueError(f'No SmartsheetGrid found for Sheet ID: {id}')
		return grid

	def get_grid_by_name(self, name: str) -> Union[models.sheet.Sheet, None]:
		grid = next((grid for grid in self.grids if grid.sheet_name == name), None)
		if not grid:
			raise ValueError(f'No SmartsheetGrid found for Sheet: {name}')
		return grid
