# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 21:31:56 2018

@author: shen1994
"""

import os
import tensorflow as tf
import numpy as np
from image_vector import load_vector
from image_vector import load_pair_vector
from image_vector import load_vector_from_index
from image_vector import safe_file_close
from model import deepid_1

def run():
    
    epocs = 100001
    batch_size = 256
    
    log_dir = "log"
    if tf.gfile.Exists(log_dir):
        tf.gfile.DeleteRecursively(log_dir)
    tf.gfile.MakeDirs(log_dir)
    
    model_dir = "model"
    if tf.gfile.Exists(model_dir):
        tf.gfile.DeleteRecursively(model_dir)
    tf.gfile.MakeDirs(model_dir)
    
    class_num = len(os.listdir("image/origin")) + 1


    with tf.name_scope('input'):
        x = tf.placeholder(tf.float32, [None, 55, 47, 3], name='x')
        y = tf.placeholder(tf.float32, [None, class_num], name='y')

    merged, loss, accuracy, optimizer = deepid_1(x, y, class_num=class_num)
    
    saver = tf.train.Saver()
    
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        train_writer = tf.summary.FileWriter(log_dir + "/train", sess.graph)
        valid_writer = tf.summary.FileWriter(log_dir + "/valid", sess.graph)
        
        t_big_number, t_size, t_index, t_pkl_file = 0, 0, 0, None
        v_big_number, v_size, v_index, v_pkl_file = 0, 0, 0, None
        step = 0
        while step < epocs:
            
            train_x, train_y, t_index, t_big_number, t_size, t_pkl_file = load_vector_from_index(
                                    "image/train_vector_dataset.pkl",
                                    batch_size,
                                    t_index,
                                    t_big_number,
                                    t_size,
                                    t_pkl_file)
            
            train_onehot_y = (np.arange(class_num) == train_y[:, None]).astype(np.float32)
            
            _ = sess.run(optimizer, {x: train_x, y: train_onehot_y})
            
            if step % 1000 == 0:
                
                # train
                summary = sess.run(merged, {x: train_x, y: train_onehot_y})
                train_writer.add_summary(summary, step)
                
                # valid
                valid_x, valid_y, v_index, v_big_number, v_size, v_pkl_file = load_vector_from_index(
                                        "image/valid_vector_dataset.pkl",
                                        batch_size,
                                        v_index,
                                        v_big_number,
                                        v_size,
                                        v_pkl_file)
                valid_onehot_y = (np.arange(class_num) == valid_y[:, None]).astype(np.float32)
                
                summary = sess.run(merged, {x: valid_x, y: valid_onehot_y})
                valid_writer.add_summary(summary, step)
                
                t_cost, t_acc = sess.run([loss, accuracy], {x: train_x, y: train_onehot_y})
                v_cost, v_acc = sess.run([loss, accuracy], {x: valid_x, y: valid_onehot_y})
                
                print(str(step) + ": train --->" + "cost:" + str(t_cost) + ", accuracy:" + str(t_acc))
                print(str(step) + ": valid --->" + "cost:" + str(v_cost) + ", accuracy:" + str(v_acc))
                print("----------------------------------------")
                
            if step % 10000 == 0 and step != 0:
                saver.save(sess, 'model/deepid%d.ckpt' % step)
                
            step += 1
            
        safe_file_close(t_pkl_file)
        safe_file_close(v_pkl_file)

if __name__ == "__main__":
    run()