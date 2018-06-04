# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 21:26:31 2018

@author: shen1994
"""

import os
import random

def test_pairs_generate(test_images_list, each_k=5):
    
    test_pairs_list = []

    test_images_length = len(test_images_list)

    for people_index, people_images in enumerate(test_images_list):
        
        # 生成相同一对的脸
        for _ in range(each_k):
            same_pair = random.sample(people_images, 2)
            test_pairs_list.append((same_pair[0], same_pair[1], 1))
            
        # 生成不同一对的脸
        for _ in range(each_k):
            index_random = people_index
            while index_random == people_index:
                index_random = random.randint(0, test_images_length - 1)
            diff_one = random.choice(test_images_list[people_index])
            diff_another = random.choice(test_images_list[index_random])
            test_pairs_list.append((diff_one, diff_another, 0))
            
    return test_pairs_list

def build_dataset(source_folder):
    
    random.seed(7)
    
    label = 1
    test_pairs_dataset = []
    train_dataset, valid_dataset, test_dataset = [], [], []
    
    for people_folder in os.listdir(source_folder):
        people_images = []
        people_folder_path = source_folder + os.sep + people_folder
        for vedio_folder in os.listdir(people_folder_path):
            vedio_folder_path = people_folder_path + os.sep + vedio_folder
            for vedio_file_name in os.listdir(vedio_folder_path):
                full_path = vedio_folder_path + os.sep + vedio_file_name
                people_images.append(full_path)
        random.shuffle(people_images)
        
        if len(people_images) < 100:
            test_dataset.append(people_images)
        else:
            valid_dataset.extend(zip(people_images[0: 10], [label] * 10))
            train_dataset.extend(zip(people_images[10: 100], [label] * 90))
            
        label += 1
    
    test_pairs_dataset = test_pairs_generate(test_dataset, each_k=5)
    
    random.shuffle(train_dataset)
    random.shuffle(valid_dataset)
    random.shuffle(test_pairs_dataset)
    
    return train_dataset, valid_dataset, test_pairs_dataset
    
def save_to_csv(dataset, file_name):
    
    with open(file_name, "w") as f:
        for item in dataset:
            f.write(",".join(map(str, item)) + "\n")
            
def run():
    
    train_dataset, valid_dataset, test_dataset = build_dataset("image\\result")
    train_dataset_path = "image\\train_dataset.csv"
    valid_dataset_path = "image\\valid_dataset.csv"
    test_dataset_path = "image\\test_dataset.csv"
    save_to_csv(train_dataset, train_dataset_path)
    save_to_csv(valid_dataset, valid_dataset_path)
    save_to_csv(test_dataset, test_dataset_path)

if __name__ == "__main__":
    run()
    
        