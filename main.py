
#TODO 画像比率

import argparse
from time import sleep
import uuid
import glob
from datetime import date
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# コマンドライン引数関係
parser = argparse.ArgumentParser(description="anki")
split_list = lambda x:list(map(int, x.split("x")))
parser.add_argument("--show", help="処理中の自動操作されてる画面を表示するか", action="store_true")
parser.add_argument("-s", "--imgsize", help="画像サイズ", type=split_list, default=[700, 700])
#TODO これファイル名にする prefixにする？
parser.add_argument("-t", "--searchtag", help="検索用タグ", type=str, default=str(date.today()))
parser.add_argument("-d", "--outputdir", help="画像ファイルの出力先ディレクトリ", type=str,
                    default=glob.glob("/Users/*/Library/Application Support/Anki2/*/collection.media")[0])
parser.add_argument("-c", "--searchcolumn", help="検索する列（クイズの問題集とかだったら2がいいと思う）", type=int, default=1)
#TODO これいる？
parser.add_argument("-p", "--prefix", help="ファイル名の頭につける文字列", type=str, default="google-img--")
args = parser.parse_args()


# seleniumの設定
options = webdriver.ChromeOptions()
if not args.show:
    options.add_argument("--headless")
options.add_argument('--hide-scrollbars')
driver = webdriver.Chrome(options=options)
driver.set_window_size(args.imgsize[0], args.imgsize[1])

# 出力用ディレクトリがなかったら生成
if not os.path.isdir("./output"):
    os.mkdir("./output")

# 同じ階層にある.txtファイル取得
anki_files = glob.glob("./*.txt")

# ankiファイル1個ずつ処理
for anki_file in anki_files:
    print(f"{anki_file} を処理中...")
    with open(anki_file) as f:
        output_lines = []
        lines = f.readlines()
        lines_len = len(lines)

    # 1行ずつ処理
    for cnt,line in enumerate(lines):

        # コメントの行は無視
        if not line[0] == "#":
            column = line.replace("\n","").split("\t")
            search_word = column[args.searchcolumn - 1]

            # 画像検索
            driver.get("https://www.bing.com/images/search?safeSearch=Moderate&mkt=en-US&q="+search_word)

            # 読み込まれるまで待つ（15秒読み込まれなかったらタイムアウト）
            WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
            sleep(1)    # 念の為追加

            # 検索バーとか隠す
            driver.execute_script("""
document.querySelector("#b_header").hidden = true;
document.querySelector("#rfPane").hidden = true;
""")

            # 画像ファイルの名前（重複回避にUUID）
            word_uuid = str(uuid.uuid1())
            img_name = args.prefix + search_word + "-" + word_uuid + "-" + args.searchtag

            # スクショ
            driver.save_screenshot(args.outputdir+"/"+img_name+".png")

            # 1秒待つ（短い期間にアクセスしすぎるとよくない）
            sleep(1)

            # output_line = f'{column[0]}\t"{column[1]}<br><img src=""{img_name}.png"" width=""{img_size}%"" height=""{img_size}%"">"\n'
            output_line = f'{column[0]}\t"{column[1]}<br><img src=""{img_name}.png"">"\n'
            output_lines.append(output_line)

        else:
            output_lines.append(line)

        # 進捗表示
        progress = int(((cnt+1)/lines_len)*50)
        progress_per = "{:.1f}".format(((cnt+1)/lines_len)*100)
        print("\r{}%  {}".format(progress_per, "#"*progress), end="")

    # outputファイル生成
    output_file_name = "./output/"+os.path.basename(anki_file)
    if os.path.isfile(output_file_name):
        os.remove(output_file_name)
    with open(output_file_name, "x") as f:
        f.writelines(output_lines)

    # 出力見やすいように
    print("\n")


# 終了
driver.quit()
print("--- 処理が完了しました ---")
