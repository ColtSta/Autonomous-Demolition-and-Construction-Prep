#importing modules
from collections import deque
import cv2
import numpy as np
import imutils
import time
import serial

#Set arduino Serial connection
arduino = serial.Serial('COM6',115200)

#capturing video through webcam
cap = cv2.VideoCapture(0)

#goals for each tractor with a demo area of (3,3) on the grid.  This will be more algorithmic once this begins working
arduino.write(b'<fl>' + b'<g353132222040>')
time.sleep(.5)
arduino.write(b'<ex>' + b'<g43>')
time.sleep(.5)
arduino.write(b'<dt>' + b'<g5352>')
time.sleep(.5)

ret,img1 = cap.read()
#Set up arrays that can be appended to from both sides (deque array) to hold location points for determining direction 
pts1 = deque(maxlen = 32)
pts2 = deque(maxlen = 32)
pts3 = deque(maxlen = 32)

#Set direction and location arrays for printing on screen
(dirX1, dirY1) = ("", "")
counter1 = 0
(dX1, dY1) = (0, 0)
direction1 = ""
(dirX2, dirY2) = ("", "")
counter2 = 0
(dX2, dY2) = (0, 0)
direction2 = ""
(dirX3, dirY3) = ("", "")
counter3 = 0
(dX3, dY3) = (0, 0)
direction3 = ""

#Set numpy array for keeping track of grid location
sectorGrid = np.array([[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0]],
					  [[0,1],[1,1],[2,1],[3,1],[4,1],[5,1]],
					  [[0,2],[1,2],[2,2],[3,2],[4,2],[5,2]],
					  [[0,3],[1,3],[2,3],[3,3],[4,3],[5,3]],
					  [[0,4],[1,4],[2,4],[3,4],[4,4],[5,4]],
					  [[0,5],[1,5],[2,5],[3,5],[4,5],[5,5]]])


#Set numpy array to keep track of pixel location.  Initialized with zeros to be filled later. [xMin, xMax, yMin, yMax]
pixelGrid = np.array([[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
					  [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
					  [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
					  [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
					  [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
					  [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]])


#Set screen size constants
gridX = 480#640
gridY = 480#480

#Set offset pixel value for 6x6 grid
offsetX = int(gridX/6)
offsetY = int(gridY/6)

#Set individual grid size
boxSize = (int(gridX/6),int(gridY/6))

#Count variables for printing on screen
countX = 0
countY = 5

#Set index variables for pixelGrid information
xMin = 0
xMax = 1
yMin = 2
yMax = 3

#Iterate through 6x6 grid on the screen and set pixelGrid data 
for i in range(6): 
	for j in range(6):
		currentOrigin =(offsetX*i, offsetY*j)
		pixelGrid[i][j][xMin] = currentOrigin[0]
		pixelGrid[i][j][xMax] = currentOrigin[0] + boxSize[0]
		pixelGrid[i][j][yMin] = gridY - offsetY - currentOrigin[1]
		pixelGrid[i][j][yMax] = gridY - offsetY - currentOrigin[1] + boxSize[1]	


# Determine Demo Locations from user ==========================================================================================================================
#==============================================================================================================================================================

#boolean to determine when to move on to main program
ready = False

#boolean to determine if demo location has been set by user
getNumGrid = False

#Initialize variables for demo area
demoAreaX = []
demoAreaY = []
xPixelMin = []
xPixelMax = []
yPixelMin = []
yPixelMax = []

#Create opencv window to display chosen demo area
cv2.namedWindow("Demo Area", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Demo Area", 1350, 680)

#Get demo location from user and print it on screen for confirmation
while not ready:
	
	#Take a picture
	_, img1 = cap.read()
	
	#If demo area has not been set, print grid to the screen
	if not getNumGrid and not ready:
		countX = 0
		countY = 5
		for i in range(6): 
			for j in range(6):
				currentOrigin =(offsetX*i, offsetY*j)
				img1 = cv2.rectangle(img1, currentOrigin, (currentOrigin[0]+boxSize[0],currentOrigin[1]+boxSize[1]),(0,255,255),1)
				img1 = cv2.putText(img1,"{}-{}".format(countX,countY),(currentOrigin[0],currentOrigin[1]+20),cv2.FONT_HERSHEY_COMPLEX_SMALL,.5,(0,255,255),1)
				countY-=1
			countX+=1
			countY=5
	
	cv2.imshow("Demo Area", img1)
	cv2.waitKey(5)
	
	#If demo area has not been set, ask user for information
	if not getNumGrid:
		numGrid = int(input("HOW MANY GRID LOCATIONS TO DEMO "))
		for i in range(0,numGrid):
			#Get x and y coordinates for each demo area specified
			demoAreaX.append(int(input("Demolition x Coordinate {}: ".format(i + 1))))
			demoAreaY.append(int(input("Demolition y Coordinate {}: ".format(i + 1))))
			
			#Set pixel locations for demo area based on pixelGrid values
			xPixelMin.append(pixelGrid[demoAreaX[i]][demoAreaY[i]][xMin])
			xPixelMax.append(pixelGrid[demoAreaX[i]][demoAreaY[i]][xMax])
			yPixelMin.append(pixelGrid[demoAreaX[i]][demoAreaY[i]][yMin])
			yPixelMax.append(pixelGrid[demoAreaX[i]][demoAreaY[i]][yMax])
		getNumGrid = True
	
	countX = 0
	countY = 5
	
	#Rewrite grid on screen with x's through grid locations to demo
	for i in range(6): 
			for j in range(6):
				currentOrigin =(offsetX*i, offsetY*j)
				img1 = cv2.rectangle(img1, currentOrigin, (currentOrigin[0]+boxSize[0],currentOrigin[1]+boxSize[1]),(0,255,255),1)
				img1 = cv2.putText(img1,"{}-{}".format(countX,countY),(currentOrigin[0],currentOrigin[1]+20),cv2.FONT_HERSHEY_COMPLEX_SMALL,.5,(0,255,255),1)
				for k in range(len(demoAreaX)):
					img1 = cv2.line(img1,(xPixelMin[k],yPixelMin[k]),(xPixelMax[k],yPixelMax[k]), (0,0,255), 2)
					img1 = cv2.line(img1,(xPixelMin[k],yPixelMax[k]),(xPixelMax[k],yPixelMin[k]), (0,0,255), 2)
					cv2.imshow("Demo Area", img1)
					cv2.waitKey(5)
				countY-=1
			countX+=1
			countY=5
	#Check to see if demo area is correct
	g2g = input("PRESS ENTER TO CONTINUE: ")
	
	#If "enter" is pressed, move on to main program
	if g2g == "":
		ready = True
		cv2.destroyAllWindows()
		break
	#If anythin else is pressed, reset values and begin again
	else:
		ready = False
		getNumGrid = False
		demoAreaX = []
		demoAreaY = []
		xPixelMin = []
		xPixelMax = []
		yPixelMin = []
		yPixelMax = []
	

	
# Start tracking and running Autonomous Demolition and Construction Prep=======================================================================================
#==============================================================================================================================================================
gridLocation1 = sectorGrid[5][5]
gridLocation2 = sectorGrid[5][5]
gridLocation3 = sectorGrid[5][5]

#Phase variables for each vehicle to determine which task to perform
phaseOne = [True,True,True]
phaseTwo = [False,False,False]
phaseThree = [False,False,False]
phaseFour = [False,False,False]

#dummy function to pass in to createTrackbar function
def nothing(x):
    pass
# Creating windows for RED, BLUE, and YELLOW HSV values
cv2.namedWindow('RED HSV')
cv2.resizeWindow('RED HSV',300,300)
cv2.namedWindow('BLUE HSV')
cv2.resizeWindow('BLUE HSV',300,300)
cv2.namedWindow('YELLOW HSV')
cv2.resizeWindow('YELLOW HSV',300,300)
# Starting with 100's to prevent error while masking
h,s,v = 100,100,100

# Create trackbars for each HSV value
cv2.createTrackbar('h_lower', 'RED HSV',119,179,nothing)
cv2.createTrackbar('s_lower', 'RED HSV',112,255,nothing)
cv2.createTrackbar('v_lower', 'RED HSV',127,255,nothing)
cv2.createTrackbar('h_upper', 'RED HSV',179,179,nothing)
cv2.createTrackbar('s_upper', 'RED HSV',255,255,nothing)
cv2.createTrackbar('v_upper', 'RED HSV',255,255,nothing)

cv2.createTrackbar('h_lower', 'BLUE HSV',0,179,nothing)
cv2.createTrackbar('s_lower', 'BLUE HSV',202,255,nothing)
cv2.createTrackbar('v_lower', 'BLUE HSV',164,255,nothing)
cv2.createTrackbar('h_upper', 'BLUE HSV',144,179,nothing)
cv2.createTrackbar('s_upper', 'BLUE HSV',255,255,nothing)
cv2.createTrackbar('v_upper', 'BLUE HSV',255,255,nothing)

cv2.createTrackbar('h_lower', 'YELLOW HSV',40,179,nothing)
cv2.createTrackbar('s_lower', 'YELLOW HSV',139,255,nothing)
cv2.createTrackbar('v_lower', 'YELLOW HSV',137,255,nothing)
cv2.createTrackbar('h_upper', 'YELLOW HSV',88,179,nothing)
cv2.createTrackbar('s_upper', 'YELLOW HSV',255,255,nothing)
cv2.createTrackbar('v_upper', 'YELLOW HSV',255,255,nothing)

#Set temporary grid locations to check when tractors cross into new grid location
gridTemp1 = sectorGrid[0][0]
gridTemp2 = sectorGrid[0][0]
gridTemp3 = sectorGrid[0][0]

#Boolean to be set true when vehicle changes locations
sendLocation1 = False
sendLocation2 = False
sendLocation3 = False

#Variables for tasks
global excavate
global dump
global p2Reverse
p2Reverse = True
dump = False
excavate = False

while(1):
	#Take picture
	_, img = cap.read()
	
	#convert frame(img i.e RGB) to HSV (hue-saturation-value)
	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	
	#Get hsv values from track bars
	REDh_lower = cv2.getTrackbarPos('h_lower','RED HSV')
	REDs_lower = cv2.getTrackbarPos('s_lower','RED HSV')
	REDv_lower = cv2.getTrackbarPos('v_lower','RED HSV')
	REDh_upper = cv2.getTrackbarPos('h_upper','RED HSV')
	REDs_upper = cv2.getTrackbarPos('s_upper','RED HSV')
	REDv_upper = cv2.getTrackbarPos('v_upper','RED HSV')
	
	BLUEh_lower = cv2.getTrackbarPos('h_lower','BLUE HSV')
	BLUEs_lower = cv2.getTrackbarPos('s_lower','BLUE HSV')
	BLUEv_lower = cv2.getTrackbarPos('v_lower','BLUE HSV')
	BLUEh_upper = cv2.getTrackbarPos('h_upper','BLUE HSV')
	BLUEs_upper = cv2.getTrackbarPos('s_upper','BLUE HSV')
	BLUEv_upper = cv2.getTrackbarPos('v_upper','BLUE HSV')
	
	YELLOWh_lower = cv2.getTrackbarPos('h_lower','YELLOW HSV')
	YELLOWs_lower = cv2.getTrackbarPos('s_lower','YELLOW HSV')
	YELLOWv_lower = cv2.getTrackbarPos('v_lower','YELLOW HSV')
	YELLOWh_upper = cv2.getTrackbarPos('h_upper','YELLOW HSV')
	YELLOWs_upper = cv2.getTrackbarPos('s_upper','YELLOW HSV')
	YELLOWv_upper = cv2.getTrackbarPos('v_upper','YELLOW HSV')
	
	#defining the range of RED
	red_lower = np.array([REDh_lower,REDs_lower,REDv_lower],np.uint8)
	red_upper = np.array([REDh_upper,REDs_upper,REDv_upper],np.uint8)
	
	#defining the range of BLUE 
	blue_lower = np.array([BLUEh_lower,BLUEs_lower,BLUEv_lower],np.uint8)
	blue_upper = np.array([BLUEh_upper,BLUEs_upper,BLUEv_upper],np.uint8)
	
	#defining the range of the YELLOW
	yellow_lower = np.array([YELLOWh_lower,YELLOWs_lower,YELLOWv_lower],np.uint8)
	yellow_upper = np.array([YELLOWh_upper,YELLOWs_upper,YELLOWv_upper],np.uint8)
	
	#finding the range of RED,BLUE, and YELLOW in the image
	red = cv2.inRange(hsv, red_lower, red_upper)
	blue = cv2.inRange(hsv, blue_lower, blue_upper)
	yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
	
	#Morphological transformation, Dilation... ???
	kernal = np.ones((5, 5), "uint8")
	
	red = cv2.dilate(red, kernal)
	res = cv2.bitwise_and(img, img, mask = red)
	
	blue = cv2.dilate(blue, kernal)
	res1 = cv2.bitwise_and(img, img, mask = blue)
	
	yellow = cv2.dilate(yellow, kernal)
	res2 = cv2.bitwise_and(img, img, mask = yellow)
	
	#Tracking RED-----------------------------------------------------------------------------------------------------------------------------------------Red
	#Find the contours based on the image of RED
	(_,contours, hierarchy) = cv2.findContours(red, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	#If RED is seen and there are contours found...
	if len(contours) > 0:
		#find the largest contour in the image 
		c = max(contours, key = cv2.contourArea)
		#Set x, y, and radius of the smallest enclosing circle of the largest contour in the image
		((x,y), radius) = cv2.minEnclosingCircle(c)
		#Find the center of mass of the contour object... ???
		M = cv2.moments(c)
		center1 = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		
		#If an object is seen and has a radius larger than 10...
		if radius > 10:
			# draw the circle and centroid on the frame, then update the list of tracked points
			cv2.circle(img, (int(x), int(y)), int(radius), (0, 0, 255), 2)
			cv2.circle(img, center1, 5, (0, 0, 255), -1)
			pts1.appendleft(center1)
			
			#Iterate through each grid locations pixel data, check it against the center of the tracked object.  When the center of the object is within 
			#a certain pixel grids area, the objects grid location is set 
			flCount = 0
			for i in range(6):
				for j in range(6):
					if center1[0] >= pixelGrid[i][j][xMin] and center1[0] <= pixelGrid[i][j][xMax] and center1[1] >= pixelGrid[i][j][yMin] and center1[1] <= pixelGrid[i][j][yMax]:
						gridLocation1 = sectorGrid[j][i]
						#If the grid location is different from previous the grid location, update grid location and send it to arduino
						if gridTemp1[0] != gridLocation1[0] or gridTemp1[1] != gridLocation1[1]:
							gridTemp1 = gridLocation1
							sendLocation1 = True
							
			for i in np.arange(1, len(pts1)):
				(dirX1, dirY1) = ("", "")
							
				cv2.putText(img, "{}".format(gridLocation1), (500, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
				
				flCount += 1
	
	if sendLocation1:
		#Phase One =========================================================================================================================
		if phaseOne[0]:
					
			if str(gridLocation1[0]) == str(demoAreaX[0]) and str(gridLocation1[1]) == str(demoAreaY[0]):
				phaseOne[0] = False
				dump = True
				arduino.write(b'<fl>' + b'<w>') 
				phaseTwo[0] = True
				print("Phase 1 FL complete")
					
		#===================================================================================================================================
					
		#Phase Two =========================================================================================================================
		elif phaseTwo[0]:
				
			if str(gridLocation1[0]) == str(demoAreaX[0]) and str(gridLocation1[1]) == str(1) and phaseTwo[0]:
				phaseTwo[0] = False
				phaseThree[0] = True
				arduino.write(b'<fl>' + b'<w>') # if phase one is complete, get to prep location for phase two and wait ('w')
				print("Phase Two FL Complete")
		#===================================================================================================================================
		
		arduino.write(b'<fl>' + b'<' + str(gridLocation1[0]).encode() + str(gridLocation1[1]).encode() + b'>') # + str(xGoal1).encode() + str(yGoal1).encode() + b'>')
		sendLocation1 = False
	
	
	#Tracking Excavator ------------------------------------------------------------------------------------------------------------------------------------EX
	(_,contours, hierarchy) = cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	if len(contours) > 0:
		c = max(contours, key = cv2.contourArea)
		((x,y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center2 = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10:
			# draw the circle and centroid on the frame, then update the list of tracked points
			cv2.circle(img, (int(x), int(y)), int(radius), (255, 0, 0), 2)
			cv2.circle(img, center2, 5, (255, 0, 0), -1)
			pts2.appendleft(center2)
			
			for i in range(6):
				for j in range(6):
					if center2[0] >= pixelGrid[i][j][xMin] and center2[0] <= pixelGrid[i][j][xMax] and center2[1] >= pixelGrid[i][j][yMin] and center2[1] <= pixelGrid[i][j][yMax]:
						gridLocation2 = sectorGrid[j][i]
						if gridTemp2[0] != gridLocation2[0] or gridTemp2[1] != gridLocation2[1]:
							gridTemp2 = gridLocation2
							sendLocation2 = True
							
			for i in np.arange(1, len(pts2)):
				(dirX2, dirY2) = ("", "")
				
				cv2.putText(img, "{}".format(gridLocation2), (500, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
			
			counter2 += 1
			
	if sendLocation2:
		
		#Phase One =========================================================================================================================
		if phaseOne[1]:
					
			if str(gridLocation2[0]) == str(int(demoAreaX[0])+1) and str(gridLocation2[1]) == str(demoAreaY[0]):
				phaseOne[1] = False
				arduino.write(b'<ex>' + b'<w>') 
				phaseTwo[1] = True
		#===================================================================================================================================
					
		#Phase Two =========================================================================================================================
		elif phaseTwo[1]:
									
			if str(gridLocation2[0]) == str(int(demoAreaX)+1) and str(gridLocation2[1]) == str(0):
				phaseTwo[1] = False
				phaseThree[1] = True
				arduino.write(b'<ex>' + b'<w>') # if phase one is complete, get to prep location for phase two and wait ('w')
				print("Phase Two FL Complete")
		
		arduino.write(b'<ex>' + b'<' + str(gridLocation2[0]).encode() + str(gridLocation2[1]).encode() + b'>')
		sendLocation2 = False
		
	if excavate and not phaseOne[1]:
				arduino.write(b'<ex>' + b'<x>')
				excavate = False
				
	#Tracking DumpTruck-------------------------------------------------------------------------------------------------------------------------------------DT
	(_,contours,hierarchy) = cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	if len(contours) > 0:
		c = max(contours, key = cv2.contourArea)
		((x,y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center3 = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(img, center3, 5, (0, 255, 255), -1)
			pts3.appendleft(center3)
			
			for i in range(6):
				for j in range(6):
					if center3[0] >= pixelGrid[i][j][xMin] and center3[0] <= pixelGrid[i][j][xMax] and center3[1] >= pixelGrid[i][j][yMin] and center3[1] <= pixelGrid[i][j][yMax]:
						gridLocation3 = sectorGrid[j][i]
						if gridTemp3[0] != gridLocation3[0] or gridTemp3[1] != gridLocation3[1]:
							gridTemp3 = gridLocation3
							sendLocation3 = True
		
			for i in np.arange(1, len(pts3)):
				(dirX3, dirY3) = ("", "")
				cv2.putText(img, "{}".format(gridLocation3), (500,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
			counter3 += 1
	
	if sendLocation3:
		#Phase One =========================================================================================================================
		if phaseOne[2]:
					
			if str(gridLocation3[0]) == str(int(demoAreaX[0])+2) and str(gridLocation3[1]) == str(demoAreaY[0]):
				phaseOne[2] = False
				excavate = True
				arduino.write(b'<dt>' + b'<w>') 
				phaseTwo[2] = True
					
		#===================================================================================================================================
					
		#Phase Two =========================================================================================================================
		elif phaseTwo[2]:
			if str(gridLocation3[0]) == str(int(demoAreaX[0])+1) and str(gridLocation3[1]) == str(1):
				phaseTwo[2] = False
				phaseThree[2] = True
				print("Phase Two DT Complete")
		
		arduino.write(b'<dt>' + b'<' + str(gridLocation3[0]).encode() + str(gridLocation3[1]).encode() + b'>')
		sendLocation3 = False
		
	if dump and str(gridLocation1[0]) == str(demoAreaX[0]) and str(gridLocation1[1]) == str(1) and not p2Reverse:
		arduino.write(b'<dt>' + b'<d>')
		dump = False
	elif p2Reverse and dump:
		arduino.write(b'<dt>' + b'<s>')
		p2Reverse = False
		
	#Draw the grid, demolition, and dump areas on the screen
	countX = 0	
	for i in range(6): 
		for j in range(6):
			currentOrigin =(offsetX*i, offsetY*j)
			img = cv2.rectangle(img, currentOrigin, (currentOrigin[0]+boxSize[0],currentOrigin[1]+boxSize[1]),(0,255,255),1)
			img = cv2.putText(img,"{}-{}".format(countX,countY),(currentOrigin[0],currentOrigin[1]+20),cv2.FONT_HERSHEY_COMPLEX_SMALL,.5,(0,255,255),1)
			countY-=1
			for k in range(len(demoAreaX)):
					img = cv2.line(img,(xPixelMin[k],yPixelMax[k]),(xPixelMax[k],yPixelMax[k]), (0,0,255), 2)
					img = cv2.line(img,(xPixelMin[k],yPixelMin[k]),(xPixelMax[k],yPixelMin[k]), (0,0,255), 2)
					img = cv2.line(img,(xPixelMin[k],yPixelMin[k]),(xPixelMin[k],yPixelMax[k]), (0,0,255), 2)
					img = cv2.line(img,(xPixelMax[k],yPixelMin[k]),(xPixelMax[k],yPixelMax[k]), (0,0,255), 2)
					
					img = cv2.line(img,(pixelGrid[5][0][xMin],pixelGrid[5][0][yMax]),(pixelGrid[5][0][xMax],pixelGrid[5][0][yMax]), (255,0,0), 2)
					img = cv2.line(img,(pixelGrid[5][0][xMin],pixelGrid[5][0][yMin]),(pixelGrid[5][0][xMax],pixelGrid[5][0][yMin]), (255,0,0), 2)
					img = cv2.line(img,(pixelGrid[5][0][xMin],pixelGrid[5][0][yMin]),(pixelGrid[5][0][xMin],pixelGrid[5][0][yMax]), (255,0,0), 2)
					img = cv2.line(img,(pixelGrid[5][0][xMax],pixelGrid[5][0][yMin]),(pixelGrid[5][0][xMax],pixelGrid[5][0][yMax]), (255,0,0), 2)
		countX+=1
		countY=5
		

	#Open windows for main program and HSV colors
	cv2.namedWindow("Color Tracking",cv2.WINDOW_NORMAL)
	cv2.resizeWindow("Color Tracking", 1350, 680)
	cv2.imshow("Color Tracking",img)
	
	cv2.imshow("red",res)
	cv2.imshow("blue",res1)
	cv2.imshow("yellow",res2)
	if cv2.waitKey(10) & 0xFF == ord('q'):
		cap.release()
		cv2.destroyAllWindows()
		break