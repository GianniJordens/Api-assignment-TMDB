import urllib.parse
import requests
import re
from prettytable import PrettyTable

#variabelen instellen
api_token= ""

#Als je uw token in een bepaald bestand bewaard.
def read_token(api_path):
    f= open(api_path,"r")
    token = f.read()
    return token

#zoeken naar film door naam van de film in te geven
def zoek_film_naam(api_token,film_naam):
    zoek_url= "https://api.themoviedb.org/3/search/movie?"
    query_url= zoek_url + urllib.parse.urlencode({"query":film_naam})
    zoek_headers= {'authorization': 'bearer ' +api_token}
    zoek_film_json_data =requests.get(query_url,headers=zoek_headers).json()
    return zoek_film_json_data


def meerdere_resultaten(movie_query_json):
    print("Er zijn meerdere resultaten voor deze zoekopdracht gevonden.")
    teller = 1
    alle_resultaten_naam = PrettyTable(['Nummer', "Titel", "ID nummer", "Populariteit"])
    for each in movie_query_json['results']:
        alle_resultaten_naam.add_row([teller, each["title"], each["id"], each["popularity"]])
        teller += 1
    print(alle_resultaten_naam)




while True:
    # check of er een  api token is ingegeven
    if api_token == "":
        api_token_file = input('Heeft u een bestand waarin uw API Read Access Token (v4) wordt bewaard ? y/n: ')
        if api_token_file == 'y' or api_token_file == 'yes':
            api_path = input('Geef het pad naar uw API Read Access Token (v4) bestand in: ')
            api_token = read_token(api_path).rstrip()
        elif api_token_file == 'q' or api_token_file == 'quit' or api_token_file == 'exit':
            break
        else:
            api_token = input('Geef uw API Read Access Token (v4) in: ')
            if api_token == 'q' or api_token == 'quit' or api_token == 'exit':
                api_token = ""
                break
    #ingeven van filmnaam
    film_naam = input ('Geef de te zoeken filmnaam op: ')
    print ('\n')
    if film_naam == 'q' or film_naam == 'quit' or film_naam == 'exit':
        break
    #filmnamen die spaties bevatten moeten verandert worden zodat spaties in + tekens veranderen
    film_naam= re.sub(" ","+",film_naam)


    movie_query_json = zoek_film_naam(api_token,film_naam)
    resultaten=movie_query_json['total_results']
    #als er 1 of meerdere filmnamen gevonden zijn worden ze in een tabel weergegeven
    if resultaten >= 1:
        meerdere_resultaten(movie_query_json)

    else:
        print("Er zijn geen films gevonden met deze naam.")
    print("-------------------------------------------------------------------------")
