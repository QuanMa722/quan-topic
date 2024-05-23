# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import logging
import jieba

jieba.setLogLevel(logging.INFO)


def get_topic():
    try:

        # deactivated lists can be modified based on subject lines
        with open(file="../data/stopwords.txt", mode="r", encoding="utf-8") as stop_file:
            stopwords: list = stop_file.read().splitlines()

        with open(file="../data/process4.txt", mode="r", encoding="utf-8") as f:
            comment_dict_list: list = f.readlines()

        comment_list = [eval(item)["评论内容"] for item in comment_dict_list]

        corpus_list = []
        for sentence in comment_list:
            corpus = jieba.lcut(sentence)
            corpus = [word for word in corpus if word not in stopwords and word != '']
            corpus = " ".join(corpus)
            corpus_list.append(corpus)

        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(corpus_list)

        # min_num_topics = 2
        # max_num_topics = 20
        #
        # perplexity_scores = []
        # for num_topics in range(min_num_topics, max_num_topics + 1):
        #     lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
        #     lda.fit(X)
        #     score = lda.perplexity(X)
        #     perplexity_scores.append(score)
        #
        #     print(f"Num topics: {num_topics}, Perplexity: {score}")
        #
        # best_num_topics = np.argmin(perplexity_scores) + min_num_topics
        # print(f"Best number of topics: {best_num_topics}")

        best_num_topics = 5

        lda = LatentDirichletAllocation(n_components=best_num_topics,
                                        random_state=42,
                                        learning_method='batch')
        lda.fit(X)

        print('Perplexity:', lda.perplexity(X))

        feature_names = vectorizer.get_feature_names_out()

        print("-" * 75)
        top_features_words_list = []
        for topic_idx, topic in enumerate(lda.components_):
            top_features_idx = topic.argsort()[-10:][::-1]
            top_features_words = [feature_names[i] for i in top_features_idx]
            print(top_features_words)
            top_features_words_list += top_features_words

        print("-" * 75)
        return list(set(top_features_words_list))

    except Exception as e:
        print(f"Error: {e}")


def get_file(topic_words):
    try:

        with open(file="../data/process4.txt", mode="r", encoding="utf-8") as f1:
            comment_dict_list: list = f1.readlines()

        with open(f"../data/lda4.txt", "a", encoding="utf-8") as f2:
            for comment in comment_dict_list:
                corpus = jieba.lcut(eval(comment)["评论内容"])
                for word in corpus:
                    if word in topic_words:
                        f2.write(str(comment))
                        break
                    else:
                        continue
            print("Done")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    top_words_list = get_topic()
    # processing the original data after determining the list of deactivated words
    # get_file(top_words_list)
