import matplotlib.pyplot as plt

def plot_image(image):
    plt.figure(figsize=(12,4))
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show()

def plot_result(*args):
    total_images = len(args)
    fig, axis = plt.subplots(nrows=1, ncols=total_images, figsize=(12,4))
    names = [*[f'Image {i}' for i in range(1, total_images)], 'Result']
    for ax, name, image in zip(axis, names, args):
        ax.set_title(name)
        ax.imshow(image, cmap='gray')
        ax.axis('off')
    plt.tight_layout()
    plt.show()

def plot_histogram(image):
    fig, axis = plt.subplots(nrows=1, ncols=3, figsize=(12,4), sharex=True, sharey=True)
    colors = ['red', 'green', 'blue']
    for index, (ax,color  in enumerate(zip(axis, colors)):
        ax.set_title(f'{color.title()} Histogram')
        ax.hist(image[:, :, index].ravel(), bins=256, color=color, alpha=0.8)
    fig.tight_layout()
    plt.show()
