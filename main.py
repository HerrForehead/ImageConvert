from flask import Flask, request, redirect, url_for, render_template
import os
import subprocess
from PIL import Image 

from imageSplitter import convert_black, convert_red
from resizeimg import process_image

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the POST request has a file part
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']

        # Check if the user selected a file
        if file.filename == '':
            return redirect(request.url)

        # Check if the file has a valid extension
        allowed_extensions = ['.png', '.jpg', '.jpeg']
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            return 'Invalid file type. Only .png or .jpg/.jpeg files are allowed.'

        # Save the file to the inputImage folder with the name "input"
        filename = 'input' + os.path.splitext(file.filename)[1]
        file.save(os.path.join('inputImage', filename))

        print("1")

        # Resize image if larger than 122 x 250
        process_image(f"./inputImage/input"+ os.path.splitext(file.filename)[1])
        # Remove the original image after resizing
        os.remove(f"./inputImage/input"+ os.path.splitext(file.filename)[1])

        # Convert the image to a 3-color BMP image
        commandimg = f"convert .\\inputImage\\processed_image.png -dither FloydSteinberg -define dither:diffusion-amount=85% -remap eink-3color.png -depth 4 BMP3:.\imgToBMP\output.bmp"
        os.system(commandimg)
        # Remove the processed image after conversion
        os.remove(f".\\inputImage\\processed_image.png")

        # Change output.bmp to 4 bit depth
        img = Image.open(".\\imgToBMP\\output.bmp")
        img = img.convert("P", palette=Image.ADAPTIVE, colors=4)
        img.save(".\\imgToBMP\\output.bmp")

        # Convert images to black and red format.
        convert_red(f".\\imgToBMP\\output.bmp", ".\\output\\output_red.bmp")
        convert_black(f".\\imgToBMP\\output.bmp", ".\\output\\output_black.bmp")

        # Convert the images to 4 bit depth
        img = Image.open(".\\output\\output_red.bmp")
        img = img.convert("P", palette=Image.ADAPTIVE, colors=4)
        img.save(".\\output\\output_red.bmp")

        # Do the same for the black image
        img = Image.open(".\\output\\output_black.bmp")
        img = img.convert("P", palette=Image.ADAPTIVE, colors=4)
        img.save(".\\output\\output_black.bmp")

        # Remove the original BMP file after conversion
        os.remove(".\\imgToBMP\\output.bmp")

        # Turn output_black.bmp and output_red.bmp into byte arrays using bmp2hex
        os.system(f"powershell python.exe ./bmp2array.py ./output/output_black.bmp, ./output/output_red.bmp > ./output/Graphics.h")
        
        return 'File uploaded successfully!'
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
