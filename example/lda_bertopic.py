# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
from hdbscan import HDBSCAN
from umap import UMAP
import warnings
import logging
import jieba

# Suppress warnings and set logging level for jieba
warnings.filterwarnings("ignore")
jieba.setLogLevel(logging.INFO)


def get_topic(file_path) -> list:
    """
    Extract topics from text data using Latent Dirichlet Allocation (LDA).

    Args:
        file_path (str): Path to the file containing raw text data.

    Returns:
        list: A list of keywords representing topics.
    """

    try:
        # Load stopwords
        with open(file="stopwords.txt", mode="r", encoding="utf-8") as stop_file:
            stopwords_list = stop_file.read().splitlines()

        # Load raw data
        with open(file=file_path, mode="r", encoding="utf-8") as f:
            comment_dict_list = f.readlines()

        # Extract comments
        comment_list = [eval(item)["评论内容"] for item in comment_dict_list]
        print(f"Raw data volume: {len(comment_list)}")

        # Preprocess data: Tokenize and remove stopwords
        corpus_list = []
        for sentence in comment_list:
            corpus = jieba.lcut(sentence)
            corpus = [word for word in corpus if word not in stopwords_list and word != '']
            corpus_list.append(" ".join(corpus))

        # Convert the corpus to a word frequency matrix
        vectorizer = CountVectorizer()
        feature_matrix = vectorizer.fit_transform(corpus_list)

        # Train the LDA model
        lda = LatentDirichletAllocation(
            n_components=5,
            random_state=42,
            learning_method='batch'
        )

        lda.fit(feature_matrix)

        # Extract top words for each topic
        feature_names = vectorizer.get_feature_names_out()
        top_features_words_list = []
        for topic_idx, topic in enumerate(lda.components_):
            top_features_idx = topic.argsort()[-10:][::-1]
            top_features_words = [feature_names[i] for i in top_features_idx]
            top_features_words_list += top_features_words

        # Return a list of unique top words representing topics
        topic_list = list(set(top_features_words_list))
        return topic_list

    except Exception as e:
        print(f"Error: {e}")
        return []


def process_data(topic_list):
    """
    Filter comments based on the presence of topic-related keywords.

    Args:
        topic_list (list): List of keywords representing topics.

    Returns:
        list: A list of comments that contain at least one topic keyword.
    """
    try:
        # Load and preprocess test data
        with open(file="test_data.txt", mode="r", encoding="utf-8") as f1:
            comment_dict_list = f1.readlines()

        comment_list = [eval(item)["评论内容"] for item in comment_dict_list]
        comment_process_list = []

        # Filter comments containing topic-related keywords
        for comment in comment_list:
            corpus = jieba.lcut(comment)
            if any(word in topic_list for word in corpus):
                comment_process_list.append(comment)

        print(f"Processed data volume: {len(comment_process_list)}")
        return comment_process_list

    except Exception as e:
        print(f"Error: {e}")
        return []


def bertopic_apply(comment_process_list):
    """
    Apply BERTopic for topic modeling and visualization.

    Args:
        comment_process_list (list): List of processed comments to analyze.
    """
    try:
        # Load stopwords
        with open(file="stopwords.txt", mode="r", encoding="utf-8") as stop_file:
            stopwords_list = stop_file.read().splitlines()

        # Initialize embedding model
        # Possibility to change the embedded model
        embedding_model = SentenceTransformer(
            "thenlper/gte-base-zh"
        )

        # Preprocess and embed the comments
        corpus_list = []
        for sentence in comment_process_list:
            corpus = jieba.lcut(sentence)
            corpus = [word for word in corpus if word not in stopwords_list and word != '']
            corpus_list.append(" ".join(corpus))

        embeddings = embedding_model.encode(corpus_list, show_progress_bar=True)

        # Initialize UMAP and HDBSCAN models
        umap_model = UMAP(
            n_neighbors=15,
            n_components=5,
            min_dist=0.0,
            metric='cosine',
            random_state=30
        )

        hdbscan_model = HDBSCAN(
            min_cluster_size=35,
            min_samples=10,
            metric='euclidean'
        )

        vectorizer_model = CountVectorizer()

        # Initialize BERTopic model
        topic_model = BERTopic(
            embedding_model=embedding_model,
            vectorizer_model=vectorizer_model,
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
        )

        # Fit the BERTopic model
        topics, _ = topic_model.fit_transform(corpus_list, embeddings=embeddings)

        # Visualize the results
        fig_barchart = topic_model.visualize_barchart()
        fig_barchart.show()

        # Visualisation as required
        # fig_topics = topic_model.visualize_topics()
        # fig_topics.show()
        #
        # reduced_embeddings = UMAP(n_neighbors=10, n_components=2, min_dist=0.0, metric='cosine').fit_transform(
        #     embeddings)
        # fig_documents = topic_model.visualize_documents(corpus_list, reduced_embeddings=reduced_embeddings,
        #                                                 hide_document_hover=True)
        # fig_documents.show()
        #
        # hierarchical_topics = topic_model.hierarchical_topics(corpus_list)
        # fig_hierarchy = topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics)
        # fig_hierarchy.show()

    except Exception as e:
        print(f"Error: {e}")
        return []


if __name__ == '__main__':
    # Define file path for single-day data
    # You can make changes to the code associated with the data file
    file_path = 'test_data.txt'

    # Obtaining Topic Words for Short Text Data Using LDA Models
    topic_list = get_topic(file_path)

    # A filtering of the original data using subject headings
    comment_process_list = process_data(topic_list)

    # Load raw data
    with open(file=file_path, mode="r", encoding="utf-8") as f:
        comment_dict_list = f.readlines()
    comment_list = [eval(item)["评论内容"] for item in comment_dict_list]

    # Perform a comparison of the effect of the original data with that of the processed data.
    bertopic_apply(comment_list)
    bertopic_apply(comment_process_list)
