artist_id_dict = {"乃木坂46": 12550, "櫻坂46": 29512, "日向坂46": 22163}
print(artist_id_dict)
domain = "https://www.uta-net.com/artist/"
artist_url_lst = []
for artist_name, artist_id in artist_id_dict.items():
    url = domain + str(artist_id) + "/"
    artist_url_lst.append([artist_name, url])
print(artist_url_lst)
