import numpy as np
import skimage.color import rgb2gray
import skimage.metrics import structural_similarity
import skimage.exposure import match_histograms

def find_difference(image1, image2):
    assert image1.shape == image2.shape, "Specify 2 images with the same shape!"

    gray_image1, gray_image2 = rgb2gray(image1), rgb2gray(image2)
    (socre, difference) = structural_similarity(gray_image1, gray_image2, full=True)
    print("Similarity of the images: ", score)

    normalized_difference_image = (difference - np.min(difference))/(np.max(difference)-np.min(difference))
    return normalized_difference_image

def transfer_histogram(image1, image2):
    matched_image = match_histograms(image1, image2, multichannel=True)
    return matched_image
