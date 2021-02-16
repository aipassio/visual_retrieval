import os
from skimage.feature import local_binary_pattern
from scipy.stats import itemfreq
from sklearn.preprocessing import normalize
import cv2
import numpy as np
from tqdm import tqdm
CHANNEL_DECODE = {
    1: 'HSV',
    0: 'BGR'
}
HISTOGRAM_OPTIONS = {
    "channel" : [0, 1], # 1: HSV, 0: BGR
    "grid" : [[1 ,1], [1, 2], [2, 1], [2,2]]
}
def histogram_intersection(h1, h2):
    # import ipdb; ipdb.set_trace()
    sm = np.concatenate((np.expand_dims(h1, 1), np.expand_dims(h2, 1)), axis = 1)
    sm = np.min(sm, axis = 1)
    # import ipdb; ipdb.set_trace()
    return sm

def l2_distance(h1, h2):
    return np.linalg.norm(h1-h2)

def naive(img):
    img = cv2.resize(img, (224,224))/255
    return img.flatten()

def lbp(img_gray, no_points = 16, radius = 4, bin = 512):
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
    radius = 4
    no_points = 9
    lpb_array = local_binary_pattern(img_gray, no_points, radius)
    lpb_array = np.histogram(lpb_array, bins=bin)
    # lpb_array = itemfreq(lpb_array.ravel())
    # Normalize the histogram
    # lpb_array = lpb_array[:, 1]/sum(lpb_array[:, 1])
    # import ipdb; ipdb.set_trace()
    # gt_array.append([int(gt_name.split("_")[0]), lpb_array[0]])
    return lpb_array[0]

def extract_hist_sub(array, row_ratio, column_ratio):
    row_uni = int(array.shape[0]/row_ratio)
    column_uni = int(array.shape[1]/column_ratio)
    resized_shape = (row_uni*row_ratio, column_ratio*column_uni)
    area_uni = row_uni*column_uni
    list_sub = []
    for row_idx in range(row_ratio):
        for column_idx in range(column_ratio):
            spatial_array = array[row_idx:(row_idx+1)*row_uni, column_idx:(column_idx+1)*column_uni]
            spatial_hist = np.histogram(spatial_array, bins=256, range = (0,255))
            # import ipdb; ipdb.set_trace()
            list_sub.append(spatial_hist[0]/area_uni)
    # import ipdb; ipdb.set_trace()
    return np.concatenate(list_sub)

def extract_histogram(img, row_ratio, column_ratio, hsv):
    if hsv == 1:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    B, G, R = img[:,:,0], img[:,:,1],img[:,:,2]
    B_array = extract_hist_sub(B, row_ratio, column_ratio)
    G_array = extract_hist_sub(G, row_ratio, column_ratio)
    R_array = extract_hist_sub(R, row_ratio, column_ratio)
    # import ipdb; ipdb.set_trace()
    return np.hstack((B_array,G_array,R_array))

def histogram(img, row_ratio=1, column_ratio=1, hsv=0, all_ = True):
    if all_:
        features_dict = dict()
        for channel_option in HISTOGRAM_OPTIONS["channel"]:
            for grid_option in HISTOGRAM_OPTIONS["grid"]:
                features_dict[CHANNEL_DECODE[channel_option]+"_"+str(grid_option[0])+"_"+str(grid_option[1])] = \
                    extract_histogram(img, grid_option[0], grid_option[1],channel_option)
        return features_dict
    else:
        return histogram(img, row_ratio, column_ratio, hsv)

def BGR_1_1(img, row_ratio=1, column_ratio=1, hsv=0):
    return extract_histogram(img, row_ratio, column_ratio, hsv)

def BGR_1_2(img, row_ratio=1, column_ratio=2, hsv=0):
    return extract_histogram(img, row_ratio, column_ratio, hsv)

def BGR_2_1(img, row_ratio=2, column_ratio=1, hsv=0):
    return extract_histogram(img, row_ratio, column_ratio, hsv)

def BGR_2_2(img, row_ratio=2, column_ratio=2, hsv=0):
    return extract_histogram(img, row_ratio, column_ratio, hsv)

def HSV_1_1(img, row_ratio=1, column_ratio=1, hsv=1):
    return extract_histogram(img, row_ratio, column_ratio, hsv)

def HSV_1_2(img, row_ratio=1, column_ratio=2, hsv=1):
    return extract_histogram(img, row_ratio, column_ratio, hsv)

def HSV_2_1(img, row_ratio=2, column_ratio=1, hsv=1):
    return extract_histogram(img, row_ratio, column_ratio, hsv)

def HSV_2_2(img, row_ratio=2, column_ratio=2, hsv=1):
    return extract_histogram(img, row_ratio, column_ratio, hsv)
    