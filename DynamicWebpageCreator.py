import xml.etree.ElementTree as etree
import time
#from ReplaceResource import ReplaceResource
import subprocess
import datetime

global MainPath
MainPath = "/home/pratesh_ubuntu/dsnproject/"
global Label
Label    = 'LocalActive'
global XMLFile
XMLFile  = Label+'.xml'
global Current_P
global Current_Q
global Current_R


global tree
tree = etree.parse(MainPath+XMLFile)
global root
root = tree.getroot()

global HTMLpagesPath
HTMLpagesPath = MainPath+Label+'/'+'loading.html'



P=len(list(root[0]))   #no. of elements in high tag
Q=len(list(root[1]))    #no. of elements in medium tag
R=len(list(root[2]))    #no. of elements in low tag
################

i=0     #counter for high priority elements
j=0     #counter for medium priority elements
k=0     #counter for low priority elements


class finalone:
		  
	def VideoCreator(self,html,level1,level2):

		hfile=open(MainPath+"LocalActive"+'/'+str(html)+'.html',"w")

		html_str="""
		<html>
		<BODY style="background-color:black">
		<H1 style="color:white"><center>$TOPIC$</center></H1>
		<video width="1270" height="730" autoplay>
		  <source src="$VIDEO_FILE$" type="video/mp4">
		  Your browser does not support the video tag.
		</video>
		</BODY>
		 
		<script type="text/javascript">
		var redirectURL ='$NEXT_HTML$'; // edit this value for the next page
		var redirectDelayInSeconds = $LOOP_TIME$; // edit this value after how many seconds
		var d = redirectDelayInSeconds * 1000;
		window.setTimeout ('parent.location.replace(redirectURL)', d);
		</script>
		</html>
		"""

		html_str=html_str.replace('$TOPIC$',root[level1][level2].find('topic').text)

		VideoFile=root[level1][level2].find('filename').text
		VideoFile=MainPath+'LocalRepository/'+ VideoFile
		html_str=html_str.replace('$VIDEO_FILE$',VideoFile)

		NextHtml = str((html + 1)%6) + '.html'
		html_str=html_str.replace('$NEXT_HTML$',NextHtml)

		html_str=html_str.replace('$LOOP_TIME$',root[level1][level2].find('loop_time').text)
		#print html_str
		print VideoFile
		hfile.write(html_str)
		hfile.close()
	
	def ImageCreator(self,html,level1,level2):

		hfile=open(MainPath+"LocalActive"+'/'+str(html)+'.html',"w")

		html_str="""
		<HTML>
		 <HEAD>
		  <TITLE>
		      $TOPIC$
		  </TITLE>
		 </HEAD>
		 <BODY style="background-color:black">
		  <H1 style="color:white"><center>$TOPIC$</center></H1>
		      <img src="$IMAGE_FILE$"
		       style="height:730px;width:1270px"
               > 
		 </BODY>
		 <script type="text/javascript">
		 var redirectURL ='$NEXT_HTML$'; // edit this value for the next page
		 var redirectDelayInSeconds = $LOOP_TIME$; // edit this value after how many seconds
		 var d = redirectDelayInSeconds * 1000;
		 window.setTimeout ('parent.location.replace(redirectURL)', d);
		 </script>
		</HTML>
		"""
		#html_str=re.sub('#NEXTHTML','hello.html',html_str)
		html_str=html_str.replace('$TOPIC$',root[level1][level2].find('topic').text)

		ImageFile=root[level1][level2].find('filename').text
		ImageFile= MainPath+'LocalRepository/'+ ImageFile
		html_str=html_str.replace('$IMAGE_FILE$',ImageFile)

		NextHtml = str((html + 1)%6) + '.html'
		html_str=html_str.replace('$NEXT_HTML$',NextHtml)

		html_str=html_str.replace('$LOOP_TIME$',root[level1][level2].find('loop_time').text)
		#print html_str
		print ImageFile
		hfile.write(html_str)
		hfile.close()
	
	def EventCreator(self,html,level1,level2):

		hfile=open(MainPath+"LocalActive"+'/'+str(html)+'.html',"w")

		html_str="""
		<HTML>
		 <HEAD>
		  <TITLE>
		      $TOPIC$
		  </TITLE>
		 </HEAD>
		 <BODY style="background-color:#0174DF">
		 <div align="center" style="width:1240px">
		  <H1 style="color:white;margin-top:200;font-size:40pt;">$TOPIC$</H1>
		      <P style="color:white;font-size:30pt;">$DETAILS$</P>
		 </div> 
		 </BODY>
		 <script type="text/javascript">
		 var redirectURL ='$NEXT_HTML$'; // edit this value for the next page
		 var redirectDelayInSeconds = $LOOP_TIME$; // edit this value after how many seconds
		 var d = redirectDelayInSeconds * 1000;
		 window.setTimeout ('parent.location.replace(redirectURL)', d);
		 </script>
		</HTML>
		"""
		#html_str=re.sub('#NEXTHTML','hello.html',html_str)
		html_str=html_str.replace('$TOPIC$',root[level1][level2].find('topic').text)

		details = etree.tostring(root[level1][level2].find('text'))
		details = details.replace('<text>','')
		details = details.replace('</text>','')
		details = details.replace('&lt;','<')
		details = details.replace('&gt;','>')
		html_str=html_str.replace('$DETAILS$',details)

		NextHtml = str((html + 1)%6) + '.html'
		html_str=html_str.replace('$NEXT_HTML$',NextHtml)

		html_str=html_str.replace('$LOOP_TIME$',root[level1][level2].find('loop_time').text)
		print html_str
		print details
		hfile.write(html_str)
		hfile.close()
		
	def ReplaceResource(self,html,priority,level2):
		if (priority == 'High'):
		    level1=0
		elif (priority == 'Medium'):
		    level1=1	    
		elif (priority == 'Low'):
		    level1=2 
	
		if root[level1][level2].find('filetype').text == 'text':
		   self.EventCreator(html,level1,level2)

		elif root[level1][level2].find('filetype').text == 'image':
		   self.ImageCreator(html,level1,level2)	
		   
		elif root[level1][level2].find('filetype').text == 'video':
		   self.VideoCreator(html,level1,level2)
	

class rfid:

	def RFIDdetect(self):
		#Label will actually change when ever the RFID part will change its input.
		#So,XMLFile will get its input from RFID part using a file in between.
		global Label,P,Q,R
		RFIDtxt= open(MainPath+"RFID.txt")
		Labeltemp  = RFIDtxt.readline()
		RFIDtxt.close()

		if Labeltemp != Label:
			Label = Labeltemp
			XMLFile  = Label+'.xml'
			print XMLFile
			tree = etree.parse(MainPath+XMLFile)
			root = tree.getroot()
			#then get the updated P,Q,R
			P=len(list(root[0]))    #no. of elements in high tag
	 		Q=len(list(root[1]))    #no. of elements in medium tag
			R=len(list(root[2]))    #no. of elements in low tag
			#print P,Q,R
			
	def GetCurrentElements(self):
		global Current_P,Current_Q,Current_R
		if P != 0:
			Current_P=self.CountCurrentElements(0,P) #list of high elements that are to be shown at the current time
		if Q != 0:
			Current_Q=self.CountCurrentElements(1,Q)
		if R != 0:
			Current_R=self.CountCurrentElements(2,R)

	def CountCurrentElements(self,priorityValue,ElementsCount):
		CurrentElementList=[]
		for i in range(0,ElementsCount):
			ElementTimeStamp=root[priorityValue][i].find('start_date').text + ' ' +root[priorityValue][i].find('start_time').text
			if( datetime.datetime.strptime(ElementTimeStamp,'%Y-%m-%d %H:%M:%S') <= datetime.datetime.now()): #past time is less than presnt
				CurrentElementList.append(i)
		return CurrentElementList



f1=finalone()
rf=rfid()
#NOW trigger the launch of first HTML page
#subprocess.call(["midori", HTMLpagesPath])
subprocess.Popen(["midori", HTMLpagesPath,"&"])  #this will actually be run in startup shell script not here

htmlPageNumber=0
#time.sleep(2)

while True:


	rf.RFIDdetect()

	print "PAGE0\n"
	if len(Current_P) != 0:

		f1.ReplaceResource(htmlPageNumber,'High',i)
		htmlPageNumber = (htmlPageNumber+1)%6
		time.sleep(int(root[0][i].find('loop_time').text)-0.1)
		i = (i+1)%len(Current_P)

	rf.RFIDdetect()
	
	print "PAGE1\n"
	if len(Current_Q) != 0:
		f1.ReplaceResource(htmlPageNumber,'Medium',j)
		htmlPageNumber = (htmlPageNumber+1)%6
		time.sleep(int(root[1][j].find('loop_time').text)-0.1)
		j = (j+1)%len(Current_Q)

	rf.RFIDdetect()
	
	print "PAGE2\n"
	if len(Current_P) != 0:
		f1.ReplaceResource(htmlPageNumber,'High',i)
		htmlPageNumber = (htmlPageNumber+1)%6
		time.sleep(int(root[0][i].find('loop_time').text)-0.1)
		i = (i+1)%len(Current_P)

	rf.RFIDdetect()
	

	print "PAGE3\n"
	if len(Current_R) != 0:
		f1.ReplaceResource(htmlPageNumber,'Low',k)
		htmlPageNumber = (htmlPageNumber+1)%6
		time.sleep(int(root[2][k].find('loop_time').text)-0.1)
 		k = (k+1)%len(Current_R)

 	rf.RFIDdetect()
        

 	print "PAGE4\n"
	if len(Current_Q) != 0:
		f1.ReplaceResource(htmlPageNumber,'Medium',j)
		htmlPageNumber = (htmlPageNumber+1)%6
		time.sleep(int(root[1][j].find('loop_time').text)-0.1)
 		j = (j+1)%len(Current_Q)

	rf.RFIDdetect()
        
        
 	print "PAGE5\n"
	if len(Current_P) != 0:
		f1.ReplaceResource(htmlPageNumber,'High',i)
		htmlPageNumber = (htmlPageNumber+1)%6
		time.sleep(int(root[0][i].find('loop_time').text)-0.1)
 		i = (i+1)%len(Current_P)
	
	#Label will actually change when ever the RFID part will change its input.
	#So,XMLFile will get its input from RFID part using a file in between.
	#RFIDtxt= open(MainPath+"RFID.txt")
	#Labeltemp  = RFIDtxt.readline()
	#RFIDtxt.close()

	#if Labeltemp != Label:
	#	Label = Labeltemp
	#	XMLFile  = Label+'.xml'
		#try if u can load the loading.html everytime the Label changes.
	    #the problem is that if u launch the midori seperatly for each lable change then
	    #it may genernate a new tab insted of opening in the same tab.
	#	subprocess.call(["rm","-f","~/.config/midori/session.xbel"])
	#	HTMLpagesPath = MainPath+Label+'/'+'loading.html'
	#	subprocess.call(["midori",HTMLpagesPath,"&"])


	tree = etree.parse(MainPath+XMLFile)
	root = tree.getroot()
	#then get the updated P,Q,R
	P=len(list(root[0]))   #no. of elements in high tag
	Q=len(list(root[1]))    #no. of elements in medium tag
	R=len(list(root[2]))    #no. of elements in low tag
	print P,Q,R
	rf.GetCurrentElements()
	#print Current_P
	#print Current_Q
	#print Current_R
	


	
	
   


