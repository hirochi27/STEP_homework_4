# グラフアルゴリズム


## ファイルについて
* graph.py　メインのファイル
* wikiのデータの入ったフォルダは重すぎるのでgit ignoreしています

## 実行方法
```
python graph.py pages_small.txt links_small.txt
```
```
python graph.py pages_medium.txt links_medium.txt
```

## 現状
#### 宿題１
BFS（幅優先探索）を利用した最短経路の検索

```
def find_shortest_path
```
BFSのグラフ検索ができました！<br>
mediumのデータで動作したので大丈夫だと思います
#### 宿題２
ページランクの実装
```
def find_most_popular_pages
```
ページランクの分配はできるようになりました！<br>
* ランクが収束したかどうかの判断と、分配のループの実装ができていません
* ページランクの更新後「全部のノードのページランクの合計値」が一定になっているか確認したいのですが、”5.999999999999999
"と”6”とかで少しずつズレてしまいます。pythonの仕様かなと思うのですが何とかるでしょうか？
