import pandas as pd
import calendar
import os
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import datetime
import re
import pandas as pd
from fredapi import Fred
import time
from datetime import datetime,timedelta
from cif import cif
from io import StringIO
import urllib
import requests_cache
import urllib.request
import requests
from geopy.geocoders import Nominatim
import subprocess
import json
import xml.etree.ElementTree as ET

class dataprocessing:
    
    def help(self):
        print("This is the help section. The functions in the package are as follows:")

        print("\n1. get_wd_levels")
        print("   - Description: Get the working directory with the option of moving up parents.")
        print("   - Usage: get_wd_levels(levels)")
        print("   - Example: get_wd_levels(0)")

        print("\n2. remove_rows")
        print("   - Description: Removes a specified number of rows from a pandas DataFrame.")
        print("   - Usage: remove_rows(data_frame, num_rows_to_remove)")
        print("   - Example: remove_rows(df, 2)")

        print("\n3. aggregate_daily_to_wc_long")
        print("   - Description: Aggregates daily data into weekly data, grouping and summing specified columns, starting on a specified day of the week.")
        print("   - Usage: aggregate_daily_to_wc_long(df, date_column, group_columns, sum_columns, wc, aggregation='sum')")
        print("   - Example: aggregate_daily_to_wc_long(df, 'date', ['platform'], ['cost', 'impressions', 'clicks'], 'mon', 'average')")

        print("\n4. convert_monthly_to_daily")
        print("   - Description: Converts monthly data in a DataFrame to daily data by expanding and dividing the numeric values.")
        print("   - Usage: convert_monthly_to_daily(df, date_column, divide)")
        print("   - Example: convert_monthly_to_daily(df, 'date')")

        print("\n5. plot_two")
        print("   - Description: Plots specified columns from two different DataFrames using a shared date column. Useful for comparing data.")
        print("   - Usage: plot_two(df1, col1, df2, col2, date_column, same_axis=True)")
        print("   - Example: plot_two(df1, 'cost', df2, 'cost', 'obs', True)")

        print("\n6. remove_nan_rows")
        print("   - Description: Removes rows from a DataFrame where the specified column has NaN values.")
        print("   - Usage: remove_nan_rows(df, col_to_remove_rows)")
        print("   - Example: remove_nan_rows(df, 'date')")

        print("\n7. filter_rows")
        print("   - Description: Filters the DataFrame based on whether the values in a specified column are in a provided list.")
        print("   - Usage: filter_rows(df, col_to_filter, list_of_filters)")
        print("   - Example: filter_rows(df, 'country', ['UK', 'IE'])")

        print("\n8. plot_one")
        print("   - Description: Plots a specified column from a DataFrame.")
        print("   - Usage: plot_one(df1, col1, date_column)")
        print("   - Example: plot_one(df, 'Spend', 'OBS')")

        print("\n9. week_of_year_mapping")
        print("   - Description: Converts a week column in 'yyyy-Www' or 'yyyy-ww' format to week commencing date.")
        print("   - Usage: week_of_year_mapping(df, week_col, start_day_str)")
        print("   - Example: week_of_year_mapping(df, 'week', 'mon')")

        print("\n10. exclude_rows")
        print("    - Description: Removes rows from a DataFrame based on whether the values in a specified column are not in a provided list.")
        print("    - Usage: exclude_rows(df, col_to_filter, list_of_filters)")
        print("    - Example: exclude_rows(df, 'week', ['2022-W20', '2022-W21'])")

        print("\n11. rename_cols")
        print("    - Description: Renames columns in a pandas DataFrame.")
        print("    - Usage: rename_cols(df, name)")
        print("    - Example: rename_cols(df, 'ame_facebook'")

        print("\n12. merge_new_and_old")
        print("    - Description: Creates a new DataFrame with two columns: one for dates and one for merged numeric values.")
        print("    - Merges numeric values from specified columns in the old and new DataFrames based on a given cutoff date.")
        print("    - Usage: merge_new_and_old(old_df, old_col, new_df, new_col, cutoff_date, date_col_name='OBS')")
        print("    - Example: merge_new_and_old(df1, 'old_col', df2, 'new_col', '2023-01-15')")

        print("\n13. merge_dataframes_on_date")
        print("    - Description: Merge a list of DataFrames on a common column.")
        print("    - Usage: merge_dataframes_on_date(dataframes, common_column='OBS', merge_how='outer')")
        print("    - Example: merge_dataframes_on_date([df1, df2, df3], common_column='OBS', merge_how='outer')")

        print("\n14. merge_and_update_dfs")
        print("    - Description: Merges two dataframes on a key column, updates the first dataframe's columns with the second's where available, and returns a dataframe sorted by the key column.")
        print("    - Usage: merge_and_update_dfs(df1, df2, key_column)")
        print("    - Example: merged_dataframe = merge_and_update_dfs(processed_facebook, finalised_meta, 'OBS')")

        print("\n15. convert_us_to_uk_dates")
        print("    - Description: Convert a DataFrame column with mixed date formats to datetime.")
        print("    - Usage: convert_us_to_uk_dates(df, date_col)")
        print("    - Example: convert_us_to_uk_dates(df, 'date')")
        
        print("\n16. combine_sheets")
        print("    - Description: Combines multiple DataFrames from a dictionary into a single DataFrame.")
        print("    - Usage: combine_sheets(all_sheets)")
        print("    - Example: combine_sheets({'Sheet1': df1, 'Sheet2': df2})")
        
        print("\n17. pivot_table")
        print("    - Description: Dynamically pivots a DataFrame based on specified columns.")
        print("    - Usage: pivot_table(df, index_col, columns, values_col, filters_dict=None, fill_value=0,aggfunc='sum',margins=False,margins_name='Total',datetime_trans_needed=True,reverse_header_order = 'False',fill_missing_weekly_dates=False,week_commencing='W-MON')")
        print("    - Example: pivot_table(df, 'OBS', 'Channel Short Names', 'Value',filters_dict={'Master Include':' == 1','OBS':' >= datetime(2019,9,9)','Metric Short Names':' == 'spd''}, fill_value=0,aggfunc='sum',margins=False,margins_name='Total',datetime_trans_needed=True,reverse_header_order = 'True',fill_missing_weekly_dates=True,week_commencing='W-MON')")
        
        print("\n18. apply_lookup_table_for_columns")
        print("    - Description: Equivalent of xlookup in excel. Allows you to map a dictionary of substrings within a column. If multiple columns are need for the LUT then a | seperator is needed.")
        print("    - Usage: apply_lookup_table_for_columns(df, col_names, to_find_dict, if_not_in_dict='Other', new_column_name='Mapping')")
        print("    - Example: apply_lookup_table_for_columns(df, col_names, {'spend':'spd','clicks':'clk'}, if_not_in_dict='Other', new_column_name='Metrics Short')")

        print("\n19. aggregate_daily_to_wc_wide")
        print("   - Description: Aggregates daily data into weekly data, grouping and summing specified columns, starting on a specified day of the week.")
        print("   - Usage: aggregate_daily_to_wc_wide(df, date_column, group_columns, sum_columns, wc, aggregation='sum', include_totals=False)")
        print("   - Example: aggregate_daily_to_wc_wide(df, 'date', ['platform'], ['cost', 'impressions', 'clicks'], 'mon', 'average', True)")

        print("\n20. merge_cols_with_seperator")
        print("   - Description: Merge multiple columns in a dataframe into 1 column with a seperator '_'.Can be used if multiple columns are needed for a LUT.")
        print("   - Usage: merge_cols_with_seperator(self, df, col_names,seperator='_',output_column_name = 'Merged',starting_prefix_str=None,ending_prefix_str=None)")
        print("   - Example: merge_cols_with_seperator(df, ['Campaign','Product'],seperator='|','Merged Columns',starting_prefix_str='start_',ending_prefix_str='_end')")        

        print("\n21. check_sum_of_df_cols_are_equal")
        print("   - Description: Checks if the sum of two columns in two dataframes are the same, and provides the sums of each column and the difference between them.")
        print("   - Usage: check_sum_of_df_cols_are_equal(df_1,df_2,cols_1,cols_2)")
        print("   - Example: check_sum_of_df_cols_are_equal(df_1,df_2,'Media Cost','Spend')")        

        print("\n22. convert_2_df_cols_to_dict")
        print("   - Description: Can be used to create an LUT. Creates a dictionary using two columns in a dataframe.")
        print("   - Usage: convert_2_df_cols_to_dict(df, key_col, value_col)")
        print("   - Example: convert_2_df_cols_to_dict(df, 'Campaign', 'Channel')")        

        print("\n23. create_FY_and_H_columns")
        print("   - Description: Used to create a financial year, half year, and financial half year column.")
        print("   - Usage: create_FY_and_H_columns(df, index_col, start_date, starting_FY,short_format='No',half_years='No',combined_FY_and_H='No')")
        print("   - Example: create_FY_and_H_columns(df, 'Week (M-S)', '2022-10-03', 'FY2023',short_format='Yes',half_years='Yes',combined_FY_and_H='Yes')")        
        
        print("\n24. keyword_lookup_replacement")
        print("   - Description: Essentially provides an if statement with a xlookup if a value is something. Updates certain chosen values in a specified column of the DataFrame based on a lookup dictionary.")
        print("   - Usage: keyword_lookup_replacement(df, col, replacement_rows, cols_to_merge, replacement_lookup_dict,output_column_name='Updated Column')")
        print("   - Example: keyword_lookup_replacement(df, 'channel', 'Paid Search Generic', ['channel','segment','product'], qlik_dict_for_channel,output_column_name='Channel New')")        

        print("\n25. create_new_version_of_col_using_LUT")
        print("   - Description: Creates a new column in a dataframe, which takes an old column and uses a lookup table to changes values in the new column to reflect the lookup table. The lookup is based on a column in the dataframe.")
        print("   - Usage: create_new_version_of_col_using_LUT(df, keys_col,value_col, dict_for_specific_changes, new_col_name='New Version of Old Col')")
        print("   - Example: keyword_lookup_replacement(df, '*Campaign Name','Campaign Type',search_campaign_name_retag_lut,'Campaign Name New')")        

        print("\n26. convert_df_wide_2_long")
        print("   - Description: Changes a dataframe from wide to long format.")
        print("   - Usage: convert_df_wide_2_long(df,value_cols,variable_col_name='Stacked',value_col_name='Value')")
        print("   - Example: keyword_lookup_replacement(df, ['Media Cost','Impressions','Clicks'],variable_col_name='Metric')") 
        
        print("\n27. manually_edit_data")
        print("   - Description: Allows the capability to manually update any cell in dataframe by applying filters and chosing a column to edit in dataframe.")
        print("   - Usage: manually_edit_data(df, filters_dict, col_to_change, new_value, change_in_existing_df_col='No', new_col_to_change_name='New', manual_edit_col_name=None, add_notes='No', existing_note_col_name=None, note=None)")
        print("   - Example: keyword_lookup_replacement(df, {'OBS':' <= datetime(2023,1,23)','File_Name':' == 'France media''},'Master Include',1,change_in_existing_df_col = 'Yes',new_col_to_change_name = 'Master Include',manual_edit_col_name = 'Manual Changes')")      

        print("\n28. format_numbers_with_commas")
        print("   - Description: Converts data in numerical format into numbers with commas and a chosen decimal place length.")
        print("   - Usage: format_numbers_with_commas(df, decimal_length_chosen=2)")
        print("   - Example: format_numbers_with_commas(df,1)")         
    
        print("\n29. filter_df_on_multiple_conditions")
        print("   - Description: Filters dataframe on multiple conditions, which come in the form of a dictionary.")
        print("   - Usage: filter_df_on_multiple_conditions(df, filters_dict)")
        print("   - Example: filter_df_on_multiple_conditions(df, {'OBS':' <= datetime(2023,1,23)','File_Name':' == 'France media''})")       

        print("\n30. read_and_concatenate_files")
        print("   - Description: Read and Concatinate all files of one type in a folder.")
        print("   - Usage: read_and_concatenate_files(folder_path, file_type='csv')")
        print("   - Example: read_and_concatenate_files(folder_path, file_type='csv')")  

        print("\n31. remove_zero_values")
        print("   - Description: Remove zero values in a specified column.")
        print("   - Usage: remove_zero_values(self, data_frame, column_to_filter)")
        print("   - Example: remove_zero_values(None, df, 'Funeral_Delivery')")       

        print("\n32. upgrade_outdated_packages")
        print("   - Description: Upgrades all packages.")
        print("   - Usage: upgrade_outdated_packages()")
        print("   - Example: upgrade_outdated_packages()")
        
        print("\n33. convert_mixed_formats_dates")
        print("   - Description: Convert a mix of US and UK dates to datetime.")
        print("   - Usage: convert_mixed_formats_dates(df, datecol)")
        print("   - Example: convert_mixed_formats_dates(df, 'OBS')")
        
        print("\n34. fill_weekly_date_range")
        print("   - Description: Fill in any missing weeks with 0.")
        print("   - Usage: fill_weekly_date_range(df, date_column, freq)")
        print("   - Example: fill_weekly_date_range(df, 'OBS', 'W-MON')")     

        print("\n35. add_prefix_and_suffix")
        print("   - Description: Add Prefix and/or Suffix to Column Headers.")
        print("   - Usage: add_prefix_and_suffix(df, prefix='', suffix='', date_col=None)")
        print("   - Example: add_prefix_and_suffix(df, prefix='media_', suffix='_spd', date_col='obs')") 

        print("\n36. create_dummies")
        print("   - Description: Changes time series to 0s and 1s based off threshold")
        print("   - Usage: create_dummies(df, date_col=None, dummy_threshold=0, add_total_dummy_col='No', total_col_name='total')")
        print("   - Example: create_dummies(df, date_col='obs', dummy_threshold=100, add_total_dummy_col='Yes', total_col_name='med_total_dum')") 

        print("\n37. replace_substrings")
        print("   - Description: Replace substrings in column of strings based off dictionary, can also change column to lower")
        print("   - Usage: replace_substrings(df, column, replacements, to_lower=False, new_column=None)")
        print("   - Example: replace_substrings(df, 'Influencer Handle', replacement_dict, to_lower=True, new_column='Short Version')") 

        print("\n38. add_total_column")
        print("   - Description: Sums all columns with the option to exclude an date column to create a total column")
        print("   - Usage: add_total_column(df, exclude_col=None, total_col_name='Total')")
        print("   - Example: add_total_column(df, exclude_col='obs', total_col_name='total_media_spd')")   
        
        print("\n39. apply_lookup_table_based_on_substring")
        print("    - Description: Equivalent of xlookup in excel, but only based on substrings. If a substring is found in a cell, than look it up in the dictionary. Otherwise use the other label")
        print("    - Usage: apply_lookup_table_based_on_substring(df, column_name, category_dict, new_col_name='Category', other_label='Other')")
        print("    - Example: apply_lookup_table_based_on_substring(df, 'Campaign Name', campaign_dict, new_col_name='Campaign Name Short', other_label='Full Funnel')")
        
        print("\n40. compare_overlap")
        print("    - Description: With two matching dataset, it takes the common columns and rows and takes the difference between them, outputing a differences and total differences table")
        print("    - Usage: compare_overlap(df1, df2, date_col)")
        print("    - Example: compare_overlap(df_1, df_2, 'obs')")        

        print("\n41. week_commencing_2_week_commencing_conversion")
        print("    - Description: Take a week commencing column say sunday and creates a new column with a different week commencing e.g. monday")
        print("    - Usage: week_commencing_2_week_commencing_conversion(df,date_col,week_commencing='sun')")
        print("    - Example: week_commencing_2_week_commencing_conversion(df,'obs,week_commencing='mon')")          

        print("\n42. week_commencing_2_week_commencing_conversion")
        print("    - Description: Take a week commencing column say sunday and creates a new column with a different week commencing e.g. monday")
        print("    - Usage: week_commencing_2_week_commencing_conversion(df,date_col,week_commencing='sun')")
        print("    - Example: week_commencing_2_week_commencing_conversion(df,'obs,week_commencing='mon')")           
        
        
                
    def get_wd_levels(self, levels):
        """
        Gets the current wd of whoever is working on it and gives the options to move the number of levels up.

        Parameters:
        - data_frame: pandas DataFrame
            The input data frame.
        - num_rows_to_remove: int
            The number of levels to move up pathways.

        Returns:
        - Current wd
        """

        directory = os.getcwd()
        for _ in range(levels):
            directory = os.path.dirname(directory)
        return directory

    def remove_rows(self, data_frame, num_rows_to_remove):
        """
        Removes the specified number of rows from the given data frame, including the top row containing column names. 
        The next row will be treated as the new set of column headings.

        Parameters:
        - data_frame: pandas DataFrame
            The input data frame.
        - num_rows_to_remove: int
            The number of rows to remove from the data frame, starting from the original header.

        Returns:
        - pandas DataFrames
            The modified data frame with rows removed and new column headings.

        Raises:
        - TypeError: If num_rows_to_remove is not an integer.
        - ValueError: If num_rows_to_remove is negative or exceeds the total number of rows.
        """
        
        if not isinstance(num_rows_to_remove, int):
            raise TypeError("num_rows_to_remove must be an integer")

        if num_rows_to_remove < 0 or num_rows_to_remove >= len(data_frame):
            raise ValueError("Number of rows to remove must be non-negative and less than the total number of rows in the data frame.")

        if num_rows_to_remove == 0:
            return data_frame

        new_header = data_frame.iloc[num_rows_to_remove - 1]
        modified_data_frame = data_frame[num_rows_to_remove:] 
        modified_data_frame.columns = new_header

        return modified_data_frame
    
    def aggregate_daily_to_wc_long(self, df : pd.DataFrame, date_column : str, group_columns : list[str], sum_columns : list[str], wc : str = 'sun', aggregation : str = 'sum') -> pd.DataFrame:
        """
        Aggregates daily data into weekly data, starting on a specified day of the week, 
        and groups the data by additional specified columns. It aggregates specified numeric columns 
        by summing, averaging, or counting them, and pivots the data to create separate columns for each combination 
        of the group columns and sum columns. NaN values are replaced with 0 and the index is reset. 
        The day column is renamed from 'Day' to 'OBS'.

        Parameters:
        - df: pandas DataFrame
            The input DataFrame containing daily data.
        - date_column: string
            The name of the column in the DataFrame that contains date information.
        - group_columns: list of strings
            Additional column names to group by along with the weekly grouping.
        - sum_columns: list of strings
            Numeric column names to be aggregated during aggregation.
        - wc: string
            The week commencing day (e.g., 'sun' for Sunday, 'mon' for Monday).
        - aggregation: string, optional (default 'sum')
            Aggregation method, either 'sum', 'average', or 'count'.

        Returns:
        - pandas DataFrame
            A new DataFrame with weekly aggregated data. The index is reset,
            and columns represent the grouped and aggregated metrics. The DataFrame 
            is in long format, with separate columns for each combination of 
            grouped metrics.
        """

        # Map the input week commencing day to a weekday number (0=Monday, 6=Sunday)
        days = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}
        if wc.lower() not in days:
            return print(f"Incorrect week commencing day input: '{wc}'. Please choose a valid day of the week (e.g., 'sun', 'mon', etc.).")

        start_day = days[wc.lower()]

        # Make a copy of the DataFrame
        df_copy = df.copy()

        # Convert the date column to datetime
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])

        # Determine the start of each week
        df_copy['week_start'] = df_copy[date_column].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - start_day) % 7))

        # Convert sum_columns to numeric and fill NaNs with 0, retaining decimal values
        for col in sum_columns:
            df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce').fillna(0)

        # Group by the new week start column and additional columns, then aggregate the numeric columns
        if aggregation == 'average':
            grouped = df_copy.groupby(['week_start'] + group_columns)[sum_columns].mean().reset_index()
        elif aggregation == 'count':
            grouped = df_copy.groupby(['week_start'] + group_columns)[sum_columns].count().reset_index()
        else:  # Default to 'sum' if any other value is provided
            grouped = df_copy.groupby(['week_start'] + group_columns)[sum_columns].sum().reset_index()

        # Rename 'week_start' column to 'OBS'
        grouped = grouped.rename(columns={'week_start': 'OBS'})

        return grouped
    
    def convert_monthly_to_daily(self, df, date_column, divide = True):
        """
        Convert a DataFrame with monthly data to daily data.
        This function takes a DataFrame and a date column, then it expands each
        monthly record into daily records by dividing the numeric values by the number of days in that month.

        :param df: DataFrame with monthly data.
        :param date_column: The name of the column containing the date.
        :param divide: boolean divide by the number of days in a month (default True)
        :return: A new DataFrame with daily data.
        """

        # Convert date_column to datetime
        df[date_column] = pd.to_datetime(df[date_column])

        # Initialize an empty list to hold the daily records
        daily_records = []

        # Iterate over each row in the DataFrame
        for _, row in df.iterrows():
            # Calculate the number of days in the month
            num_days = calendar.monthrange(row[date_column].year, row[date_column].month)[1]

            # Create a new record for each day of the month
            for day in range(1, num_days + 1):
                daily_row = row.copy()
                daily_row[date_column] = row[date_column].replace(day=day)

                # Divide each numeric value by the number of days in the month
                for col in df.columns:
                    if pd.api.types.is_numeric_dtype(df[col]) and col != date_column:
                        if divide == True:
                            daily_row[col] = row[col] / num_days
                        else: 
                            daily_row[col] = row[col]
                daily_records.append(daily_row)

        # Convert the list of daily records into a DataFrame
        daily_df = pd.DataFrame(daily_records)
        
        return daily_df
    
    def plot_two(self, df1, col1, df2, col2, date_column, same_axis=True):
        """
        Plots specified columns from two different dataframes with both different and the same lengths,
        using a specified date column as the X-axis, and charting on either the same or separate y axes.

        :param df1: First DataFrame
        :param col1: Column name from the first DataFrame
        :param df2: Second DataFrame
        :param col2: Column name from the second DataFrame
        :param date_column: The name of the date column to use for the X-axis
        :param same_axis: If True, plot both traces on the same y-axis; otherwise, use separate y-axes.
        :return: Plotly figure
        """
        # Ensure date columns are datetime
        df1[date_column] = pd.to_datetime(df1[date_column])
        df2[date_column] = pd.to_datetime(df2[date_column])
        
        # Create traces for the first and second dataframes
        trace1 = go.Scatter(x=df1[date_column], y=df1[col1], mode='lines', name=col1, yaxis='y1')
        
        if same_axis:
            trace2 = go.Scatter(x=df2[date_column], y=df2[col2], mode='lines', name=col2, yaxis='y1')
        else:
            trace2 = go.Scatter(x=df2[date_column], y=df2[col2], mode='lines', name=col2, yaxis='y2')
            
        # Define layout for the plot
        layout = go.Layout(
            title="",
            xaxis=dict(title="OBS", showline=True, linecolor='black'),
            yaxis=dict(title="", showline=True, linecolor='black', rangemode='tozero'),
            yaxis2=dict(title="", overlaying='y', side='right', showline=True, linecolor='black', rangemode='tozero'),
            showlegend=True,
            plot_bgcolor='white'  # Set the plot background color to white
        )

        # Create the figure with the defined layout and traces
        fig = go.Figure(data=[trace1, trace2], layout=layout)

        return fig

    def remove_nan_rows(self, df, col_to_remove_rows):
    # This line drops rows where the specified column has NaN values
        return df.dropna(subset=[col_to_remove_rows])
    
    def filter_rows(self, df, col_to_filter, list_of_filters):
    # This line filters the DataFrame based on whether the values in the specified column are in the list_of_filters
        return df[df[col_to_filter].isin(list_of_filters)]
    
    def plot_one(self, df1, col1, date_column):
        """
        Plots specified column from a DataFrame with white background and black axes,
        using a specified date column as the X-axis.

        :param df1: DataFrame
        :param col1: Column name from the DataFrame
        :param date_column: The name of the date column to use for the X-axis
        """

        # Check if columns exist in the DataFrame
        if col1 not in df1.columns or date_column not in df1.columns:
            raise ValueError("Column not found in DataFrame")

        # Check if the date column is in datetime format, if not convert it
        if not pd.api.types.is_datetime64_any_dtype(df1[date_column]):
            df1[date_column] = pd.to_datetime(df1[date_column])

        # Plotting using Plotly Express
        fig = px.line(df1, x=date_column, y=col1)

        # Update layout for white background and black axes lines, and setting y-axis to start at 0
        fig.update_layout(
            plot_bgcolor='white',
            xaxis=dict(
                showline=True,
                linecolor='black'
            ),
            yaxis=dict(
                showline=True,
                linecolor='black',
                rangemode='tozero'  # Setting Y-axis to start at 0 if suitable
            )
        )

        return fig

    def week_of_year_mapping(self,df, week_col, start_day_str):

        # Mapping of string day names to day numbers (1 for Monday, 7 for Sunday)
        day_mapping = {
            'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7
        }

        # Convert the day string to a number, or raise an error if not valid
        start_day = day_mapping.get(start_day_str.lower())
        if start_day is None:
            raise ValueError(f"Invalid day input: '{start_day_str}'. Please use one of 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'.")

        # Function to convert week number to start date of the week
        def week_to_startdate(week_str, start_day):
            year, week = map(int, week_str.split('-W'))
            first_day_of_year = datetime(year, 1, 1)
            first_weekday_of_year = first_day_of_year.weekday()  # Monday is 0 and Sunday is 6

            # Calculate days to adjust to the desired start day of the week
            days_to_adjust = (start_day - 1 - first_weekday_of_year) % 7
            start_of_iso_week = first_day_of_year + timedelta(days=days_to_adjust)

            # Calculate the start of the desired week
            start_of_week = start_of_iso_week + timedelta(weeks=week - 1)
            return start_of_week

        # Apply the function to each row in the specified week column
        df['OBS'] = df[week_col].apply(lambda x: week_to_startdate(x, start_day)).dt.strftime('%d/%m/%Y')
        return df
    
    def exclude_rows(self, df, col_to_filter, list_of_filters):
        # This line filters the DataFrame based on whether the values in the specified column are not in the list_of_filters
        return df[~df[col_to_filter].isin(list_of_filters)]
    
    def rename_cols(self, df, name = 'ame_'):
        new_columns = {}
        for col in df.columns:
            if col != 'OBS':
                new_col_name = name + col.replace(" ", "_").lower()
            else:
                new_col_name = col
            new_columns[col] = new_col_name
        return df.rename(columns=new_columns)
    
    def merge_new_and_old(self, old_df, old_col, new_df, new_col, cutoff_date, date_col_name='OBS'):
        """
        Creates a new DataFrame with two columns: one for dates and one for merged numeric values.
        Merges numeric values from specified columns in the old and new DataFrames based on a given cutoff date.

        Parameters:
        - old_df: pandas DataFrame
            The old DataFrame from which to take the numeric values up to the specified date.
        - old_col: str
            The name of the numeric column in the old DataFrame whose values are to be taken.
        - new_df: pandas DataFrame
            The new DataFrame from which to take the numeric values from the specified date onwards.
        - new_col: str
            The name of the numeric column in the new DataFrame whose values are to be taken.
        - cutoff_date: str
            The cut-off date in 'YYYY-MM-DD' format to split the data between the two DataFrames.
        - date_col_name: str, optional (default 'OBS')
            The name of the date column in both DataFrames.

        Returns:
        - pandas DataFrame
            A new DataFrame with two columns: 'Date' and a column named after 'new_col' containing merged numeric values.
        """

        # Convert date columns in both dataframes to datetime for comparison
        old_df[date_col_name] = pd.to_datetime(old_df[date_col_name])
        new_df[date_col_name] = pd.to_datetime(new_df[date_col_name])

        # Convert the cutoff date string to datetime
        cutoff_date = pd.to_datetime(cutoff_date)

        # Split old and new dataframes based on the cutoff date
        old_values = old_df[old_df[date_col_name] <= cutoff_date]
        new_values = new_df[new_df[date_col_name] > cutoff_date]

        # Create a new DataFrame with two columns: 'Date' and a column named after 'new_col'
        merged_df = pd.DataFrame({
            'OBS': pd.concat([old_values[date_col_name], new_values[date_col_name]], ignore_index=True),
            new_col: pd.concat([old_values[old_col], new_values[new_col]], ignore_index=True)
        })

        return merged_df
    
    def merge_dataframes_on_column(self, dataframes, common_column='OBS', merge_how='outer'):
        """
        Merge a list of DataFrames on a common column.

        Parameters:
        - dataframes: A list of DataFrames to merge.
        - common_column: The name of the common column to merge on.
        - merge_how: The type of merge to perform ('inner', 'outer', 'left', or 'right').

        Returns:
        - A merged DataFrame.
        """
        if not dataframes:
            return None
        
        merged_df = dataframes[0]  # Start with the first DataFrame

        for df in dataframes[1:]:
            merged_df = pd.merge(merged_df, df, on=common_column, how=merge_how)

        # Check if the common column is of datetime dtype
        if merged_df[common_column].dtype == 'datetime64[ns]':
            merged_df[common_column] = pd.to_datetime(merged_df[common_column])
        merged_df = merged_df.sort_values(by=common_column)
        merged_df = merged_df.fillna(0)
        
        return merged_df
    
    def merge_and_update_dfs(self, df1, df2, key_column):
        """
        Merges two dataframes on a key column, updates the first dataframe's columns with the second's where available,
        and returns a dataframe sorted by the key column.

        Parameters:
        df1 (DataFrame): The first dataframe to merge (e.g., processed_facebook).
        df2 (DataFrame): The second dataframe to merge (e.g., finalised_meta).
        key_column (str): The name of the column to merge and sort by (e.g., 'OBS').

        Returns:
        DataFrame: The merged and updated dataframe.
        """

        # Sort both DataFrames by the key column
        df1_sorted = df1.sort_values(by=key_column)
        df2_sorted = df2.sort_values(by=key_column)

        # Perform the full outer merge
        merged_df = pd.merge(df1_sorted, df2_sorted, on=key_column, how='outer', suffixes=('', '_finalised'))

        # Update with non-null values from df2
        for column in merged_df.columns:
            if column.endswith('_finalised'):
                original_column = column.replace('_finalised', '')
                merged_df.loc[merged_df[column].notnull(), original_column] = merged_df.loc[merged_df[column].notnull(), column]
                merged_df.drop(column, axis=1, inplace=True)

        # Sort the merged DataFrame by the key column
        merged_df.sort_values(by=key_column, inplace=True)

        # Handle null values (optional, can be adjusted as needed)
        merged_df.fillna(0, inplace=True)

        return merged_df
    
    def convert_us_to_uk_dates(self, df, date_col):
        """
        Processes the date column of a DataFrame to remove hyphens and slashes, 
        and converts it to a datetime object.
        
        Parameters:
        df (pd.DataFrame): The DataFrame containing the date column.
        date_col (str): The name of the date column.
        
        Returns:
        pd.DataFrame: The DataFrame with the processed date column.
        """
        df[date_col] = df[date_col].str.replace(r'[-/]', '', regex=True)
        df[date_col] = pd.to_datetime(
            df[date_col].str.slice(0, 2) + '/' +
            df[date_col].str.slice(2, 4) + '/' +
            df[date_col].str.slice(4, 8),
            format='%m/%d/%Y'
        )
        return df

    def combine_sheets(self, all_sheets):
        """
        Combines multiple DataFrames from a dictionary into a single DataFrame.
        Adds a column 'SheetName' indicating the origin sheet of each row.

        Parameters:
        all_sheets (dict): A dictionary of DataFrames, typically read from an Excel file with multiple sheets.

        Returns:
        DataFrame: A concatenated DataFrame with an additional 'SheetName' column.
        """
        combined_df = pd.DataFrame()

        for sheet_name, df in all_sheets.items():
            df['SheetName'] = sheet_name 
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        return combined_df
    
    def pivot_table(self, df, index_col, columns, values_col, filters_dict=None, fill_value=0, aggfunc='sum', margins=False, margins_name="Total", datetime_trans_needed=True, reverse_header_order=False,fill_missing_weekly_dates=False,week_commencing='W-MON'):
        """
        Provides the ability to create pivot tables, filtering the data to get to data you want and then pivoting on certain columns

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            index_col (str): Name of Column for your pivot table to index on
            columns (str): Name of Columns for your pivot table.
            values_col (str): Name of Values Columns for your pivot table.
            filters_dict (dict, optional): Dictionary of conditions for the boolean mask i.e. what to filter your df on to get to your chosen cell. Defaults to None
            fill_value (int, optional): The value to replace nan with. Defaults to 0.
            aggfunc (str, optional): The method on which to aggregate the values column. Defaults to sum.
            margins (bool, optional): Whether the pivot table needs a total rows and column. Defaults to False.
            margins_name (str, optional): The name of the Totals columns. Defaults to "Total".
            datetime_trans_needed (bool, optional): Whether the index column needs to be transformed into datetime format. Defaults to False.
            reverse_header_order (bool, optional): Reverses the order of the column headers. Defaults to False.
            fill_missing_weekly_dates (bool, optional): Fills in any weekly missing dates. Defaults to False.
            week_commencing (str,optional): Fills in missing weeks if option is specified. Defaults to 'W-MON'.

        Returns:
            pandas.DataFrame: The pivot table specified
        """
        
        # Create the filtered df by applying the conditions
        if filters_dict is None:
            df_filtered = df
        else:
            df_filtered = self.filter_df_on_multiple_conditions(df, filters_dict)
        
        # Ensure index column is in datetime format for proper sorting
        df_filtered = df_filtered.copy()
        
        # If datetime transformation is needed
        if datetime_trans_needed:
            df_filtered[index_col] = pd.to_datetime(df_filtered[index_col], dayfirst=True)
        
        # Create the pivot table
        pivoted_df = df_filtered.pivot_table(index=index_col, columns=columns, values=values_col, aggfunc=aggfunc, margins=margins, margins_name=margins_name)
            
        # Handling MultiIndex columns if present, making them a flat structure
        if not reverse_header_order:
            if isinstance(pivoted_df.columns, pd.MultiIndex):
                pivoted_df.columns = ['_'.join(map(str, col)).strip() for col in pivoted_df.columns.values]
            else:
                pivoted_df.columns = pivoted_df.columns.map(str)
        else:
            if isinstance(pivoted_df.columns, pd.MultiIndex):
                # Reorder the MultiIndex columns
                pivoted_df.columns = ['_'.join(reversed(list(map(str, col)))).strip() for col in pivoted_df.columns.values]
            else:
                pivoted_df.columns = pivoted_df.columns.map(str)
                # Reverse the order for single index columns
                pivoted_df.columns = ['_'.join(reversed(col.split('_'))).strip() for col in pivoted_df.columns]
        
        # Reset the pivot before returning
        pivoted_df = pivoted_df.reset_index()
        
        # Sort by index column from oldest to newest
        if datetime_trans_needed:
            pivoted_df[index_col] = pd.to_datetime(pivoted_df[index_col])  # Ensure sorting works correctly
            pivoted_df = pivoted_df.sort_values(by=index_col)
            
            # Convert index column back to a string in YYYY-MM-DD format for display purposes
            pivoted_df[index_col] = pivoted_df[index_col].dt.strftime('%Y-%m-%d')
        
        # Fill in any NaNs
        pivoted_df = pivoted_df.fillna(fill_value)
        
        # If there is a need to fill in missing weeks
        if fill_missing_weekly_dates == True:
            pivoted_df = self.fill_weekly_date_range(pivoted_df, index_col, freq=week_commencing)

        return pivoted_df

    def apply_lookup_table_for_columns(self, df, col_names, to_find_dict, if_not_in_dict="Other", new_column_name="Mapping"):
        """
        Creates a new DataFrame column based on a look up table, possibly with multiple columns to look up on (dictionary of substrings to class mappings).

        Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        col_names (list of str): these are the columns which are used for the lookup. One column or several columns can be inputted as a list, provided there is a merged column to lookup on. If there are multiple columns to look up on then a merged column must be inputted as the key of the dictionary of format e.g. col1|col2|col3
        to_find_dict (dict): your look up table, where keys are the values being looked up, and the values are the resulting mappings. 
        if_not_in_dict (str, optional): default value if no substring matches are found in the look up table dictionary. Defaults to "Other".
        new_column_name (str, optional): name of new column. Defaults to "Mapping".

        Returns:
        pandas.DataFrame: DataFrame with a new column containing the look up table results.
        """

        # Create regex pattern from the dictionary keys
        regex_pattern = "|".join(re.escape(key) for key in to_find_dict.keys())
        
        # Preprocess DataFrame if multiple columns
        if len(col_names) > 1:
            df["Merged"] = df[col_names].astype(str).apply('|'.join, axis=1)
            col_to_use = "Merged"
        else:
            col_to_use = col_names[0]

        # Extract the first match using the regex pattern
        matches = df[col_to_use].str.extract(f'({regex_pattern})', expand=False, flags=re.IGNORECASE)
        
        # Map the matches to the corresponding values in the dictionary
        df[new_column_name] = matches.str.lower().map({k.lower(): v for k, v in to_find_dict.items()}).fillna(if_not_in_dict)
        
        # Drop intermediate column if created
        if len(col_names) > 1:
            df.drop(columns=["Merged"], inplace=True)

        return df

    def aggregate_daily_to_wc_wide(self, df : pd.DataFrame, date_column : str, group_columns : list[str], sum_columns : list[str], wc : str = 'sun', aggregation : str = 'sum', include_totals : bool = False) -> pd.DataFrame:
        """
        Aggregates daily data into weekly data, starting on a specified day of the week, 
        and groups the data by additional specified columns. It aggregates specified numeric columns 
        by summing, averaging, or counting them, and pivots the data to create separate columns for each combination 
        of the group columns and sum columns. NaN values are replaced with 0 and the index is reset. 
        The day column is renamed from 'Day' to 'OBS'.

        Parameters:
        - df: pandas DataFrame
            The input DataFrame containing daily data.
        - date_column: string
            The name of the column in the DataFrame that contains date information.
        - group_columns: list of strings
            Additional column names to group by along with the weekly grouping.
        - sum_columns: list of strings
            Numeric column names to be aggregated during aggregation.
        - wc: string
            The week commencing day (e.g., 'sun' for Sunday, 'mon' for Monday).
        - aggregation: string, optional (default 'sum')
            Aggregation method, either 'sum', 'average', or 'count'.
        - include_totals: boolean, optional (default False)
            If True, include total columns for each sum_column.

        Returns:
        - pandas DataFrame
            A new DataFrame with weekly aggregated data. The index is reset,
            and columns represent the grouped and aggregated metrics. The DataFrame 
            is in wide format, with separate columns for each combination of 
            grouped metrics.
        """
        
        grouped = self.aggregate_daily_to_wc_long(df, date_column, group_columns, sum_columns, wc, aggregation)
        
        # Pivot the data to wide format
        if group_columns:
            wide_df = grouped.pivot_table(index='OBS', 
                                        columns=group_columns, 
                                        values=sum_columns,
                                        aggfunc='first')
            # Flatten the multi-level column index and create combined column names
            wide_df.columns = ['_'.join(col).strip() for col in wide_df.columns.values]
        else:
            wide_df = grouped.set_index('OBS')

        # Fill NaN values with 0
        wide_df = wide_df.fillna(0)

        # Adding total columns for each unique sum_column, if include_totals is True
        if include_totals:
            for col in sum_columns:
                total_column_name = f'Total {col}'
                if group_columns:
                    columns_to_sum = [column for column in wide_df.columns if col in column]
                else:
                    columns_to_sum = [col]
                wide_df[total_column_name] = wide_df[columns_to_sum].sum(axis=1)

        # Reset the index of the final DataFrame
        wide_df = wide_df.reset_index()

        return wide_df

    def merge_cols_with_seperator(self, df, col_names,seperator='_',output_column_name = "Merged",starting_prefix_str=None,ending_prefix_str=None):
        """
        Creates a new column in the dataframe that merges 2 or more columns together with a "_" seperator, possibly to be used for a look up table where multiple columns are being looked up

        Parameters:
        df (pandas.DataFrame): Dataframe to make changes to.
        col_names (list): list of columm names ot merge.
        seperator (str, optional): Name of column outputted. Defaults to "_".
        output_column_name (str, optional): Name of column outputted. Defaults to "Merged".
        starting_prefix_str (str, optional): string of optional text to be added before the merged column str value
        ending_prefix_str (str, optional): string of optional text to be added after the merged column str value

        Raises:
        ValueError: if more less than two column names are inputted in the list there is nothing to merge on

        Returns:
        pandas.DataFrame: DataFrame with additional merged column
        """
        # Specify more than one column must be entered
        if len(col_names) < 2:
            raise ValueError("2 or more columns must be specified to merge")
        
        # Create a new column with the merged columns
        df[output_column_name] = df[col_names].astype(str).apply(seperator.join, axis=1)

        # Add string before 
        if starting_prefix_str is not None:
            df[output_column_name] = starting_prefix_str + df[output_column_name].astype(str)
        
        # Add string after
        if ending_prefix_str is not None:
            df[output_column_name] = df[output_column_name].astype(str) + ending_prefix_str
                    
        return df

    def check_sum_of_df_cols_are_equal(self, df_1,df_2,cols_1,cols_2):
        """
        Checks the sum of two different dataframe column or columns are equal

        Parameters:
        df_1 (pandas.DataFrame): First dataframe for columnsa to be summed on.
        df_2 (pandas.DataFrame): Second dataframe for columnsa to be summed on.
        cols_1 (list of str): Columns from first dataframe to sum.
        cols_2 (list of str): Columns from second dataframe to sum.

        Returns:
        Tuple: Answer is the true or false answer to whether sums are the same, df_1_sum is the sum of the column/columns in the first dataframe, df_2_sum is the sum of the column/columns in the second dataframe
        """
        # Find the sum of both sets of columns
        df_1_sum = df_1[cols_1].sum().sum()
        df_2_sum = df_2[cols_2].sum().sum()
        
        # If the the two columns are 
        if df_1_sum == df_2_sum:
            Answer = "They are equal"
        if df_1_sum != df_2_sum:
            Answer = "They are different by " + str(df_2_sum-df_1_sum)     
            
        return Answer,df_1_sum,df_2_sum
    
    def convert_2_df_cols_to_dict(self, df, key_col, value_col):
        """
        Create a dictionary mapping from two columns of a DataFrame.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        key_col (str): The column name to use as keys in the dictionary.
        value_col (str): The column name to use as values in the dictionary.

        Returns:
        dict: A dictionary with keys from 'key_col' and values from 'value_col'.
        """
        if key_col not in df or value_col not in df:
            raise ValueError("Specified columns are not in the DataFrame")

        return {df[key_col].iloc[i]: df[value_col].iloc[i] for i in range(len(df))}
    
    def create_FY_and_H_columns(self, df, index_col, start_date, starting_FY,short_format="No",half_years="No",combined_FY_and_H="No"):
        """
        Creates new DataFrame columns containing companies' Financial Year, Half Years and Financial Half years, based on the start date of the first full financial year 

        Parameters:
        df (pandas.DataFrame): Dataframe to operate on.
        index_col (str): Name of the column to use for datetime
        start_date (str): String used to specify the start date of an FY specified, needs to be of format "yyyy-mm-dd" e.g. 2021-11-31
        starting_FY (str): String used to specify which FY the start date refers to, needs to be formatted LONG e.g. FY2021
        short_format (str, optional): String used to specify if short format is desired (e.g. FY21) or if long format is desired (e.g. FY2021). Defaults to "No".
        half_years (str, optional): String used to specify if half year column is desired. Defaults to "No".
        combined_FY_and_H (str, optional): String used to specify is a combined half year and FY column is desired. Defaults to "No".

        Returns:
        pandas.DataFrame: DataFrame with a new column 'FY' containing the FY as well as, if desired, a half year column and a combined FY half year column.
        """
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            print("Error: Date must be of format yyyy-mm-dd")
            return df
        
        df["OBS"] = pd.to_datetime(df[index_col])
        df["OBS as string"] = df["OBS"].dt.strftime("%Y-%m-%d")

        df[index_col] = pd.to_datetime(df[index_col])

        start_year = int(starting_FY[2:])

        def calculate_FY_vectorized(date_series):
            years_since_start = ((date_series - start_date).dt.days / 364).astype(int)
            fy = 'FY' + (start_year + years_since_start).astype(str)
            if short_format == "Yes":
                fy = 'FY' + fy.str[-2:]
            return fy

        df['FY'] = calculate_FY_vectorized(df[index_col])

        if half_years == "Yes" or combined_FY_and_H == "Yes":
            def calculate_half_year_vectorized(date_series):
                fy_years_since_start = ((date_series - start_date).dt.days / 364).astype(int)
                fy_start_dates = start_date + fy_years_since_start * pd.DateOffset(years=1)
                fy_end_of_h1 = fy_start_dates + pd.DateOffset(weeks=26) - pd.DateOffset(weeks=1)
                half_year = np.where(date_series <= fy_end_of_h1, 'H1', 'H2')
                return half_year
            
            df['Half Years'] = calculate_half_year_vectorized(df[index_col])
        
        if combined_FY_and_H == "Yes":
            df['Financial Half Years'] = df['FY'] + ' ' + df['Half Years']

        return df
    
    def keyword_lookup_replacement(self, df, col, replacement_rows, cols_to_merge, replacement_lookup_dict,output_column_name="Updated Column"):
        """
        This function updates values in a specified column of the DataFrame based on a lookup dictionary.
        It first merges several columns into a new 'Merged' column, then uses this merged column to determine
        if replacements are needed based on the dictionary.

        Parameters:
        df (pd.DataFrame): The DataFrame to process.
        col (str): The name of the column whose values are potentially replaced.
        replacement_rows (str): The specific value in 'col' to check for replacements.
        cols_to_merge (list of str): List of column names whose contents will be merged to form a lookup key.
        replacement_lookup_dict (dict): Dictionary where keys are merged column values and values are the new data to replace in 'col'.
        output_column_name (str, optional): Name of column outputted. Defaults to "Updated Column".

        Returns:
        pd.DataFrame: The modified DataFrame with updated values in the specified column.
        """
        df["Merged"] = df[cols_to_merge].apply(lambda row: '|'.join(row.values.astype(str)), axis=1)
        
        def replace_values(x):
            if x[col] == replacement_rows:
                merged_value = x['Merged']  
                if merged_value in replacement_lookup_dict:
                    return replacement_lookup_dict[merged_value]
            return x[col]
        
        df[output_column_name] = df.apply(replace_values, axis=1)
        
        return df
    
    def create_new_version_of_col_using_LUT(self, df, keys_col,value_col, dict_for_specific_changes, new_col_name="New Version of Old Col"):
        """
        Creates a new column in a dataframe, which takes an old column and uses a lookup table to changes values in the new column to reflect the lookup table. 
        The lookup is based on a column in the dataframe. Can only input one column and output one new column.

        Parameters:
            df (pandas.DataFrame): The DataFrame containing the data.
            keys_col (str): The name of the column which the LUT will be refercing to ouput a value.
            value_col (str): The name of the column which the new column will be based off. If a key in the key column is not found in the LUT, the values from this column are used instead.
            dict_for_specific_changes (dict): The LUT which the keys_col will be mapped on to find any values that need changing in the new column.
            new_col_name (str, optional): This is the name of the new column being generated. Defaults to "New Version of Old Col".

        Returns:
        pandas.DataFrame: DataFrame with a new column which is similar to the old column, except for where changes have been made to reflect the lookup table.
        """
    
        # Extract columns to change using new dictionary
        smaller_df = df[[keys_col,value_col]]

        # Use the new dictionary to create a new LUT
        smaller_df_with_LUT = self.apply_lookup_table_for_columns(smaller_df,[keys_col,value_col],dict_for_specific_changes)
        
        # In a new column, keep values from the old column that don't need updating as they are not in the dictionary, and replace values that do need updating with values from the dictionary based on the keys
        smaller_df_with_LUT["Updated Col"]=smaller_df_with_LUT.apply(lambda x: x['Mapping'] if x['Mapping'] != "Other" else x[value_col],axis=1)

        # Drop the extra unecessary cols
        smaller_df_with_LUT.drop([keys_col,'Mapping'],axis=1,inplace=True)
        
        # # Output dataframes as dictionary to be used in a LUT
        new_dict = self.convert_2_df_cols_to_dict(smaller_df_with_LUT,value_col,"Updated Col")

        # # Use new dictionary to create a new version of an old column
        df_final = self.apply_lookup_table_for_columns(df,[keys_col],new_dict,"other",new_col_name)
        
        return df_final
    
    def convert_df_wide_2_long(self, df,value_cols,variable_col_name='Stacked',value_col_name='Value'):
        """
        Changes a dataframe from wide to long format.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            value_cols (list of str or str if only one): list of column names which are to be transformed from several columns into one.
            variable_col_name (str, optional): Name of new variables column, which contains the names of the columns which have been stacked into one. Defaults to 'Stacked'.
            value_col_name (str, optional): Name of the new value column which contains all the data from the stacked columns. Defaults to 'Value'.

        Returns:
            pandas.DataFrame:: Returns dataframe transformed from long to wide.
            
        Raises:
            ValueError: If number of column names to be depivoted is less than 2, then this function is not neccesary.
        """
        
        # Check length of value cols is greater than 1
        if len(value_cols) < 2:
            raise ValueError("Number of inputs in list must be greater than 1")
        
        # Find the columns that are not to be depivoted into one column
        id_vars = list(set(df.columns.tolist()) - set(value_cols))
        
        # Melt all columns chosen into one column
        df_final = pd.melt(df, id_vars,value_cols,var_name=variable_col_name,value_name=value_col_name)
        
        return df_final
    
    def manually_edit_data(self, df, filters_dict, col_to_change, new_value, change_in_existing_df_col="No", new_col_to_change_name='New', manual_edit_col_name=None, add_notes="No", existing_note_col_name=None, note=None):
        """
        Allows the capability to manually update any cell in dataframe by applying filters and chosing a column to edit in dataframe

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            filters_dict (dict): Dictionary of conditions for the boolean mask i.e. what to filter your df on to get to your chosen cell
            col_to_change (str): String name of column to edit
            new_value (any): Value of new input for cell
            change_in_existing_df_col (str, optional): Input of Yes or No to describe whether to make the change in an existing column. Defaults to "No".
            new_col_to_change_name (str, optional): Name of the new column to copy the column being edited into and to make the change in. Defaults to 'New'.
            manual_edit_col_name (str, optional): Name of the current manual edits column, if one is not specified it will be created. Defaults to None.
            add_notes (str, optional): Gives the option to create a new notes column. Defaults to "No".
            existing_note_col_name (str, optional): If there is an existing notes column this can be specified. Defaults to None.
            note (str), optional): The string of the note to be added to the column. Defaults to None.

        Raises:
            TypeError: The column for the column to change can only be specified as one column as it is a string not a list
            ValueError: You can only input the values of "Yes" or "No" for whether to make the change in existing column
            ValueError: You can only input the values of "Yes" or "No" for whether to make a new notes column

        Returns:
            pandas.DataFrame: Dataframe with manual changes added
        """
        # Raise type error if more than one col is supported
        if isinstance(col_to_change, list):
            raise TypeError("Col to change must be specified as a string, not a list")
        
        # Raises value error if input is invalid for change_in_existing_df_col
        if change_in_existing_df_col not in ["Yes", "No"]:
            raise ValueError("Invalid input value for change_in_existing_df_col. Allowed values are: ['Yes', 'No']")
        
        # Raises value error if input is invalid for add_notes_col
        if add_notes not in ["Yes", "No"]:
            raise ValueError("Invalid input value for add_notes. Allowed values are: ['Yes', 'No']")

        # Create the filtered df by applying the conditions
        df_filtered = self.filter_df_on_multiple_conditions(df, filters_dict)

        # Create a new column to add the changes if desired, else edit in the current chosen column
        col_to_update = col_to_change if change_in_existing_df_col == "Yes" else new_col_to_change_name
        if change_in_existing_df_col == "No" and new_col_to_change_name not in df.columns:
            df = df.copy()
            df[new_col_to_change_name] = df[col_to_change]
            
        # Update the new cell in the chosen column
        df.loc[df_filtered.index, col_to_update] = new_value

        # Add in manual edit column if desired or specify where one already is
        if manual_edit_col_name:
            if manual_edit_col_name not in df.columns:
                df[manual_edit_col_name] = 0
            df.loc[df_filtered.index, manual_edit_col_name] = 1
        elif not manual_edit_col_name and 'Manual Changes' not in df.columns:
            df['Manual Changes'] = 0
            df.loc[df_filtered.index, 'Manual Changes'] = 1

        # Add note if desired in new column or an existing column
        if add_notes == "Yes":
            note_col = existing_note_col_name if existing_note_col_name else 'Notes'
            if note_col not in df.columns:
                df[note_col] = None
            df.loc[df_filtered.index, note_col] = note

        return df
    
    def format_numbers_with_commas(self, df, decimal_length_chosen=2):
        """
        Converts data in numerical format into numbers with commas and a chosen decimal place length

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            decimal_length_chosen (int, optional): _description_. Defaults to 2.
            
        Returns:
            pandas.DataFrame: The dataframe with the chosen updated format
        """
        def format_number_with_commas(x, decimal_length=decimal_length_chosen):
            if isinstance(x, (int, float)):
                if decimal_length is not None:
                    format_str = "{:,.{}f}".format(x, decimal_length)
                    formatted_number = format_str.format(x)
                else:
                    formatted_number = "{:,}".format(x)
                return formatted_number
            else:
                return x  # Return unchanged if not a number


        # Apply the function across several columns using applymap()
        formatted_df = df.applymap(format_number_with_commas)

        return formatted_df
    
    def filter_df_on_multiple_conditions(self, df, filters_dict):
        """
        Filter a dataframe based on mulitple conditions

        Args:
            df (pandas.DatFrame): Dataframe to filter on
            filters_dict (dict): Dictionary with strings as conditions

        Returns:
            pandas.DatFrame: Filtered Da
        """
        mask = pd.Series(True, index=df.index)
        for col, cond in filters_dict.items():
            cond = cond.strip()
            operator, value = cond.split(maxsplit=1)
            
            # If value is a string condition make sure to check if there are new lines
            if "'" in value:
                value = value.strip().strip("'\"")
            # If not a string e.g. datetime or number condition you need to transform the string into a value
            else:
                value = eval(value)  

            if operator == "==":
                temp_mask = (df[col] == value)
            elif operator == "!=":
                temp_mask = (df[col] != value)
            elif operator == ">=":
                temp_mask = (df[col] >= value)
            elif operator == "<=":
                temp_mask = (df[col] <= value)
            elif operator == ">":
                temp_mask = (df[col] > value)
            elif operator == "<":
                temp_mask = (df[col] < value)                          
            mask &= temp_mask

        # Create the filtered df by applying the conditions
        df_filtered = df[mask]
    
        return df_filtered
    
    def read_and_concatenate_files(self, folder_path, file_type='csv'):
        """
        Reads all files of a specified type (CSV or XLSX) from a given folder 
        and concatenates them into a single DataFrame.
        
        Parameters:
        folder_path (str): The path to the folder containing the files.
        file_type (str): The type of files to read ('csv' or 'xlsx'). Defaults to 'csv'.
        
        Returns:
        pd.DataFrame: A DataFrame containing the concatenated data from all files.
        """
        
        # Initialize an empty list to hold dataframes
        dataframes = []

        # Define file extension based on file_type
        if file_type == 'csv':
            extension = '.csv'
        elif file_type == 'xlsx':
            extension = '.xlsx'
        else:
            raise ValueError("file_type must be either 'csv' or 'xlsx'")

        # Loop through all files in the folder
        for filename in os.listdir(folder_path):
            # Check if the file has the correct extension
            if filename.endswith(extension):
                file_path = os.path.join(folder_path, filename)
                # Read the file into a DataFrame
                if file_type == 'csv':
                    df = pd.read_csv(file_path)
                elif file_type == 'xlsx':
                    df = pd.read_excel(file_path)
                # Append the DataFrame to the list
                dataframes.append(df)

        # Concatenate all DataFrames into a single DataFrame
        combined_df = pd.concat(dataframes, ignore_index=True)
        
        return combined_df
    
    def remove_zero_values(self, data_frame, column_to_filter):
            """
        Removes zero values from given columns

        Parameters:
        df - input data frame
        column_to_filter - a column to filter out zero values from

        Returns:
        Pandas data frame without null values 
        """

        #This line removes zero values from given column
            
            return data_frame.loc[~(data_frame[column_to_filter] ==0)]

    def upgrade_outdated_packages(self):
        try:
            # Get all installed packages
            installed_packages_result = subprocess.run("pip list --format=json", shell=True, capture_output=True, text=True)
            installed_packages = json.loads(installed_packages_result.stdout)

            # Get the list of outdated packages
            outdated_packages_result = subprocess.run("pip list --outdated --format=json", shell=True, capture_output=True, text=True)
            outdated_packages = json.loads(outdated_packages_result.stdout)

            # Create a set of outdated package names for quick lookup
            outdated_package_names = {pkg['name'] for pkg in outdated_packages}

            # Upgrade only outdated packages
            for package in installed_packages:
                package_name = package['name']
                if package_name in outdated_package_names:
                    try:
                        print(f"Upgrading package: {package_name}")
                        upgrade_result = subprocess.run(f"pip install --upgrade {package_name}", shell=True, capture_output=True, text=True)
                        if upgrade_result.returncode == 0:
                            print(f"Successfully upgraded {package_name}")
                        else:
                            print(f"Failed to upgrade {package_name}: {upgrade_result.stderr}")
                    except Exception as e:
                        print(f"An error occurred while upgrading {package_name}: {e}")
                else:
                    print(f"{package_name} is already up to date")
        except Exception as e:
            print(f"An error occurred during the upgrade process: {e}")

    def convert_mixed_formats_dates(self, df, column_name):
        # Convert initial dates to datetime with coercion to handle errors
        df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
        df[column_name] = df[column_name].astype(str)
        corrected_dates = []
        
        for date_str in df[column_name]:
            date_str = date_str.replace('-', '').replace('/', '')
            if len(date_str) == 8:
                year = date_str[:4]
                month = date_str[4:6]
                day = date_str[6:8]
                if int(day) <= 12:
                    # Swap month and day
                    corrected_date_str = f"{year}-{day}-{month}"
                else:
                    corrected_date_str = f"{year}-{month}-{day}"
                # Convert to datetime
                corrected_date = pd.to_datetime(corrected_date_str, errors='coerce')
            else:
                corrected_date = pd.to_datetime(date_str, errors='coerce')
            
            corrected_dates.append(corrected_date)
        
        # Check length of the corrected_dates list
        if len(corrected_dates) != len(df):
            raise ValueError("Length of corrected_dates does not match the original DataFrame")
        
        # Assign the corrected dates back to the DataFrame
        df[column_name] = corrected_dates
        return df

    def fill_weekly_date_range(self, df, date_column, freq='W-MON'):
        # Ensure the date column is in datetime format
        df[date_column] = pd.to_datetime(df[date_column])
        
        # Generate the full date range with the specified frequency
        full_date_range = pd.date_range(start=df[date_column].min(), end=df[date_column].max(), freq=freq)
        
        # Create a new dataframe with the full date range
        full_date_df = pd.DataFrame({date_column: full_date_range})
        
        # Merge the original dataframe with the new full date range dataframe
        df_full = full_date_df.merge(df, on=date_column, how='left')
        
        # Fill missing values with 0
        df_full.fillna(0, inplace=True)
        
        return df_full
    
    def add_prefix_and_suffix(self, df, prefix='', suffix='', date_col=None):
        """
        Adds a specified prefix and/or suffix to the column names of a DataFrame. Optionally, a column (e.g., a date column) can be excluded.

        Args:
        df (pd.DataFrame): The DataFrame whose column names will be modified.
        prefix (str, optional): The prefix to add to each column name. Default is an empty string.
        suffix (str, optional): The suffix to add to each column name. Default is an empty string.
        date_col (str, optional): The name of the column to exclude from adding prefix and suffix, typically a date column. Default is None.

        Returns:
        pd.DataFrame: The DataFrame with updated column names.
        """
        
        # If there is no date column
        if date_col is None:
            # Add prefixes and suffixes to all columns
            df.columns = [prefix + col + suffix for col in df.columns]
        else:
            # Add prefixes and suffixes to all columns except the date column
            df.columns = [prefix + col + suffix if col != date_col else col for col in df.columns]
            
        return df

    def create_dummies(self, df, date_col=None, dummy_threshold=0, add_total_dummy_col='No', total_col_name='total'):
        """
        Creates dummy variables for the DataFrame, converting values greater than the threshold to 1 and others to 0.
        Optionally adds a total dummy column indicating whether any row contains at least one value greater than the threshold.

        Args:
        df (pd.DataFrame): The DataFrame to process.
        date_col (str, optional): The column name to exclude from the dummy conversion, typically a date column. Default is None.
        dummy_threshold (int, optional): The threshold value; values greater than this become 1, others become 0. Default is 0.
        add_total_dummy_col (str, optional): If set to any value other than 'No', adds a column that contains the max value (1 or 0) for each row. Default is 'No'.
        total_col_name (str, optional): The name of the total column to add if add_total_dummy_col is not 'No'. Default is 'total'.

        Returns:
        pd.DataFrame: The modified DataFrame with dummies applied and optional total column.
        """
    
        # If there is no date column
        if date_col is None:
            df = df.applymap(lambda x: 1 if x > dummy_threshold else 0)

            if add_total_dummy_col != 'No':
                # Find max value of rows
                df[total_col_name] = df.max(axis=1)

        # If there is a date column
        else:
            # Create dummies
            df.loc[:, df.columns != date_col] = df.loc[:, df.columns != date_col].applymap(lambda x: 1 if x > dummy_threshold else 0)

            if add_total_dummy_col != 'No':
                # Find max value of rows
                df[total_col_name] = df.loc[:, df.columns != date_col].max(axis=1)

        return df

    def replace_substrings(self, df, column, replacements, to_lower=False, new_column=None):
        """
        Replaces substrings in a column of a DataFrame based on a dictionary of replacements. 
        Optionally converts the column values to lowercase and allows creating a new column or modifying the existing one.

        Args:
        df (pd.DataFrame): The DataFrame containing the column to modify.
        column (str): The column name where the replacements will be made.
        replacements (dict): A dictionary where keys are substrings to replace and values are the replacement strings.
        to_lower (bool, optional): If True, the column values will be converted to lowercase before applying replacements. Default is False.
        new_column (str, optional): If provided, the replacements will be applied to this new column. If None, the existing column will be modified. Default is None.

        Returns:
        pd.DataFrame: The DataFrame with the specified replacements made, and optionally with lowercase strings.
        """
        
        if new_column is not None:
            # Create a new column for replacements
            df[new_column] = df[column]
            temp_column = new_column
        else:
            # Modify the existing column
            temp_column = column
        
        # Apply substring replacements
        for old, new in replacements.items():
            df[temp_column] = df[temp_column].str.replace(old, new, regex=False)
        
        # Optionally convert to lowercase
        if to_lower:
            df[temp_column] = df[temp_column].str.lower()
        
        return df

    def add_total_column(self, df, exclude_col=None, total_col_name='Total'):
        """
        Adds a total column to a DataFrame by summing across all columns. Optionally excludes a specified column.

        Args:
        df (pd.DataFrame): The DataFrame to modify.
        exclude_col (str, optional): The column name to exclude from the sum. Default is None.
        total_col_name (str, optional): The name of the new total column. Default is 'Total'.

        Returns:
        pd.DataFrame: The DataFrame with an added total column.
        """
        # If exclude_col is provided, drop that column before summing
        if exclude_col:
            df[total_col_name] = df.drop(columns=[exclude_col]).sum(axis=1)
        else:
            # Sum across all columns if exclude_col is not provided
            df[total_col_name] = df.sum(axis=1)
        
        return df

    def apply_lookup_table_based_on_substring(self, df, column_name, category_dict, new_col_name='Category', other_label='Other'):
        """
        Categorizes text in a specified DataFrame column by applying a lookup table based on substrings.

        Args:
        df (pd.DataFrame): The DataFrame containing the column to categorize.
        column_name (str): The name of the column in the DataFrame that contains the text data to categorize.
        category_dict (dict): A dictionary where keys are substrings to search for in the text and values are the categories to assign when a substring is found.
        new_col_name (str, optional): The name of the new column to be created in the DataFrame, which will hold the resulting categories. Default is 'Category'.
        other_label (str, optional): The name given to category if no substring from the dictionary is found in the cell

        Returns:
        pd.DataFrame: The original DataFrame with an additional column containing the assigned categories.
        """

        def categorize_text(text):
            """
            Assigns a category to a single text string based on the presence of substrings from a dictionary.

            Args:
            text (str): The text string to categorize.

            Returns:
            str: The category assigned based on the first matching substring found in the text. If no 
            matching substring is found, returns other_name.
            """
            for key, category in category_dict.items():
                if key.lower() in text.lower():  # Check if the substring is in the text (case-insensitive)
                    return category
            return other_label  # Default category if no match is found

        # Apply the categorize_text function to each element in the specified column
        df[new_col_name] = df[column_name].apply(categorize_text)
        return df

    def compare_overlap(df1, df2, date_col):
        """
        Compare overlapping periods between two DataFrames and provide a summary of total differences.

        Args:
            df1 (pandas.DataFrame): First DataFrame containing date-based data.
            df2 (pandas.DataFrame): Second DataFrame containing date-based data.
            date_col (str): The name of the date column used for aligning data.

        Returns:
            tuple: A tuple containing the DataFrame of differences and a summary DataFrame with total differences by column.
        """
        # Ensure date columns are in datetime format
        df1[date_col] = pd.to_datetime(df1[date_col])
        df2[date_col] = pd.to_datetime(df2[date_col])
        
        # Determine the overlap period
        start_date = max(df1[date_col].min(), df2[date_col].min())
        end_date = min(df1[date_col].max(), df2[date_col].max())
        
        # Filter dataframes to the overlapping period
        df1_overlap = df1[(df1[date_col] >= start_date) & (df1[date_col] <= end_date)]
        df2_overlap = df2[(df2[date_col] >= start_date) & (df2[date_col] <= end_date)]
        
        # Merge the dataframes on the date column to align data for comparison
        merged_df = pd.merge(df1_overlap, df2_overlap, on=date_col, suffixes=('_df1', '_df2'))
        
        # Get the common columns between the two DataFrames, excluding the date column
        common_cols = [col for col in df1.columns if col != date_col and col in df2.columns]
        
        # Initialize a list to collect total differences for each column
        total_diff_list = []
        
        # Create a DataFrame for the differences
        diff_df = pd.DataFrame({date_col: merged_df[date_col]})  # Initialize diff_df with the date column
        
        for col in common_cols:
            # Calculate the difference for each row
            diff_col = f'diff_{col}'
            diff_df[diff_col] = merged_df[f'{col}_df1'] - merged_df[f'{col}_df2']
            
            # Calculate the total difference for the column and add it to the list
            total_diff = diff_df[diff_col].sum()
            total_diff_list.append({'Column': col, 'Total Difference': total_diff})
        
        # Create a DataFrame for the summary of total differences
        total_diff_df = pd.DataFrame(total_diff_list)
        
        # Apply formatting to the numerical columns
        float_format = "{:,.2f}".format  # Format to 2 decimal places with comma as thousand separator
        diff_df.iloc[:, 1:] = diff_df.iloc[:, 1:].applymap(float_format)
        total_diff_df['Total Difference'] = total_diff_df['Total Difference'].apply(float_format)
        
        return diff_df, total_diff_df
    
    # Convert week commencing col (should be most likely monday to sunday or vice versa)
    def week_commencing_2_week_commencing_conversion(df,date_col,week_commencing='sun'):
        """
        Convert week commencing column in a DataFrame to the start of another day specified.

        Args:
            df (pandas.DataFrame): The DataFrame containing the date-based data.
            date_col (str): The name of the date column in the DataFrame.
            week_commencing (str, optional): The day of the week that the week starts on ('sun' for Sunday, 'mon' for Monday, etc.). Defaults to 'sun'.

        Returns:
            pandas.DataFrame: The original DataFrame with an additional column indicating the start of the week.
        """
        # Week commencing dictionary
        day_dict = {"mon": 0, "tue": 1, "wed": 2, "thur": 3, "fri": 4, "sat": 5, "sun": 6}
        df['week_start_'+ week_commencing] = df[date_col].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))
        
        return df
    
    def plot_chart(df, date_col, value_cols, chart_type='line', title='Chart', x_title='Date', y_title='Values', **kwargs):
        """
        Plot various types of charts using Plotly.

        Args:
            df (pandas.DataFrame): DataFrame containing the data.
            date_col (str): The name of the column with date information.
            value_cols (list): List of columns to plot.
            chart_type (str): Type of chart to plot ('line', 'bar', 'scatter', 'pie', 'box', 'heatmap', 'area', 'bubble', 'funnel', 'waterfall', 'contour', 'scatter3d').
            title (str): Title of the chart.
            x_title (str): Title of the x-axis.
            y_title (str): Title of the y-axis.
            **kwargs: Additional keyword arguments for customization.

        Returns:
            plotly.graph_objects.Figure: The Plotly figure object.
        """
        # Ensure the date column is in datetime format
        df[date_col] = pd.to_datetime(df[date_col])
        
        # Initialize the figure
        fig = go.Figure()
        
        # Make sure the date col is excluded from the line cols
        value_cols = [x for x in value_cols if x!=date_col]

        # Add each value column to the plot based on the chart type
        for col in value_cols:
            if chart_type == 'line':
                fig.add_trace(go.Scatter(
                    x=df[date_col],
                    y=df[col],
                    mode='lines',
                    name=col,
                    **kwargs
                ))
            elif chart_type == 'bar':
                fig.add_trace(go.Bar(
                    x=df[date_col],
                    y=df[col],
                    name=col,
                    **kwargs
                ))
            elif chart_type == 'scatter':
                fig.add_trace(go.Scatter(
                    x=df[date_col],
                    y=df[col],
                    mode='markers',
                    name=col,
                    **kwargs
                ))
            elif chart_type == 'histogram':
                fig.add_trace(go.Histogram(
                    x=df[col],
                    name=col,
                    **kwargs
                ))
            elif chart_type == 'pie':
                fig.add_trace(go.Pie(
                    labels=df[date_col],  # or another column for labels
                    values=df[col],
                    name=col,
                    **kwargs
                ))
            elif chart_type == 'box':
                fig.add_trace(go.Box(
                    y=df[col],
                    name=col,
                    **kwargs
                ))
            elif chart_type == 'heatmap':
                fig.add_trace(go.Heatmap(
                    z=df.pivot_table(index=date_col, columns=value_cols[0], values=value_cols[1]),
                    x=df[value_cols[0]],
                    y=df[date_col],
                    **kwargs
                ))
            elif chart_type == 'area':
                fig.add_trace(go.Scatter(
                    x=df[date_col],
                    y=df[col],
                    mode='lines',  # Use 'lines+markers' if you want markers
                    fill='tozeroy',  # Fill the area under the line
                    name=col,
                    **kwargs
                ))
            elif chart_type == 'bubble':
                fig.add_trace(go.Scatter(
                    x=df[value_cols[0]],
                    y=df[value_cols[1]],
                    mode='markers',
                    marker=dict(size=df[value_cols[2]]),
                    name='Bubble Chart',
                    **kwargs
                ))
            elif chart_type == 'funnel':
                fig.add_trace(go.Funnel(
                    y=df[date_col],
                    x=df[col],
                    **kwargs
                ))
            elif chart_type == 'waterfall':
                fig.add_trace(go.Waterfall(
                    x=df[date_col],
                    y=df[col],
                    measure=df[value_cols[1]],  # measures like 'increase', 'decrease', 'total'
                    **kwargs
                ))
            elif chart_type == 'contour':
                fig.add_trace(go.Contour(
                    z=df.pivot_table(index=value_cols[0], columns=value_cols[1], values=value_cols[2]),
                    x=df[value_cols[0]],
                    y=df[value_cols[1]],
                    **kwargs
                ))
            elif chart_type == 'scatter3d':
                fig.add_trace(go.Scatter3d(
                    x=df[value_cols[0]],
                    y=df[value_cols[1]],
                    z=df[value_cols[2]],
                    mode='markers',
                    **kwargs
                ))
            else:
                raise ValueError(f"Unsupported chart type: {chart_type}")

        # Update the layout of the figure
        fig.update_layout(
            title=title,
            xaxis_title=x_title,
            yaxis_title=y_title,
            legend_title='Series',
            template='plotly_dark'
        )
        
        return fig
    
########################################################################################################################################
########################################################################################################################################











    
ims_proc = dataprocessing()
    
class datapull:
    
    def help(self):
        print("This is the help section. The functions in the package are as follows:")

        print("\n1. pull_fred_data")
        print("   - Description: Get data from FRED by using series id tokens.")
        print("   - Usage: pull_fred_data(week_commencing, series_id_list)")
        print("   - Example: pull_fred_data('mon', ['GPDIC1', 'Y057RX1Q020SBEA', 'GCEC1', 'ND000333Q', 'Y006RX1Q020SBEA'])")

        print("\n2. pull_boe_data")
        print("   - Description: Fetch and process Bank of England interest rate data.")
        print("   - Usage: pull_boe_data(week_commencing)")
        print("   - Example: pull_boe_data('mon')")

        print("\n3. pull_ons_data")
        print("   - Description: Fetch and process time series data from the ONS API.")
        print("   - Usage: pull_ons_data(series_list, week_commencing)")
        print("   - Example: pull_ons_data([{'series_id': 'LMSBSA', 'dataset_id': 'LMS'}], 'mon')")

        print("\n4. pull_oecd")
        print("   - Description: Fetch macroeconomic data from OECD for a specified country.")
        print("   - Usage: pull_oecd(country='GBR', week_commencing='mon', start_date: '1950-01-01')")
        print("   - Example: pull_oecd('GBR', 'mon', '1950-01-01')")

        print("\n5. get_google_mobility_data")
        print("   - Description: Fetch Google Mobility data for the specified country.")
        print("   - Usage: get_google_mobility_data(country, wc)")
        print("   - Example: get_google_mobility_data('United Kingdom', 'mon')")

        print("\n6. pull_combined_dummies")
        print("   - Description: Generate combined dummy variables for seasonality, trends, and COVID lockdowns.")
        print("   - Usage: pull_combined_dummies(week_commencing)")
        print("   - Example: pull_combined_dummies('mon')")

        print("\n7. pull_weather")
        print("   - Description: Fetch and process historical weather data for the specified country.")
        print("   - Usage: pull_weather(week_commencing, country)")
        print("   - Example: pull_weather('mon', 'GBR')")

        print("\n8. pull_covid_data")
        print("   - Description: Get covid pandemic data for the country of interest.")
        print("   - Usage: pull_covid_data(folder_path, country, week_commencing)")
        print("   - Example: pull_covid_data('C:/Users/--username--/OneDrive/', 'GB', 'mon')")
    
    ###############################################################  MACRO ##########################################################################

    def pull_fred_data(self, week_commencing: str = 'mon', series_id_list: list[str] = ["GPDIC1", "Y057RX1Q020SBEA", "GCEC1", "ND000333Q", "Y006RX1Q020SBEA"]) -> pd.DataFrame:
        '''
        Parameters
        ----------
        week_commencing : str
            specify the day for the week commencing, the default is 'sun' (e.g., 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')

        series_id_list : list[str]
            provide a list with IDs to download data series from FRED (link: https://fred.stlouisfed.org/tags/series?t=id). Default list is 
            ["GPDIC1", "Y057RX1Q020SBEA", "GCEC1", "ND000333Q", "Y006RX1Q020SBEA"]
        
        Returns
        ----------
        pd.DataFrame
            Return a data frame with FRED data according to the series IDs provided

        Example
        ----------
        pull_fred_data("mon", ["GCEC1", "SP500"])
        '''
        # Fred API
        fred = Fred(api_key='76f5f8156145fdb8fbaf66f1eb944f8a')

        # Fetch the metadata for each series to get the full names
        series_names = {series_id: fred.get_series_info(series_id).title for series_id in series_id_list}

        # Download data from series id list
        fred_series = {series_id: fred.get_series(series_id) for series_id in series_id_list}

        # Data processing
        date_range = {'OBS': pd.date_range("1950-01-01", datetime.today().strftime('%Y-%m-%d'), freq='d')}
        fred_series_df = pd.DataFrame(date_range)

        for series_id, series_data in fred_series.items():
            series_data = series_data.reset_index()
            series_data.columns = ['OBS', series_names[series_id]]  # Use the series name as the column header
            fred_series_df = pd.merge_asof(fred_series_df, series_data, on='OBS', direction='backward')

        # Handle duplicate columns
        for col in fred_series_df.columns:
            if '_x' in col:
                base_col = col.replace('_x', '')
                fred_series_df[base_col] = fred_series_df[col].combine_first(fred_series_df[base_col + '_y'])
                fred_series_df.drop([col, base_col + '_y'], axis=1, inplace=True)

        # Ensure sum_columns are present in the DataFrame
        sum_columns = [series_names[series_id] for series_id in series_id_list if series_names[series_id] in fred_series_df.columns]

        # Aggregate results by week
        fred_df_final = ims_proc.aggregate_daily_to_wc_wide(df=fred_series_df, 
                                                    date_column="OBS", 
                                                    group_columns=[], 
                                                    sum_columns=sum_columns,
                                                    wc=week_commencing,
                                                    aggregation="average")

        # Remove anything after the instance of any ':' in the column names and rename, except for 'OBS'
        fred_df_final.columns = ['OBS' if col == 'OBS' else 'macro_' + col.lower().split(':')[0].replace(' ', '_') for col in fred_df_final.columns]

        return fred_df_final
    
    def pull_boe_data(self, week_commencing="mon", max_retries=30, delay=5):
        """
        Fetch and process Bank of England interest rate data.

        Args:
            week_commencing (str): The starting day of the week for aggregation. 
                                Options are "mon", "tue", "wed", "thur", "fri", "sat", "sun". 
                                Default is "sun".
            max_retries (int): Maximum number of retries to fetch data in case of failure. Default is 30.
            delay (int): Delay in seconds between retry attempts. Default is 5.

        Returns:
            pd.DataFrame: A DataFrame with weekly aggregated Bank of England interest rates. 
                        The 'OBS' column contains the week commencing dates in 'dd/mm/yyyy' format 
                        and 'macro_boe_intr_rate' contains the average interest rate for the week.
        """
        # Week commencing dictionary
        day_dict = {"mon": 0, "tue": 1, "wed": 2, "thur": 3, "fri": 4, "sat": 5, "sun": 6}
        
        # Function to fetch the data with retries
        def fetch_data_with_retries(url, max_retries, delay):
            for attempt in range(max_retries):
                try:
                    html_table = pd.read_html(url)[0]
                    return html_table
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    else:
                        raise
        
        # Import HTML data from Bank of England rate
        url = 'https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp'
        html_table = fetch_data_with_retries(url, max_retries, delay)
        
        df = pd.DataFrame(html_table)
        df.rename(columns={"Date Changed": "OBS", "Rate": "macro_boe_intr_rate"}, inplace=True)
        
        # Change date column to datetime and find the corresponding week to the date
        df["OBS"] = pd.to_datetime(df["OBS"], format="%d %b %y")
        df.sort_values("OBS", axis=0, inplace=True)
        
        # Create a daily date range and find the week commencing for that day
        date_range = pd.date_range(df["OBS"].iloc[0], datetime.today(), freq="d")
        df_daily = pd.DataFrame(date_range, columns=["OBS"])
        
        # Adjust each date to the specified week commencing day
        df_daily['Week_Commencing'] = df_daily["OBS"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))
        
        # Outer merge the daily date range on the boe dataframe and forward fill in the blanks
        df_final = df_daily.merge(df, on='OBS', how="left")
        df_final["macro_boe_intr_rate"].ffill(inplace=True)
        
        # Group by the week start date and get the mean of the interest rates for each week
        df_final = df_final.groupby('Week_Commencing')['macro_boe_intr_rate'].mean().reset_index()
        
        df_final['Week_Commencing'] = df_final['Week_Commencing'].dt.strftime('%d/%m/%Y')
        df_final.rename(columns={'Week_Commencing': 'OBS'}, inplace=True)
        
        return df_final

    def pull_ons_data(self, series_list, week_commencing):
        """
        Fetch and process time series data from the ONS API.

        Args:
            series_list (list): A list of dictionaries where each dictionary represents a time series.
                                Each dictionary should have the keys 'series_id' and 'dataset_id'.
            week_commencing (str): The starting day of the week for aggregation. 
                                Options are "mon", "tue", "wed", "thur", "fri", "sat", "sun".

        Returns:
            pd.DataFrame: A DataFrame with weekly aggregated ONS data. The 'OBS' column contains the week 
                        commencing dates and other columns contain the aggregated time series values.
        """ 
        
        def parse_quarter(date_str):
            """Parses a string in 'YYYY Q#' format into a datetime object."""
            year, quarter = date_str.split(' ')
            quarter_number = int(quarter[1])
            month = (quarter_number - 1) * 3 + 1
            return pd.Timestamp(f"{year}-{month:02d}-01")

        # Generate a date range from 1950-01-01 to today
        date_range = pd.date_range(start="1950-01-01", end=datetime.today(), freq='D')
        daily_df = pd.DataFrame(date_range, columns=['OBS'])
        
        # Keep track of the renamed value columns
        value_columns = []

        for series in series_list:
            series_id = series['series_id']
            dataset_id = series['dataset_id']
            
            # Construct the URL for data
            data_url = f"https://api.ons.gov.uk/timeseries/{series_id}/dataset/{dataset_id}/data"
            
            # Make the request to the ONS API for data
            data_response = requests.get(data_url)
            
            # Check if the request was successful
            if data_response.status_code != 200:
                print(f"Failed to fetch data for series {series_id}: {data_response.status_code} {data_response.text}")
                continue
            
            # Parse the JSON response for data
            data = data_response.json()
            
            # Attempt to extract the name of the time series from the data response
            series_name = data.get('description', {}).get('title', 'Value')
            
            # Determine the most granular time series data available
            if 'months' in data and data['months']:
                time_series_data = data['months']
            elif 'quarters' in data and data['quarters']:
                time_series_data = data['quarters']
            elif 'years' in data and data['years']:
                time_series_data = data['years']
            else:
                print("No time series data found in the response")
                continue
            
            # Create a DataFrame from the time series data
            df = pd.DataFrame(time_series_data)
            
            # Handle different frequencies in the data
            if 'date' in df.columns:
                if any(df['date'].str.contains('Q')):  
                    df['date'] = df['date'].apply(parse_quarter)
                else:  
                    df['date'] = pd.to_datetime(df['date'])
            
            df = df.rename(columns={'date': 'OBS', 'value': series_name})
            
            # Rename the value column
            new_col_name = 'macro_' + series_name.lower().replace(':', '').replace(' ', '_').replace('-', '_')
            df = df.rename(columns={series_name: new_col_name})
            
            # Track the renamed value column
            value_columns.append(new_col_name)
            
            # Merge the data based on the observation date
            daily_df = pd.merge_asof(daily_df, df[['OBS', new_col_name]], on='OBS', direction='backward')
                
        # Ensure columns are numeric
        for col in value_columns:
            if col in daily_df.columns:
                daily_df[col] = pd.to_numeric(daily_df[col], errors='coerce').fillna(0)
            else:
                print(f"Column {col} not found in daily_df")
        
        # Aggregate results by week
        ons_df_final = ims_proc.aggregate_daily_to_wc_wide(df=daily_df, 
                                                    date_column="OBS", 
                                                    group_columns=[], 
                                                    sum_columns=value_columns,
                                                    wc=week_commencing,
                                                    aggregation="average")
        
        return ons_df_final
    
    def pull_oecd(self, country: str = "GBR", week_commencing: str = "mon", start_date: str = "1950-01-01") -> pd.DataFrame:
        """
        Fetch and process time series data from the OECD API.

        Args:
            country (list): A string containing a 3-letter code the of country of interest (E.g: "GBR", "FRA", "USA", "DEU")
            week_commencing (str): The starting day of the week for aggregation. 
                                Options are "mon", "tue", "wed", "thur", "fri", "sat", "sun".
            start_date (str): Dataset start date in the format "YYYY-MM-DD"

        Returns:
            pd.DataFrame: A DataFrame with weekly aggregated OECD data. The 'OBS' column contains the week 
                        commencing dates, and other columns contain the aggregated time series values.
        """ 

        def parse_quarter(date_str):
            """Parses a string in 'YYYY-Q#' format into a datetime object."""
            year, quarter = date_str.split('-')
            quarter_number = int(quarter[1])
            month = (quarter_number - 1) * 3 + 1
            return pd.Timestamp(f"{year}-{month:02d}-01")

        # Generate a date range from 1950-01-01 to today
        date_range = pd.date_range(start=start_date, end=datetime.today(), freq='D')

        url_details = [
            ["BCICP",    "SDD.STES,DSD_STES@DF_CLI,",                       ".....",              "macro_business_confidence_index"],
            ["CCICP",    "SDD.STES,DSD_STES@DF_CLI,",                       ".....",              "macro_consumer_confidence_index"],
            ["N.CPI",    "SDD.TPS,DSD_PRICES@DF_PRICES_ALL,",               "PA._T.N.GY",         "macro_cpi_total"],        
            ["N.CPI",    "SDD.TPS,DSD_PRICES@DF_PRICES_ALL,",               "PA.CP041T043.N.GY",  "macro_cpi_housing"],
            ["N.CPI",    "SDD.TPS,DSD_PRICES@DF_PRICES_ALL,",               "PA.CP01.N.GY",       "macro_cpi_food"],
            ["N.CPI",    "SDD.TPS,DSD_PRICES@DF_PRICES_ALL,",               "PA.CP045_0722.N.GY", "macro_cpi_energy"],
            ["UNE_LF_M", "SDD.TPS,DSD_LFS@DF_IALFS_UNE_M,",                 "._Z.Y._T.Y_GE15.",   "macro_unemployment_rate"],
            ["EAR",      "SDD.TPS,DSD_EAR@DF_HOU_EAR,",                     ".Y..S1D",            "macro_private_hourly_earnings"],
            ["RHP",      "ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,1.0", "",                   "macro_real_house_prices"],
            ["PRVM",     "SDD.STES,DSD_KEI@DF_KEI,4.0",                     "IX.C..",             "macro_manufacturing_production_volume"],
            ["TOVM",     "SDD.STES,DSD_KEI@DF_KEI,4.0",                     "IX...",              "macro_retail_trade_volume"],
            ["IRSTCI",   "SDD.STES,DSD_KEI@DF_KEI,4.0",                     "PA...",              "macro_interbank_rate"],
            ["IRLT",     "SDD.STES,DSD_KEI@DF_KEI,4.0",                     "PA...",              "macro_long_term_interest_rate"],
            ["B1GQ",     "SDD.NAD,DSD_NAMAIN1@DF_QNA,1.1",                  "._Z....GY.T0102",    "macro_gdp_growth_yoy"]
        ]

        # Create empty final dataframe
        oecd_df_final = pd.DataFrame()

        daily_df = pd.DataFrame({'OBS': date_range})
        value_columns = []

        # Iterate for each variable of interest
        for series_details in url_details:
            series = series_details[0]
            dataset_id = series_details[1]
            filter = series_details[2]
            col_name = series_details[3]

            # check if request was successful and determine the most granular data available
            for freq in ['M', 'Q', 'A']:
                
                if series in ["UNE_LF_M", "EAR"]:
                    data_url = f"https://sdmx.oecd.org/public/rest/data/OECD.{dataset_id}/{country}.{series}.{filter}.{freq}?startPeriod=1950-01"
                elif series in ["B1GQ"]:
                    data_url = f"https://sdmx.oecd.org/public/rest/data/OECD.{dataset_id}/{freq}..{country}...{series}.{filter}?startPeriod=1950-01"
                else:
                    data_url = f"https://sdmx.oecd.org/public/rest/data/OECD.{dataset_id}/{country}.{freq}.{series}.{filter}?startPeriod=1950-01"

                # Make the request to the OECD API for data
                data_response = requests.get(data_url)

                # Check if the request was successful
                if data_response.status_code != 200:
                    print(f"Failed to fetch data for series {series} with frequency '{freq}' for {country}: {data_response.status_code} {data_response.text}")
                    url_test = False
                    continue
                else:
                    url_test = True
                    break
            
            # get data for the next variable if url doesn't exist
            if url_test == False:
                continue

            root = ET.fromstring(data_response.content)

            # Define namespaces if necessary (the namespace is included in the tags)
            namespaces = {'generic': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic'}

            # Lists to store the data
            dates = []
            values = []

            # Iterate over all <Obs> elements and extract date and value
            for obs in root.findall('.//generic:Obs', namespaces):        

                # Extracting the time period (date)
                time_period = obs.find('.//generic:ObsDimension', namespaces).get('value')
                
                # Extracting the observation value
                value = obs.find('.//generic:ObsValue', namespaces).get('value')
                
                # Storing the data
                if time_period and value:
                    dates.append(time_period)
                    values.append(float(value))  # Convert value to float

            # Add variable names that were found to a list
            value_columns.append(col_name)

            # Creating a DataFrame
            data = pd.DataFrame({'OBS': dates, col_name: values})

            # Convert date strings into datetime format
            if freq == 'Q':
                data['OBS'] = data['OBS'].apply(parse_quarter)
            else:
                # Display the DataFrame
                data['OBS'] = data['OBS'].apply(lambda x: datetime.strptime(x, '%Y-%m'))

            # Sort data by chronological order
            data.sort_values(by='OBS', inplace=True)

            # Merge the data based on the observation date
            daily_df = pd.merge_asof(daily_df, data[['OBS', col_name]], on='OBS', direction='backward')


        # Ensure columns are numeric
        for col in value_columns:
            if col in daily_df.columns:
                daily_df[col] = pd.to_numeric(daily_df[col], errors='coerce').fillna(0)
            else:
                print(f"Column {col} not found in daily_df")

        # Aggregate results by week
        country_df = ims_proc.aggregate_daily_to_wc_wide(df=daily_df, 
                                                        date_column="OBS", 
                                                        group_columns=[], 
                                                        sum_columns=value_columns,
                                                        wc=week_commencing,
                                                        aggregation="average")
        
        oecd_df_final = pd.concat([oecd_df_final, country_df], axis=0, ignore_index=True)

        return oecd_df_final
    
    def get_google_mobility_data(self, country: str, wc: str) -> pd.DataFrame:
        """
        Fetch Google Mobility data for the specified country.
        
        Parameters:
        - country (str): The name of the country for which to fetch data.

        Returns:
        - pd.DataFrame: A DataFrame containing the Google Mobility data.
        """
        # URL of the Google Mobility Reports CSV file
        url = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"
        
        # Fetch the CSV file
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code}")
        
        # Load the CSV file into a pandas DataFrame
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        
        # Filter the DataFrame for the specified country
        country_df = df[df['country_region'] == country]
        
        final_covid = ims_proc.aggregate_daily_to_wc_wide(country_df, "date", [],  ['retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline',
                                                                                'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline',
                                                                                'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline'], wc, "average")
        
        final_covid1 = ims_proc.rename_cols(final_covid, 'covid_')
        return final_covid1
        
    ###############################################################  Seasonality  ##########################################################################

    def pull_combined_dummies(self, week_commencing):
        # Week commencing dictionary
        day_dict = {"mon": 0, "tue": 1, "wed": 2, "thur": 3, "fri": 4, "sat": 5, "sun": 6}
        
        # Create daily date range dataframe
        date_range = pd.date_range(datetime(2015, 1, 1), datetime.today(), freq="d")
        df_daily = pd.DataFrame(date_range, columns=["Date"])

        # Create weekly date range dataframe
        df_daily['week_start'] = df_daily["Date"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))
        df_weekly_start = df_daily[['week_start']].drop_duplicates().reset_index(drop=True)
        df_weekly_start.rename(columns={'week_start': "Date"}, inplace=True)
        
        df_weekly_start.index = np.arange(1, len(df_weekly_start) + 1)
        df_weekly_start.set_index("Date", inplace=True)
        
        # Create individual weekly dummies
        dummy_columns = {}
        for i in range(len(df_weekly_start)):
            col_name = f"dum_{df_weekly_start.index[i].strftime('%Y_%m_%d')}"
            dummy_columns[col_name] = [0] * len(df_weekly_start)
            dummy_columns[col_name][i] = 1
        
        df_dummies = pd.DataFrame(dummy_columns, index=df_weekly_start.index)
        df_weekly_start = pd.concat([df_weekly_start, df_dummies], axis=1)
        
        # Create monthly dummies
        df_daily["Month"] = df_daily["Date"].dt.month_name().str.lower()
        df_monthly_dummies = pd.get_dummies(df_daily, prefix="seas", columns=["Month"])
        df_monthly_dummies['week_start'] = df_daily["Date"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))
        df_monthly_dummies = df_monthly_dummies.groupby('week_start').sum(numeric_only=True).reset_index().rename(columns={'week_start': "Date"})
        
        df_monthly_dummies.set_index("Date", inplace=True)
        df_monthly_dummies = df_monthly_dummies / 7
        
        # Combine weekly and monthly dataframes
        df_combined = pd.concat([df_weekly_start, df_monthly_dummies], axis=1)
        
        # Create weekly dummies
        df_combined.reset_index(inplace=True)
        df_combined["Week"] = df_combined["Date"].dt.isocalendar().week
        df_combined = pd.get_dummies(df_combined, prefix="wk", columns=["Week"])
        
        # Create yearly dummies
        df_combined["Year"] = df_combined["Date"].dt.year
        df_combined = pd.get_dummies(df_combined, prefix="seas", columns=["Year"])
        
        # Add constant
        df_combined["Constant"] = 1
        
        # Add trend
        df_combined["Trend"] = df_combined.index + 1
        
        # Set date as index
        df_combined.set_index("Date", inplace=True)
        
        # Create COVID lockdown dummies
        lockdown_periods = [
            # Lockdown 1
            ("2020-03-23", "2020-05-24"),
            # Lockdown 2
            ("2020-11-05", "2020-12-02"),
            # Lockdown 3
            ("2021-01-04", "2021-03-08")
        ]
        
        df_covid = pd.DataFrame(date_range, columns=["Date"])
        df_covid["national_lockdown"] = 0
        
        for start, end in lockdown_periods:
            df_covid.loc[(df_covid["Date"] >= start) & (df_covid["Date"] <= end), "national_lockdown"] = 1
        
        df_covid['week_start'] = df_covid["Date"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))
        df_covid.drop("Date", axis=1, inplace=True)
        df_covid.rename(columns={"week_start": "OBS"}, inplace=True)
        df_national_lockdown_total = df_covid.groupby('OBS').sum(numeric_only=True)
        df_national_lockdown_total.rename(columns={"national_lockdown": "covid_uk_national_lockdown_total"}, inplace=True)
        
        df_national_lockdown_1 = df_national_lockdown_total.copy(deep=True)
        df_national_lockdown_2 = df_national_lockdown_total.copy(deep=True)
        df_national_lockdown_3 = df_national_lockdown_total.copy(deep=True)

        df_national_lockdown_1.loc[df_national_lockdown_1.index > "2020-05-24"] = 0
        df_national_lockdown_1.rename(columns={"covid_uk_national_lockdown_total": "covid_uk_national_lockdown_1"}, inplace=True)

        df_national_lockdown_2.loc[df_national_lockdown_2.index < "2020-11-05"] = 0
        df_national_lockdown_2.loc[df_national_lockdown_2.index > "2020-12-02"] = 0                          
        df_national_lockdown_2.rename(columns={"covid_uk_national_lockdown_total": "covid_uk_national_lockdown_2"}, inplace=True)

        df_national_lockdown_3.loc[df_national_lockdown_3.index < "2021-01-04"] = 0
        df_national_lockdown_3.rename(columns={"covid_uk_national_lockdown_total": "covid_uk_national_lockdown_3"}, inplace=True)

        df_final_covid = pd.concat([df_national_lockdown_total, df_national_lockdown_1, df_national_lockdown_2, df_national_lockdown_3], axis=1)
        df_final_covid.reset_index(inplace=True)
        df_final_covid.rename(columns={"index": "OBS"}, inplace=True)
        
        # Create seasonal indicators for the last day and last Friday of the month
        min_date = '2019-12-29'
        max_date = datetime.today().strftime('%Y-%m-%d')
        date_range_seas = pd.date_range(start=min_date, end=max_date)
        
        df_seas = pd.DataFrame(date_range_seas, columns=['Date'])
        df_seas['Last_Day_of_Month'] = df_seas['Date'].apply(lambda x: 1 if x == x.to_period('M').to_timestamp('M') else 0)
        
        def is_last_friday(date):
            last_day_of_month = date.to_period('M').to_timestamp('M')
            last_day_weekday = last_day_of_month.dayofweek
            if last_day_weekday >= 4:
                days_to_subtract = last_day_weekday - 4
            else:
                days_to_subtract = last_day_weekday + 3
            last_friday = last_day_of_month - pd.Timedelta(days=days_to_subtract)
            return 1 if date == last_friday else 0
        
        df_seas['Last_Friday_of_Month'] = df_seas['Date'].apply(is_last_friday)
        
        df_seas['week_start'] = df_seas["Date"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))
        df_seas = df_seas.groupby('week_start').sum(numeric_only=True).reset_index().rename(columns={'week_start': "Date"})
        df_seas.set_index("Date", inplace=True)
        
        # Combine all dataframes
        df_combined = df_combined.reset_index().rename(columns={"Date": "OBS"})
        df_final_combined = pd.merge(df_combined, df_final_covid, how='left', left_on='OBS', right_on='OBS')
        df_final_combined = pd.merge(df_final_combined, df_seas, how='left', left_on='OBS', right_on='Date')

        # Fill any NaN values with 0
        df_final_combined.fillna(0, inplace=True)
        
        return df_final_combined
    
    def pull_weather(self, week_commencing, country) -> pd.DataFrame:
        import pandas as pd
        import urllib.request
        from datetime import datetime
        import requests
        from geopy.geocoders import Nominatim

        # Week commencing dictionary
        day_dict = {"mon": 0, "tue": 1, "wed": 2, "thur": 3, "fri": 4, "sat": 5, "sun": 6}

        # Country dictionary
        country_dict = {"AUS": "AU__ASOS", "GBR": "GB__ASOS", "USA": "USCRN", "DEU": "DE__ASOS", "CAN": "Canada", "ZAF": "ZA__ASOS"}

        # Function to flatten a list of nested lists into a list
        def flatten_list(nested_list):
            return [item for sublist in nested_list for item in sublist]

        # Choose country
        country = country_dict[country]

        # Choose start and end dates
        start_day = 1
        start_month = 1
        start_year = 2014
        formatted_date = datetime(start_year, start_month, start_day).strftime("%Y-%m-%d")
        today = datetime.now()
        end_day = today.day
        end_month = today.month
        end_year = today.year

        if country == "GB__ASOS":
            stations = ["&stations=EGCC", "&stations=EGNM", "&stations=EGBB",
                        "&stations=EGSH", "&stations=EGFF", "&stations=EGHI",
                        "&stations=EGLC", "&stations=EGHQ", "&stations=EGAC",
                        "&stations=EGPF", "&stations=EGGD", "&stations=EGPE",
                        "&stations=EGNT"]
        elif country == "AU__ASOS":
            stations = ["&stations=YPDN", "&stations=YBCS", "&stations=YBBN",
                        "&stations=YSSY", "&stations=YSSY", "&stations=YMEN",
                        "&stations=YPAD", "&stations=YPPH"]
        elif country == "USCRN":
            stations = ["&stations=64756", "&stations=64758", "&stations=03761", "&stations=54797",  # North
                        "&stations=53968", "&stations=53960", "&stations=54932", "&stations=13301",  # Midwest
                        "&stations=64756", "&stations=64756", "&stations=92821", "&stations=63862",  # South
                        "&stations=53152", "&stations=93245", "&stations=04138", "&stations=04237"]  # West
        elif country == "DE__ASOS":
            stations = ["&stations=EDDL", "&stations=EDDH", "&stations=EDDB",
                        "&stations=EDDN", "&stations=EDDF", "&stations=EDDK",
                        "&stations=EDLW", "&stations=EDDM"]
        elif country == "FR__ASOS":
            stations = ["&stations=LFPB"]
        elif country == "Canada":
            institute_vector = ["CA_NB_ASOS", "CA_NF_ASOS", "CA_NT_ASOS", "CA_NS_ASOS",
                                "CA_NU_ASOS"]
            stations_list = [[] for _ in range(5)]
            stations_list[0].append(["&stations=CYQM", "&stations=CERM", "&stations=CZCR",
                                    "&stations=CZBF", "&stations=CYFC", "&stations=CYCX"])

            stations_list[1].append(["&stations=CWZZ", "&stations=CYDP", "&stations=CYMH",
                                    "&stations=CYAY", "&stations=CWDO", "&stations=CXTP",
                                    "&stations=CYJT", "&stations=CYYR", "&stations=CZUM",
                                    "&stations=CYWK", "&stations=CYWK"])

            stations_list[2].append(["&stations=CYHI", "&stations=CZCP", "&stations=CWLI",
                                    "&stations=CWND", "&stations=CXTV", "&stations=CYVL",
                                    "&stations=CYCO", "&stations=CXDE", "&stations=CYWE",
                                    "&stations=CYLK", "&stations=CWID", "&stations=CYRF",
                                    "&stations=CXYH", "&stations=CYWY", "&stations=CWMT"])

            stations_list[3].append(["&stations=CWEF", "&stations=CXIB", "&stations=CYQY",
                                    "&stations=CYPD", "&stations=CXNP", "&stations=CXMY",
                                    "&stations=CYAW", "&stations=CWKG", "&stations=CWVU",
                                    "&stations=CXLB", "&stations=CWSA", "&stations=CWRN"])

            stations_list[4].append(["&stations=CYLT", "&stations=CWEU", "&stations=CWGZ",
                                    "&stations=CYIO", "&stations=CXSE", "&stations=CYCB",
                                    "&stations=CWIL", "&stations=CXWB", "&stations=CYZS",
                                    "&stations=CWJC", "&stations=CYFB", "&stations=CWUW"])

        elif country == "ZA__ASOS":
            cities = ["Johannesburg", "Cape Town", "Durban", "Pretoria"]
            stations = []

            for city in cities:
                geolocator = Nominatim(user_agent="MyApp")
                location = geolocator.geocode(city)
                stations.append(f"&latitude={location.latitude}&longitude={location.longitude}")

        # Temperature
        if country in ["GB__ASOS", "AU__ASOS", "DE__ASOS", "FR__ASOS"]:
            # We start by making a data frame of the following weather stations
            station_query = ''.join(stations)

            raw_weather_list = ''.join(["https://mesonet.agron.iastate.edu/cgi-bin/request/daily.py?network=", country,
                                        station_query,
                                        "&year1=", str(start_year), "&month1=", str(start_month), "&day1=", str(start_day),
                                        "&year2=", str(end_year), "&month2=", str(end_month), "&day2=", str(end_day)])
            raw_weather = urllib.request.urlopen(raw_weather_list)
            raw_weather = pd.read_csv(raw_weather)

            # Replace the occurrences of "None" with Missing Value
            raw_weather["max_temp_f"].replace("None", 0, inplace=True)
            raw_weather["min_temp_f"].replace("None", 0, inplace=True)

            # Remove any data that isn't temperature-related
            weather = raw_weather.iloc[:, 0:4]

            weather[["max_temp_f", "min_temp_f"]] = weather[["max_temp_f", "min_temp_f"]].apply(pd.to_numeric)

            # Estimate mean temperature
            weather["mean_temp_f"] = (weather["max_temp_f"] + weather["min_temp_f"]) / 2

            # Convert Fahrenheit to Celsius for max_temp_f
            weather["max_temp_c"] = (weather["max_temp_f"] - 32) * 5 / 9

            # Convert Fahrenheit to Celsius for min_temp_f
            weather["min_temp_c"] = (weather["min_temp_f"] - 32) * 5 / 9

            # Convert Fahrenheit to Celsius for mean_temp_f
            weather["mean_temp_c"] = (weather["mean_temp_f"] - 32) * 5 / 9

            # Aggregate the data to week commencing sunday taking the average of the data
            # Convert the date column to a Date type
            weather["day"] = pd.to_datetime(weather["day"], format="%Y-%m-%d")

            # Determine the starting chosen day for each date
            weather['week_starting'] = weather["day"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))

            # Group by week_starting and summarize
            numeric_columns = weather.select_dtypes(include='number').columns
            weekly_avg_temp = weather.groupby("week_starting")[numeric_columns].mean()
            weekly_avg_temp.rename(columns={"max_temp_f": "avg_max_temp_f",
                                            "min_temp_f": "avg_min_temp_f",
                                            "mean_temp_f": "avg_mean_temp_f",
                                            "max_temp_c": "avg_max_temp_c",
                                            "min_temp_c": "avg_min_temp_c",
                                            "mean_temp_c": "avg_mean_temp_c"}, inplace=True)
        elif country == "Canada":
            for i in range(len(institute_vector)):
                station_query_temp = ''.join(flatten_list(stations_list[i]))
                institute_temp = institute_vector[i]
                raw_weather_temp = ''.join(["https://mesonet.agron.iastate.edu/cgi-bin/request/daily.py?network=", institute_temp,
                                            station_query_temp,
                                            "&year1=", str(start_year), "&month1=", str(start_month), "&day1=", str(start_day),
                                            "&year2=", str(end_year), "&month2=", str(end_month), "&day2=", str(end_day)])
                raw_weather_temp = urllib.request.urlopen(raw_weather_temp)
                raw_weather_temp = pd.read_csv(raw_weather_temp)

                if len(raw_weather_temp.index) == 0:
                    continue
                raw_weather_temp = raw_weather_temp[['station', 'day', 'max_temp_f', 'min_temp_f', 'precip_in']]

                if i == 1:
                    raw_weather = raw_weather_temp
                else:
                    raw_weather = pd.concat([raw_weather, raw_weather_temp])

                # Drop error column if it exists
                if 'ERROR: Invalid network specified' in list(raw_weather.columns):
                    raw_weather.drop('ERROR: Invalid network specified', axis=1, inplace=True)

                # Replace none values
                raw_weather["max_temp_f"].replace("None", 0, inplace=True)
                raw_weather["min_temp_f"].replace("None", 0, inplace=True)
                raw_weather["precip_in"].replace("None", 0, inplace=True)

                weather = raw_weather
                weather[["max_temp_f", "min_temp_f", "precip_in"]] = weather[["max_temp_f", "min_temp_f", "precip_in"]].apply(pd.to_numeric)

                # Estimate mean temperature
                weather["mean_temp_f"] = (weather["max_temp_f"] + weather["min_temp_f"]) / 2

                # Convert Fahrenheit to Celsius for max_temp_f
                weather["max_temp_c"] = (weather["max_temp_f"] - 32) * 5 / 9

                # Convert Fahrenheit to Celsius for min_temp_f
                weather["min_temp_c"] = (weather["min_temp_f"] - 32) * 5 / 9

                # Convert Fahrenheit to Celsius for mean_temp_f
                weather["mean_temp_c"] = (weather["mean_temp_f"] - 32) * 5 / 9

                # Aggregate the data to week commencing sunday taking the average of the data
                # Convert the date column to a Date type
                weather["day"] = pd.to_datetime(weather["day"], format="%Y-%m-%d")

                # Determine the starting chosen day for each date
                weather['week_starting'] = weather["day"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))

                # Group by week_starting and summarize
                numeric_columns = weather.select_dtypes(include='number').columns
                weekly_avg_temp = weather.groupby("week_starting")[numeric_columns].mean()
                weekly_avg_temp.rename(columns={"max_temp_f": "avg_max_temp_f",
                                                "min_temp_f": "avg_min_temp_f",
                                                "mean_temp_f": "avg_mean_temp_f",
                                                "max_temp_c": "avg_max_temp_c",
                                                "min_temp_c": "avg_min_temp_c",
                                                "mean_temp_c": "avg_mean_temp_c",
                                                "precip_in": "avg_mean_perc"}, inplace=True)
        elif country == "ZA__ASOS":
            weather_data_list = []

            for city in cities:
                geolocator = Nominatim(user_agent="MyApp")
                location = geolocator.geocode(city)
                url = "https://archive-api.open-meteo.com/v1/archive"

                params = {
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "start_date": formatted_date,
                    "end_date": today.strftime("%Y-%m-%d"),
                    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                    "timezone": "auto"
                }

                response = requests.get(url, params=params)
                response_data = response.json()

                daily_data = response_data["daily"]
                dates = daily_data["time"]

                data = pd.DataFrame({
                    "day": dates,
                    "max_temp_f": daily_data["temperature_2m_max"],
                    "min_temp_f": daily_data["temperature_2m_min"],
                    "precip_in": daily_data["precipitation_sum"]
                })
                data["city"] = city
                weather_data_list.append(data)

            weather = pd.concat(weather_data_list)

            # Convert the date column to a Date type
            weather["day"] = pd.to_datetime(weather["day"])

            # Replace None values
            weather["max_temp_f"].replace("None", 0, inplace=True)
            weather["min_temp_f"].replace("None", 0, inplace=True)
            weather["precip_in"].replace("None", 0, inplace=True)

            weather[["max_temp_f", "min_temp_f", "precip_in"]] = weather[["max_temp_f", "min_temp_f", "precip_in"]].apply(pd.to_numeric)

            # Estimate mean temperature
            weather["mean_temp_f"] = (weather["max_temp_f"] + weather["min_temp_f"]) / 2

            # Convert Fahrenheit to Celsius for max_temp_f
            weather["max_temp_c"] = (weather["max_temp_f"] - 32) * 5 / 9

            # Convert Fahrenheit to Celsius for min_temp_f
            weather["min_temp_c"] = (weather["min_temp_f"] - 32) * 5 / 9

            # Convert Fahrenheit to Celsius for mean_temp_f
            weather["mean_temp_c"] = (weather["mean_temp_f"] - 32) * 5 / 9

            # Determine the starting chosen day for each date
            weather['week_starting'] = weather["day"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))

            # Group by week_starting and summarize
            numeric_columns = weather.select_dtypes(include='number').columns
            weekly_avg_temp = weather.groupby("week_starting")[numeric_columns].mean()
            weekly_avg_temp.rename(columns={"max_temp_f": "avg_max_temp_f",
                                            "min_temp_f": "avg_min_temp_f",
                                            "mean_temp_f": "avg_mean_temp_f",
                                            "max_temp_c": "avg_max_temp_c",
                                            "min_temp_c": "avg_min_temp_c",
                                            "mean_temp_c": "avg_mean_temp_c",
                                            "precip_in": "avg_mean_perc"}, inplace=True)

        else:
            # We start by making a data frame of the following weather stations
            station_query = ''.join(stations)

            raw_weather_list = ''.join(["https://mesonet.agron.iastate.edu/cgi-bin/request/daily.py?network=", country,
                                        station_query,
                                        "&year1=", str(start_year), "&month1=", str(start_month), "&day1=", str(start_day),
                                        "&year2=", str(end_year), "&month2=", str(end_month), "&day2=", str(end_day)])
            raw_weather = urllib.request.urlopen(raw_weather_list)
            raw_weather = pd.read_csv(raw_weather)

            raw_weather = raw_weather[['day', 'max_temp_f', 'min_temp_f', 'precip_in']]

            # Replace the occurrences of "None" with Missing Value
            raw_weather["max_temp_f"].replace("None", 0, inplace=True)
            raw_weather["min_temp_f"].replace("None", 0, inplace=True)
            raw_weather["precip_in"].replace("None", 0, inplace=True)

            # Remove any data that isn't temperature-related
            weather = raw_weather

            weather[["max_temp_f", "min_temp_f", "precip_in"]] = weather[["max_temp_f", "min_temp_f", "precip_in"]].apply(pd.to_numeric)

            # Estimate mean temperature
            weather["mean_temp_f"] = (weather["max_temp_f"] + weather["min_temp_f"]) / 2

            # Convert Fahrenheit to Celsius for max_temp_f
            weather["max_temp_c"] = (weather["max_temp_f"] - 32) * 5 / 9

            # Convert Fahrenheit to Celsius for min_temp_f
            weather["min_temp_c"] = (weather["min_temp_f"] - 32) * 5 / 9

            # Convert Fahrenheit to Celsius for mean_temp_f
            weather["mean_temp_c"] = (weather["mean_temp_f"] - 32) * 5 / 9

            # Aggregate the data to week commencing sunday taking the average of the data
            # Convert the date column to a Date type
            weather["day"] = pd.to_datetime(weather["day"], format="%Y-%m-%d")

            # Determine the starting chosen day for each date
            weather['week_starting'] = weather["day"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))

            # Group by week_starting and summarize
            numeric_columns = weather.select_dtypes(include='number').columns
            weekly_avg_temp = weather.groupby("week_starting")[numeric_columns].mean()
            weekly_avg_temp.rename(columns={"max_temp_f": "avg_max_temp_f",
                                            "min_temp_f": "avg_min_temp_f",
                                            "mean_temp_f": "avg_mean_temp_f",
                                            "max_temp_c": "avg_max_temp_c",
                                            "min_temp_c": "avg_min_temp_c",
                                            "mean_temp_c": "avg_mean_temp_c",
                                            "precip_in": "avg_mean_perc"}, inplace=True)

        # Rainfall
        if country == "GB__ASOS":
            # Define cities and date range
            cities = ["Manchester", "Leeds", "Birmingham", "Norwich", "Cardiff", "Southampton", "London", "Newquay", "Belfast", "Glasgow", "Bristol", "Newcastle"]
            
            start_date = formatted_date
            end_date = today.strftime("%Y-%m-%d")

            # Initialize an empty list to store the weather data for each city
            weather_data_list = []

            # Loop through each city and fetch weather data
            for city in cities:
                # Initialize Nominatim API
                geolocator = Nominatim(user_agent="MyApp")
                location = geolocator.geocode(city)
                url = "https://archive-api.open-meteo.com/v1/archive"

                params = {
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "start_date": start_date,
                    "end_date": end_date,
                    "daily": "precipitation_sum",
                    "timezone": "auto"
                }

                response = requests.get(url, params=params)
                response_data = response.json()

                daily_data = response_data["daily"]["precipitation_sum"]
                dates = response_data["daily"]["time"]

                data = pd.DataFrame({"date": dates, "rainfall": daily_data})
                data["city"] = city

                weather_data_list.append(data)

            # Combine all city data into a single data frame
            all_weather_data = pd.concat(weather_data_list)

            # Convert the date column to a Date type
            all_weather_data["date"] = pd.to_datetime(all_weather_data["date"])

            # Set week commencing col up
            all_weather_data['week_starting'] = all_weather_data["date"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))

            # Group by week_starting and summarize
            numeric_columns = all_weather_data.select_dtypes(include='number').columns
            weekly_avg_rain = all_weather_data.groupby("week_starting")[numeric_columns].mean()
            weekly_avg_rain.rename(columns={"rainfall": "avg_rainfall"}, inplace=True)

            # Change index to datetime
            weekly_avg_rain.index = pd.to_datetime(weekly_avg_rain.index)

        elif country == "AU__ASOS":

            # Define cities and date range
            cities = ["Darwin", "Cairns", "Brisbane", "Sydney", "Melbourne", "Adelaide", "Perth"]

            start_date = formatted_date
            end_date = today.strftime("%Y-%m-%d")

            # Initialize an empty list to store the weather data for each city
            weather_data_list = []

            # Loop through each city and fetch weather data
            for city in cities:
                # Initialize Nominatim API
                geolocator = Nominatim(user_agent="MyApp")
                location = geolocator.geocode(city)
                url = "https://archive-api.open-meteo.com/v1/archive"

                params = {
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "start_date": start_date,
                    "end_date": end_date,
                    "daily": "precipitation_sum",
                    "timezone": "auto"
                }

                response = requests.get(url, params=params)
                response_data = response.json()

                daily_data = response_data["daily"]["precipitation_sum"]
                dates = response_data["daily"]["time"]

                data = pd.DataFrame({"date": dates, "rainfall": daily_data})
                data["city"] = city

                weather_data_list.append(data)

            # Combine all city data into a single data frame
            all_weather_data = pd.concat(weather_data_list)

            # Convert the date column to a Date type
            all_weather_data["date"] = pd.to_datetime(all_weather_data["date"])

            # Set week commencing col up
            all_weather_data['week_starting'] = all_weather_data["date"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))

            # Group by week_starting and summarize
            numeric_columns = all_weather_data.select_dtypes(include='number').columns
            weekly_avg_rain = all_weather_data.groupby("week_starting")[numeric_columns].mean()
            weekly_avg_rain.rename(columns={"rainfall": "avg_rainfall"}, inplace=True)

            # Change index to datetime
            weekly_avg_rain.index = pd.to_datetime(weekly_avg_rain.index)

        elif country == "DE__ASOS":

            # Define cities and date range
            cities = ["Dortmund", "Düsseldorf", "Frankfurt", "Munich", "Cologne", "Berlin", "Hamburg", "Nuernberg"]

            start_date = formatted_date
            end_date = today.strftime("%Y-%m-%d")

            # Initialize an empty list to store the weather data for each city
            weather_data_list = []

            # Loop through each city and fetch weather data
            for city in cities:
                # Initialize Nominatim API
                geolocator = Nominatim(user_agent="MyApp")
                location = geolocator.geocode(city)
                url = "https://archive-api.open-meteo.com/v1/archive"

                params = {
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "start_date": start_date,
                    "end_date": end_date,
                    "daily": "precipitation_sum",
                    "timezone": "auto"
                }

                response = requests.get(url, params=params)
                response_data = response.json()

                daily_data = response_data["daily"]["precipitation_sum"]
                dates = response_data["daily"]["time"]

                data = pd.DataFrame({"date": dates, "rainfall": daily_data})
                data["city"] = city

                weather_data_list.append(data)

            # Combine all city data into a single data frame
            all_weather_data = pd.concat(weather_data_list)

            # Convert the date column to a Date type
            all_weather_data["date"] = pd.to_datetime(all_weather_data["date"])

            # Set week commencing col up
            all_weather_data['week_starting'] = all_weather_data["date"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))

            # Group by week_starting and summarize
            numeric_columns = all_weather_data.select_dtypes(include='number').columns
            weekly_avg_rain = all_weather_data.groupby("week_starting")[numeric_columns].mean()
            weekly_avg_rain.rename(columns={"rainfall": "avg_rainfall"}, inplace=True)

            # Change index to datetime
            weekly_avg_rain.index = pd.to_datetime(weekly_avg_rain.index)

        elif country == "FR__ASOS":

            # Define cities and date range
            cities = ["Paris"]

            start_date = formatted_date
            end_date = today.strftime("%Y-%m-%d")

            # Initialize an empty list to store the weather data for each city
            weather_data_list = []

            # Loop through each city and fetch weather data
            for city in cities:
                # Initialize Nominatim API
                geolocator = Nominatim(user_agent="MyApp")
                location = geolocator.geocode(city)
                url = "https://archive-api.open-meteo.com/v1/archive"

                params = {
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "start_date": start_date,
                    "end_date": end_date,
                    "daily": "precipitation_sum",
                    "timezone": "auto"
                }

                response = requests.get(url, params=params)
                response_data = response.json()

                daily_data = response_data["daily"]["precipitation_sum"]
                dates = response_data["daily"]["time"]

                data = pd.DataFrame({"date": dates, "rainfall": daily_data})
                data["city"] = city

                weather_data_list.append(data)

            # Combine all city data into a single data frame
            all_weather_data = pd.concat(weather_data_list)

            # Convert the date column to a Date type
            all_weather_data["date"] = pd.to_datetime(all_weather_data["date"])

            # Set week commencing col up
            all_weather_data['week_starting'] = all_weather_data["date"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))

            # Group by week_starting and summarize
            numeric_columns = all_weather_data.select_dtypes(include='number').columns
            weekly_avg_rain = all_weather_data.groupby("week_starting")[numeric_columns].mean()
            weekly_avg_rain.rename(columns={"rainfall": "avg_rainfall"}, inplace=True)

            # Change index to datetime
            weekly_avg_rain.index = pd.to_datetime(weekly_avg_rain.index)

        elif country == "ZA__ASOS":
            cities = ["Johannesburg", "Cape Town", "Durban", "Pretoria"]
            start_date = formatted_date
            end_date = today.strftime("%Y-%m-%d")

            weather_data_list = []

            for city in cities:
                geolocator = Nominatim(user_agent="MyApp")
                location = geolocator.geocode(city)
                url = "https://archive-api.open-meteo.com/v1/archive"

                params = {
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "start_date": start_date,
                    "end_date": end_date,
                    "daily": "precipitation_sum",
                    "timezone": "auto"
                }

                response = requests.get(url, params=params)
                response_data = response.json()

                daily_data = response_data["daily"]["precipitation_sum"]
                dates = response_data["daily"]["time"]

                data = pd.DataFrame({"date": dates, "rainfall": daily_data})
                data["city"] = city

                weather_data_list.append(data)

            # Combine all city data into a single data frame
            all_weather_data = pd.concat(weather_data_list)

            # Convert the date column to a Date type
            all_weather_data["date"] = pd.to_datetime(all_weather_data["date"])

            # Set week commencing col up
            all_weather_data['week_starting'] = all_weather_data["date"].apply(lambda x: x - pd.Timedelta(days=(x.weekday() - day_dict[week_commencing]) % 7))

            # Group by week_starting and summarize
            numeric_columns = all_weather_data.select_dtypes(include='number').columns
            weekly_avg_rain = all_weather_data.groupby("week_starting")[numeric_columns].mean()
            weekly_avg_rain.rename(columns={"rainfall": "avg_rainfall"}, inplace=True)

            # Change index to datetime
            weekly_avg_rain.index = pd.to_datetime(weekly_avg_rain.index)

        # Merge the dataframes
        if country in ["AU__ASOS", "DE__ASOS", "FR__ASOS", "GB__ASOS", "ZA__ASOS"]:
            merged_df = weekly_avg_rain.merge(weekly_avg_temp, on="week_starting")
        else:
            merged_df = weekly_avg_temp

        merged_df.reset_index(drop=False, inplace=True)
        merged_df.rename(columns={'week_starting': 'OBS'}, inplace=True)

        final_weather = ims_proc.rename_cols(merged_df, 'seas_')

        return final_weather
    
    def pull_covid_data(self, folder_path: str, country: str = "GB", week_commencing: str = "mon") -> pd.DataFrame:
        """
        Get covid pandemic data for the country of interest.

        Args:
            folder_path (str): A string containing the local location of the OneDrive folder.
                                Example: "C:/Users/-- username --/OneDrive - im-sciences.com"
                                The file location within the MasterDrive of the worldwide covid data is: 
                                MasterDrive/Central Database/Covid/oxford-government-response.csv
            country (str): A string containing the country of interest (E.g: "GB", "FR")
            week_commencing (str): The starting day of the week for aggregation.
                                Options are "mon", "tue", "wed", "thur", "fri", "sat", "sun".

        Returns:
            pd.DataFrame: A DataFrame containing seasonality and public holiday dummies for the country of interest.
                            The 'OBS' column contains the week commencing dates.
        """

        df = pd.read_csv(f'{folder_path}/MasterDrive/Central Database/Covid/oxford-government-response.csv')

        country_df = df[df['location_key']==country]
        country_df.rename(columns={'date': 'OBS'}, inplace=True)
        country_df.drop('location_key', axis=1, inplace=True)

        agg_df = ims_proc.aggregate_daily_to_wc_wide(country_df, 'OBS', [], country_df.columns.to_list(), week_commencing, 'average')

        covid_df = ims_proc.rename_cols(agg_df, 'covid_')

        covid_df['OBS'] = covid_df['OBS'].apply(lambda x: x[0].date())

        return covid_df
    