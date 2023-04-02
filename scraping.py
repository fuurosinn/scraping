from selenium import webdriver # web開くために必須
from selenium.webdriver.common.by import By # 全体をimportしても全てはimportされないので指定してimport必須
import urllib.request # 画像データ取得のために必須
from fake_useragent import UserAgent # 直リンクの403エラー(アクセス拒否)を接続要求のリファラー部分を改竄して回避するので必須
import time # 時間関連。後で接続出来てないのを検知するために使う可能性があるので必須
import os # ファイルとか存在有無を調べたりファイル作成のために必須
from random import uniform, randint # 乱数入れてプログラムとバレにくくしたいけど効果は不明
import sys
"""
main.eroterestのopen()のところで
"UnicodeDecodeError: 'cp932' codec can't decode byte 0x86 in position 23: illegal multibyte sequence"
が起こるけど、それを回避するためにsys.getdefaultencoding()でopen関数のエンコーディングを合わせておかないといけないので必須
"""
ua = UserAgent()
ua_chrome = ua.chrome # chromeのUser Agent取得

del_charactors = [".", "\\", "/", ":", ";", "*", "?", "\"", "<", ">", "|", ""] # ファイル名として使ったらエラー出る(「.」とか「/」みたいな動作に関わる奴ら)文字のブラックリスト。これを参照して文字を削除する。 ただしこれは単体の文字であるために"com"などの禁止されている文字列には非対応

def req_data(referrer, url, fname): # referrer ==> リファラー, request data, fname ==> file name
    opener = urllib.request.build_opener()
    opener.addheaders = [("referer", referrer), ("UserAgent", str(ua_chrome))]
    with opener.open(url) as bimg, open(fname, mode="wb") as wimg:
        wimg.write(bimg.read())
    print(f"Successed saving:{url}")

class main:
    def __init__(self, anum=1): # anum ==> account number(default=0)
        self.num = anum
        self.UserDir = os.getlogin() # C:\Users\(UserDir)\AppData\Local\Google\Chrome\User Data ユーザー名取得
        self.options = webdriver.ChromeOptions()
        self.options.use_chromium = True # エラーを出なくする
        self.options.add_argument("--start-maximized") # 最大画面で開始
#        self.options.add_argument("--headless")
        self.options.add_experimental_option("prefs", {"download.default_directory":"./accounts/{}/download".format(self.num), "credentials_service":False}) # download directoryの指定, password保存機能のポップアップ無効化
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument("--user-data-dir="+"C:/Users/"+self.UserDir+"/AppData/Local/Google/Chrome/User Data") # User Dir追加
        with open("./accounts/"+str(self.num)+"/dir.txt", mode="r") as f:
            self.options.add_argument("--profile-directory="+f.readlines()[0]) # googleにログインした状態で開始
        self.driver_dir = "./webdriver/chromedriver.exe" # web driverのディレクトリ指定
        self.driver = webdriver.Chrome(executable_path=self.driver_dir, options=self.options)
        self.driver.get("https://www.google.co.jp") # google展開 /html/body/div[1]/div[2]/div/div[2]/div/div[2]/div[3]/div/div/section/div[3]/div/ul/li[1]/div/div[1]/div/a

    def pixiv(self, name=(), commands=(), delay=5): # pixivの画像自動収集プログラム, name ==> ユーザーの番号で, commands ==> 取得しない例外等を設けられる, delay ==> 接続拒否回避のために入れる待機時間, ミリ秒で指定, 目的とするurlを開いてから
        self.pixiv_path = f"./accounts/{self.num}/download/pixiv"
        if os.path.isdir(self.pixiv_path) == False: # download内部にpixivディレクトリが存在しない場合はディレクトリを生成
            os.makedirs(self.pixiv_path)
        self.rejected_file_type = () # この中に入っている拡張子は保存しない

        for i in name: # lim ==> 制限等
            self.driver.get(f"https://www.pixiv.net/users/{i}/artworks") # アクセス
            self.name = self.driver.find_element(By.XPATH, "//*[@id=\"root\"]/div[2]/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/h1").text # 対象のユーザー名
            print(f"Start:name={self.name}")
            self.target_url = []

            self.name_path = self.pixiv_path + f"/{self.name}" # 処理中に開いているpixivのユーザーのディレクトリのパス生成
            if os.path.isdir(self.name_path) == False: # ディレクトリが存在しないならば作成
                os.makedirs(self.name_path)

            self.page = 0
            while True:
                print(f"Page:{self.page}")
                self.pix_t0 = time.time()
                for elem in self.driver.find_elements(By.XPATH, "//a[@class=\"sc-d98f2c-0 sc-rp5asc-16 iUsZyY sc-eWnToP khjDVZ\"]"): # class指定してタグaを選別
                    self.elem = elem.get_attribute("href")
                    self.target_url.append(self.elem[self.elem.rfind("/")+1:]) # わざわざhttps~~/artworks/(number)丸ごと記録するよりも、(number)のみのほうが良いので数字抜き出して記録
                if self.driver.find_elements(By.XPATH, "//a[@class=\"sc-d98f2c-0 sc-xhhh7v-2 cCkJiq sc-xhhh7v-1-filterProps-Styled-Component Vhbyn\"]")[-1].get_attribute("aria-disabled") == "true": # 「>」みたいなボタンが隠されているならbreak
                    break
                self.page += 1
                while True:
                    if time.time()-self.pix_t0 >= delay:
                        break
                    time.sleep(0.1)
                self.driver.get(self.driver.find_elements(By.XPATH, "//a[@class=\"sc-d98f2c-0 sc-xhhh7v-2 cCkJiq sc-xhhh7v-1-filterProps-Styled-Component Vhbyn\"]")[-1].get_attribute("href"))

            for artnum in self.target_url:
#                self.driver.get("https://www.google.co.jp")
                self.artworks_url = f"https://pixiv.net/artworks/{artnum}"
                time.sleep(delay)
                self.driver.get(self.artworks_url) # 作品に接続
                print(f"Accessed:{self.artworks_url}")
                if len(self.driver.find_elements(By.XPATH, "//button[@class=\"sc-emr523-0 guczbC\"]")) > 0: # "全て見る"ボタンが存在しているなら要素数が1になる
                    if self.driver.find_element(By.XPATH, "//button[@class=\"sc-emr523-0 guczbC\"]/div[@class=\"sc-emr523-2 drFRmD\"]").text == "作品を読む":
                        print("Button Type is not \"show all\":continue")
                        continue
                    self.driver.find_element(By.XPATH, "//button[@class=\"sc-emr523-0 guczbC\"]").click()
                self.title = self.driver.find_element(By.XPATH, "//h1[@class=\"sc-1u8nu73-3 lfwBiP\"]").text # タイトル取得
                self.posted_time = self.driver.find_element(By.XPATH, "//div[@class=\"sc-5981ly-0 jTkljN\"]").text # 投稿日時取得, "/html/body/div[1]/div[2]/div/div[2]/div/div[1]/main/section/div[1]/div/figcaption/div/div/div[4]"

                self.editted_title = self.title # タイトルの中に含まれるファイル名にしたらエラー出る文字を編集(削除する)
                self.detected_charactors = list((set(list(self.title)) & set(del_charactors)))
                if len(self.detected_charactors) != 0:
                    print(f"Detected charactor that listed in blacklist:{self.detected_charactors}")
                for charactor in self.detected_charactors:
                    print(f"Delete:\"{charactor}\"")
                    self.editted_title = self.editted_title.replace(charactor, "") # ブラックリストに含まれる文字を削除

                if os.path.isdir(f"{self.name_path}/{self.editted_title}") == False:
                    os.makedirs(f"{self.name_path}/{self.editted_title}") # 作品名ごとにファイル作成
                try:
                    with open(f"{self.name_path}/{self.title}/info.txt", mode="w") as f: # ハッシュタグ等記録関連
                        f.write(f"title:{self.title}\n") # タイトル(未編集)
                        f.write(f"url:{self.artworks_url}\n") # url
                        f.write(f"posted time:{self.posted_time}\n") # 投稿日時
                        f.write("tags:")
                        self.tags = ""
                        for tags_num in self.driver.find_elements(By.XPATH, "//li[@class=\"sc-pj1a4x-1 iWBYKe\"]//a"): # ハッシュタグ記録
                            self.tags = self.tags+tags_num.text
                            self.tags = self.tags+", "
                        self.tags = self.tags[:-2]
                        f.write(self.tags)
                except:
                    print("Error:tag error")

                self.img_number = -1
                for elem in self.driver.find_elements(By.XPATH, "//a[@class=\"sc-1qpw8k9-3 eFhoug gtm-expand-full-size-illust\"]"): # 画像url取得
                    self.img_number += 1
                    self.file_type = elem.get_attribute("href") # 拡張子判定
                    try:
                        self.file_type = self.file_type[self.file_type.rindex("."):]
                        if self.file_type in self.rejected_file_type:
                            continue
                    except:
                        continue
                    self.url = elem.get_attribute("href")
                    req_data(self.artworks_url, self.url, f"{self.name_path}/{self.editted_title}/{self.img_number}{self.file_type}")
                    time.sleep(uniform(2.0, 3.0))

    def eroterest_spam(self, path=None, time=100, delay=3): # path ==> .txtに書き込んでやるとその中から均等な割合でランダムに選んでスパムする。
        self.encoding_type = sys.getdefaultencoding() # oepn関数のエンコーディング方法を合わせるために必須
        print(f"Encoding Type:{self.encoding_type}")
        path_ = f"./accounts/{self.num}/eroterest/spam.txt" if path == None else path
        with open(path_, mode="r", encoding=self.encoding_type) as f:
            self.words = f.readlines()
        self.len = len(self.words)-1
        self.driver.get("https://anime.eroterest.net")
        i = 0
        while i < 10:
            self.search_bar = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/div[1]/div/div/div[1]/div/div[1]/form/div/input")
            self.search_bar.clear()
            self.search_bar.send_keys(self.words[randint(0, self.len)])
            try:
                self.search_bar.submit()
            except:
                pass
            time.sleep(delay)
            i += 1
#            pass # /html/body/div[1]/div/div[3]/div[1]/div[1]/div/div/div[1]/div/div[1]/form/div/input

    def quit(self): # 終わり
        self.driver.quit()

def activator(num=(1,)):
    data = main()
#    data.pixiv((39123643, 2886368, 2848117, 3316400, 14488269, 3316400)) # 64390150, 59578913, ←終了済み| 10706782, 29362997, ←まだ
    data.eroterest_spam()
    data.quit()

if __name__ == "__main__":
    activator((1,))