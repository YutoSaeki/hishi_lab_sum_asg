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

PyTorchをインストールした後、インポートしたらエラー吐いた時に参考にしたサイト：
https://qiita.com/sakusaku3939/items/1a133729c7f38e8403ce

BERTの最大トークン数は512であるため、入力できるテキストは500から600文字くらいが限界？
入力できるテキストの最大をそれよりも下に設定するのが無難

・自然言語処理のタスクメモ
はじめに、テキスト教材で使用していた日本語の事前学習済みモデルをそのまま使用し文章分類を試してみた。結果としては精度が低く、ネガティブとポジティブの確率を見てみるとほとんどのテキストでそれぞれ50%付近の値が取れたため、モデルが入力テキストに対する判断に自信がない事が分かった。
次に事前学習済みモデルをファインチューニングして作成したモデルを使って文章分類してみる。

Spotify APIのアクセストークンを取得するときに参考にしたサイト：
https://apidog.com/jp/blog/spotify-web-api-guide/

spotify web playback sdk 公式ドキュメント：
https://developer.spotify.com/documentation/web-playback-sdk/tutorials/getting-started












