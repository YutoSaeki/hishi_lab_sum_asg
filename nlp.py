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