# -------------------------------------------------------
# Spotify API用の関数（検索と楽曲の絞り込み）
# -------------------------------------------------------

# Flask周り
from flask import Flask, render_template, request, jsonify, redirect, session, url_for, make_response

# Spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import base64
import requests
import time
import random

# Spotify APIを使った処理
def search_spotify(keywords, negaposi):
    token = session.get('access_token')

    # 検索
    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': 'Bearer ' + token
    }
    params = {
        'q': ' '.join(keywords),
        'type': 'track',
        'limit': 50
    }
    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()

    # 検索結果から楽曲の情報を取得
    tracks = data['tracks']['items']

    # 複数曲の楽曲IDを取得しリストに代入
    track_ids = [track['id'] for track in tracks]

    # 複数曲の情報を一括で取得することでAPIのリクエスト回数を減らせる
    audio_features_url = 'https://api.spotify.com/v1/audio-features'
    params = {
        'ids': ','.join(track_ids)  # track_idsをカンマで結合すれば一括で取得できる
    }
    audio_response = requests.get(audio_features_url, headers=headers, params=params)
    audio_data = audio_response.json()['audio_features']

    # 一度にリクエストを送りすぎないために、スリープを入れる
    time.sleep(3)  # 3秒待機

    # それぞれの内部パラメータごとで閾値よりも高いor低い曲を変数に代入（楽曲IDで管理）
    energy_songs = []
    valence_songs = []
    loudness_songs = []
    danceability_songs = []
    mode_songs = []
    tempo_songs =[]
    # instrumentalness_songs = []

    # テキストがネガティブだった場合
    if negaposi == 0:
        for i in range(len(track_ids)):
            # エネルギッシュな曲か
            if audio_data[i]['energy'] <= 0.4:
                energy_songs.append(track_ids[i])
            # 陽性の感情か
            if audio_data[i]['valence'] <= 0.4:
                valence_songs.append(track_ids[i])
            # 音が大きいか
            if audio_data[i]['loudness'] >= -60 and audio_data[i]['loudness'] <= -20:
                loudness_songs.append(track_ids[i])
            # ダンスに適しているか
            if audio_data[i]['danceability'] <= 0.4:
                danceability_songs.append(track_ids[i])
            # 主音がメジャーかマイナーか
            if audio_data[i]['mode'] == 0:
                mode_songs.append(track_ids[i])
            # テンポが速いか
            if audio_data[i]['tempo'] <= 90:
                tempo_songs.append(track_ids[i])
            # インストか
            # if audio_data[i]['instrumentalness'] >= 0.5:
            #     instrumentalness_songs.append(track_ids[i])

    # テキストがポジティブだった場合    
    else:
        for i in range(len(track_ids)):
            # エネルギッシュな曲か
            if audio_data[i]['energy'] >= 0.6:
                energy_songs.append(track_ids[i])
            # 陽性の感情か
            if audio_data[i]['valence'] >= 0.6:
                valence_songs.append(track_ids[i])
            # 音が大きいか
            if audio_data[i]['loudness'] >= -5:
                loudness_songs.append(track_ids[i])
            # ダンスに適しているか
            if audio_data[i]['danceability'] >= 0.6:
                danceability_songs.append(track_ids[i])
            # 主音がメジャーかマイナーか
            if audio_data[i]['mode'] == 1:
                mode_songs.append(track_ids[i])
            # テンポが速いか
            if audio_data[i]['tempo'] >= 120:
                tempo_songs.append(track_ids[i])

    # フィルタリングした楽曲の中から、IDごとにカウントする
    count_list = []
    # エネルギッシュな曲か
    for i in range(len(energy_songs)):
        count_list.append([energy_songs[i], 1])
    # 陽性の感情か
    for i in range(len(valence_songs)):
        state = 0    # count_listに同じ楽曲があったかを確認するようの変数
        for j in range(len(count_list)):
            if valence_songs[i] == count_list[j][0]:
                count_list[j][1] += 1
                state = 1
        if state == 0:
            count_list.append([valence_songs[i], 1])
    # 音が大きいか
    for i in range(len(loudness_songs)):
        state = 0    # count_listに同じ楽曲があったかを確認するようの変数
        for j in range(len(count_list)):
            if loudness_songs[i] == count_list[j][0]:
                count_list[j][1] += 1
                state = 1
        if state == 0:
            count_list.append([loudness_songs[i], 1])
    # ダンスに適しているか
    for i in range(len(danceability_songs)):
        state = 0    # count_listに同じ楽曲があったかを確認するようの変数
        for j in range(len(count_list)):
            if danceability_songs[i] == count_list[j][0]:
                count_list[j][1] += 1
                state = 1
        if state == 0:
            count_list.append([danceability_songs[i], 1])
    # 主音がメジャーかマイナーか
    for i in range(len(mode_songs)):
        state = 0    # count_listに同じ楽曲があったかを確認するようの変数
        for j in range(len(count_list)):
            if mode_songs[i] == count_list[j][0]:
                count_list[j][1] += 1
                state = 1
        if state == 0:
            count_list.append([mode_songs[i], 1])
    # テンポが速いか
    for i in range(len(tempo_songs)):
        state = 0    # count_listに同じ楽曲があったかを確認するようの変数
        for j in range(len(count_list)):
            if tempo_songs[i] == count_list[j][0]:
                count_list[j][1] += 1
                state = 1
        if state == 0:
            count_list.append([tempo_songs[i], 1])
    # インストか
    # if negaposi == 0:
    #     for i in range(len(instrumentalness_songs)):
    #         state = 0    # count_listに同じ楽曲があったかを確認するようの変数
    #         for j in range(len(count_list)):
    #             if instrumentalness_songs[i] == count_list[j][0]:
    #                 count_list[j][1] += 1
    #                 state = 1
    #         if state == 0:
    #             count_list.append([instrumentalness_songs[i], 1])

    print("----------------------------------------------------------------------------------------------------------------------------------------------------")
    print("楽曲ごとの合計:")
    print(count_list)

    # 最もカウントが多かったものを適した楽曲として採用する
    # 最大のカウント数をリストの中から見つける
    suitable_song = []
    suitable_song.append(count_list[0])
    for i in range(1, len(count_list)):
        if count_list[i][1] > suitable_song[0][1]:
            suitable_song = [count_list[i]]

    # print("最大カウント数: ", suitable_song[0][1])

    # 最もカウントが多かったものは複数ある可能性があるため、ランダムに再生するようにする
    suitable_songs = []
    # suitable_songs.append(suitable_song)
    for i in range(len(count_list)):
        if count_list[i][1] == suitable_song[0][1]:
            suitable_songs.append(count_list[i])
    print("最もカウントが多い曲: ", suitable_songs)
    # print(len(suitable_songs))
    ran = random.randint(0, len(suitable_songs) -1)
    print("乱数: ", ran)

    # 楽曲リンクに変換
    suitable_songs_id = suitable_songs[ran][0]
    track_link = "https://open.spotify.com/embed/track/" + suitable_songs_id + "?utm_source=generator&theme=0"

    # 楽曲情報を再度取得
    track_url = f'https://api.spotify.com/v1/tracks/{suitable_songs_id}'
    response = requests.get(track_url, headers=headers)
    data = response.json()

    audio_features_url = f'https://api.spotify.com/v1/audio-features/{suitable_songs_id}'
    audio_response = requests.get(audio_features_url, headers=headers)
    audio_data = audio_response.json()

    print("----------------------------------------------------------------------------------------------------------------------------------------------------")
    print("再生する楽曲の情報:")
    print(f"楽曲名: {data['name']}, アーティスト名: {data['artists'][0]['name']}")
    print("楽曲IDと合計", suitable_songs[ran])
    print("楽曲のリンク",track_link)
    print("内部パラメータ: ")
    pprint.pprint(audio_data)

    return track_link