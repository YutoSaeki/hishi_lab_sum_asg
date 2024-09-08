from flask import Flask, render_template, request

import numpy as np

import torch.nn.functional as F

# 必要なライブラリの読み込み
import random
import glob
from tqdm import tqdm

import torch
from torch.utils.data import DataLoader
from transformers import BertJapaneseTokenizer, BertForSequenceClassification
import pytorch_lightning as pl

# シードの固定
seed = 42
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

# 日本語の事前学習モデル
MODEL_NAME = 'tohoku-nlp/bert-base-japanese-whole-word-masking'

# 事前学習モデルのロード
tokenizer = BertJapaneseTokenizer.from_pretrained(MODEL_NAME)
bert_sc = BertForSequenceClassification.from_pretrained(
    MODEL_NAME, num_labels=2
)
# CUDAが利用できる場合のみ.cuda()を呼び出す（MACではCUDAがサポートされていないため利用できない→CPUを使ってモデルをロード）
#bert_sc = bert_sc.cuda()

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nlp', methods=['POST'])
def nlp():
    if request.method == 'POST':
        #text = None
        text = request.form['content']
        print("入力テキスト:", text) #確認用

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
        print("予測: ", labels_predicted_list)

        # スコアを確率に変換
        probs = F.softmax(scores, dim=-1)
        print("ネガポジの確率:", probs)

        return render_template('index.html', text=text, scores=scores, labels_predicted=labels_predicted_list, probs=probs)
        #return
    else :
        return "失敗しました"
    

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True, port=5001)