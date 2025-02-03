# このプログラムについて
[Anki](https://apps.ankiweb.net)の単語ファイルに画像を追加するやつです
Pythonとseleniumの導入説明は検索してください...（そのうち書くかも）

# 動作確認済み環境
- macOS Sequoia 15.1
- Python 3.11.4
- selenium 4.15.2

# 使い方
<!--
## 1. Python導入
ターミナルで
```
python -V
```
を実行して
が表示されなかったら飛ばしてください

## 2. selenium導入
飛ばしてください
-->

## 実行準備
1. [github](https://github.com/udonhazinsei/anki)開いて緑色の「Code」ボタンを押して一番下の「Download Zip」を押す
1. ダウンロードしたzipファイルを解凍
1. 解凍してできた「anki-main」フォルダをデスクトップに移動
1. 「anki-main」フォルダの中にankiでエクスポートしたファイルいれる

## 実行
ターミナルで
```
cd desktop/anki-main
```
```
python main.py
```
を順に実行<br>
処理が終わったら（「--- 処理が完了しました ---」がターミナルに表示されたら）「anki-main」フォルダの中の「output」フォルダの中に処理が終わったファイルが生成されてるからそれをankiにインポートしておわり

### コマンドライン引数について
```python main.py```のあとに引数を指定できます（全部オプション）<br>
例：
```
python main.py --show -s 500x500 -d /Users/*/Desktop -c 2 -p abc -r 0.5
```
- ```--show```：この引数が存在する場合、自動操作中のChromeのウィンドウを表示する（見てると楽しいかも？）
- ```-s 500x500```：画像のサイズを横×縦で指定（「x（小文字のエックス）」で区切ってください） 大きくすると含まれる画像の数が増える この例の場合だと500×500の範囲の画像になる
- ```-d /Users/*/Desktop/test```：画像ファイルを出力するディレクトリを指定（ワイルドカードが使えます） この例の場合だとデスクトップ上にある「test」という名前のフォルダに格納される
- ```-c 2```：画像検索する文字列をどの列から取るか（1か2で指定） この例だと2列目（解答側）の文字列で画像検索する
- ```-p abc```：この例の場合だと生成される画像ファイルの名前が「abc--検索したワード-UUID.png」になる
- ```-r 0.5```：画像の拡大率 ```-s```で画像サイズを大きくするとAnki上でも大きく表示されてしまうのでここで倍率を指定 この例の場合だと指定しないときの半分のサイズで表示される

# 参考サイトなど
- https://github.com/t9md/bulk-screen-capture
