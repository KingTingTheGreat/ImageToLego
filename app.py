from flask import Flask, render_template, request, send_file
from Converter import Converter
from LegofiedImage import LegofiedImage, LEGO_COLORS, BRICKLINK_COLORS, PART_NUMBERS
import os

app = Flask(__name__, static_folder='static')

c = Converter()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = c.convert(request.files['image'], int(request.form['length']), True)
        image.draw()
        return send_file('static/{}.html'.format(image.name), mimetype='text/html')
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
