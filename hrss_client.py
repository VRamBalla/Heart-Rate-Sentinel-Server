import requests
import time

# url = 'http://127.0.0.1:5000'  # This is the local url. Change this to the
# # actual one once the code is deployed in VM server
url = 'http://vcm-29744.vm.duke.edu:5000'  # External VM server url

# Test the server status
r = requests.get(url + "/")
print(r.status_code)
print(r.text)

# POST /api/new_attending
out_data = {
    "attending_username": 'Banks.J',
    "attending_email": 'DrBanksJohn@BLH_hospital.com',
    "attending_phone": '228-677-1325'
}
r = requests.post(url + "/api/new_attending",
                  json=out_data)
print(r.status_code)
print(r.text)

# POST /api/new_patient
out_data = {
    "patient_id": 1,
    "attending_username": 'Banks.J',
    "patient_age": 25  # in years
}
r = requests.post(url + "/api/new_patient",
                  json=out_data)
print(r.status_code)
print(r.text)

# POST /api/heart_rate
out_data = {
    "patient_id": 1,
    "heart_rate": 90  # in bpm
}
r = requests.post(url + "/api/heart_rate",
                  json=out_data)
print(r.status_code)
print(r.text)

time.sleep(1)  # Sleep for 1 sec. Sleeping between consecutive post requests
# is necessary to avoid the server code from using the same datetime stamp to
# overwrite the previous heart rate record

out_data = {
    "patient_id": 1,
    "heart_rate": 95  # in bpm
}
r = requests.post(url + "/api/heart_rate",
                  json=out_data)
print(r.status_code)
print(r.text)

time.sleep(1)

out_data = {
    "patient_id": 1,
    "heart_rate": 140  # in bpm
}
r = requests.post(url + "/api/heart_rate",
                  json=out_data)
print(r.status_code)
print(r.text)

# GET /api/status/<patient_id>
r = requests.get(url + "/api/status/1")
print(r.status_code)
print(r.text)

# GET /api/heart_rate/<patient_id>
r = requests.get(url + "/api/heart_rate/1")
print(r.status_code)
print(r.text)

# GET /api/heart_rate/average/<patient_id>
r = requests.get(url + "/api/heart_rate/average/1")
print(r.status_code)
print(r.text)

# POST /api/heart_rate/interval_average
out_data = {
    "patient_id": 1,
    "heart_rate_average_since": '2018-03-09 11:00:36'
}
r = requests.post(url + "/api/heart_rate/interval_average",
                  json=out_data)
print(r.status_code)
print(r.text)

# GET /api/patients/<attending_username>
r = requests.get(url + "/api/patients/Banks.J")
print(r.status_code)
print(r.text)

# POST /api/new_administrator
admin = {"admin_username": "RamanaB", "admin_password": "RamanaB2"}
r = requests.post(url + "/api/new_administrator",
                  json=admin)
print(r.status_code)
print(r.text)

# POST /api/admin/all_attendings
out_data = {
    "admin_username": 'RamanaB',
    "admin_password": 'RamanaB2'
}
r = requests.post(url + "/api/admin/all_attendings",
                  json=out_data)
print(r.status_code)
print(r.text)

# POST /api/admin/all_patients
out_data = {
    "admin_username": 'RamanaB',
    "admin_password": 'RamanaB2'
}
r = requests.post(url + "/api/admin/all_patients",
                  json=out_data)
print(r.status_code)
print(r.text)

# POST /api/admin/all_tachycardia

in_admin = {"admin_username": "RamanaB",
            "admin_password": "RamanaB2",
            "since_time": "2018-03-09 11:00:36"}

r1 = requests.post(url + "/api/admin/"
                         "all_tachycardia", json=in_admin)
print(r1.status_code)
print(r1.text)

# Additional tests
patient = {"patient_id": '12',
           "attending_username": "JunqiL", "patient_age": 7}
r3 = requests.post(url + "/api/new_patient",
                   json=patient)

in_admin = {"admin_username": "RamanaB", "admin_password": "RamanaB2"}
r1_b = requests.post(url + "/api/admin/"
                           "all_patients", json=in_admin)

physician = {"attending_username": "JunqiL",
             "attending_phone": "9176-838-8888",
             "attending_email": "ssr@gmail.com"}
r2 = requests.post(url + "/api/new_attending",
                   json=physician)
