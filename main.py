from Converter import Converter
from LegofiedImage import LegofiedImage, LEGO_COLORS, BRICKLINK_COLORS, PART_NUMBERS

c = Converter()
path = input('Enter path to image: ')
image:LegofiedImage = c.convert_file(path, 16*5, progress_bar=True, use_lego=False)
image.save_image()
image.draw()