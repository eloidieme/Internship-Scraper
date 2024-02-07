import requests
import json
from bs4 import BeautifulSoup
import os

from src.processor import Processor

class SocGenScraper:
    def __init__(self, locations = ['La Defense, France', 'Paris, France'], categories = ['IT (Information Technology)', 'Banking operations processing', 'Innovation / Project / Organization', 'Corporate & Investment banking'], contracts = ['Internship']) -> None:
        self.url = "https://careers.societegenerale.com/search-proxy.php"
        self.locations = locations
        self.categories = categories
        self.contracts = contracts

    def grant_credentials(self):
        headers = {
            "authority": "careers.societegenerale.com",
            "accept": "*/*",
            "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization-api": "",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "_ALGOLIA=anonymous-9643bf35-6531-488f-b26b-bd230e6e2bb4; _pcid=...",
            "origin": "https://careers.societegenerale.com",
            "pragma": "no-cache",
            "referer": "https://careers.societegenerale.com/en/search?refinementList...",
            "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "x-proxy-url": "https://sso.sgmarkets.com/sgconnect/oauth2/access_token"
        }
        data = "grant_type=client_credentials&scope=api.corpsrc-00257.v1"

        response = requests.post(self.url, headers=headers, data=data)
        access_token = response.json()['access_token']
        return access_token

    def get_job_data(self):
        payload = json.dumps({
            "profile": "ces_profile_sgcareers",
            "query": {
                "advanced": [
                    {
                        "type": "simple",
                        "name": "sourcestr6",
                        "op": "eq",
                        "value": "job"
                    },
                    {
                        "type": "multi",
                        "name": "sourcecsv1",
                        "op": "eq",
                        "values": [
                            "FRA",
                            "FRA_A20_D005_L025",
                            "FRA_A20_D001_L001"
                        ]
                    },
                    {
                        "type": "multi",
                        "name": "sourcestr8",
                        "op": "eq",
                        "values": [
                            "INTERNSHIP"
                        ]
                    }
                ],
                "skipCount": 100,
                "skipFrom": 0
            },
            "lang": "en",
            "responseType": "SearchResult"
        })
        headers = {
            'authority': 'careers.societegenerale.com',
            'accept': '*/*',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization-api': f'Bearer {self.grant_credentials()}',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'cookie': '_ALGOLIA=anonymous-9643bf35-6531-488f-b26b-bd230e6e2bb4; _pcid=%7B%22browserId%22%3A%22ls9inz7xnmhnabz0%22%2C%22_t%22%3A%22m7xxlgk3%7Cls9inz83%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbAOwAPYagDmAawBsAH1QQAnPSQAvABzSQAXyA; SOCGENCRRLB=4bb3a3d8bd3cdcd57f0839fc7df0e71e100fdd833e4711aa51021a1be836a74bdcccedf6; didomi_token=eyJ1c2VyX2lkIjoiMThkN2I2ZjItNzMyMS02ZjRhLWE0ZDQtMDk2YzZlOGJkMjUyIiwiY3JlYXRlZCI6IjIwMjQtMDItMDVUMjI6NDE6MzkuNjM1WiIsInVwZGF0ZWQiOiIyMDI0LTAyLTA1VDIyOjQxOjQxLjQ2MVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiYzpwaW5nZG9tLWtCeTRlanduIiwiYzphdGludGVybmUtY1I3UDdDM2UiLCJjOmhvdGphci1yVGpyRnBiNyIsImM6Z29vZ2xlYWR2LXh3Z2ZBZXBjIiwiYzpkb3VibGVjbGktWVRlSlBMSzYiLCJjOnlvdXR1YmUtM3hVck1XcVEiLCJjOmRyYXdicmlkZ2UtRE5Ea05wcW4iLCJjOmxpbmtlZGludy1ubUh5NHRVZCIsImM6ZmFjZWJvb2stQ0ZBVjhkNkMiLCJjOnNvY2lldGVnZS1QclY0TGFoWiJdfSwicHVycG9zZXMiOnsiZW5hYmxlZCI6WyJhZHZlcnRpc2luLWlRTmgzQTM0IiwibWVzdXJlZGEtUjdoclZWUjQiLCJ2aWRlb3JlbGEtNFE4d3RtSEYiLCJzaGFyaW5nY28tcXJiNmNSVTIiXX0sInZlcnNpb24iOjJ9; euconsent-v2=CP5gXIAP5gXIAAHABBENAmEgAPNAAAAAAAAACJQAQCJAAAAA.fmgAAAAAAAAA; pa_privacy=%22optin%22; _hjSession_921254=eyJpZCI6ImUzOTEwNTIwLTA5ZmMtNGY1Ni04M2FjLWE5MWEzYjkzMWQ3YiIsImMiOjE3MDcxNzI5MDE2MDgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _hjSessionUser_921254=eyJpZCI6IjNiMWIxNzZkLTg5NWItNWUxZC05OGQzLTZmNmE3N2VjZWIyYSIsImNyZWF0ZWQiOjE3MDcxNzI5MDE2MDgsImV4aXN0aW5nIjp0cnVlfQ==',
            'origin': 'https://careers.societegenerale.com',
            'pragma': 'no-cache',
            'referer': 'https://careers.societegenerale.com/en/search?refinementList[jobLocation][0]=FRA&refinementList[jobLocation][1]=FRA_A20_D005_L025&refinementList[jobLocation][2]=FRA_A20_D001_L001&refinementList[jobType][0]=INTERNSHIP',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'x-proxy-url': 'https://api.socgen.com/business-support/it-for-it-support/cognitive-service-knowledge/api/v1/search-profile'
        }

        response = requests.request(
            "POST", self.url, headers=headers, data=payload)

        return response

    def get_offer_data(self, offer):
        data = requests.get(offer["lien"])
        soup = BeautifulSoup(data.content, 'html.parser')
        spans = soup.find_all(name="span", attrs={"class":"text-extra-dark-gray text-small display-block font-weight-500"})
        wanted_span = list(filter(lambda tag: tag.string == 'Date de début:', spans))[0]
        starting_date = wanted_span.next_sibling.next_sibling.contents[0].string
        return {
            "id": offer["id"],
            "date": offer["date"],
            "titre": offer["titre"],
            "contrat": "Stage",
            "lien": offer["lien"],
            "lieu": offer["lieu"],
            "categorie": offer["categorie"],
            "debut": starting_date,
        }
    
    def get_relevant_data(self):
        data = self.get_job_data().json()['Result']['Docs']
        map_obj = map(lambda dic: {"id": dic["sourcestr4"],"date": dic['modified'], "titre": dic['title'], "lien": dic['resulturl'], "contrat": dic["sourcestr8"], "lieu": dic["sourcestr7"], "categorie": dic["sourcestr10"]}, data)
        return list(map_obj)
    
    def get_processed_data(self):
        data = self.get_relevant_data()
        filtered = Processor(data, self.locations, self.categories, self.contracts).get_filtered_data()
        processed = list(map(lambda offer: self.get_offer_data(offer), filtered))
        return processed
    
    def save_data(self):
        with open(os.path.join(os.pardir,'json', 'data_sg.json'), 'w') as file:
            json.dump(self.get_processed_data(), file)

class CAScraper:
    def __init__(self, locations = ['Montrouge'], categories = ['Types de métiers Crédit Agricole S.A. - Financement et Investissement', 'Types of Jobs - IT, Digital et Data'], contracts = ['Stage']) -> None:
        self.url = "https://jobs.ca-cib.com/offre-de-emploi/liste-offres.aspx"
        self.soup = None
        self.locations = locations
        self.categories = categories
        self.contracts = contracts

    def get_offer_links(self, titles=False):
        data = requests.get(self.url)
        soup = BeautifulSoup(data.content, 'html.parser')
        a_tags = soup.findAll(name="a", attrs={"class": "ts-offer-card__title-link"})
        if titles:
            return [{"lien": f'https://jobs.ca-cib.com/{str(tag["href"])}', "titre" : str(tag.string)[2:].strip(' ').lstrip(' ')[:-2]} for tag in a_tags]
        else:
            return [f'https://jobs.ca-cib.com/{str(tag["href"])}' for tag in a_tags]
    
    def get_offer_data(self, link):
        data = requests.get(link)
        soup = BeautifulSoup(data.content, 'html.parser')
        title = soup.find(name="p", attrs={"id": "fldjobdescription_jobtitle"}).string
        starting_date = soup.find(name="p", attrs={"id":"fldjobdescription_date1"})
        if starting_date is None:
            starting_date = "Non spécifié"
        else:
            starting_date = starting_date.string
        ref = soup.find(name="div", attrs={"class":"ts-offer-page__reference"}).contents[-1].strip()
        date = soup.find(name="div", attrs={"class":"ts-offer-page__maj-date"}).contents[-1].strip()
        lieu = soup.find(name="p", attrs={"id": "fldlocation_joblocation"}).string.strip()
        categorie = soup.find(name="p", attrs={"id": "fldjobdescription_primaryprofile"})
        if categorie is None:
            categorie = "Non spécifié"
        else:
            categorie = categorie.string
        contrat = soup.find(name="p", attrs={"id": "fldjobdescription_contract"}).string
        return {
            "id": ref,
            "date": date,
            "titre": title,
            "contrat": contrat,
            "lien": link,
            "lieu": lieu,
            "categorie": categorie,
            "debut": starting_date,
        }
    
    def get_relevant_data(self):
        links = self.get_offer_links()
        data = list(map(lambda link: self.get_offer_data(link), links))
        return data
    
    def get_processed_data(self):
        data = self.get_relevant_data()
        processed = Processor(data, self.locations, self.categories, self.contracts).get_filtered_data()
        return processed

    def save_data(self):
        with open(os.path.join(os.pardir,'json', 'data_ca.json'), 'w') as file:
            json.dump(self.get_processed_data(), file)
