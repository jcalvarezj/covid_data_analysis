# Data Analysis Tool for COVID-19-related Datasets

## -- Work In Progress --

This program made in Python is used to filter data from CSV files from two datasets related to the COVID-19 pandemic:

1. [Global Hospital Beds Capacity (for covid-19) by Igor Kiulian](https://www.kaggle.com/ikiulian/global-hospital-beds-capacity-for-covid19)
2. [COVID-19 containment and mitigation measures by Paul Mooney](https://www.kaggle.com/paultimothymooney/covid19-containment-and-mitigation-measures)


## Requirements

**Python 3.x**, any version of **pip**, and **virtualenv**


## Installation

- Clone into a new directory and navigate inside it

- Create a new virtual environment using **virtualenv**

    For example, `virtualenv venv`

- Activate venv

    For Windows: `.\venv\Scripts\activate.bat`

    For Unix/Linux: `source venv/bin/activate` or `./venv/bin/activate.sh`

    (Run the `deactivate` command when done with this software's execution)

- Install dependencies

    `pip install -r requirements.txt`


## Execution

Use either  `python main.py`  or  `python3 main.py` for a guided Command Line Interface menu, or execute using arguments as follows:

`python main.py <index of dataset> <index of filter> [post]`

**For the values of datasets:**

1. Bed capacity
2. Measures and restrictions

**Bed capacity's filters:**

1. Number and percentage of beds per type, by country (scale)
2. Top 10 countries with highest bed capacity (scale)
3. Top 10 countries with lowest bed capacity (scale)
4. Top 10 countries with highest bed capacity (estimated total)    
5. Top 10 countries with lowest bed capacity (estimated total)
6. Top 10 countries with highest average bed capacity (scale)
7. Top 10 countries with lowest average bed capacity (scale)
8. Top 10 countries with highest average bed capacity (estimated)
9. Top 10 countries with lowest average bed capacity (estimated)
10. General dataset statistics

**Measures and restrictions filters:**

1. General measures information by country
2. Top 10 countries with highest number of different measures/restrictions
3. Top 10 countries with lowest number of different measures/restrictions
4. Top 10 countries with highest number of measures/restrictions records
5. Top 10 countries with lowest number of measures/restrictions records
6. General dataset information


Finally, the optional argument 'post' can be added to send a request to the defined backend API


## Usage

Activate the virtual environment and run the program using a CLI. Follow the instructions that appear on screen (only shown in argumentless CLI mode)

You will find the generated JSON files in the **export** folder

### Bed Capacity Dataset

The generated output files are stored in ./export/beds/. These files are named with the **_GENERAL** and **_TYPES** suffixes to indicate whether they refer to general information or specific bed types information. The file name prefixes are the respective filters.

### Measures/Restrictions Dataset

Same as above, but stored in ./export/measures/ and with the **_GENERAL** and **_MEASURES** suffixes