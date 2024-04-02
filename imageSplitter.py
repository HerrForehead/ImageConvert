from PIL import Image

def convert_black(input_image_path, output_image_path):
    # Open the image
    img = Image.open(input_image_path)
    # Convert to RGB mode (in case it's in grayscale)
    img = img.convert('RGB')
    # Get the pixel data
    pixels = img.load()
    # Iterate through each pixel
    for i in range(img.size[0]):  # width
        for j in range(img.size[1]):  # height
            # If the pixel is red, set it to white
            if pixels[i, j][0] > pixels[i, j][1] + pixels[i, j][2]:
                pixels[i, j] = (255, 255, 255)
    # Save the modified image
    img.save(output_image_path)

def convert_red(input_image_path, output_image_path):
    # Open the image
    img = Image.open(input_image_path)
    # Convert to RGB mode (in case it's in grayscale)
    img = img.convert('RGB')
    # Get the pixel data
    pixels = img.load()
    # Iterate through each pixel
    for i in range(img.size[0]):  # width
        for j in range(img.size[1]):  # height
            # If the pixel is black, set it to white
            if pixels[i, j] == (0, 0, 0):
                pixels[i, j] = (255, 255, 255)
    # Save the modified image
    img.save(output_image_path)


