import json
from compensation_info import CompensationInfo

survey_2_field_mapper = {
    'salary': 'Total Base Salary in 2018 (in USD)',
    'employment_type': 'Employment Type',
    'vacation_weeks': 'Annual Vacation (in Weeks)',
    'company': 'Company Name',
    'job_title': 'Job Title In Company'
}

def get_data(file_path):
    """Reads JSON file from path and returns Python object"""
    
    with open(file_path) as f:
        data = json.load(f)

    return data


def get_normalized_records(file_path = 'salary_survey-2.json'):
    """Normalizes field names from list of dicts into friendly/consistent field names"""
    survey_2_data = get_data(file_path)

    records = [
        { k : x[survey_2_field_mapper[k]] for k in survey_2_field_mapper } 
        for x in survey_2_data
    ]

    return records


def get_records(request_args):
    """Gets records that match the request arguments.

    Args:
        request_args (ImmutableMultiDict): Request query params for specifying data to return.
        data_file_path (str): Optional; The relative path to the JSON data file.
    
    Returns:
        list: List of records as dicts.
    """

    records = get_normalized_records()

    sort_field = request_args.get('sort')
    limit = request_args.get('limit')

    records = filter_by(request_args, records)
    if sort_field is not None:
        records = sort_by(sort_field, records)
    if limit is not None:
        records = limit_by(limit, records)

    return records


def get_record(id):
    """Returns dict from list by its index"""
    records = get_normalized_records()
    try:
        return records[id]
    except IndexError:
        return None


def get_gte(records, field, requested_value):
    """Returns list of records with field value greater than or equal to field and value requested"""

    return [x for x in records if float(x[field]) >= int(requested_value)]


def get_match(records, field, requested_value):
    """Returns list of records that match the field and value requested"""

    return [x for x in records if x[field].lower() == requested_value.lower()]


def filter_by(filter_args, records):
    """Returns list of records matching requested filter arguments"""

    for k, v in filter_args.items():
        if k[-5:] == '[gte]':
            records = get_gte(records, k[:-5], v)
        elif k in survey_2_field_mapper.keys():
            records = get_match(records, k, v)
    
    return records


def sort_by(field, records):
    return sorted(records, key=lambda k: k[field])


def limit_by(limit, records):
    return records[:int(limit)]


def validate_request_args(request_args):
    """Validates field and value of request arguments.

    Args:
        request_args (ImmutableMultiDict): Request query params.
    
    Returns:
        None
    
    Raises:
        ValueError: Unknown field, or invalid value, or invalid value type was provided.
    """

    sort_field = request_args.get('sort')
    valid_fields = survey_2_field_mapper.keys()
    if sort_field is not None and sort_field not in valid_fields:
        raise ValueError(f'Invalid sort argument: "{sort_field}". Must be one of: {list(valid_fields)}')
    
    integer_type_fields = ['limit', 'salary', 'salary[gte]', 'vacation_weeks']
    for arg in integer_type_fields:
        val = request_args.get(arg)
        if val is not None:
            try:
                int(val)
            except:
                raise ValueError(f'Invalid value passed for "{arg}": "{val}" must be an integer.')
