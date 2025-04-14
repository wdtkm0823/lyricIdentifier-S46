import requests
from bs4 import BeautifulSoup

artist_id_dict = {"乃木坂46": 12550, "櫻坂46": 29512, "日向坂46": 22163}
domain = "https://www.uta-net.com/artist/"
artist_url_lst = []
for artist_name, artist_id in artist_id_dict.items():
    url = domain + str(artist_id) + "/"
    artist_url_lst.append([artist_name, url])


def get_song_df(artist_info):
    artist_name, artist_url = artist_info[0], artist_info[1]
    response = requests.get(artist_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        info_list = soup.find_all("tr", class_="border-bottom")
        filtered_info_list = []
        for info in info_list:
            cells = info.find_all("td", class_="sp-w-100 pt-0 pt-lg-2")
            if len(cells)>0:
                filtered_info_list.append(info)
        info_list = filtered_info_list
        print(info_list)

for artist_info in artist_url_lst:
    each_song_df = get_song_df(artist_info)
