import os
import time
import logging
import openslide
import matplotlib.pyplot as plt
from queue import Queue
from threading import Thread
import PIL
import queue
from multiprocessing import Lock, Process, Queue, current_process, cpu_count
import json

class TileSlide():
    tileSizeX = 256
    tileSizeY = 256
    num_threads = 10
    slide = "error"
    level = 0
    json_slide = {}
    outputFolder = ""

    def __init__(self):
        print("CreateTile")
        logging.basicConfig(filename='run_002.log', level=logging.DEBUG)

    def getRed(self, redVal):
        return '#%02x%02x%02x' % (redVal, 0, 0)

    def getGreen(self, greenVal):
        return '#%02x%02x%02x' % (0, greenVal, 0)

    def getBlue(self, blueVal):
        return '#%02x%02x%02x' % (0, 0, blueVal)

    def createHistogram(self, thumbnail_histogram, outputFolder, imageNameWithoutExtension, fullImageName):
        print(fullImageName + ": Create Histogramm")
        start_time_load_slide = time.perf_counter()
        plt.figure(0)
        for i in range(0, 256):
            plt.bar(i, thumbnail_histogram[0:256][i], color=self.getRed(i), edgecolor=self.getRed(i), alpha=0.3)
        plt.savefig(os.path.join(outputFolder, str(imageNameWithoutExtension) + "_thumbnail_histogram_r.png"))
        plt.figure(1)
        for i in range(0, 256):
            plt.bar(i, thumbnail_histogram[256:512][i], color=self.getGreen(i), edgecolor=self.getGreen(i), alpha=0.3)
        plt.savefig(os.path.join(outputFolder, str(imageNameWithoutExtension) + "_thumbnail_histogram_g.png"))
        plt.figure(2)
        for i in range(0, 256):
            plt.bar(i, thumbnail_histogram[512:768][i], color=self.getBlue(i), edgecolor=self.getBlue(i), alpha=0.3)
        plt.savefig(os.path.join(outputFolder, str(imageNameWithoutExtension) + "_thumbnail_histogram_b.png"))
        plt.close()
        end_time_load_slide = time.perf_counter()
        loginfo = fullImageName + ": " + f"Create Histogramm in {end_time_load_slide - start_time_load_slide:0.4f} seconds"
        print(loginfo)
        logging.info(loginfo)

    def tileImageTile(self, imagename, iamgename_without_extension, tilePositionX, tilePositionY, slideWidth, slideHeight):
        start_time_tiling = time.perf_counter()
        json_tile = {}
        json_tile["tile"] = "x" + str(tilePositionX) + "_y" + str(tilePositionY)
        json_tile["pos_x"] = tilePositionX
        json_tile["pos_y"] = tilePositionY
        locationX = tilePositionX * self.tileSizeX
        locationY = tilePositionY * self.tileSizeY
        tileWidth = min(slideWidth, locationX + self.tileSizeX) - locationX
        tileHeight = min(slideHeight, locationY + self.tileSizeY) - locationY
        json_tile["tileWidth"] = tileWidth
        json_tile["tileHeight"] = tileHeight
        tile = self.slide.read_region((locationX, locationY), self.level, (tileWidth, tileHeight))
        tile.load()
        tile_image = PIL.Image.new("RGB", tile.size, (255, 255, 255))
        tile_image.paste(tile, mask=tile.split()[3])
        self.json_slide["tile"].append(json_tile)

        start_time_save_tiling = time.perf_counter()
        tile_image.save(os.path.join(self.outputFolder, "x" + str(tilePositionX) + "_y" + str(tilePositionY) + '.png'))
        end_time_save_tiling = time.perf_counter()
        loginfo = imagename + ": " + f"Save Tile in {end_time_save_tiling - start_time_save_tiling:0.4f} seconds"
        print(loginfo)
        logging.info(loginfo)

        '''
        start_time_save_histogram_tiling = time.perf_counter()
        tileHistogram = tile_image.histogram()
        plt.figure(0)
        for i in range(0, 256):
            plt.bar(i, tileHistogram[0:256][i], color=self.getRed(i), edgecolor=self.getRed(i), alpha=0.3)
        plt.savefig(os.path.join(self.outputFolder, "x" + str(tilePositionX) + "_y" + str(tilePositionY) + '_r.png'))
        plt.figure(1)
        for i in range(0, 256):
            plt.bar(i, tileHistogram[256:512][i], color=self.getGreen(i), edgecolor=self.getGreen(i), alpha=0.3)
        plt.savefig(os.path.join(self.outputFolder, "x" + str(tilePositionX) + "_y" + str(tilePositionY) + '_g.png'))
        plt.figure(2)
        for i in range(0, 256):
            plt.bar(i, tileHistogram[512:768][i], color=self.getBlue(i), edgecolor=self.getBlue(i), alpha=0.3)
        plt.savefig(os.path.join(self.outputFolder, "x" + str(tilePositionX) + "_y" + str(tilePositionY) + '_b.png'))

        plt.close()

        end_time_save_histogram_tiling = time.perf_counter()
        loginfo = imagename + ": " + f"Save Histogram for Tile in {end_time_save_histogram_tiling - start_time_save_histogram_tiling:0.4f} seconds"
        print(loginfo)
        logging.info(loginfo)
        '''

        tile_image.close()

    def runWorker(self, workingQueue):
        while True:
            try:
                #imagename, iamgename_without_extension, tilePositionX, tilePositionY, slideWidth, slideHeight = \
                task = workingQueue.get_nowait()
            except queue.Empty:

                break
            else:
                taskdata = json.loads(task)
                if taskdata["imagename"] is None:
                    break
                self.tileImageTile(taskdata["imagename"], taskdata["iamgename_without_extension"], taskdata["tilePositionX"], taskdata["tilePositionY"], taskdata["slideWidth"], taskdata["slideHeight"])
        return True

    def tileSlide(self, inputpath, outputpath, imagename, level):
        start_time_total = time.perf_counter()
        print(imagename + ": Stating Tiling")
        fileExtenstionPosition = imagename.rfind(".")
        iamgename_without_extension = str(imagename[:fileExtenstionPosition])
        self.outputFolder = os.path.join(outputpath,
                                    str(iamgename_without_extension) + "_" + str(self.tileSizeX) + "x" + str(
                                        self.tileSizeY))

        if not os.path.exists(self.outputFolder):
            os.makedirs(self.outputFolder)
        else:
            return

        # Load Slide
        start_time_load_slide = time.perf_counter()
        self.slide = openslide.OpenSlide(os.path.join(inputpath))
        end_time_load_slide = time.perf_counter()
        loginfo = imagename + ": " + f"Load Slide in {end_time_load_slide - start_time_load_slide:0.4f} seconds"
        print(loginfo)
        logging.info(loginfo)

        # Create Json for Slide
        self.json_slide["slide"] = imagename[:fileExtenstionPosition]
        self.json_slide["level_count"] = self.slide.level_count
        self.json_slide["dimensions"] = self.slide.dimensions
        self.json_slide["level_dimensions"] = self.slide.level_dimensions
        self.json_slide["level_downsamples"] = self.slide.level_downsamples

        # Set Export layer
        thumbnaillevellocal = level
        if thumbnaillevellocal > self.slide.level_count - 1:
            thumbnaillevellocal = self.slide.level_count - 1

        self.json_slide["thumbnail_dimensions"] = self.slide.level_dimensions[thumbnaillevellocal]
        self.json_slide["tile"] = []

        # Create Thumbnail & Histogram
        thumbnail = self.slide.get_thumbnail(self.slide.level_dimensions[self.slide.level_count - 1])
        thumbnail.load()
        thumbnail_histogram = thumbnail.histogram()
        thumbnail.save(os.path.join(self.outputFolder, str(iamgename_without_extension) + "_thumbnail.png"))

        self.createHistogram(thumbnail_histogram, self.outputFolder, iamgename_without_extension, imagename)

        slideWidth, slideHeight = self.slide.level_dimensions[level]

        tilesX = int(slideWidth / self.tileSizeX) + 1
        tilesY = int(slideHeight / self.tileSizeY) + 1

        # Multi Process

        workingQueue = Queue()
        processes = []

        for tilePositionX in range(tilesX):
            for tilePositionY in range(tilesY):
                workingQueue.put(json.dumps({"imagename":imagename, "iamgename_without_extension":iamgename_without_extension,
                                             "tilePositionX":tilePositionX, "tilePositionY":tilePositionY,
                                             "slideWidth":slideWidth, "slideHeight":slideHeight}))

        for i in range(self.num_threads):
            workerpros = Process(target=self.runWorker, args=(workingQueue,))
            processes.append(workerpros)
            workerpros.start()

        for p in processes:
            p.join()

        end_time_total = time.perf_counter()
        loginfo = imagename + ": " + f"Processed silde in {end_time_total - start_time_total:0.4f} seconds"
        print(loginfo)
        logging.info(loginfo)