from flask import Flask, request, redirect, url_for
import os
import subprocess

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

        # Convert the image to a 3-color BMP image
        commandimg = "convert .\inputImage\input.png -dither FloydSteinberg -define dither:diffusion-amount=85% -remap eink-3color.png BMP3:.\imgToBMP\output.bmp"
        print(commandimg)
        os.system(commandimg)
        subprocess.run(["convert", ".\inputImage\input.png", "-dither", "FloydSteinberg", "-define", "dither:diffusion-amount=85%", "-remap", "eink-3color.png", "BMP3:.\imgToBMP\output.bmp"], shell=True)        
        
        return 'File uploaded successfully!'
    
    return '''
    <!doctype html>
    <html>
    <body>
    <h1>Upload an Image</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run()
