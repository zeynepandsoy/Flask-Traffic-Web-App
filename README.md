[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=10410173&assignment_repo_type=AssignmentRepo)
# COMP0034 Coursework 2 

To set up your project:

1. Clone this repository in your IDE (e.g. PyCharm, Visual Studio Code) from GitHub. Follow the help in your IDE
   e.g. [clone a GitHub repo in PyCharm.](https://www.jetbrains.com/help/pycharm/manage-projects-hosted-on-github.html#clone-from-GitHub)
2. Create and then activate a virtual environment (venv). Use the instructions for your IDE
   or [navigate to your project directory and use python.](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
3. Install the requirements from requirements.txt. Use the instructions for your IDE
   or [the pip documentation](https://pip.pypa.io/en/latest/user_guide/#requirements-files).
4. Edit .gitignore to add any config files and folders for your IDE. 


## Repository link

GitHub Repository Link: https://github.com/ucl-comp0035/comp0034-cw2-i-zeynepandsoy.git


# Set-up Instructions to run the app 

## Please ask Sarah Sanders to mark this coursework herself, this has been discussed and agreed upon.

Python environment is created, please activate a venv.

Install the packages from requirements.txt.

**The app is ran entering below command in terminal:**

`python3 -m flask --app 'COMP0034_CW2/traffic_app:create_app("config.DevConfig")' --debug run`

**The tests are ran entering below command in terminal:**

`python -m pytest -v tests/ -W ignore::DeprecationWarning`

A single test can be ran with the command: `python -m pytest -v tests//test_filename.py::test_specific__test`
i.e., python -m pytest -v tests//test_routes.py::test_get_all_data


## Instructions to query the API route to get all data using URL endpoints

**No filter:** `/data/` i.e., 127.0.0.1:5000/data/ 

Without any filter, the url enpoint `/data/` returns all data in JSON format

**Single filter:** `/data/?<header>=<option>` i.e., 127.0.0.1:5000/data/?day=23

Adding a single filter can be accomplished commanding `?<header>=` , given the category and unique value are acceptable inputs from the dataset. This action return all data of the selected category in JSON format

**Several filters:** `/data/?<header>=<option>&<another_header>=<another_option>...` 

With `&` command new query parameters can be added to further constraint and personalize the scope of traffic observations

i.e., 127.0.0.1:5000/data/?day=23&month=10&year=2015 would return the traffic details for the specific date 23/10/2015

***Remark:*** To query values with two or more words, i.e. Colombus Day, `%20` must be used instead of spaces between the words. i.e. /data/?holiday=Columbus%20Day, or /data/?holiday=New%20Years%20Day

# TESTING

## Results of running tests



![Test Results](/traffic_app/static/assets/TestResults.png)