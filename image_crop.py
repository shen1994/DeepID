# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 10:30:30 2018

@author: shen1994
"""

import os
from PIL import Image

def crop_from_image(src_file, des_file, crop_size):
    
    img = Image.open(src_file, "r")
    img_width, img_height = img.size
    start_point_x = int(img_width / 4)
    start_point_y = int(img_height / 4)
    x_move = start_point_x + int(img_width / 2)
    y_move = start_point_y + int(img_height / 2)
    box = (start_point_x, start_point_y, x_move, y_move)
    img_crop = img.crop(box)
    img_resize_crop = img_crop.resize(crop_size)
    img_resize_crop.save(des_file)
    
def folder_for_crop(db_folder, result_folder, crop_size):
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    
    number = 0
    for people_folder in os.listdir(db_folder):
        number += 1
        src_people_path = db_folder + os.sep + people_folder
        des_people_path = result_folder  + os.sep + people_folder
        if not os.path.exists(des_people_path):
            os.mkdir(des_people_path)
        
        step = 0
        counter = 0
        for vedio_folder in os.listdir(src_people_path):
            step += 1
            src_vedio_path = src_people_path + os.sep + vedio_folder
            des_vedio_path = des_people_path + os.sep + vedio_folder
            if not os.path.exists(des_vedio_path):
                os.mkdir(des_vedio_path)
            for img_file in os.listdir(src_vedio_path):
                counter += 1
                src_img_path = src_vedio_path  + os.sep + img_file
                des_img_path = des_vedio_path  + os.sep + img_file
                crop_from_image(src_img_path, des_img_path, crop_size)
                
            print(people_folder + ": id--->" + str(number) 
                    + " step--->" + str(step) + " counter--->" + str(counter))
    
def run():
    db_folder = "image\\origin"
    result_folder = "image\\result"
    folder_for_crop(db_folder, result_folder, (47, 55))
    
if __name__ == "__main__":
    run()
    