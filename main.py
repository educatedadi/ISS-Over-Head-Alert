from datetime import datetime
import requests
import smtplib

MY_LAT = 24.047930  # My Latitude
MY_LONG = 84.069099  # My Longitude

my_email = "adisenpai101@gmail.com"
password = "ar_@12345"
receiver_mail = "rockadityaraj21@gmail.com"


def iss_in_range_of_view():
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()
    iss_current_latitude = float(iss_data["iss_position"]["latitude"])
    iss_current_longitude = float(iss_data["iss_position"]["longitude"])

    if (MY_LAT - 5) < iss_current_latitude < (MY_LAT + 5):
        if (MY_LONG - 5) < iss_current_longitude < (MY_LONG + 5):
            return True
    return False


def is_night_time():
    parameters = {
        'lat': MY_LAT,
        'lng': MY_LONG,
        'formatted': 0,
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    sunset_hour = int(data["results"]["sunset"].split('T')[1].split(':')[0])

    today = datetime.now()
    current_hour = today.hour

    if current_hour >= sunset_hour:
        print('it night time, there is possibility to see iss')
        return True

    return False


if iss_in_range_of_view() and is_night_time():
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=receiver_mail,
                            msg='Subject:Look for ISS \n\nLook up there will be ISS in few mins')
else:
    print("ISS is not in range")
