import csv
from datetime import datetime
from typing import Dict

DEFAULT_PHONE_NUM_FORMAT = "%Y-%m-%d"

PATH_TO_RESULT = "result.csv"
BIT_MASK_FOR_ENDING_DATE = 0b10
BIT_MASK_FOR_STARTING_DATE = 0b01
ERROR_MESSAGE_WHEN_DUPLICATION_OCCURS = "Something weird happen. How comes existing two records with same {}?"


# Note the time complexity of the whole program is O(2n) and space complexity is O(n)
def is_starting_date_already_exist(date_nature):
    return date_nature & BIT_MASK_FOR_STARTING_DATE != 0


def is_ending_date_already_exist(date_nature):
    return date_nature & BIT_MASK_FOR_ENDING_DATE != 0


def check_date_user_supply_valid(date_nature, is_starting_date):
    if is_starting_date:
        if is_starting_date_already_exist(date_nature):
            raise Exception(ERROR_MESSAGE_WHEN_DUPLICATION_OCCURS.format("starting date"))
        date_nature += BIT_MASK_FOR_STARTING_DATE
    if not is_starting_date:
        if is_ending_date_already_exist(date_nature):
            raise Exception(ERROR_MESSAGE_WHEN_DUPLICATION_OCCURS.format("ending date"))


class PhoneNumber:
    # fixmeX passing phone_num_format to constructor
    def __init__(self, phone_number: str, phone_num_format) -> None:
        self.phone_num_format = phone_num_format
        self.phone_number = phone_number
        # Note number of phone numbers [1; n].
        self.date_dictionary = dict()
        # Note observation: number_of_date_added_so_far is approximately equal to number_of_record_in_input_file
        # assume two of them are equal to make further calculation
        self.number_of_date_added_so_far = 0
        self.number_of_record_in_input_file = 0
        super().__init__()

    def add_record(self, record):
        activation_date = record[1]
        deactivation_date = record[2]

        if not activation_date:
            raise Exception("Strange! Activation date of {} is null. "
                            "Only deactivation date can be null."
                            "Please check the data again before running the program.".format(self.phone_number))

        activation_date = datetime.strptime(activation_date, self.phone_num_format)
        self.add_date(activation_date, True)

        if deactivation_date:
            deactivation_date = datetime.strptime(deactivation_date, self.phone_num_format)
            self.add_date(deactivation_date, False)

        self.number_of_record_in_input_file += 1

    def add_date(self, date_user_supply: datetime, is_activation_date: bool):
        # Date nature has only three possible values:
        # 0b01 (if the date is starting date),
        # 0b10 (ending date),
        # 0b11 (both)
        if not date_user_supply:
            return
        date_nature = self.date_dictionary.get(date_user_supply)

        if date_nature:
            check_date_user_supply_valid(date_nature, is_activation_date)
            if is_activation_date:
                self.date_dictionary[date_user_supply] += BIT_MASK_FOR_STARTING_DATE
            else:
                self.date_dictionary[date_user_supply] += BIT_MASK_FOR_ENDING_DATE
        else:
            if is_activation_date:
                self.date_dictionary[date_user_supply] = BIT_MASK_FOR_STARTING_DATE
            else:
                self.date_dictionary[date_user_supply] = BIT_MASK_FOR_ENDING_DATE
            self.number_of_date_added_so_far += 1

    def find_last_activation_dates(self) -> datetime:
        max_date = None
        for date, date_nature in self.date_dictionary.items():
            if date_nature == BIT_MASK_FOR_STARTING_DATE:
                if max_date and date > max_date:
                    max_date = date
                else:
                    max_date = date
        return max_date

    # def number_of_records_in_original_file(self):
    #     number_of_records = self.number_of_date_added_so_far / 2
    #     if self.number_of_date_added_so_far % 2 == 0:
    #         return number_of_records
    #     else:
    #         return math.ceil(number_of_records)


class FindLastActivationDate:

    def __init__(self, path_to_file_containing_phone_number: str, containing_header=True,
                 path_to_result: str = PATH_TO_RESULT, phone_num_format=DEFAULT_PHONE_NUM_FORMAT) -> None:
        self.phone_num_format = phone_num_format
        self.path_to_file_containing_phone_number = path_to_file_containing_phone_number
        self.containing_header = containing_header
        self.path_to_result = path_to_result
        self.phone_numbers = self.initialize_phone_numbers(path_to_file_containing_phone_number)

    def initialize_phone_numbers(self, path_to_file_containing_phone_number: str) -> Dict[str, PhoneNumber]:
        phone_numbers = dict()
        with open(path_to_file_containing_phone_number, 'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if self.containing_header:
                next(reader)
            for record in reader:
                phone_number = record[0]
                # TODOx check month format
                if not phone_numbers.get(phone_number):
                    phone_numbers[phone_number] = PhoneNumber(phone_number, self.phone_num_format)
                phone_number_object = phone_numbers[phone_number]
                # TODOx check time complexity
                # TODOx check allocate memory
                phone_number_object.add_record(record)

        return phone_numbers

    def run(self):
        with open(self.path_to_result, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["PHONE_NUMBER", "REAL_ACTIVATION_DATE"])

            # this method takes:
            # SUM(i_frst=0, i_last=number_of_phone_numbers, number_of_date_added_so_far) ~=
            # SUM(i_frst=0, i_last=number_of_phone_numbers, number_of_record_in_input_file) = n
            # Therefore, time complexity of this method is O(n)
            # TODOx checking my assumption
            for phone_number, phone_number_object in self.phone_numbers.items():
                # TODOx check time complexity of this method
                last_activation_date = phone_number_object.find_last_activation_dates()
                writer.writerow([phone_number, last_activation_date.strftime(self.phone_num_format)])
