from django.shortcuts import render

# Create your views here.
import cv2
import numpy as np
import os

import DetectChars
import DetectPlates
import PossiblePlate
from django.http import HttpResponse, JsonResponse
# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

###################################################################################################

def homePageView(request):
    return HttpResponse('Home page')

def readPlateNumber(request, imageName):
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()  # attempt KNN training

    if blnKNNTrainingSuccessful == False:  # if KNN training was not successful
        print("\nerror: KNN traning was not successful\n")  # show error message
        return  # and exit program
    # end if

    imagePath = "D:/personal/Project Python/plateNumberImage/" + imageName
    imgOriginalScene = cv2.imread(imagePath)  # open image

    if imgOriginalScene is None:  # if image was not read successfully
        print("\nerror: image not read from file \n\n")  # print error message to std out
        #os.system("pause")  # pause so user can see error message
        data = {
            'status': 'OK',
            'plateNumber': ''
        }
        return JsonResponse(data)
        # and exit program
    # end if

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

    if len(listOfPossiblePlates) == 0:  # if no plates were found
        print("\nno license plates were detected\n")  # inform user no plates were found
        data = {
            'status': 'OK',
            'plateNumber': ''
        }
        return JsonResponse(data)
    else:  # else
        # if we get in here list of possible plates has at leat one plate

        # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
        listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)

        # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = listOfPossiblePlates[0]
        licPlate1 = listOfPossiblePlates[1]
        if len(licPlate.strChars) == 0:  # if no chars were found in the plate
            print("\nno characters were detected\n\n")  # show message
            return  # and exit program
        # end if

        print("\nlicense plate read from image = " + licPlate1.strChars + "-" + licPlate.strChars + "\n")  # write license plate text to std out
        print("----------------------------------------")
        data = {
            'status': 'OK',
            'plateNumber': licPlate1.strChars + "-" + licPlate.strChars
        }
    return JsonResponse(data)
