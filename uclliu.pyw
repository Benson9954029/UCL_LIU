# -*- coding: utf-8 -*-
VERSION=1.37
import portalocker
import os
import sys
import gtk
from gtk import gdk 
    
import gobject
import hashlib
import php
# trad to simp or simp to trad
import stts 
import re
import win32api
import configparser
#,,,z ,,,x 用thread去輸出字
import thread
import base64
import random
# 播放打字音用
import pyaudio
import audioop
import wave
paudio_player = pyaudio.PyAudio()
# 播放打字音用
#from pydub import AudioSegment
#from pydub.playback import play



# Fix exit crash problem
# 改用 
# https://stackoverflow.com/questions/23727539/runtime-error-in-python/24035224#24035224
# 用來取反白字
# https://stackoverflow.com/questions/1007185/how-to-retrieve-the-selected-text-from-the-active-window
# import win32ui
# https://superuser.com/questions/1120624/run-script-on-any-selected-text

# 額外出字處理的 app
f_arr = [ "putty","pietty","pcman","xyplorer","kinza.exe","oxygennotincluded.exe","iedit.exe","iedit_.exe" ]
f_big5_arr = [ "zip32w","daqkingcon.exe","EWinner.exe" ]
# 不使用肥米的 app
# 2021-03-19 2077 也不能使用肥米
# 2021-07-03 vncviewer.exe 不需要肥米
f_pass_app = [ "mstsc.exe","Cyberpunk2077.exe","vncviewer.exe" ]

# 2019-10-20 增加出字模式
UCL_PIC_BASE64 = "AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAMIOAADCDgAAAAAAAAAAAAD////////////////////////////////////////////////////////////////////////////////////////////////+/v7//Pz8//v7+//7+/v//f39////////////////////////////////////////////////////////////1s7B/1pVU/9PT0//Tk5Q/56rtP/Cua7/bGlp/2pqa/9tbGz/ampp/25xd//R2eL//////////////////////8O1of8kIyn/fYCD/0A0Lf9vgZD/kIJv/yUrMv9WUEr/FBcd/19eXv8fHR//q7zL///////////////////////CtKH/MDE4/6qwt/9zZFf/boCP/49/bf9VZXf/v7Ok/y0zP//T09P/QDcw/6q7yv//////////////////////w7Wj/yEcGv8pKy//OTUy/3GCkf+Pf23/VWV3/7+zo/8sMz//09PS/0A3MP+qu8r//////////////////////8KzoP84O0H/b2to/y4pJf9wgpH/j4Bt/1BfcP+1qpv/KjA7/8fHx/89NC//qrvK///////////////////////Cs6D/O0FM/9HS0f9IOi//boGQ/5KCcP8UFhn/Ly0p/w0PEv80MzP/FRcc/62+zP//////////////////////wrOh/zI1Ov9hXFT/AwAB/3GDk/+QgW//NkBK/6iqrP+trKz/qqqq/62vs//l6u///////////////////////76vnf8aFhb/Mzs+/0M9OP9wgpD/j39t/1Fhc//7//////////////////////////////////////////////+vnYv/QUtX/9ff3/96alv/bX+P/49/bf9RYHL/+/7/////////////v7Ko/5ifqf/7/v//////////////////inhn/19vgf//////fGpa/21/jv+Of23/UWBy//v+/////////////4Z0Yv9KWmv/+f3/////////////+/bv/1pNQv+Kmaf/samg/z01L/93iZn/n5B+/ygrMf93eXr/fHx8/3p4dv8vKib/eIqc//////////////////37+P/Mycf/5+rt/9HMxv+zs7X/3uPo/+zo4/+4trT/srKy/7Kysv+ysrL/tba5/+Tp7v//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="
DEFAULT_OUTPUT_TYPE = "DEFAULT"
#BIG5
#PASTE

#import pywinauto             
#pwa = pywinauto.keyboard

my = php.kit()

# 2021-08-08 將簡、繁轉換抽離成獨立 class
mystts = stts.kit()

reload(sys)
sys.setdefaultencoding('UTF-8')

# Debug 模式
is_DEBUG_mode = False



message = ("\nUCLLIU 肥米輸入法\nBy 羽山秋人(http://3wa.tw)\nVersion: %s\n\n若要使用 Debug 模式：uclliu.exe -d\n" % (VERSION));

def about_uclliu():
  _msg_text = ("肥米輸入法\n\n作者：羽山秋人 (http://3wa.tw)\n版本：%s" % VERSION)
  _msg_text += "\n\n熱鍵提示：\n\n"
  _msg_text += "「,,,VERSION」目前版本\n"
  _msg_text += "「,,,UNLOCK」回到正常模式\n"
  _msg_text += "「,,,LOCK」進入遊戲模式\n"
  _msg_text += "「,,,C」簡體模式\n"
  _msg_text += "「,,,T」繁體模式\n"
  _msg_text += "「,,,S」UI變窄\n"
  _msg_text += "「,,,L」UI變寬\n"
  _msg_text += "「,,,+」UI變大\n"
  _msg_text += "「,,,-」UI變小\n"
  _msg_text += "「,,,X」框字的字根轉回文字\n"
  _msg_text += "「,,,Z」框字的文字變成字根\n"
  return _msg_text  

if len(sys.argv)!=2:
  print( my.utf8tobig5(message) );
elif sys.argv[1]=="-d":
  is_DEBUG_mode = True

def debug_print(data):
  global is_DEBUG_mode
  if is_DEBUG_mode == True:
    print(data)
    
def md5_file(fileName):
    """Compute md5 hash of the specified file"""
    m = hashlib.md5()
    try:
        fd = open(fileName,"rb")
    except IOError:
        debug_print("Reading file has problem:", filename)
        return
    x = fd.read()
    fd.close()
    m.update(x)
    return m.hexdigest()


#PWD=my.pwd()   
PWD = os.path.dirname(os.path.realpath(sys.argv[0]))
#my.file_put_contents("c:\\temp\\aaa.txt",PWD);
#debug_print(PWD)
#sys.exit(0)

#此是防止重覆執行
#if os.path.isdir("C:\\temp") == False:
#  os.mkdir("C:\\temp")
check_file_run = open(PWD + '\\UCLLIU.lock', "a+")
try:  
  portalocker.lock(check_file_run, portalocker.LOCK_EX | portalocker.LOCK_NB)
except:
  md = gtk.MessageDialog(None, 
          gtk.DIALOG_DESTROY_WITH_PARENT, 
          gtk.MESSAGE_QUESTION, 
          gtk.BUTTONS_OK, "【肥米輸入法】已執行...")          
  md.set_position(gtk.WIN_POS_CENTER)
  response = md.run()            
  if response == gtk.RESPONSE_OK or response == gtk.RESPONSE_DELETE_EVENT:
    md.destroy()
    ctypes.windll.user32.PostQuitMessage(0)
    #atexit.register(cleanup)
    #os.killpg(0, signal.SIGKILL)
    sys.exit(0)
         
import ctypes
import pythoncom, pyHook
from pyHook import HookManager
from pyHook.HookManager import HookConstants 

import win32clipboard
import pango
import SendKeysCtypes
import time

#http://wiki.alarmchang.com/index.php?title=Python_%E5%AD%98%E5%8F%96_Windows_%E7%9A%84%E5%89%AA%E8%B2%BC%E7%B0%BF_ClipBoard_%E7%AF%84%E4%BE%8B
import win32gui
import win32process
import psutil
#import win32com
import win32con
#import win32com.client

#2018-07-13 1.12版增加
#檢查 C:\temp\UCLLIU.ini 初始化設定檔
#取螢幕大小

#2019-03-02 調整，將 UCLLIU.ini 跟隨在 UCLLIU.exe 旁
INI_CONFIG_FILE = 'C:\\temp\\UCLLIU.ini'
if my.is_file(INI_CONFIG_FILE):
  my.copy(INI_CONFIG_FILE,PWD+"\\UCLLIU.ini")
  my.unlink(INI_CONFIG_FILE)
INI_CONFIG_FILE = PWD + "\\UCLLIU.ini" 

#user32 = ctypes.windll.user32
#user32.SetProcessDPIAware()

#screen_width=user32.GetSystemMetrics(0)
#screen_height=user32.GetSystemMetrics(1)
#debug_print("screen width, height : %s , %s" % (screen_width,screen_height))
#window = gtk.Window()
#From : https://www.familylifemag.com/question/701406/how-do-i-get-monitor-resolution-in-python
myScreensObj = gtk.gdk.Screen()
myScreenStatus = {
  "main_monitor" : 0, # 面積大的當作 main
  "first_time_x": 0, # 系統初始位置，使用下面主螢幕中心點位置移至右下150x150
  "first_time_y": 0,
  "screens": [
    # x,y,w,h,area, c_x,c_y
  ]
}
debug_print("get_n_monitors(): %d\n" % (myScreensObj.get_n_monitors()));
#debug_print(myScreensObj.get_monitor_geometry(0)); #gtk.gdk.Rectangle(1280, 0, 2560, 1080)
#debug_print(myScreensObj.get_monitor_geometry(1)); #gtk.gdk.Rectangle(0, 59, 1280, 1024)

for i in range(0,myScreensObj.get_n_monitors()):
  d = {
    "x": myScreensObj.get_monitor_geometry(i)[0],
    "y": myScreensObj.get_monitor_geometry(i)[1],
    "w": myScreensObj.get_monitor_geometry(i)[2],
    "h": myScreensObj.get_monitor_geometry(i)[3],
    "area": (myScreensObj.get_monitor_geometry(i)[2] * myScreensObj.get_monitor_geometry(i)[3]),
    "c_x": (myScreensObj.get_monitor_geometry(i)[0] + (myScreensObj.get_monitor_geometry(i)[2] / 2)),
    "c_y": (myScreensObj.get_monitor_geometry(i)[1] + (myScreensObj.get_monitor_geometry(i)[3] / 2)),  
  }
  myScreenStatus["screens"].append(d);
  if i == 0:
    myScreenStatus["main_monitor"] = i;
    #調整第一次執行的中心位置
    myScreenStatus["first_time_x"] = d["c_x"]+150
    myScreenStatus["first_time_y"] = d["c_y"]+150    
  else:
    _is_bigger = True
    for j in range(0,len(myScreenStatus["screens"])-1):
      if myScreenStatus["screens"][j] > d["area"]:
        _is_bigger = False;
        break;
    if _is_bigger == True:
      myScreenStatus["main_monitor"]=i; # 最大螢幕易主
      myScreenStatus["first_time_x"] = d["c_x"]+150
      myScreenStatus["first_time_y"] = d["c_y"]+150
      
debug_print(my.json_encode(myScreenStatus));
screen_width = gtk.gdk.screen_width()
screen_height = gtk.gdk.screen_height()

debug_print("screen_width: %d\n" % (screen_width));
debug_print("screen_height: %d\n" % (screen_height));


  
config = configparser.ConfigParser()
config['DEFAULT'] = {
                      "X": myScreenStatus["first_time_x"],
                      "Y": myScreenStatus["first_time_y"],
                      "ALPHA": "1", #嘸蝦米全顯示時時的初值
                      "SHORT_MODE": "0", #0:簡短畫面，或1:長畫面
                      "ZOOM": "1", #整體比例大小
                      "SEND_KIND_1_PASTE": "", #出字模式1
                      "SEND_KIND_2_BIG5": "", #出字模式2
                      "SEND_KIND_3_NOUCL":"", #Force no UCL
                      "KEYBOARD_VOLUME": "30", #打字聲音量，0~100
                      "SP": "0", #短根
                      "CTRL_SP": "0", #使用CTRL+SPACE換肥米
                      "PLAY_SOUND_ENABLE": "0" #打字音
                    };
if my.is_file(INI_CONFIG_FILE):
  _config = configparser.ConfigParser()
  _config.read(INI_CONFIG_FILE)    
  for k in _config['DEFAULT'].keys(): # ['X','Y','ALPHA','ZOOM','SHORT_MODE','SEND_KIND_1_PASTE','SEND_KIND_2_BIG5'] 
    if k in config['DEFAULT'].keys():
      config['DEFAULT'][k]=_config['DEFAULT'][k]
      
config['DEFAULT']['X'] = str(int(config['DEFAULT']['X']));
config['DEFAULT']['Y'] = str(int(config['DEFAULT']['Y'])); 
config['DEFAULT']['ALPHA'] = "%.2f" % ( float(config['DEFAULT']['ALPHA'] ));
config['DEFAULT']['SHORT_MODE'] = str(int(config['DEFAULT']['SHORT_MODE']));
config['DEFAULT']['ZOOM'] = "%.2f" % ( float(config['DEFAULT']['ZOOM'] ));
config['DEFAULT']['SEND_KIND_1_PASTE'] = str(config['DEFAULT']['SEND_KIND_1_PASTE']);
config['DEFAULT']['SEND_KIND_2_BIG5'] = str(config['DEFAULT']['SEND_KIND_2_BIG5']);
config['DEFAULT']['KEYBOARD_VOLUME'] = str(int(config['DEFAULT']['KEYBOARD_VOLUME']));
config['DEFAULT']['SP'] = str(int(config['DEFAULT']['SP']));
config['DEFAULT']['CTRL_SP'] = str(int(config['DEFAULT']['CTRL_SP']));
config['DEFAULT']['PLAY_SOUND_ENABLE'] = str(int(config['DEFAULT']['PLAY_SOUND_ENABLE']));

# merge f_arr and f_big5_arr
config['DEFAULT']['SEND_KIND_1_PASTE'] = my.trim(config['DEFAULT']['SEND_KIND_1_PASTE'])
config['DEFAULT']['SEND_KIND_1_PASTE'] =  my.str_replace("\"","",config['DEFAULT']['SEND_KIND_1_PASTE'])
config['DEFAULT']['SEND_KIND_2_BIG5'] = my.trim(config['DEFAULT']['SEND_KIND_2_BIG5'])
config['DEFAULT']['SEND_KIND_2_BIG5'] =  my.str_replace("\"","",config['DEFAULT']['SEND_KIND_2_BIG5'])
config['DEFAULT']['SEND_KIND_3_NOUCL'] =  my.str_replace("\"","",config['DEFAULT']['SEND_KIND_3_NOUCL'])

if config['DEFAULT']['SEND_KIND_1_PASTE'] != "": 
  f_arr = f_arr + my.explode(",",config['DEFAULT']['SEND_KIND_1_PASTE'])
if config['DEFAULT']['SEND_KIND_2_BIG5'] != "": 
  f_big5_arr = f_big5_arr + my.explode(",",config['DEFAULT']['SEND_KIND_2_BIG5'])
if config['DEFAULT']['SEND_KIND_3_NOUCL'] != "": 
  f_pass_app = f_pass_app + my.explode(",",config['DEFAULT']['SEND_KIND_3_NOUCL'])  


if int(config['DEFAULT']['KEYBOARD_VOLUME']) < 0:
  config['DEFAULT']['KEYBOARD_VOLUME'] = "0"
if int(config['DEFAULT']['KEYBOARD_VOLUME']) > 100:
  config['DEFAULT']['KEYBOARD_VOLUME'] = "100"
  
#debug_print(f_arr)
#debug_print(f_big5_arr)

# array_unique
# 2021-07-22 防止使用者在 f_arr 這些打多的逗號、空白
f_arr = my.array_remove_empty_and_trim(list(set(f_arr)))
f_big5_arr = my.array_remove_empty_and_trim(list(set(f_big5_arr)))
f_pass_app = my.array_remove_empty_and_trim(list(set(f_pass_app)))

#debug_print(f_arr)
#debug_print(f_big5_arr)

if float(config['DEFAULT']['ALPHA'])>=1:
  config['DEFAULT']['ALPHA']="1"
if float(config['DEFAULT']['ALPHA'])<=0.1:
  config['DEFAULT']['ALPHA']="0.1"
  
if int(config['DEFAULT']['SHORT_MODE'])>=1:
  config['DEFAULT']['SHORT_MODE']="1"
if int(config['DEFAULT']['SHORT_MODE'])<=0:
  config['DEFAULT']['SHORT_MODE']="0"
  
if float(config['DEFAULT']['ZOOM'])>=3:
  config['DEFAULT']['ZOOM']="3"
if float(config['DEFAULT']['ZOOM'])<=0.1:
  config['DEFAULT']['ZOOM']="0.1"

if int(config['DEFAULT']['SP'])<=0:
  config['DEFAULT']['SP']="0"  
else:
  config['DEFAULT']['SP']="1"  
  
if int(config['DEFAULT']['CTRL_SP'])<=0:
  config['DEFAULT']['CTRL_SP']="0"  
else:
  config['DEFAULT']['CTRL_SP']="1"    

if int(config['DEFAULT']['PLAY_SOUND_ENABLE'])<=0:
  config['DEFAULT']['PLAY_SOUND_ENABLE']="0"  
else:
  config['DEFAULT']['PLAY_SOUND_ENABLE']="1"  

# GUI Font
GLOBAL_FONT_FAMILY = "Mingliu,Malgun Gothic,roman" #roman
GUI_FONT_12 = my.utf8tobig5("%s %d" % (GLOBAL_FONT_FAMILY,int( float(config['DEFAULT']['ZOOM'])*12) ));
GUI_FONT_14 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*14) ));
GUI_FONT_16 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*16) ));
GUI_FONT_18 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*18) ));
GUI_FONT_20 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*20) ));
GUI_FONT_22 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*22) ));
GUI_FONT_26 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*26) ));
# print config setting
debug_print("UCLLIU.ini SETTING:")
debug_print("X:%s" % (config["DEFAULT"]["X"]))
debug_print("Y:%s" % (config["DEFAULT"]["Y"]))
debug_print("ALPHA:%s" % (config["DEFAULT"]["ALPHA"]))
debug_print("SHORT_MODE:%s" % (config["DEFAULT"]["SHORT_MODE"]))
debug_print("ZOOM:%s" % (config["DEFAULT"]["ZOOM"]))
debug_print("SEND_KIND_1_PASTE:%s" % (config["DEFAULT"]["SEND_KIND_1_PASTE"]))
debug_print("SEND_KIND_2_BIG5:%s" % (config["DEFAULT"]["SEND_KIND_2_BIG5"]))
debug_print("SP:%s" % (config["DEFAULT"]["SP"]))

def saveConfig():
  global config
  global INI_CONFIG_FILE
  with open(INI_CONFIG_FILE, 'w') as configfile:
    config.write(configfile)
def run_big_small(kind):
  global config
  global GLOBAL_FONT_FAMILY
  global GUI_FONT_12
  global GUI_FONT_14
  global GUI_FONT_16
  global GUI_FONT_18
  global GUI_FONT_20
  global GUI_FONT_22
  global GUI_FONT_26
  global simple_btn
  global x_btn
  global gamemode_btn
  global uclen_btn
  global hf_btn
  global type_label
  global word_label
  kind = float(kind)
  if kind > 0:
    if float(config['DEFAULT']['ZOOM']) < 3:
      config['DEFAULT']['ZOOM'] = str(float(config['DEFAULT']['ZOOM'])+kind)
  else:
    if float(config['DEFAULT']['ZOOM']) > 0.3:
      config['DEFAULT']['ZOOM'] = str(float(config['DEFAULT']['ZOOM'])+kind)
  
  GUI_FONT_12 = my.utf8tobig5("%s %d" % (GLOBAL_FONT_FAMILY,int( float(config['DEFAULT']['ZOOM'])*12) ));
  GUI_FONT_14 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*14) ));
  GUI_FONT_16 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*16) ));
  GUI_FONT_18 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*18) ));
  GUI_FONT_20 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*20) ));
  GUI_FONT_22 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*22) ));
  GUI_FONT_26 = my.utf8tobig5("%s bold %d" % (GLOBAL_FONT_FAMILY,int(float(config['DEFAULT']['ZOOM'])*26) ));  
  
  if is_simple():
    simple_btn.set_size_request(0,int( float(config['DEFAULT']['ZOOM'])*40))  
  simple_label=simple_btn.get_child()
  simple_label.modify_font(pango.FontDescription(GUI_FONT_16))
  
  x_label=x_btn.get_child()
  x_label.modify_font(pango.FontDescription(GUI_FONT_14))  
  x_btn.set_size_request(int( float(config['DEFAULT']['ZOOM'])*40),int( float(config['DEFAULT']['ZOOM'])*40))

  gamemode_label=gamemode_btn.get_child()
  gamemode_label.modify_font(pango.FontDescription(GUI_FONT_12))
  gamemode_btn.set_size_request(int( float(config['DEFAULT']['ZOOM'])*80),int( float(config['DEFAULT']['ZOOM'])*40))
    
  uclen_label=uclen_btn.get_child()
  uclen_label.modify_font(pango.FontDescription(GUI_FONT_22))
  uclen_btn.set_size_request(int(float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40 ))
  
  hf_label=hf_btn.get_child()
  hf_label.modify_font(pango.FontDescription(GUI_FONT_22))
  hf_btn.set_size_request(int( float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40) )
  
  type_label.modify_font(pango.FontDescription(GUI_FONT_22))
  type_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*100) ,int( float(config['DEFAULT']['ZOOM'])*40) )
 
  word_label.modify_font(pango.FontDescription(GUI_FONT_20))
  word_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*350),int( float(config['DEFAULT']['ZOOM'])*40))
          
  saveConfig()
    
def play_sound():  
  global m_play_song
  global max_thread___playMusic_counts
  global step_thread___playMusic_counts
  global NOW_VOLUME
  global o_song
  global PWD
  
  m_play_song.extend( [ random.choice(o_song.keys()) ])
  if len(o_song.keys())!=0 and step_thread___playMusic_counts < max_thread___playMusic_counts:
    step_thread___playMusic_counts = step_thread___playMusic_counts + 1                  
    
    thread.start_new_thread( thread___playMusic,(NOW_VOLUME,))
                            
def run_short():
  global config
  global word_label
  global type_label
  global gamemode_btn
  word_label.set_visible(False)
  type_label.set_visible(False)
  gamemode_btn.set_visible(False)
  config["DEFAULT"]["SHORT_MODE"]="1"
  saveConfig()
def run_long():
  global word_label
  global type_label
  global gamemode_btn
  word_label.set_visible(True)
  type_label.set_visible(True)
  gamemode_btn.set_visible(True)
  config["DEFAULT"]["SHORT_MODE"]="0"
  type_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*100),int( float(config['DEFAULT']['ZOOM'])*40))
  word_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*385),int( float(config['DEFAULT']['ZOOM'])*40))
  saveConfig()
  
saveConfig()    
#check if exists tab cin json
is_need_trans_tab = False
is_need_trans_cin = False
is_all_fault = False
#my.unlink("liu.json")
#my.unlink("liu.cin")
if my.is_file(PWD + "\\liu.json") == False:
  if my.is_file(PWD + "\\liu.cin") == False:
    if my.is_file(PWD + "\\liu-uni.tab") == False:
      is_all_fault=True
    else:
      is_need_trans_tab=True
      is_need_trans_cin=True   
  else:
    is_need_trans_cin=True  

if is_all_fault==True and my.is_file("C:\\windows\\SysWOW64\\liu-uni.tab")==True:
  my.copy("C:\\windows\\SysWOW64\\liu-uni.tab",PWD+"\\liu-uni.tab")
  is_all_fault=False
  is_need_trans_tab=True
  is_need_trans_cin=True
  
if is_all_fault==True and my.is_file("C:\\Program Files\\BoshiamyTIP\\liu-uni.tab")==True:
  my.copy("C:\\Program Files\\BoshiamyTIP\\liu-uni.tab",PWD+"\\liu-uni.tab")
  is_all_fault=False
  is_need_trans_tab=True
  is_need_trans_cin=True

# 2019-04-13 加入 小小輸入法臺灣包2018年版wuxiami.txt，http://fygul.blogspot.com/2018/05/yong-tw2018.html 裡linux包中的/tw/wuxiami.txt
if is_all_fault==True and my.is_file(PWD + "\\wuxiami.txt")==True:
  debug_print("Run wuxiami.txt ...");
  my.copy(PWD+"\\wuxiami.txt",PWD+"\\liu.cin");
  data = my.file_get_contents(PWD+"\\liu.cin");
  m = my.explode("#修正錯誤：2018-4-15,17",data);
  data = my.trim(m[1])
  data = my.str_replace("\t"," ",data);
  data = my.implode("\n",m);  
  # 修正 cin 用的表頭
  data = '''%gen_inp
%ename liu
%cname 肥米
%encoding UTF-8
%selkey 0123456789
%keyname begin
a Ａ
b Ｂ
c Ｃ
d Ｄ
e Ｅ
f Ｆ
g Ｇ
h Ｈ
i Ｉ
j Ｊ
k Ｋ
l Ｌ
m Ｍ
n Ｎ
o Ｏ
p Ｐ
q Ｑ
r Ｒ
s Ｓ
t Ｔ
u Ｕ
v Ｖ
w Ｗ
x Ｘ
y Ｙ
z Ｚ
, ，
. ．
' ’
[ 〔
] 〔
%keyname end
%chardef begin
''' + data +"\n%chardef end\n";
  my.file_put_contents(PWD+"\\liu.cin",data);
  is_need_trans_tab = False;
  is_need_trans_cin = True;
  is_all_fault = False;  
# 2018-06-25 加入 RIME liur_trad.dict.yaml 表格支援
if is_all_fault==True and my.is_file(PWD + "\\liur_trad.dict.yaml")==True:
  debug_print("Run Rime liur_trad.dict.yaml ...");
  my.copy(PWD+"\\liur_trad.dict.yaml",PWD+"\\liu.cin");
  data = my.file_get_contents(PWD+"\\liu.cin");
  # 2021-03-21
  # 不知道為啥 rime 要把好字的打改成 ~ 開頭@_@?
  data = my.str_replace("~","",data); 
  # 2021-03-21
  # 修正 ... 因為字根裡也有 ... 笑死 XD
  m = my.explode("#字碼格式: 字 + Tab + 字碼",data);
  data = my.trim(m[1])
  data = my.str_replace("\t"," ",data);
  # swap field
  m = my.explode("\n",data);
  for i in range(1,len(m)):
    d = my.explode(" ",m[i]);
    m[i] = "%s %s" % (d[1],d[0]);
  data = my.implode("\n",m);  
  # 修正 cin 用的表頭
  data = '''%gen_inp
%ename liu
%cname 肥米
%encoding UTF-8
%selkey 0123456789
%keyname begin
a Ａ
b Ｂ
c Ｃ
d Ｄ
e Ｅ
f Ｆ
g Ｇ
h Ｈ
i Ｉ
j Ｊ
k Ｋ
l Ｌ
m Ｍ
n Ｎ
o Ｏ
p Ｐ
q Ｑ
r Ｒ
s Ｓ
t Ｔ
u Ｕ
v Ｖ
w Ｗ
x Ｘ
y Ｙ
z Ｚ
, ，
. ．
' ’
[ 〔
] 〔
%keyname end
%chardef begin
''' + data +"\n%chardef end\n";
  my.file_put_contents(PWD+"\\liu.cin",data);
  is_need_trans_tab = False;
  is_need_trans_cin = True;
  is_all_fault = False;
  
# 2018-04-08 加入 terry 表格支援
if is_all_fault==True and my.is_file(PWD + "\\terry_boshiamy.txt")==True:
  #將 terry_boshiamy.txt 轉成 正常的 liu.cin、然後轉成 liu.json
  debug_print("Run terry ...")
  my.copy(PWD+"\\terry_boshiamy.txt",PWD+"\\liu.cin");
  data = my.file_get_contents(PWD+"\\liu.cin");
  m = my.explode("## 無蝦米-大五碼-常用漢字：",data);
  data = my.trim(m[1])
  # 修正 cin 用的表頭
  data = '''%gen_inp
%ename liu
%cname 肥米
%encoding UTF-8
%selkey 0123456789
%keyname begin
a Ａ
b Ｂ
c Ｃ
d Ｄ
e Ｅ
f Ｆ
g Ｇ
h Ｈ
i Ｉ
j Ｊ
k Ｋ
l Ｌ
m Ｍ
n Ｎ
o Ｏ
p Ｐ
q Ｑ
r Ｒ
s Ｓ
t Ｔ
u Ｕ
v Ｖ
w Ｗ
x Ｘ
y Ｙ
z Ｚ
, ，
. ．
' ’
[ 〔
] 〔
%keyname end
%chardef begin
''' + data +"\n%chardef end\n";
  my.file_put_contents(PWD+"\\liu.cin",data);
  is_need_trans_tab = False;
  is_need_trans_cin = True;
  is_all_fault = False;
  
  
# 2018-03-22 加入 fcitx 輸入法支援
if is_all_fault==True and my.is_file(PWD + "\\fcitx_boshiamy.txt")==True:
  #將 fcitx_boshiamy.txt 轉成 正常的 liu.cin、然後轉成 liu.json
  debug_print("Run fcitx ...")
  my.copy(PWD+"\\fcitx_boshiamy.txt",PWD+"\\liu.cin");
  data = my.file_get_contents(PWD+"\\liu.cin");
  data = my.str_replace("键码=,.'abcdefghijklmnopqrstuvwxyz[]\n","",data);
  data = my.str_replace("码长=5\n","",data);
  data = my.str_replace("[数据]",'''%gen_inp
%ename liu
%cname 肥米
%encoding UTF-8
%selkey 0123456789
%keyname begin
a Ａ
b Ｂ
c Ｃ
d Ｄ
e Ｅ
f Ｆ
g Ｇ
h Ｈ
i Ｉ
j Ｊ
k Ｋ
l Ｌ
m Ｍ
n Ｎ
o Ｏ
p Ｐ
q Ｑ
r Ｒ
s Ｓ
t Ｔ
u Ｕ
v Ｖ
w Ｗ
x Ｘ
y Ｙ
z Ｚ
, ，
. ．
' ’
[ 〔
] 〔
%keyname end
%chardef begin
''',data);
  #這版的日文很怪，正常的 a, 、 s, 都有怪字，我看全拿掉，用 j開頭的版本
  bad_words = [];
  res = re.findall('^(?!j)(\w+[,\.]\w*) (.*)\n',data,re.M);
  for k in res:
    d=" ".join(k);
    bad_words.append(d);
  #然後修正看不到的奇怪字
  #bad_words = ['','','','']
  mdata = my.explode("\n",data);
  new_mdata = [];
  for line in mdata:
    if not any(bad_word in line for bad_word in bad_words):
      new_mdata.append(line);
  data = my.implode("\n",new_mdata);
  #然後修正日文 ja, = あ 也相容 a, = あ
  res = re.findall('j(\w*[,\.]) (.*)\n',data,re.M);
  #debug_print(res) 
  for k in res:
    d=" ".join(k);
    data = data + d +"\n";  
  data = data + "%chardef end";
  my.file_put_contents(PWD+"\\liu.cin",data);
  is_need_trans_tab = False;
  is_need_trans_cin = True;
  is_all_fault = False;  
  
if is_all_fault == True:
  message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
  message.set_markup("無字根檔，請購買正版嘸蝦米，將「C:\\windows\\SysWOW64\\liu-uni.tab」或「C:\\Program Files\\BoshiamyTIP\\liu-uni.tab」與uclliu.exe放在一起執行")  
  response = message.run()
  #debug_print(gtk.ResponseType.BUTTONS_OK)
  if response == -5 or response == -4:
    ctypes.windll.user32.PostQuitMessage(0)
    #atexit.register(cleanup)
    #os.killpg(0, signal.SIGKILL)
    my.exit()
  #message.show()
  gtk.main()
           
if is_need_trans_tab==True:
  #需要轉tab檔                                                                             
  #Check liu-uni.tab md5 is fuck up
  if md5_file( ("%s\\liu-uni.tab" % (PWD)) )== "4e89501681ba0405b4c0e03fae740d8c":
    message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
    message.set_markup("請不要使用義守大學的字根檔，這組 liu-uni.tab 太舊不支援...");
    response = message.run()
    #debug_print(gtk.ResponseType.BUTTONS_OK)
    if response == -5 or response == -4:
      ctypes.windll.user32.PostQuitMessage(0)
      #atexit.register(cleanup)
      #os.killpg(0, signal.SIGKILL)
      my.exit()
    #message.show()
    gtk.main()
  if md5_file( ("%s\\liu-uni.tab" % (PWD)) )== "260312958775300438497e366b277cb4":
    message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
    message.set_markup("此組字根檔並非正常的 liu-uni.tab，這個不支援...");
    response = message.run()
    #debug_print(gtk.ResponseType.BUTTONS_OK)
    if response == -5 or response == -4:
      ctypes.windll.user32.PostQuitMessage(0)
      #atexit.register(cleanup)
      #os.killpg(0, signal.SIGKILL)
      my.exit()
    #message.show()
    gtk.main()
  import liu_unitab2cin
  #debug_print(PWD)  
  liu_unitab2cin.convert_liu_unitab( ("%s\\liu-uni.tab" % (PWD)), ("%s\\liu.cin" % (PWD) ))

if is_need_trans_cin==True:
  import cintojson
  cinapp = cintojson.CinToJson()
  cinapp.run( "liu" , "liu.cin",False)


last_key = "" #to save last 7 word for game mode
flag_is_capslock_down=False
flag_is_play_capslock_otherkey=False 
flag_is_win_down=False
flag_is_shift_down=False
flag_is_ctrl_down=False
flag_is_play_otherkey=False
flag_shift_down_microtime=0
flag_isCTRLSPACE=False
play_ucl_label=""
ucl_find_data=[]
same_sound_data=[] #同音字表
same_sound_index=0 #預設第零頁
same_sound_max_word=6 #一頁最多五字
is_has_more_page=False #是否還有下頁
same_sound_last_word="" #lastword

NOW_VOLUME = (int(config['DEFAULT']['KEYBOARD_VOLUME'])) #預設音量
wavs = my.glob(PWD + "\\*.wav")
#debug_print("PWD : %s" % (PWD))
#debug_print(wavs)
o_song = {}
m_play_song = []
max_thread___playMusic_counts = 3 #最多同時五個執行緒在作動
step_thread___playMusic_counts = 0 #目前0個執行緒
for i in range(0,len(wavs)):
  #from : https://pythonbasics.org/python-play-sound/
  #m_song.extend([ AudioSegment.from_wav(wavs[i]) ])
  o_song[ wavs[i] ] = {
                        "lastKey": None,
                        "mainname" : my.mainname(wavs[i]).lower(),
                        "filename":wavs[i],
                        "data":[],
                        "wf":"",
                        "paudio_stream":""      
                      }
  if o_song[ wavs[i] ]["mainname"] == "enter" or o_song[ wavs[i] ]["mainname"] == "return":
    o_song[ wavs[i] ]["lastKey"]=13;
  elif o_song[ wavs[i] ]["mainname"] == "delete" or o_song[ wavs[i] ]["mainname"] == "del":
    o_song[ wavs[i] ]["lastKey"]=46;
  elif o_song[ wavs[i] ]["mainname"] == "backspace" or o_song[ wavs[i] ]["mainname"] == "bs":
    o_song[ wavs[i] ]["lastKey"]=8;
  elif o_song[ wavs[i] ]["mainname"] == "space" or o_song[ wavs[i] ]["mainname"] == "sp":
    o_song[ wavs[i] ]["lastKey"]=32;
debug_print(my.json_encode(o_song))                      
#debug_print(PWD)
#debug_print(list(m_song))
#my.exit()
# 用來出半型字的
# https://stackoverflow.com/questions/2422177/python-how-can-i-replace-full-width-characters-with-half-width-characters
HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
HALF2FULL[0x20] = 0x3000

WIDE_MAP = dict((i, i + 0xFEE0) for i in xrange(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000
                  
def widen(s):
  #https://gist.github.com/jcayzac/1485005
  """
  Convert all ASCII characters to the full-width counterpart.
  
  >>> print widen('test, Foo!')
  ｔｅｓｔ，　Ｆｏｏ！
  >>> 
  """
  return unicode(s).translate(WIDE_MAP)

#def pleave(self, event):
#  my.exit();

if my.is_file(PWD + "\\liu.json") == False:
  message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
  message.set_markup("缺少liu.json")  
  response = message.run()
  #debug_print(gtk.ResponseType.BUTTONS_OK)
  if response == -5 or response == -4:
    ctypes.windll.user32.PostQuitMessage(0)
    #atexit.register(cleanup)
    #os.killpg(0, signal.SIGKILL)
    my.exit()
  #message.show()
  gtk.main()
  #my.exit()
if my.is_file(PWD + "\\pinyi.txt")==True:
  same_sound_data = my.explode("\n",my.trim(my.file_get_contents(PWD + "\\pinyi.txt")))  
  
uclcode = my.json_decode(my.file_get_contents(PWD + "\\liu.json"))

uclcode_r = {}
#然後把 chardefs 的字碼，變成對照字根，可以加速 ,,,z、,,,x 反查的速度
#only short key
for k in uclcode["chardefs"]:
   for kk in range(0,len(uclcode["chardefs"][k])):
     _word = uclcode["chardefs"][k][kk]     
     if _word not in uclcode_r:
       uclcode_r[_word] = k
     else:
       if len(k) < len(uclcode_r[_word]):
         uclcode_r[_word] = k


def thread___playMusic(keyboard_volume):
  global lastKey
  global PWD
  #try:
  # https://stackoverflow.com/questions/43679631/python-how-to-change-audio-volume
  # 調整聲音大小
  # https://stackoverrun.com/cn/q/10107660
  # Last : https://www.thinbug.com/q/45219574
  global paudio_player
  global o_song
  global m_play_song
  global wave
  global step_thread___playMusic_counts   
  try:                   
    if len(m_play_song) !=0 :      
      # https://stackoverflow.com/questions/36664121/modify-volume-while-streaming-with-pyaudio
      chunk = 2048
      #s = random.choice(m_song)
      #print(my.json_encode(m_play_song))                    
      #m_play_song = m_play_song[ : 2]
      #s = m_play_song.pop(0) #m_play_song[0]   
  
      #debug_print("lastKey")
      #debug_print(lastKey)      
      s = ""
      if my.in_array(lastKey,[13,46,32,8]):
        for key in o_song:
          #debug_print("Key")
          #debug_print(key)
          #debug_print(o_song[key]["lastKey"])
          if o_song[key]["lastKey"]!=None and o_song[key]["lastKey"] == lastKey:
            s = key
            #print("s")
            #print(s)  
            break;     
      if s == "":
        _arr = []
        for key in o_song:
          if o_song[key]["lastKey"]==None:
            _arr.append(key)
          pass
        s = _arr[my.rand(0,len(_arr)-1)]
        
      #debug_print(my.json_encode(s))      
      #return     
      if len(o_song[s]["data"]) == 0 or o_song[s]["volume"] != keyboard_volume:        
        o_song[s]["volume"] = keyboard_volume
        o_song[s]["data"] = []
        debug_print("wave s: %s" % (s) )
        o_song[s]["wf"] = wave.open(s, 'rb')
        o_song[s]["paudio_stream"] = paudio_player.open(format = paudio_player.get_format_from_width(o_song[s]["wf"].getsampwidth()),
                      channels = o_song[s]["wf"].getnchannels(),
                      rate = o_song[s]["wf"].getframerate(),
                      output = True)
        # 寫聲音檔輸出來播放
        while True:
          d = o_song[s]["wf"].readframes(chunk)
          if d == "": 
            break      
          # 這是調整音量大小的方法
          o_song[s]["data"].extend([ audioop.mul(d, 2, keyboard_volume / 100.0 ) ])                    
      for i in range(0,len(o_song[s]["data"])):
        o_song[s]["paudio_stream"].write(o_song[s]["data"][i])
    if step_thread___playMusic_counts > 0:
      step_thread___playMusic_counts = step_thread___playMusic_counts -1         
  except Exception as e:
    thread___playMusic(keyboard_volume)
    #debug_print("thread___playMusic error:")
    #debug_print(e)    
           
def thread___x(data):
  #字根轉中文 thread  
  selectData=my.trim(data);  
  menter = my.explode("\n",selectData);
  output = "";
  for kLine in range(0,len(menter)):
    m = my.explode(" ", menter[kLine]);        
    #debug_print(len(m));
    for i in range(0,len(m)):
      #轉小寫
      ucl_split_code = my.strtolower(m[i])
      output += uclcode_to_chinese(ucl_split_code)      
    if kLine != len(menter)-1:      
      output+="{ENTER}"
  senddata(output)  
def word_to_sp(data):
  #中文轉最簡字根
  #回傳字根文字
  #中文轉字根 thread  
  selectData=data; #my.trim(data);
  selectData=selectData.replace("\r","");
  menter = my.explode("\n",selectData);
  output = "";
  for kLine in range(0,len(menter)):
    output_arr = []
    m = mystts.split_unicode_chrs(menter[kLine]);
    for k in range(0,len(m)):
      _uclcode = find_ucl_in_uclcode(m[k]);
      if _uclcode!="":
        output_arr.append(_uclcode)  
    output += my.implode(" ",output_arr);    
    if kLine != len(menter)-1:      
      output+="{ENTER}"
  #debug_print(output)
  output = output.replace(" ","{SPACE}");
  output = output.replace("\n ","{ENTER}");  
  output = output.replace("\n","{ENTER}"); 
  return output 
def show_sp_to_label(data):
  #顯示最簡字根到輸入結束框後
  global config
  global play_ucl_label
  if config['DEFAULT']['SP']=="0":
    return
  sp = "簡根："+my.strtoupper(word_to_sp(data))
  #word_label.set_label(sp)
  #word_label.modify_font(pango.FontDescription(GUI_FONT_18))
  type_label_set_text(sp)     
def thread___z(data):
  output = word_to_sp(data)                   
  senddata(output) 
       
def find_ucl_in_uclcode(chinese_data):
  #用中文反找蝦碼(V1.10版寫法)
  global uclcode_r
  if chinese_data in uclcode_r:
    return uclcode_r[chinese_data];
  else:
    return chinese_data;
     
def find_ucl_in_uclcode_old(chinese_data):
  #用中文反找蝦碼(V1.9版寫法)
  finds = []  
  for k in uclcode["chardefs"]:
    if chinese_data in uclcode["chardefs"][k]:
      index = uclcode["chardefs"][k].index(chinese_data)
      finds.append(k+"_"+str(index))
  finds.sort(key=len, reverse=False)
  
  shorts_arr = []
  shorts_len = 999;
  for k in finds:
    if len(shorts_arr)==0 or len(k) <=shorts_len :
      if len(k) == shorts_len:
        shorts_arr.append(k)
        shorts_len = len(k)
      else:
        shorts_arr = []
        shorts_arr.append(k)
        shorts_len = len(k)
  shorts_arr = sorted(shorts_arr, key = lambda x: int(x.split("_")[1]))
  if len(shorts_arr) >= 1:
    d = shorts_arr[0].split("_")
    return d[0]        
  else:
    return "";

#debug_print(find_ucl_in_uclcode("肥"))
#my.exit();
def UCLGUI_CLOSEST_MONITOR():
  global myScreenStatus
  #肥米靠近哪個螢幕
  [ _x,_y ] = win.get_position()
  [_width,_height] = win.get_size()
  #肥米中心點
  UCL_c_x = _x + ( _width / 2 );
  UCL_c_y = _y + ( _height / 2 );
  _UCL_Closest_Monitor_NO = 0; #哪一個螢幕            
  _UCL_Closest_Monitor_Distinct = 0; #距離    
  for i in range(0, len(myScreenStatus["screens"])):
    if i == 0:
      _UCL_Closest_Monitor_NO = i
      #距離 = ((x1-x2)^2 + (y1-y2)^2) ** 0.5
      _UCL_Closest_Monitor_Distinct = (  (UCL_c_x-myScreenStatus["screens"][i]["c_x"]) ** 2 + (UCL_c_y-myScreenStatus["screens"][i]["c_y"]) ** 2 ) ** 0.5; 
    else:
      _distinct = (  (UCL_c_x-myScreenStatus["screens"][i]["c_x"]) ** 2 + (UCL_c_y-myScreenStatus["screens"][i]["c_y"]) ** 2 ) ** 0.5;
      if _distinct < _UCL_Closest_Monitor_Distinct:
        _UCL_Closest_Monitor_Distinct = _distinct
        _UCL_Closest_Monitor_NO = i
  return _UCL_Closest_Monitor_NO      
        
def toAlphaOrNonAlpha():
  global uclen_btn
  global hf_btn
  global win
  global config
  global user32 
  global win
  #2019-10-22 check screen size and uclliu position
  # 偵測肥米的位置，超出螢幕時，彈回
  #screen_width=user32.GetSystemMetrics(0)
  #screen_height=user32.GetSystemMetrics(1)  
  screen_width = gtk.gdk.screen_width()
  screen_height = gtk.gdk.screen_height()  
  
  #2021-07-27 改成偵測現在肥米離哪個螢幕中心點比較近，如果超過該螢幕限範圍回，要修正位置
  #debug_print("UCL Closest Monitor: %s\n" % (UCLGUI_CLOSEST_MONITOR()))
  #顯示該螢幕的 info
  #debug_print(my.json_encode(myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]))
  # {"area": 2764800, "h": 1080, "c_y": 540, "w": 2560, "c_x": 1280, "y": 0, "x": 0}
  
  [ _x,_y ] = win.get_position()
  [_width,_height] = win.get_size()
  
  new_position_x = _x
  new_position_y = _y
  
  # 每次都重刷 DB ?
  myScreenStatus["screens"] = []
  for i in range(0,myScreensObj.get_n_monitors()):
    d = {
      "x": myScreensObj.get_monitor_geometry(i)[0],
      "y": myScreensObj.get_monitor_geometry(i)[1],
      "w": myScreensObj.get_monitor_geometry(i)[2],
      "h": myScreensObj.get_monitor_geometry(i)[3],
      "area": (myScreensObj.get_monitor_geometry(i)[2] * myScreensObj.get_monitor_geometry(i)[3]),
      "c_x": (myScreensObj.get_monitor_geometry(i)[0] + (myScreensObj.get_monitor_geometry(i)[2] / 2)),
      "c_y": (myScreensObj.get_monitor_geometry(i)[1] + (myScreensObj.get_monitor_geometry(i)[3] / 2)),  
    }
    myScreenStatus["screens"].append(d);  
  
  if _x  > (myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["x"] + myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["w"]) - _width:
    new_position_x = (myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["x"] + myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["w"])-_width-20    
    win.move( new_position_x,new_position_y)
  if _y > (myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["y"] + myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["h"]) - _height:
    new_position_y = (myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["y"] + myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["h"]) - _height - 60 
    win.move( new_position_x,new_position_y)
  
  if _x < myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["x"]:
    new_position_x = myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["x"]+20;
    win.move( new_position_x,new_position_y)
  if _y < myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["y"]:
    new_position_y = myScreenStatus["screens"][UCLGUI_CLOSEST_MONITOR()]["y"]+20
    win.move( new_position_x,new_position_y)  
  
  #c = hf_btn.get_child()
  #hf_kind = c.get_label()
  #hf_kind = hf_btn.get_label()
  if uclen_btn.get_label()=="英" and hf_btn.get_label()=="半":
    win.set_opacity(0.2)
    #win.set_mnemonics_visible(True)
    win.set_keep_above(False)
    win.set_keep_below(True)    
  else:
    #win.set_opacity(1)
    #debug_print(win.get_opacity())
    #if float(win.get_opacity()) != float(config["DEFAULT"]["ALPHA"]): 
    win.set_opacity( float(config["DEFAULT"]["ALPHA"]) )
    #debug_print(float(config["DEFAULT"]["ALPHA"]))
    #win.set_mnemonics_visible(True)
    win.set_keep_above(True)
    win.set_keep_below(False)
def toggle_ucl():
  global uclen_btn
  global play_ucl_label
  global win
  global debug_print
  global GUI_FONT_22
  if uclen_btn.get_label()=="肥":
    uclen_btn.set_label("英")
    play_ucl_label=""
    type_label_set_text()
    win.set_keep_above(False)
    win.set_keep_below(True)
  else:
    uclen_btn.set_label("肥")
    win.set_keep_above(True)
    win.set_keep_below(False)
  uclen_label=uclen_btn.get_child()
  uclen_label.modify_font(pango.FontDescription(GUI_FONT_22))
                                              
  #window_state_event_cb(None,None)
  debug_print("window_state_event_cb(toggle_ucl)")
  toAlphaOrNonAlpha()    
def is_ucl():
  global uclen_btn  
  #print("WTF: %s" % uclen_btn.get_label())
  if uclen_btn.get_label()=="肥":
    return True
  else:
    return False
def is_simple():
  global simple_btn      
  #print("WTF simple: %s" % simple_btn.get_visible())
  #(w,h) = simple_btn.get_size_request();  
  return simple_btn.get_visible()
      
def gamemode_btn_click(self):
  global gamemode_btn 
  if gamemode_btn.get_label()=="正常模式":
    gamemode_btn.set_label("遊戲模式")
    if uclen_btn.get_label() == "肥":
      uclen_btn_click(uclen_btn)    
  else:
    gamemode_btn.set_label("正常模式")
def x_btn_click(self):
  print("Bye Bye");
  global tray
  #global menu  
  tray.set_visible(False)
  #menu.set_visible(False)
  ctypes.windll.user32.PostQuitMessage(0)
  #atexit.register(cleanup)
  #os.killpg(0, signal.SIGKILL)
  sys.exit()
# draggable
def winclicked(self, event):
  # make UCLLIU can draggable  
  self.window.begin_move_drag(event.button, int(event.x_root), int(event.y_root), event.time)
  #self.window.begin_move_drag(event.button, int(event.x_root), int(event.y_root), event.time)
  #self.window.begin_resize_drag(event.button, int(event.x_root), int(event.y_root), event.time)
  # Write to UCLLIU.ini
  global config
  global win
  
  #_x = win.get_allocation().width
  #_y = win.get_allocation().height
  
  [ _x,_y ] = win.get_position()
  #debug_print( "x_root , y_root : %d , %d" % (event.x,event.y))
  #debug_print( "WIN X,Y:%d , %d" % (_x,_y)) 
  config["DEFAULT"]["X"] = str(int(_x))
  config["DEFAULT"]["Y"] = str(int(_y))
  debug_print( "config X,Y:%s , %s" % (config["DEFAULT"]["X"],config["DEFAULT"]["Y"])) 
  saveConfig();
  pass
def uclen_btn_click(self):
  toggle_ucl()
  #pass
def hf_btn_click(self):
  global GUI_FONT_22
  kind=self.get_label()
  if kind=="半":
    self.set_label("全")    
  else:
    self.set_label("半")    
  hf_label=self.get_child()
  hf_label.modify_font(pango.FontDescription(GUI_FONT_22))
  toAlphaOrNonAlpha()
  pass
def is_hf(self):
  global hf_btn
  c = hf_btn.get_child()
  kind = c.get_label()
  return (kind=="半")
   
# http://stackoverflow.com/questions/7050448/write-image-to-windows-clipboard-in-python-with-pil-and-win32clipboard
def type_label_set_text(last_word_label_txt=""):
  global type_label
  global play_ucl_label
  global debug_print
  global GUI_FONT_22
  global GUI_FONT_20
  global config
  type_label.set_label(play_ucl_label)
  type_label.modify_font(pango.FontDescription(GUI_FONT_22))
  if my.strlen(play_ucl_label) > 0:
    debug_print("ShowSearch")
    show_search()
    pass
  else:    
    word_label.set_label("")
    word_label.modify_font(pango.FontDescription(GUI_FONT_20))
    pass
  # 如果 last_word_label_txt 不是空值，代表有簡根或其他用字
  word_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
  if last_word_label_txt != "":
    word_label.set_label( last_word_label_txt )
    word_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color("#007fff"))
  #如果是短米，自動看幾個字展長
  if config["DEFAULT"]["SHORT_MODE"]=="1":
    _tape_label = type_label.get_label()
    _len_tape_label = len(_tape_label)
    #一字30
    if _len_tape_label == 0:
      type_label.set_visible(False)
    else:
      type_label.set_visible(True)
    type_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*18*_len_tape_label) ,int( float(config['DEFAULT']['ZOOM'])*40) ) 
    
    _word_label = word_label.get_label()
    _len_word_label = len(_word_label)
    #一字30
    if _len_word_label == 0:
      word_label.set_visible(False)
    else:
      word_label.set_visible(True)
    word_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*15*_len_word_label) ,int( float(config['DEFAULT']['ZOOM'])*40) )    
    
  return True
def word_label_set_text():
  global word_label
  global ucl_find_data   
  global play_ucl_label
  global is_has_more_page
  global GUI_FONT_20
  global GUI_FONT_18
  global GUI_FONT_16
  global GUI_FONT_14
  global GUI_FONT_12
  
  if play_ucl_label == "":
    word_label.set_label("")
    word_label.modify_font(pango.FontDescription(GUI_FONT_18))
    return
  step=0
  m = []
  try:  
    for k in ucl_find_data:
      m.append("%d%s" % (step,k))
      step=step+1
    tmp = my.implode(" ",m)
    if is_has_more_page == True:
      tmp = "%s ..." % (tmp)
    word_label.set_label(tmp)
    
    debug_print(("word_label lens: %d " % (len(tmp))));
    debug_print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
    lt = len(tmp);
    word_label.modify_font(pango.FontDescription(GUI_FONT_20))
    '''
    if lt<=10: 
      word_label.modify_font(pango.FontDescription(GUI_FONT_20))
    elif lt>10 and lt<=18:
      word_label.modify_font(pango.FontDescription(GUI_FONT_18))
    elif lt>18 and lt<25:
      word_label.modify_font(pango.FontDescription(GUI_FONT_16))
    else:
      word_label.modify_font(pango.FontDescription(GUI_FONT_12))
    '''
    if config["DEFAULT"]["SHORT_MODE"]=="1":
      _word_label = word_label.get_label()
      _len_word_label = len(_word_label)
      #一字30
      if _len_word_label == 0:
        word_label.set_visible(False)
      else:
        word_label.set_visible(True)
      if is_has_more_page==False:
        word_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*12*_len_word_label) ,int( float(config['DEFAULT']['ZOOM'])*40) )
      else:
        #有額外的分頁，加了...
        debug_print("More page...")
        word_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*13*_len_word_label) ,int( float(config['DEFAULT']['ZOOM'])*40) )    
        
    return True
  except:
    play_ucl_label=""
    play_ucl("")
    word_label.set_label("")
    word_label.modify_font(pango.FontDescription(GUI_FONT_18))  
    return True
def uclcode_to_chinese(code):
  global ucl_find_data
  global debug_print  
  c = code
  c = my.trim(c)
  if c == "":
    return ""
  #debug_print(c)
  if c not in uclcode["chardefs"] and c[-1]=='v' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=2 :
    #debug_print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][1]       
    return ucl_find_data
  elif c not in uclcode["chardefs"] and c[-1]=='r' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=3 :
    #debug_print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][2]       
    return ucl_find_data
  elif c not in uclcode["chardefs"] and c[-1]=='s' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=4 :
    #debug_print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][3]       
    return ucl_find_data
  elif c not in uclcode["chardefs"] and c[-1]=='f' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=5 :
    #debug_print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][4]       
    return ucl_find_data
  elif c in uclcode["chardefs"]:
    #debug_print("Debug V2")
    ucl_find_data = uclcode["chardefs"][c][0]    
    return ucl_find_data
  else:    
    return code 
def show_search():
  #真的要顯示了
  global play_ucl_label
  global ucl_find_data
  global ucl_find_data_orin_arr
  global is_need_use_pinyi
  global is_has_more_page
  global same_sound_index
  global same_sound_last_word
  global debug_print
  global same_sound_max_word
  same_sound_index = 0
  is_has_more_page = False
  same_sound_last_word=""
  debug_print("ShowSearch1")
  c = my.strtolower(play_ucl_label)
  c = my.trim(c)
  #debug_print("ShowSearch2")
  #debug_print("C[-1]:%s" % c[-1])
  #debug_print("C[:-1]:%s" % c[:-1])  
  # 此部分可以修正 V 可以出第二字，還不錯
  # 2017-07-13 Fix when V is last code
  #debug_print("LAST V : %s" % (c[-1]))
  is_need_use_pinyi=False  
  if c[0] == "'" and len(c)>1:
    c=c[1:]
    is_need_use_pinyi=True
  if c not in uclcode["chardefs"] and c[-1]=='v' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=2 :
    #debug_print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][1]   
    word_label_set_text()
    return True
  elif c not in uclcode["chardefs"] and c[-1]=='r' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=3 :
    #debug_print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][2]   
    word_label_set_text()
    return True
  elif c not in uclcode["chardefs"] and c[-1]=='s' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=4 :
    #debug_print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][3]   
    word_label_set_text()
    return True
  elif c not in uclcode["chardefs"] and c[-1]=='f' and c[:-1] in uclcode["chardefs"] and len(uclcode["chardefs"][c[:-1]])>=5 :
    #debug_print("Debug V1")
    ucl_find_data = uclcode["chardefs"][c[:-1]][4]   
    word_label_set_text()
    return True
  elif c in uclcode["chardefs"]:
    #debug_print("Debug V2")
    ucl_find_data = uclcode["chardefs"][c]
    ucl_find_data_orin_arr = ucl_find_data
    if len(ucl_find_data) > same_sound_max_word:
      #Need page
      ucl_find_data = ucl_find_data_orin_arr[same_sound_index:same_sound_max_word]  
      is_has_more_page = True         
    word_label_set_text()
    return True
  else:
    #debug_print("Debug V3")
    ucl_find_data=[]  
    #play_ucl_label=""  
    #ucl_find_data=[]
    word_label_set_text()
    return False  
  
  #debug_print(find)
  #debug_print("ShowSearch3")
  #debug_print("FIND: [%s] %s" % (play_ucl_label,find))
  #pass
def play_ucl(thekey):
  global type_label
  global play_ucl_label
  play_ucl_label = type_label.get_label();
  # 不可以超過5個字
  if len(play_ucl_label) < 5:
    play_ucl_label = "%s%s" % (play_ucl_label,thekey)
    type_label_set_text()
  return True
def senddata(data):
  global play_ucl_label
  global ucl_find_data
  global same_sound_index
  global is_has_more_page
  global same_sound_last_word
  global debug_print
  global f_arr
  global f_big5_arr
  #2019-10-20 增加出字強制選擇
  global DEFAULT_OUTPUT_TYPE
  #for i in range(0,len(mTC_TDATA)):
  #  debug_print(mTC_TDATA[i]);
  #my.exit(); 
  #debug_print(mTC_TDATA)
  #簡繁轉換  
  if is_simple():    
    data = mystts.trad2simple(data)
      
    
  
  same_sound_index = 0 #回到第零頁
  is_has_more_page = False #回到沒有分頁
  same_sound_last_word=""
  play_ucl_label=""
  ucl_find_data=[]  
  type_label_set_text()  
  
  
  
  hwnd = win32gui.GetForegroundWindow()
  pid = win32process.GetWindowThreadProcessId(hwnd)
  #debug_print("Title: -------------------------- ") #批踢踢實業坊 - Google Chrome
  #debug_print(win32gui.GetWindowText(hwnd))
  program_title = win32gui.GetWindowText(hwnd)
  
  pp="";
  if len(pid) >=2:
    pp=pid[1]
  else:
    pp=pid[0]
  #debug_print("PP:%s" % (pp))
  debug_print("PP:%s" % (pp))
  p=psutil.Process(pp)
  
  debug_print("ProcessP:%s" % (p))
  
  check_kind="0"
  
  # 這是貼上模式
  for k in f_arr:
    #break;
    k = my.strtolower(k)
    exec_proc = my.strtolower(p.exe())
    # 2021-08-08 term.ptt.cc (批踢踢實業坊 - Google Chrome) 改成，強制 paste
    if my.is_string_like(exec_proc,k) or DEFAULT_OUTPUT_TYPE == "PASTE" or program_title == "批踢踢實業坊 - Google Chrome":  
      check_kind="1"      
      
      win32clipboard.OpenClipboard()
      orin_clip=""
      try:
        orin_clip=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
      except:
        pass
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, "")
      win32clipboard.EmptyClipboard()
      win32clipboard.CloseClipboard()
            
      win32clipboard.OpenClipboard() 
      win32clipboard.EmptyClipboard()#這一行特別重要，經過實驗如果不加這一行的話會做動不正常
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, data)
      win32clipboard.CloseClipboard()
      #https://win32com.goermezer.de/microsoft/windows/controlling-applications-via-sendkeys.html
      #shell.SendKeys("+{INSERT}", 0)
      #2018-04-05 修正 vim 下打中文字的問題
      #debug_print("Debug Oxygen Not Included")
      #SendKeysCtypes.SendKeys("+{INSERT}",pause=0)
      if k == "oxygennotincluded.exe":
        #2019-02-10 修正 缺氧 無法輸入中文的問題
        SendKeysCtypes.SendKeys("^v",pause=0)
      elif k == "iedit_.exe":
        #2019-10-29 修正 PhotoImpact x3 無法輸入中文的問題
        SendKeysCtypes.SendKeys("^v",pause=0)
      else:
        SendKeysCtypes.SendKeys("+{INSERT}",pause=0)
      #SendKeysCtypes.SendKeys("ggggg",pause=0)
      #0xA0 = left shift
      #0x2d = insert            
      #win32api.keybd_event(0x10, 1,0,0)
      #win32api.keybd_event(45, 1,0,0)      
      #time.sleep(.05)            
      #win32api.keybd_event(45,0 ,win32con.KEYEVENTF_KEYUP ,0)
      #win32api.keybd_event(0x10,0 ,win32con.KEYEVENTF_KEYUP ,0)
      
      #win32api.keybd_event(win32con.SHIFT_PRESSED, 0, 0x2d, 0,win32con.KEYEVENTF_KEYUP ,0)
       
      #reload(sys)                                    
      #sys.setdefaultencoding('UNICODE') 
      #SendKeysCtypes.SendKeys("肥".encode("UTF-8"),pause=0)
      #reload(sys)                                    
      #sys.setdefaultencoding('UTF-8')
      #也許要設delay...
      time.sleep(0.05)
      win32clipboard.OpenClipboard()    
      win32clipboard.EmptyClipboard()
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip)
      win32clipboard.CloseClipboard()            
      break
  for k in f_big5_arr:
    k = my.strtolower(k)
    if my.is_string_like(my.strtolower(p.exe()),k) or DEFAULT_OUTPUT_TYPE == "BIG5":
      debug_print("Debug_f_big5_arr")
      #SendKeysCtypes.SendKeys(my.utf8tobig5(data),pause=0)
      check_kind="2"
      win32clipboard.OpenClipboard()
      orin_clip=""
      try:
        orin_clip=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
      except:
        pass      
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, "")
      win32clipboard.EmptyClipboard()
      win32clipboard.SetClipboardData(win32con.CF_TEXT, my.utf8tobig5(data))
      win32clipboard.CloseClipboard()
      #之前是用 shell，改用 SendKeysCtypes.SendKeys 看看
      #shell = win32com.client.Dispatch("WScript.Shell")
      #shell.SendKeys("^v", 0)
      SendKeysCtypes.SendKeys("^v")
      time.sleep(0.05)
      win32clipboard.OpenClipboard()    
      win32clipboard.EmptyClipboard()
      win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip)
      win32clipboard.CloseClipboard()         
      break
            
  if check_kind=="0":
    #reload(sys)                                    
    #sys.setdefaultencoding('UTF-8')
    #debug_print("CP950")
    #2019-03-02 
    #修正斷行、空白、自定詞庫等功能
    _str = data.decode("UTF-8")
    _str = my.str_replace(" ","{SPACE}",_str)
    _str = my.str_replace("(","{(}",_str)
    _str = my.str_replace(")","{)}",_str)
    _str = my.str_replace("\n","{ENTER}",_str)
    SendKeysCtypes.SendKeys(_str,pause=0)
    #reload(sys)
    #sys.setdefaultencoding('UTF-8')
  
  #reload(sys)                                    
  #sys.setdefaultencoding('auto')
  #SendKeysCtypes.SendKeys(data.decode("auto"),pause=0)
  
def use_pinyi(data):
  global same_sound_data
  global ucl_find_data
  global same_sound_index
  global same_sound_max_word
  global is_has_more_page
  global debug_print
  finds=""
  for k in same_sound_data:
    if my.is_string_like(k,data):
      #if k.startswith(u'\xe7\x9a\x84'):
      #  k = u[1:]
      finds="%s%s " % (finds,my.trim(k))
      #debug_print(k)
  finds=my.trim(finds);
  finds=my.explode(" ",finds)
  #debug_print(finds)
  #finds=finds[:] 
  #for k in finds:
  #  debug_print(k.encode("UTF-8"))
  finds = my.array_unique(finds)
  #debug_print("Debug data: %s " % data.encode("UTF-8"))
  debug_print("Debug Finds: %d " % len(finds))
  debug_print("Debug same_sound_index: %d " % same_sound_index)
  debug_print("Debug same_sound_max_word: %d " % same_sound_max_word)  
  maxword = same_sound_index + same_sound_max_word
  # 2020-08-10 103 分頁異常，修正同音字少一字，最後分頁有機會顯示錯誤的問題
  if maxword >= len(finds):
    maxword = len(finds)
    is_has_more_page = False
  else:
    is_has_more_page = True
  ucl_find_data = finds[same_sound_index:maxword]
  debug_print("DEBUG same_sound_index: %d " % same_sound_index)
  same_sound_index=same_sound_index+same_sound_max_word
   
  if same_sound_index>=len(finds):
    same_sound_index=0
  word_label_set_text()
  #finds=my.str_replace(data," ",finds)
  #finds=my.str_replace("  "," ",finds)
def OnMouseEvent(event):
  global flag_is_shift_down
  global flag_is_play_otherkey
  global hm
  #if flag_is_shift_down==True:
    #如果同時按著 shift 時，滑鼠有操作就視窗按別的鍵 ok
  if event.MessageName == "mouse left down" or event.MessageName == "mouse right down" :
    #flag_is_shift_down=False
    flag_is_play_otherkey=True
    #debug_print(('MessageName: %s' % (event.MessageName)))
    #debug_print(('Message: %s' % (event.Message))) 
    #debug_print("Debug event MouseA")
    #debug_print(flag_is_play_otherkey)
    #hm.UnhookMouse()
  return True

# run always thread  
# 2021-08-08 修正 打字音按著鍵會連續音消除
lastKey = None    
def OnKeyboardEvent(event):  
  global last_key # save keyboard last 10 word for ,,,j ,,,x ,,,z...
  global flag_is_win_down
  global flag_is_shift_down
  global flag_is_capslock_down
  global flag_is_play_capslock_otherkey
  global flag_is_ctrl_down    
  global flag_is_play_otherkey
  global play_ucl_label
  global ucl_find_data
  global is_need_use_pinyi
  global same_sound_last_word
  global gamemode_btn
  global simple_btn
  global debug_print
  global VERSION
  global f_arr
  global GUI_FONT_16
  global f_pass_app
  global config 
  global m_play_song
  global max_thread___playMusic_counts
  global step_thread___playMusic_counts
  global flag_shift_down_microtime
  global same_sound_index 
  global hm 
  global is_has_more_page
  global same_sound_max_word
  global ucl_find_data_orin_arr
  global lastKey # save keyboard last word for same keyin sound
     
  # From : https://stackoverflow.com/questions/20021457/playing-mp3-song-on-python
  # 1.26 版，加入打字音的功能
  # 1.37 版，打字音不會因為壓著一直響
  
  try:
    if config['DEFAULT']['PLAY_SOUND_ENABLE'] == "1" and event.MessageName == "key down":
      #and len(o_song.keys())!=0 and step_thread___playMusic_counts < max_thread___playMusic_counts:
      if lastKey != event.KeyID:
        lastKey = event.KeyID
        #debug_print("lastKey: ");   
        #debug_print(lastKey);
        play_sound()      
      #thread___playMusic(m_song,int(config['DEFAULT']['KEYBOARD_VOLUME']))
    if config['DEFAULT']['PLAY_SOUND_ENABLE'] == "1" and event.MessageName == "key up":
      lastKey = None    
    
    #  playsound.playsound(mp3s[1])
    #debug_print(dir())  
    #try:  
    #debug_print(event)
    '''
    debug_print(('MessageName: %s' % (event.MessageName)))
    debug_print(('Message: %s' % (event.Message)))
    debug_print(('Time: %s' % (event.Time)))
    debug_print(('Window: %s' % (event.Window)))
    debug_print(('WindowName: %s' % (event.WindowName)))
    debug_print(('Ascii: %s, %s' % (event.Ascii, chr(event.Ascii))))
    debug_print(('Key: %s' % (event.Key)))
    debug_print(('KeyID: %s' % (event.KeyID)))
    debug_print(('ScanCode: %s' % (event.ScanCode)))
    debug_print(('Extended: %s' % (event.Extended)))
    debug_print(('Injected: %s' % (event.Injected)))
    debug_print(('Alt: %s' % (event.Alt)))
    debug_print(('Transition: %s' % (event.Transition)))
    debug_print(('IS_UCL %s' % (is_ucl())))
    debug_print('---')
    debug_print(('last_key: %s' % (last_key[-8:])))
    '''
    
    hwnd = win32gui.GetForegroundWindow()  
    pid = win32process.GetWindowThreadProcessId(hwnd)
    pp="";
    if len(pid) >=2:
      pp=pid[1]
    else:
      pp=pid[0]
    #debug_print("PP:%s" % (pp))
    #debug_print("PP:%s" % (pp))
    p=psutil.Process(pp)
    #debug_print("ProcessP:%s" % (p))
    #debug_print("GGGGGGG %s " % (p.exe()))
    
    #debug_print(dir(p))
    exec_proc = my.strtolower(p.exe())
    #debug_print("Process :%s" % (exec_proc))
    #print ("HWND:")
    #print (win32gui.GetWindowText(hwnd))
    
    for k in f_pass_app:        
      if my.is_string_like(exec_proc,k):
        if is_ucl()==True:
          toggle_ucl()
        return True
    # chrome 遠端桌面也不需要肥米
    if my.is_string_like(my.strtolower(win32gui.GetWindowText(hwnd)),"- chrome "):
      if is_ucl()==True:
        toggle_ucl()
      return True
    
    #debug_print("Title: -------------------------- ") #批踢踢實業坊 - Google Chrome
    #debug_print(win32gui.GetWindowText(hwnd))
    
    
    if event.MessageName == "key up":    
          
      last_key = last_key + chr(event.Ascii)
      last_key = last_key[-10:]
      if my.strtolower(last_key[-4:])==",,,c":
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        if is_ucl()==False:
          # change to ucl
          toggle_ucl()
        simple_btn.set_size_request( int(float(config['DEFAULT']['ZOOM'])*40),int(float(config['DEFAULT']['ZOOM'])*40) )
        simple_label=simple_btn.get_child()
        simple_label.set_label("簡")
        simple_btn.set_visible(True)
        simple_label.modify_font(pango.FontDescription(GUI_FONT_16))      
        #simple_label.set_justify(gtk.JUSTIFY_CENTER)
      if my.strtolower(last_key[-4:])==",,,t":
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        if is_ucl()==False:
          # change to ucl
          toggle_ucl()
        simple_btn.set_size_request(0,int(float(config['DEFAULT']['ZOOM'])*40) )
        simple_label=simple_btn.get_child()
        simple_label.set_label("")
        simple_btn.set_visible(False)
        simple_label.modify_font(pango.FontDescription(GUI_FONT_16))       
      if my.strtolower(last_key[-7:])==",,,lock":
        last_key = ""
        if gamemode_btn.get_label()=="正常模式":
          gamemode_btn_click(gamemode_btn)
      if my.strtolower(last_key[-4:])==",,,-":
        #run small
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha()
        run_big_small(-0.1)        
      if my.strtolower(last_key[-4:])==",,,+":
        #run big
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha()
        run_big_small(0.1)
      if my.strtolower(last_key[-4:])==",,,s":
        # run short
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        run_short()
      if my.strtolower(last_key[-4:])==",,,l":
        # run long
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        run_long()
      if my.strtolower(last_key[-4:])==",,,x" and is_ucl():
        # 將框選嘸蝦米的文字，轉成中文字
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha() 
        orin_clip=""
        try:
          win32clipboard.OpenClipboard()
          orin_clip=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        except:
          pass
        try:
          win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, "")
          win32clipboard.EmptyClipboard()
          win32clipboard.CloseClipboard()
        except:
          pass      
        SendKeysCtypes.SendKeys("^C",pause=0.05)
        #也許要設delay...      
        #try:
        win32clipboard.OpenClipboard()
        #try:
        selectData=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        # 參考 http://www.runoob.com/python/python-multithreading.html      
        thread.start_new_thread( thread___x, (selectData, ))
        win32clipboard.CloseClipboard()       
        #except:
        #  pass
        #也許要設delay...
        time.sleep(0.05)
        try:
          win32clipboard.OpenClipboard()    
          win32clipboard.EmptyClipboard()
          win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip)
          win32clipboard.CloseClipboard()           
        except:
          pass
        return False   
      if my.strtolower(last_key[-4:])==",,,z" and is_ucl():
        # 將框選的文字，轉成嘸蝦米的字
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha()                   
        orin_clip=""
        try:
          win32clipboard.OpenClipboard()
          orin_clip=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        except:
          pass
        try:
          win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, "")
          win32clipboard.EmptyClipboard()
          win32clipboard.CloseClipboard()
        except:
          pass
        SendKeysCtypes.SendKeys("^C",pause=0.05)
        try:
          win32clipboard.OpenClipboard()
          #try:
          time.sleep(0.05)
          selectData=win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
          #簡轉繁
          selectData = mystts.simple2trad(selectData)       
                          
          thread.start_new_thread( thread___z, (selectData, ))
        except:
          pass
        #也許要設delay...
        time.sleep(0.05)
        try:
          win32clipboard.OpenClipboard()    
          win32clipboard.EmptyClipboard()
          win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, orin_clip)
          win32clipboard.CloseClipboard()
        except:
          pass
        return False             
      if my.strtolower(last_key[-9:])==",,,unlock":          
        last_key = ""               
        if gamemode_btn.get_label()=="遊戲模式":
          gamemode_btn_click(gamemode_btn)
      if my.strtolower(last_key[-10:])==",,,version":
        last_key= ""   
        message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
        message.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        message.set_keep_above(True)
        _msg_text = about_uclliu()       
        message.set_markup( _msg_text )
        #toAlphaOrNonAlpha()
        message.show()
        toAlphaOrNonAlpha()  
        response = message.run()
        #toAlphaOrNonAlpha()
        debug_print("Show Version")
        debug_print(response)
        #debug_print(gtk.ResponseType.BUTTONS_OK)
        if response == -5 or response == -4:
          #message.hide()
          message.destroy()
          #toAlphaOrNonAlpha()  
          play_ucl_label=""
          ucl_find_data=[]
          type_label_set_text()
          toAlphaOrNonAlpha()
          return False      
    #debug_print("LAST_KEY:" + last_key)
    if gamemode_btn.get_label()=="遊戲模式":      
      return True    
    
    #thekey = chr(event.Ascii)
    # KeyID = 91 = Lwinkey
    # 2019-07-19
    # 增加，如果是肥模式，且輸入的字>=1以上，按下 esc 鍵，會把字消除  
    if event.MessageName == "key down" and is_ucl() == True and len(play_ucl_label) >=1 and event.Key == "Escape":
      #debug_print("2019-07-19 \n 增加，如果是肥模式，且輸入的字>=1以上，按下 esc 鍵，會把字消除)");
      play_ucl_label = ""
      type_label_set_text()
      return False
    if event.MessageName == "key down" and (event.KeyID == 91 or event.KeyID == 92):
      flag_is_win_down = True
      debug_print("Debug event A")
    if event.MessageName == "key up" and (event.KeyID == 91 or event.KeyID == 92):
      flag_is_win_down = False
      debug_print("Debug event B")
    if event.MessageName == "key down" and (event.Key == "Lshift" or event.Key == "Rshift"):
      if flag_is_shift_down==False:
        flag_is_play_otherkey=False
        flag_shift_down_microtime = my.microtime()      
      flag_is_shift_down=True
      debug_print("Debug event CC")
    if event.MessageName == "key down" and (event.Key == "Lshift" or event.Key == "Rshift") and config['DEFAULT']['CTRL_SP'] == "0":
      #2019-10-22 如果按著 shift 還用 滑鼠，不會切換 英/肥
      #hm.UnhookMouse()
      if flag_is_shift_down==False:
        flag_is_play_otherkey=False
        flag_shift_down_microtime = my.microtime()      
      flag_is_shift_down=True
      
      #hm.HookMouse()            
      debug_print("Debug event C") 
    if event.MessageName == "key down" and (event.Key == "Lcontrol" or event.Key == "Rcontrol"):  # and config['DEFAULT']['CTRL_SP'] == "1"
      #2019-10-22 如果按著 shift 還用 滑鼠，不會切換 英/肥
      #2021-03-22 修正英/全時，複製、貼上，按著 Ctrl + 任意鍵 有問題
      #hm.UnhookMouse()        
      flag_is_ctrl_down=True      
      #hm.HookMouse()            
      debug_print("Debug event Ctrl C 1")         
    if event.MessageName == "key up" and (event.Key == "Lcontrol" or event.Key == "Rcontrol"): #  and config['DEFAULT']['CTRL_SP'] == "1"
      #2019-10-22 如果按著 shift 還用 滑鼠，不會切換 英/肥
      #2021-03-22 修正英/全時，複製、貼上，按著 Ctrl + 任意鍵 有問題
      #hm.UnhookMouse()                  
      flag_is_ctrl_down=False      
      #hm.HookMouse()            
      debug_print("Debug event Ctrl C 2")
      return True
    if event.MessageName == "key down" and event.Key == "Capital":
      flag_is_capslock_down=True
      flag_is_play_capslock_otherkey=False
      debug_print("Debug event E")
      return True
    if event.MessageName == "key down" and event.Key != "Capital":
      flag_is_play_capslock_otherkey=True
      debug_print("Debug event F")
    if event.MessageName == "key up" and event.Key == "Capital":
      flag_is_capslock_down=False
      flag_is_play_capslock_otherkey=False
      debug_print("Debug event E")
    if event.MessageName == "key down" and (event.Key != "Lshift" and event.Key != "Rshift") and config['DEFAULT']['CTRL_SP'] == "0":
      debug_print("Debug event D")
      flag_is_play_otherkey=True   
    
    if flag_is_capslock_down == True and flag_is_play_capslock_otherkey == True:
      # 2019-03-06 增加，如果是 肥 模式，且輸入字是 backspace 且框有字根，就跳過這個 True
      if event.Key == "Back" and is_ucl()==True and len(play_ucl_label) >= 1:
        debug_print("Debug 2019-03-06 CapsLock + backspace")
        pass
      else:  
        return True
    if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Rshift"):
      flag_is_shift_down=False
               
    if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Rshift") and config['DEFAULT']['CTRL_SP'] == "0":
      debug_print("Debug event G")
      debug_print("event.MessageName:"+event.MessageName)
      debug_print("event.Ascii:"+str(event.Ascii))
      debug_print("event.KeyID:"+str(event.KeyID))
      debug_print("flag_is_play_otherkey:"+str(flag_is_play_otherkey))
      debug_print("flag_is_shift_down:"+str(flag_is_shift_down))        
      debug_print("flag_is_capslock_down:"+str(flag_is_capslock_down))
      debug_print("flag_is_play_capslock_otherkey:"+str(flag_is_play_capslock_otherkey))
      flag_is_shift_down=False
      #hm.UnhookMouse()
      debug_print("Press shift")
      
      #2021-03-20 如果 microtime() - flag_shift_down_microtime>=500 flag_is_play_otherkey = true
      st = my.microtime() - flag_shift_down_microtime
      debug_print("st: %d " % (st))
      if st>=500:
         flag_is_play_otherkey = True
      # 不可是右邊的2、4、6、8      
      #toAlphaOrNonAlpha()
      if flag_is_play_otherkey==False and (event.Ascii > 40 or event.Ascii < 37) :
        toggle_ucl()
        debug_print("Debug15")        
        debug_print("Debug14")
  
      #toAlphaOrNonAlpha()
      return True
    if event.MessageName == "key down" and event.Ascii==32 and flag_is_shift_down==True:
      # Press shift and space
      # switch 半/全
      # 2021-07-05 如果有下一頁， shift + space 改成換下頁哦
      if my.is_string_like(word_label.get_label(),"...") == True:
        debug_print("FFFFFFFIND WORDS...")
        debug_print("ucl_find_data_orin_arr")
        debug_print(ucl_find_data_orin_arr)        
        debug_print("ucl_find_data")
        debug_print(ucl_find_data)
        debug_print("same_sound_index")
        debug_print(same_sound_index)        
        same_sound_index = same_sound_index+same_sound_max_word
        if same_sound_index > len(ucl_find_data_orin_arr)-1:
          same_sound_index = 0  
        maxword = same_sound_index + same_sound_max_word
        if maxword > len(ucl_find_data_orin_arr)-1:
           maxword = len(ucl_find_data_orin_arr)           
        ucl_find_data = ucl_find_data_orin_arr[same_sound_index:maxword]  
        debug_print("after ucl_find_data")
        debug_print(ucl_find_data)                               
        word_label_set_text()        
        return False                     
      else:
        hf_btn_click(hf_btn)
        flag_is_play_otherkey=True
        flag_is_shift_down=False    
        debug_print("Debug13")
        return False         
        
      
    if is_ucl():
      #debug_print("is ucl")    
      if event.MessageName == "key down" and flag_is_win_down == True : # win key
        return True
      #2018-05-05要考慮右邊數字鍵的 . 
      if event.MessageName == "key down" and ( event.Ascii>=48 and event.Ascii <=57) or (event.Key=="Decimal" and event.Ascii==46) : #0~9 . 
        if len(ucl_find_data)>=1 and int(chr(event.Ascii)) < len(ucl_find_data):
          # send data        
          data = ucl_find_data[int(chr(event.Ascii))]
          #debug_print(ucl_find_data)
          
          senddata(data)
          show_sp_to_label(data.decode('utf-8'))
          #debug_print(data)
          #快選用的
          #debug_print(data)        
          debug_print("Debug12")
          return False
        else:
          if len(event.Key) == 1 and is_hf(None)==False:
            #k = widen(event.Key)
            kac = event.Ascii          
            k = widen(chr(kac))
            debug_print("event.Key to Full:%s %s" % (event.Key,k))
            senddata(k)
            debug_print("Debug11")
            return False
          
          debug_print("Debug10")
          #2017-10-24要考慮右邊數字鍵的狀況
          #2018-05-05要考慮右邊數字鍵的 .
          # event.Ascii==46 or (event.Key=="Decimal" and event.Ascii==46)
          # 先出小點好了
          if is_hf(None)==False and ( event.Ascii==49 or event.Ascii==50 or event.Ascii==51 or event.Ascii==52 or event.Ascii==53 or event.Ascii==54 or event.Ascii==55 or event.Ascii==56 or event.Ascii==57 or event.Ascii==47 or event.Ascii==42 or event.Ascii==45 or event.Ascii==43 or event.Ascii==48):
            kac = event.Ascii        
            k = widen(chr(kac))
            #if event.Ascii==46:
            #  senddata("a")
            #else:
            senddata(k)
            debug_print("Debug100")
            return False
          else:  
            return True                    
      if event.MessageName == "key down" and ( (event.Ascii>=65 and event.Ascii <=90) or (event.Ascii>=97 and event.Ascii <=122) or event.Ascii==44 or event.Ascii==46 or event.Ascii==39 or event.Ascii==91 or event.Ascii==93):
        # 這裡應該是同時按著SHIFT的部分
        flag_is_play_otherkey=True
        if flag_is_shift_down==True:
          if len(event.Key) == 1 and is_hf(None)==False:
            #k = widen(event.Key)
            kac = event.Ascii
            if kac>=65 and kac<=90:
              kac=kac+32
            else:
              kac=kac-32
            k = widen(chr(kac))
            debug_print("285 event.Key to Full:%s %s" % (event.Key,k))
            senddata(k)
            debug_print("Debug9")
            return False
          debug_print("Debug8")
          return True
        else:
          # Play ucl
          #debug_print("Play UCL")
          #debug_print(thekey)
          play_ucl(chr(event.Ascii))
          debug_print("Debug7")
          return False    
      if event.MessageName == "key down" and ( event.Ascii == 8 ): # ←      
        if my.strlen(play_ucl_label) <= 0:                    
          play_ucl_label=""
          play_ucl("")
          debug_print("Debug6")
          return True
        else:
          play_ucl_label = play_ucl_label[:-1]
          type_label_set_text()
          debug_print("Debug5")        
          return False       
      if event.MessageName == "key down" and event.Key=="Space" and config['DEFAULT']['CTRL_SP']=="1": # check ctrl + space
          if flag_is_ctrl_down == True:
            toggle_ucl()
            return False
      if event.MessageName == "key down" and event.Key=="Space": #空白
        # Space                          
        if len(ucl_find_data)>=1:        
          #丟出第一個字                
          text = ucl_find_data[0]
          if same_sound_last_word=="":
            same_sound_last_word=text
          #] my.utf8tobig5("好的")          
          if is_need_use_pinyi==True:
            #使用同音字
            debug_print("Debug use pinyi")
            use_pinyi(same_sound_last_word)
          else:
            #在這作，如果有分頁，要切換分頁
            #2021-07-05            
            finds = my.array_unique(ucl_find_data)
            #debug_print("Debug data: %s " % data.encode("UTF-8"))
            debug_print("Debug Finds: %d " % len(finds))
            debug_print("Debug same_sound_index: %d " % same_sound_index)
            debug_print("Debug same_sound_max_word: %d " % same_sound_max_word)  
            maxword = same_sound_index + same_sound_max_word
            # 2020-08-10 103 分頁異常，修正同音字少一字，最後分頁有機會顯示錯誤的問題
            if maxword >= len(finds):
              maxword = len(finds)
              is_has_more_page = False
            else:
              is_has_more_page = True
            ucl_find_data = finds[same_sound_index:maxword]
            debug_print("DEBUG same_sound_index: %d " % same_sound_index)
            same_sound_index=same_sound_index+same_sound_max_word
             
            if same_sound_index>=len(finds):
              same_sound_index=0
           
            senddata(text)   
            #2021-07-22 補 sp 出字
            show_sp_to_label(text)             
          debug_print("Debug4")
          return False 
        elif len(ucl_find_data)==0 and len(play_ucl_label)!=0:
          #無此字根時，按到空白鍵
          debug_print("Debug11")
          play_ucl_label=""
          ucl_find_data=[]
          type_label_set_text()
          return False 
        else:
          #沒字時直接出空白
          debug_print("Debug1")
          if is_hf(None)==False:        
            kac = event.Ascii        
            k = widen(chr(kac))
            senddata(k)
            debug_print("Debug23")
            return False
          else:
            return True
      elif event.MessageName == "key down" and ( event.Ascii==58 or event.Ascii==59 or event.Ascii==123 or event.Ascii==125 or event.Ascii==40 or event.Ascii==41 or event.Ascii==43 or event.Ascii==126 or event.Ascii==33 or event.Ascii==64 or event.Ascii==35 or event.Ascii==36 or event.Ascii==37 or event.Ascii==94 or event.Ascii==38 or event.Ascii==42 or event.Ascii==95 or event.Ascii==60 or event.Ascii==62 or event.Ascii==63 or event.Ascii==34 or event.Ascii==124 or event.Ascii==47 or event.Ascii==45) : # : ;｛｝（）＋～！＠＃＄％＾＆＊＿＜＞？＂｜／－
        #修正 肥/全 時，按分號、冒號只出半型的問題
        if is_hf(None)==False:        
          kac = event.Ascii        
          k = widen(chr(kac))
          senddata(k)
          debug_print("Debug22")
          return False
        else:
          debug_print("Debug22OK")
          return True     
      else:                  
        return True            
        
    else:
      debug_print("DDDDDDDDD: event.Key: " + event.Key + "\nDDDDDDDDD: event.KeyID: " + str(event.KeyID) + "\nDDDDDDDDD: event.MessageName: " +  event.MessageName )
      debug_print("flag_is_shift_down:"+str(flag_is_shift_down))
      debug_print("flag_is_ctrl_down:"+str(flag_is_ctrl_down))
      debug_print("Debug3")  
      debug_print(event.KeyID)
      # 2018-03-27 此部分修正「英/全」時，按Ctrl A 無效的問題，或ctrl+esc等問題
      # 修正enter、winkey 在「英/全」的狀況
      if event.MessageName == "key down" and event.KeyID == 13:
        return True
      if event.MessageName == "key down" and ( event.KeyID == 91 or event.KeyID == 92): #winkey
        flag_is_win_down=True
        return True
      # 修正  在「英/全」的狀況，按下 esc (231 + 27 ) 無效的問題
      if event.MessageName == "key down" and ( event.KeyID == 231 or event.KeyID == 27):
        flag_is_win_down=False
        debug_print("Fix 23+27")
        return True                
      if event.MessageName == "key down" and flag_is_win_down == True : # win key
        flag_is_win_down=False
        return True          
      #if event.MessageName == "key down" and ( event.KeyID == 231 or event.KeyID == 162 or event.KeyID == 163):
      #  flag_is_ctrl_down=True
      #  debug_print("Ctrl key")
      #  return True
      #if flag_is_ctrl_down == True:
      #  flag_is_ctrl_down=False
      #  return True       
      if event.MessageName == "key down" and (event.Key == "Lshift" or event.Key == "Rshift"):      
        flag_is_shift_down=True
        flag_is_play_otherkey=False      
        debug_print("Debug331")                
      if event.MessageName == "key down" and (event.Key != "Lshift" and event.Key != "Rshift"): 
        flag_is_play_otherkey=True                                                                               
        debug_print("Debug332")                
      if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Rshift"):
        debug_print("Debug333")
        #shift
        flag_is_shift_down=False
        debug_print("Press shift")
      if event.MessageName == "key up" and (event.Key == "Lshift" or event.Key == "Rshift") and config['DEFAULT']['CTRL_SP'] == "0":
        if flag_is_play_otherkey==False:
          toggle_ucl()
          debug_print("Debug315")    
        debug_print("Debug314")
        return True
                
      if event.MessageName == "key down" and event.Key=="Space" and config['DEFAULT']['CTRL_SP']=="1": # check ctrl + space
        if flag_is_ctrl_down == True:
          toggle_ucl()
          return False
      #2021-03-22 修正 英/全 模式下，按 CTRL + 任意鍵，也是穿透的問題
      if is_hf(None)==False and event.MessageName == "key down" and flag_is_ctrl_down == True:
        return True        
      #if event.MessageName == "key up" and len(event.Key) == 1 and is_hf(None)==False:
      #  k = widen(event.Key)
      #  debug_print("335 event.Key to Full:%s %s" % (event.Key,k))
      #  senddata(k)
      #  return False
      #if len(event.Key) == 1 and is_hf(None)==False and event.KeyID !=0 and event.KeyID !=145 and event.KeyID !=162:
      #  k = widen(event.Key)      
      #  senddata(k) 
      debug_print("Debug3: %s" % (event.Transition))
      if event.KeyID==8 or event.KeyID==20 or event.KeyID==45 or event.KeyID==46 or event.KeyID==36 or event.KeyID==33 or event.KeyID==34 or event.KeyID==35 or event.KeyID==160 or event.KeyID==161 or event.KeyID==9 or event.KeyID == 37 or event.KeyID == 38 or event.KeyID == 39 or event.KeyID == 40 or event.KeyID == 231 or event.KeyID == 162 or event.KeyID == 163: #↑←→↓
        return True
      if event.MessageName == "key down" and len( str(chr(event.Ascii)) ) == 1 and is_hf(None)==False and event.Injected == 0 :
        k = widen( str(chr(event.Ascii)) )
        #debug_print("ｋｋｋｋｋｋｋｋｋｋｋｋｋｋｋK:%s" % k)
        senddata(k)
        return False
      return True    
  except Exception as e:
    # 理論上不會發生，也不該發生
    debug_print("KeyPressed")
    debug_print(e)
    return True
      
#程式主流程
#功能說明


# create a hook manager
hm = pyHook.HookManager()
#hm.UnhookMouse();
# watch for all mouse events
hm.KeyAll = OnKeyboardEvent
debug_print(dir(hm))
# set the hook
hm.HookKeyboard()
# wait forever

# watch for all mouse events
# 2021-03-19 改成只Hook MouseAllButtons，MouseAll 好像會造成lag
# From : http://pyhook.sourceforge.net/doc_1.5.0/
#hm.MouseAll = OnMouseEvent
#hm.MouseAllButtons = OnMouseEvent
# set the hook
# 改成按到 shift 才 hook
#hm.HookMouse()

        
#win=gtk.Window(type=gtk.WINDOW_POPUP)
win=gtk.Window(type=gtk.WINDOW_POPUP)
win.set_modal(True)
win.set_resizable(False)



#win.move(screen_width-700,int(screen_height*0.87))
win.move( int(config["DEFAULT"]["X"]) , int(config["DEFAULT"]["Y"]))
#always on top
win.set_keep_above(True)
win.set_keep_below(False)
win.set_skip_taskbar_hint(False)  
win.set_skip_pager_hint(False)
win.set_decorated(False)
win.set_accept_focus(False)
win.set_icon_name(None)

win.add_events( gdk.BUTTON_PRESS_MASK)
win.connect ('button-press-event', winclicked)


vbox = gtk.VBox(False)

hbox=gtk.HBox()
vbox.pack_start(hbox, False)

uclen_btn=gtk.Button("肥")
uclen_label=uclen_btn.get_child()
uclen_label.modify_font(pango.FontDescription(GUI_FONT_22))
uclen_btn.connect("clicked",uclen_btn_click)
uclen_btn.set_size_request(int(float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40 ))
hbox.add(uclen_btn)

hf_btn=gtk.Button("半")
hf_label=hf_btn.get_child()
hf_label.modify_font(pango.FontDescription(GUI_FONT_22))
hf_btn.connect("clicked",hf_btn_click)
hf_btn.set_size_request(int( float(config['DEFAULT']['ZOOM'])*40) ,int(float(config['DEFAULT']['ZOOM'])*40) )
hbox.add(hf_btn)

type_label=gtk.Label("")
type_label.modify_font(pango.FontDescription(GUI_FONT_22))
type_label.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
type_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*100) ,int( float(config['DEFAULT']['ZOOM'])*40) )
type_label.set_alignment(xalign=0.1, yalign=0.5) 
f_type = gtk.Frame()
f_type.add(type_label)
hbox.add(f_type)

word_label=gtk.Label("")
word_label.modify_font(pango.FontDescription(GUI_FONT_20))
word_label.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
word_label.set_size_request(int( float(config['DEFAULT']['ZOOM'])*350),int( float(config['DEFAULT']['ZOOM'])*40))
word_label.set_alignment(xalign=0.05, yalign=0.5)
f_word = gtk.Frame()
f_word.add(word_label)
hbox.add(f_word)

# 加一個簡繁互換的
simple_btn=gtk.Button("")
simple_btn.set_size_request(0,int( float(config['DEFAULT']['ZOOM'])*40))
simple_label=simple_btn.get_child()
simple_label.modify_font(pango.FontDescription(GUI_FONT_16))
#simple_label.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
#simple_label.set_justify(gtk.JUSTIFY_CENTER)
#simple_label.set_alignment(xalign=0.05, yalign=0.5)
f_word = gtk.Frame()
f_word.add(simple_btn)
hbox.add(f_word)


gamemode_btn=gtk.Button("正常模式")
gamemode_label=gamemode_btn.get_child()
gamemode_label.modify_font(pango.FontDescription(GUI_FONT_12))
gamemode_btn.connect("clicked",gamemode_btn_click)
gamemode_btn.set_size_request(int( float(config['DEFAULT']['ZOOM'])*80),int( float(config['DEFAULT']['ZOOM'])*40))
hbox.add(gamemode_btn)

x_btn=gtk.Button("╳")
x_label=x_btn.get_child()
x_label.modify_font(pango.FontDescription(GUI_FONT_14))
x_btn.connect("clicked",x_btn_click)
x_btn.set_size_request(int( float(config['DEFAULT']['ZOOM'])*40),int( float(config['DEFAULT']['ZOOM'])*40))
hbox.add(x_btn)



win.add(vbox)

# 2019-10-20 加入 trayicon
def message(data=None):
  "Function to display messages to the user."
  
  msg=gtk.MessageDialog(None, gtk.DIALOG_MODAL,
    gtk.MESSAGE_INFO, gtk.BUTTONS_OK, data)
  msg.run()
  msg.destroy()

# From : https://github.com/gevasiliou/PythonTests/blob/master/TrayAllClicksMenu.py
class TrayIcon(gtk.StatusIcon):
    def __init__(self):
      global VERSION
      global PWD
      global UCL_PIC_BASE64
      gtk.StatusIcon.__init__(self)
      #self.set_from_icon_name('help-about')
      #debug_print(PWD+"\\UCLLIU.png")
      # base64.b64decode
      # From : https://sourceforge.net/p/matplotlib/mailman/message/20449481/
      raw_data = base64.decodestring(UCL_PIC_BASE64)
      #debug_print(gtk.gdk.Pixbuf)
      w = 16
      h = 16
      img_pixbuf = gtk.gdk.pixbuf_new_from_data(
              raw_data, gtk.gdk.COLORSPACE_RGB, True, 8, w, h, w*4)

      self.set_from_pixbuf(img_pixbuf)
      self.set_tooltip("肥米輸入法：%s" % (VERSION))
      self.set_has_tooltip(True)
      self.set_visible(True)
      self.connect("button-press-event", self.on_click)

    def m_about(self,data=None):  # if i ommit the data=none section python complains about too much arguments passed on greetme
      message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
      message.set_position(gtk.WIN_POS_CENTER_ALWAYS)
      message.set_keep_above(True)
      _msg_text = about_uclliu()       
      message.set_markup( _msg_text )
      #toAlphaOrNonAlpha()
      message.show()
      toAlphaOrNonAlpha()  
      response = message.run()
      #toAlphaOrNonAlpha()
      debug_print("Show Version")
      debug_print(response)
      #debug_print(gtk.ResponseType.BUTTONS_OK)
      if response == -5 or response == -4:
        #message.hide()
        message.destroy()
        #toAlphaOrNonAlpha()  
        play_ucl_label=""
        ucl_find_data=[]
        type_label_set_text()
        toAlphaOrNonAlpha()
        #return False
    def m_sp_switch(self,data=None):
      global config
      if config['DEFAULT']['SP'] == "0":        
        config['DEFAULT']['SP']="1"
      else:
        config['DEFAULT']['SP']="0"
      #切換後，都要存設定
      saveConfig()
    def m_ctrlsp_switch(self,data=None):
      global config
      if config['DEFAULT']['CTRL_SP'] == "0":        
        config['DEFAULT']['CTRL_SP']="1"
      else:
        config['DEFAULT']['CTRL_SP']="0"
      #切換後，都要存設定
      saveConfig()            
    def m_pm_switch(self,data=None):
      global config
      #is_play_music
      if config['DEFAULT']['PLAY_SOUND_ENABLE'] == "0":
         config['DEFAULT']['PLAY_SOUND_ENABLE'] = "1"
      else:
         config['DEFAULT']['PLAY_SOUND_ENABLE'] = "0"
      #切換後，都要存設定
      saveConfig()
    def m_game_switch(self,data=None):
      global gamemode_btn_click
      global gamemode_btn
      gamemode_btn_click(gamemode_btn)      
    def m_quit(self,data=None):
      self.set_visible(False)      
      x_btn_click(self)
    def m_output_type(self,data=None,kind="DEFAULT"):
      global DEFAULT_OUTPUT_TYPE
      debug_print(kind)
      DEFAULT_OUTPUT_TYPE=kind
    def m_none(self,data=None):
      return False
    def on_click(self,data,event): #data1 and data2 received by the connect action line 23
      #print ('self :', self)
      #debug_print('data :',data)
      #debug_print('event :',event)
      btn=event.button #Bby controlling this value (1-2-3 for left-middle-right) you can call other functions.
      #debug_print('event.button :',btn)
      time=gtk.get_current_event_time() # required by the popup. No time - no popup.
      #debug_print ('time:', time)

      global menu
      global menu_items
      global gamemode_btn
      global DEFAULT_OUTPUT_TYPE
      global config      
      global uclen_btn
      global uclen_btn_click
      global hf_btn
      global hf_btn_click
      #debug_print(dir(menu))
      
      #2021-07-22 當按下右下角肥時，原本如果是 肥 -> 英，全 -> 半 才不會檔到畫面
      if is_ucl() == True:
        uclen_btn_click(uclen_btn) 
      if is_hf(None) == False:
        hf_btn_click(hf_btn)
               
      menu.set_visible(False)
      #menu = gtk.Menu()
      for i in range(0,len(menu_items)):
        menu.remove(menu_items[i])
      menu_items=[]
      menu_items.append(gtk.MenuItem("1.關於肥米輸入法"))
      menu.append( menu_items[len(menu_items)-1] )
      menu_items[len(menu_items)-1].connect("activate", self.m_about) #added by gv - it had nothing before
      
      if gamemode_btn.get_label()=="正常模式":        
        menu_items.append(gtk.MenuItem("2.切換至「遊戲模式」"))
      else:
        menu_items.append(gtk.MenuItem("2.切換至「正常模式」"))
      menu.append( menu_items[len(menu_items)-1] )
      menu_items[len(menu_items)-1].connect("activate", self.m_game_switch) #added by gv - it had nothing before

      menu_items.append(gtk.MenuItem("4.選擇出字模式"))
      menu.append( menu_items[len(menu_items)-1] )
      menu_items[len(menu_items)-1].connect("activate", self.m_none)
      #debug_print(dir(menu_items[len(menu_items)-1]))
      # From : https://www.twblogs.net/a/5beb3c312b717720b51efe87
      sub_menu = gtk.Menu()
      sub_menu_items = []
      is_o = ""
      if DEFAULT_OUTPUT_TYPE=="DEFAULT":
        is_o = "●"
      else:
        is_o = "　"      
      sub_menu_items.append(gtk.MenuItem("【%s】正常出字模式" % (is_o)))
      sub_menu.append( sub_menu_items[len(sub_menu_items)-1] )
      sub_menu_items[len(sub_menu_items)-1].connect("activate", self.m_output_type,"DEFAULT")
      
      if DEFAULT_OUTPUT_TYPE=="BIG5":
        is_o = "●"
      else:
        is_o = "　"
      sub_menu_items.append(gtk.MenuItem("【%s】BIG5模式" % (is_o)))
      sub_menu.append( sub_menu_items[len(sub_menu_items)-1] )
      sub_menu_items[len(sub_menu_items)-1].connect("activate", self.m_output_type,"BIG5")
      
      if DEFAULT_OUTPUT_TYPE=="PASTE":
        is_o = "●"
      else:
        is_o = "　"
      sub_menu_items.append(gtk.MenuItem("【%s】複製貼上模式" % (is_o)))
      sub_menu.append( sub_menu_items[len(sub_menu_items)-1] )
      sub_menu_items[len(sub_menu_items)-1].connect("activate", self.m_output_type,"PASTE")
      
      menu_items[len(menu_items)-1].set_submenu(sub_menu)
      #sub_menu.show_all()
      #sub_menu.popup(None, None, None, btn, 2)
      #menu_items[len(menu_items)-1].connect("activate", self.m_game_switch) #added by gv - it had nothing before
      
      if config['DEFAULT']['CTRL_SP'] == "1":
        menu_items.append(gtk.MenuItem("4.【●】使用 CTRL+SPACE 切換輸入法"))
        menu.append( menu_items[len(menu_items)-1] )
        menu_items[len(menu_items)-1].connect("activate", self.m_ctrlsp_switch)
      else:
        menu_items.append(gtk.MenuItem("4.【　】使用 CTRL+SPACE 切換輸入法"))
        menu.append( menu_items[len(menu_items)-1] )
        menu_items[len(menu_items)-1].connect("activate", self.m_ctrlsp_switch)
      
      if config['DEFAULT']['SP'] == "1":
        menu_items.append(gtk.MenuItem("5.【●】顯示短根"))
        menu.append( menu_items[len(menu_items)-1] )
        menu_items[len(menu_items)-1].connect("activate", self.m_sp_switch)
      else:
        menu_items.append(gtk.MenuItem("5.【　】顯示短根"))
        menu.append( menu_items[len(menu_items)-1] )
        menu_items[len(menu_items)-1].connect("activate", self.m_sp_switch)
      
      if config['DEFAULT']['PLAY_SOUND_ENABLE'] == "1":
        menu_items.append(gtk.MenuItem("6.【●】打字音"))
        menu.append( menu_items[len(menu_items)-1] )
        menu_items[len(menu_items)-1].connect("activate", self.m_pm_switch)
      else:
        menu_items.append(gtk.MenuItem("6.【　】打字音"))
        menu.append( menu_items[len(menu_items)-1] )
        menu_items[len(menu_items)-1].connect("activate", self.m_pm_switch)
                        
      menu_items.append(gtk.MenuItem(""))
      menu.append( menu_items[len(menu_items)-1] )
      
      menu_items.append(gtk.MenuItem("離開(Quit)"))
      menu.append( menu_items[len(menu_items)-1] )
      menu_items[len(menu_items)-1].connect("activate", self.m_quit)

      #add space
      menu_items.append(gtk.MenuItem(""))
      menu.append( menu_items[len(menu_items)-1] )
      menu_items.append(gtk.MenuItem(""))
      menu.append( menu_items[len(menu_items)-1] )
      menu_items.append(gtk.MenuItem(""))
      
      
      menu.show_all()      
      menu.popup(None, None, None, btn, 2) #button can be hardcoded (i.e 1) but time must be correct.      
      #menu.reposition()
      #debug_print(dir(menu))

  #message("Status Icon Left Clicked")
  #make_menu(event_button, event_time)
# 生成肥圖片
#if my.is_file(PWD+"\\UCLLIU.png") == False:
#  my.file_put_contents(PWD+"\\UCLLIU.png",my.base64_decode(UCL_PIC_BASE64))  
menu_items = []
menu = gtk.Menu()  
tray = TrayIcon()

#icon.set_visible(True)
# Create menu

 


win.show_all()
simple_btn.set_visible(False)

if config["DEFAULT"]["SHORT_MODE"] == "1":
  run_short()
else:
  run_long()  
  


win.set_focus(None)

# 初使化按二次
#uclen_btn_click(uclen_btn)
#uclen_btn_click(uclen_btn)

#set_interval(1)

#gtk.main()
updateGUI_Step = 0
def updateGUI():
  global updateGUI_Step
  #global is_shutdown
  while gtk.events_pending():
    gtk.main_iteration(False)
  updateGUI_Step = updateGUI_Step + 1
  if updateGUI_Step % 100 == 0:
    updateGUI_Step = 0
    toAlphaOrNonAlpha()
while True:
  time.sleep(0.01)
  #debug_print("gg")
  updateGUI()      
pythoncom.PumpMessages()     

#mainloop()
  
 
