import requests

a = input("Digite o nome do artista ou música: ")
response = requests.get("https://itunes.apple.com/search?entity=song&limit=5&term=" + a)

o = response.json()

for result in o["results"]:
    print(result["trackName"])
