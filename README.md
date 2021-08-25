# Flask REST API

## Description
A read-only REST API that returns one or more records from static set of compensation data (JSON file).

### Why I chose this exercise:
I do a fair amount of both API design and data modeling in my current position, but in terms of an exercise that would demonstrate my abilities, the API exercise seemed like a more fun way to spend an afternoon. It's a bit more interactive and there's a little more immediate satisfaction when it works. Sometimes you don't know if data modeling is successful until it isn't.

### A short explanation:
I chose to use Flask for this exercise because it was an appropriate tool for the job. I have some working experience with Flask so having a familiar friend within the time constraint was helpful as well.

I took a pretty minimal approach to deserialization by immediately converting the list of dicts from the JSON file to a standardized dict with a few friendly-named fields. This created a nice path for adding additional data sources in the future. In a more typical, real world application the data would likely be stored in a relational database and represented in the code as a class object. And the queries would be SQL. Doing some pseudo querying using class attributes would then be less typical, make the logic lean toward field-level specificity and make it more difficult to change as fields or requirements changed.

I enjoy using TDD when it makes sense, so the test suite is representative of that process and mostly includes success cases.

The records straight from the JSON file don't have a unique identifier, so used the index in the list of records from the JSON file as a sort of record ID that can be used to request/return a single record.

### Feedback
The acceptance criteria for this exercise around normalizing/serializing was a little vague. I wasn't sure if the intent was for the response itself to be serialized back to JSON, which you almost get for free in this case, or for it to just have friendly field names that matched the query params. Maybe an example response would have helped, but maybe also be too prescriptive. I spent a good amount of time waffling and second guessing around this criteria.

## Steps to run locally
- Clone repo and navigate to project directory
- Set up and activate virtual environment, e.g.:
    ```
    $ python3 -m venv env
    $ source env/bin/activate
    ```
- Install dependencies:
    ```
    $ pip install -r requirements.txt
    ```
- Start the app:
    ```
    $ python app.py
    ```
- Navigate to `localhost:5000/compensation_data` in your browser to retrieve all records.


## Running unit tests
Within virtual environment and from project directory:
```
$ pytest
```

---

## Usage
### Get single record
Example:
- `GET /compensation_data/50`

### Filter results by exact match
Field options:
- `salary` (int)
- `employment_type` (str)
- `vacation_weeks` (int)
- `company` (str)
- `job_title` (str)

Example:
- `GET /compensation_data?salary=120000&employment_type=part-time` returns records that match the provided values.

### Filter results greater than or equal to
Fields:
- `salary[gte]` (int)

Example:
- `GET /compensation_data?salary[gte]=120000` returns matches with salaries greater or equal to the provided value.

### Sort results

Field options:
- `salary` (int)
- `employment_type` (str)
- `vacation_weeks` (int)
- `company` (str)
- `job_title` (str)

Example:
- `GET /compensation_data?salary[gte]=120000&sort=vacation_weeks` returns matches with salaries greater or equal to the provided value sorted by annual vacation weeks ascending.

### Limit results

Example:
- `GET /compensation_data?limit=10` returns the first 10 records.
