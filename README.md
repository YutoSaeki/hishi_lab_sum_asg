# hishi_lab_sum_asg
## 大学3年研究室の夏休み課題
## Spotify APIと自然言語処理を用いた、ユーザの感情に応じて楽曲を再生するWEBアプリケーションの作成。

1. 学習内容
- 内容（どのような技術とターゲットについて学習するか）
- 

2. 学習成果目標
- 内容1
- 内容2
- 内容3

4. 習作（練習のための作品）の概要
- 概要
- 特徴：アピールポイント
- 組み込む機能
- 使用する技術
- Spotify APIについて

5. 参考にした類似物


6. 学習全体のスケジュール
- 8月
- 9月

7. 懸念点


8. 画面遷移図


9. 各画面の内容


10. メモ

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
入力できるテキストの最大をそれよりも下に設定するのが無難

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











