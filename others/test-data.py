import urllib.request, json

with urllib.request.urlopen("http://192.168.1.12:3000?9991354") as url:
    data = json.loads(url.read().decode())
    print(data)
