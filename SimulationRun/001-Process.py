from multiprocessing import Lock, Process, Queue, current_process, cpu_count
import logging
import queue
import os
import json
import time
import csv
import openslide
import numpy as np
import matplotlib.pyplot as plt
from skimage import filters
from skimage import color
from tileProcessing.tile_image import TileSlide
import tflearn
import glob

import deepfocus.classificationModel3
import deepfocus.hyperparameterModel

print("Number of cpu : ", cpu_count())
logfile="00001_simulation.log"
logging.basicConfig(filename=logfile, level=logging.DEBUG)

def run_job(tasks_queue):
    while True:
        try:
            '''
                try to get task from the queue. get_nowait() function will 
                raise queue.Empty exception if the queue is empty. 
                queue(False) function would do the same task also.
            '''
            task = tasks_queue.get_nowait()
        except queue.Empty:

            break
        else:
            '''
                if no exception has been raised, add the task completion 
                message to task_that_are_done queue
            '''
            starting_time_slide = time.perf_counter()
            taskdata = json.loads(task)
            logging.info(taskdata["name"] + ": starting Calculation")

            # Run Deep Focus
            '''
            starting_time_deep_focus = time.perf_counter()
            runDeepFocus(os.path.join(taskdata["root"], taskdata["name"]), taskdata["name"], os.path.join(taskdata["outputpath"],"deepfocus"))
            stop_time_deep_focus = time.perf_counter()
            loginfo = taskdata["name"] + ": " + f"Run DeepFocus on Slide in {stop_time_deep_focus - starting_time_deep_focus:0.4f} seconds"
            print(loginfo)
            logging.info(loginfo)
            '''

            # Tile Image
            starting_time_tiling = time.perf_counter()
            tileing = TileSlide()
            tileing.tileSlide(os.path.join(taskdata["root"], taskdata["name"]), os.path.join(taskdata["outputpath"]), taskdata["name"], 0)
            stop_time_tiling = time.perf_counter()
            loginfo = taskdata["name"] + ": " + f"Run Tile on Slide in {stop_time_tiling - starting_time_tiling:0.4f} seconds"
            print(loginfo)
            logging.info(loginfo)

            stop_time_slide = time.perf_counter()
            loginfo = taskdata["name"] + ": " + f"Processed Slide in {stop_time_slide - starting_time_slide:0.4f} seconds"
            print(loginfo)
            logging.info(loginfo)
    return True

def runDeepFocus(filepath, filename, outputfile):
    params = deepfocus.hyperparameterModel.hyperparameterModel()

    outputpath = 'deepfocus/'
    outputFile = outputpath + 'ver5'
    # Model training

    tflearn.init_graph()
    g = deepfocus.classificationModel3.createModel(params)
    model = tflearn.DNN(g)
    model.load(outputFile)
    results = analyze(filepath, model, outputfile)
    logging.info(filename + ': ' + str(results[0]) + ' ' + str(results[1]))

def analyze(imgpath,model,outputfile):
    imgname=os.path.basename(imgpath)
    kernelSize=64;
    kernelStepSize=1;
    bufferVal = 8# will load kernelSize x bufferVal
    stepsize=1

    slide = openslide.open_slide(imgpath)
    #tissue detection
    thumbnail=np.array (slide.get_thumbnail((slide.level_dimensions[0][0]/64,slide.level_dimensions[0][1]/64)))
    thumbnailGray = color.rgb2gray(thumbnail)
    val = filters.threshold_otsu(thumbnailGray)
    tissueMask = thumbnailGray < max(val,0.8)
    plt.imsave('tissue.png', tissueMask) #save the thumb of tissue mask

    buffersize=kernelSize*bufferVal;
    resultMask = thumbnail.astype(np.uint8) * 0;
    if stepsize>1:
        resultMask=np.resize(resultMask,( int(resultMask.shape[0]/stepsize) , int(resultMask.shape[1]/stepsize) ,resultMask.shape[2]))
    counter1=0
    counter2=0
    expectedStep = tissueMask.shape[0] / bufferVal
    outputsVec=[]
    for i in range( 0,tissueMask.shape[0]-bufferVal,bufferVal): #Height

        curMod= i %  (bufferVal*max(5,int(expectedStep/20)))
        if curMod==0:
            print('.', end='', flush=True)
        for j in range(0,tissueMask.shape[1]-bufferVal,bufferVal): #Width

            if np.mean(tissueMask[i:i+bufferVal,j:j+bufferVal])< (8/16):  #most of them are background
                continue
            bigTile=np.array(slide.read_region((j*kernelSize,i*kernelSize),0,[buffersize,buffersize]))
            bigTile=color.rgba2rgb(bigTile)
            sz = bigTile.itemsize
            h, w,cs = bigTile.shape
            bh, bw =kernelSize,kernelSize
            shape = (int(h / bh/stepsize), int(w / bw/stepsize), bh, bw, cs)
            strides = (stepsize*w * bh * sz * cs, stepsize * sz * cs*bw, w * sz * cs, sz * cs, sz)
            blocks = np.lib.stride_tricks.as_strided(bigTile, shape=shape, strides=strides)
            blocks= blocks.reshape(blocks.shape[0]*blocks.shape[1], blocks.shape[2], blocks.shape[3], blocks.shape[4])
            predictions = model.predict(blocks)
            outputsVec=outputsVec+predictions
            qwe = np.array(predictions)
            qwe = qwe.reshape(int(h / bh/stepsize), int(w / bw / stepsize),2)
            counter1= counter1 + sum(np.array(predictions)[:,1]>0.5)
            counter2= counter2 + len(predictions)- sum(np.array(predictions)[:,1]>0.5)
            resultMask[int(i/stepsize): int((i + bufferVal)/stepsize) , int(j/stepsize): int((j+ bufferVal)/stepsize),0]=255*qwe[:,:,1]
            resultMask[int(i/stepsize): int((bufferVal+i)/stepsize) , int(j/stepsize):int((bufferVal +j)/stepsize), 1] = 255*qwe[:, :, 0]
    outputname= os.path.join(outputfile, '/' + imgname +'-f'+ str(counter2)+'-o'+ str(counter1)+'.png')
    plt.imsave(outputname, resultMask, cmap=plt.cm.gray)
    outputname2 = os.path.join(outputfile, 'output/' + imgname + '-f' + str(counter2) + '-o' + str(counter1) + '.csv')
    writeXML(outputname2, outputsVec)
    return (counter2,counter1)

def writeXML(filename,data):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def main():
    slideextension2 = "svs"
    number_of_processes = 5
    task_list = Queue()
    processes = []
    # datasetpath = "/opt/storage/testImageTiling/"
    # outputpath = "/opt/storage/testImageTilingOutput_001/"
    datasetpath = "/home/reihsr/Documents/development/TestSlides/"
    outputpath = "/home/reihsr/Documents/development/TestSlides/testoutput/"

    for root, dirs, files in os.walk(datasetpath, topdown=False):
        for name in files:
            if name.endswith(slideextension2):
                logging.info("Adding file to processing queue: " + os.path.join(root, name))
                task_list.put(json.dumps({"root":root, "outputpath": outputpath, "name": name, "logfile": logfile, "slide_level":0}))

    # creating processes
    for w in range(number_of_processes):
        p = Process(target=run_job, args=(task_list,))
        processes.append(p)
        p.start()

    # completing process
    for p in processes:
        p.join()

    return True

if __name__ == '__main__':
    main()