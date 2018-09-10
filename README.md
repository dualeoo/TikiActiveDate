# Find newest phone activation date

## Overview

### 1. The data is transformed into a dictionary (FindLastActivationDate.phone_numbers)

The key of the dictionary is the phone number, the value is a Phone number object. 
The core of the PhoneNumber object is PhoneNumber.date_dictionary. 
The key of this dictionary is a distinct date and the value can either of these three values:

- 0b01 (if the date only appear as activation date) 
- 0b10 (if the date only appear as deactivation date),
- 0b11 (if both) 

### 2. For each phone number, find the newest activation date (PhoneNumber.find_last_activation_date)

We now look at PhoneNumber.date_dictionary of each phone number. 
For each date in PhoneNumber.date_dictionary, we look for the date with corresponding value =  0b01. Why?
Obviously we don't care about deactivation date so we don't care those with 0b10. 
Those with value of 0b11 represents transition from prepaid to postpaid or vice versa.
Therefore, 0b01 is what we are interested.
