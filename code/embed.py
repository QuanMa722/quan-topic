# -*- coding: utf-8 -*-

from sentence_transformers import SentenceTransformer
import numpy as np
import warnings

warnings.filterwarnings("ignore")

with open(file="../data/lda2.txt", mode="r", encoding="utf-8") as f:
    comment_dict_list: list = f.readlines()

comment_list: list = []
for item in comment_dict_list:
    comment_list.append(eval(item)["评论内容"])

embedding_model = SentenceTransformer(
    "thenlper/gte-base-zh"
    # "thenlper/gte-large-zh"
    # "thenlper/gte-small-zh"
    # "paraphrase-multilingual-MiniLM-L12-v2"
)

embeddings = embedding_model.encode(comment_list, show_progress_bar=True)
np.save('embedding.npy', embeddings)

print(type(embeddings), embeddings.shape)