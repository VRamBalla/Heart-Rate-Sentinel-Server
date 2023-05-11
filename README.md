# Heart Rate Sentinel Server Assignment



## Project description 
This program is designed to build a simple centralized heart rate sentinel 
server to process the patients', physicals', and administrators' information 
and 
monitor the 
heart rate. The server was running on http://vcm-29744.vm.duke.edu:5000

## Authors: BLH team 
**Ziwei He**
* <ziwei.he974@duke.edu>
* Department of Biomedical Engineering
* Routes covered 
  * `POST /api/new_administrator` 
  * `POST /api/admin/all_attendings` 
  * `POST /api/admin/all_patients` 
  * `POST /api/admin/all_tachycardia`

**Junqi Lu**
* <junqi.lu@duke.edu>
* Department of Electrical & Computer Engineering
* Routes covered
  * `POST /api/new_patient` 
  * `POST /api/heart_rate` 
  * `GET /api/status/<patient_id>`
  * `GET /api/heart_rate/<patient_id>`

**Ramana Balla**
* <venkataramana.balla@duke.edu>
* Department of Biomedical Engineering
* Routes covered
  * `POST /api/new_attending` 
  * `GET /api/heart_rate/average/<patient_id>`
  * `POST /api/heart_rate/interval_average` 
  * `GET /apli/patients/<attending_username>`

## Database structure 
Data for this project will be saved into 3 datasets. They will be in the type of pandas DataFrame in the program. 

* physician_db (`/dummy_data/physicians_data.csv`) has 3 columns: 
    * attending_username: for each row, it contains 1 **string** in the format of `lastName.initialFirstName`
    * attending_email: for each row, it contains 1 **string** in the format of `DrLastnameFirstname@BLH_hospital.com`
    * attending_phone: for each row, it contains 1 **string** of 10 numeric digits in the format of `###-###-####`
* patient_db (`/dummy_data/patients_clean_data.csv`) has 4 columns: 
    * patient_id: for each row, it contains 1 unique **int**
    * attending_username: for each row, it contains 1 **string** in the format of `lastName.initialFirstName`
    * patient_age: for each row, it contains 1 **int** that is bigger than 1
    * heart_rate_history: for each row, it contains 1 **dictionary** whose length is at least 1. The data pairs in this dictionary follow the format below 
        * data_time (_key_): for each data pair, it is a **string** in the format of `%Y-%m-%d %H:%M:%S`
        * heart_rate (_value_): for each data pair, it is an **int**
* admin_db (`/dummy_data/admin_data.csv`) has 2 columns: 
    * admin_username: for each row, it contains 1 unique non-empty **string**
    * admin_password: for each row, it contains 1 **string** that must be 8 or more characters in length and include at least one letter and one number with no spaces 

The dummy data of the 3 datasets were generated into CSV files inside this repository and will be read into the program by init_database() into pandas DataFrame. 

## Code description and demo
Recall that the server is running on http://vcm-29744.vm.duke.edu:5000

Primarily, you should send a get request through from the simple route `/` 
to check on the server status. Once you get the message saying "Server is 
on", you can proceed to the following route requests as you need. 

The server is built to receive the following GET and POST request:
1. ```POST /api/new_attending```: This POST request receives JSON input containing
the username, email and phone of an attending. Depending on validation
which is then added to a database containing all the physicians' info.
2. ```POST /api/new_patient```: This POST request receives JSON input containing
information for a new patient entry, comprising an id, the username of the
attending, and the patient's age. If the input passes validation, it is then
added to a database containing information on all the patients.
3. ```POST /api/heart_rate```: This POST request receives JSON input containing
a patient id and a heart rate measurement of the corresponding patient. 
Following validation, this heart rate measurement is added to the heart rate
history of the corresponding patient along with a time stamp for when the 
input was sent.
4. ```GET /api/status/<patient_id>```: This GET request receives a a patient id as
input, and after validation, sends the most recent heart rate, time stamp of 
the latest heart rate and information on whether the latest heart rate was
tachycardic.
5. ```GET /api/heart_rate/patient_id```: This GET request receives a patient id
and returns all the previous heart rate measurements corresponding to the 
patient.
6. ```GET /api/heart_rate/average/<patient_id>```: This GET request receives a
patient id and returns the average heart rate of all the heart rate
measurements.
7. ```POST /api/heart_rate/interval_average```: This POST request receives a 
JSON input containing the patient id and time stamp. It returns the
average heart rate of the patient since the input time stamp.
8. ```GET /api/patients/<attending_username>```: This GET request receives
an attending username as input. It returns a list of dictionaries containing 
the id, last heart rate measurement and its time stamp, and tachycardic status
of the latest heart rate for all the patients that have the attending given
as input.
9. ```POST /api/new_administrator```: Add new administrator to this server based on the input information. The username should not be empty and the password should be at least eight characters with at least one letter and digit. No space is allowed in the password.
10. ```POST /api/admin/all_attendings```: This route allows the registered administrator to check all attending physician information (username, email, phone number) using their username and password. The information will be returned in a list of dictionary.
11. ```POST /api/admin/all_patients```: This route allows the registered administrator to check all patients' information (attending username, patient id, patient age) using their username and password. The information will be returned in a list of dictionary.
12. ```POST /api/admin/all_tachycardia ```: This route allows the registered administrator to check all patients' heart rate using their username and password and list all the time points of tachycardia. The information will be returned in a list of dictionary.

### Caveats
We used the pandas DataFrame (df) as the data structure to store all the 
data in 
database. Whenever the code needs to add a dictionary to a cell inside a 
df, it first adds the dictionary inside a list and then changes all the 
lists in that column into a dictionary. This is a less elegent way, but it 
is the only way as pandas is currently developing the feature of directly 
adding in a dictionary. To read more about this, please refer to 
https://github.com/pandas-dev/pandas/issues/17777

We have written our data type validation functions that in addition to meet 
the requirements demonstrated in the assignment, it 
* Ensures in_data from the requests are always in the type of dict.
* Sends out warnings if one or more required data fields are missing from 
  in_data.
* Allows for extra data field to exist inside in_data. As long as all the 
  required fields are in the correct format inside in_data, it'll ignore 
  the other extra fields and the requests will still be sucessful.

Our `test_hrss_server.py` has its own init_database() function call to 
initialize 
some dummy databases for use to test our functions. However, you might 
notice that init_database() function call is put inside the 
test_initialize_database(), which does not test for anything. We have 
to do this because we have test functions that are testing for cases when 
the databases are empty and thus need to be done before init_database() 
function call. Thus, we have such a function to force the order on testing. 
test_initialize_database() has "test" in its name though it doesn't test 
for anything because without "test", pytest won't run that function and 
init_database() inside will never be called. 

Our `hrss_client.py` has some sleep of 1 second between some consecutive 
requests. For example, the 3 consecutive post requests to 
route "/api/heart_rate" are separated by 2 1-sec sleep such that when 
adding the new heart_rate into the heart rate history directionary, the new 
record doesn't overwrite the previous one by using the same date-time stamp.
This also makes sense in real life since within 1 second, the machine 
shouldn't send out multiple heart rate measurements. 




## MIT license
MIT License

Copyright (c) 2022 Ziwei He, Junqi Lu, Ramana Balla

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

