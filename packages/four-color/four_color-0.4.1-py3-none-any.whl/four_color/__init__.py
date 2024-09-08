import typing
from itertools import product

from PIL import Image, ImageDraw

if typing.TYPE_CHECKING:
    import networkx as nx

# see pyproject.toml
__version__ = "0.4.0"
__author__ = "Saito Tsutomu <tsutomu7@hotmail.co.jp>"


def load_image(src: str, times: int = 1) -> Image.Image:
    """画像ファイルの読込み"""
    from collections import Counter
    from random import seed, shuffle
    from urllib.request import urlopen

    with urlopen(src) if src.startswith("http") else open(src, "rb") as fd:
        im = Image.open(fd).convert("RGB")
    # 代表色(最も使用頻度の多い色)を抽出
    cc = sorted([(v, k) for k, v in Counter(im.getdata()).items()])[-1][1]
    # RGB=(0,1,?)の色をなくす
    for y, x in product(range(im.height), range(im.width)):
        r, g, b = im.getpixel((x, y))[:3]
        if (r, g) == (0, 1):
            im.putpixel(0, 0, b)
    # 代表色のエリアをRGB=(0,1,通し番号)で塗りつぶす
    n = 0
    for y, x in product(range(im.height), range(im.width)):
        if im.getpixel((x, y)) != cc:
            continue
        ImageDraw.floodfill(im, (x, y), (0, 1, n))
        n += 1
    # 境界を少し広げる
    seed(1)
    dd = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    for _ in range(times):
        lst = list(product(range(1, im.height - 1), range(1, im.width - 1)))
        shuffle(lst)
        for y, x in lst:
            c = im.getpixel((x, y))
            if c[:2] == (0, 1):
                for i, j in dd:
                    if im.getpixel((x + i, y + j))[:2] != (0, 1):
                        im.putpixel((x + i, y + j), c)
    return im


def make_graph(im: Image.Image):
    """グラフ作成"""
    import networkx as nx

    g = nx.Graph()
    for y, x in product(range(im.height - 1), range(im.width - 1)):
        c1 = im.getpixel((x, y))
        if c1[:2] != (0, 1):
            continue
        c2 = im.getpixel((x + 1, y))
        c3 = im.getpixel((x, y + 1))
        if c2[:2] == (0, 1) and c1[2] != c2[2]:
            g.add_edge(c1[2], c2[2])
        if c3[:2] == (0, 1) and c1[2] != c3[2]:
            g.add_edge(c1[2], c3[2])
    return g


def solve_four_color(g: "nx.Graph"):
    """4色問題を解く"""
    from pulp import LpBinary, LpProblem, LpVariable, lpDot, lpSum, value

    r4 = range(4)
    m = LpProblem()  # 数理モデル
    # エリアiを色jにするかどうか
    v = {i: [LpVariable(f"v{i}_{j}", cat=LpBinary) for j in r4] for i in g.nodes()}
    for i in g.nodes():
        m += lpSum(v[i]) == 1
    for i, j in g.edges():
        for k in r4:
            m += v[i][k] + v[j][k] <= 1
    m.solve()
    return {k: int(value(lpDot(r4, w))) for k, w in v.items()}  # 結果


def write_four_color(im: Image.Image, g: "nx.Graph"):
    result = solve_four_color(g)
    co = [(97, 132, 219), (228, 128, 109), (255, 241, 164), (121, 201, 164)]  # 4色
    for y, x in product(range(im.height - 1), range(im.width - 1)):
        c = im.getpixel((x, y))
        if c[:2] == (0, 1) and c[2] in result:  # エリアならば、結果で塗る
            ImageDraw.floodfill(im, (x, y), co[result[c[2]]])
