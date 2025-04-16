import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os

base_dir = os.path.dirname(__file__)
main_dir = os.path.join(base_dir, "LYLICS")

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
            if len(cells) > 0:
                filtered_info_list.append(info)
        info_list = filtered_info_list
    song_name_list = []
    lyric_list = []
    lyric_staff_list = []

    # 曲ごとに情報を取得
    for info in info_list:
        # 曲名取得
        song_name = info.find("span", class_="fw-bold songlist-title pb-1 pb-lg-0").text

        # 歌詞取得
        lyric = info.find(
            "span", class_="d-block d-lg-none utaidashi text-truncate"
        ).text

        # 作詞者取得
        staff_list = info.find_all("td", class_="sp-none fw-bold")
        staff_list = [
            staff.find("a") for staff in staff_list if len(staff.find_all("a")) > 0
        ]
        lyric_staff = staff_list[0].text if staff_list else "不明"

        # リストに追加
        song_name_list.append(song_name)
        lyric_list.append(lyric)
        lyric_staff_list.append(lyric_staff)
        print(
            f"artist_name: {artist_name}, song_name: {song_name}, lyric_staff: {lyric_staff}, lyric: {lyric}"
        )

        # 2秒待機
        time.sleep(2)

    # データフレーム化する
    df = pd.DataFrame(
        {
            "artist_name": artist_name,
            "song_name": song_name_list,
            "lyric_staff": lyric_staff_list,
            "lyric": lyric_list,
        }
    )

    return df


all_song_df = pd.DataFrame(columns=["artist_name", "song_name", "lyric_staff", "lyric"])
for artist_info in artist_url_lst:
    each_song_df = get_song_df(artist_info)
    all_song_df = pd.concat([all_song_df, each_song_df], axis=0, ignore_index=True)

# CSVに保存
file_path = os.path.join(main_dir, "lyric_by_artist.csv")
all_song_df.to_csv(file_path, encoding='cp932',errors="ignore")
