import io
from PIL import Image
from flask import Flask, render_template, request, send_file, redirect
from Converter import Converter
from LegofiedImage import LegofiedImage, LEGO_COLORS, BRICKLINK_COLORS, PART_NUMBERS

PATH:str = 'working/legofied_image.png'

app = Flask(__name__, static_folder='static')

C = Converter()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_image = request.files['input_image'].read()
        request.files['input_image'].close()
        if not input_image:
            return redirect('/')
        image:Image = Image.open(io.BytesIO(input_image))
        length:int = int(request.form['length'])
        legofied_image:LegofiedImage = C.convert_image(image, length, progress_bar=False)
        legofied_image.save_image(filename='static/'+PATH)
        return render_template('index.html', image=PATH)
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debugpip=False, host='0.0.0.0')
