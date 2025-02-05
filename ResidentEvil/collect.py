# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
# %%

cookies = {
        '_gid': 'GA1.2.319372371.1738773323',
        '_gat_gtag_UA_29446588_1': '1',
        '_ga': 'GA1.1.1968568849.1738773323',
        '__gads': 'ID=23d23f2710375fa2:T=1738773328:RT=1738776242:S=ALNI_MYYxZJaVZWSlaSr42ax7miU6tdwFg',
        '__gpi': 'UID=000010368326925a:T=1738773328:RT=1738776242:S=ALNI_MbJMQTzWc6tSSSsmC2KQ9yfSW7qxA',
        '__eoi': 'ID=1ff9164ccfcd632c:T=1738773328:RT=1738776242:S=AA-AfjYuexWdjUCCOOBd4cjNqDlQ',
        'FCNEC': '%5B%5B%22AKsRol-vj-KU76Ue4YqeK_M0etZW0zQzplF9C-wMc66ZXfAuYy0P60RYOxvnU545rz2mQmyrLILlO6a1IIj7qPMuBx30r3hXz8RFIGJJg8WDqG1dnSg0ajO9U7qjOQDClQ4hwSaTgMrI2q06zja24Wzv1FjT1M3UtA%3D%3D%22%5D%5D',
        '_ga_DJLCSW50SC': 'GS1.1.1738776236.2.1.1738776238.58.0.0',
        '_ga_D6NF5QC4QT': 'GS1.1.1738776236.2.1.1738776238.58.0.0',
    }

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': 'https://www.residentevildatabase.com/personagens/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

def get_content(url):

    response = requests.get(url, headers=headers, cookies=cookies)
    return response

def get_data(soup):
    div_page = soup.find("div", class_="td-page-content")
    paragrafo = div_page.find_all("p")[1]
    ems = paragrafo.find_all("em")

    data = {}
    for i in ems:
        chave, valor, *_ = i.text.split(":")
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")

    return data

def get_aparicoes(soup):
    lis = (soup.find("div", class_="td-page-content")
                .find("h4")
                .find_next()
                .find_all("li"))

    aparicoes = [i.text for i in lis]
    return aparicoes

# %%

def get_personagem_infos(url):
    response = get_content(url)

    if response.status_code != 200:
        print("Erro ao acessar a página")
        return{}
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        data = get_data(soup)
        data["aparicoes"] = get_aparicoes(soup)
        return data
# %%

def get_links():
    url = "https://www.residentevildatabase.com/personagens/"
    response = requests.get(url, headers=headers, cookies=cookies)
    soup_personagens = BeautifulSoup(response.text, "html.parser")
    ancoras = (soup_personagens.find("div", class_="td-page-content")
                                .find_all("a"))


    links = [i["href"] for i in ancoras]
    return links
# %%

links = get_links()
data = []
for i in tqdm(links):
    d = get_personagem_infos(i)
    d["link"] = i
    nome = i.strip("/").split("/")[-1].replace("-", " ").title()
    d["Some"] = nome
    data.append(d)
# %%
df = pd.DataFrame(data)
df.to_csv("personagens.csv", index=False)
df.to_parquet('personagens.parquet', index=False)
df.to_pickle('personagens.pkl')
# %%
