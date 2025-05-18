# Employee Management System Using Django

## Project Structure

/server folder contains django server for running the application.

/employees folder contains django app for employee management system.

## Running the application

Requirements: python 3.10

### First install python packages from requirements.txt file by creating a virtual environment in project root

```shell
# 1. Creates an environment.
python3 -m venv .venv

# 2. Activate the environment(linux).
source .venv/bin/activate

# 2. Activate the environment(windows).
.venv\Scripts\activate

# 3. Install packages.
pip install -r requirements.txt
```

#### Then run the following when in project root

```shell
python manage.py runserver
```

#### Open web browser and navigate to [http://127.0.0.1:8000/employee/api/](http://127.0.0.1:8000/employee/api/)
