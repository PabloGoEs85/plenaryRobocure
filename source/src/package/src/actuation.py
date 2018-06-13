#!/usr/bin/env python
#print("Python: Actuation node")
import rospy
import random
import qi
import sys
import time
import os
#import functools
import actionlib
import threading

from package.srv import *

#def play_video(session, url): 
#	try:
#		print("Playing video... " + url)
		#tabletService = session.service("ALTabletService")
		#tabletService.enableWifi()
		#result = tabletService.playVideo(url)      
#	except Exception, e:
#		print "Error occured: ", e


#def moveForward(session, speed):
#	x = 1.0
#	y = 0.0
#	theta = 0.0
#	try:
#		print("Moving forwards")
#		moveService = session.service("ALMotion")
#		moveService.moveToward(x, y, theta, [["Frequency", speed]])
#		time.sleep(3)
#		moveService.stopMove()
#	except Exception, e:
#		print "Error occured: ", e
#
#def moveBack(session, speed):
#	x = 1.0
#	y = 0.0
#	theta = -1.0
#	try:
#		print("Moving backwards")
#		moveService = session.service("ALMotion")
#		moveService.moveToward(x, y, theta, [["Frequency", speed]])
#		time.sleep(3)
#		moveService.stopMove()
#	except Exception, e:
#		print "Error occured: ", e


#speaks with animations
def speak(text, profile):
	global robotSpeaks
	if (profile ==-1.0): #fully introvert
		speed = 80
		volume = 0.5
		pitch = 0.8
	elif (profile == -0.5): #slightly introvert
		speed = 90
		volume = 0.6
		pitch = 0.8
	elif (profile == 0.0): #ambivert
		speed = 100
		volume = 1.0
		pitch = 0.9
	elif (profile == 0.5): #slightly extrovert
		speed = 120
		volume = 1.0
		pitch = 1.1
	elif (profile == 1.0): #fully extrovert
		speed = 125
		volume = 1.0
		pitch = 1.1 
	
	try:
		print("Saying... " + text)
		sayAnimatedService = session.service("ALAnimatedSpeech")
		sayService = session.service("ALTextToSpeech")		
   		
		sayService.setParameter("pitchShift",pitch) #[1,4]
		sayService.setParameter("speed",speed) #[50,400]
		#sayService.resetSpeed() 
		sayService.setVolume(volume) 
		sayService.say("Hi! I am Pepper. Do you need any help?")   	

		#sayAnimatedService.say("hey there, I'm a social robot")   

		robotSpeaks = True
	except Exception, e:
		print "Error occured: ", e   

#sets idle motion
def idleMotion(profile, finish):
	
	motion_service = session.service("ALMotion")
	if(finish == True):
		print "finishing idleMotion"
		motion_service.setIdlePostureEnabled("Body", False)		
		motion_service.setIdlePostureEnabled("Arms", False)	
		motion_service.setIdlePostureEnabled("Head", False)	
	else:
		aux = random.random()
		if(profile == -1.0): #fully introvert
			print "idleMotion fully introvert. Breath"
			motion_service.setBreathEnabled("Body", False)		
			motion_service.setBreathEnabled("Arms", True)
			motion_service.setBreathEnabled("Head", False)
		elif(profile == -0.5): #slightly introvert
			print "idleMotion slightly introvert. Breath"
			motion_service.setBreathEnabled("Body", True)		
			motion_service.setBreathEnabled("Arms", True)
			motion_service.setBreathEnabled("Head", False)
		elif(profile == 0.0): #ambivert
			print "idleMotion ambivert. Breath"
			motion_service.setBreathEnabled("Body", True)		
			motion_service.setBreathEnabled("Arms", True)
			motion_service.setBreathEnabled("Head", True)
		elif(profile == 0.5): #slightly extrovert
			print "idleMotion slightly extrovert. Breath"
			motion_service.setBreathEnabled("Body", True)		
			motion_service.setBreathEnabled("Arms", True)
			motion_service.setBreathEnabled("Head", True)
		elif(profile == 1.0): #fully extrovert
			print "idleMotion fully extrovert. Breath"
			motion_service.setBreathEnabled("Body", True)		
			motion_service.setBreathEnabled("Arms", True)
			motion_service.setBreathEnabled("Head", True)


#tracks attention
def attentionTracker(profile, finish):
	awarenessService = session.service("ALBasicAwareness")
	if (finish == True):
		print "finishing attentionTracker"
		awarenessService.setEnabled(False) #for naoqi2.5
#		awarenessService.stopAwareness() #naoqi 2.1
		posture_service = session.service("ALRobotPosture")
		posture_service.goToPosture("Crouch", 0.7)
	else:
		if (profile == -1.0): #Fully introvert
			print "attentionTracker fully introvert"
			awarenessService.setParameter("LookStimulusSpeed",0.1)
			awarenessService.setParameter("LookBackSpeed",0.1)
			awarenessService.setStimulusDetectionEnabled("Sound",False)
			awarenessService.setStimulusDetectionEnabled("Movement",False)
			awarenessService.setStimulusDetectionEnabled("NavigationMotion",False)
			awarenessService.setStimulusDetectionEnabled("TabletTouch",True)
			awarenessService.setStimulusDetectionEnabled("Touch",True)
			awarenessService.setStimulusDetectionEnabled("People",True)
			awarenessService.setEngagementMode("FullyEngaged")
			awarenessService.setTrackingMode("Head")
		elif (profile == -0.5): #Slightly introvert
			print "attentionTracker slighlty introvert"
			awarenessService.setParameter("LookStimulusSpeed",0.7)
			awarenessService.setParameter("LookBackSpeed",0.7)
			awarenessService.setStimulusDetectionEnabled("Sound",True)
			awarenessService.setStimulusDetectionEnabled("Movement",False)
			awarenessService.setStimulusDetectionEnabled("NavigationMotion",False)
			awarenessService.setStimulusDetectionEnabled("TabletTouch",True)
			awarenessService.setStimulusDetectionEnabled("Touch",True)
			awarenessService.setStimulusDetectionEnabled("People",True)
			awarenessService.setEngagementMode("FullyEngaged")
			awarenessService.setTrackingMode("BodyRotation")
		elif (profile == 0.0): #Ambivert
			print "attentionTracker ambivert"
			awarenessService.setParameter("LookStimulusSpeed",0.5)
			awarenessService.setParameter("LookBackSpeed",0.5)
			awarenessService.setStimulusDetectionEnabled("Sound",True)
			awarenessService.setStimulusDetectionEnabled("Movement",True)
			awarenessService.setStimulusDetectionEnabled("NavigationMotion",False)
			awarenessService.setStimulusDetectionEnabled("TabletTouch",True)
			awarenessService.setStimulusDetectionEnabled("Touch",True)
			awarenessService.setStimulusDetectionEnabled("People",True)
			awarenessService.setEngagementMode("SemiEngaged")
			awarenessService.setTrackingMode("BodyRotation")

		elif (profile == 0.5): #Slighlty Extrovert
			print "attentionTracker slighlty extrovert"
			awarenessService.setParameter("LookStimulusSpeed",0.7)
			awarenessService.setParameter("LookBackSpeed",0.7)
			awarenessService.setStimulusDetectionEnabled("Sound",True)
			awarenessService.setStimulusDetectionEnabled("Movement",True)
			awarenessService.setStimulusDetectionEnabled("NavigationMotion",True)
			awarenessService.setStimulusDetectionEnabled("TabletTouch",True)
			awarenessService.setStimulusDetectionEnabled("Touch",True)
			awarenessService.setStimulusDetectionEnabled("People",True)
			awarenessService.setEngagementMode("Unengaged")
			awarenessService.setTrackingMode("BodyRotation")

		elif (profile == 1.0): #Fully Extrovert
			print "attentionTracker fully extrovert"
			awarenessService.setParameter("LookStimulusSpeed",1.0)
			awarenessService.setParameter("LookBackSpeed",1.0)
			awarenessService.setStimulusDetectionEnabled("Sound",True)
			awarenessService.setStimulusDetectionEnabled("Movement",True)
			awarenessService.setStimulusDetectionEnabled("NavigationMotion",True)
			awarenessService.setStimulusDetectionEnabled("TabletTouch",True)
			awarenessService.setStimulusDetectionEnabled("Touch",True)
			awarenessService.setStimulusDetectionEnabled("People",True)
			awarenessService.setEngagementMode("Unengaged")
			awarenessService.setTrackingMode("BodyRotation")
		awarenessService.setEnabled(True)


#facialExpression
def facialExpression(emotionId, profile):
	facialExpressionService = session.service("ALLeds")
#	facialExpressionService.on("FaceLeds")
	global colorLed	
	global faceExpression
	if (emotionId == 1): #happyFace
		colorLed = "green"	
	elif (emotionId == 2): #sadFace
		colorLed = "blue"
	elif (emotionId == 0): #neutralFace
		colorLed = "white"
#	elif (emotionId == 3): #angerFace
#		colorLed = "red"
	elif (emotionId == 4): #fearFace
		colorLed = "yellow"

	faceExpression = emotionId
	if(profile == -1.0): #fully introvert
		facialExpressionService.setIntensity("FaceLeds",0.2)	
		facialExpressionService.fadeRGB("FaceLeds", colorLed, 1)	
		wait = 0.75
	elif(profile == -0.5): #slightly introvert
		facialExpressionService.setIntensity("FaceLeds",0.35)
		facialExpressionService.fadeRGB("FaceLeds", colorLed, 1.25)
		wait = 1
	elif(profile == 0.0): #ambivert
		facialExpressionService.setIntensity("FaceLeds",0.5)
		facialExpressionService.fadeRGB("FaceLeds", colorLed, 1.5)
		wait = 1.25
	elif(profile == 0.5): #slightly extrovert
		facialExpressionService.setIntensity("FaceLeds",0.7)
		facialExpressionService.fadeRGB("FaceLeds", colorLed, 1.75)
		wait = 1.5
	elif(profile == 1.0): #fully extrovert
		facialExpressionService.setIntensity("FaceLeds",1)
		facialExpressionService.fadeRGB("FaceLeds", colorLed, 2)
		wait = 2
	time.sleep(wait)
	colorLed = "white"
	facialExpressionService.fadeRGB("FaceLeds", colorLed, 1)
	eyeBlinkingBehavior(profile) #as face expression has changed, it needs to update that info


#eye blinking
def eyeBlinkingBehavior(profile):
	global gazeVariation	
	global robotEngagedInTask
	global faceExpression
	global faceExpressionPrevious
	global robotSpeaks
	
	def blinkMorphology():
		def eyeBlinkCommand(duration, fullBlink, blinkType):
			print "About to blink"
			facialExpressionService = session.service("ALLeds")
			facialExpressionService.on("FaceLeds")
			global colorLed #does this work?
			
			result = facialExpressionService.fadeRGB("FaceLeds", colorLed, 0.0)
			if (result == False):
				print "problem coloring eyes"
			if (fullBlink):
				groupLeds = "FaceLeds"
			else:
				groupLeds = "FaceLedsTop"

			for i in range(blinkType):
				result = facialExpressionService.fadeRGB(groupLeds, 0x000000, duration)
				if (result == False):
					print "problem coloring eyes"
	
				#_ledsProxy.fadeRGB(groupLeds, 0x000000, duration / 5. / 1000.); #blinking time shortened by a fourth for NAO as it has no eyelids to move and divided by 1000 to move from milliseconds to seconds
				#_ledsProxy.fadeRGB("FaceLeds", _colorLed, 0.0);
				result = facialExpressionService.fadeRGB("FaceLeds", colorLed, 0.0)
				if (result == False):
					print "problem coloring eyes"
		duration = 0.0
		aux = random.random()
		if(aux < 0.85): #Single blink
			blinkType = 1 
		else:
			aux = random.random()
			if(aux < 0.8): #double blink
				blinkType = 2 
			else: #triple blink
				blinkType = 3

		aux = random.random()
	  
		if(aux < 0.91): #Full blink
			fullBlink = True
		   #Blink duration with 432ms as mean and 72ms as standard deviation (random number between 360 ms and 504 ms)
			aux2 = random.randint(1,144)/100 # Base (0.36) + a value between the range of [0-144] which is the difference between 504ms and 360ms
			duration = 0.36 + aux2
		else: #half blink
			fullBlink = False
		   #Blink duration with 266ms as mean and 4ms as standard deviation (random number between 262 ms and 270 ms)
			aux2 = random.randint(1,8)/100 # Base (0.262) + a value between the range of [0-8] which is the difference between 270ms and 262ms
			duration = 0.262+aux2
		
		#send eye blinking behavior
		eyeBlinkCommand(duration, fullBlink, blinkType)
	   
	probabilityBlink = 0.0
	numberOcurrences = 0.0	
	if(gazeVariation and robotEngagedInTask):
		probabilityBlink += 0.61
		numberOcurrences += 1
		gazeVariation = False

	elif(gazeVariation and not robotEngagedInTask):
		probabilityBlink += 0.72
		numberOcurrences += 1
		gazeVariation=False

	if ((faceExpression != 0)and(faceExpression != faceExpressionPrevious)):
		probabilityBlink += 0.285
		numberOcurrences += 1
		faceExpressionPrevious = faceExpression

	if (robotSpeaks):
		probabilityBlink += 0.31
		numberOcurrences += 1
		robotSpeaks = False
	
	aux = (numberOcurrences/50)
	if(numberOcurrences > 0):
		probabilityBlink = (probabilityBlink+aux)/(1.75+aux) #Probability normalize between 0 and 1. BlinkingRate = 1.75

	threshold = random.random()

	if (threshold < probabilityBlink):
		blinkMorphology()
	
	else:
		threshold2 = random.random()
		if(threshold2 > (0.5-(profile/10))): 
			blinkMorphology()

def readSensors():
	global finish
	global profileFromAdapter
	def whenTouched(bodyPart): #associates a gesture to the touched body part
		facialExpression(1,profileFromAdapter) #happy face

		if (bodyPart ==1): #left bumper
			if (profileFromAdapter > -0.1):
				aux = random.random()
				if (aux < 0.33):
					gesture = "Stand/Gestures/BowShort_2" 
				elif (aux < 0.66):
					gesture = "Stand/Gestures/BowShort_1" 
				else:
					gesture = "Stand/Gestures/BowShort_3" 
			else: 
				aux2 = random.random()
				if (aux2 < 0.5):
					gesture = "Stand/Gestures/BowShort_1" 
				else:
					gesture = "Stand/Gestures/BowShort_3" 	

		elif (bodyPart ==2): #right bumper
			if (profileFromAdapter > -0.1):		
				aux = random.random()
				if (aux < 0.25):
					gesture = "Stand/Gestures/BowShort_2" 
				elif (aux < 0.5):
					gesture = "Stand/Gestures/BowShort_1" 
				elif (aux < 0.75):
					gesture = "Stand/Reactions/SeeSomething_8" 
				else:
					gesture = "Stand/Gestures/BowShort_3" 
			else: 
				aux2 = random.random()
				if (aux2 < 0.5):
					gesture = "Stand/Gestures/BowShort_1" 
				else:
					gesture = "Stand/Gestures/BowShort_3" 

		elif (bodyPart == 3): #head
			if (profileFromAdapter > 0.1):			
				aux = random.random()
				if (aux < 0.25):
					gesture = "Stand/Reactions/TouchHead_1" 
				elif (aux < 0.5):
					gesture = "Stand/Reactions/TouchHead_2" 
				elif (aux < 0.75):
					gesture = "Stand/Reactions/TouchHead_3"
				else:
					gesture = "Stand/Reactions/TouchHead_4"
			elif (profileFromAdapter > -0.6): 
				aux2 = random.random()
				if (aux2 < 0.33):
					gesture = "Stand/Emotions/Negative/Surprise_1" 
				elif (aux2 < 0.66):
					gesture = "Stand/Emotions/Neutral/Innocent_1" 
				else:
					gesture = "Stand/Emotions/Negative/Surprise_2"
			else:
				aux2 = random.random()
				if (aux2 < 0.33):
					gesture = "Stand/Emotions/Neutral/Embarrassed_1"
				elif (aux2 < 0.66):
					gesture = "Stand/Emotions/Negative/Hurt_2" 
				else:
					gesture = "Stand/Emotions/Positive/Shy_1" 
		elif (bodyPart == 4): #left hand
			if (profileFromAdapter < 0.1):
				aux2 = random.random()
				if (aux2 < 0.5):
					gesture = "Stand/Reactions/SeeSomething_5"  
				else: 
					gesture = "Stand/BodyTalk/Listening/Listening_6"  
			else:
				aux2 = random.random()
				if (aux2 < 0.5):
					gesture = "Stand/BodyTalk/Listening/Listening_1" 
				else: 
					gesture = "Stand/BodyTalk/Listening/Listening_6" 

		elif (bodyPart == 5): #right hand
			if (profileFromAdapter > -0.1):
				aux2 = random.random()
				if (aux2 < 0.33):
					gesture = "Stand/BodyTalk/Listening/Listening_2" 
				elif (aux2 < 0.66):
					gesture = "Stand/Reactions/SeeSomething_4" 
				else:
					gesture = "Stand/BodyTalk/Listening/Listening_6" 

			elif (profileFromAdapter > -0.9):
				aux2 = random.random()
				if (aux2 < 0.33):
					gesture = "Stand/Reactions/SeeSomething_5"  
				elif(aux2 < 0.66):
					gesture = "Stand/BodyTalk/Listening/Listening_5" 
				else:
					gesture = "Stand/BodyTalk/Listening/Listening_6" 
			else:
				aux2 = random.random()
				if (aux2 < 0.5):
					gesture = "Stand/Reactions/SeeSomething_6" 
				else:
					gesture = "Stand/BodyTalk/Listening/Listening_6"  

		result = gesturesService.runBehavior(gesture) 
		if (result == False):	
			print "running gesture failed"  

		facialExpression(0,profileFromAdapter)
	try:
		memoryService = session.service("ALMemory")

	except Exception:	
		print "Error when creating memory proxy:"
	gesturesService = session.service("ALBehaviorManager")
	while (not finish):
		time.sleep(1)
		leftBumperTouched = 0
		leftBumperTouched = memoryService.getData("LeftBumperPressed")
		if (leftBumperTouched > 0.5):
			whenTouched(1)
			print "Left bumper touched"

		rightBumperTouched = 0
		rightBumperTouched = memoryService.getData("RightBumperPressed")
		if (rightBumperTouched > 0.5):
			whenTouched(2)
			print "Right bumper touched"

		leftHandTouched = 0
		leftHandTouched = memoryService.getData("HandLeftBackTouched")
		if (leftHandTouched > 0.5):
			whenTouched(4)
			print "Left hand touched"
	
		rightHandTouched = 0
		rightHandTouched = memoryService.getData("HandRightBackTouched")
		if (rightHandTouched > 0.5):
			whenTouched(5)
			print "Right hand touched"

		headTouched = 0
		headFrontTouched = memoryService.getData("FrontTactilTouched")
		headMiddleTouched  = memoryService.getData("MiddleTactilTouched")
		headBackTouched = memoryService.getData("RearTactilTouched")
		if ((headFrontTouched > 0.5)or(headMiddleTouched > 0.5)or(headBackTouched > 0.5)):
			whenTouched(3)
			print "Head touched"


def startIdle():
	global finish
	global profileFromAdapter

	global faceExpressionPrevious
	global gazeVariation
	global robotEngagedInTask
	global faceExpression
	global robotSpeaks
	global finish
	global colorLed

	colorLed = "white"
	finish = False
	faceExpressionPrevious = 0
	gazeVariation = False
	robotEngagedInTask = False
	faceExpression = 0
	robotSpeaks = False

	posture_service = session.service("ALRobotPosture")
	if (posture_service.getPostureFamily() != "Standing"):
		posture_service.goToPosture("StandInit", 0.25)
	
	def setIdleBehavior(profile, finishValue):
	
		attentionTracker(profile, finishValue)
		idleMotion(profile, finishValue)

	#set idle behaviors ON
	setIdleBehavior(profileFromAdapter, finish)

	while(not finish):
		eyeBlinkingBehavior(profileFromAdapter)
		time.sleep(4)

	#set idle behaviors OFF
	setIdleBehavior(profileFromAdapter, finish)

def scriptManager(): #manages the script
	global finish
	global quizFromGUI
	print "Script Manager %d" %quizFromGUI
	#launches random quiz but keeps track of which
	time.sleep(5)
	finish = True

#def sendQuestionnaire(request):

#	return QuestionnaireResponse(entry1,entry2,entry3,entry4,entry5,entry6,entry7,entry8,entry9,entry10,entry11,entry12,entry13,entry14,entry15,flag,entryId)

def main(session):

	global finish
	global profileFromAdapter
	global quizFromGUI
	rospy.init_node('actuation')

	rospy.wait_for_service('GUICommand') #controls script
	try:
		guiClient = rospy.ServiceProxy('GUICommand', GUICommand)
		guiCommand = guiClient()
		commandFromGUI = guiCommand.command_response
		quizFromGUI = guiCommand.command_quiz
		if (commandFromGUI == 1): #launches personality quiz
			print "launches quiz actuation"
			#reads info from memory and sends it back to gui
			#srvActuationToGUIServer = rospy.Service('questionnaire', Questionnaire, sendQuestionnaire)
		elif (commandFromGUI == 2): #starts system
			print "launches system"
			#thread to run idle behaviors
#			tIdle = threading.Thread(target=startIdle)
#			tIdle.start()
		
			#thread to receive tasks + finish flag from interface
			tScript = threading.Thread(target=scriptManager)
			tScript.start()

			#thread to listen to sensory information
#			tSensorsWhile = threading.Thread(target=readSensors)
#			tSensorsWhile.start()
		elif (startCommandFromGUI == 3): #stops system
			finish = True
	except rospy.ServiceException, e:
		print "profile call failed: %s"%e

	rospy.wait_for_service('adapterPersonality')
	try:
		profileClient = rospy.ServiceProxy('adapterPersonality', Personality)
		profile = profileClient()
		profileFromAdapter = profile.personality_profile

		print "Actuation got profile: %s"%profileFromAdapter

	except rospy.ServiceException, e:
		print "profile call failed: %s"%e

	rospy.spin()

if __name__ == "__main__":
	try: 
		print("Connecting to naoqi...")
		session = qi.Session()
		robotIp = os.environ.get("ROBOT_IP")
		session.connect("tcp://" + robotIp + ":9559")
		print('Connected to naoqi')
	except RuntimeError:
		print ("Cannot connect to naoqi")
	#	sys.exit(1)
	main(session)
