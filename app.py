from __future__ import unicode_literals
from flask import Flask,render_template,url_for,request,jsonify
import pickle
import keras
from keras.preprocessing.sequence import pad_sequences
import time
import flask
import numpy as np
from summarize_nltk import nltk_summarizer
import time
import requests

app = Flask(__name__)
#Let's load the best model obtained during training
best_model = keras.models.load_model("best_model2.hdf5")
max_words = 5000
max_len = 200
with open('tokenizer.pickle', 'rb') as handle:

	tokenizer = pickle.load(handle)

# loading tokenizer
def preprocess_texts(text):
	max_words = 5000
	max_len = 200
    # saving tokenizer
	with open('tokenizer.pickle', 'rb') as handle:

		tokenizer = pickle.load(handle)
	sequence = tokenizer.texts_to_sequences(text)
	test = pad_sequences(sequence, maxlen=max_len)
	return test

def lstm_sent(text):
	""" 
	param:takes in a json file containing the text we want to summarize
	returns: returns json containing sentiment value
	"""
	#array of sentiment
	sentiment = ['Negative','Positive']
	sequence = tokenizer.texts_to_sequences([text])
	test = pad_sequences(sequence, maxlen=max_len)
	senti = sentiment[np.around(best_model.predict(test), decimals=0).argmax(axis=1)[0]]
	#end = time.time()
	#final_time = end-start
	#print(final_time)
	return senti


######################
#home page
#######################
@app.route('/', methods =['GET','POST'])
def index():
	return ("sentiment Analysis home page")

##########################################
#sentiment Analysis
##########################################
@app.route('/api/sentiment', methods =['GET','POST'])
def lstm_sentiment():
	""" 
	param:takes in a json file containing the text we want to summarize
	returns: returns json containing sentiment value
	"""
	start = time.time()
	if request.method == 'POST':
		#text = request.form['text']
		request_data = request.get_json()
		text = request_data['text']
		#array of sentiment
		sentiment = ['Negative','Positive']
		sequence = tokenizer.texts_to_sequences([text])
		test = pad_sequences(sequence, maxlen=max_len)
		senti = sentiment[np.around(best_model.predict(test), decimals=0).argmax(axis=1)[0]]
		end = time.time()
		final_time = end-start
		print(final_time)
		return(jsonify(sentiment =senti , Time=final_time))




##########################################
#Text summarization
##########################################
@app.route('/api/text_summarization',methods=['GET','POST'])
def text_sum():
	""" 
	param: takes in json containing text to be summarized
	returns:returns summarized text and the time taken to summarize it
	"""
	start = time.time()
	if request.method == 'POST':
		request_data = request.get_json()
		rawtext  = request_data['text']		
		#final_reading_time = readingTime(rawtext)
		final_summary_nltk = nltk_summarizer(rawtext)
		#summary_reading_time_nltk = readingTime(final_summary_nltk)

		end = time.time()
		final_time = end-start
		print(final_time)
		sentiment = lstm_sent(final_summary_nltk)
	return flask.jsonify(Summary=final_summary_nltk , Time=final_time, Sentiment =sentiment)





if __name__ == '__main__':
	#app.run(debug=True)
	app.run(debug=True, host = "10.10.30.98")