# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 22:19:51 2018

@author: shen1994
"""

import pickle
import numpy as np
from PIL import Image

def image_to_vector(image_path):
    with Image.open(image_path, "r") as image:
        array_image = np.array(image, dtype="float32")
        return array_image
        
def vector_counter(csv_path, size):
    
    csv_file = open(csv_path, "r")
    line = csv_file.readline()
    counter = 0
    while line:
        counter += 1
        line = csv_file.readline()
    csv_file.close()
    
    if counter % size == 0:
        return counter
    else:
        return int(counter / size + 1) * size 
        
def save_to_vector(csv_path, pkl_path, size=16):
    
    vector_number = vector_counter(csv_path, size)
    
    csv_file = open(csv_path, "r")
    pkl_file = open(pkl_path, "wb")
    
    counter = 0
    vectors_counter =0
    x, y = [], []

    pickle.dump((vector_number, size, 2), pkl_file, pickle.HIGHEST_PROTOCOL)
    
    line = csv_file.readline()
    line = line.replace(",", " ")
    
    while line:
        
        path, label = line.strip().split()
        
        x.append(image_to_vector(path))
        y.append(int(label))
        counter += 1
        vectors_counter +=1
        
        if counter == size:
              
            pickle.dump(np.asarray(x, dtype="float32"), pkl_file, pickle.HIGHEST_PROTOCOL)
            pickle.dump(np.asarray(y, dtype="int32"), pkl_file, pickle.HIGHEST_PROTOCOL)
            
            print("save vector:" + " vectors number" + "--->" + str(vector_number) 
                    + " vectors counter" + "--->" + str(vectors_counter) 
                    + " block size" + "--->" + str(counter))
            
            counter = 0
            x, y = [], []
            
        line = csv_file.readline()
        line = line.replace(",", " ")
        
    if counter != 0:
        
        if counter % size == 0:
        
            pickle.dump(np.asarray(x, dtype="float32"), pkl_file, pickle.HIGHEST_PROTOCOL)
            pickle.dump(np.asarray(y, dtype="int32"), pkl_file, pickle.HIGHEST_PROTOCOL)
            
        else:
            
            csv_file.seek(0)
            line = csv_file.readline()
            line = line.replace(",", " ")
            while line:
                path, label = line.strip().split()
                x.append(image_to_vector(path))
                y.append(int(label))
                counter += 1
                
                if counter == size:
                    pickle.dump(np.asarray(x, dtype="float32"), pkl_file, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(np.asarray(y, dtype="int32"), pkl_file, pickle.HIGHEST_PROTOCOL)
                    break
                
                line = csv_file.readline()
                line = line.replace(",", " ") 
        
        print("save vector:" + " vectors number" + "--->" + str(vector_number)
                + " vectors counter" + "--->" + str(vectors_counter) 
                + " block size" + "--->" + str(counter))
        
    csv_file.close()
    pkl_file.close()
    
def load_vector(pkl_path, vector_number):
    
    pkl_file = open(pkl_path, "rb")
    
    big_number, size, v_number = pickle.load(pkl_file)
    
    x, y = [], []

    if vector_number > big_number:
        
        for _ in range(int(big_number / size)):
            x.extend(list(pickle.load(pkl_file)))
            y.extend(list(pickle.load(pkl_file)))
            
        if big_number % size != 0:
            x.extend(list(pickle.load(pkl_file)))
            y.extend(list(pickle.load(pkl_file)))
        
        x = np.asarray(x, dtype="float32")
        y = np.asarray(y, dtype="int32")
          
        pkl_file.close()
        
        return x, y
            
    for _ in range(int(vector_number / size)):
        x.extend(list(pickle.load(pkl_file)))
        y.extend(list(pickle.load(pkl_file)))
    
    remain_number = int(vector_number % size)
    if remain_number != 0:
        x.extend(list(pickle.load(pkl_file))[0: remain_number])
        y.extend(list(pickle.load(pkl_file))[0: remain_number])
        
    x = np.asarray(x, dtype="float32")
    y = np.asarray(y, dtype="int32")
    
    pkl_file.close()
    
    return x, y
    
def load_vector_from_index(pkl_path, batch_size, index, big_number, size, pkl_file):
 
    x, y = [], []

    if index == 0 or not pkl_file:
        
        pkl_file = open(pkl_path, "rb")
        
        big_number, size, v_number = pickle.load(pkl_file)       
        if batch_size % size != 0:
            batch_size = size * int(batch_size / size)    
        index = index % big_number
        
    if batch_size >= big_number:
        
        batch_size = big_number / batch_size
        x.extend(list(pickle.load(pkl_file)))
        y.extend(list(pickle.load(pkl_file)))
            
        pkl_file.seek(0)
        
        big_number, size, v_number = pickle.load(pkl_file)
        index = 0
    
    if (index + batch_size) >= big_number:
        
        for _ in range(int((big_number - index) / size)):
            x.extend(list(pickle.load(pkl_file)))
            y.extend(list(pickle.load(pkl_file)))
            
        pkl_file.seek(0)
        
        big_number, size, v_number = pickle.load(pkl_file)
        if batch_size % size != 0: 
            batch_size = size * int(batch_size / size)    
        index = index % big_number
        
        for _ in range(int((index + batch_size - big_number) / size)):
            x.extend(list(pickle.load(pkl_file)))
            y.extend(list(pickle.load(pkl_file)))
        
    for _ in range(int(batch_size / size)):
        x.extend(list(pickle.load(pkl_file)))
        y.extend(list(pickle.load(pkl_file)))
         
    x = np.asarray(x, dtype="float32")
    y = np.asarray(y, dtype="int32")
         
    return x, y, (index + batch_size), big_number, size, pkl_file
    

def safe_file_close(pkl_file):

    if pkl_file:
        pkl_file.close()
       
def save_pair_to_vector(csv_path, pkl_path, size=16):
    
    vector_number = vector_counter(csv_path, size)
    
    csv_file = open(csv_path, "r")
    pkl_file = open(pkl_path, "wb")
    
    counter = 0
    vectors_counter = 0
    x_1, x_2, y = [], [], []

    pickle.dump((vector_number, size, 3), pkl_file, pickle.HIGHEST_PROTOCOL)
    
    line = csv_file.readline()
    line = line.replace(",", " ")
    
    while line:
        
        path_1, path_2, label = line.strip().split()
        
        x_1.append(image_to_vector(path_1))
        x_2.append(image_to_vector(path_2))
        y.append(int(label))
        counter += 1
        vectors_counter += 1
        
        if counter == size:
              
            pickle.dump(np.asarray(x_1, dtype="float32"), pkl_file, pickle.HIGHEST_PROTOCOL)
            pickle.dump(np.asarray(x_2, dtype="float32"), pkl_file, pickle.HIGHEST_PROTOCOL)
            pickle.dump(np.asarray(y, dtype="int32"), pkl_file, pickle.HIGHEST_PROTOCOL)
            
            print("save vector:" + " vectors number" + "--->" + str(vector_number) 
                    + " vectors counter" + "--->" + str(vectors_counter) 
                    + " block size" + "--->" + str(counter))
            
            counter = 0
            x_1, x_2, y = [], [], []
            
        line = csv_file.readline()
        line = line.replace(",", " ")
        
    if counter != 0:
        
        if counter % size == 0:
            pickle.dump(np.asarray(x_1, dtype="float32"), pkl_file, pickle.HIGHEST_PROTOCOL)
            pickle.dump(np.asarray(x_2, dtype="float32"), pkl_file, pickle.HIGHEST_PROTOCOL)
            pickle.dump(np.asarray(y, dtype="int32"), pkl_file, pickle.HIGHEST_PROTOCOL)   
        else:
            
            csv_file.seek(0)
            line = csv_file.readline()
            line = line.replace(",", " ")
            while line:
                path_1, path_2, label = line.strip().split()
                x_1.append(image_to_vector(path_1))
                x_2.append(image_to_vector(path_2))
                y.append(int(label))
                counter += 1
                
                if counter == size:
                    pickle.dump(np.asarray(x_1, dtype="float32"), pkl_file, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(np.asarray(x_2, dtype="float32"), pkl_file, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(np.asarray(y, dtype="int32"), pkl_file, pickle.HIGHEST_PROTOCOL)   
                    break
                
                line = csv_file.readline()
                line = line.replace(",", " ")
        
        print("save vector:" + " vectors number" + "--->" + str(vector_number) 
                + "vectors counter" + "--->" + str(vectors_counter) 
                + "block size" + "--->" + str(counter))
        
    csv_file.close()
    pkl_file.close()
    
def load_pair_vector(pkl_path, vector_number):
    
    pkl_file = open(pkl_path, "rb")
    
    big_number, size, v_number = pickle.load(pkl_file)
    
    x_1, x_2, y = [], [], []

    if vector_number > big_number:
        
        for _ in range(int(big_number / size)):
            x_1.extend(list(pickle.load(pkl_file)))
            x_2.extend(list(pickle.load(pkl_file)))
            y.extend(list(pickle.load(pkl_file)))
            
        if big_number % size != 0:
            x_1.extend(list(pickle.load(pkl_file)))
            x_2.extend(list(pickle.load(pkl_file)))
            y.extend(list(pickle.load(pkl_file)))
        
        x_1 = np.asarray(x_1, dtype="float32")
        x_2 = np.asarray(x_2, dtype="float32")
        y = np.asarray(y, dtype="int32")
          
        pkl_file.close()
        
        return x_1, x_2, y
            
    for _ in range(int(vector_number / size)):
        x_1.extend(list(pickle.load(pkl_file)))
        x_2.extend(list(pickle.load(pkl_file)))
        y.extend(list(pickle.load(pkl_file)))
    
    remain_number = int(vector_number % size)
    if remain_number != 0:
        x_1.extend(list(pickle.load(pkl_file))[0: remain_number])
        x_2.extend(list(pickle.load(pkl_file))[0: remain_number])
        y.extend(list(pickle.load(pkl_file))[0: remain_number])
        
    x_1 = np.asarray(x_1, dtype="float32")
    x_2 = np.asarray(x_2, dtype="float32")
    y = np.asarray(y, dtype="int32")
    
    pkl_file.close()
    
    return x_1, x_2, y
        
def run():
    
    print("---------------------------------\n")
    print("write in train--->waiting\n")
    save_to_vector("image/train_dataset.csv", "image/train_vector_dataset.pkl", size=32)
    
    print("---------------------------------\n")
    print("write in valid--->waiting\n")
    save_to_vector("image/valid_dataset.csv", "image/valid_vector_dataset.pkl", size=32)
    
    print("---------------------------------\n")
    print("write in test--->waiting\n")
    save_pair_to_vector("image/test_dataset.csv", "image/test_vector_dataset.pkl", size=32)
    
    print("---------------------------------\n")
    print("write in all--->OK\n")

if __name__ == "__main__":
    run()
    