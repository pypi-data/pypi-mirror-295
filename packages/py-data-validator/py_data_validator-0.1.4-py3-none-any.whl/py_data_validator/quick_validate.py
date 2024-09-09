from py_data_validator.validator import Validator


def quick_validate(data, rules, messages=None):
    validator = Validator(data, rules, messages)

    response = validator.validate()

    return response.validated
