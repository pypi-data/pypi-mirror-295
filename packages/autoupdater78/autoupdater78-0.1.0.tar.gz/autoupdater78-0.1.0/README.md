<h1 align="center">AutoUpdater</h1>
<div align="center">

English | [简体中文](./README.cn.md) 

[![License](https://img.shields.io/badge/license-Apache%202-green.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Test Status](https://github.com/www778878net/AutoUpdater/actions/workflows/BuildandTest.yml/badge.svg?branch=main)](https://github.com/www778878net/AutoUpdater/actions/workflows/BuildandTest.yml)
[![QQ Group](https://img.shields.io/badge/QQ%20Group-323397913-blue.svg?style=flat-square&color=12b7f5&logo=qq)](https://qm.qq.com/cgi-bin/qm/qr?k=it9gUUVdBEDWiTOH21NsoRHAbE9IAzAO&jump_from=webapi&authKey=KQwSXEPwpAlzAFvanFURm0Foec9G9Dak0DmThWCexhqUFbWzlGjAFC7t0jrjdKdL)
</div>

## Feedback QQ Group (Click to join): [323397913](https://qm.qq.com/cgi-bin/qm/qr?k=it9gUUVdBEDWiTOH21NsoRHAbE9IAzAO&jump_from=webapi&authKey=KQwSXEPwpAlzAFvanFURm0Foec9G9Dak0DmThWCexhqUFbWzlGjAFC7t0jrjdKdL)

## 1. `AutoUpdater` Class Documentation

### Overview

`AutoUpdater` is a Python-based automatic update tool used to compare MD5 values of local and remote files and download updated files. It supports initializing local directories, generating MD5 file lists, updating files, and more.

### Installation

Clone the repository to your local machine:

~~~
git clone https://github.com/www778878net/AutoUpdater.git
cd AutoUpdater
~~~

### Quick Start

Here's a basic example of how to use `AutoUpdater`:

~~~python
from autoupdater import AutoUpdater, initialize_directory

# Initialize local directory
local_dir = "/path/to/local/directory"
remote_url = "http://example.com/remote/"
result = initialize_directory(local_dir, remote_url)
print(result)

# Create AutoUpdater instance and update files
updater = AutoUpdater(local_dir, remote_url)
update_result = updater.update_files()
print(update_result)
~~~

### Main Methods

- `initialize_directory(local_directory, remote_base_url)`: Initialize local directory.
- `update_files()`: Update local files.
- `get_file_list_with_md5(directory)`: Get MD5 values for all files in the specified directory.
- `save_md5_json(output_file="md5.json")`: Generate and save a JSON file containing file MD5 values.

### Example: Initializing Directory

~~~python
from autoupdater import initialize_directory

local_dir = "/path/to/local/directory"
remote_url = "http://example.com/remote/"
result = initialize_directory(local_dir, remote_url)
print(result)
~~~

### Example: Updating Files

~~~python
from autoupdater import AutoUpdater

updater = AutoUpdater("/path/to/local/directory", "http://example.com/remote/")
result = updater.update_files()
print(result)
~~~

### Running Tests

To run tests, execute the following command in the project root directory:

~~~
python -m unittest discover tests
~~~

### Other

For more detailed information, please refer to the project's [GitHub repository](https://github.com/www778878net/AutoUpdater) or API documentation.