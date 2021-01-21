import os
from processing.tile_image import TileSlide
from queue import Queue
from threading import Thread
from time import time
import logging

logging.basicConfig(filename='run3.log', level=logging.DEBUG)

def preprocessing():
   ts = time()
   slideextension1 = "mrxs"
   slideextension2 = "svs"
   datasetpath = "/opt/storage/testImageTiling/"
   outputpath = "/opt/storage/testImageTilingOutput3/"

   # Preprocessing:
   queue = Queue()

   for x in range(50):
           worker = TileSlide(queue)
           # Setting daemon to True will let the main thread exit even though the workers are blocking
           worker.daemon = True
           worker.start()

   for root, dirs, files in os.walk(datasetpath, topdown=False):
      for name in files:
         if name.endswith(slideextension1) or name.endswith(slideextension2):
            logging.info(name)
            print(name)
            queue.put((root, outputpath, name, 0))
            #print(os.path.join(root, name))
            #tileSlide( root, outputpath, name, 0)

   queue.join()
   logging.info('Preprocessing took %s', time() - ts)
   print('Preprocessing took %s', time() - ts)

if __name__ == '__main__':
    preprocessing()