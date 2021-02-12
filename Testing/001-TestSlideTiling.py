import os
from processing.tile_image import TileSlide
from queue import Queue
from threading import Thread
from time import time
import logging

logging.basicConfig(filename='run_global_001.log', level=logging.DEBUG)

def preprocessing():
   print("preprocessing_001 started")
   ts = time()
   slideextension1 = "mrxs"
   slideextension2 = "svs"
   datasetpath = "/opt/storage/testImageTiling/"
   outputpath = "/opt/storage/testImageTilingOutput_001/"

   os.mkdir(outputpath)

   # Preprocessing:
   queue = Queue()

   for x in range(60):
           worker = TileSlide(queue)
           # Setting daemon to True will let the main thread exit even though the workers are blocking
           worker.daemon = True
           worker.start()

   for root, dirs, files in os.walk(datasetpath, topdown=False):
      for name in files:
         if name.endswith(slideextension2):
            logging.info(name)
            print(name)
            queue.put((root, outputpath, name, 0, 4))

   queue.join()
   logging.info('Preprocessing took %s', time() - ts)
   print('Preprocessing took %s', time() - ts)

if __name__ == '__main__':
    preprocessing()