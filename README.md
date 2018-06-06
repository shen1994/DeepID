# DeepID

## 0. 效果展示  
> * 训练图(极小数据测试训练)  
![image](https://github.com/shen1994/README/raw/master/images/DeepID_train.jpg)  
> * 测试图  
![image](https://github.com/shen1994/README/raw/master/images/DeepID_test.jpg)  
> * 训练曲线accuracy  
![image](https://github.com/shen1994/README/raw/master/images/DeepID_acc.jpg)  
> * 训练曲线loss  
![image](https://github.com/shen1994/README/raw/master/images/DeepID_loss.jpg)

## 1. 数据地址及工具  
> * 人脸数据下载地址: [ aligned_images_DB.tar.gz](http://www.cs.tau.ac.il/~wolf/ytfaces/)  
> * 人脸数据私人下载地址: [patch1, 密码: mor2](https://pan.baidu.com/s/18p9wnxLBmMMsNcDoH1M2Pg)   
> * 人脸数据私人下载地址: [patch2, 密码: 4eni](https://pan.baidu.com/s/1dl1VIlyzbG6BjC1SVTZXZw)   
> * 有账号密码下载地址: [用户名: wolftau, 密码: wtal997](http://www.cslab.openu.ac.il/personal/Hassner/wolftau/)  
> * 本项目测试图库: [密码: fa33](https://pan.baidu.com/s/1T9REvuxCZfG5rgaSz39vig)  
> * 已训练完的模型: [密码: dnla](https://pan.baidu.com/s/1m_587kj39tdFA2oXYts5GQ)  

## 2. 执行指令  
> * 防止数据不均衡，小于100张的用于测试，不足600的做数据扩充  
`python image_augmentation.py`  
> * 将原图剪裁，剪裁成（47 * 55）大小的图片，原图是人脸对齐的  
`python image_crop.py`
> * 将图库进行划分，保存各分块的本地地址，存储为csv文件  
`python image_split.py`  
> * 将划分后的数据保存成向量存储形式, 存储为pkl文件  
`python image_vector.py`  
> * 训练数据  
`python train.py`  
> * 在命令行输入,启动tensorboard观测曲线  
`tensorboard --logdir=log`  
> * 在浏览器中输入,显示曲线  
`http://localhost:6006/#scalars`  
> * 测试数据  
`python test.py`  

## 3. 参考链接  
> * [GITHUB代码库](https://github.com/jinze1994/DeepID1)
> * [DeepID论文](https://www.cv-foundation.org/openaccess/content_cvpr_2014/papers/Sun_Deep_Learning_Face_2014_CVPR_paper.pdf)  
