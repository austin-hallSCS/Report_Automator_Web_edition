import pandas as pd
import os
import time
from datetime import datetime as dt, timedelta
class Report:
    def __init__(self):
        self.dataFrame = self.prepare_Spreadsheet(self.inFile.filePath)

    # Loads excel file as a dataframe and formats the data.
    @staticmethod
    def prepare_Spreadsheet(file):
        # Load the excel file as a dataframe
        df = pd.read_excel(file, skiprows=4)
        
        # Drop the empty columns
        df.dropna(how='all', axis=1, inplace=True)

        # Convert the first row to headers
        headers = df.iloc[0]
        df = pd.DataFrame(df.values[1:], columns=headers)

        # Remove all the columns we don't use
        headersToDelete = ['Domain/Workgroup', 'ConfigMgr Site Name', 'Service Pack Level', 'Memory (KBytes)', 'Processor (GHz)', 'Total Disk Space (MB)', 'Free Disk Space (MB)']
        for header in headersToDelete:
            try:
                df.drop(header, axis=1, inplace=True)
            except KeyError as e:
                print(f"There was an error removing one or more unused columns:\n{e}")

        # Add new column at the end for warranty dates
        df['Warranty End Date'] = ''

        return df