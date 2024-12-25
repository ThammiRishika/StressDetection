#!/usr/bin/env python
# coding: utf-8

# <h1 style="text-align: center">Twitter Sentiment Analysis</h1>

# #### Import the packages

# In[ ]:


import numpy as np
import pandas as pd
import json, nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud 
import seaborn as sns

from string import punctuation
from os import listdir
from numpy import array
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D

# nltk.download('wordnet')   # for Lemmatization

#get_ipython().run_line_magic('matplotlib', 'inline')


# ###### The dataset is not in "UTF-8" encoding

# In[ ]:


total_data = pd.read_csv("stressdataset.csv", encoding="ISO-8859-1")


# ##### Import [Contractions](https://stackoverflow.com/a/19794953/8141330)

# In[ ]:


with open('assets/contractions.json', 'r') as f:
    contractions_dict = json.load(f)
contractions = contractions_dict['contractions']


# ###### Setting Pandas DataFrame to show non-truncated table

# In[ ]:


pd.set_option('display.max_colwidth', -1)


# ##### Printing the dataset

# In[ ]:


total_data.head()


# ##### Taking column names into variables

# In[ ]:


tweet = total_data.columns.values[2]
sentiment = total_data.columns.values[1]
tweet, sentiment


# In[ ]:


total_data.info()


# <br/>
# 
# # 1)  Preprocessing

# ##### Define a function which handles emoji classifications

# In[ ]:


def emoji(tweet):
    # Smile -- :), : ), :-), (:, ( :, (-:, :') , :O
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\)|:O)', ' positiveemoji ', tweet)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' positiveemoji ', tweet)
    # Love -- <3, :*
    tweet = re.sub(r'(<3|:\*)', ' positiveemoji ', tweet)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-; , @-)
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;|@-\))', ' positiveemoji ', tweet)
    # Sad -- :-(, : (, :(, ):, )-:, :-/ , :-|
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:|:-/|:-\|)', ' negetiveemoji ', tweet)
    # Cry -- :,(, :'(, :"(
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' negetiveemoji ', tweet)
    return tweet


# ###### Define a function which will preprocess the tweets

# In[ ]:


import re

def process_tweet(tweet):
    tweet = tweet.lower()                                             # Lowercases the string
    tweet = re.sub('@[^\s]+', '', tweet)                              # Removes usernames
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' ', tweet)   # Remove URLs
    tweet = re.sub(r"\d+", " ", str(tweet))                           # Removes all digits
    tweet = re.sub('&quot;'," ", tweet)                               # Remove (&quot;) 
    tweet = emoji(tweet)                                              # Replaces Emojis
    tweet = re.sub(r"\b[a-zA-Z]\b", "", str(tweet))                   # Removes all single characters
    for word in tweet.split():
        if word.lower() in contractions:
            tweet = tweet.replace(word, contractions[word.lower()])   # Replaces contractions
    tweet = re.sub(r"[^\w\s]", " ", str(tweet))                       # Removes all punctuations
    tweet = re.sub(r'(.)\1+', r'\1\1', tweet)                         # Convert more than 2 letter repetitions to 2 letter
    tweet = re.sub(r"\s+", " ", str(tweet))                           # Replaces double spaces with single space    
    return tweet


# ###### Now make a new column for side by side comparison of new tweets vs old tweets

# In[ ]:


total_data['processed_tweet'] = np.vectorize(process_tweet)(total_data[tweet])


# ###### Let's compare unprocessed tweets with the processed one

# In[ ]:


total_data.head(10)


# ### Stop words

#    
# <br/>
# *["i", "me", "my", "myself", "we", "our", "ours", "ourselves",
#  "you", "your", "yours", "yourself", "yourselves", "he", "him",
#  "his", "himself", "she", "her", "hers", "herself", "it", "its",
#  "itself", "they", "them", "their", "theirs", "themselves", "what",
#  "which", "who", "whom", "this", "that", "these", "those", "am", "is",
#  "are", "was", "were", "be", "been", "being", "have", "has", "had",
#  "having", "do", "does", "did", "doing", "a", "an", "the", "and",
#  "but", "if", "or", "because", "as", "until", "while", "of", "at",
#  "by", "for", "with", "about", "against", "between", "into", "through",
#  "during", "before", "after", "above", "below", "to", "from", "up",
#  "down", "in", "out", "on", "off", "over", "under", "again", "further",
#  "then", "once", "here", "there", "when", "where", "why", "how", "all",
#  "any", "both", "each", "few", "more", "most", "other", "some", "such",
#  "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very",
#  "s", "t", "can", "will", "just", "don", "should", "now"]*
# <br/>  
# *We can't use every word from here. Because some words like `"no"`, `"nor"` etc. playes significant roles in sentiment.*
# 
# ##### So we will be making our custom list of stopwords.

# In[ ]:


# stop_words = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves",
#             "you", "your", "yours", "yourself", "yourselves", "he", "him",
#             "his", "himself", "she", "her", "hers", "herself", "it", "its",
#             "itself", "they", "them", "their", "theirs", "themselves", "what",
#             "which", "who", "whom", "this", "that", "these", "those", "am", "is",
#             "are", "was", "were", "be", "been", "being", "have", "has", "had",
#             "having", "do", "does", "did", "doing", "a", "an", "the", "and",
#             "but", "if", "or", "because", "as", "until", "while", "of", "at",
#             "by", "for", "with", "about", "against", "between", "into", "through",
#             "during", "before", "after", "above", "below", "to", "from", "up",
#             "down", "in", "out", "on", "off", "over", "under", "again", "further",
#             "then", "once", "here", "there", "when", "where", "why", "how", "all",
#             "any", "both", "each", "few", "more", "most", "other", "some", "such",
#             "only", "own", "same", "so", "than", "too", "very",
#             "can", "will", "just", "should", "now"}


# # 2) Most used words

# In[ ]:

 


# ## 2.2) Most used positive words

# In[ ]:

 


# ## 2.3) Most used negetive words

# In[ ]:

 


# #### See the word `lol`. It is used both in positive and negetive(sarcastic) sentiments. We still can't classify sarcasm.

# # 3) Feature extraction (vectorization)

# ## N-grams included (Unigram, Bigram, Trigram)

# *Tf-idf* is different from *CountVectorizer*. *CountVectorizer* gives equal weightage to all the words, i.e. a word is converted to a column (in a dataframe for example) and for each document, it is equal to 1 if it is present in that doc else 0. 
# Apart from giving this information, *Tf-idf* says how important that word is to that document with respect to the corpus.

# ## 3.1) Count vectorizer

# As we all know, all machine learning algorithms are good with numbers; we have to extract or convert the text data into numbers without losing much of the information. One way to do such transformation is *Bag-Of-Words (BOW)* which gives a number to each word but that is very inefficient. So, a way to do it is by *CountVectorizer*: it counts the number of words in the document i.e it converts a collection of text documents to a matrix of the counts of occurences of each word in the document.

# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer

count_vectorizer = CountVectorizer(ngram_range=(1,2))    # Unigram and Bigram
final_vectorized_data = count_vectorizer.fit_transform(total_data['processed_tweet'])  
final_vectorized_data


# # 4) Splitting

# ##### Splitting train data to test accuracy

 


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(final_vectorized_data, total_data[sentiment],
                                                    test_size=0.2, random_state=69)  


# ##### Printing splitted dataset sizes

 
 


from sklearn.naive_bayes import MultinomialNB  # Naive Bayes Classifier
#from sklearn.feature_extraction.text import CountVectorizer

comment2 = [" @cindolce awe........thanks sweets!! Thank you for all your advice, I owe you!! "]
 
      
check = count_vectorizer.transform(comment2).toarray() 
check
model_naive = MultinomialNB().fit(X_train, y_train) 
predicted_naive = model_naive.predict(check)
print(predicted_naive)
# define model

#structure_test = Sequential()
#e = Embedding(100000, 200, input_length=45)
#structure_test.add(e)
#structure_test.add(Conv1D(filters=100, kernel_size=2, padding='valid', activation='relu', strides=1))
#structure_test.add(GlobalMaxPooling1D())
#structure_test.summary()
#model_cnn_01 = Sequential()
#e = Embedding(100000, 200, weights=[embedding_matrix], input_length=45, trainable=False)
#model_cnn_01.add(e)
#model_cnn_01.add(Conv1D(filters=100, kernel_size=2, padding='valid', activation='relu', strides=1))
#model_cnn_01.add(GlobalMaxPooling1D())
#model_cnn_01.add(Dense(256, activation='relu'))
#model_cnn_01.add(Dense(1, activation='sigmoid'))
#model_cnn_01.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#model_cnn_01.fit(x_train_seq, y_train, validation_data=(x_val_seq, y_validation), epochs=5, batch_size=32, verbose=2)


 
