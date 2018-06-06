# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 16:13:20 2018

@author: shen1994
"""

import tensorflow as tf
import numpy as np
from image_vector import load_pair_vector

def cosine(a, b): 
    
    t = np.float(np.dot(a.T, b))
    k = np.linalg.norm(a) * np.linalg.norm(b)
    cos = t / k
    
    return (1 - cos)

def run(threshold=0.43):
    
    ckpt = tf.train.latest_checkpoint('model')
    saver = tf.train.import_meta_graph(ckpt + '.meta')
    
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, ckpt)
        
        x = tf.get_default_graph().get_tensor_by_name("input/x:0")
        vector = tf.get_default_graph().get_tensor_by_name("DeepID/Relu:0")
        
        real_x_1, real_x_2, real_y = load_pair_vector("image/test_vector_dataset.pkl", 20)
        
        pre_vector_1 = sess.run(vector, {x: real_x_1})
        pre_vector_2 = sess.run(vector, {x: real_x_2})
        
        pre_y = np.array([cosine(x, y) for x, y in zip(pre_vector_1, pre_vector_2)])
        thre_y = []
        
        for i in range(len(pre_y)):
            
            if pre_y[i] < threshold:
                thre_y.append(1)
            else:
                thre_y.append(0)
        
        print("------------------------------")
        print(u"预测：", thre_y)
        print(u"真实：", list(real_y))
        print("------------------------------")

if __name__ == "__main__":
    run()
    