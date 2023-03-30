[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=10410173&assignment_repo_type=AssignmentRepo)

# COMP0034 Coursework 2 - Flask Traffic Web App

### Repository link

GitHub Repository Link: https://github.com/ucl-comp0035/comp0034-cw2-i-zeynepandsoy.git

## Please ask Sarah Sanders to mark this coursework herself, this has been discussed and agreed upon.

## Overview 

This Flask web app provides summary statistics of traffic data from a SQLite database across several categories. It also offers an API endpoint for users to access the raw data in JSON format.

## Setup 

Before running the app, create and activate a virtual environment. Then, install the required dependencies from the `requirements.txt` file using the following command:

```
pip install -r requirements.txt
```

## Usage

To run the app, execute the following command:

```
python3 -m flask --app 'COMP0034_CW2/traffic_app:create_app("config.DevConfig")' --debug run
```


## Routes

The code defines several routes (i.e., URLs) that correspond to different pages in the web application.

**Blueprints** allow modularizing the Flask application by breaking it up into smaller, more manageable pieces. In this project, two blueprints are defined and used to organize and group related routes together:

* `auth_bp`  Contains routes related to user authentication (e.g., login, logout, registration)
* `main_bp` Contains all other routes  including logged in page routes and an API route


## Authentication

User authentication is handled by Flask-Login. The authentication routes are defined using the @auth_bp.route() decorator, and include:

* `/signup` Allows new users to sign up and create an account.
* `/login` Allows registered users to log in to their account.
* `/logout` Logs out the user and redirects them to the login page.


## Main routes

Main routes are defined using the @main_bp.route() decorator

'Traffic Home' is the homepage of the app defined by the dashboard() function. It displays the column headers of all data in the database as cards. Users can click on a column header to see a dropdown menu of distinct values in that column.

The query() function is responsible for displaying the dropdown menu of distinct values for a specified column in the Query table. It first replaces any invalid special characters in the column name with underscores, then queries the database for the distinct values of the specified column. 

The result() function is responsible for displaying summary statistics for a particular query option (i.e., dropdown value). It first replaces any underscores in the query option with spaces, then queries the database for all rows that have the specified column value. It computes basic summary statistics -average, minimum, maximum- on traffic volume column based on the chosen option and displays the category of the option (e.g., "moderate" or "relatively high"). 

### API Endpoint

The app provides an API endpoint that enables users to retrieve/access data from the database in JSON format. Users can query the data with different filters or parameters, the data is then serialized using a QuerySchema and returned as a JSON response. To use the API endpoint, make a GET request to get_all_data route with enpoint `/data/` with the desired query parameters.

**Querying the API Endpoint**

The available query parameters are the same as the column names in the database. 

**No filter:** `/data/` 

Without any filter, the enpoint `/data/` retrieves all data in JSON format


**Single filter:** `/data/?<header>=<option>` 

Adding a single filter can be accomplished commanding `?<header>=` , given the category and unique value are acceptable inputs from the dataset. This action return all data of the selected option in JSON format

For example, to filter by a specific day from the day column, use the following URL: `/data/?day=23`

Multiple query parameters can be used to filter the data further:

**Several filters:** `/data/?<header>=<option>&<another_header>=<another_option>...` 

With `&` command new query parameters can be added to further constraint and personalize the scope of traffic observations

For example: To filter by a specific date, say 23/10/2015 use the following URL: `/data/?day=23&month=10&year=2015`

***Remark:*** To query values with two or more words, i.e. Colombus Day, `%20` must be used instead of spaces between the words. For example: `/data/?holiday=Columbus%20Day`, or `/data/?holiday=New%20Years%20Day` would be appropriate.


# TESTING

Run the tests with the following command:

```
python -m pytest -v tests/ -W ignore::DeprecationWarning
```

Run a single test with the command: `python -m pytest -v tests//test_filename.py::test_specific__test`
i.e., python -m pytest -v tests//test_routes.py::test_get_all_data

## Test Results 

**Test Results and Coverage**

![Evidence of running Test Results and Coverage Reports](/traffic_app/static/assets/TestResults-CoverageReport.png)

Percentage of code coverage achieved by the tests ranges from 73% to 100%, with an overall coverage of 94%

The report shows that there are some lines of code that are not covered by the tests, which means though the tests cover a significant portion of the application code, there are some areas that are not tested.

**CI workflow**
GitHub Actions page repository: https://github.com/ucl-comp0035/comp0034-cw2-i-zeynepandsoy/actions

