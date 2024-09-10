# Deepan's Regression Tool

## Overview

Deepan's Regression Tool is designed to automate regression testing by running commands specified in an Excel file and logging the results. This tool is especially useful for managing large-scale testing environments where multiple test cases need to be executed and monitored.

## Features

- Executes commands specified in an Excel file.
- Logs the results of each command.
- Handles various error scenarios and retries failed commands.
- Updates the Excel file with the status of each command.

## License

This tool is licensed under the GNU General Public License v3.0. For more details, visit: [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Installation

To use this tool, install it via pip:

```sh
pip3 install deepan_regression_tool
```
## Prerequisites
- Python >=3.9
- openpyxl
- Linux operating system

## Usage
Importing the Module
After installation, you can import the module as follows:
```python
import deepan_regression_tool
```
## Running Regression
To run the regression, use the run_regression function provided by the module.

```python
import deepan_regression_tool

def check_results (input1, input2):
    ...
    ...
    ...
    return [flag, status]

deepan_regression_tool.check_results = check_results

deepan_regression_tool.regression(json_file_name,number_of_iteratables,max_bit_widths1,max_bait_widths2,iteratable_freq,random_iteratable_values,timeout_for_run_command)

help = deepan_regression_tool.HELP_MESSAGE
```
flag can take boolean values - True,Flase
status can take string values - PASS,FAIL,terminate,try_again,clean_db_try_again

## Fair Use
This tool is provided as-is under the GNU General Public License v3.0. You are free to use, modify, and distribute this tool, provided that you adhere to the terms of the license. For more details, visit: GNU GPL v3.0.

## Contact
For questions or suggestions, please open an issue on the GitHub repository.
