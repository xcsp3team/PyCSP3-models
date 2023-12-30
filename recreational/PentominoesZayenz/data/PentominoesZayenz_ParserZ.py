from pycsp3.problems.data.parsing import *
import re

skip_empty_lines(or_prefixed_by="%")

data["size"] = number_in(line())
nTiles = number_in(next_line())
next_line()
tiles = [next_line()[3:-4] for _ in range(nTiles)]

tiles = [re.sub('\[.*?\]', 'A', tile) for tile in tiles]
tiles = [re.sub('\{1\}', '', tile) for tile in tiles]


def cut(subtile):
    j = 0
    cnt = 0
    while subtile[j] == 'A':
        if subtile[j + 1] == '*':
            assert cnt == 0
            break
        if subtile[j + 1] == ' ':
            cnt += 1
            j = j + 2
        elif subtile[j + 1] == '{':
            jj = j + 2 + subtile[j + 2:].index('}')
            cnt += int(subtile[j + 2:jj])
            j = jj + 2
        else:
            assert False
    return j, cnt


def reduce(tile):
    j = 0
    while j < len(tile):
        if tile[j] == 'A':
            length, cnt = cut(tile[j:])
            if cnt > 0:
                tile = tile[:j] + "A{" + str(cnt) + "} " + tile[j + length:]
        j += 1
    return tile


data['tiles'] = [reduce(tiles[i]) for i in range(nTiles)]
