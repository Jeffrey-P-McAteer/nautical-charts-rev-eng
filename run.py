#!/usr/bin/env python3

import os, sys, subprocess
import io
import traceback
import time

import PIL
from PIL import Image

#from xvfbwrapper import Xvfb
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

BEGIN_URL = "http://fishing-app.gpsnauticalcharts.com/i-boating-fishing-web-app/fishing-marine-charts-navigation.html"

def parse_lat_lon_from_url(url):
  parts = url.split("/")[-3:] # grab last 3 parts: lat, lon, zoom
  return float(parts[1]), float(parts[2])

def build_url_to(zoom, lat, lon):
  return BEGIN_URL+"#"+str(zoom)+"/"+str(lat)+"/"+str(lon)

if __name__ == '__main__':
  if len(sys.argv) < 6 or '-h' in sys.argv or '--help' in sys.argv:
    print("""Usage: python run.py zoom latlon_step_size lat_begin lon_begin lat_end lon_end

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

  fireFoxOptions = webdriver.FirefoxOptions()
  #fireFoxOptions.headless = True # Causes webGL to not load

  driver = webdriver.Firefox(options=fireFoxOptions)
  #driver.get(BEGIN_URL+"#"+zoom+"/"+begin_lat+"/"+begin_lon)
  begin_url = build_url_to(zoom, lat_begin, lon_begin)
  print("begin_url={}".format(begin_url))
  driver.get(begin_url)
  
  # Poll for app to have loaded...
  # while not driver.execute_script("// todo figure out what variables indicate map load"):
  #   time.sleep(0.1)
  # Neverming, "Polling"
  time.sleep(5.0)

  if not os.path.exists("output"):
    os.makedirs("output")

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

  for lat in lat_range:
    for lon in lon_range:
      # Go to URL...
      driver.get(build_url_to(zoom, lat, lon))
      driver.save_screenshot(os.path.join("output", "{}_{}_{}.png".format(zoom,lat,lon)))


  # png_data contains a .png image as a bytearray
  # which may be written to a file or stitched in-memory using PIL
  #png_data = driver.get_screenshot_as_png()

  # actions = ActionChains(driver)
  # lon_dir = 1
  # # Pan right until web URL longitude > lon_end
  # while True:
  #   curr_lat, curr_lon = parse_lat_lon_from_url(driver.current_url)
    
  #   # Check used while debugging zoom issue
  #   if not ( str(zoom) in driver.current_url or "#"+str(int(zoom)) in driver.current_url ):
  #     raise Exception("{} does not contain original zoom {}".format(driver.current_url, zoom))

  #   print("Currently at {}".format( (curr_lat, curr_lon) ))
  #   if lon_dir > 0: # aka == 1
  #     if curr_lon < lon_end:
  #       # pan in the direction of lon_dir
  #       #driver.execute_script("map.mousedown.")
  #       body_elm = driver.find_element_by_id("map")
  #       actions.drag_and_drop_by_offset(body_elm, -200.0 * lon_dir, 0.0).pause(0.5).release().perform()

  #     else:
  #       # pan down and switch direction
  #       lon_dir = -lon_dir
  #       actions.drag_and_drop_by_offset(body_elm, 0.0, 200.0).pause(0.5).release().perform()

  #   else: # lon_dir == -1
  #     if curr_lon > lon_begin:
  #       # pan in the direction of lon_dir
  #       #driver.execute_script("map.mousedown.")
  #       body_elm = driver.find_element_by_id("map")
  #       actions.drag_and_drop_by_offset(body_elm, -200.0 * lon_dir, 0.0).pause(0.5).release().perform()

  #     else:
  #       # pan down and switch direction
  #       lon_dir = -lon_dir
  #       actions.drag_and_drop_by_offset(body_elm, 0.0, 200.0).pause(0.5).release().perform()


  #   # actions.release().perform()
  #   actions.reset_actions()#.perform()

  #   time.sleep(0.25)


  # # image = Image.open(io.BytesIO(png_data))
  # # image.show()

  driver.close()
  driver.quit()





