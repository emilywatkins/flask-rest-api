from data_retriever import get_data, get_records, get_gte, get_match, filter_by, sort_by, limit_by, validate_request_args, get_normalized_records
from werkzeug.datastructures import ImmutableMultiDict
import pytest

def test_get_data():
    data = get_data('test_salary_survey-2.json')

    assert type(data) == list
    assert len(data) == 2


def test_get_gte():
    records = get_data('test_salary_survey-2.json')
    expected = records[0]
    result = get_gte(records, 'Total Base Salary in 2018 (in USD)', '160000')

    assert len(result) == 1
    assert result[0] == expected


def test_get_match():
    records = get_data('test_salary_survey-2.json')
    expected = records[1]
    result = get_match(records, 'Employment Type', 'Part-time')

    assert len(result) == 1
    assert result[0] == expected


def test_filter_by():
    records = get_normalized_records('test_salary_survey-2.json')
    salary = records[0]['salary']
    filters = ImmutableMultiDict([('salary', salary)])

    result = filter_by(filters, records)
    assert len(result) == 1


def test_sort_by():
    records = get_normalized_records('test_salary_survey-2.json')
    record1 = records[0]
    record1_vacation_weeks = record1['vacation_weeks']
    record2 = records[1]
    record2_vacation_weeks = record2['vacation_weeks']

    assert record1_vacation_weeks > record2_vacation_weeks

    result = sort_by('vacation_weeks', records)
    assert result[0] == records[1]


def test_limit_by():
    records = get_data('test_salary_survey-2.json')
    assert len(records) == 2

    result = limit_by(1, records)
    assert len(result) == 1


def test_validate_request_args_raises_error():
    # sort field
    args = ImmutableMultiDict([('sort', '123')])
    with pytest.raises(ValueError, match='123'):
        validate_request_args(args)
    
    # integer field types
    integer_types = ['limit', 'salary', 'salary[gte]', 'vacation_weeks']
    for t in integer_types:
        args = ImmutableMultiDict([(t, 'abc')])
        with pytest.raises(ValueError, match='abc'):
            validate_request_args(args)


def test_validate_request_args_success():
    args = ImmutableMultiDict(
        [
            ('sort', 'salary'),
            ('limit', '10'),
            ('salary', '1'),
            ('salary[gte]', '1'),
            ('employment_type', 'part-time'),
            ('vacation_weeks', '4')
        ]
    )

    validate_request_args(args)


# def test_deserialize():
#     result = survey_2_compensation_info()
#     print(result[0].salary)
#     assert False


def test_normalize():
    result = get_normalized_records()
    print(result[0])
    assert False