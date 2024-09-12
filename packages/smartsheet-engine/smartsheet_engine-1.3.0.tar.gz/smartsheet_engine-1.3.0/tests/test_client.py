"""
- test_smartsheet_retry

SmartsheetAPIClient
-------------------
- MockSmartsheetAPIClient
- test_init
- test_smartsheet_get_sheet_response_ok
- test_smartsheet_get_sheet_response_not_ok
- test_smartsheet_share_sheet_response_ok
- test_smartsheet_share_sheet_response_not_ok
- test_smartsheet_update_rows_response_ok
- test_smartsheet_update_rows_response_not_ok
- test_smartsheet_add_rows_response_ok
- test_smartsheet_add_rows_response_not_ok
- test_smartsheet_delete_rows_response_ok
- test_smartsheet_delete_rows_response_not_ok
- test_smartsheet_add_columns_response_ok
- test_smartsheet_add_columns_response_not_ok
- test_smartsheet_update_column_response_ok
- test_smartsheet_update_column_response_not_ok
- test_gen_rows_to_append_valid_dataframe
- test_gen_rows_to_append_malformed_dataframe
- test_gen_rows_to_append_dataframe_has_no_matching_columns
- test_gen_rows_to_update_valid_dataframe
- test_gen_rows_to_update_malformed_dataframe
- test_gen_rows_to_update_dataframe_has_no_matching_columns
- test_gen_rows_to_update_missing_row_id_column
- test_gen_rows_to_delete_valid_dataframe
- test_gen_rows_to_delete_missing_row_id_column
- test_gen_rows_to_update_dataframe_has_no_matching_columns
"""

from unittest.mock import Mock, MagicMock, patch
import pytest
from smartsheet_engine.client import smartsheet_retry, SmartsheetAPIClient


@patch('smartsheet_engine.client.SmartsheetAPIClient_get_sheet')
def test_smartsheet_get_sheet_response_ok(mock_get_sheet):
    sheet_id = '1234567890123456'
    mock_get_sheet.return_value = Mock()
    mock_get_sheet.return_value.json.return_value = 0