# Ascii-Postcard

## Description
Ascii-Postcard is a fun project that allows users to create an Ascii Postcard using a photo you've taken on your travels. 

![image](https://github.com/ygeorgaras/Ascii-Postcard/assets/35781849/2c2fa86a-ba91-4ae3-bb99-95bf836e54ed)
![20220413_142950](https://github.com/ygeorgaras/Ascii-Postcard/assets/35781849/34cccfca-a4d6-4cb2-a317-1c1a23a5efae)

## How it works
After selecting an image from your travels, we leverage OpenCV for its Canny edge detection. This is a popular and widely used edge detection technique that aims to identify and extract the edges of objects within an image. After we split the image into chunks of pixels and calculate the average color in each chunk and add it to a map. We then use the Canny Image to create a map of all the edges to use along with a map of the average color.

At this point we are able to generate the string needed for the Ascii Postcard.


## Installation
git clone https://github.com/ygeorgaras/Ascii-Postcard.git

cd Ascii-Postcard

pip install -r ./requirements.txt





## Other Examples

![image](https://github.com/ygeorgaras/Ascii-Postcard/assets/35781849/aa156f00-cc6b-436e-8032-2bb7623f12e1) ![20220413_143227](https://github.com/ygeorgaras/Ascii-Postcard/assets/35781849/20f560ab-57bf-4dc2-92cc-502bd8521022)

![image](https://github.com/ygeorgaras/Ascii-Postcard/assets/35781849/071d7ed0-0eb7-4e3a-b265-e3da1381d8ad) ![sunset](https://github.com/ygeorgaras/Ascii-Postcard/assets/35781849/b63cb01a-790c-4c0b-8335-66ae17ed1963)


