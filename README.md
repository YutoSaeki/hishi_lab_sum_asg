# hishi_lab_sum_asg
## 大学3年研究室の夏休み課題
## Spotify APIと自然言語処理を用いた、ユーザの感情に応じて楽曲を再生するWEBアプリケーションの作成。

1. 学習内容
- 内容（どのような技術とターゲットについて学習するか）
  - Pythonの理解を深め，自然言語処理について学習する。
  - 自然言語処理の学習についてはこの教材を使用する．（https://amzn.asia/d/07ceOtOG）
- 目標成果物
  - 目標成果物としてSpotifyを用いて，入力したテキストからユーザの気分を分析して適した楽曲を再生できるWebアプリケーションを作成する。

2. 学習成果目標
- 内容1 : Pythonの理解を深める。
- 内容2 : Pythonを使った自然言語処理の理解。
- 内容3 : 入力したテキストからユーザの気分に適した楽曲を再生するWebアプリの作成。

4. 習作（練習のための作品）の概要
- 概要
  Web画面上で入力したテキストからユーザの感情を分析して、気分に合った楽曲を再生する。注意点としてユーザはSpotifyにサブスク登録している必要がある。
- 特徴：アピールポイント
  - その日、その時の気分に応じて音楽を聴くことができる。
  - 音楽を聴きたい気分だけど何を聴くか選ぶのが面倒さい時に。
  - 新たな音楽と出会えるかもしれない。
- 組み込む機能
  - Spotifyのログインとアクセストークンを取得する機能。
  - ユーザがテキストで今の気分や思ったことなどを入力する機能。
  - 入力したテキストを分析する機能。
  - Spotify APIを用いた楽曲検索と楽曲情報を取得する機能。
  - 取得した楽曲データの中から1曲に絞り込む機能。
  - 楽曲を再生する機能。
- 使用する技術
  - Python
  - Flask
  - html
  - css
  - javascript
  - Spotify API
  - BERT
- Spotify APIについて
  - Spotify APIには音楽データの取得，管理，再生するための機能が用意されている．Spotify APIを使用することで楽曲検索や楽曲・アルバム・アーティスト情報の取得などができる．また，楽曲ごとに特徴量を数値化したパラメータが付与されている．楽曲を絞り込む機能については、この内部パラメータを使用する。
- 取得した楽曲データの中から1曲に絞り込む機能について
  はじめに楽曲50曲分の内部パラメータを取得する。それぞれの内部パラメータごとで閾値よりも高いor低い楽曲を変数に代入する（ここの閾値はネガポジの０、1によって判定する）。内部パラメータごとに選ばれた楽曲が入った変数それぞれの中で、楽曲ごとにカウントし、最もカウントが多かったものを適した楽曲として採用した。

5. 参考にした類似物
- SpotifyのSong Psychic：今年の3月くらいに期間限定で行っていた歌占いのようなサービス．
https://qiita.com/sayuyuyu/items/4ca06a851fca41f6b270

6. メモ

テキスト第6章（文章分類）のサンプルコードのリンク：　
https://colab.research.google.com/github/stockmarkteam/bert-book/blob/master/Chapter6.ipynb

インストールしたライブラリ
・PyTorch　（深層学習のフレームワーク）
・Transformers　（ニューラル言語モデルのライブラリ）
・Fugashi　（日本語の形態素解析ツールのMeCabをPythonから使えるようにしたもの）
・ipadic　（Mecabで形態素解析を行う際に用いる辞書）
・PyTorch Lightning　（PyTorchで書く必要がある処理がメソッド化されており、簡単にコードが書けるフレームワーク）
・spotipy　（SpotifyのAPIを扱うためのライブラリ）

BERTの最大トークン数は512であるため、入力できるテキストは500から600文字くらいが限界？
入力できるテキストの最大をそれよりも下に設定するのが無難（125文字までしか入力できなかった）

PyTorchをインストールした後、インポートしたらエラー吐いた時に参考にしたサイト：
https://qiita.com/sakusaku3939/items/1a133729c7f38e8403ce

Spotify API 公式ドキュメント:
https://developer.spotify.com/documentation/web-api

Spotify APIのアクセストークンを取得するときに参考にしたサイト：
https://apidog.com/jp/blog/spotify-web-api-guide/

spotify web playback sdk 公式ドキュメント：
https://developer.spotify.com/documentation/web-playback-sdk/tutorials/getting-started

Spotify Web API 取得可能なデータまとめ:
https://qiita.com/toxic_apple/items/a66f81d233608e1eda77

Spotify APIの楽曲内部パラメータをまとめたサイト:
https://qiita.com/sayuyuyu/items/4ca06a851fca41f6b270

100MB以上のファイルをGithubにPushする方法:
https://qiita.com/ArG0rithm-Ace/items/0f0e0e225db756162e24

構築中サイトのテスト公開に便利、「ngrok」(エングロック)の使い方:
https://qiita.com/yama-github/items/94514830ad7759bc3687

ngrok の無料版でドメイン・サブドメインを固定できる仕組みを試す！:
https://qiita.com/youtoy/items/8a79d6954bb37f935f1b

Spotifyの認証プロセスでユーザーに毎回アドレスとパスワードの入力を強制する方法は、現時点ではSpotifyの仕様上、提供されていない。
SpotifyのOAuth認証は、ユーザーが一度認証すればセッションを保持し、以降のログイン時には再認証なしでアクセスできるようにする設計になっている。











