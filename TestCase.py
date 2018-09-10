import csv
import unittest
from pathlib import Path

from Main import FindLastActivationDate

PATH_TO_RESULT = "result.csv"

# input.csv is a testing file in which the number of records = ?, the number of phone number = ?
PATH_TO_INPUT_FILE = "input.csv"

# expected_result.csv contains the expected answer. The result return by the program should be identical to this file
PATH_TO_EXPECTED_RESULT = "expected_result.csv"

EXPECTED_NUMBER_OF_PHONE_NUMBER_INSIDE_DEFAULT_INPUT_FILE = 3


class TestFindLastActivationDate(unittest.TestCase):

    def __init__(self, methodName='runTest',
                 path_to_result=PATH_TO_RESULT,
                 path_to_input_file=PATH_TO_INPUT_FILE,
                 path_to_expected_result=PATH_TO_EXPECTED_RESULT,
                 expected_number_of_phone_number=EXPECTED_NUMBER_OF_PHONE_NUMBER_INSIDE_DEFAULT_INPUT_FILE,
                 contain_header=True):
        """

        :param methodName: as defined in Python docs
        :param path_to_result: the name of the output file the test program would generate
        :param path_to_input_file: self-explanatory
        :param path_to_expected_result: self-explanatory
        :param expected_number_of_phone_number: the expected number of phone numbers inside the input file. For example,
        the default input file contains three phone numbers in total. Therefore, 3 is passed to the program.
        """
        super().__init__(methodName)
        self.contain_header = contain_header
        self.expected_number_of_phone_number = expected_number_of_phone_number
        self.path_to_expected_result = path_to_expected_result
        self.path_to_input_file = path_to_input_file
        self.path_to_result = path_to_result

    def setUp(self):
        # self.expected_result = self.load_result(self.path_to_expected_result)

        self.find_last_activation_date = FindLastActivationDate(self.path_to_input_file,
                                                                path_to_result=self.path_to_result)
        # self.phone_numbers = self.find_last_activation_date.phone_numbers
        self.find_last_activation_date.run()

        # self.result = self.load_result(self.path_to_result)

    def load_result(self, path):
        with open(path, 'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if self.contain_header:
                next(reader)
            result = dict()
            for row in reader:
                phone_number = row[0]
                newest_activation_date = row[1]
                result[phone_number] = newest_activation_date
            return result

    # TODOx check if the result.csv match expected_result.csv
    def test_whole_program(self):
        """
        Testing the FindLastActivationDate.run method - the crux of the whole program. THe idea of this test case is
        to check the result file is identical to the expected_result_file
        :return: None
        """
        expected_result = self.load_result(self.path_to_expected_result)
        result = self.load_result(self.path_to_result)
        self.assertDictEqual(result, expected_result, "The result returned by the program is different from"
                                                      "the result expected.")
        # fixmeX the date print to csv is not at the correct format
        # TODOx create an input.csv and
        # TODOx test real

    # TODOx check exist result file
    def test_result_file_is_generated(self):
        result_file = Path(self.path_to_result)
        self.assertTrue(result_file.is_file(), "The program fails to create {}".format(self.path_to_result))

    # TODOx check number of key (phone number) correct
    def test_dict_phone_numbers_contain_all_numbers(self):
        """
        This test case check whether FindLastActivationDate.initialize_phone_numbers. The idea is to check whether
        FindLastActivationDate.phone_numbers dictionary object contains all the phone numbers
        :return: None
        """
        phone_numbers = self.find_last_activation_date.phone_numbers
        number_of_phone_numbers_in_dict = len(phone_numbers)
        self.assertEqual(number_of_phone_numbers_in_dict,
                         self.expected_number_of_phone_number,
                         "Input file contains {} phone "
                         "numbers but output file contains "
                         "only {}".format(self.expected_number_of_phone_number, number_of_phone_numbers_in_dict))
