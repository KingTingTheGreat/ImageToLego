import os
import sys
import pygame
from functools import cache
from openpyxl import Workbook


LEGO_COLORS:dict[str, str] = {\
    '#4B9F4A': 'BrightGreen', 
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
    '#A0A5A9': 'MediumStoneGrey', # light bluish gray
    '#D9D9D9': 'WhiteGlow' # glow in dark white
}
        
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
    '#D9D9D9': 'GlowInDarkWhite'
}

PART_NUMBERS:dict[str, str] = {\
    '#352100': '6322813', # dark brown
    '#6074A1': '6322842', # sand blue
    '#B3D7D1': '6322818', # aqua
    '#FE8A18': '6284582', # bright orange, orange
    '#FF698F': '6311436', # coral, vibrant coral
    '#F8BB3D': '6322822', # flame yellowish orange, bright light orange
    '#9B9A5A': '6284595', # olive green
    '#BBE90B': '6284583', # bright yellowish green, lime
    '#720E0F': '6284585', # dark red
    '#68BCC5': '6299918', # glitter trans light blue
    '#FFFFFF': '6284572', # white, glitter trans clear
    '#9FC3E9': '6322823', # light royal blue, bright light blue
    '#008F9B': '6311437', # bright bluish green, dark turquoise
    '#C870A0': '6322821', # bright purple, dark pink
    '#0A3463': '6284584', # earth blue, dark blue
    '#582A12': '6284586', # reddish brown
    '#958A73': '6322841', # sand yellow, dark tan
    '#E4ADC8': '6284587', # light purple, trans pink
    '#D09168': '6343472', # nougat
    '#AA7F2E': '6238891', # warm gold, pearl gold
    '#078BC9': '6322824', # dark azur, dark azure
    '#6C6E68': '6284596', # dark stone grey, dark bluish gray
    '#D9D9D9': '6284592', # white glow, glow in dark white
    '#36AEBF': '6322819', # medium azur, medium azure
    '#F5CD2F': '6274740', # trans yellow
    '#DF6695': '6325421	', # glitter trans dark pink
    '#A0A5A9': '6284071', # medium stone grey, light bluish gray
    '#AA7D55': '6284589', # medium nougat
    '#898788': '6238890', # silver metallic, flat silver
    '#DFEEA5': '6284598', # spring yellowish green, yellowish green
    '#923978': '6322816', # bright reddish violet, magenta
    '#A95500': '6322840', # dark orange
    '#FFF03A': '6343806', # cool yellow, bright light yellow
    '#5A93DB': '6284602', # medium blue
    '#E1D5ED': '6322820', # lavender
    '#C91A09': '6284574', # bright red, trans red
    '#0055BF': '6284575', # bright blue, blue
    '#184632': '6396247', # dark green
    '#AC78BA': '6346374', # medium lavender
    '#AEEFEC': '6274739', # trans light blue, trans blue opal
    '#E4CD9E': '6284573', # brick yellow, tan
    '#F6D7B3': '6315196', # light nougat
    '#05131D': '6284070', # black
    '#F08F1C': '6274747', # trans orange
    '#4B9F4A': '6353793', # bright green
    '#F2CD37': '6284577' # bright yellow, yellow
}

SIZE = 10
SPACING = 1

class LegofiedImage:

    def __init__(self, image:list[list[str]], colors:dict[str, str], title:str='LegofiedImage'):
        self.image:list[list[str]] = image
        self.colors:dict[str, str] = colors
        self.title:str = title
        self.length:int = len(image[0])
        self.height:int = len(image)
        self.screen_length:int = self.length*SIZE + (self.length-1)*SPACING
        self.screen_height:int = self.height*SIZE + (self.height-1)*SPACING

    @cache
    def create_image(self) -> None:
        try:
            length, height = self.length, self.height
            screen = pygame.display.set_mode((self.screen_length, self.screen_height))
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

    def image_tostring(self) -> bytes:
        screen = self.create_image()
        return pygame.image.tostring(screen, 'RGB')

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
    
    def save_parts_list(self, path=None) -> None:
        if path is None:
            path = self.title
        if not path.endswith('.xlsx'):
            path += '.xlsx'
        quantities = {}
        for i in range(len(self.image)):
            for j in range(len(self.image[i])):
                quantities[self.image[i][j]] = quantities.get(self.image[i][j], 0) + 1
        wb = Workbook()
        ws = wb.active
        for color in quantities:
            ws.append([PART_NUMBERS[color], quantities[color], color, self.colors[color]])
        wb.save(path)


