import os

import PyPDF2
#import goto
import nltk
import json
import pdfplumber
import textract
from docutils.nodes import label
from nltk import WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords, wordnet
from nltk.metrics.aline import similarity_matrix
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
from string import punctuation
import numpy as np
import pandas as pd
import language_check
import math

import sys


def synonyms_find(items):
    synonyms = []
    for word in items:
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
    g = set(synonyms)
    j = list(g)
    return j

def stopword(strf):
    # Write a for-loop to open many files (leave a comment if you'd like to learn how).
    filename = strf
    text=""
    with pdfplumber.open(filename) as pdf:
        for page in pdf.pages:
            text=text+page.extract_text()
    # print(text)
    if text != "":
        text = text
    # If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text.
    else:
        text = textract.process(filename, method='tesseract', language='eng')
    # Now we have a text variable that contains all the text derived from our PDF file. Type print(text) to see what it contains. It likely contains a lot of spaces, possibly junk such as '\n,' etc.
    # Now, we will clean our text variable and return it as a list of keywords.
    # The word_tokenize() function will break our text phrases into individual words.
    #replace apostrophes
    text = ' '.join([w.lower() for w in word_tokenize(text)])
    text2 = text
    text= ''.join(c for c in text if not c.isdigit())
    text=' '.join([w for w in text.split() if len(w) > 1])

    text=''.join(c for c in text if c not in punctuation)
    np.char.replace(text, "'", "")

    #single character removal
    tokens = word_tokenize(text2)
    # We'll create a new list that contains punctuation we wish to clean.
    punctuations = ['(', ')', ';', ':', '[', ']', ',','!','#','?','$','%','&','*','+','-','--','..','.','/','<','=','>','@','^','_','`','{','|','}','~','\n']
    # We initialize the stopwords variable, which is a list of words like "The," "I," "and," etc. that don't hold much value as keywords.
    pattern = '[0-9]'
    stop_words = stopwords.words('english')
    wordnet_lemmatizer = WordNetLemmatizer()
    word_tokens = nltk.word_tokenize(text2)
    lemmatized_word = [wordnet_lemmatizer.lemmatize(word) for word in word_tokens]
    #print("lemet")
    #print(lemmatized_word)
    snowball_stemmer = SnowballStemmer('english')
    word_tokens = nltk.word_tokenize(text2)
    stemmed_word = [snowball_stemmer.stem(word) for word in lemmatized_word]
    #print(stemmed_word)
    # We create a list comprehension that only returns a list of words that are NOT IN stop_words and NOT IN punctuations.
    keywords = [word for word in tokens if not word in stop_words and not word in punctuations and word not in pattern]
    keywordsnew=[word for word in lemmatized_word if not word in stop_words and not word in punctuations and word not in pattern]
    #print(keywordsnew)
    text5 = ' '.join([str(elem) for elem in keywordsnew])
    listtext=nltk.sent_tokenize(text2)
    text3=list(text2)
    del pdf
    return text5
    #tfidf(keywords,listtext)


def tfidf(text,sttnew):
    corpus=[text]
    vocabulary=[]
    # print("tfidf")
    vocabulary=vocabulary+(sttnew["best"])
    cbest=len(vocabulary)
    #print(cbest)
    vocabulary=vocabulary+(sttnew["average"])
    cavg=len(vocabulary)
    #print(cavg)
    vocabulary=vocabulary+(sttnew["common"])
    ccom=len(vocabulary)
    #print(ccom)
    #print(vocabulary)
    pipe = Pipeline([('count', CountVectorizer(vocabulary=vocabulary)),('tfid', TfidfTransformer(use_idf=True))]).fit(corpus)
    # print(pipe['count'].transform(corpus).toarray())
    voc=pipe['count'].transform(vocabulary).toarray()
    tfidf_matrixx=pipe['count'].transform(corpus).toarray()
    # print (dict(zip(vocabulary,pipe['tfid'].idf_)))
    m = pipe['tfid'].idf_
    # print(pipe.transform(corpus).shape)
    sum=0
    count = len(vocabulary)
    # print(count)

    # print(cosine_similarity(voc[0:count],tfidf_matrixx))
    cosvalues = cosine_similarity(voc[0:count], tfidf_matrixx)
    # print("cos values")
    sw=0
    for p in range(ccom):
        if p<cbest:
            sw=sw+(cosvalues[p]*1)
            #print(cosvalues[p])
        elif p<cavg:
            sw=sw+(cosvalues[p]*0.75)
            #print(cosvalues[p])
        else:
            sw=sw+(cosvalues[p]*0.5)
            #print(cosvalues[p])
    # print(sw)
    divd=(1*cbest)+(0.75*(cavg-cbest+1))+(0.5*(ccom-(cavg+cbest)+1))
    # print(divd)
    swa=sw/(divd)
    # print("savg")
    swa=swa*100

    swa=int(swa)
    #print(swa)
    return swa

def plagiarism(strf):
    document=[]
    for filename in strf:
        #print(filename)
        filename="D:/AEG/Uploads/Evaluated/" +filename

        text = ""
        with pdfplumber.open(r'' + filename) as pdf:
            for page in pdf.pages:
                text = text + page.extract_text()
        #print(text)


        if text != "":
            text = text
        # If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text.
        else:
            text = textract.process(filename, method='tesseract', language='eng')
        text = ' '.join([w.lower() for w in word_tokenize(text)])
        document.append(text)
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(document)
    dictplag={}
    # OPTIONAL: Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix,
                      columns=count_vectorizer.get_feature_names(),
                      index=[file for file in strf])
    #print(df)
    pdfmat = cosine_similarity(df, df)
    # print(pdfmat)
    # print(pdfmat.item((0)))
    row=len(document)
    column=len(document)
    # print(row,column)

    for i in range(row):
        doc1 = strf[i]
        dictplag[doc1]=[]
        for j in range(column):
            #print(i,j)
            if(i<j):
                if (float(pdfmat[i][j]) >= 0.99999):
                    doc2=strf[j]
                    flag = 1
                    for k,v in dictplag.items():
                        if(doc2==k):
                            pass
                        else:

                            for y in range(len(v)):
                                if(doc2==v[y]):
                                    flag=0
                                    pass
                    if(flag==1):
                        dictplag[doc1].append(doc2)
    del pdf
    return dictplag
def grammarcheck(strf):
    tool = language_check.LanguageTool('en-US')
    filename = strf
    text = ""
    with pdfplumber.open(filename) as pdf:
        for page in pdf.pages:
            text = text + page.extract_text()
    #print(text)
    if text != "":
        text = text
    # If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text.
    else:
        text = textract.process(filename, method='tesseract', language='eng')
    #text = ' '.join([w.lower() for w in word_tokenize(text)])
    words = text.split()
    #print(text)
    #print('Number of words in text file :', len(words))
    matches = tool.check(text)
    #print(len(matches))
    score=(len(matches)/len(words))
    score2=round(50-score*50)
    dict=score2
    sf=strf.name
    w=sf.split(".")
    wnew=w[0].split("/")


    filepath = os.path.join('media/Essays/Report', wnew[2]+'.txt')
    if not os.path.exists('media/Essays/Report'):
        os.makedirs('media/Essays/Report')
    f = open(filepath, "w+")

    #f = open('Essays\Report/'+wnew[2]+'.txt', 'w+')
    for m in range(len(matches)):
        #print(str(matches[m]))
        strnn = str(matches[m])
        for i in strnn:
            #print("kkk", i)
            try:
                f.write(i)
            except:
                # print("An exception occurred")
                sti=i.encode(encoding='utf-8')
                f.write(str(sti))
        f.write("\n")
    f.close()
    del f
    del pdf
    return(dict)

