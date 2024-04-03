from flask import Flask, request, redirect, url_for, render_template, send_file
import os
import subprocess
from PIL import Image 

from imageSplitter import convert_black, convert_red
from resizeimg import process_image

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        # Acccept file and save it to the inputImage folder
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        allowed_extensions = ['.png', '.jpg', '.jpeg']
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            return 'Invalid file type. Only .png or .jpg/.jpeg files are allowed.'

        filename = 'input' + os.path.splitext(file.filename)[1]
        file.save(os.path.join('inputImage', filename))

        # Resize the image to the necessary size
        process_image(f"./inputImage/input"+ os.path.splitext(file.filename)[1])

        # Remove the temporary file
        os.remove(f"./inputImage/input"+ os.path.splitext(file.filename)[1])

        # Convert the image to a 3-color BMP
        commandimg = f"convert .\\inputImage\\processed_image.png -dither FloydSteinberg -define dither:diffusion-amount=85% -remap eink-3color.png -depth 4 BMP3:.\imgToBMP\output.bmp"
        os.system(commandimg)

        # Remove the temporary file
        os.remove(f".\\inputImage\\processed_image.png")

        img = Image.open(".\\imgToBMP\\output.bmp")
        img = img.convert("P", palette=Image.ADAPTIVE, colors=4)
        img.save(".\\imgToBMP\\output.bmp")

        # Copy the image to the output folder
        os.system("copy .\\imgToBMP\\output.bmp .\\output\\result.bmp")

        # Separate the image into red and black layers
        convert_red(f".\\imgToBMP\\output.bmp", ".\\output\\output_red.bmp")
        convert_black(f".\\imgToBMP\\output.bmp", ".\\output\\output_black.bmp")

        # Convert the images to 4-bit depth
        img = Image.open(".\\output\\output_red.bmp")
        img = img.convert("P", palette=Image.ADAPTIVE, colors=4)
        img.save(".\\output\\output_red.bmp")

        img = Image.open(".\\output\\output_black.bmp")
        img = img.convert("P", palette=Image.ADAPTIVE, colors=4)
        img.save(".\\output\\output_black.bmp")

        # Remove the temporary file
        os.remove(".\\imgToBMP\\output.bmp")
        
        # generate the Graphics.h file with img2hex.py
        os.system("python.exe ./img2hex.py")

        # Get the paths for the preview images and Graphics.h
        preview_red = "/output/output_red.bmp"
        preview_black = "/output/output_black.bmp"
        preview_result = "/output/result.bmp"
        graphics_h = "/downloadfile"
        
        # Pass the paths to the template
        return render_template('index.html', preview_red=preview_red, preview_black=preview_black, preview_result=preview_result, graphics_h=graphics_h)
    
    return render_template('index.html')

# Convert the image to hex
@app.route('/img2hex.html', methods=['GET', 'POST'])
def convert_to_hex():
    return render_template('img2hex.html')

# Sending the file to the user
@app.route('/downloadfile')
def download():
   return send_file('./output/Graphics.h', as_attachment=True)

# Send the preview images to the user
@app.route('/output/output_red.bmp')
def preview_red():
    return send_file('./output/output_red.bmp')

@app.route('/output/output_black.bmp')
def preview_black():
    return send_file('./output/output_black.bmp')

@app.route('/output/result.bmp')
def result():
    return send_file('./output/result.bmp')

if __name__ == '__main__':
    app.run()
