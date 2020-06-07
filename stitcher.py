#!/usr/bin/env python3

import os, sys, subprocess
import io, glob

import PIL
from PIL import Image


if __name__ == '__main__':
  if len(sys.argv) < 6 or '-h' in sys.argv or '--help' in sys.argv:
    print("""Usage: python stitcher.py zoom latlon_step_size lat_begin lon_begin lat_end lon_end
(we use the same numbers as run.py to re-match where the file names go)
""")
    sys.exit(1)

  zoom = float(sys.argv[1])
  latlon_step_size = float(sys.argv[2])
  lat_begin = float(sys.argv[3])
  lon_begin = float(sys.argv[4])
  lat_end = float(sys.argv[5])
  lon_end = float(sys.argv[6])

  print("""
zoom={}
latlon_step_size={}
lat_begin={}
lon_begin={}
lat_end={}
lon_end={}
""".format(zoom, latlon_step_size, lat_begin, lon_begin, lat_end, lon_end))

  step_size = latlon_step_size

  if lat_begin < lat_end:
    lat_range = [lat_begin]
    while lat_range[-1] < lat_end:
      lat_range.append( lat_range[-1] + step_size)
  else:
    lat_range = [lat_begin]
    while lat_range[-1] > lat_end:
      lat_range.append( lat_range[-1] - step_size)

  if lon_begin < lon_end:
    lon_range = [lon_begin]
    while lon_range[-1] < lon_end:
      lon_range.append( lon_range[-1] + step_size)
  else:
    lon_range = [lon_begin]
    while lon_range[-1] > lon_end:
      lon_range.append( lon_range[-1] - step_size)

  print("lat_range={}".format(lat_range))
  print("lon_range={}".format(lon_range))

  # We assume the images are all the same size, so we grab the first image's dimensions in pixels
  tile_w, tile_h = (None, None)
  with Image.open(os.path.join("output", "{}_{}_{}.png".format(zoom,lat_range[0],lon_range[0]))) as im:
    tile_w, tile_h = im.size
  print("tile_w={}, tile_h={}".format(tile_w, tile_h))

  mosaic_w = tile_w * len(lon_range)
  mosaic_h = tile_h * len(lat_range)
  print("mosaic_w={}, mosaic_h={}".format(mosaic_w, mosaic_h))

  mosaic_img = Image.new('RGB', (mosaic_w, mosaic_h))

  for lat_i, lat in enumerate(lat_range):
    for lon_i, lon in enumerate(lon_range):
      image_f = os.path.join("output", "{}_{}_{}.png".format(zoom,lat,lon))
      if  not os.path.exists(image_f):
        raise Exception("Required image does not exist: {}".format(image_f))
      
      with Image.open(os.path.join("output", "{}_{}_{}.png".format(zoom,lat,lon))) as im:
        mosaic_img.paste(im, (lon_i * tile_w, lat_i * tile_h))

  mosaic_img.save('output/combined_{}.png'.format(zoom))
