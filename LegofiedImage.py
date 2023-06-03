import sys
import pygame
import pandas as pd
from functools import cache


LEGO_COLORS:dict[str, str] = {\
    '#4b9f4a': 'BrightGreen', 
    '#36AEBF': 'MediumAzur', # medium azure
    '#923978': 'BrightReddishViolet', # magenta
    '#352100': 'DarkBrown', 
    '#008F9B': 'BrightBluishGreen', # dark turquoise 
    '#0055BF': 'BrightBlue', # blue
    '#AA7D55': 'MediumNougat', 
    '#F2CD37': 'BrightYellow', # yellow
    '#C91A09': 'BrightRed', # red
    '#E4CD9E': 'BrickYellow', # tan
    '#FFFFFF': 'White', 
    '#05131D': 'Black', 
    '#0A3463': 'EarthBlue', # dark blue
    '#FFF03A': 'CoolYellow', # bright light yellow
    '#5A93DB': 'MediumBlue', 
    '#DFEEA5': 'SpringYellowishGreen', # yellowish green
    '#E4ADC8': 'LightPurple', # bright pink
    '#BBE90B': 'BrightYellowishGreen', # lime
    '#6074A1': 'SandBlue', 
    '#958A73': 'SandYellow', # dark tan
    '#A95500': 'DarkOrange', 
    '#078BC9': 'DarkAzur', # dark azure
    '#9FC3E9': 'LightRoyalBlue', # bright light blue
    '#F8BB3D': 'FlameYellowishOrange', # bright light orange
    '#C870A0': 'BrightPurple', # dark pink
    '#E1D5ED': 'Lavender', 
    '#B3D7D1': 'Aqua', 
    '#FF698F': 'VibrantCoral', # coral
    '#898788': 'SilverMetallic', # flat silver
    '#AA7F2E': 'WarmGold', # pearl gold
    '#FE8A18': 'BrightOrange', # orange
    '#F6D7B3': 'LightNougat', 
    '#6C6E68': 'DarkStoneGrey', # dark bluish gray
    '#582A12': 'ReddishBrown', 
    '#720E0F': 'DarkRed', 
    '#A0A5A9': 'MediumStoneGrey'} # light bluish gray
        
BRICKLINK_COLORS:dict[str, str] = {\
    '#05131D': 'Black', 
    '#0055BF': 'Blue', 
    '#4B9F4A': 'BrightGreen', 
    '#9FC3E9': 'BrightLightBlue', 
    '#F8BB3D': 'BrightLightOrange', 
    '#FFF03A': 'BrightLightYellow', 
    '#E4ADC8': 'TransPink', 
    '#583927': 'Brown', 
    '#FF698F': 'Coral', 
    '#078BC9': 'DarkAzure', 
    '#0A3463': 'DarkBlue', 
    '#6C6E68': 'DarkBluishGray', 
    '#352100': 'DarkBrown', 
    '#184632': 'DarkGreen', 
    '#A95500': 'DarkOrange', 
    '#C870A0': 'DarkPink', 
    '#720E0F': 'DarkRed', 
    '#958A73': 'DarkTan', 
    '#008F9B': 'DarkTurquoise', 
    '#237841': 'Green', 
    '#E1D5ED': 'Lavender', 
    '#ADC3C0': 'LightAqua', 
    '#A0A5A9': 'LightBluishGray', 
    '#9BA19D': 'LightGray', 
    '#F6D7B3': 'LightNougat', 
    '#FECCCF': 'LightPink', 
    '#BBE90B': 'Lime', 
    '#923978': 'Magenta', 
    '#36AEBF': 'MediumAzure', 
    '#5A93DB': 'MediumBlue', 
    '#AC78BA': 'MediumLavender', 
    '#AA7D55': 'MediumNougat', 
    '#FFA70B': 'MediumOrange', 
    '#EBD800': 'NeonYellow', # vibrant yellow
    '#D09168': 'Nougat', 
    '#9B9A5A': 'OliveGreen', 
    '#FE8A18': 'Orange', 
    '#FC97AC': 'Pink', 
    '#C91A09': 'TransRed', 
    '#582A12': 'ReddishBrown', 
    '#6074A1': 'SandBlue', 
    '#E4CD9E': 'Tan', 
    '#FFFFFF': 'GlitterTransClear', 
    '#F2CD37': 'Yellow', 
    '#DFEEA5': 'YellowishGreen', 
    '#635F52': 'TransBlack', 
    '#D9E4A7': 'TransBrightGreen', 
    '#FCFCFC': 'SatinTransClear', # trans clear opal
    '#0020A0': 'SatinTransDarkBlue', # trans dark blue opal
    '#DF6695': 'GlitterTransDarkPink', 
    '#84B68D': 'SatinTransBrightGreen', 
    '#AEEFEC': 'TransLightBlue', # trans blue opal
    '#C9E788': 'TransLightBrightGreen', 
    '#FCB76D': 'TransLightOrange', # trans flame yellowish orange
    '#F8F184': 'TransNeonGreen', 
    '#FF800D': 'TransNeonOrange', 
    '#DAB000': 'TransNeonYellow', 
    '#F08F1C': 'TransOrange', 
    '#A5A5CB': 'TransPurple', 
    '#F5CD2F': 'TransYellow', 
    '#E0E0E0': 'ChromeSilver', 
    '#B48455': 'FlatDarkGold', 
    '#898788': 'FlatSilver', 
    '#575857': 'PearlDarkGray', 
    '#AA7F2E': 'PearlGold', 
    '#DCBC81': 'PearlLightGold', 
    '#68BCC5': 'GlitterTransLightBlue', 
    '#DBAC34': 'MetallicGold', 
    '#D4D5C9': 'GlowInDarkOpaque', 
    '#D9D9D9': 'GlowInDarkWhite'}

PART_NUMBERS:dict[str, str] = {\
}

SIZE = 10
SPACING = 1

class LegofiedImage:

    def __init__(self, image:list[list[str]], lego_colors:dict[str, str], title:str='Legofied Image'):
        self.image:list[list[str]] = image
        self.lego_colors:dict[str, str] = lego_colors
        self.title:str = title
        self.length:int = len(image[0])
        self.height:int = len(image)

    @cache
    def create_image(self) -> None:
        try:
            length, height = self.length, self.height
            screen_width = length*SIZE + (length-1)*SPACING
            screen_height = height*SIZE + (height-1)*SPACING
            screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption(self.title)
            screen.fill((0, 0, 0))
            for i in range(height):
                for j in range(length):
                    x = j*(SIZE+SPACING) + SIZE//2 + SPACING
                    y = i*(SIZE+SPACING) + SIZE//2 + SPACING
                    pygame.draw.circle(screen, self.image[i][j], (x, y), SIZE//2)
            pygame.display.update()
        except Exception as e:
            print(e)
            print('Error: could not create image')
            print(self.image[i][j])
        return screen

    def draw(self) -> None:
        screen = self.create_image()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def save_image(self, filename=None) -> None:
        if filename is None:
            filename = self.title
        if not filename.endswith('.png'):
            filename = filename.split('.')[0] + '.png'
        screen = self.create_image()
        pygame.image.save(screen, filename)

    def save_to_textfile(self, filename=None) -> None:
        if filename is None:
            filename = self.title
        if not filename.endswith('.txt'):
            filename += '.txt'
        open(filename, 'w').close() # clear file
        with open(filename, 'w') as f:
            f.write('[[')
            for i in range(len(self.image)):
                for j in range(len(self.image[i])):
                    f.write(self.image[i][j])
                    if j != len(self.image[i]) - 1:
                        f.write(', ')
                if i != len(self.image) - 1:
                    f.write('],\n [')
            f.write(']]')
    
    def save_to_csv(self, filename=None) -> None:
        if filename is None:
            filename = self.title
        if not filename.endswith('.csv'):
            filename += '.csv'
        quantities = {}
        for i in range(len(self.image)):
            for j in range(len(self.image[i])):
                quantities[self.image[i][j]] = quantities.get(self.image[i][j], 0) + 1
        df = pd.DataFrame(quantities.items(), columns=['Color', 'Quantity'])
        df.to_csv(filename, index=False, header=False)


