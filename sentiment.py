# -*- coding: utf-8 -*-
"""Untitled.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FE0ZJEAoy9DNMoDwu5ePOPt7m7wfnHrL
"""

#!pip3 install tensorflow-gpu==2.0.0-alpha0
import tensorflow as tf
from tensorflow.keras import layers,Sequential
from tensorflow.keras.preprocessing import sequence

class Attention(layers.Layer):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.dense = layers.Dense(30,activation='relu')
        self.attention_values = layers.Dense(1)
        
        
    def call(self,x):
        batch_length,seq_len,embed_length=x.shape
        out = tf.reshape(x,shape=[-1,embed_length])
        
        out = self.dense(out)
        out = self.attention_values(out)
        
        out = tf.reshape(out,shape=[-1,seq_len,1])
        
        out = tf.nn.softmax(out,axis=1)
        
        output = tf.reduce_sum(x*out,axis=1)
        
        return output



def load_model(vocab_length,sentence_length,embedding_length):

	model = Sequential()
	model.add(layers.Embedding(vocab_length,embedding_length,input_shape=(sentence_length,)))
	model.add(layers.Bidirectional(layers.LSTM(128,return_sequences=True)))
	model.add(Attention())
	model.add(layers.Dense(300,activation='relu'))
	#model.add(layers.Dense(300,activation='relu'))
	model.add(layers.Dense(1,activation='sigmoid'))
	model.compile(loss = tf.keras.losses.binary_crossentropy,optimizer='adam',metrics =['acc'])

	return model
	



