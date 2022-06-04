import cv2, cv2.aruco as aruco, numpy as np, serial, glob, time, math

def findArucoMarkers(img, markerSize = 4, totalMarkers=100, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    return aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    #bboxs, ids, rejected

# Connect with Arduino
try:
    ports = glob.glob('/dev/ttyACM*')
    ser = serial.Serial(ports[0], 9600)
except:
    print("Connect the device")
    exit()
time.sleep(2)
arucoCodeDimension = 97 #mm
focalLenght = 800#Focal Length of the camera in pixels
posX = 90
posY = 120
ser.write(("X90:Y120").encode())
message = ""
messageBefore = ""
# To capture video from webcam. 
cap = cv2.VideoCapture(0)

while True:
    # Read the frame
    img = cap.read()[1]
    center = (img.shape[1]/2, img.shape[0]/2)

    markers = findArucoMarkers(img)
    code = markers[0]
    cv2.rectangle(img, (img.shape[1]//2-50, img.shape[0]//2-50), (img.shape[1]//2+50, img.shape[0]//2+50), (0,255, 0), 2)
    if code != ():
        cv2.polylines(img,[np.int32(code[0])],True,(0,255,0), 2)
        center = (int(min(code[0][0][:,0:1:])+(max(code[0][0][:,0:1:])-min(code[0][0][:,0:1:]))//2), int(min(code[0][0][:,1:2:])+ (max(code[0][0][:,1:2:])-min(code[0][0][:,1:2:]))//2))
        cv2.circle(img, center, 1, (0,0,255), -1)
    
    #move cam right
        if center[0]>img.shape[1]/2 and center[0]-img.shape[1]/2>40:
            message = "D"
            posX = posX if posX-(center[0]-img.shape[1]/2)/45<=0 else posX-(center[0]-img.shape[1]/2)/45

        #move cam left
        elif center[0]<img.shape[1]/2 and img.shape[1]/2-center[0]>40:
            message = "A"
            posX = posX if posX+(img.shape[1]/2-center[0])/45>=180 else posX+(img.shape[1]/2-center[0])/45

        #move cam down
        if center[1]>img.shape[0]/2 and center[1]-img.shape[0]/2>50:
            posY = posY if posY-(center[1]-img.shape[0]/2)/65<=45 else posY-(center[1]-img.shape[0]/2)/65

        #move cam upword
        elif center[1]<img.shape[0]/2 and img.shape[0]/2-center[1]>50:
            posY = posY if posY+(img.shape[0]/2-center[1])/65>=150 else posY+(img.shape[0]/2-center[1])/65

        #move car foreward or backwards
        edges = []
        for i in range(len(code[0][0])):#james
            edges.append(((float(str(code[0][0][i][0])) - float(str(code[0][0][(i+1)%len(code[0][0])][0])))**2 + (float(str(code[0][0][i][1])) - float(str(code[0][0][(i+1)%len(code[0][0])][1])))**2)**0.5)
        
        #Focal Length*dimension of code(mm)/dimension of code(pixel) = distance in mm
        if (focalLenght*arucoCodeDimension/max(edges))*math.cos(math.radians(abs(posY-90)))<(750-75):
            message += "S"
            #move car backwards
        elif (focalLenght*arucoCodeDimension/max(edges))*math.cos(math.radians(abs(posY-90)))>(750+75):
            message += "W"
            #move car foreward
        else:
            message += "Q"
    else:
        message = "Q"
            
    # Stop if escape key is pressed
    key = cv2.waitKey(1)
    if key==ord("q"):
        break
    
    if key==ord(" "):
        message = "Q"
    
    if messageBefore != (message + 'X'+str(90)+':Y'+str(int(posY))) or "A" in message or "D" in message:
        messageBefore = (message + 'X'+str(90)+':Y'+str(int(posY)))
        #print(message + ' -- X'+str(90)+':Y'+str(int(posY)))
        ser.write((message + 'X'+str(90)+':Y'+str(int(posY))).encode())
    message = ""
    # Display
    cv2.imshow('img', img)
        
# Release the VideoCapture object
cap.release()
