from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import keyboard
import os

class main:
    def __init__(self, anum=1): # anum ==> account number(default=0)
        self.num = anum
        self.UserDir = os.getlogin() # C:\Users\(UserDir)\AppData\Local\Google\Chrome\User Data ユーザー名取得
        self.options = webdriver.ChromeOptions()
        self.options.use_chromium = True # エラーを出なくする
        self.options.add_argument("--start-maximized") # 最大画面で開始
        self.options.add_experimental_option("prefs", {"download.default_directory":"./accounts/{}/download".format(anum), "credentials_service":False}) # download directoryの指定, password保存機能のポップアップ無効化
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument("--user-data-dir="+"C:/Users/"+self.UserDir+"/AppData/Local/Google/Chrome/User Data") # User Dir追加
        with open("./accounts/"+str(anum)+"/dir.txt", mode="r") as f:
            self.options.add_argument("--profile-directory="+f.readlines()[0]) # googleにログインした状態で開始
        self.driver_dir = "./webdriver/chromedriver.exe" # web driverのディレクトリ指定
        self.driver = webdriver.Chrome(executable_path=self.driver_dir, options=self.options)
        self.driver.get("https://www.google.co.jp") # google展開 /html/body/div[1]/div[2]/div/div[2]/div/div[2]/div[3]/div/div/section/div[3]/div/ul/li[1]/div/div[1]/div/a

    def pixiv(self, name=(), delay=5): # pixivの画像自動収集プログラム, name ==> ユーザーの番号で, delay ==> 接続拒否回避のために入れる待機時間, 目的とするurlを開いてから
        self.pixiv_path = f"./accounts/{self.num}/download/pixiv"
        if os.path.isdir(self.pixiv_path) == False: # download内部にpixivディレクトリが存在しない場合はディレクトリを生成
            os.makedirs(self.pixiv_path)
        self.target_url = []
        self.save_dir_path = [] # DLしてきたデータをセーブする場所一覧(絵師ごとに分けるために必須のリスト)
        for i in name:
            self.driver.get(f"https://www.pixiv.net/users/{i}")
            self.name = self.driver.find_element(By.XPATH, "//*[@id=\"root\"]/div[2]/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/h1").text
            self.name_path = self.pixiv_path + f"/{self.name}" # 処理中に開いているpixivのユーザーのディレクトリのパス生成
            if os.path.isdir(self.name_path) == False: # ディレクトリが存在しないならば作成
                os.makedirs(self.name_path)
            self.save_dir_path.append(self.name_path) # urlを取得する作品群を描いた絵師の絵を保存しているディレクトリパス
            self.target_url.append([])
            for elem in self.driver.find_elements_by_xpath("//a"):
                self.target_url[-1].append(elem.get_attribute("href")) # 目的のユーザーの作品一覧から作品のurlのリストを作成
#        print(self.target_url)
        

    def quit(self): # 終わり
        self.driver.quit()

def activator(num=(1,)):
    data = []
    for i in num:
        data.append(main(i))
        data[-1].pixiv((2848117, ))

if __name__ == "__main__":
    activator((1,))