# Flask周り
from flask import Flask, render_template, request, jsonify, redirect, session, url_for, make_response

# 自然言語処理
import numpy as np
import torch.nn.functional as F
import random
import glob
import torch
import pytorch_lightning as pl
from tqdm import tqdm
from torch.utils.data import DataLoader
from transformers import BertJapaneseTokenizer, BertForSequenceClassification

# Spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import base64
import requests
import time
import random

#アクセストークン取得に必要な情報
CLIENT_ID = '4abe8764fa6846ae8218beb2f9ddd3a1'
CLIENT_SECRET = '8bee0afd727b4be68a4ae8f01ea68647'
REDIRECT_URI = 'http://localhost:5001/callback'  # Spotifyに設定したリダイレクトURI
# REDIRECT_URI = 'https://stephen-federal-zoloft-muslim.trycloudflare.com/callback'  # Spotifyに設定したリダイレクトURI
# REDIRECT_URI = 'https://resolved-viable-quetzal.ngrok-free.app/callback'  # 外部公開用のリダイレクトURI

# Spotifyの認可エンドポイントとトークンエンドポイント
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

# 日本語の事前学習モデル
#MODEL_NAME = 'tohoku-nlp/bert-base-japanese-whole-word-masking'

# ファインチューニングしたモデル
MODEL_NAME = 'fine_tuned_model'

# 事前学習モデルのロード
tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
bert_sc = BertForSequenceClassification.from_pretrained(
    MODEL_NAME, num_labels=2
)

# CUDAが利用できる場合のみ.cuda()を呼び出す（MACではCUDAがサポートされていないため利用できない→CPUを使ってモデルをロード）
#bert_sc = bert_sc.cuda()


app = Flask(__name__)
app.secret_key = 'secret_key'

# ホーム画面
@app.route('/')
def home():
    return render_template('home.html')

# 戻るボタン(入力フォームへ遷移するボタン)
@app.route('/back')
def back():
    return render_template('index.html')

# ログアウト機能
@app.route('/logout')
def logout():

    # セッション内のデータを削除
    session.pop('access_token', None)
    session.pop('refresh_token', None)

    # クッキーを削除する
    response = make_response(redirect(url_for('logout_redirect')))
    response.set_cookie('access_token', '', expires=0)
    response.set_cookie('refresh_token', '', expires=0)

    # キャッシュを無効にするためのヘッダーを追加
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'

    return response

# Spotifyをログアウトした後、home.htmlへリダイレクトさせる
@app.route('/logout_redirect')
def logout_redirect():
    # SpotifyでログアウトするためのURL
    spotify_logout_url = 'https://accounts.spotify.com/logout'

    # Spotifyでログアウトした後、jsで自動的にhome.htmlへ戻す。（未実装）
    return render_template('logout.html', spotify_logout_url=spotify_logout_url)

# 認可のためのエンドポイント
@app.route('/login')
def login():
    # セッション内のデータを削除
    session.clear()

    scope = 'user-read-playback-state user-modify-playback-state'
    auth_url = f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={scope}&prompt=login"
    return redirect(auth_url)

# 認可コードを受け取り、アクセストークンを取得するエンドポイント
@app.route('/callback')
def callback():
    code = request.args.get('code')
    # 認可コードを使ってアクセストークンを取得
    auth_headers = {
        'Authorization': 'Basic ' + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    auth_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    response = requests.post(TOKEN_URL, headers=auth_headers, data=auth_data)
    token_info = response.json()

    # print("トークンが取得できたかの確認: ", token_info)

    # レスポンスに 'access_token' が含まれているか確認
    if 'access_token' in token_info:
        # アクセストークンとリフレッシュトークンをセッションに保存
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']

        #扱いやすいようにアクセストークンを変数で管理しておく(使わない可能性あり)
        # token = token_info['access_token']
        # print("token=" , token)
    else:
        # エラーメッセージを表示
        print('Error response:', token_info)
        return 'Failed to retrieve access token'

    print("アクセストークン: ", token_info['access_token'])
    
    # return render_template('index.html', access_token=session['access_token'])
    return render_template('index.html')

# アクセストークンのリフレッシュ
@app.route('/refresh_token')
def refresh_token():
    refresh_token = session.get('refresh_token')

    refresh_data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }

    response = requests.post(TOKEN_URL, data=refresh_data)
    token_info = response.json()

    session['access_token'] = token_info['access_token']
    
    return jsonify(token_info)


# 自然言語処理
def nlp(text):
    # データの符号化
    encoding = tokenizer(
        text, 
        padding='longest',
        return_tensors='pt'
    )

    # 推論 (推論時は”torch.no_grad():”の中で処理を行う。)
    with torch.no_grad():
        output = bert_sc(**encoding)

    # 分類スコア
    scores = output.logits
    scores_list = scores.tolist()

    # スコアが最も高いラベル
    labels_predicted = scores.argmax(-1)
    labels_predicted_list = labels_predicted.tolist()

    print("ネガポジの信頼度: ", scores)

    # スコアを確率に変換
    probs = F.softmax(scores, dim=-1)
    print("ネガポジの確率:", probs)

    if 0 in labels_predicted_list:
        negaposi = 0
    else:
        negaposi = 1 

    print("分類結果: ", negaposi)
    print("[0]: ネガティブ、 [1]: ポジティブ")

    return negaposi

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

    
# 送信ボタンが押されたときの処理（自然言語処理 + Spotify API）
@app.route('/process', methods=['POST'])
def process():
    print("----------------------------------------------------------------------------------------------------------------------------------------------------")
    if request.method == 'POST':
        text = request.form['content']
        print("入力テキスト:", text) #確認用

        # 自然言語処理を行う関数を呼び出す
        nlp_negaposi = nlp(text)

        #  Spotify APIの処理を行う関数を呼び出す
        keywords = text
        tracks = search_spotify(keywords, nlp_negaposi)
        # print(tracks)
        print("----------------------------------------------------------------------------------------------------------------------------------------------------")

        return render_template('spotify.html', text=text, negaposi=nlp_negaposi, tracks=tracks, token=session['access_token'])
    else :
        return "失敗しました"
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)