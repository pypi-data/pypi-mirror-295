import skimage.transform import resize

def resize_image(image, proportion):
    assert 0 <= proportion <= 1, "Specify a proportion between 0 and 1!"

    img_h, img_w = image.shape[0], image.shape[1]


    height = round(img_h*proportion)
    width = round(img_w*proportion)
    resized_image = resize(image, (height, width), anti_aliasing=True)
    return resized_image
