import numpy as np
import pandas as pd
from wordcloud import STOPWORDS
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import text2emotion as te
import spacy
from sklearn.feature_extraction.text import CountVectorizer
import warnings
warnings.filterwarnings("ignore")
import nltk
import ssl

import en_core_web_sm



def avg_rating(data):
    avg = round(data["Rating"].mean(),2)
    return avg


def text_cleaner(text):
    cleaned_text =  ' '.join(re.sub('([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', str(text).lower()).split())
    return cleaned_text

def sentiment_analysis(data):
    sid = SentimentIntensityAnalyzer()
    vader_scores = []
    for index in range(len(data["cleaned_review"])):
        score = sid.polarity_scores(data["cleaned_review"][index])
        if score["pos"] > score["neg"]:
            vader_scores.append("Positive")
        elif score["pos"] < score["neg"]:
            vader_scores.append("Negative")
        else:
            vader_scores.append("Neutral")


    data["Sentiment_VADER"] = vader_scores
    return data    



def get_positive(data):
    positive_reviews = data[data['Sentiment_VADER']=='Positive']
    return len(positive_reviews)

def get_negative(data):
    negative_reviews = data[data['Sentiment_VADER']=='Negative']
    return len(negative_reviews)

def get_neutral(data):
    neutral_reviews = data[data['Sentiment_VADER']=='Neutral']
    return len(neutral_reviews)


def rating_value_counter(data):
    rating_dict = dict(data["Rating"].value_counts())
    lst = rating_dict.items()

    sorted_list = sorted(lst, key = lambda x : x[0])

    new_list = []

    for tuples in sorted_list:
        key = f"{int(tuples[0])} star"
        val = tuples[1]
    
        key_vals = [key, val]
        new_list.append(key_vals)
    
    
    return new_list



    




def lemma_words_para(type_data):
    cleaned_df = type_data["cleaned_review"]
    
    reviews = [sentence for sentence in cleaned_df]
    # print(reviews)
    reviews = [x for x in reviews if x]

    text = " ".join(reviews)

    text_tokens = word_tokenize(text)


    text_tokens_lower = []
    for word in text_tokens:
        text_tokens_lower.append(word.lower())

    stopwords = STOPWORDS

    no_stop_tokens = []

    for word in text_tokens_lower:
        if word not in stopwords:
            no_stop_tokens.append(word)
    # print(no_stop_tokens)

    stripped_space = [word.strip(" ") for word in no_stop_tokens]

    del_small_words = [word for word in stripped_space if len(word) > 2]
    
    # print(no_stop_tokens)

    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in del_small_words] 

    words_counter = dict(Counter(lemmas))


    sorted_list_desc = list(sorted(words_counter.items(),
                           key=lambda item: item[1],
                           reverse=True))

    sorted_list= []
    sorted_values = []


    for i in range(len(sorted_list_desc)):
        sorted_list.append(sorted_list_desc[i][0])
        sorted_values.append(sorted_list_desc[i][1])
    

    sorted_list = sorted_list[:35]
    sorted_values = sorted_values[:35]

    ret_list = [sorted_list, sorted_values] 
    return ret_list



def pol_test(data):
    sid = SentimentIntensityAnalyzer()
    polarity = sid.polarity_scores(data["cleaned_review"][0])
    return polarity

def extreme_sentiments(data):
    sid = SentimentIntensityAnalyzer()

    vader_sentiments = []


    for index in range(len(data["cleaned_review"])):
        score = sid.polarity_scores(data["cleaned_review"][index])

    
        if score["pos"] > score["neg"] and score["pos"] >= 0.8:
            vader_sentiments.append("Very positive")
        elif score["pos"] < score["neg"] and score["neg"] >= 0.8:
            vader_sentiments.append("Very negative")
        elif score["pos"] > score["neg"]:
            vader_sentiments.append("Positive")
        elif score["neg"] > score["pos"]:
            vader_sentiments.append("Negative")
        else:
            vader_sentiments.append("Neutral")

    data["Sentiment_VADER"] = vader_sentiments

    
    vader_dict = dict(data["Sentiment_VADER"].value_counts())
    
    return vader_dict


def ner_analysis(data):
    nlp = en_core_web_sm.load()

    para = []
    
    for string in data['cleaned_review']:
        para.append(string)
    
    
    one_block = ''.join(para)
    doc_block = nlp(one_block)
    
    adjectives = [token.text for token in doc_block if token.pos_ in ('ADJ')]
    
    cv = CountVectorizer()

    X = cv.fit_transform(adjectives)
    sum_words = X.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in cv.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)


    return words_freq[:10]



def ngram_words(df, ngram_low, ngram_high):
    data = df["Review_content"]
    cv = CountVectorizer(ngram_range=(ngram_low,ngram_high))
    X = cv.fit_transform(data)
    sum_words = X.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in cv.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)

    return words_freq[:10]


def date_analyzer(data):
    print(data['Date'].iloc[0])
    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values(by='Date')
    data["Date"] = [str(x) for x in data["Date"]]

    my_dict = dict(data.Date.str.slice(0,4).value_counts())
    myList = my_dict.items()
    myList = sorted(myList) 
    x, y = zip(*myList)
    
    final_data = [x[0],x[-1], y]

    return final_data


def single_sentiment_analyzer(text):
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(text)

    return score

def single_emotion_analyzer(text):
    emot = te.get_emotion(text)

    return emot


def single_sentiment_blob(text):
    blob = TextBlob(text)
    return blob.sentiment[0]