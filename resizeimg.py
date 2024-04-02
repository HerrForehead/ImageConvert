from PIL import Image
import os

def process_image(image_path):
    # Open the image
    img = Image.open(image_path)
    
    # Check if the image is wider than it is tall
    if img.width > img.height:
        # Rotate the image 90 degrees
        img = img.transpose(Image.ROTATE_90)
    
    # Resize the image if its width is wider than 122 pixels
    if img.width > 122:
        # Calculate new height to maintain aspect ratio
        new_height = int(122 / img.width * img.height)
        img = img.resize((122, new_height))
    
    # Shorten the image if its height is greater than 250 pixels
    if img.height > 250:
        # Calculate new width to maintain aspect ratio
        new_width = int(250 / img.height * img.width)
        img = img.resize((new_width, 250))
    
    # Convert image to RGB mode if it's RGBA
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    # Get the file extension
    _, extension = os.path.splitext(image_path)
    
    # Save the processed image with the original file extension
    output_path = "./inputImage/processed_image.png"
    img.save(output_path)
