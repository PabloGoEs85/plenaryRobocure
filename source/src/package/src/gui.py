#!/usr/bin/env python2.7
import rospy
from Tkinter import *
from package.srv import *

def launchSystem():
	global CKsimilarity
	def sendQuestionnaire(request):
		global e1
		global e2
		global e3
		global e4
		global e5
		global e6
		global e7
		global e8
		global e9
		global e10
		global e11
		global e12
		global e13
		global e14
		global e15	
		global CKsimilarity

		entry1 = int(e1.get())
		entry2 = int(e2.get())
		entry3 = int(e3.get())
		entry4 = int(e4.get())
		entry5 = int(e5.get())
		entry6 = int(e6.get())
		entry7 = int(e7.get())
		entry8 = int(e8.get())
		entry9 = int(e9.get())
		entry10 = int(e10.get())
		entry11 = int(e11.get())
		entry12 = int(e12.get())
		entry13 = int(e13.get())
		entry14 = int(e14.get())
		entry15 = int(e15.get())

		flag = int(CKsimilarity.get())

		return QuestionnaireResponse(entry1,entry2,entry3,entry4,entry5,entry6,entry7,entry8,entry9,entry10,entry11,entry12,entry13,entry14,entry15,flag)
	
	
	def sendCommand(command_request):
		global tabletDone
		global eID
		if(tabletDone):
			command_response = 2
	
		else: 
			command_response = 1
			tabletDone = True
		command_quiz = int(eID.get())
		return GUICommandResponse(command_response, command_quiz)
	
	global paperBased
	global tabletDone
	
	#disables Q1 to Q15, CBtablet, CBsimilarity and ID
	editEntries('disabled')

	#launch system sending Q1 to Q15 and similarity flag --> to adapter - actuation? or some coordinator
	if (paperBased):
		srvGUIAdapterServer = rospy.Service('questionnaire', Questionnaire, sendQuestionnaire)
		tabletDone = True
		srvGUIActuationServer = rospy.Service('GUICommand', GUICommand, sendCommand)
#	else: 
#		tabletDone = False
#		srvGUIActuationServer = rospy.Service('GUIcommand', StartStop, sendCommand)
		#waits for feedback from quiz
		#rospy.wait_for_service('QuizFeedback')
		#try:
		#	quizFeedbackClient = rospy.ServiceProxy('QuizFeedback', Questionnaire)
		#	quizFeedback = quizFeedbackClient()
		#	quizFeedbackFromGUI = quizFeedback.command_response
			
		#except rospy.ServiceException, e:
		#	print "profile call failed: %s"%e
		#then sets tabletDone = True and calls again
#		tabletDone = True
#		srvGUIActuationServer = rospy.Service('GUIcommand', StartStop, sendCommand)
def editEntries(status):
	global e1
	global e2
	global e3
	global e4
	global e5
	global e6
	global e7
	global e8
	global e9
	global e10
	global e11
	global e12
	global e13
	global e14
	global e15
	global eID

	e1.pack_forget()
	e1.config(state=status)
	e1.grid(row=0, column=1)

	e2.pack_forget()
	e2.config(state=status)		
	e2.grid(row=1, column=1)

	e3.pack_forget()
	e3.config(state=status)
	e3.grid(row=2, column=1)		

	e4.pack_forget()
	e4.config(state=status)
	e4.grid(row=3, column=1)

	e5.pack_forget()
	e5.config(state=status)
	e5.grid(row=4, column=1)

	e6.pack_forget()
	e6.config(state=status)
	e6.grid(row=5, column=1)

	e7.pack_forget()
	e7.config(state=status)
	e7.grid(row=6, column=1)

	e8.pack_forget()
	e8.config(state=status)
	e8.grid(row=7, column=1)

	e9.pack_forget()
	e9.config(state=status)
	e9.grid(row=8, column=1)

	e10.pack_forget()
	e10.config(state=status)
	e10.grid(row=9, column=1)	

	e11.pack_forget()
	e11.config(state=status)
	e11.grid(row=10, column=1)

	e12.pack_forget()
	e12.config(state=status)
	e12.grid(row=11, column=1)
	
	e13.pack_forget()
	e13.config(state=status)
	e13.grid(row=12, column=1)

	e14.pack_forget()
	e14.config(state=status)
	e14.grid(row=13, column=1)

	e15.pack_forget()
	e15.config(state=status)
	e15.grid(row=14, column=1)

	eID.pack_forget()
	eID.config(state=status)
	eID.grid(row=4, column=3)

def tabletVSpaper():
	#disables CBtablet from now on
	global CBtablet
	global paperBased

	if (CBtablet.get()==1): #tablet --> launches personality quiz (via actuation?)
		print "quizzzz"
		editEntries('disabled')
		paperBased = False
		launchSystem()
	elif (CBtablet.get()==2): #paper --> enables questions + similar/complementary + go button
		paperBased = True	
		editEntries('normal')
		print "paperrrr"
	

def main():	
	global CBtablet
	global CKsimilarity	
	global e1
	global e2
	global e3
	global e4
	global e5
	global e6
	global e7
	global e8
	global e9
	global e10
	global e11
	global e12
	global e13
	global e14
	global e15
	global eID

#fileObject = open("GuiLog.txt","w")
	rospy.init_node("gui")
	window = Tk()
	CKsimilarity = IntVar()
	CKsimilarity.set(0)	
	CBtablet = IntVar()	
	CBtablet.set(0)
	window.title('Robot Quiz')
	widthScreen = window.winfo_screenwidth()
	heightScreen = window.winfo_screenheight()
	window.attributes("-fullscreen", False)#full screen disavantage:toolbar disappear

	##### TEXT #####
	frameUpL = Frame(window,width = int(0.2*widthScreen),height = int(0.2*heightScreen))
	frameUpL.grid(row = 0, column = 0)
	frameUpL.pack_propagate(False)
	#fieldLabel = Label(frameUpL,text="Personality Test input",font = ('',int(20.0/768.0*heightScreen), "bold"),wraplength = int(0.2*widthScreen))
	#fieldLabel.pack()

	Label(frameUpL, text="Q1").grid(row=0, column=0)
	Label(frameUpL, text="Q2").grid(row=1, column=0)	
	Label(frameUpL, text="Q3").grid(row=2, column=0)	
	Label(frameUpL, text="Q4").grid(row=3, column=0)
	Label(frameUpL, text="Q5").grid(row=4, column=0)
	Label(frameUpL, text="Q6").grid(row=5, column=0)
	Label(frameUpL, text="Q7").grid(row=6, column=0)
	Label(frameUpL, text="Q8").grid(row=7, column=0)
	Label(frameUpL, text="Q9").grid(row=8, column=0)
	Label(frameUpL, text="Q10").grid(row=9, column=0)
	Label(frameUpL, text="Q11").grid(row=10, column=0)
	Label(frameUpL, text="Q12").grid(row=11, column=0)
	Label(frameUpL, text="Q13").grid(row=12, column=0)
	Label(frameUpL, text="Q14").grid(row=13, column=0)
	Label(frameUpL, text="Q15").grid(row=14, column=0)

	e1 = Entry(frameUpL)
	e2 = Entry(frameUpL)
	e3 = Entry(frameUpL)
	e4 = Entry(frameUpL)
	e5 = Entry(frameUpL)
	e6 = Entry(frameUpL)
	e7 = Entry(frameUpL)
	e8 = Entry(frameUpL)
	e9 = Entry(frameUpL)
	e10 = Entry(frameUpL)
	e11 = Entry(frameUpL)
	e12 = Entry(frameUpL)
	e13 = Entry(frameUpL)
	e14 = Entry(frameUpL)
	e15 = Entry(frameUpL)
	eID = Entry(frameUpL)

	editEntries('disabled')
	
	Radiobutton(frameUpL, variable=CBtablet, value = 1, text="Tablet", command=tabletVSpaper).grid(row=2, column=2)
	Radiobutton(frameUpL, variable=CBtablet, value = 2, text="Paper", command=tabletVSpaper).grid(row=3, column=2)
	Label(frameUpL, text="Quiz ID").grid(row=4, column=2)

	Radiobutton(frameUpL, variable=CKsimilarity, value = 0, text="Neutral").grid(row=5, column=2)
	Radiobutton(frameUpL, variable=CKsimilarity, value = 1, text="Similar").grid(row=6, column=2)
	Radiobutton(frameUpL, variable=CKsimilarity, value = 2, text="Complementary").grid(row=7, column=2)

	bGo = Button(frameUpL, text='Go', command=launchSystem,state='normal')
	bGo.grid(row=1, column = 2)
		
	frameDoR = Frame(window,width = int(0.2*widthScreen),height = int(0.2*heightScreen))
	frameDoR.grid(row = 0, column = 1)
	frameDoR.pack_propagate(False)
	
    ##### BUTTON #####
	button = Button(frameDoR,text = "Next",font = ('',int(15.0/768.0*heightScreen), "bold"),\
                    command = window.destroy,width = int(0.01*widthScreen),height = int(0.001*heightScreen))
	button.pack(side = "bottom")

    ##### GRAPHICAL INTERFACE + ROBOT BEHAVIOR TOGETHER #####
	window.update_idletasks()
	window.update()

	window.mainloop()
	rospy.spin()

if __name__ == "__main__":
    main()
