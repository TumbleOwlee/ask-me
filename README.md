# AskMe

This script is completely terminal based. No user interface is added. You can get the command line options by using the `--help` argument.

Make sure the config.yml is placed in the same directory. The configuration is needed to access all necessary information.

Extracting data: `python ./ExtractQuestions.py extracted_data.yml` or `python ./ExtractQuestions.py --json extracted_data.json`

Using questionaire: `python ./AskMe.py extracted_data.yml` or `python ./AskMe.py --json extracted_data.json`

## Requirements

You will need Python with the Numpy and PyYaml library. 

### Linux

1. Install packages python and python-pip:
    * Ubuntu: `sudo apt install python python-pip`
    * Arch: `sudo pacman install python python-pip`
2. Check your install via `pip3 --version` and `python --version`
3. Install Numpy: `sudo pip3 install numpy`
4. Install Numpy: `sudo pip3 install pyyaml`
5. Run the script via `python AskMe.py`

### Windows

1. Install python (latest release): https://www.python.org/downloads/windows/
2. Check your install via `pip3 --version` and `python --version`
3. Install numpy: `pip3 install numpy`
4. Install Numpy: `sudo pip3 install pyyaml`
5. Run the script via `python AskMe.py` in terminal or double click the script
    * If double click opens the script in a text editor, then right-click the file -> Open With... -> Python

### Mac

1. Install python (latest release): https://www.python.org/downloads/mac-osx/
2. Check your install via `pip3 --version` and `python --version`
3. Install numpy: `pip3 install Numpy`
4. Install Numpy: `sudo pip3 install pyyaml`
5. Run the script via `python AskMe.py` in terminal
    * Maybe the script is executable. I can't check it because of missing access to apple devices.
    * If the script is not executable, you can build the executable via pyinstaller.

## Build executable on Windows/Mac/Linux

1. Install pyinstaller: 
    * Linux: `sudo pip3 install pyinstaller`
    * Windows: `pip3 install pyinstaller`
    * Mac: `pip3 install pyinstaller`
2. Run `pyinstaller --onefile AskMe.py`
3. Check created `dist` directory for executable

## Extract questions from website

1. Use your web browser to visit finalexam.eu
2. Login with your credentials
3. Open web console
4. Go to storage and extract your cookie string
5. Enter your cookie string into the config.yaml
6. Start ExtractQuestions.py and you will receive all questions as yaml or json

