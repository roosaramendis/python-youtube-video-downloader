# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'py_ytdownloader_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

#created by: sidhas roosara mendis (DRAGON) 
#github link:

#__________imports_______________
from logging import exception
from typing import ParamSpecArgs
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QInputDialog,QErrorMessage
from PyQt5.QtCore import QSettings
import pytube
from pytube import YouTube
from pytube import streams
#import ytdownloader
from threading import Thread
import time
import random
import re
import os
import pickle
import traceback
#..........................................

#____________global variables________________
global videodic  #to save yt video title and link (key = video title , value = video url)
videodic = {}
global keyslist # to save yt videos titles from videodic var 
keyslist = []
global selectedvideos # to save selected videos title from list viewer 
selectedvideos = []
global videostate # to save video states (queue, downloaded,error)
videostate ={}
global proggrespresent5 # for proggresbra prestage 
proggrespresent5 = 0
global d_finished
d_finished = False
global mydir # for save dir of software installed
mydir = os.path.dirname(os.path.realpath(__file__))
global borderroundness # to save border roundness value (this is created as list of strings. because to save separately default values and user changed values )
borderroundness = ["1px"]
global bordersize # to save size of border value (this is created as list of strings. because to save separately default values and user changed values )
bordersize = ["2px"] 
global textcolor # to save text color (this is created as list of strings. because to save separately default values and user changed values )
textcolor = ["#ff0000"]
global askeverytime # to save value ask where to you need to download every time you clicked download. (this is created as list of bool. because to save separately default values and user changed values )
global usecustomedownpath # to save value if you using custome path to download. (this is created as list of bool. because to save separately default values and user changed values )
usecustomedowpath = [False]
askeverytime = [False]
global customdownloadpath # to save path if you r using custome path to download. (this is created as list of bool. because to save separately default values and user changed values )
customdownloadpath =[""] 
global bordercolor # to save border color (this is created as list of strings. because to save separately default values and user changed values )
bordercolor = ["#ff0000"]
global downloadpath # to save default download path as string (this is created as list of strings. because to save separately default values and user changed values )
downloadpath = [mydir+"/videos"]
bimageurl = "url("+mydir+"/assets/bacground image.png);"
print(bimageurl)
global customdownloadpathstr
customdownloadpathstr = [""]
global d_finished1
d_finished1 = [False]
global errorexct # to save error exception as string list
errorexct = [""]
global vqultybyitagdic # to save video qulity as a key and itag as value
vqultybyitagdic = {}
#.......................................................

# class for get qualitys in vided
class getvideoqultys_tread(QtCore.QThread):

    setqltycombobox = QtCore.pyqtSignal(list)
    callerror = QtCore.pyqtSignal(str)
    def __init__(self,url, parent=None):
        super(getvideoqultys_tread,self).__init__(parent)
        self.url = url
    def run(self):
        print("geting streams ")
        itagstr = []
        vqultydic = {}
        stlist = ["",""]
        stlistforcombo = []
        try:
            if self.url !="":
                if(re.search("playlist",self.url)):
                    print("its playlist")
                else:
                    q = YouTube(str(self.url))
                    for s in q.streams.filter(adaptive=True):
                        try:
                    
                            print("itag " + str(s))    
                                
                        except:
                            traceback.print_exc()
                        else:
                            itagstr.append(str(s))
                            stlist[0] = str(s.mime_type)
                            stlist[1] = str(s.resolution)
                            stlistforcombo.append(str(stlist))
                            vqultydic[str(stlist)] = str(s.itag)
                            vqultybyitagdic[str(stlist)] = (s.itag)
                            print(str(stlist))
                            print(str(s.itag)+" "+str(s.resolution)+" "+str(s.mime_type))
                        
                    print(itagstr)
                    print(vqultydic)
                    print(type(itagstr)) 
                    self.setqltycombobox.emit(stlistforcombo)
                    
        except:
            #errorexct[0] = str(e)
            self.callerror.emit(str(errorexct))    

# class for dowload selected video in another tread        
class dowload_selected_tread(QtCore.QThread):
    calldowloadvideo = QtCore.pyqtSignal(str,str)
    callerror = QtCore.pyqtSignal(str)
    def __init__(self,url, qulity, parent=None):
        super(dowload_selected_tread,self).__init__(parent)
        self.url = url
        self.qlty = qulity
    def getvideolink(self,videoname):
        link = videodic.get(videoname)    
        return link
    def run(self):
        
        if usecustomedowpath[0] == "true":
            downloadpath[0] = customdownloadpathstr[0]
        if askeverytime[0]== "true":
            downpath1 = QtWidgets.QFileDialog.getExistingDirectory(None, 'download path',mydir)
            downloadpath[0] = downpath1
        for vname in selectedvideos:
            print("dfinished "+str(d_finished1[0]))
            if videostate.get(vname) == "q" or videostate.get(vname) == "error":
                yturl = self.getvideolink(vname)
                vqulity = self.qlty
                print(vqulity+" combo")
                print("print download")
                global ytvd
                q = YouTube(yturl)
                ress = []
                try:
                    for s in q.streams.filter(adaptive=True):
                        try:
                            print("resolution: " + s.resolution)    
                        except:
                            traceback.print_exc()
                        else:
                            ress.append(s.resolution)
                    print(ress)
                    if vqulity in ress:
                        pass
                    else:
                        vqulity = "720p"
                    print(vqulity+" downloading")
                    self.calldowloadvideo.emit(str(yturl),str(vqulity))
                    time.sleep(0.4)
                    print("dfinished state "+str(d_finished1[0]))
                    while d_finished1[0] == False:
                        print(" downloading "+ vname)
                        time.sleep(0.3)
                    videostate[vname] = "downloaded"
                    time.sleep(0.4)
                    print("continue")
                except Exception as e:
                    traceback.print_exc()
                    print(str(e))
                    errorexct[0] = str(e)
                    self.callerror.emit(str(errorexct))

                    try:
                        videostate[str(self.video.title)] = "error" 
                        print("unknowen error,check internet contion and if yoou are using vpn disconect try again")
                    except Exception as e:
                        traceback.print_exc()
                        print(str(e))
                        errorexct[0] = str(e)
                        self.callerror.emit(str(errorexct))

            elif videostate.get(vname) == "downloading":
                print("dowloading")

            elif videostate.get(vname) == "downlaaded":
                print ('video downloaded')
# class for download videos in another tread
class video_dowload_tread(QtCore.QThread):
    change_value = QtCore.pyqtSignal(int,str)
    finishvname = QtCore.pyqtSignal(str)
    callerror = QtCore.pyqtSignal(str)
    def __init__(self,url, qulity, parent=None):
        super(video_dowload_tread,self).__init__(parent)
        self.yturl = url
        self.qlty = qulity
        print (str(url) + " video url")
        self.timestarted =0.0
        d_finished1[0] = False
            
    def run(self):
        def progres_func(stream, chunk,bytes_remaining):    
            size = self.video.filesize
            nameofdownloading = self.video.title
            downloadedsize = abs(bytes_remaining-size)
            print("print download size "+str(downloadedsize))
            timeecleped = time.mktime(time.localtime())- self.timestarted
            print(str(timeecleped)+" time") 
            speed = ((downloadedsize/1024)/timeecleped)/1024
            print("spped "+str(speed))
            progress = (float(abs(bytes_remaining-size)/size)*float(100))
            print(progress)
        
            self.change_value.emit(int(progress),str(speed)[0:3]+" mbps " + "downloading "+nameofdownloading)
        def finishedfunc(stream,filepath):
            self.finishvname.emit(str(self.video.title))
            d_finished1[0] = True
        
        try:
            d_finished1[0] = False
            self.timestarted = time.mktime(time.localtime())
            print(str(self.timestarted)+" time started")
            yt=YouTube(self.yturl,on_progress_callback=progres_func,on_complete_callback=finishedfunc)
            print(self.qlty)
            print(type(self.qlty))
            if type(self.qlty) == int:
                self.video = yt.streams.filter(adaptive=True).get_by_itag(self.qlty)
                self.audio = yt.streams.filter(only_audio=True).first()
            else:     
                self.video = yt.streams.filter(progressive=True).get_by_resolution(self.qlty)
            print(downloadpath[0])
            
            self.video.download(downloadpath[0])
            try:
                if self.audio != None:
                
                    self.audio.download(downloadpath[0],filename_prefix="audio_")
                else:
                    print("audio none")    
            except:
                print("downloading with proggressive")
        except:
            traceback.print_exc()
            try:
                print("reslution fix area")
                self.video = yt.streams.filter(adaptive=True).get_highest_resolution()
                self.video.download(downloadpath[0])
            except Exception as e:
                print(str(e))
                errorexct[0] = str(e)
                self.callerror.emit(str(errorexct))                           
#class for UI defenitions and setting up
class Ui_Form(object):
    pp = 0
    # function for setting up UI 
    def setupUi(self, Form):
        Form.setObjectName("DRAGON YT DOWNLOADER")#Form
        #Form.resize(640, 520)
        Form.setFixedSize(640, 520)
        self.makesettingvals()  # calling foe function for make sattings value on registry if not exist      
        self.setdefsettingvals() # calling for function for seve default settings value to registry if not exist or if software opening first time 
        self.getsettingvals() # calling for function for get settings value from registry 
        # _________style sheets____________ 
        self.stylesheet =( "background-image: "+bimageurl+";"+ 
        "background-repeat: no-repeat;"+ 
        "background-position: center;")
        self.commenstyle =("*{border: "+bordersize[0]+" solid "+bordercolor[0]+";"+
                        "color: "+textcolor[0]+";"+
                        "border-radius: "+borderroundness[0]+";}"+
                        "*:hover{background: 'blue';}")    
        self.textinputstyle = ("*{border: "+bordersize[0]+" solid "+bordercolor[0]+";"+
                            "color: "+textcolor[0]+";"+
                            "border-radius: "+borderroundness[0]+";}"+
                            "*:hover{background: 'blue';}")        
        self.commenstyle2 =  ("*{border: "+bordersize[0]+" solid "+bordercolor[0]+";"+
                            "text-align: center;"+
                            "color: "+textcolor[0]+";"+
                            "border-radius: "+borderroundness[0]+";}")
        #..........................................................................

        #____________setup of line edit that use for get url_______________
        self.LE_ulr = QtWidgets.QLineEdit(Form)
        self.LE_ulr.setGeometry(QtCore.QRect(10, 70, 618, 21))
        self.LE_ulr.setObjectName("LE_ulr")
        self.LE_ulr.setToolTip(" paste url here you want to download . if you need to download playlist you can add yt playlist link and the click add video")
        self.LE_ulr.setStyleSheet(self.textinputstyle)
        self.LE_ulr.textChanged.connect(self.getvideosinstreamscall)
        #...........................................................................

        #_____________setup of add url button______________________
        self.pb_addurl = QtWidgets.QPushButton(Form)
        self.pb_addurl.setGeometry(QtCore.QRect(10, 10, 61, 51))
        self.pb_addurl.setObjectName("pb_addurl")
        self.pb_addurl.setToolTip(" this is for add video or video playlist in url to list view ")
        self.pb_addurl.setStyleSheet(self.commenstyle)
        self.pb_addurl.clicked.connect(self.clk_addvideo)
        #...............................................................

        #_____________setup of list viewer______________________
        self.lv_url = QtWidgets.QListView(Form)
        self.lv_url.setGeometry(QtCore.QRect(10, 150, 618, 331))
        self.lv_url.setObjectName("lv_url")
        self.lv_url.setStyleSheet(self.commenstyle2)
        #.......................................................

        #_____________setup of error message____________
        self.errmsg = QtWidgets.QErrorMessage(Form)
        self.errmsg.setStyleSheet(self.commenstyle)
        #................................................

        #_______________setup of download video button___________________
        self.pb_downloadvideo = QtWidgets.QPushButton(Form)
        self.pb_downloadvideo.setGeometry(QtCore.QRect(84, 10, 91, 51))
        self.pb_downloadvideo.setCheckable(False)
        self.pb_downloadvideo.setObjectName("pb_downloadvideo")
        self.pb_downloadvideo.setToolTip(" this is for download video in url directly(only able to download one video cant download a list) ")
        self.pb_downloadvideo.setStyleSheet(self.commenstyle)
        self.pb_downloadvideo.clicked.connect(self.clk_dowloadvideo)
        #..................................................................

        #_______________setup of download selected button______________________
        self.pb_downloadselected = QtWidgets.QPushButton(Form)
        self.pb_downloadselected.setGeometry(QtCore.QRect(190, 10, 101, 51))
        self.pb_downloadselected.setObjectName("pb_downloadselected")
        self.pb_downloadselected.setToolTip(" this is for download only selected videos (this will able to download a playlist or multiple playlists)")
        self.pb_downloadselected.clicked.connect(self.clk_downloadselectedcall)
        self.pb_downloadselected.setStyleSheet(self.commenstyle)
        #.......................................................................

        #____________setup of settings button_______________________
        self.pb_settings = QtWidgets.QPushButton(Form)
        self.pb_settings.setGeometry(QtCore.QRect(575, 10, 50, 31))
        self.pb_settings.setObjectName("pb_settings")
        self.pb_settings.setStyleSheet(self.commenstyle)
        #...........................................................

        #__________setup of proggers bar____________________
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QtCore.QRect(10, 485, 301, 30))
        self.progressBar.setStyleSheet(self.commenstyle2)
        self.progressBar.setValue(proggrespresent5)
        #...................................................

        #_____________setup of combobox for select video qulty____________
        self.CB_vqulity = QtWidgets.QComboBox(Form)
        self.CB_vqulity.setObjectName(u"CB_vqulity")
        self.CB_vqulity.setGeometry(QtCore.QRect(300, 120, 324, 22))
        self.CB_vqulity.addItems(["720p","360p","144p"])
        
        self.CB_vqulity.setStyleSheet(self.commenstyle)
        #.................................................................

        #_________setup for stats showing lable_______________________  
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QtCore.QRect(325, 485, 301, 30))
        self.label.setText("")
        self.label.setStyleSheet(self.commenstyle2)
        #...............................................................

        #_______________setup save list button _________________
        self.savelist = QtWidgets.QPushButton(Form)
        self.savelist.setObjectName(u"savelist")
        self.savelist.setGeometry(QtCore.QRect(10, 120, 75, 23))
        self.savelist.setToolTip(" this is for save list of video you add on your hdd ")
        self.savelist.setStyleSheet(self.commenstyle)
        self.savelist.clicked.connect(self.clk_savelist)
        #..........................................................

        #_____________setup of remove selected button__________________
        self.removeselecteditems = QtWidgets.QPushButton(Form)
        self.removeselecteditems.setObjectName(u"removeselecteditems")
        self.removeselecteditems.setGeometry(QtCore.QRect(170, 120, 91, 23))
        self.removeselecteditems.setToolTip(" you can use selected video from list")
        self.removeselecteditems.setStyleSheet(self.commenstyle)
        self.removeselecteditems.clicked.connect(self.clk_removeselected)
        #..................................................................

        #_____________setup load list button________________
        self.loadlistinhdd = QtWidgets.QPushButton(Form)
        self.loadlistinhdd.setObjectName(u"loadlistinhdd")
        self.loadlistinhdd.setGeometry(QtCore.QRect(90, 120, 75, 23))
        self.loadlistinhdd.setToolTip(" this is for load saved list in hdd ")
        self.loadlistinhdd.setStyleSheet(self.commenstyle)
        self.loadlistinhdd.clicked.connect(self.clk_loadlistinhdd)
        #.......................................................

        #___________setup stop events_____________________
        self.stopevents = QtWidgets.QPushButton(Form)
        self.stopevents.setObjectName(u"stopevents")
        self.stopevents.setGeometry(QtCore.QRect(310, 10, 81, 51))
        self.stopevents.clicked.connect(self.stoptreads)
        self.stopevents.setStyleSheet(self.commenstyle)
        #.................................................
        self.msgbox = QtWidgets.QMessageBox(Form)
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    #this func for get keys of videodic dictionary and return list of keys
    def getkeyslist(self,dict):
        list = []
        for key in dict.keys():
            list.append(key)
          
        return list
    #unusset func 
    def clk_addvideocall(self):
        t3 = Thread(target=self.clk_addvideo)
        t3.start()
    #this is for do functionly when clicked add video button
    def clk_addvideo(self):
        """when click addvideo button this func will get pasted youtube url on LE_ulr(LE = line edit)
            then searching for its playlist url or not if playlist all urls in playlist appendto video dictionary
            (calling to appendvideodic func in loop). else just appendcideodic func in one time .after all calling to 
            listviwer func""" 
        self.CB_vqulity.clear()
        self.CB_vqulity.addItems(["720p","360p","144p"])    
        if self.LE_ulr.text() !="":
            if(re.search("playlist",self.LE_ulr.text())):
                print("its playlist")
                pl = pytube.Playlist(self.LE_ulr.text())
                for urli in pl.video_urls:
                    print(urli)
                    self.appendvideodic(urli)
            else:
                self.appendvideodic(self.LE_ulr.text())
                #keyslist = self.getkeyslist(videodic)
            
            keyslist = self.getkeyslist(videodic)
            self.listviwer(keyslist)
            print(videodic)
    #this func for append video title and url to videodic variable
    def appendvideodic(self,url):
        """this func for appendvideo name and url to videodic variable"""
        try:
            vid = YouTube(url)
            videodic[vid.title] = str(url)
            videostate[vid.title] = "q"
        except Exception as e:
            errorexct[0] = str(e)
            self.errorpopup(errorexct[0])
    # this func for show list of keys in video dict in list viewer                
    def listviwer(self,keysofvdic):
        """this func getting key of videodic and creating listview with checkbox"""
        global model
        model = QtGui.QStandardItemModel()
        for i in keysofvdic:
            print(i)
            item = QtGui.QStandardItem(i)
            check = QtCore.Qt.Checked
            item.setCheckState(check)
            item.setText(str(i))
            print(item.text()+" lisetview"+" "+str(item.checkState()))
            
            item.setCheckable(True)
            model.appendRow(item)
            print(model)
        self.lv_url.setModel(model) 
    # this func for get checked items of list viewer
    def getcheckditems(self,models):
        for index in range(models.rowCount()):
            item = models.item(index)
            if item.checkState() == QtCore.Qt.Checked:
                print(item.text()+" getcheck"+" "+str(item.checkState()))
                if(re.search("download finished", item.text())):
                    i = item.text().replace(" download finished","")
                    print(i+" download finished removed")
                    selectedvideos.clear()
                    selectedvideos.append(i)
                #selectedvideos.append(item.text())
                else:
                    selectedvideos.append(item.text())
                    print(item.text())
    #this func for get video link by video title .return link 
    def getvideolink(self,videoname):
        link = videodic.get(videoname)    
        return link
    #this func for do functionly when clicked cownload selected button
    def clk_downloadselectedcall(self):
        try:
            self.getcheckditems(model)
        except:
            traceback.print_exc()
            print("empty list")
        
        yturl = "self.getvideolink(vname)"
        vqulity = self.CB_vqulity.currentText()
        self.thread1 = dowload_selected_tread(url= yturl,qulity= vqulity)
        self.thread1.start()
        self.thread1.calldowloadvideo.connect(self.downloadytvideo)
        self.thread1.callerror.connect(self.errorpopup)
    #this func for do functionly when clicked download video button
    def clk_dowloadvideo(self):
        vurl = self.LE_ulr.text()
        vqulity = self.CB_vqulity.currentText()
        print("vq global "+ str(vqultybyitagdic))
        try:
            q = YouTube(vurl)
            ress = []
            #for i in q.streams: print(str(i.resolution))
            itags = q.streams.filter(adaptive=True)
            itagsstr = []
            if vqulity in vqultybyitagdic.keys():
                print(str(vqultybyitagdic.get(vqulity)))
                selecteditag = vqultybyitagdic.get(vqulity)
                svqulity = selecteditag
            else:
                svqulity = self.CB_vqulity.currentText()    
                for s in q.streams.filter(progressive=True):
                    try:
                        print("resolution: " + s.resolution)
                        print("itag " + str(s))    
                                
                    except:
                        traceback.print_exc()
                    else:
                        ress.append(s.resolution)
                        
                    print(ress)        
                print(vqulity)
                if vqulity in ress:
                    pass
                else:
                    svqulity = "720p"
                        

            print(str(svqulity)+" downloading")
            print(type(askeverytime[0]))
            if usecustomedowpath[0] == "true"and vurl !="":
                downloadpath[0] = customdownloadpathstr[0]
                print("downpath in usecustom path "+ downloadpath[0])
            if askeverytime[0]== "true" and vurl !="":
                #downloadpath.clear()
                downpath1 = QtWidgets.QFileDialog.getExistingDirectory(None, 'download path',mydir)
                downloadpath[0] = downpath1
                
            if vurl !="":
                print(downloadpath[0])
                self.downloadytvideo(vurl,svqulity)
        except Exception as e:
            traceback.print_exc()
            print(str(e))
            errorexct[0] = str(e)
            self.errorpopup(errorexct[0])        
    #unused
    def setcolor_state(self,model,color,vdeoname):
        color1 = str(color)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor('#7fc97f'))
        model1=model 
        for i in range(model1.rowCount()):
            item = model.item(i)
            if item.text() == vdeoname:
                model.item(i).setBackground(brush)
                print("seting color to list viewer items")
                model.item(i).setText(str(vdeoname)+" download finished")
    #unused            
    def downloadytvideocall(self,url,videoqulity):
        t1 = Thread(target=self.downloadytvideo,args=(url,videoqulity))
        t1.start()
    #this func for call video download thread
    def downloadytvideo(self,url,videoqulity):
        self.thread1 = video_dowload_tread(url= url,qulity= videoqulity)
        
        
        self.thread1.start()
        self.thread1.change_value.connect(self.setProgressVal)
        self.thread1.finishvname.connect(self.downfineshscallback)
        self.thread1.callerror.connect(self.errorpopup)
    #this func for do things after download finished
    def downfineshscallback(self,finishvnam):
        print("download finished "+ finishvnam)
        try:
            self.setcolor_state(model,"blue",finishvnam)
        except:
            pass    
        self.label.setText(finishvnam+" download finished")
        videostate[finishvnam] = "downloaded"
        #d_finished1 = True
        d_finished1[0] = True
        '''try:
            self.thread1.setTerminationEnabled(True)
            self.thread1.terminate()
            d_finished1[0] = True
            self.progressBar.setValue(0)
            #self.label.setText("Stoped")
        except Exception as e:
            traceback.print_exc()
            print(e)
            errorexct[0] = str(e)
            print(errorexct)
            self.errorpopup(str(errorexct))'''
    #this func for set proggres bar value
    def setProgressVal(self,prval,downloadspeed):
        print(str(prval)+" %")
        self.progressBar.setValue(prval)
        self.label.setText(downloadspeed)
    #this func for do functionly when clicked save list button
    def clk_savelist(self):
        print("save list in to HDD")
        print(mydir)
        path =  mydir+"/saves"
        savefilename = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File',path)               
        if os.path.exists(path)==False:
            print("not exist have to create")  
            os.mkdir(path)
        else:
            if(savefilename !=""):
                savepath = path
                pickle.dump((videodic,videostate),open(savefilename[0]+".dytd","wb"))
                print(savefilename[0])
    #this func for do functionly when clicked remove selected button          
    def clk_removeselected(self):
        print("remove selected")
        '''try:'''
        self.getcheckditems(model)
        print(selectedvideos)
        for i in selectedvideos:
            print(i + str("fsafas"))
            try:    
                videodic.pop(i)
            except Exception as e:
                errorexct[0] = str(e)
                self.errorpopup(str(errorexct))
            else:        
                print(str(i)+"removed")
        self.listviwer(videodic)
        selectedvideos.clear()
        """except:
            print("empty")"""
    #this func for do functionly when clicked load button
    def clk_loadlistinhdd(self):
        path =  mydir+"/saves"
        openfilename = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File',path)
        print(openfilename[0])
        if openfilename[0] !="":
            datainfile = pickle.load(open(openfilename[0],"rb"))
            vdictinfile = datainfile[0]
            videostateinfile = datainfile[1]
            videodic.update(vdictinfile)
            videostate.update(videostateinfile)
            self.listviwer(videodic)
            print(str(vdictinfile))
            print(str(videostateinfile))
    #this func for meke settings values on reg
    def makesettingvals(self):
        self.settingval = QSettings("Dragon yt downloader","settings vals")
    #this func for setting up default settings on reg
    def setdefsettingvals(self):
        settingkeylist = self.settingval.allKeys()
        #print(str(len(settingkeylist)))
        if(settingkeylist == None):
            print("making regedit")
            self.settingval.setValue("borderroundness","1px")
            self.settingval.setValue("bordersize","2px")
            self.settingval.setValue("textcolor","#ff0000")
            self.settingval.setValue("askeverytime",False)
            self.settingval.setValue("usecustomdownpath",False)
            self.settingval.setValue("bordercolor","#ff0000")
            
        elif len(settingkeylist)==0:
            self.settingval.setValue("borderroundness","1px")
            self.settingval.setValue("bordersize","2px")
            self.settingval.setValue("textcolor","#ff0000") 
            self.settingval.setValue("askeverytime",False)
            self.settingval.setValue("usecustomdownpath",False)
            self.settingval.setValue("bordercolor","#ff0000")    
    #this func for get settings values in reg and seve values to vars 
    def getsettingvals(self):
        self.settingval = QSettings("Dragon yt downloader","settings vals")
        borderroundness[0] = str(self.settingval.value("borderroundness"))
        bordersize[0] = str(self.settingval.value("bordersize"))
        textcolor[0] = str(self.settingval.value("textcolor"))
        askeverytime[0] = self.settingval.value("askeverytime")
        usecustomedowpath[0] = self.settingval.value("usecustomdownpath")
        customdownloadpathstr[0] =self.settingval.value("customedownloadpathstr")
        bordercolor[0] = self.settingval.value("bordercolor")
        print( borderroundness[0] + bordersize[0]+bordercolor[0]+str(askeverytime[0]))
        self.stylesheet =( "background-image: url(D:/youtube downloader/assets/bacground image.png);"+ 
        "background-repeat: no-repeat;"+ 
        "background-position: center;")
        self.commenstyle =("*{border: "+bordersize[0]+" solid "+bordercolor[0]+";"+
                        "color: "+textcolor[0]+";"+
                        "border-radius: "+borderroundness[0]+";}"+
                        "*:hover{background: 'blue';}")    
        self.textinputstyle = ("*{border: "+bordersize[0]+" solid "+bordercolor[0]+";"+
                            "color: "+textcolor[0]+";"+
                            "border-radius: "+borderroundness[0]+";}"+
                            "*:hover{background: 'blue';}")        
        self.commenstyle2 =  ("*{border: "+bordersize[0]+" solid "+bordercolor[0]+";"+
                            "text-align: center;"+
                            "color: "+textcolor[0]+";"+
                            "border-radius: "+borderroundness[0]+";}")
    #this func for do thing if error occurred
    def errorpopup(self,errorexct):
        print(str(errorexct))
        self.errmsg.showMessage(str(errorexct))
        d_finished1[0] = True
    #this func for stop running thread
    def stoptreads(self):
        print("stoptreads called")
        try:
            self.thread1.setTerminationEnabled(True)
            self.thread1.terminate()
            d_finished1[0] = True
            self.progressBar.setValue(0)
            self.label.setText("Stoped")
        except Exception as e:
            traceback.print_exc()
            print(e)
            errorexct[0] = str(e)
            print(errorexct)
            self.errorpopup(str(errorexct))
    #this func for get qulitys in paseted video
    def getvideosinstreamscall(self):
        print("getting video qulitys")
        self.thread1 = getvideoqultys_tread(url=str(self.LE_ulr.text()))

        self.thread1.start()
        self.thread1.setqltycombobox.connect(self.setqcombobox)
        self.thread1.callerror.connect(self.errorpopup)
    #this func for set combobox list
    def setqcombobox(self,qltylist):

        self.CB_vqulity.addItems(qltylist)
    
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("DRAGON YT DOWNLOADER", "DRAGON YT DOWNLOADER"))
        self.pb_addurl.setText(_translate("Form", "Add URL"))
        self.pb_downloadvideo.setText(_translate("Form", "Download Video"))
        self.pb_downloadselected.setText(_translate("Form", "Download Selected"))
        self.pb_settings.setText(_translate("Form", "settings"))
        self.savelist.setText(_translate("Form", "Save List"))
        self.loadlistinhdd.setText(_translate("Form", "Load List"))
        self.removeselecteditems.setText(_translate("Form", "Remove selected"))
        self.stopevents.setText(_translate("Frame", "Stop Events"))
        #self.selectall.setText(_translate("Form", "Select All"))
        Form.setStyleSheet("border: 1px solid black;"+"background-color: Black;")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
