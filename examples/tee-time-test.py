import sys
#import pyautogui
#import pyscreeze
from seleniumbase import SB
#import datetime
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
import argparse
import os

### Define Functions

def get_text(source_text = None, left = None, right = None, count = 1):
    if source_text is None or left is None or right is None:
        return ''

    left_position = source_text.find(left)
    if left_position == -1: return ''
    right_position = source_text.find(right, left_position + 1)
    if right_position == -1: return ''

    if count > 1:
        occurrence_count = 2
        while occurrence_count <= count:
            occurrence_count += 1
            left_position = source_text.find(left, right_position + 1)
            if left_position == -1: return ''
            right_position = source_text.find(right, left_position + 1)
            if right_position == -1: return ''

    return source_text[left_position + len(left) : right_position].strip()

def main():
  print("****************************************")
  print("Auto Tee Time Script version 3.0 Using SeleniumBase CDP")
  #### Initialize Variables
  testMode = True
  ghost = False
  memberNumber = "785-000"
  memberPassword="rodif1806"
  #memberPassword = os.environ["TOKEN"]
  memberName = "Rochelle Cohn"
  triggerTimeStr = ""    # string  HH:MM:SS AP 
  firstTime = "6:00 AM"
  daysOut = 5
  partner1 = ""
  partner2 = ""
  partner3 = ""
  
  ##### 
  
  # Construct the argument parser
  ap = argparse.ArgumentParser()
  ap.add_argument("-a","--action_time", type=str, help="Time when desired date becomes available, AKA trigger time")
  ap.add_argument("-d","--days_out", type=int, help="Number of days from today to look for tee time")
  ap.add_argument("-e","--early_time", type=str, help="Earliest time to look for an opening, AKA first time")
  ap.add_argument("-m","--member_number", type=str, help="Member Number to use for log in")
  ap.add_argument("-n","--name", type=str, help="Member Name select user")
  ap.add_argument("-p","--password", type=str, help="Password to use for log in")
  ap.add_argument("-r","--run",action="store_true", help="run mode must be selected to save tee time")
  ap.add_argument("-g","--ghost",action="store_true", help="ghost to hide chrome window")
  ap.add_argument("-t","--test",action="store_true", help="test mode must be selected to NOT save tee time")
  ap.add_argument("-1","--partner1", type=str, help="Last, First name of partner 1")
  ap.add_argument("-2","--partner2", type=str, help="Last, First name of partner 2")
  ap.add_argument("-3","--partner3", type=str, help="Last, First name of partner 3")
  args=ap.parse_args()
  
  if args.action_time:
      triggerTimeStr=args.action_time
      print("trigger time set by command line to: "+triggerTimeStr)
  else:
      print("Trigger time set by default to: "+triggerTimeStr)
  
  if args.days_out:
      daysOut=args.days_out
      print("days out set by command line to: "+str(daysOut))
  else:
      print("days out time set by default to: "+str(daysOut))
  
  if args.early_time:
      firstTime=args.early_time
      print("first time set by command line to: "+firstTime)
  else:
      print("first time set by default to: "+firstTime)
  
  if args.member_number:
      memberNumber=args.member_number
      print("Member Number set by command line to: "+memberNumber)
  else:
      print("Member Number set by default to: "+memberNumber)
  
  if args.name:
      memberName=args.name
      print("Member Name set by command line to: "+memberName)
  else:
      print("Member Name set by default to: "+memberName)
  
  if args.password:
      memberPassword=args.password
      print("Password set by command line to: "+memberPassword)
  else:
      print("Password set by default to: "+memberPassword)
  
  if args.run:
      testMode=False
      print("test mode is set by command line to "+str(testMode))
      
  else:
      print("no run mode setting from command line, test mode stays as: "+str(testMode))
  
  if args.test:
      testMode=True
      print("test mode is set by command line to "+str(testMode))
  else:
      print("no test mode setting from command line, test mode stays as: "+str(testMode))
  
  if args.ghost:
      print("browser display set to ghost command line")
      ghost = True
  else:
      print("browser set to show by default")
  
  if args.partner1:
      partner1=args.partner1
      print("partner1 set by command line to: "+partner1)
  else:
      print("Partner1 set by default to: "+partner1)
  
  if args.partner2:
      partner2=args.partner2
      print("partner2 set by command line to: "+partner2)
  else:
      print("Partner2 set by default to: "+partner2)
  
  if args.partner3:
      partner3=args.partner3
      print("partner2 set by command line to: "+partner3)
  else:
      print("Partner2 set by default to: "+partner3)
  
  partnerList = [partner1, partner2, partner3]
  
  
  
  if triggerTimeStr == "":
      triggerTime = datetime.now() +timedelta(seconds=45)
      triggerTimeStr=triggerTime.strftime("%-I:%M:%S %p")
  print("Trigger time: "+triggerTimeStr)
  
  
  requestDate = datetime.now() + timedelta(days = daysOut)
  requestDateStr = requestDate.strftime("%m/%d/%Y")
  print("Requested Tee Time Date: "+requestDateStr)
  ssName = requestDate.strftime("%Y%m%d")
  
  agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0.0.0"
  if "linux" in sys.platform:
      agent = None  # Use the default UserAgent
  
  with SB(uc=True, test=True, rtf=True, agent=agent, headed= False) as sb:
      #sb.maximize_window()
      url = "https://www.elcaminoclub.com/login"
      sb.activate_cdp_mode(url)
      #sb.uc_gui_handle_cf()  # Ready if needed!
      sb.cdp.type("#lgUserName",memberNumber)
      sb.cdp.type("#lgPassword",memberPassword)
      sb.cdp.click("#lgLoginButton")
      sb.cdp.click("#hovDiv")
      sb.sleep(2)
      sb.cdp.save_screenshot(ssName+"_ss1.png")
      sb.cdp.click(memberName)
      sb.sleep(2)
      sb.cdp.save_screenshot(ssName+"_ss2.png")
      #print(sb.get_text("#tt1_left > p > span.serverClock > span > b"))
      serverClock=sb.cdp.get_text("#tt1_left > p > span.serverClock > span > b")
      print(serverClock+" vs "+triggerTimeStr)
      while serverClock != triggerTimeStr:
      
          serverClock=sb.cdp.get_text("#tt1_left > p > span.serverClock > span > b")
      
      print("Trigger Time Reach, Loading tee time sheet")
      
      date_url ="https://www1.foretees.com/v5/elcaminocc_golf_m56/Member_sheet?calDate="+requestDateStr+"&course=&displayOpt=0"
      sb.cdp.open(date_url)
      
      
      ###TODO make sure we got to the teesheet page for the requested date
      
      ### find the first open tee time after first time parameter
      earlyTime = datetime.strptime(firstTime, "%I:%M %p")
      time_str = ""
      pageText =sb.cdp.get_page_source()
      availableTimeCount = pageText.count('newreq')
      print("number of tt choices to check: " + str(availableTimeCount))
      for tt in range(availableTimeCount):
          time_code =get_text(pageText,'newreq', 'a>',tt+1)
          time_str =get_text(time_code,'>','<')
          print('available tee time: '+time_str)
          availableTimeValue = datetime.strptime(time_str, "%I:%M %p")
          if availableTimeValue >= earlyTime:
              print('found an open tee time '+time_str)
              break
    
      sb.cdp.click(time_str)
  
  
      sb.sleep(1)
      sb.cdp.save_screenshot(ssName+"_ss3.png")
      
      if sb.cdp.is_element_visible('body > div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.newpropushbelowmenu.ui-dialog-buttons > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(2) > span'):
          #Click continue if alternate tee time dialog box is presented
          print("tee time selected is already in use")
          sb.cdp.click('/html/body/div[5]/div[4]/div/button[2]/span')
          sb.sleep(1)
          
      else:
          print("tee time selected is avaialble")
  
      
  
      #confirm that transport is selected for initial member, if not set it to gc
      sb.cdp.click("/html/body/div[3]/div/div[3]/div[6]/div/div[2]/div/div[2]/form/div[1]/div[2]/div[1]/div[4]/select")
      sb.sleep(1)
      sb.cdp.click("/html/body/div[3]/div/div[3]/div[6]/div/div[2]/div/div[2]/form/div[1]/div[2]/div[1]/div[4]/select")
      sb.cdp.type("/html/body/div[3]/div/div[3]/div[6]/div/div[2]/div/div[2]/form/div[1]/div[2]/div[1]/div[4]/select",'G')
  
      ## Enter partner 1
      if partner1:
          print("Entering partner 1 "+ partner1)
          sb.cdp.click('//*[@id="main"]/div[6]/div/div[1]/div[2]/div[2]/ul/li[2]/div')
          sb.sleep(1)
          sb.cdp.click('/html/body/div[3]/div/div[3]/div[6]/div/div[1]/div[2]/div[2]/div[2]/div[1]/input')
          sb.sleep(1)
          sb.cdp.type('//*[@id="main"]/div[6]/div/div[1]/div[2]/div[2]/div[2]/div[1]/input', partner1)
          sb.cdp.click('/html/body/div[3]/div/div[3]/div[6]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/div/span') 
          #Set Transport Type   
          sb.cdp.click("/html/body/div[3]/div/div[3]/div[6]/div/div[2]/div/div[2]/form/div[1]/div[2]/div[2]/div[4]/select")
          sb.sleep(1)
          sb.cdp.click("/html/body/div[3]/div/div[3]/div[6]/div/div[2]/div/div[2]/form/div[1]/div[2]/div[2]/div[4]/select")
          sb.cdp.type("/html/body/div[3]/div/div[3]/div[6]/div/div[2]/div/div[2]/form/div[1]/div[2]/div[2]/div[4]/select",'G')
  
      
      ## Enter partner 2
      if partner2:
          print("Entering partner 1 "+ partner2)
          sb.cdp.click('//*[@id="main"]/div[6]/div/div[1]/div[2]/div[2]/ul/li[2]/div')
          sb.sleep(1)
          sb.cdp.click('/html/body/div[3]/div/div[3]/div[6]/div/div[1]/div[2]/div[2]/div[2]/div[1]/input')
          sb.sleep(1)
          sb.cdp.type('//*[@id="main"]/div[6]/div/div[1]/div[2]/div[2]/div[2]/div[1]/input', partner2)
          sb.cdp.click('/html/body/div[3]/div/div[3]/div[6]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/div/span') 
          #Set Transport Type   
          sb.cdp.click("/html/body/div[3]/div/div[3]/div[6]/div/div[2]/div/div[2]/form/div[1]/div[2]/div[3]/div[4]/select")
          sb.sleep(1)
          sb.cdp.click("/html/body/div[3]/div/div[3]/div[6]/div/div[2]/div/div[2]/form/div[1]/div[2]/div[3]/div[4]/select")
          sb.cdp.type("/html/body/div[3]/div/div[3]/div[6]/div/div[2]/div/div[2]/form/div[1]/div[2]/div[3]/div[4]/select",'G')
  
      ## Enter partner 3
      if partner3:
          print("Entering partner 1 "+ partner3)
          sb.cdp.click('//*[@id="main"]/div[6]/div/div[1]/div[2]/div[2]/ul/li[2]/div')
          sb.sleep(1)
          sb.cdp.click('/html/body/div[3]/div/div[3]/div[6]/div/div[1]/div[2]/div[2]/div[2]/div[1]/input')
          sb.sleep(1)
          sb.cdp.type('//*[@id="main"]/div[6]/div/div[1]/div[2]/div[2]/div[2]/div[1]/input', partner3)
          sb.cdp.click('/html/body/div[3]/div/div[3]/div[6]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/div/span') 
          #Set Transport Type   
          sb.cdp.click("/html/body/div[3]/div/div[3]/div[6]/div/div[2]/div/div[2]/form/div[1]/div[2]/div[4]/div[4]/select")
          sb.sleep(1)
          sb.cdp.click("/html/body/div[3]/div/div[3]/div[6]/div/div[2]/div/div[2]/form/div[1]/div[2]/div[4]/div[4]/select")
          sb.cdp.type("/html/body/div[3]/div/div[3]/div[6]/div/div[2]/div/div[2]/form/div[1]/div[2]/div[4]/div[4]/select",'G')
  
      sb.cdp.save_screenshot(ssName+"_ss4.png")
  
  
      if testMode:
          print("Test mode enabled, tee time will not be saved")
          sb.cdp.click("Go Back")
      else:
          print("real mode enabled, tee time will be saved.")
          sb.cdp.click("submit_request_button")
          sb.sleep(2)
          sb.cdp.click('/html/body/div[5]')
          sb.cdp.click('/html/body/div[5]/div[4]/div/button')
      sb.sleep(5) 
      sb.cdp.save_screenshot(ssName+"_ss5.png")
      print("tee time script completed")

if __name__ == '__main__':
  main()
