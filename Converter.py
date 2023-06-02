import numpy as np
from PIL import Image
from tqdm import tqdm
from LegofiedImage import LegofiedImage, LEGO_COLORS, BRICKLINK_COLORS, PART_NUMBERS

class Converter:

    def __init__(self, use_lego=True):
        self.colors:dict[str, str] = LEGO_COLORS if use_lego else BRICKLINK_COLORS
        
    def find_closest_color(self, target:str) -> str:
        """ returns key corresponding to closest color to target in self.colors """
        closest_color:str = ''
        closest_distance:float = 500  # two colors can't be more than 441 apart
        for color in self.colors:
            distance:float = self.color_distance(color, target)
            if distance < closest_distance:
                closest_color = color
                closest_distance = distance
        return closest_color
    
    def color_distance(self, color1:str, color2:str) -> float:
        """ returns the euclidean distance between two hexcode colors """
        color1 = np.array([int(color1[i:i+2], 16) for i in range(1, 6, 2)])
        color2 = np.array([int(color2[i:i+2], 16) for i in range(1, 6, 2)])
        diff = color1 - color2
        return np.sqrt(np.dot(diff.T, diff))

    def convert(self, path:str, length:int, progress_bar=False, resampling_func=Image.Resampling.BILINEAR) -> LegofiedImage:        
        image = Image.open(path, mode='r')
        l, h = image.size
        height = int((length/l)*h)

        im = image.resize((length, height), resample=resampling_func)

        iter = range(height) if not progress_bar else tqdm(range(height))
        results = []
        for i in iter:
            row = []
            for j in range(length):
                pix = im.getpixel((j, i))
                if type(pix) == int:
                    pix = (pix, pix, pix)
                row.append(self.find_closest_color('#%02x%02x%02x' % pix))
            results.append(row)
    
        return LegofiedImage(results, self.colors, path.split('/')[-1])