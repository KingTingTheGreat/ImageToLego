import io
import base64
from PIL import Image
from flask import Flask, render_template, request, send_file, redirect
from Converter import Converter
from LegofiedImage import LegofiedImage, LEGO_COLORS, BRICKLINK_COLORS, PART_NUMBERS

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
        legofied = C.convert_image(image, length, progress_bar=False)

        # save parts list
        legofied.save_parts_list(path='./tmp/LegofiedImage.xlsx')

        # send image to client
        image = Image.frombytes('RGB', (legofied.screen_length, legofied.screen_height), legofied.image_tostring())
        image_stream = io.BytesIO()
        image.save(image_stream, 'PNG')
        image_stream.seek(0)
        image_data = base64.b64encode(image_stream.getvalue()).decode('utf-8')


        return render_template('index.html', image_data=image_data)
    return render_template('index.html')

@app.route('/download_parts_list')
def download_parts_list():
    return send_file('tmp/LegofiedImage.xlsx', as_attachment=True)


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=False, host='0.0.0.0')
