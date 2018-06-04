# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 19:39:19 2018

@author: shen1994
"""

import os
import random
from PIL import Image
from PIL import ImageEnhance

def enhance_image(image_path):
    
    image = Image.open(image_path)
    
    # 随机亮度
    enhance_image = ImageEnhance.Brightness(image)
    bright = random.uniform(0.2, 1.8)
    enhance_image = enhance_image.enhance(bright)
    
    # 随机饱和度
    enhance_image = ImageEnhance.Contrast(enhance_image)
    contrast = random.uniform(0.2, 1.8)
    enhance_image = enhance_image.enhance(contrast)
    
    # 随机左右翻转
    if random.randint(0,1) == 1:
        enhance_image = enhance_image.transpose(Image.FLIP_LEFT_RIGHT)
        
    return enhance_image

def add_image(folder_list, folder_path, max_number):
    
    folder_length = len(folder_list)
    random_folder_list = []
    
    for _ in range(max_number - folder_length):  
        index = random.randint(0, folder_length - 1)
        random_folder_list.append(folder_list[index])
    
    add_path = "add"
    full_add_path = folder_path + os.sep + add_path
    if not os.path.exists(full_add_path):
        os.mkdir(full_add_path)
    
    counter = 0
    for path in random_folder_list:
        new_image = enhance_image(path)
        new_image.save(full_add_path + os.sep + str(counter) + ".jpg")
        counter += 1

def image_augmentation(db_folder, limit_number=100, max_number=600):
    
    number = 0
    for people_folder in os.listdir(db_folder):
        number += 1
        
        src_people_path = db_folder + os.sep + people_folder
        
        counter = 0
        people_folder_list = []
        for vedio_folder in os.listdir(src_people_path):
            
            src_vedio_path = src_people_path + os.sep + vedio_folder

            for img_file in os.listdir(src_vedio_path):
                counter += 1
                src_img_path = src_vedio_path + os.sep + img_file
                people_folder_list.append(src_img_path)
        
        if counter < limit_number or counter >= max_number:
            continue
        else:
            add_image(people_folder_list, src_people_path, max_number)
            
            print(people_folder + ": id--->" + str(number) + "--->OK")

def run():
    random.seed(7)
    db_folder = "image\\origin"
    image_augmentation(db_folder)

if __name__ == "__main__":
    run()