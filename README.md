# LogArchiver

LogArchiver is a Python-based tool designed to archive log files.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.x
- pip

### Installation

1. Clone the repository to your local machine.
   `git clone https://github.com/aykut-canturk/LogArchiver.git`
2. Navigate to the project directory.
   `cd LogArchiver`
3. Install the necessary Python packages using pip:
   `pip install -r requirements.txt`

## Usage

1. Open the `config.json` file located in the root directory of the project.
2. Configure the following parameters according to your preferences:

   - **DirsToSearch**: List of directories to search for log files. Example: `["/path/to/logs_dir1", "/path/to/logs_dir2"]`
   - **ArchiveThresholdDays**: Maximum number of days threshold for considering a log file as old and archiving it. Example: `30`

3. Save the `config.json` file.
4. Start the program by running `python main.py`.

## Running the Tests

To run unit tests, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the following command:
   `python -m unittest discover -s tests`
   This command will discover and run all test files located in the "tests" directory and its subdirectories.

## Creating an Executable

If you want to create an executable file from this Python script, you can do so using PyInstaller. First, install PyInstaller using pip:
`pip install pyinstaller`

Then, you can create the executable with the following command:
`pyinstaller --onefile main.py`

## License

This project is licensed under the MIT license. For more information, see the [LICENSE](LICENSE) file.
