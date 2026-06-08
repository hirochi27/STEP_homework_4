import sys
import collections
from collections import deque

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}


        #タイトルからIDを探すための辞書を作る
        self.title_to_id = {}


        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []

                self.title_to_id[title] = id

        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        
        path = []
        d = deque()
        visited = set() #一回訪れたところは、キューに追加しないようにするため、記録する

        print(self.links)
        print(self.titles)

        #与えられた単語のIDを探す
        #self.title_to_id :　タイトル → ID　の辞書
        start_ID = self.title_to_id[start]
        goal_ID = self.title_to_id[goal]

        visited.add(start_ID)
        

        #2番目のページをキューに入れる
        next_pages = self.links[start_ID]
        for page in next_pages:

            #キューに入れる前に、"visited"にIDを記録（繰り返し参照しないようにするため）
            if page not in visited:
                visited.add(page)

            #source：リンク元、target：リンク先
            page = {"source": None, "target": page}
            d.append(page)


        #3番目以降のページをキューに入れる処理
        #目的のページを見つけたらTeueにする
        flag = False 
        #popした値が目的の値だったらwhile文を抜ける
        #"キューから取り出した値にリンクされたページ"を新しくキューに入れる        
        while flag == False:
            now_page = d.popleft()   


            #取り出した値が目的のページだった場合、Trueに　→　whileを抜ける
            if now_page["target"] == goal_ID:
                print("complete")
                flag = True
                target = now_page
                continue


            #リンクされたページを更にキューに入れる
            next_pages = self.links[now_page["target"]] #next_page:今のページにリンクされてるページたち
            for page in next_pages:
                #既に処理をしていたらとばす
                if page in visited:
                    continue
                else:
                    visited.add(page)
                #キューに追加：sourceにリンク元のIDを入れることで後から経路を辿れるようにする
                page = {"source": now_page, "target": page}
                d.append(page)
    

        #pathをさかのぼる
        path.append(target["target"])
        source = target["source"]
        while source != None:
            #print("path!!!!!!!!!!")
            path.insert(0, source["target"])#pathをさかのぼってリストの最初に入れていく
            source = source["source"]
        

        path.insert(0, start_ID)
        print(f"path:{path}")


        wikipedia.assert_path(path, start, goal)

        #------------------------#
    


    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        #------------------------#
        # Write your code here!  #

        #重みづけ用
        #全てのノードに初期値1.0を割り振る(ページランク専用の辞書を作る)
        weight = {}
        for node in self.links:
            weight[node] = 1.0
            #print(weight)


        count = 0
        # while count <= 5:
        #各ノードの隣接ノードに、重みを均等に割り振る
        flag = False
        while flag == False:#重みに変化が無くなるまでループする

            count += 1
            print(count)
            if count % 10000 == 0:
                print("processed:", count, "queue:", len(d), flush=True)
                #print(f"count : {count}")

            #元の重みを保持:こっちから重みを計算
            prev_weight = weight.copy() 
            #新しく分配する重みを保持
            new_weight = {} 
            for node in self.links:
                new_weight[node] = 0


            #それぞれのノードが分配する重みを計算
            for node in weight:
                count_nodes = len(self.links[node])
                #print(count_nodes)
                if count_nodes == 0: #隣接ノードがない時
                    count_even_next = 0
                    count_even_all = prev_weight[node] / len(self.links)
                else:
                    count_even_next = prev_weight[node] / 100 * 85 / count_nodes
                    count_even_all = prev_weight[node] / 100 * 15 / len(self.links)


                #隣接ノードに85%を分配
                #ここドカ重い
                for next_node in self.links[node]:
                    new_weight[next_node] += count_even_next

                #全ノードに15%を分配 / 隣接ノードが無い場合は100%
                #ここもドカ重い
                for all_node in self.links:
                    new_weight[all_node] += count_even_all


            #新しい重みを辞書本体に適用
            weight = new_weight.copy()


            #古い重みと、現在の重みの差を計算
            #重みが変わらなくなったらwhile文を抜ける
            for page in weight:
                total = 0

                #print(weight[page])
                #print(prev_weight[page])

                diff = weight[page] - prev_weight[page]
                diff_ex = diff ** 2
                total += diff_ex
                #print(f"total:{total}")

            if total < 0.01:
                flag = True


            #count += 1

            #全体の重みが一定に保持されているかの判断
            weight_count = 0
            for node in weight:
                weight_count += weight[node]

            #print(weight_count)
            #print(len(self.links))
            assert abs(len(self.links) - weight_count) < 10 ** (-10)  #少しのズレは許容        
            #print(weight)
            #print(count_even_all)


        #重みが一番大きいページを探す
        max_weight_page = max(weight, key = weight.get)
        print(f"一番大きなページ！：{max_weight_page}")

        #------------------------#
        


    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])
        visited = {}
        for node in path:
            assert(node not in visited)
            visited[node] = True

        print("assert OK")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        #実行時コマンド
        #python3 graph.py wikipedia_dataset/wikipedia_dataset/pages_small.txt wikipedia_dataset/wikipedia_dataset/links_small.txt
        #python3 graph.py wikipedia_dataset/wikipedia_dataset/pages_medium.txt wikipedia_dataset/wikipedia_dataset/links_medium.txt
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    #wikipedia.find_longest_titles()
    # Example
    #wikipedia.find_most_linked_pages()


    # Homework #1
    #wikipedia.find_shortest_path('A', 'D')
    #wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    #wikipedia.find_longest_path("渋谷", "池袋")