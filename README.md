[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=10410173&assignment_repo_type=AssignmentRepo)
# COMP0034 Coursework 2 starter code template

To set up your project:

1. Clone this repository in your IDE (e.g. PyCharm, Visual Studio Code) from GitHub. Follow the help in your IDE
   e.g. [clone a GitHub repo in PyCharm.](https://www.jetbrains.com/help/pycharm/manage-projects-hosted-on-github.html#clone-from-GitHub)
2. Create and then activate a virtual environment (venv). Use the instructions for your IDE
   or [navigate to your project directory and use python.](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
3. Install the requirements from requirements.txt. Use the instructions for your IDE
   or [the pip documentation](https://pip.pypa.io/en/latest/user_guide/#requirements-files).
4. Edit .gitignore to add any config files and folders for your IDE. 





# Set-up Instructions to run the app 

## Set-up

## Please ask Sarah Sanders to mark this coursework herself, this has been discussed and agreed upon


Python environment is created, please activate a venv.

Install the packages from requirements.txt.

*To app is ran entering below command in terminal:

python3 -m flask --app 'COMP0034_CW2/traffic_app:create_app("config.DevConfig")' --debug run

*Tests are run entering below command in terminal:
python -m pytest -v tests/ -W ignore::DeprecationWarning

to run api links
no filter:   `/data/`         i.e., 127.0.0.1:5000/data/ 
 without any filter paramaters returns all data in json format

single filter:  `/data/?<header>=<option>`         i.e., 127.0.0.1:5000/data/?day=23
Adding a single filter can be accomplished with `?<header>=` syntax, given the category and unique value are acceptable inputs from the dataset

several filters: `/data/?<header>=<option>&<another_header>=<another_option>...`  i.e., 127.0.0.1:5000/data/?day=23&month=10&year=2015 would return the traffic details for the specific date 23.10.2015
With `&` symbol new query parameters can be added to further constraint and personalize the scope of traffic observations

note: query values with two or more words, i.e. colombus day, use `%20` for spaces between words:
/data/?holiday=Columbus%20Day, or /data/?holiday=New%20Years%20Day



## Repository link

GitHub Repository Link: https://github.com/ucl-comp0035/comp0034-cw2-i-zeynepandsoy.git