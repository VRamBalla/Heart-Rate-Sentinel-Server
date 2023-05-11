import pytest
import pandas as pd
from testfixtures import LogCapture
import numpy as np
import logging
from ast import literal_eval

# **************************Junqi Lu starts**************************

logging.basicConfig(level=logging.INFO, filename='logFile.log',
                    filemode='w')
logging.getLogger("urllib3").setLevel(logging.WARNING)  # Supress debug
# logging from urllib3 in test_hrss_server.py, which seems to be related
# to the email server

# Initialize the global databases with corresponding columns but no data yet,
# so all of their len() will be 0. They're ready to store data
physician_db = pd.DataFrame(
    columns=['attending_username', 'attending_email', 'attending_phone'])
patient_db = pd.DataFrame(
    columns=['patient_id', 'attending_username', 'patient_age',
             'heart_rate_history'])
admin_db = pd.DataFrame(columns=['admin_username', 'admin_password'])


@pytest.mark.parametrize('value_msg_list, value_judgement, in_data, '
                         'expect_msg, expect_status', [
                             (['No matching attending physician from '
                               'physician database.'], False,
                              {"patient_id": 820,
                               "attending_username": 'Banks.J',
                               "patient_age": 25},
                              'No matching attending physician from '
                              'physician database.\nThe physician database '
                              'is empty. You need to have at least 1 '
                              'physician available to start to register for '
                              'new patients.',
                              400),
                             (['No matching attending physician from '
                               'physician database.'], False,
                              {"patient_id": '820',
                               "attending_username": 'Banks.J',
                               "patient_age": 25},
                              'No matching attending physician from '
                              'physician database.\nThe physician database '
                              'is empty. You need to have at least 1 '
                              'physician available to start to register for '
                              'new patients.',
                              400),
                             (['No matching attending physician from '
                               'physician database.'], False,
                              {"patient_id": 820,
                               "attending_username": 'Banks.J',
                               "patient_age": '25'},
                              'No matching attending physician from '
                              'physician database.\nThe physician database '
                              'is empty. You need to have at least 1 '
                              'physician available to start to register for '
                              'new patients.',
                              400),
                             (['No matching attending physician from '
                               'physician database.'], False,
                              {"patient_id": '820',
                               "attending_username": 'Banks.J',
                               "patient_age": '25'},
                              'No matching attending physician from '
                              'physician database.\nThe physician database '
                              'is empty. You need to have at least 1 '
                              'physician available to start to register for '
                              'new patients.',
                              400),
                             ([
                                  "Field \"patient_id\" value does not match "
                                  "regex '^[0-9][0-9]*$'."],
                              False, {"patient_id": 'l820',
                                      "attending_username": 'Banks.J',
                                      "patient_age": 25},
                              "Field \"patient_id\" value does not match "
                              "regex '^[0-9][0-9]*$'.\nThe physician "
                              "database is empty. You need to have at least "
                              "1 physician available to start to register "
                              "for new patients.",
                              400),
                             ([
                                  "Field \"patient_id\" value does not match "
                                  "regex '^[0-9][0-9]*$'."],
                              False, {"patient_id": '8l20',
                                      "attending_username": 'Banks.J',
                                      "patient_age": 25},
                              "Field \"patient_id\" value does not match "
                              "regex '^[0-9][0-9]*$'.\nThe physician "
                              "database is empty. You need to have at "
                              "least 1 physician available to start to "
                              "register for new patients.",
                              400),
                             ([
                                  "Field \"patient_id\" value does not match "
                                  "regex '^[0-9][0-9]*$'."],
                              False, {"patient_id": '820l',
                                      "attending_username": 'Banks.J',
                                      "patient_age": 25},
                              "Field \"patient_id\" value does not match "
                              "regex '^[0-9][0-9]*$'.\nThe physician "
                              "database is empty. You need to have at "
                              "least 1 physician available to start to "
                              "register for new patients.",
                              400),
                             ([
                                  "Field \"patient_age\" value does not "
                                  "match regex '^[0-9][0-9]*$'."],
                              False, {"patient_id": '820',
                                      "attending_username": 'Banks.J',
                                      "patient_age": 'l25'},
                              "Field \"patient_age\" value does not "
                              "match "
                              "regex '^[0-9][0-9]*$'.\nThe physician "
                              "database is empty. You need to have at "
                              "least 1 physician available to start to "
                              "register for new patients.",
                              400),
                             ([
                                  "Field \"patient_age\" value does not "
                                  "match regex '^[0-9][0-9]*$'."],
                              False, {"patient_id": '820',
                                      "attending_username": 'Banks.J',
                                      "patient_age": '2l5'},
                              "Field \"patient_age\" value does not "
                              "match "
                              "regex '^[0-9][0-9]*$'.\nThe physician "
                              "database is empty. You need to have at "
                              "least 1 physician available to start to "
                              "register for new patients.",
                              400),
                             ([
                                  "Field \"patient_age\" value does not "
                                  "match regex '^[0-9][0-9]*$'."],
                              False, {"patient_id": '820',
                                      "attending_username": 'Banks.J',
                                      "patient_age": '25l'},
                              "Field \"patient_age\" value does not "
                              "match "
                              "regex '^[0-9][0-9]*$'.\nThe physician "
                              "database is empty. You need to have at least "
                              "1 physician available to start to register "
                              "for new patients.",
                              400)
                         ])
def test_empty_db_post_new_patient_worker(value_msg_list, value_judgement,
                                          in_data, expect_msg, expect_status):
    from hrss_server import post_new_patient_worker

    out_msg, status = post_new_patient_worker(value_msg_list, value_judgement,
                                              in_data)

    assert status == expect_status
    assert out_msg == expect_msg


@pytest.mark.parametrize('value_msg_list, value_judgement, in_data, '
                         'expect_msg, expect_status', [
                             (['This patient_id does not exist.'], False,
                              {"patient_id": 82,
                               "heart_rate": 151},
                              'This patient_id does not exist.\nThe patient '
                              'database is empty. You '
                              'need to have at least 1 patient available to '
                              'register for new heart '
                              'rate measurement.', 400),
                             (['This patient_id does not exist.'], False,
                              {"patient_id": '82',
                               "heart_rate": 151},
                              'This patient_id does not exist.\nThe patient '
                              'database is empty. You '
                              'need to have at least 1 patient available to '
                              'register for new heart '
                              'rate measurement.', 400),
                             (['This patient_id does not exist.'], False,
                              {"patient_id": 82,
                               "heart_rate": '151'},
                              'This patient_id does not exist.\nThe patient '
                              'database is empty. You '
                              'need to have at least 1 patient available to '
                              'register for new heart '
                              'rate measurement.', 400),
                             (['This patient_id does not exist.'], False,
                              {"patient_id": '82',
                               "heart_rate": '151'},
                              'This patient_id does not exist.\nThe patient '
                              'database is empty. You '
                              'need to have at least 1 patient available to '
                              'register for new heart '
                              'rate measurement.', 400),
                             ([
                                  "Field \"patient_id\" value does not match "
                                  "regex '^[0-9][0-9]*$'."],
                              False, {"patient_id": 'l82', "heart_rate": 151},
                              "Field \"patient_id\" "
                              "value does not match "
                              "regex '^[0-9]["
                              "0-9]*$'.\nThe patient database is empty. You "
                              "need to have at least 1 patient available to "
                              "register for new heart rate measurement.",
                              400),
                             ([
                                  "Field \"patient_id\" value does not match "
                                  "regex '^[0-9][0-9]*$'."],
                              False, {"patient_id": '8l2', "heart_rate": 151},
                              "Field \"patient_id\" "
                              "value does not match "
                              "regex '^[0-9]["
                              "0-9]*$'.\nThe patient database is empty. You "
                              "need to have at least 1 patient available to "
                              "register for new heart rate measurement.",
                              400),
                             ([
                                  "Field \"patient_id\" value does not match "
                                  "regex '^[0-9][0-9]*$'."],
                              False, {"patient_id": '82l', "heart_rate": 151},
                              "Field \"patient_id\" "
                              "value does not match "
                              "regex '^[0-9]["
                              "0-9]*$'.\nThe patient database is empty. You "
                              "need to have at least 1 patient available to "
                              "register for new heart rate measurement.",
                              400),
                             ([
                                  "Field \"heart_rate\" value does not match "
                                  "regex '^[0-9][0-9]*$'."],
                              False, {"patient_id": 82, "heart_rate": 'l151'},
                              "Field \"heart_rate\" "
                              "value does not match "
                              "regex '^[0-9]["
                              "0-9]*$'.\nThe patient database is empty. You "
                              "need to have at least 1 patient available to "
                              "register for new heart rate measurement.",
                              400),
                             ([
                                  "Field \"heart_rate\" value does not match "
                                  "regex '^[0-9][0-9]*$'."],
                              False, {"patient_id": 82, "heart_rate": '1l51'},
                              "Field \"heart_rate\" "
                              "value does not match "
                              "regex '^[0-9]["
                              "0-9]*$'.\nThe patient database is empty. You "
                              "need to have at least 1 patient available to "
                              "register for new heart rate measurement.",
                              400),
                             ([
                                  "Field \"heart_rate\" value does not match "
                                  "regex '^[0-9][0-9]*$'."],
                              False, {"patient_id": 82, "heart_rate": '151l'},
                              "Field \"heart_rate\" "
                              "value does not match "
                              "regex '^[0-9]["
                              "0-9]*$'.\nThe patient database is empty. You "
                              "need to have at least 1 patient available to "
                              "register for new heart rate measurement.",
                              400),
                             ([
                                  "Field \"heart_rate\" value does not match "
                                  "regex '^[0-9][0-9]*$'.",
                                  "Field "
                                  "\"patient_id\" value does not match regex "
                                  "'^[0-9][0-9]*$'."],
                              False,
                              {"patient_id": 'l82', "heart_rate": 'l151'},
                              "Field "
                              "\"heart_rate\" "
                              "value does not match "
                              "regex '^[0-9]["
                              "0-9]*$'.\nField "
                              "\"patient_id\" value does not match regex '^["
                              "0-9][0-9]*$'.\nThe "
                              "patient database is empty. You need to have "
                              "at least 1 patient available to register for "
                              "new heart rate measurement.",
                              400)

                         ])
def test_empty_db_post_heart_rate_worker(value_msg_list, value_judgement,
                                         in_data, expect_msg, expect_status):
    from hrss_server import post_heart_rate_worker
    out_msg, status = post_heart_rate_worker(value_msg_list,
                                             value_judgement, in_data)

    assert out_msg == expect_msg
    assert status == expect_status


@pytest.mark.parametrize('value_msg_list, value_judgement, patient_id, '
                         'expect_msg, expect_status', [
                             (['This patient_id does not exist.'], False, 82,
                              "This patient_id does not exist.\nThe patient "
                              "database is empty. You "
                              "need to have at least 1 patient available to "
                              "get the info of the last heart rate "
                              "measurement of a patient.",
                              400),
                             (
                                     [
                                         "The patient_id's data format is "
                                         "wrong."],
                                     False,
                                     '8l2', "The patient_id's data format is "
                                            "wrong.\nThe patient database is "
                                            "empty. "
                                            "You need to have at "
                                            "least 1 patient available to "
                                            "get the info of "
                                            "the last heart rate measurement "
                                            "of a patient.",
                                     400),
                             (
                                     [
                                         "The patient_id's data format is "
                                         "wrong."],
                                     False,
                                     'li',
                                     "The patient_id's data format is "
                                     "wrong.\nThe "
                                     "patient database is empty. You need to "
                                     "have at "
                                     "least 1 patient available to get the "
                                     "info of "
                                     "the last heart rate measurement of a "
                                     "patient.",
                                     400)
                         ])
def test_empty_db_get_patient_status_worker(value_msg_list, value_judgement,
                                            patient_id, expect_msg,
                                            expect_status):
    from hrss_server import get_patient_status_worker
    out_msg, status = get_patient_status_worker(value_msg_list,
                                                value_judgement, patient_id)

    assert out_msg == expect_msg
    assert status == expect_status


@pytest.mark.parametrize('value_msg_list, value_judgement, patient_id, '
                         'expect_msg, expect_status', [
                             (['This patient_id does not exist.'], False, 82,
                              "This patient_id does not exist.\nThe patient "
                              "database is empty. You "
                              "need to have at least 1 patient available to "
                              "get all the heart rates in a list of a "
                              "patient.",
                              400),
                             (
                                     [
                                         "The patient_id's data format is "
                                         "wrong."],
                                     False,
                                     '8l2',
                                     "The patient_id's data format is "
                                     "wrong.\nThe patient database is empty. "
                                     "You need to have at least 1 patient "
                                     "available to get all the heart rates "
                                     "in a list of a patient.",
                                     400),
                             (
                                     [
                                         "The patient_id's data format is "
                                         "wrong."],
                                     False,
                                     'li',
                                     "The patient_id's data format is "
                                     "wrong.\nThe patient database is empty. "
                                     "You need to have at least 1 patient "
                                     "available to get all the heart rates "
                                     "in a list of a patient.",
                                     400)
                         ])
def test_empty_db_get_heart_rate_list_worker(value_msg_list, value_judgement,
                                             patient_id, expect_msg,
                                             expect_status):
    from hrss_server import get_heart_rate_list_worker
    out_msg, status = get_heart_rate_list_worker(value_msg_list,
                                                 value_judgement,
                                                 patient_id)
    assert out_msg == expect_msg
    assert status == expect_status


def test_initialize_database():  # I have to put the initialization
    # process in a test function merely to force pytest to initialize the db
    # after testing all the cases when a user is trying to obtain info from
    # empty db--those test functions need to run before db initialization.
    # This function is not testing anything; having "test" in the function
    # name is needed or pytest won't run this function
    from hrss_server import init_database
    init_database()  # Initialize all these dummy data's df for unit testing of
    # the functions below


@pytest.mark.parametrize('in_data, parent_function, expect_judgement, '
                         'expect_msg_list', [
                             ({"patient_id": 39,
                               "attending_username": 'Hernandez.O',
                               "patient_age": 25}, 'new_patient_type_validate',
                              True, []),
                             ({"patient_id": '39',
                               "attending_username": 'Hernandez.O',
                               "patient_age": 25}, 'new_patient_type_validate',
                              True, []),
                             ({"patient_id": 39,
                               "attending_username": 'Hernandez.O',
                               "patient_age": '25'},
                              'new_patient_type_validate', True, []),
                             ({"patient_id": '39',
                               "attending_username": 'Hernandez.O',
                               "patient_age": '25'},
                              'new_patient_type_validate', True, []),
                             ({"patient_id": 'p39',
                               "attending_username": 'Hernandez.O',
                               "patient_age": 25}, 'new_patient_type_validate',
                              False,
                              [
                                  'Field "patient_id" value does not match '
                                  'regex \'^[0-9][0-9]*$\'.']),
                             ({"patient_id": '3p9',
                               "attending_username": 'Hernandez.O',
                               "patient_age": 25}, 'new_patient_type_validate',
                              False,
                              [
                                  'Field "patient_id" value does not match '
                                  'regex \'^[0-9][0-9]*$\'.']),
                             ({"patient_id": '39p',
                               "attending_username": 'Hernandez.O',
                               "patient_age": 25}, 'new_patient_type_validate',
                              False,
                              [
                                  'Field "patient_id" value does not match '
                                  'regex \'^[0-9][0-9]*$\'.']),
                             ({"patient_id": 39,
                               "attending_username": 'Hernandez.O',
                               "patient_age": 'p25'},
                              'new_patient_type_validate', False,
                              ['Field "patient_age" value does not '
                               'match regex \'^[0-9][0-9]*$\'.']),
                             ({"patient_id": 39,
                               "attending_username": 'Hernandez.O',
                               "patient_age": '2p5'},
                              'new_patient_type_validate', False,
                              ['Field "patient_age" value does not '
                               'match regex \'^[0-9][0-9]*$\'.']),
                             ({"patient_id": 39,
                               "attending_username": 'Hernandez.O',
                               "patient_age": '25p'},
                              'new_patient_type_validate', False,
                              ['Field "patient_age" value does not '
                               'match regex \'^[0-9][0-9]*$\'.']),
                             ({"patient_id": 39,
                               "attending_username": '123Hernandez.O',
                               "patient_age": 25}, 'new_patient_type_validate',
                              False, [
                                  "Field \"attending_username\" value does "
                                  "not match regex '^[A-Z][a-z]*.[A-Z]'."]),
                             ({"patient_id": '3e9',
                               "attending_username": '123Hernandez.O',
                               "patient_age": '23p'},
                              'new_patient_type_validate', False, [
                                  "Field \"attending_username\" value does "
                                  "not match regex '^[A-Z][a-z]*.[A-Z]'.",
                                  'Field "patient_age" value does not match '
                                  'regex \'^[0-9][0-9]*$\'.',
                                  'Field "patient_id" value does not match '
                                  'regex \'^[0-9][0-9]*$\'.']),
                             ({"patient_id": '39',
                               "attending_username": '123Hernandez.O',
                               "patient_age": '23p'},
                              'new_patient_type_validate', False, [
                                  "Field \"attending_username\" value does "
                                  "not match regex '^[A-Z][a-z]*.[A-Z]'.",
                                  'Field "patient_age" value does not match '
                                  'regex \'^[0-9][0-9]*$\'.']),
                             ({"patient_id": '39p',
                               "attending_username": '123Hernandez.O',
                               "patient_age": '23'},
                              'new_patient_type_validate', False, [
                                  "Field \"attending_username\" value does "
                                  "not match regex '^[A-Z][a-z]*.[A-Z]'.",
                                  'Field "patient_id" value does not match '
                                  'regex \'^[0-9][0-9]*$\'.']),
                             ({"patient_id": 82, "heart_rate": 60},
                              'new_heart_rate_value_validate',
                              True, []),
                             ({"patient_id": '82', "heart_rate": 60},
                              'new_heart_rate_value_validate', True, []),
                             ({"patient_id": 82, "heart_rate": '60'},
                              'new_heart_rate_value_validate', True, []),
                             ({"patient_id": '82', "heart_rate": '60'},
                              'new_heart_rate_value_validate', True, []),
                             ({"patient_id": '8k2', "heart_rate": 60},
                              'new_heart_rate_value_validate', False,
                              [
                                  'Field "patient_id" value does not match '
                                  'regex \'^[0-9][0-9]*$\'.']),
                             ({"patient_id": 82, "heart_rate": '6l0'},
                              'new_heart_rate_value_validate', False,
                              [
                                  'Field "heart_rate" value does not match '
                                  'regex \'^[0-9][0-9]*$\'.']),
                             ({"patient_id": '82u', "heart_rate": 'l60'},
                              'new_heart_rate_value_validate', False,
                              [
                                  'Field "heart_rate" value does not match '
                                  'regex \'^[0-9][0-9]*$\'.',
                                  'Field "patient_id" value does not match '
                                  'regex \'^[0-9][0-9]*$\'.']),
                             ([{"patient_id": 39,
                                "attending_username": 'Hernandez.O',
                                "patient_age": 25}],
                              'new_patient_type_validate',
                              False,
                              ['The input data need to be a dictionary.']),
                             ([{"patient_id": 82, "heart_rate": 60}],
                              'new_heart_rate_value_validate', False,
                              ['The input data need to be a dictionary.']),
                             ({"attending_username": 'Hernandez.O',
                               "patient_age": 25}, 'new_patient_type_validate',
                              False, ['Field "patient_id" required field.']),
                             ({
                                  "patient_age": 25},
                              'new_patient_type_validate',
                              False, ['Field "attending_username" required '
                                      'field.', 'Field "patient_id" required '
                                                'field.']),
                             ({}, 'new_patient_type_validate',
                              False, ['Field "attending_username" required '
                                      'field.',
                                      'Field "patient_age" required field.',
                                      'Field "patient_id" required '
                                      'field.']),
                             ({"heart_rate": 60},
                              'new_heart_rate_value_validate', False,
                              ['Field "patient_id" required field.']),
                             ({},
                              'new_heart_rate_value_validate', False,
                              ['Field "heart_rate" required field.',
                               'Field "patient_id" required '
                               'field.']),
                             ({"patient_id": 39,
                               "attending_username": 'Hernandez.O',
                               "patient_age": 25, 'extra': 1000},
                              'new_patient_type_validate',
                              True, []),
                             ({"patient_id": 82, "heart_rate": 60,
                               'extra': '1000'},
                              'new_heart_rate_value_validate',
                              True, [])

                         ])
def test_in_data_type_validate(in_data, parent_function, expect_judgement,
                               expect_msg_list):
    from hrss_server import in_data_type_validate
    if parent_function == 'new_patient_type_validate':
        scheme = {
            "patient_id": {'required': True,
                           'type': ['integer', 'string'],
                           'regex': '^[0-9][0-9]*$',  # Can have leading 0
                           # If type is string, regex matches a string of
                           # number starting with any digit but zero
                           },
            "attending_username": {'required': True,
                                   'type': 'string',
                                   'regex': '^[A-Z][a-z]*.[A-Z]'
                                   # regex matches a string in the format
                                   # "LastName.FirstInitial" such as "Smith.J"
                                   },
            "patient_age": {'required': True,
                            'type': ['integer', 'string'],
                            'regex': '^[0-9][0-9]*$',
                            # If type is string, regex matches a string of
                            # number starting with any digit but zero
                            'min': 1
                            # All patients will be one year old or older
                            }
        }
    else:  # if parent_function == 'new_heart_rate_value_validate':
        scheme = {
            "patient_id": {'required': True,
                           'type': ['integer', 'string'],
                           'regex': '^[0-9][0-9]*$',
                           # If type is string, regex matches a string of
                           # number starting with any digit but zero
                           },
            "heart_rate": {'required': True,
                           'type': ['integer', 'string'],
                           'regex': '^[0-9][0-9]*$',
                           # If type is string, regex matches a string of
                           # number starting with any digit but zero. Also, the
                           # heart_rate can't be a decimal
                           }
        }

    judgement, type_msg_list = in_data_type_validate(in_data, scheme)

    assert judgement == expect_judgement
    assert type_msg_list == expect_msg_list


@pytest.mark.parametrize('in_data, expect_judgement, expect_msg_list', [
    ({"patient_id": 39, "attending_username": 'Hernandez.O',
      "patient_age": 25}, True, []),
    ({"patient_id": '39', "attending_username": 'Hernandez.O',
      "patient_age": 25}, True, []),
    ({"patient_id": 39, "attending_username": 'Hernandez.O',
      "patient_age": '25'}, True, []),
    ({"patient_id": '39', "attending_username": 'Hernandez.O',
      "patient_age": '25'}, True, []),
    ({"patient_id": 'p39', "attending_username": 'Hernandez.O',
      "patient_age": 25}, False,
     ['Field "patient_id" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": '3p9', "attending_username": 'Hernandez.O',
      "patient_age": 25}, False,
     ['Field "patient_id" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": '39p', "attending_username": 'Hernandez.O',
      "patient_age": 25}, False,
     ['Field "patient_id" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": 39, "attending_username": 'Hernandez.O',
      "patient_age": 'p25'}, False, ['Field "patient_age" value does not '
                                     'match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": 39, "attending_username": 'Hernandez.O',
      "patient_age": '2p5'}, False, ['Field "patient_age" value does not '
                                     'match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": 39, "attending_username": 'Hernandez.O',
      "patient_age": '25p'}, False, ['Field "patient_age" value does not '
                                     'match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": 39, "attending_username": '123Hernandez.O',
      "patient_age": 25}, False, [
         'Field "attending_username" value does not match regex \'^[A-Z]['
         'a-z]*.[A-Z]\'.']),
    ({"patient_id": '3e9', "attending_username": '123Hernandez.O',
      "patient_age": '23p'}, False, [
         'Field "attending_username" value does not match regex \'^[A-Z]['
         'a-z]*.[A-Z]\'.',
         'Field "patient_age" value does not match regex \'^[0-9][0-9]*$\'.',
         'Field "patient_id" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": '39', "attending_username": '123Hernandez.O',
      "patient_age": '23p'}, False, [
         'Field "attending_username" value does not match regex \'^[A-Z]['
         'a-z]*.[A-Z]\'.',
         'Field "patient_age" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": '39p', "attending_username": '123Hernandez.O',
      "patient_age": '23'}, False, [
         'Field "attending_username" value does not match regex \'^[A-Z]['
         'a-z]*.[A-Z]\'.',
         'Field "patient_id" value does not match regex \'^[0-9][0-9]*$\'.'])

])
def test_new_patient_type_validate(in_data, expect_judgement, expect_msg_list):
    from hrss_server import new_patient_type_validate
    judgement, msg_list = new_patient_type_validate(in_data)
    assert judgement == expect_judgement
    assert msg_list == expect_msg_list


@pytest.mark.parametrize('in_data, expect_judgement, expect_msg_list', [
    ({"patient_id": 39, "attending_username": 'Hernandez.O',
      "patient_age": 25}, True, []),
    ({"patient_id": '39', "attending_username": 'Hernandez.O',
      "patient_age": 25}, True, []),
    ({"patient_id": 39, "attending_username": 'Hernandez.O',
      "patient_age": '25'}, True, []),
    ({"patient_id": '39', "attending_username": 'Hernandez.O',
      "patient_age": '25'}, True, []),
    ({"patient_id": 'p39', "attending_username": 'Hernandez.O',
      "patient_age": 25}, False,
     ['Field "patient_id" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": '3p9', "attending_username": 'Hernandez.O',
      "patient_age": 25}, False,
     ['Field "patient_id" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": '39p', "attending_username": 'Hernandez.O',
      "patient_age": 25}, False,
     ['Field "patient_id" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": 39, "attending_username": 'Hernandez.O',
      "patient_age": 'p25'}, False, ['Field "patient_age" value does not '
                                     'match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": 39, "attending_username": 'Hernandez.O',
      "patient_age": '2p5'}, False, ['Field "patient_age" value does not '
                                     'match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": 39, "attending_username": 'Hernandez.O',
      "patient_age": '25p'}, False, ['Field "patient_age" value does not '
                                     'match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": 39, "attending_username": '123Hernandez.O',
      "patient_age": 25}, False, [
         'Field "attending_username" value does not match regex \'^[A-Z]['
         'a-z]*.[A-Z]\'.']),
    ({"patient_id": '3e9', "attending_username": '123Hernandez.O',
      "patient_age": '23p'}, False, [
         'Field "attending_username" value does not match regex \'^[A-Z]['
         'a-z]*.[A-Z]\'.',
         'Field "patient_age" value does not match regex \'^[0-9][0-9]*$\'.',
         'Field "patient_id" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": '39', "attending_username": '123Hernandez.O',
      "patient_age": '23p'}, False, [
         'Field "attending_username" value does not match regex \'^[A-Z]['
         'a-z]*.[A-Z]\'.',
         'Field "patient_age" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": '39p', "attending_username": '123Hernandez.O',
      "patient_age": '23'}, False, [
         'Field "attending_username" value does not match regex \'^[A-Z]['
         'a-z]*.[A-Z]\'.',
         'Field "patient_id" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": 8, "attending_username": 'Hernandez.O',
      "patient_age": 25}, False,
     ['This patient_id is already in use.']),
    ({"patient_id": 39, "attending_username": 'Apple.A',
      "patient_age": 25}, False, ['No matching attending physician '
                                  'from physician database.']),
    ({"patient_id": 8, "attending_username": 'Apple.A',
      "patient_age": 25}, False, ['This patient_id is already in use.',
                                  'No matching attending physician from '
                                  'physician database.'])
])
def test_new_patient_value_validate(in_data, expect_judgement,
                                    expect_msg_list):
    from hrss_server import new_patient_value_validate, patient_db, \
        physician_db

    judgement, msg_list = new_patient_value_validate(in_data)
    assert judgement == expect_judgement
    assert msg_list == expect_msg_list


@pytest.mark.parametrize('in_data, expect_new_row_list', [
    ({"patient_id": 39, "attending_username": 'Hernandez.O',
      "patient_age": 25},
     [39, 'Hernandez.O', 25, np.nan]),
    ({"patient_id": '39', "attending_username": 'Hernandez.O',
      "patient_age": 25}, [39, 'Hernandez.O', 25, np.nan]),
    ({"patient_id": 39, "attending_username": 'Hernandez.O',
      "patient_age": '25'},
     [39, 'Hernandez.O', 25, np.nan]),
    ({"patient_id": '39', "attending_username": 'Hernandez.O',
      "patient_age": '25'},
     [39, 'Hernandez.O', 25, np.nan])
])
def test_add_new_patient(in_data, expect_new_row_list):
    from hrss_server import add_new_patient, patient_db

    patient_db = add_new_patient(in_data)  # I have to keep the return
    # patient_db inside add_new_patient() and that's why I have the
    # "patient_db =" at the beginning of this line

    answer = patient_db.tail(1).values.flatten().tolist()  # This returns
    # the values in the last row as a list

    patient_db.drop(patient_db.tail(1).index, inplace=True)  # Drop the last
    # row, aka the newly added row so this test function doesn't modify the
    # patient_db when it's finished

    assert answer == expect_new_row_list


@pytest.mark.parametrize('value_msg_list, value_judgement, in_data, '
                         'expect_out_msg, expect_status', [
                             ([], True, {"patient_id": 39,
                                         "attending_username": 'Banks.J',
                                         "patient_age": 25},
                              'Patient with id 39 was successfully added '
                              'into the patient database.', 200),
                             ([], True, {"patient_id": '39',
                                         "attending_username": 'Hernandez.O',
                                         "patient_age": 25},
                              'Patient with id 39 was successfully added '
                              'into the patient database.', 200),
                             ([], True, {"patient_id": 39,
                                         "attending_username": 'Banks.J',
                                         "patient_age": '25'},
                              'Patient with id 39 was successfully added '
                              'into the patient database.', 200),
                             ([], True, {"patient_id": '39',
                                         "attending_username": 'Duffy.B',
                                         "patient_age": '25'},
                              'Patient with id 39 was successfully added '
                              'into the patient database.', 200),
                             ([
                                  "Field \"patient_id\" value does not match "
                                  "regex '^[1-9][0-9]*$'."],
                              False, {"patient_id": 'l39',
                                      "attending_username": 'Banks.J',
                                      "patient_age": 25},
                              "Field \"patient_id\" value does not match "
                              "regex '^[1-9][0-9]*$'.\nFix and request "
                              "again.", 400),
                             ([
                                  "Field \"patient_age\" value does not "
                                  "match regex '^[1-9][0-9]*$'.",
                                  "Field "
                                  "\"patient_id\" value does not match regex "
                                  "'^[1-9][0-9]*$'."],
                              False, {"patient_id": 'l39',
                                      "attending_username": 'Banks.J',
                                      "patient_age": '2p5'},
                              "Field \"patient_age\" value does not "
                              "match "
                              "regex '^[1-9][0-9]*$'.\nField \"patient_id\" "
                              "value does not match "
                              "regex '^[1-9][0-9]*$'.\nFix and request "
                              "again.", 400),
                             (['This patient_id is already in use.'], False,
                              {"patient_id": 93,
                               "attending_username": 'Banks.J',
                               "patient_age": 25},
                              'This patient_id is already in use.\nFix and '
                              'request again.',
                              400),
                             ([
                                  'No matching attending physician from '
                                  'physician database.'],
                              False, {"patient_id": 39,
                                      "attending_username": 'Banks.P',
                                      "patient_age": 25},
                              'No matching attending physician from '
                              'physician database.\nFix and '
                              'request again.',
                              400)
                         ])
def test_post_new_patient_worker(value_msg_list, value_judgement, in_data,
                                 expect_out_msg, expect_status):
    from hrss_server import post_new_patient_worker, patient_db
    global patient_db
    out_msg, status = post_new_patient_worker(value_msg_list,
                                              value_judgement, in_data,
                                              test_mode=True)

    assert out_msg == expect_out_msg
    assert status == expect_status


@pytest.mark.parametrize('value_msg_list, value_judgement, in_data, '
                         'expect_log', [
                             ([], True, {"patient_id": 39,
                                         "attending_username": 'Banks.J',
                                         "patient_age": 25}, ('root', 'INFO',
                                                              'Patient '
                                                              'with '
                                                              'id 39 was '
                                                              'successfully '
                                                              'added into the '
                                                              'patient '
                                                              'database.')),
                             ([], True, {"patient_id": '39',
                                         "attending_username": 'Banks.J',
                                         "patient_age": 25}, ('root', 'INFO',
                                                              'Patient '
                                                              'with '
                                                              'id 39 was '
                                                              'successfully '
                                                              'added into the '
                                                              'patient '
                                                              'database.')),
                             ([], True, {"patient_id": 39,
                                         "attending_username": 'Banks.J',
                                         "patient_age": '25'}, ('root', 'INFO',
                                                                'Patient '
                                                                'with '
                                                                'id 39 was '
                                                                'successfully '
                                                                'added into '
                                                                'the '
                                                                'patient '
                                                                'database.')),
                             ([], True, {"patient_id": '39',
                                         "attending_username": 'Dixon.K',
                                         "patient_age": '25'}, ('root', 'INFO',
                                                                'Patient '
                                                                'with '
                                                                'id 39 was '
                                                                'successfully '
                                                                'added into '
                                                                'the '
                                                                'patient '
                                                                'database.'))

                         ])
def test_log_post_new_patient_worker(value_msg_list, value_judgement,
                                     in_data, expect_log):
    from hrss_server import post_new_patient_worker, patient_db
    with LogCapture() as log_c:
        post_new_patient_worker(value_msg_list, value_judgement,
                                in_data, test_mode=True)
        # patient_db.drop(patient_db.tail(1).index,
        #                 inplace=True)  # Drop the last
        # row, aka the newly added row so this test function doesn't modify the
        # patient_db when it's finished
    log_c.check(expect_log)


@pytest.mark.parametrize('value_msg_list, value_judgement, in_data', [
    (['No matching attending physician from physician database.'],
     False, {"patient_id": 39,
             "attending_username": 'Banks.P',
             "patient_age": 25}),
    (['This patient_id is already in use.'], False,
     {"patient_id": 93,
      "attending_username": 'Banks.J',
      "patient_age": 25}),
    (["Field \"patient_id\" value does not match regex '^[1-9][0-9]*$'."],
     False, {"patient_id": 'l39',
             "attending_username": 'Banks.J',
             "patient_age": 25})

])
def test_no_log_post_new_patient_worker(value_msg_list, value_judgement,
                                        in_data):
    from hrss_server import post_new_patient_worker, patient_db
    with LogCapture() as log_c:
        post_new_patient_worker(value_msg_list, value_judgement,
                                in_data)

    log_c.check()


@pytest.mark.parametrize('in_data, expect_judgement,expect_msg_list', [
    ({"patient_id": 82, "heart_rate": 60}, True, []),
    ({"patient_id": '82', "heart_rate": 60}, True, []),
    ({"patient_id": 82, "heart_rate": '60'}, True, []),
    ({"patient_id": '82', "heart_rate": '60'}, True, []),
    ({"patient_id": '8k2', "heart_rate": 60}, False,
     ['Field "patient_id" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": 82, "heart_rate": '6l0'}, False,
     ['Field "heart_rate" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": '82u', "heart_rate": 'l60'}, False,
     ['Field "heart_rate" value does not match regex \'^[0-9][0-9]*$\'.',
      'Field "patient_id" value does not match regex \'^[0-9][0-9]*$\'.']),
])
def test_new_heart_rate_type_validate(in_data, expect_judgement,
                                      expect_msg_list):
    from hrss_server import new_heart_rate_type_validate
    judgement, msg_list = new_heart_rate_type_validate(in_data)
    assert judgement == expect_judgement
    assert msg_list == expect_msg_list


@pytest.mark.parametrize('in_data, expect_judgement,expect_msg_list', [
    ({"patient_id": 82, "heart_rate": 60}, True, []),
    ({"patient_id": '82', "heart_rate": 60}, True, []),
    ({"patient_id": 82, "heart_rate": '60'}, True, []),
    ({"patient_id": '82', "heart_rate": '60'}, True, []),
    ({"patient_id": '8k2', "heart_rate": 60}, False,
     ['Field "patient_id" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": 82, "heart_rate": '6l0'}, False,
     ['Field "heart_rate" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": '82u', "heart_rate": 'l60'}, False,
     ['Field "heart_rate" value does not match regex \'^[0-9][0-9]*$\'.',
      'Field "patient_id" value does not match regex \'^[0-9][0-9]*$\'.']),
    ({"patient_id": 820, "heart_rate": 60}, False, ['This patient_id does '
                                                    'not exist.']),
    ({"patient_id": 820, "heart_rate": '60'}, False, ['This patient_id does '
                                                      'not exist.']),
    ({"patient_id": '820', "heart_rate": 60}, False, ['This patient_id does '
                                                      'not exist.']),
    ({"patient_id": '820', "heart_rate": '60'}, False, ['This patient_id does '
                                                        'not exist.'])

])
def test_new_heart_rate_value_validate(in_data, expect_judgement,
                                       expect_msg_list):
    from hrss_server import new_heart_rate_value_validate, patient_db

    judgement, msg_list = new_heart_rate_value_validate(in_data)
    assert judgement == expect_judgement
    assert msg_list == expect_msg_list


@pytest.mark.parametrize('heart_rate_history_dict, expect', [
    ({'2016-07-10 13:12:48': 88, '2017-08-27 14:52:38': 74, '2017-10-07 '
                                                            '06:29:22': 114,
      '2019-07-25 12:35:24': 111}, {'2016-07-10 13:12:48': 88,
                                    '2017-08-27 14:52:38': 74,
                                    '2017-10-07 06:29:22': 114,
                                    '2019-07-25 12:35:24': 111}),
    ({'2019-07-25 12:35:24': 111, '2017-10-07 06:29:22': 114, '2017-08-27 '
                                                              '14:52:38': 74,
      '2016-07-10 13:12:48': 88}, {'2016-07-10 13:12:48': 88,
                                   '2017-08-27 14:52:38': 74,
                                   '2017-10-07 06:29:22': 114,
                                   '2019-07-25 12:35:24': 111}),
    ({'2019-07-25 12:35:24': 111}, {'2019-07-25 12:35:24': 111})
])
def test_sort_heart_rate_history_dict(heart_rate_history_dict, expect):
    from hrss_server import sort_heart_rate_history_dict
    answer = sort_heart_rate_history_dict(heart_rate_history_dict)

    assert answer == expect


@pytest.mark.parametrize('in_data, history_dict_exist, '
                         'expected_new_heart_rate', [
                             ({"patient_id": 62, "heart_rate": 72}, True, 72),
                             ({"patient_id": 62,
                               "heart_rate": '62'}, True, 62),
                             ({"patient_id": '62',
                               "heart_rate": 63}, True, 63),
                             ({"patient_id": '62', "heart_rate": '64'}, True,
                              64),
                             ({"patient_id": 82, "heart_rate": 65}, True, 65),
                             ({"patient_id": 82, "heart_rate": 65}, False, 65),
                             ({"patient_id": '82', "heart_rate": 65}, False,
                              65),
                             ({"patient_id": 82, "heart_rate": '65'}, False,
                              65),
                             ({"patient_id": '82', "heart_rate": '65'}, False,
                              65)
                         ])
def test_add_new_heart_rate(in_data, history_dict_exist,
                            expected_new_heart_rate):
    from hrss_server import add_new_heart_rate, \
        sort_heart_rate_history_dict, patient_db, current_time_str

    # Need the data type conversion below since these are already inside the
    # add_new_heart_rate() but I need these values
    patient_id = int(in_data['patient_id'])

    heart_rate_history_before = patient_db[patient_db['patient_id'] ==
                                           patient_id][
        'heart_rate_history'].values[0].copy()  # Using [0] is fine here since
    # each patient_id has only 1 dict that records all the heart rates. Make
    # a copy of it so heart_rate_history_before doesn't change after
    # patient_db = add_new_heart_rate(in_data)

    add_new_heart_rate(in_data, history_dict_exist)
    heart_rate_history = patient_db[patient_db['patient_id'] ==
                                    patient_id][
        'heart_rate_history'].values[0]  # Using [0] is fine here since each
    # patient_id has only 1 dict that records all the heart rates
    sorted_heart_rate_history = sort_heart_rate_history_dict(
        heart_rate_history)

    sorted_heart_rate_history_list = list(sorted_heart_rate_history)
    latest_date_time = sorted_heart_rate_history_list[-1]

    answer = sorted_heart_rate_history[latest_date_time]

    # Codes below basically revers the adding of the new heart rate so this
    # test function doesn't change the global database
    row_index = \
        patient_db.index[
            patient_db['patient_id'] == patient_id].values[
            0]  # Can use this method because all patient_id are unique

    # patient_db.loc[
    #     row_index, 'heart_rate_history'] = heart_rate_history_before  #
    # df.loc[] is the correct method to change the value of a cell in a df,
    # but it will give a ValueError: Incompatible indexer with Series when
    # the new value is a dict. pd development team is currently working on
    # this: https://github.com/pandas-dev/pandas/issues/17777

    # A less elegant way of restore the value in that cell
    patient_db.loc[row_index, 'heart_rate_history'] = [
        heart_rate_history_before]  # Add in a list of dict

    patient_db['heart_rate_history'] = patient_db['heart_rate_history'].apply(
        lambda x: x[0] if type(x) == list else x)  # For cells in column
    # "heart_rate_history", if the value of a cell is a list, convert it
    # into a dict; otherwise, keep it as it is

    assert answer == expected_new_heart_rate


@pytest.mark.parametrize('age, heart_rate, expect', [
    (2, 151, False),
    (2, 152, True),
    (5, 133, False),
    (5, 134, True),
    (15, 119, False),
    (15, 120, True),
    (16, 101, True),
    (27, 101, True),
    (100, 101, True)
])
def test_tachycardic_judge(age, heart_rate, expect):
    from hrss_server import tachycardic_judge

    answer = tachycardic_judge(age, heart_rate)
    assert answer == expect


@pytest.mark.parametrize('value_msg_list, value_judgement, in_data, '
                         'expect_out_msg, expect_status', [
                             ([], True, {"patient_id": 82, "heart_rate": 60},
                              'Patient with id 82 had a new heart rate '
                              'measurement successfully added into the heart '
                              'rate history.',
                              200),
                             ([], True, {"patient_id": '82', "heart_rate": 60},
                              'Patient with id 82 had a '
                              'new heart rate measurement successfully added '
                              'into the heart rate history.',
                              200),
                             ([], True, {"patient_id": 82, "heart_rate": '60'},
                              'Patient with id 82 had a '
                              'new heart rate measurement successfully added '
                              'into the heart rate history.',
                              200),
                             ([], True,
                              {"patient_id": '82', "heart_rate": '60'},
                              'Patient with id 82 had a new heart rate '
                              'measurement successfully added into the heart '
                              'rate history.',
                              200),
                             ([], True, {"patient_id": 82, "heart_rate": 800},
                              'E-mail sent to '
                              'DrDixonKathleen@BLH_hospital.com from '
                              'tachycardic_heart_rate@BLH_hospital.com'
                              '\nPatient with id 82 had a new heart rate '
                              'measurement successfully added into the heart '
                              'rate history.',
                              200),
                             (
                                     [], True,
                                     {"patient_id": 82, "heart_rate": '900'},
                                     'E-mail sent to '
                                     'DrDixonKathleen@BLH_hospital.com from '
                                     'tachycardic_heart_rate@BLH_hospital'
                                     '.com\nPatient with id 82 had a new '
                                     'heart rate measurement successfully '
                                     'added into the heart rate history.',
                                     200),
                             (
                                     [], True,
                                     {"patient_id": '82', "heart_rate": 1000},
                                     'E-mail sent to '
                                     'DrDixonKathleen@BLH_hospital.com from '
                                     'tachycardic_heart_rate@BLH_hospital'
                                     '.com\nPatient with id 82 had a new '
                                     'heart rate measurement successfully '
                                     'added into the heart rate history.',
                                     200),
                             ([], True,
                              {"patient_id": '82', "heart_rate": '1100'},
                              'E-mail sent to '
                              'DrDixonKathleen@BLH_hospital.com from '
                              'tachycardic_heart_rate@BLH_hospital.com'
                              '\nPatient with id 82 had a new heart rate '
                              'measurement successfully added into the heart '
                              'rate history.',
                              200),
                             (['This patient_id does not exist.'], False,
                              {"patient_id": 820,
                               "heart_rate": 1200},
                              'This patient_id does not exist.\nFix and '
                              'request again.',
                              400),
                             ([
                                  "Field \"heart_rate\" value does not match "
                                  "regex '^[1-9][0-9]*$'.",
                                  "Field "
                                  "\"patient_id\" value does not match regex "
                                  "'^[1-9][0-9]*$'."],
                              False,
                              {"patient_id": 'l82', "heart_rate": '6p0'},
                              "Field \"heart_rate\" value does not match "
                              "regex '^[1-9][0-9]*$'.\nField \"patient_id\" "
                              "value does not match regex '^[1-9]["
                              "0-9]*$'.\nFix and request again.", 400),
                             ([
                                  "Field \"heart_rate\" value does not match "
                                  "regex '^[1-9][0-9]*$'."],
                              False,
                              {"patient_id": '82', "heart_rate": '6p0'},
                              "Field \"heart_rate\" value does not match "
                              "regex '^[1-9][0-9]*$'.\nFix and request again.",
                              400),
                             (["Field "
                               "\"patient_id\" value does not match regex "
                               "'^[1-9][0-9]*$'."],
                              False,
                              {"patient_id": 'l82', "heart_rate": '60'},
                              "Field \"patient_id\" "
                              "value does not match regex '^[1-9]["
                              "0-9]*$'.\nFix and request again.", 400)

                         ])
def test_post_heart_rate_worker(value_msg_list, value_judgement, in_data,
                                expect_out_msg, expect_status):
    from hrss_server import post_heart_rate_worker, patient_db
    global patient_db
    out_msg, status = post_heart_rate_worker(value_msg_list,
                                             value_judgement, in_data,
                                             test_mode=True)

    assert out_msg == expect_out_msg
    assert status == expect_status


@pytest.mark.parametrize('value_msg_list, value_judgement, in_data, '
                         'expect_log', [
                             ([], True, {"patient_id": 82, "heart_rate": 151},
                              ('root', 'WARNING',
                               'Patient with id 82 has a tachycardic heart '
                               'rate as 151 bpm. An email has been sent to '
                               'corresponding physician at '
                               'DrDixonKathleen@BLH_hospital.com')),
                             (
                                     [], True,
                                     {"patient_id": 82, "heart_rate": '151'},
                                     ('root', 'WARNING',
                                      'Patient with id 82 has a tachycardic '
                                      'heart '
                                      'rate as 151 bpm. An email has been '
                                      'sent to '
                                      'corresponding physician at '
                                      'DrDixonKathleen@BLH_hospital.com')),
                             (
                                     [], True,
                                     {"patient_id": '82', "heart_rate": 151},
                                     ('root', 'WARNING',
                                      'Patient with id 82 has a tachycardic '
                                      'heart '
                                      'rate as 151 bpm. An email has been '
                                      'sent to '
                                      'corresponding physician at '
                                      'DrDixonKathleen@BLH_hospital.com')),
                             ([], True,
                              {"patient_id": '82', "heart_rate": '151'},
                              ('root', 'WARNING',
                               'Patient with id 82 has a tachycardic heart '
                               'rate as 151 bpm. An email has been sent to '
                               'corresponding physician at '
                               'DrDixonKathleen@BLH_hospital.com'))

                         ])
def test_log_post_heart_rate_worker(value_msg_list, value_judgement,
                                    in_data, expect_log):
    from hrss_server import post_heart_rate_worker, patient_db
    with LogCapture() as log_c:
        post_heart_rate_worker(value_msg_list, value_judgement,
                               in_data, test_mode=True)

    log_c.check(expect_log)


@pytest.mark.parametrize('value_msg_list, value_judgement, in_data', [
    ([], True, {"patient_id": 82, "heart_rate": 70}),
    ([], True, {"patient_id": '82', "heart_rate": 70}),
    ([], True, {"patient_id": 82, "heart_rate": '70'}),
    ([], True, {"patient_id": '82', "heart_rate": '70'}),

])
def test_no_log_post_heart_rate_worker(value_msg_list, value_judgement,
                                       in_data):
    from hrss_server import post_heart_rate_worker, patient_db
    with LogCapture() as log_c:
        post_heart_rate_worker(value_msg_list, value_judgement,
                               in_data, test_mode=True)

    log_c.check()


@pytest.mark.parametrize('patient_id, expect_judgement, expect_type_msg_list',
                         [
                             (62, True, []),
                             ('62', True, []),
                             ('k62', False,
                              ["The patient_id's data format is wrong."]),
                             ('6k2', False,
                              ["The patient_id's data format is wrong."]),
                             ('62k', False,
                              ["The patient_id's data format is wrong."]),
                             ('li', False,
                              ["The patient_id's data format is wrong."]),
                             (1000, True, [])
                         ])
def test_patient_id_type_validate(patient_id, expect_judgement,
                                  expect_type_msg_list):
    from hrss_server import patient_id_type_validate
    judgement, type_msg_list = patient_id_type_validate(patient_id)
    assert judgement == expect_judgement
    assert type_msg_list == expect_type_msg_list


@pytest.mark.parametrize('patient_id, expect_judgement, '
                         'expect_value_msg_list', [
                             (62, True, []),
                             ('62', True, []),
                             (10000, False, [
                                 'This patient_id does not exist.']),
                             ('10000', False, [
                                 'This patient_id does not exist.']),
                             ('k62', False,
                              ["The patient_id's data format is wrong."]),
                             ('6k2', False,
                              ["The patient_id's data format is wrong."]),
                             ('62k', False,
                              ["The patient_id's data format is wrong."]),
                             ('li', False,
                              ["The patient_id's data format is wrong."])

                         ])
def test_patient_id_value_validate(patient_id, expect_judgement,
                                   expect_value_msg_list):
    from hrss_server import patient_id_value_validate
    judgment, value_msg_list = patient_id_value_validate(patient_id)

    assert judgment == expect_judgement
    assert value_msg_list == expect_value_msg_list


@pytest.mark.parametrize('value_msg_list, value_judgement, patient_id, '
                         'expect_out, expect_status', [
                             ([], True, 62,
                              {"heart_rate": 67, "status": "not tachycardic",
                               "timestamp": "2020-06-15 12:06:15"}, 200),
                             ([], True, '62',
                              {"heart_rate": 67, "status": "not tachycardic",
                               "timestamp": "2020-06-15 12:06:15"}, 200),
                             ([], True, 82,
                              {"heart_rate": 111, "status": "tachycardic",
                               "timestamp": "2019-07-25 12:35:24"}, 200),
                             ([], True, '82',
                              {"heart_rate": 111, "status": "tachycardic",
                               "timestamp": "2019-07-25 12:35:24"}, 200),
                             ([
                                  'This patient_id does not exist in the '
                                  'patient database.'],
                              False, 1000,
                              'This patient_id does not exist in the patient '
                              'database.\nFix and request again.',
                              400),
                             ([
                                  'This patient_id does not exist in the '
                                  'patient database.'],
                              False, '1000',
                              'This patient_id does not exist in the patient '
                              'database.\nFix and '
                              'request again.',
                              400),
                             (
                                     [
                                         "The patient_id's data format is "
                                         "wrong."],
                                     False,
                                     'k62',
                                     "The patient_id's data format is "
                                     "wrong.\nFix and request again.",
                                     400),
                             (
                                     [
                                         "The patient_id's data format is "
                                         "wrong."],
                                     False,
                                     '6k2', "The patient_id's "
                                            "data format is wrong.\nFix and "
                                            "request again.",
                                     400),
                             (
                                     [
                                         "The patient_id's data format is "
                                         "wrong."],
                                     False,
                                     '62k', "The patient_id's "
                                            "data format is wrong.\nFix and "
                                            "request again.",
                                     400)
                         ])
def test_get_patient_status_worker(value_msg_list, value_judgement, patient_id,
                                   expect_out, expect_status):
    from hrss_server import get_patient_status_worker
    out, status = get_patient_status_worker(value_msg_list, value_judgement,
                                            patient_id)
    assert out == expect_out
    assert status == expect_status


@pytest.mark.parametrize('in_data, patient_value_msg_list,'
                         'patient_value_judgement,'
                         'patient_status_value_msg_lis, '
                         'patient_status_value_judgement, patient_id, '
                         'expect_out, expect_status',
                         [
                             ({"patient_id": 820,
                               "attending_username": 'Banks.J',
                               "patient_age": 25}, [], True,
                              ['This patient has no heart rate '
                               'history yet.'], False, 820,
                              "This patient has no "
                              "heart rate history yet.\nFix and request "
                              "again.",
                              400),
                             ({"patient_id": '820',
                               "attending_username": 'Banks.J',
                               "patient_age": 25}, [], True,
                              ['This patient has no heart rate '
                               'history yet.'], False, 820,
                              "This patient has no "
                              "heart rate history yet.\nFix and request "
                              "again.",
                              400),
                             ({"patient_id": 820,
                               "attending_username": 'Banks.J',
                               "patient_age": '25'}, [], True,
                              ['This patient has no heart rate '
                               'history yet.'], False, 820,
                              "This patient has no "
                              "heart rate history yet.\nFix and request "
                              "again.",
                              400),
                             ({"patient_id": '820',
                               "attending_username": 'Banks.J',
                               "patient_age": '25'}, [], True,
                              ['This patient has no heart rate '
                               'history yet.'], False, 820,
                              "This patient has no "
                              "heart rate history yet.\nFix and request "
                              "again.",
                              400)
                         ])
def test_no_history_get_patient_status_worker(in_data, patient_value_msg_list,
                                              patient_value_judgement,
                                              patient_status_value_msg_lis,
                                              patient_status_value_judgement,
                                              patient_id, expect_out,
                                              expect_status):
    from hrss_server import \
        post_new_patient_worker, get_patient_status_worker, \
        patient_db
    global patient_db

    post_new_patient_worker(patient_value_msg_list,
                            patient_value_judgement, in_data,
                            test_mode=True)

    out_msg, status = get_patient_status_worker(patient_status_value_msg_lis,
                                                patient_status_value_judgement,
                                                patient_id)

    assert out_msg == expect_out
    assert status == expect_status


@pytest.mark.parametrize('value_msg_list, value_judgement,patient_id, '
                         'expect_out_msg, expect_status', [
                             ([], True, 62,
                              [112, 84, 83, 114, 73, 90, 80, 71, 104, 97, 101,
                               93, 91, 75, 88, 78, 74,
                               67], 200),
                             ([], True, '62',
                              [112, 84, 83, 114, 73, 90, 80, 71, 104, 97, 101,
                               93, 91, 75, 88, 78, 74, 67],
                              200),
                             ([], True, 82, [88, 74, 114, 111], 200),
                             ([], True, '82', [88, 74, 114, 111], 200),
                             (
                                     [
                                         "The patient_id's data format is "
                                         "wrong."],
                                     False,
                                     'l82',
                                     "The patient_id's data format is "
                                     "wrong.\nFix "
                                     "and request again.",
                                     400),
                             (
                                     [
                                         "The patient_id's data format is "
                                         "wrong."],
                                     False,
                                     '8l2',
                                     "The patient_id's data format is "
                                     "wrong.\nFix "
                                     "and request again.",
                                     400),
                             (
                                     [
                                         "The patient_id's data format is "
                                         "wrong."],
                                     False,
                                     '82l',
                                     "The patient_id's data format is "
                                     "wrong.\nFix "
                                     "and request again.",
                                     400),
                             ([
                                  'This patient_id does not exist in the '
                                  'patient database.'],
                              False, 820,
                              "This patient_id does not exist in the patient "
                              "database.\nFix and request again.", 400),
                         ])
def test_get_heart_rate_list_worker(value_msg_list, value_judgement,
                                    patient_id, expect_out_msg, expect_status):
    from hrss_server import get_heart_rate_list_worker

    out_msg, status = get_heart_rate_list_worker(value_msg_list,
                                                 value_judgement, patient_id)

    assert out_msg == expect_out_msg
    assert status == expect_status


@pytest.mark.parametrize('in_data, patient_value_msg_list, '
                         'patient_value_judgement, '
                         'heart_list_value_msg_list, '
                         'heart_list_value_judgement,'
                         'patient_id, expect_out_msg, expect_status', [
                             ({"patient_id": 820,
                               "attending_username": 'Banks.J',
                               "patient_age": 25}, [], True,
                              ['This patient has no heart rate '
                               'history yet.'], False, 820,
                              "This patient has no "
                              "heart rate history yet.\nFix and request "
                              "again.",
                              400),
                             ({"patient_id": '820',
                               "attending_username": 'Banks.J',
                               "patient_age": 25}, [], True,
                              ['This patient has no heart rate '
                               'history yet.'], False, 820,
                              "This patient has no "
                              "heart rate history yet.\nFix and request "
                              "again.",
                              400),
                             ({"patient_id": 820,
                               "attending_username": 'Banks.J',
                               "patient_age": '25'}, [], True,
                              ['This patient has no heart rate '
                               'history yet.'], False, 820,
                              "This patient has no "
                              "heart rate history yet.\nFix and request "
                              "again.",
                              400),
                             ({"patient_id": '820',
                               "attending_username": 'Banks.J',
                               "patient_age": '25'}, [], True,
                              ['This patient has no heart rate '
                               'history yet.'], False, 820,
                              "This patient has no "
                              "heart rate history yet.\nFix and request "
                              "again.",
                              400)
                         ])
def test_no_history_get_heart_rate_list_worker(in_data, patient_value_msg_list,
                                               patient_value_judgement,
                                               heart_list_value_msg_list,
                                               heart_list_value_judgement,
                                               patient_id, expect_out_msg,
                                               expect_status):
    from hrss_server import \
        post_new_patient_worker, get_heart_rate_list_worker, \
        patient_db

    global patient_db

    post_new_patient_worker(patient_value_msg_list,
                            patient_value_judgement, in_data,
                            test_mode=True)

    out_msg, status = get_heart_rate_list_worker(heart_list_value_msg_list,
                                                 heart_list_value_judgement,
                                                 patient_id)

    assert out_msg == expect_out_msg
    assert status == expect_status


# **************************Junqi Lu ends**************************

# **************************Ramana Balla starts**************************


@pytest.mark.parametrize('in_data, expect_judgement, expect_msg_list', [
    ({"attending_username": 'Rasks.J',
      "attending_email": 'asdadsdsa@hsa.com',
      "attending_phone": '1212-1231'}, True, []),
    ({"attending_username": 123,
      "attending_email": 'sada',
      "attending_phone": 12313}, False,
     ['Field "attending_phone" must be'
      ' of [\'string\'] type.', 'Field "attending_username" must'
                                ' be of string type.'])
])
def test_new_attending_type_validate(in_data, expect_judgement,
                                     expect_msg_list):
    from hrss_server import new_attending_type_validate
    judgement, type_msg_list = new_attending_type_validate(in_data)

    assert judgement == expect_judgement
    assert type_msg_list == expect_msg_list


@pytest.mark.parametrize('hr_list, exp_avg', [
    ([11, 12, 13, 1999], 508.75),
    ([110, 111, 1231, 231], 420.75)
])
def test_avg_hr_since(hr_list, exp_avg):
    from hrss_server import avg_hr_since
    avg = avg_hr_since(hr_list)

    assert avg == exp_avg


@pytest.mark.parametrize('in_data, exp_jud, exp_list', [
    ({"patient_id": 1233,
      "heart_rate_average_since": '2016-12-31 11:11:11'},
     True, []),
    ({"patient_id": '1233',
      "heart_rate_average_since": '2016-12-31 11:11:11'},
     True, []),
    ({"patient_id": '1233',
      "heart_rate_average_since": '2016:12-31 11:11:11'},
     False, ['Field "heart_rate_average_since" '
             'field \'heart_rate_average_since\' cannot'
             ' be coerced: time data \'2016:12-31 11:11:11\' '
             'does not match '
             'format \'%Y-%m-%d %H:%M:%S\'.'])
])
def test_hr_interval_type_validate(in_data, exp_jud, exp_list):
    from hrss_server import hr_interval_type_validate

    jud, list = hr_interval_type_validate(in_data)

    assert jud == exp_jud
    assert list == exp_list
    from hrss_server import hr_interval_type_validate

    jud, list = hr_interval_type_validate(in_data)

    assert jud == exp_jud
    assert list == exp_list


# **************************Ramana Balla ends**************************

# **************************Ziwei He starts**************************


@pytest.mark.parametrize("in_data, expect_msg, expect_status", [
    ([['admin_username', 's'], ['admin_password', 'd']], "Wrong input data "
                                                         "type", 400),
    ({"admin_username": 's', "admin_password": "bla", "bla": "b"},
     "Wrong input dictionary", 400),
    ({"admin_username": 's'}, "Wrong input dictionary", 400),
    ({'admin_usr': 'a', 'admin_password': 1}, "Wrong key name", 400),
    ({'admin_username': 'a', 'adminpassword': 'a'}, "Wrong key name", 400),
    ({'admin_usr': 'a', 'admin_pasword': 'a'}, "Wrong key name", 400),
    ({'admin_username': 12, 'admin_password': 'as'}, "The username or password"
                                                     " must be strings", 400),
    ({'admin_username': '12', 'admin_password': []}, "The username or password"
                                                     " must be strings", 400),
    ({'admin_username': 12, 'admin_password': []}, "The username or password"
     + " must be strings", 400),
    ({'admin_username': "DavidH", "admin_password": '123'}, "Username is "
                                                            "already in use",
     400),
    ({'admin_username': "", "admin_password": '123'}, "Username can not be "
                                                      "empty", 400),
    ({'admin_username': "  ", "admin_password": '123'}, "Username can not be"
                                                        " empty", 400),
    ({'admin_username': " a ", "admin_password": '1234567'}, "Password should"
                                                             " have at least "
                                                             "8 characters",
     400),
    ({'admin_username': " a ", "admin_password": '12345 67'}, "Password should"
                                                              " contain at "
                                                              "least one "
                                                              "letter and "
                                                              "one number "
                                                              "without spaces",
     400)
])
def test_check_admin_register_exception(in_data, expect_msg, expect_status):
    from hrss_server import check_admin_register
    test = pd.read_csv('dummy_data/admin_data.csv')
    msg, status, _ = check_admin_register(in_data, test)
    assert msg == expect_msg
    assert status == expect_status


def test_check_admin_register_normal():
    from hrss_server import check_admin_register
    db = pd.DataFrame({
        'admin_username': ['DavidH', 'JunqiL', 'RamanaB', 'admin 1'],
        'admin_password': ['davidhe1998', 'JunqiL01', 'RamanaB2', 'asdfgh12']
    })
    in_data = {'admin_password': 'asdfgh12', 'admin_username': 'admin 1'}
    test = pd.read_csv('dummy_data/admin_data.csv')
    msg, status, test = check_admin_register(in_data, test)
    assert msg == "Successfully added new administrator information"
    assert status == 200
    pd.testing.assert_frame_equal(test, db)


@pytest.mark.parametrize("pwd, expect", [
    ("1234ad7", "Password should have at least 8 characters"),
    ("        ", "Password should contain at least one letter and one "
                 "number without spaces"),
    ("asdFfghjy", "Password should contain at least one letter and one "
                  "number without spaces"),
    ("123456789", "Password should contain at least one letter and one "
                  "number without spaces"),
    ("/,.;'-+a", "Password should contain at least one letter and one "
                 "number without spaces"),
    ("2@#$%^&*", "Password should contain at least one letter and one "
                 "number without spaces"),
    ("aSd12234 ", "Password should contain at least one letter and one "
                  "number without spaces"),
    ("as12eRf g", "Password should contain at least one letter and one "
                  "number without spaces"),
    ("zxCv1234", 'pass'),
    ("asdFghj2", 'pass'),
    ("4567893w", 'pass')
])
def test_check_pwd(pwd, expect):
    from hrss_server import check_pwd
    assert check_pwd(pwd) == expect


@pytest.mark.parametrize("in_admin, expect_flag", [
    ({'admin_usr': 'a', 'admin_password': 1}, "Wrong key name"),
    ({'admin_username': 'a', 'adminpassword': 'a'}, "Wrong key name"),
    ({'admin_usr': 'a', 'admin_pasword': 'a'}, "Wrong key name"),
    ({'admin_username': 32, 'admin_password': 'as'}, "The username or password"
                                                     " must be strings"),
    ({'admin_username': '12', 'admin_password': []}, "The username or password"
                                                     " must be strings"),
    ({'admin_username': 16, 'admin_password': {}}, "The username or password"
     + " must be strings"),
    ({'admin_username': "DavidH", "admin_password": '123'}, "Wrong password"),
    ({'admin_username': "", "admin_password": '123'}, "Invalid username"),
    ({'admin_username': "Davih", "admin_password": '1234567'}, "Invalid "
                                                               "username"),
    ({'admin_username': "JunqiL", "admin_password": 'junqiL01'}, "Wrong "
                                                                 "password"),
    ({'admin_username': "JunqiL", "admin_password": 'JunqiL01'}, "pass"),
    ({'admin_username': "RamanaB", "admin_password": 'RamanaB2'}, "pass")
])
def test_check_admin(in_admin, expect_flag):
    from hrss_server import check_admin
    admin = pd.read_csv('dummy_data/admin_data.csv')
    result = check_admin(in_admin, admin)
    assert result == expect_flag


@pytest.mark.parametrize("in_admin, expect_flag", [
    ([['admin_username', 's'], ['admin_password', 'd']], "No registered "
                                                         "administrator in "
                                                         "the database, "
                                                         "please register "
                                                         "first"),
    ({'admin_usr': 'a', 'admin_password': 1}, "No registered "
                                              "administrator in the "
                                              "database, please register "
                                              "first"),
    ({'admin_username': "JunqiL", "admin_password": 'JunqiL01'},
     "No registered administrator in the database, please register first")
])
def test_check_admin_empty(in_admin, expect_flag):
    from hrss_server import check_admin
    admin_db = pd.DataFrame(columns=['admin_username', 'admin_password'])
    result = check_admin(in_admin, admin_db)
    assert result == expect_flag


@pytest.mark.parametrize("in_admin, expect_info, expect_code", [
    ([['admin_username', 's'], ['admin_password', 'd']], "Wrong input data "
                                                         "type", 400),
    ({"admin_username": 's', "admin_password": "bla", "bla": "b"},
     "Wrong input dictionary",
     400),
    ({"admin_username": 's'}, "Wrong input dictionary", 400),
    ({'admin_username': 'a', 'adminpassword': 'a'}, "Wrong key name", 400),
    ({'admin_username': 32, 'admin_password': 'as'}, "The username or password"
                                                     " must be strings", 400),
    ({'admin_username': "Davih", "admin_password": '1234567'}, "Invalid "
                                                               "username",
     401),
    ({'admin_username': "RamanaB", "admin_password": 'junqiL01'}, "Wrong "
                                                                  "password",
     401),
    ({'admin_username': "JunqiL", "admin_password": 'JunqiL01'}, [
        {"attending_username": "Banks.J",
         "attending_email": "DrBanksJohn@BLH_hospital.com",
         "attending_phone": "228-677-1325"},
        {"attending_username": "Bowen.K",
         "attending_email": "DrBowenKaren@BLH_hospital.com",
         "attending_phone": "720-473-9173"},
        {"attending_username": "Chapman.R",
         "attending_email": "DrChapmanRhonda@BLH_hospital.com",
         "attending_phone": "513-950-5371"}], 200)
])
def test_attending_process(in_admin, expect_info, expect_code):
    from hrss_server import attending_process
    admin = pd.read_csv('dummy_data/admin_data.csv')
    physician = pd.read_csv('dummy_data/physicians_data.csv', nrows=3)
    info, status = attending_process(in_admin, physician, admin)
    assert info == expect_info
    assert status == expect_code


def test_attending_process_empty():
    from hrss_server import attending_process
    admin = pd.read_csv('dummy_data/admin_data.csv')
    admin_empty = pd.DataFrame(columns=['admin_username', 'admin_password'])
    physician = pd.DataFrame(
        columns=['attending_username', 'attending_email', 'attending_phone'])
    in_admin = {'admin_username': "JunqiL", "admin_password": 'JunqiL01'}
    info1, status1 = attending_process(in_admin, physician, admin)
    info2, status2 = attending_process(in_admin, physician, admin_empty)
    assert info1 == "No physician information found"
    assert status1 == 400
    assert info2 == "No registered administrator in the database, please " + \
           "register first"
    assert status2 == 400


@pytest.mark.parametrize("in_admin, expect_info, expect_code", [
    ([['admin_username', 's'], ['admin_password', 'd']], "Wrong input data "
                                                         "type", 400),
    ({"admin_username": 's', "admin_password": "bla", "bla": "b"},
     "Wrong input dictionary",
     400),
    ({"admin_username": 's'}, "Wrong input dictionary", 400),
    ({'admin_username': 'a', 'adminpassword': 'a'}, "Wrong key name", 400),
    ({'admin_username': 32, 'admin_password': 'as'}, "The username or password"
                                                     " must be strings", 400),
    ({'admin_username': "Davih", "admin_password": '1234567'}, "Invalid "
                                                               "username",
     401),
    ({'admin_username': "RamanaB", "admin_password": 'junqiL01'}, "Wrong "
                                                                  "password",
     401),
    ({'admin_username': "RamanaB", "admin_password": 'RamanaB2'}, [
        {"patient_id": 2,
         "attending_username": "Dixon.K",
         "patient_age": 54},
        {"patient_id": 3,
         "attending_username": "Bowen.K",
         "patient_age": 32},
        {"patient_id": 8,
         "attending_username": "Cline.A",
         "patient_age": 56}], 200)
])
def test_patient_process(in_admin, expect_info, expect_code):
    from hrss_server import patient_process
    admin = pd.read_csv('dummy_data/admin_data.csv')
    patient = pd.read_csv('dummy_data/patients_clean_data.csv', nrows=3)
    patient = patient.astype(
        {'patient_id': int,
         'attending_username': str,
         'patient_age': int}).astype(object)  # Convert the data types in
    # these 3 columns accordingly
    patient['heart_rate_history'] = patient['heart_rate_history'].apply(
        literal_eval)
    info, status = patient_process(in_admin, admin, patient)
    assert info == expect_info
    assert status == expect_code


def test_patient_process_empty():
    from hrss_server import patient_process
    admin = pd.read_csv('dummy_data/admin_data.csv')
    admin_empty = pd.DataFrame(columns=['admin_username', 'admin_password'])
    patient = pd.DataFrame(
        columns=['patient_id', 'attending_username', 'patient_age',
                 'heart_rate_history'])
    in_admin = {'admin_username': "RamanaB", "admin_password": 'RamanaB2'}
    info1, status1 = patient_process(in_admin, admin, patient)
    info2, status2 = patient_process(in_admin, admin_empty, patient)
    assert info1 == "No patient information found"
    assert status2 == 400
    assert info2 == "No registered administrator in the database, please " + \
           "register first"
    assert status2 == 400


@pytest.mark.parametrize("in_admin, expect_info, expect_code", [
    ([['admin_username', 's'], ['admin_password', 'd']], "Wrong input data " +
     "type", 400),
    ({"admin_username": 's', "admin_password": "bla",
      "since_time": "2016-01-01", "bla": "b"}, "Wrong input dictionary", 400),
    ({"admin_username": 's'}, "Wrong input dictionary", 400),
    ({'admin_username': 32, 'admin_password': 'as'}, "Wrong input dictionary",
     400),
    ({'admin_username': 32, 'admin_password': 'as', "since_time": ''},
     "The username or password must be strings",
     400),
    ({'admin_username': 'a', 'adminpassword': 'a', "since_time": ''},
     "Wrong key name", 400),
    ({'admin_username': 'a', 'admin_password': 'a',
      "since_time": '2016-01-01'}, "Invalid username", 401),
    ({'admin_username': 'DavidH', 'admin_password': 'a',
      "since_time": '2016-01-01'}, "Wrong password", 401),
    ({'admin_username': "RamanaB", "admin_password": 'RamanaB2', "sincetime":
        ''}, "Please provide a time point", 400),
    ({'admin_username': "DavidH", "admin_password": 'davidhe1998',
      "since_time": '20120102'}, "The time point should be in the format "
                                 "of 'yyyy-mm-dd hh:mm:ss', 'hh:mm:ss' is "
                                 "optional",
     400),
    ({'admin_username': "DavidH", "admin_password": 'davidhe1998',
      "since_time": 20120203}, "The time point should be in the format "
                               "of 'yyyy-mm-dd hh:mm:ss', 'hh:mm:ss' is "
                               "optional",
     400)
])
def test_tachycardia_process_exception(in_admin, expect_info, expect_code):
    from hrss_server import tachycardia_process
    admin = pd.read_csv('dummy_data/admin_data.csv')
    info, status = tachycardia_process(in_admin, None, None, admin)
    assert info == expect_info


def test_tachycardia_process_normal():
    from hrss_server import tachycardia_process
    test_db = pd.read_csv('dummy_data/patients_clean_data.csv', nrows=2)
    extra = pd.DataFrame(
        {"patient_id": [4, 5, 6],
         "attending_username": ["Patel.R", "Patel.R", "Patel.R"],
         "patient_age": [1, 3, 7],
         "heart_rate_history": ['{"2016-10-28 10:10:10": 152,'
                                '"2017-10-28 01:01:01": 151}',
                                '{"2015-01-01 01:01:01": 138,'
                                '"2016-02-01 00:00:00": 100}',
                                '{"2016-10-28 10:10:10": 100,'
                                '"2017-10-28 01:01:01": 130}']})
    test_db = pd.concat([test_db, extra])
    test_db = test_db.astype(
        {'patient_id': int,
         'attending_username': str,
         'patient_age': int}).astype(object)
    test_db['heart_rate_history'] = test_db['heart_rate_history'].apply(
        literal_eval)
    empty = pd.DataFrame({"patient_id": 6, "attending_username": "Patel.R",
                          "patient_age": 18}, index=[0])
    test_db = pd.concat([test_db, empty], ignore_index=True)

    test_db1 = pd.read_csv('dummy_data/patients_clean_data.csv', nrows=1)
    extra1 = pd.DataFrame(
        {"patient_id": [4, 5],
         "attending_username": ["Patel.R", "Patel.R"],
         "patient_age": [8, 12],
         "heart_rate_history": ['{"2016-10-28 10:10:10": 152,'
                                '"2020-10-28 01:01:01": 130}',
                                '{"2015-01-01 01:01:01": 138,'
                                '"2021-02-01 00:00:00": 100}'
                                ]})
    test_db1 = pd.concat([test_db1, extra1], ignore_index=True)
    test_db1 = test_db1.astype(
        {'patient_id': int,
         'attending_username': str,
         'patient_age': int}).astype(object)
    test_db1['heart_rate_history'] = test_db1['heart_rate_history'].apply(
        literal_eval)
    test_db1 = pd.concat([test_db1, extra1, empty], ignore_index=True)
    physician = pd.read_csv('dummy_data/physicians_data.csv')
    admin = pd.read_csv('dummy_data/admin_data.csv')

    in_admin1 = {'admin_username': "DavidH", "admin_password": 'davidhe1998',
                 "since_time": '2016-01-01'}
    in_admin2 = {'admin_username': "DavidH", "admin_password": 'davidhe1998',
                 "since_time": '2019-03-25 23:30:29'}

    info1, status1 = tachycardia_process(in_admin1, test_db, physician, admin)
    info2, status2 = tachycardia_process(in_admin2, test_db1, physician, admin)
    assert info1 == [
        {'patient_id': 2, 'attending_username': 'Dixon.K',
         'attending_email': 'DrDixonKathleen@BLH_hospital.com',
         'tachycardia_datetime': ["2016-02-17 13:56:11", "2017-11-05 12:13:57",
                                  "2019-03-25 23:30:29"]},
        {'patient_id': 3, 'attending_username': 'Bowen.K',
         'attending_email': 'DrBowenKaren@BLH_hospital.com',
         'tachycardia_datetime': ["2016-11-13 14:26:34", "2020-01-21 22:07:34",
                                  "2020-08-11 17:27:57"]},
        {'patient_id': 4, 'attending_username': 'Patel.R',
         'attending_email': 'DrPatelRyan@BLH_hospital.com',
         'tachycardia_datetime': ["2016-10-28 10:10:10"]}
    ]
    assert info2 == []
    assert status1 == 200
    assert status2 == 200


def test_tachycardia_process_empty():
    from hrss_server import tachycardia_process
    admin = pd.read_csv('dummy_data/admin_data.csv')
    admin_empty = pd.DataFrame(columns=['admin_username', 'admin_password'])
    patient = pd.read_csv('dummy_data/patients_clean_data.csv', nrows=2)
    patient_empty = pd.DataFrame(
        columns=['patient_id', 'attending_username', 'patient_age',
                 'heart_rate_history'])
    physician = pd.DataFrame(
        columns=['attending_username', 'attending_email', 'attending_phone'])
    in_admin = {'admin_username': "DavidH", "admin_password": 'davidhe1998',
                "since_time": "2016-01-01"}
    info1, status1 = tachycardia_process(in_admin, patient_empty, physician,
                                         admin)
    info2, status2 = tachycardia_process(in_admin, patient, physician,
                                         admin_empty)
    info3, status3 = tachycardia_process(in_admin, patient, physician, admin)
    assert info1 == "No patient information found"
    assert status2 == 400
    assert info2 == "No registered administrator in the database, please " + \
           "register first"
    assert status2 == 400
    assert info3 == "No physician information found"
    assert status3 == 400


@pytest.mark.parametrize("age, bpm, expect", [
    (2, 151, False), (4, 130, False), (5, 134, True), (8, 131, True),
    (11, 130, False), (15, 119, False), (16, 100, False)])
def test_is_tachycardia(age, bpm, expect):
    from hrss_server import is_tachycardia
    result = is_tachycardia(age, bpm)
    assert result == expect
# **************************Ziwei He ends**************************
