#!/usr/bin/env python
#print("Python: Adapter node")
import rospy
import actionlib
import sys
import random
import time
import os
from threading import Thread
#from package.msg import *
from package.srv import *

def sendPersonality(request):
	global personality
	global personality_profile
	#depending on the mode we choose
	#15-30 full introvert; 30-41 slightly introvert; 41-49 ambivert ;49-60 slighlty extrovert ; 60-75 full extrovert
	
	#extraversion + agreeableness (15+15) / extraversion + agreeableness + neuroticism + openness + conscientiousness (15*5)
	if (personality <= 12):
		personality_profile = -1.0 #full introvert
	elif (personality <= 16): #slightly introvert
		personality_profile = -0.5
	elif (personality <= 20):
		personality_profile = 0.0 #ambivert
	elif (personality <= 24):
		personality_profile = 0.5 #slightly extrovert
	else:
		personality_profile = 1.0 #full extrovert

	if (flag == 2): #complementary
		personality_profile = personality_profile*(-1)

	#personality_profile = 1.0 #testing purposes

	return PersonalityResponse(personality_profile)

def main():
	global personality
	global flag
	rospy.init_node("adapter")
	rospy.wait_for_service('questionnaire')
	try:
		#Gets data from service sent (my case I will need to get responses from questionnaire)
		questionnaireClient = rospy.ServiceProxy('questionnaire', Questionnaire)
		questionnaireToProfile = questionnaireClient()		
		question1 = questionnaireToProfile.q1_response
		question2 = 6-questionnaireToProfile.q2_response
		question3 = questionnaireToProfile.q3_response
		question4 = 6-questionnaireToProfile.q4_response
		question5 = questionnaireToProfile.q5_response
		question6 = 6-questionnaireToProfile.q6_response
		question7 = questionnaireToProfile.q7_response
		question8 = 6-questionnaireToProfile.q8_response
		question9 = questionnaireToProfile.q9_response
		question10 = 6-questionnaireToProfile.q10_response
		question11 = questionnaireToProfile.q11_response
		question12 = 6-questionnaireToProfile.q12_response
		question13 = questionnaireToProfile.q13_response
		question14 = 6-questionnaireToProfile.q14_response
		question15 = questionnaireToProfile.q15_response
		flag = questionnaireToProfile.flag_response

	except rospy.ServiceException, e:
		print "Service call failed: %s"%e


	#testing purposes
#	question1 = random.randint(1,5)
#	question6 = 6-random.randint(1,5)
#	question11 = random.randint(1,5)
#	question5 = random.randint(1,5)
#	question10 = 6-random.randint(1,5)
#	question15 = random.randint(1,5)
#	flag = random.randint(1,2)
	#testing purposes

	#compute personality + send profile to actuation and reactive
	extraversion = question1+question6+question11
#	neuroticism = question2+ question7+question12
#	openness = question3+question8+question13
#	conscientiousness = question4+question9+question14
	agreeableness = question5+question10+question15

#	personality = extraversion + neuroticism + openness + conscientiousness + agreeableness
	personality = extraversion + agreeableness
	print "personality %s"%personality
	print "flag %s"%flag

	#send profile to actuation
	srvAdapterActuationServer = rospy.Service('adapterPersonality', Personality, sendPersonality)

	time.sleep(5)
	rospy.spin()


if __name__ == "__main__":
    main()
