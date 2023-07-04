import numpy as np
import time
import matplotlib.pyplot as plt
from PIL import Image

from scipy.fftpack import dct as dct_scipy
from scipy.fftpack import idct as idct_scipy

def generate_random_matrix(rows, cols):
    return np.random.random((rows, cols))

# Using scipy's dct function
def dct2_scipy(matrix):
    return dct_scipy(dct_scipy(matrix, axis=0, norm='ortho'), axis=1, norm='ortho')


def idct2_scipy(coeff_matrix):
    return idct_scipy(idct_scipy(coeff_matrix, axis=1, norm='ortho'), axis=0, norm='ortho')


# JPEG
def divide_image_into_blocks(image_path, block_size):
    
    image = Image.open(image_path)
    
    if image.mode != 'L':
        print("converting image as grayscale")
        image = image.convert('L')
    
    
    image_array = np.array(image)
    
    #print(image_array)
    
    height, width = image_array.shape
    print(height, width)
    
    
    num_blocks_height = height // block_size
    num_blocks_width = width // block_size
    
    print(num_blocks_height)
    print(num_blocks_width)
    
    
    # Initialize a list to store the image blocks
    blocks = []
    
    # Iterate over the blocks and extract each block
    for i in range(num_blocks_height):
        for j in range(num_blocks_width):
            block = image_array[i * block_size:(i + 1) * block_size,
                               j * block_size:(j + 1) * block_size]
            blocks.append(block)
    
    return blocks, num_blocks_height, num_blocks_width, image_array


def get_dct2_blocks(blocks, f, d):
    dct2_blocks = []
    
    for block in blocks:
        dct2_block = dct2_scipy(block)
        
        for i in range(0, f):
            for j in range(0, f):
                if i + j >= d:
                    dct2_block[i, j] = 0
        
        
        dct2_blocks.append(dct2_block)
        
    return dct2_blocks

def get_image(dct2_blocks, f, num_blocks_height, num_blocks_width):
    
    width_list = []
    matrix_list = []
    
    support_matrix = np.zeros((f*num_blocks_height, f*num_blocks_width))
    
    width_counter = 0
    height_counter = 0
    
    for dct2_block in dct2_blocks:
        
        image_block = idct2_scipy(dct2_block)
        
        for i in range(0, f):
            for j in range(0, f):
                image_block[i, j] = round(image_block[i, j])
                image_block[i, j] = max(image_block[i, j], 0)
                image_block[i, j] = min(image_block[i, j], 255)
                
        support_matrix[height_counter:height_counter+f, width_counter:width_counter+f] = image_block
        
        
        width_counter+=f
        
        if width_counter >= f*num_blocks_width:
            width_counter = 0
            height_counter+=f
            
    
    return support_matrix

def get_jpeg(image_path, f, d):
    blocks, num_blocks_height, num_blocks_width, image = divide_image_into_blocks(image_path, f)


    dct2_blocks = get_dct2_blocks(blocks, f, d)

    image_matrix = get_image(dct2_blocks, f, num_blocks_height, num_blocks_width)

    image_name = image_path.split("\\")[-1]

    pic = Image.fromarray(image_matrix).convert('L')
    jpeg_path = f"data/output/{image_name}"
    pic.save(jpeg_path)

    return jpeg_path
    
