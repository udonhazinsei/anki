import argparse
from time import sleep
import uuid
import glob
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# コマンドライン引数関係
parser = argparse.ArgumentParser()
parser.add_argument("--show", action="store_true")
parser.add_argument("-s", "--imgsize", type=str, default="700x700")
parser.add_argument("-d", "--outputdir", type=str,
                    default="/Users/*/Library/Application Support/Anki2/*/collection.media")
parser.add_argument("-c", "--searchcolumn",type=int, default=1)
parser.add_argument("-p", "--prefix", type=str)
parser.add_argument("-r", "--imgratio", type=float, default=1)
args = parser.parse_args()

window_w, window_h = map(int, args.imgsize.split("x"))
img_ratio = args.imgratio
output_dir = glob.glob(args.outputdir)[0]


# seleniumの設定
options = webdriver.ChromeOptions()
if not args.show:
    options.add_argument("--headless")
options.add_argument('--hide-scrollbars')
driver = webdriver.Chrome(options=options)
driver.set_window_size(window_w, window_h+139)

# 出力用ディレクトリがなかったら生成
if not os.path.isdir("./output"):
    os.mkdir("./output")

# 同じ階層にある.txtファイル取得
anki_files = glob.glob("./*.txt")
files_len = len(anki_files)

# ankiファイル1個ずつ処理
for file_cnt,anki_file in enumerate(anki_files):
    # prefix
    if args.prefix:
        prefix = args.prefix + "--"
    else:
        prefix = os.path.splitext(os.path.basename(anki_file))[0] + "--"

    # ファイル読み込み
    with open(anki_file) as f:
        lines = f.readlines()
        lines_len = len(lines)

    output_lines = []

    # Log
    print(f"{anki_file} を処理中...（{file_cnt+1} / {files_len}）")

    # 1行ずつ処理
    for line_cnt,line in enumerate(lines):
        # コメントの行・改行のみの行は無視
        if line[0] == "#":
            output_lines.append(line.replace("#html:false", "#html:true"))
        elif line == "\n":
            pass
        else:
            column = line.replace("\n","").split("\t")
            search_word = column[args.searchcolumn - 1]

            # 画像検索
            driver.get("https://www.bing.com/images/search?safeSearch=Moderate&mkt=en-US&q="
                        + search_word)

            # 読み込まれるまで待つ（15秒読み込まれなかったらタイムアウト）
            WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
            sleep(1)    # 念の為追加

            # 検索バーとか隠す
            driver.execute_script("""
document.querySelector("#b_header").hidden = true;
document.querySelector("#rfPane").hidden = true;
document.querySelector("#fbpgbt").remove();
""")

            # 画像ファイルの名前（重複回避にUUID）
            word_uuid = str(uuid.uuid1())
            img_name = prefix + search_word + "-" + word_uuid

            # スクショ
            driver.save_screenshot(output_dir+"/"+img_name+".png")

            # 1秒待つ（短い期間にアクセスしすぎるとよくない）
            sleep(1)

            output_line = f'{column[0]}\t"{column[1]}<br><img src=""{img_name}.png"" \
width=""{int(window_w*img_ratio)}"" height=""{int(window_h*img_ratio)}"">"\n'
            output_lines.append(output_line)

        # 進捗表示
        progress = int(((line_cnt+1)/lines_len)*50)
        progress_per = "{:.1f}".format(((line_cnt+1)/lines_len)*100)
        print("\r{}%（{} / {}）  {}".format(progress_per, line_cnt+1, lines_len, "#"*progress), end="")

    # 書き込み
    output_file_name = "./output/"+os.path.basename(anki_file)
    if os.path.isfile(output_file_name):
        os.remove(output_file_name)
    with open(output_file_name, "x") as f:
        f.writelines(output_lines)

    # 出力見やすいように
    print("\n")


# 終了
driver.quit()
print("\n--- 処理が完了しました ---\n\n")
