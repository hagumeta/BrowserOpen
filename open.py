import os, signal
import chromedriver_binary                  # パスを通すためのコード
from dotenv import load_dotenv
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

load_dotenv()
APP_NAME="BrowserOpen"
USERDATA_DIR = os.environ["USERDATA_DIR"] or ""
PROFILE_DIR = os.environ["PROFILE_DIR"] or ""
BROWSER_MODE = os.environ["BROWSER_MODE"] or 0

def main(): 
  useSecret = True
  if BROWSER_MODE == 'user':
    useSecret = False
  elif BROWSER_MODE == 'secret':
    useSecret = True
  else:
    useSecret = messagebox.askyesno(APP_NAME, 'シークレットモードで開く？')
  
  urlList = ReadRowsFromFile()
  OpenChromeTabs(urlList, useSecret, USERDATA_DIR, PROFILE_DIR)
  messagebox.showinfo(APP_NAME, '終わったよ')


def ReadRowsFromFile():
  _rowList = []
  _typ = [('テキストファイル','*.txt')] 
  _dir = '{0}/urlFiles'.format(__file__)

  try: 
    _urlFile = filedialog.askopenfilename(filetypes = _typ, initialdir = _dir) 
    _f = open(_urlFile, 'r')
    for line in _f.readlines(): 
      _rowList.append(line.replace("\n", ""))
    _f.close()
  except: 
    _rowList = []
  finally: 
    return _rowList


def OpenChromeTabs(urlList = [], withSecretMode = True, profileUserDir = '', profileDir = ''): 
  _option = Options()                          # オプションを用意
  if withSecretMode:
    # シークレットモードの設定を付与
    _option.add_argument('--incognito')
  else:
    # 通常モードの設定を付与 
    if (not not profileUserDir) and (not not profileDir):
      _option.add_argument('--user-data-dir=' + profileUserDir)
      _option.add_argument('--profile-directory=' + profileDir)

  _driver = webdriver.Chrome(options=_option)

  try: 
    _driver.get('https://www.google.com/')
    for url in urlList:
      # URLを指定して、新しいタブを開く
      _driver.execute_script("window.open('{0}');".format(url))
  finally: 
    os.kill(_driver.service.process.pid, signal.SIGTERM)


main()