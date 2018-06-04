# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 21:36:18 2018

@author: shen1994
"""

import tensorflow as tf

def weight_variable(shape):
    with tf.name_scope('weights'):
        return tf.Variable(tf.truncated_normal(shape, stddev=0.1))

def bias_variable(shape):
    with tf.name_scope('biases'):
        return tf.Variable(tf.zeros(shape))

def conv_pool_layer(x, w_shape, b_shape, layer_name, only_conv=False):
    with tf.name_scope(layer_name):
        W = weight_variable(w_shape)
        b = bias_variable(b_shape)
        conv = tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='VALID', name='conv2d')
        h = conv + b
        relu = tf.nn.relu(h, name='relu')
        if only_conv == True:
            return relu
        pool = tf.nn.max_pool(relu, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID', name='max-pooling')
        return pool
        
def deepid_1(input_x, output_y, class_num=None):
    
    h1 = conv_pool_layer(input_x, [4, 4, 3, 20], [20], 'Conv_layer_1')
    h2 = conv_pool_layer(h1, [3, 3, 20, 40], [40], 'Conv_layer_2')
    h3 = conv_pool_layer(h2, [3, 3, 40, 60], [60], 'Conv_layer_3')
    h4 = conv_pool_layer(h3, [2, 2, 60, 80], [80], 'Conv_layer_4', only_conv=True)
    
    with tf.name_scope('DeepID'):
        h3_flattern = tf.reshape(h3, [-1, 5*4*60])
        h4_flattern = tf.reshape(h4, [-1, 4*3*80])
        h3_w = weight_variable([5*4*60, 160])
        h4_w = weight_variable([4*3*80, 160])
        b = bias_variable([160])
        h = tf.matmul(h3_flattern, h3_w) + tf.matmul(h4_flattern, h4_w) + b
        h5 = tf.nn.relu(h)
        
    with tf.name_scope("fully_connect_layer"):
        weights = weight_variable([160, class_num])
        biases = bias_variable([class_num])
        y = tf.matmul(h5, weights) + biases

    with tf.name_scope('loss'):
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=output_y, logits=y))
        tf.summary.scalar('loss', loss)
        
    with tf.name_scope('accuracy'):
        softmax_y = tf.nn.softmax(y)
        prediction = tf.equal(tf.argmax(softmax_y, 1), tf.argmax(output_y, 1))
        accuracy = tf.reduce_mean(tf.cast(prediction, tf.float32))
        tf.summary.scalar('accuracy', accuracy)
    
    with tf.name_scope('optimizer'):
        optimizer = tf.train.AdamOptimizer(1e-4).minimize(loss)
        
    merged = tf.summary.merge_all()
    
    return merged, loss, accuracy, optimizer
    
def deepid_2():
    pass

def deepid_3():
    pass
        