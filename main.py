# -------------------------------------------------------
# メインのファイル
# -------------------------------------------------------

# Flask周り
from flask import Flask, render_template, request, jsonify, redirect, session, url_for, make_response

# 自然言語処理の関数ファイルを読み込み
import nlp
# Spotify APIの関数ファイルを読み込み
import spotify

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
# REDIRECT_URI = 'https://yuto.yuto0702.com/callback'  # 外部公開用のリダイレクトURI
# REDIRECT_URI = 'https://stephen-federal-zoloft-muslim.trycloudflare.com/callback'  # 外部公開用のリダイレクトURI
# REDIRECT_URI = 'https://resolved-viable-quetzal.ngrok-free.app/callback'  # 外部公開用のリダイレクトURI

# Spotifyの認可エンドポイントとトークンエンドポイント
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'


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

    
# 送信ボタンが押されたときの処理（自然言語処理 + Spotify API）
@app.route('/process', methods=['POST'])
def process():
    print("----------------------------------------------------------------------------------------------------------------------------------------------------")
    if request.method == 'POST':
        text = request.form['content']
        print("入力テキスト:", text) #確認用

        # 自然言語処理を行う関数を呼び出す
        nlp_negaposi = nlp.nlp(text)

        # Spotify APIの処理を行う関数を呼び出す
        keywords = text
        tracks = spotify.search_spotify(keywords, nlp_negaposi)
        # print(tracks)
        print("----------------------------------------------------------------------------------------------------------------------------------------------------")

        return render_template('spotify.html', text=text, negaposi=nlp_negaposi, tracks=tracks, token=session['access_token'])
    else :
        return "失敗しました"
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)