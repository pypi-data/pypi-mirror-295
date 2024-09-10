import pygsheets
import os
from logging import info
import pandas as pd
from pygsheets import ExportType

download_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '.', "media", "downloads"))


class SheetUtils:

    def __init__(self, sheet_url, service_account_json):
        self.sheet_url = sheet_url
        self.sheet_auth = pygsheets.authorize(service_account_json=service_account_json)
        self.workbook = self.sheet_auth.open_by_url(sheet_url)

    def get_sheet_values_as_df(self, title=""):
        worksheet = self.workbook.worksheet_by_title(title)
        return worksheet.get_as_df()

    def get_sheet_values(title=""):
        return SheetUtils.get_sheet_values_as_df(title).to_dict('list')

    def get_row_values_by_specific_value(self, title="", column_name="", row_value=""):
        worksheet = self.workbook.worksheet_by_title(title)
        data = worksheet.get_as_df()
        row_values = data.loc[data[column_name] == row_value].to_dict('list')
        return row_values

    def get_sheet_row_values(self, title="", index=0):
        worksheet = self.workbook.worksheet_by_title(title)
        data = worksheet.get_as_df()
        p_data = data.iloc[index].tolist()
        return p_data

    def get_sheet_row_values_by_name(self, title="", column_name=""):
        worksheet = self.workbook.worksheet_by_title(title)
        data = worksheet.get_as_df()
        p_data = data[column_name].tolist()
        return p_data

    def get_number_of_rows_cols(self, title=""):
        worksheet = self.workbook.worksheet_by_title(title)
        data = worksheet.get_as_df()
        no_of_cols = len(data.columns)
        no_of_rows = len(data)
        data_rows_cols = (no_of_rows, no_of_cols)
        return data_rows_cols

    def update_sheet_values(self, title, data, clear_data=None):
        worksheet = self.workbook.worksheet_by_title(title)
        if clear_data:
            worksheet.clear()
        df = pd.DataFrame(data)
        df.head()
        worksheet.set_dataframe(df, (1, 1))

    def update_specific_sheet_values(self, title, index, column_name, new_value):
        worksheet = self.workbook.worksheet_by_title(title)
        data = worksheet.get_as_df()
        df = pd.DataFrame(data)
        df.at[index, column_name] = new_value
        worksheet.set_dataframe(df, (1, 1))

    def get_index_from_df(self, title, column_name, row_value):
        worksheet = self.workbook.worksheet_by_title(title)
        data = worksheet.get_as_df()
        df = pd.DataFrame(data)
        index_value = df.index[df[column_name] == row_value].tolist()
        return index_value[0]

    def update_specific_column_values(self, title, column_name, new_values):
        worksheet = self.workbook.worksheet_by_title(title)
        data = worksheet.get_as_df()
        df = pd.DataFrame(data)
        index = df.columns.get_loc(column_name) + 1
        worksheet.update_col(index, new_values, 1)

    def update_cells_with_hyperlinks(self, title, column_name, href_value, column_alphabet):
        worksheet = self.workbook.worksheet_by_title(title)
        all_cell_values = SheetUtils.get_sheet_row_values_by_name(title, column_name)
        for i in range(len(all_cell_values)):
            # print(all_cell_values[i])
            if all_cell_values[i] != "":
                worksheet.update_value('{}{}'.format(column_alphabet, i + 2),
                                       '=HYPERLINK("{}{}", "{}")'
                                       .format(href_value, all_cell_values[i], all_cell_values[i]))

    def clear_existing_df(self, title):
        worksheet = self.workbook.worksheet_by_title(title)
        worksheet.clear()

    def update_existing_df(self, title, new_df, index):
        worksheet = self.workbook.worksheet_by_title(title)
        df = worksheet.get_as_df()
        new_df = pd.DataFrame(new_df, index=[index])
        # df = df.append(new_df, ignore_index=True)
        df = pd.concat([df, new_df])
        worksheet.set_dataframe(df.fillna("Not Filled"), (1, 1))
        return df

    def download_sheets(self, title="", export_type=ExportType.CSV, file_name="output"):
        worksheet = self.workbook.worksheet_by_title(title)
        worksheet.export(file_format=export_type, filename=file_name, path=download_path)
        info("Sheet downloaded to " + download_path)

    def create_new_sheet(self, sheet_title="", user = "", role = "writer", type = "user", emailMessage = "Created from google sheets api"):
        wb = self.sheet_auth.create("automation-test-data")
        wb.share(user, role=role, type=type,
                 emailMessage=emailMessage)
        info("Sheets url : " + wb.url)

    def get_existing_df(self, title):
        worksheet = self.workbook.worksheet_by_title(title)
        df = worksheet.get_as_df()
        return df, worksheet

    def set_new_dataframe(self, worksheet, df):
        self.worksheet.set_dataframe(df, (1, 1))
