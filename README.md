# Pixel video upscaler
## Motivation
I had a [trailer](https://www.youtube.com/watch?v=jb6uOKTxTlc&ab_channel=Yolwoocle) for one of my PICO-8 games, but it was too blurry due to compression and me exporting to a size too small. Unfortunately, I have lost the original files so I had no choice but to try to work with the compressed video I had, and try to recover the original pixels from the video.

# How to use 
This is a Python script that attempts to read the frames of a video, then for every "metapixel" tries to determine the average color there. Then it tries to find the closest color in the given palette, then outputs a frame. It's not perfect, but it's close.

Provide the frames of your video in the `source` folder, in PNG format, with names in the following format :
```
0000.png
0001.png
0002.png
0003.png
...
0275.png
...
```

Modify the variables in the `process.py` file, then run it. The outputted files are in `new`. 

[Contact me](https://yolwoocle.github.io/about.html) if you have any questions or [open an issue](https://github.com/Yolwoocle/bwg_trailer_fix/issues).
