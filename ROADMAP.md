## Things to add
- Negative unit tests and edge case coverage
- Additional data validation, protobuf might be a nice option.
- Authentication/authorization
- API/integration testing
- Additional CRUD endpoints

## Things to change
- `data_retriever.py` is doing more thatn just retrieving data. Some of this can/should be abstracte and tested separately.
- Do the other exercise, too (together they make one the other more interesting)
    - Import all three JSON datasets into relational database
    - Deserialize db record into class object
    - Query data using SQL instead of parsing through a list of dicts