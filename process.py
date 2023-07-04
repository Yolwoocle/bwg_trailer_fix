from PIL import Image, ImageDraw
from tqdm import tqdm 
from math import *

# ____CHANGE THESE:____

## How many frames the video contains.
num_frames = 1705

## The original resolution of the video.
source_w = 1280
source_h = 1280
target_w = 128
target_h = 128

## The size in real pixels of a metapixel in your video.
## In this case, it's 10
metapixel_size = floor(source_w / target_w)

## Affects how many pixels are sampled. 
## Ex: If metapixel_size = 10 and sample_offset = 3, pixels within a metapixel will 
## be sampled within a rectangle from (3, 3) to (6, 6) 
sample_offest = 3

## The color palette you wish to use.
palette = [
    (0x00, 0x00, 0x00),
    (0x11, 0x1d, 0x35), # This is not the original PICO-8 dark blue, use (0x1d, 0x2b, 0x53) if you wish to use the original PICO-8 palette.
    (0x7E, 0x25, 0x53),
    (0x00, 0x87, 0x51),
    (0xAB, 0x52, 0x36),
    (0x5F, 0x57, 0x4F),
    (0xC2, 0xC3, 0xC7),
    (0xFF, 0xF1, 0xE8),
    (0xFF, 0x00, 0x4D),
    (0xFF, 0xA3, 0x00),
    (0xFF, 0xEC, 0x27),
    (0x00, 0xE4, 0x36),
    (0x29, 0xAD, 0xFF),
    (0x83, 0x76, 0x9C),
    (0xFF, 0x77, 0xA8),
    (0xFF, 0xCC, 0xAA),
]

def col_dist_eucl(c1, c2):
    dr = c2[0] - c1[0]
    dg = c2[1] - c1[1]
    db = c2[2] - c1[2]
    return dr*dr + dg*dg + db*db

def col_dist(c1, c2):
    # https://en.wikipedia.org/wiki/Color_difference
    rbar = (c1[0] + c2[0])
    dr = c2[0] - c1[0]
    dg = c2[1] - c1[1]
    db = c2[2] - c1[2]
    rcomp = (2 + rbar/256) * dr*dr
    gcomp = 4 * dg*dg
    bcomp = (2 + (255-rbar)/256)*db*db
    return rcomp + gcomp + bcomp

def get_closest_color(col):
    closest_cols = []
    closest_dist = 999_999_999_999
    for pal_col_i in range(len(palette)):
        pal_col = palette[pal_col_i]
        d = col_dist(pal_col, col)
        if d <= closest_dist:
            closest_dist = d
            if d == closest_cols:
                closest_cols.append(pal_col_i)
            else: 
                closest_cols = [pal_col_i]
    
    return closest_cols, closest_dist

def metapixel_get_mostest_closest_color(img, ix, iy):
    inf = float("inf")
    num_close = [0 for _ in range(16)]
    
    for jx in range(sample_offest, metapixel_size-sample_offest):
        for jy in range(sample_offest, metapixel_size-sample_offest):
            img_x = ix*metapixel_size + jx
            img_y = iy*metapixel_size + jy
            pixel_color = img.getpixel((img_x, img_y))
            closest_colors, dist = get_closest_color(pixel_color)            
            for c in closest_colors:
                num_close[c] += 1
    
    max_i = 0
    for i in range(1, len(num_close)):
        if num_close[i] > num_close[max_i]:
            max_i = i
    
    if max_i == -1:
        raise Exception("color -1 found")
    return palette[max_i]


def metapixel_get_closest_average_color(img, ix, iy):
    avg_col = [0, 0, 0]
    
    for jx in range(metapixel_size):
        for jy in range(metapixel_size):
            img_x = ix*metapixel_size + jx
            img_y = iy*metapixel_size + jy
            pixel_color = r, g, b = img.getpixel((img_x, img_y))
            avg_col[0] += r
            avg_col[1] += g
            avg_col[2] += b

    v = metapixel_size*metapixel_size
    avg_col[0] /= v
    avg_col[1] /= v
    avg_col[2] /= v
    
    closest_cols, closest_dist = get_closest_color(avg_col)
    if len(closest_cols) > 1:
        print(f"Warning: more than 1 best color : {closest_cols}")
    return palette[closest_cols[0]]
    

def main1():
    for i_frame in tqdm(range(num_frames)):
        name = ("0000"+str(i_frame))[-4:]
        img = Image.open(f"source/{name}.png")
        rgb_img = img.convert('RGB')
        
        new_img = Image.new("RGB", (128, 128), (255, 255, 255)) 
        draw = ImageDraw.Draw(new_img)

        for ix in range(128):
            for iy in range(128):
                col = metapixel_get_closest_average_color(rgb_img, ix, iy)
                draw.point((ix, iy), fill=col)
                
        new_img.save(f"new/new_{name}.png")
        
def main():
    # Upscale the images
    for i in tqdm(range(num_frames)):
        name = ("0000"+str(i))[-4:]     
        img = Image.open(f"new/new_{name}.png").convert('RGB')
        
        fac = 5 # Scaling factor
        new_img = img.resize((128*fac, 128*fac), resample=Image.BOX)
        
        new_img.save(f"new_big/big_{name}.png")

if __name__ == "__main__":
    main()