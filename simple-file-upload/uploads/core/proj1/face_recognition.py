#!/usr/bin/python
from django.conf import settings

import sys
import os
import dlib
import glob
from skimage import io

import csv
import numpy as np

predictor_path = settings.ML_ROOT + 'shape_predictor_5_face_landmarks.dat'
face_rec_model_path = settings.ML_ROOT + 'dlib_face_recognition_resnet_model_v1.dat'
faces_folder_path = settings.ML_ROOT + 'train/'

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

def preprocess():
    reps = []

    for di in os.listdir(faces_folder_path):
        print("faces_folder_path" + faces_folder_path)
        print("os.path" + os.path)
        for f in glob.glob(os.path.join(faces_folder_path+di, "*")):
            print("Processing file: {}".format(f))
            img = io.imread(f)

            dets = detector(img, 1)

            for k, d in enumerate(dets):
                shape = sp(img, d)
                face_descriptor = facerec.compute_face_descriptor(img, shape)
                reps.append((di, face_descriptor)) 

    with open(settings.ML_ROOT + 'csv/labels.csv', 'w') as csvfile:
        cs = csv.writer(csvfile)
        for i in reps:
            cs.writerow([i[0]])

    with open(settings.ML_ROOT + 'csv/reps.csv', 'w') as csvfile:
        cs = csv.writer(csvfile)
        for i in reps:
            cs.writerows([i[1]])
                        
            
        
def preprocess_img(f):
    reps = []
    img = io.imread(f)
    dets = detector(img, 1)
    for k, d in enumerate(dets):
        shape = sp(img, d)
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        reps.append((os.path.basename(f), face_descriptor)) 
        return face_descriptor



def dist(img):
    labels = []
    with open(settings.ML_ROOT + 'csv/labels.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            labels.append(row[0])   
           
    reps = []    
    with open(settings.ML_ROOT + 'csv/reps.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            rep = []
            for ro in row:
                rep.append(float(ro)) 
            reps.append(rep)
    
    img_label = os.path.basename(img)
    img_reps = preprocess_img(img)

    
    if img_reps == None:
        return "no face"

    le = np.unique(labels, return_index=True, return_counts=True)
   
    n_classes = len(le[0])
    
    l2 = 'unknown'
    for i in range(n_classes):
        start = le[1][i]
        end = start + le[2][i] 
        s = 0
        for j in range(start, end):
            dif = 0
            for k in range(len(reps[0])):
                di = (reps[j][k] - img_reps[k])**2
                dif = dif + di
            #print(dif)
            #dif = dif**0.5
            s = s + dif
        s = s/le[2][i]
        
        print(str(le[0][i]) + ':' + str(s))

        if s < 0.25:
            l2 = str(le[0][i])
            
    if l2 != 'unknown':
        print('hello ' + l2)
    else:
        print('unknown person')
    return l2
    
        



def train():
    preprocess()

def test(name, img):
    return dist(img)