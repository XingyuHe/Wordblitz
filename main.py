import threading
from collections import deque
import heapq

import twl
# import nltk
# from nltk.corpus import words
# nltk.download('words')

from threading import Thread
from time import sleep



def printGrid(grid, coords, word):
    print(f"==================={word}=====================")
    n = len(grid)
    for i in range(n):
        for j in range(n):
            if (i, j) in coords:
                print(coords.index((i, j)), end="")
            else:
                print(grid[i][j], end="")
        print()


def dfs(grid, coords, maxlen, foundCoords, foundWords,foundLock):
    n = len(grid)
    word = "".join([grid[i][j] for i, j in coords])
    # print(word)
    i, j = coords[-1]
    isValid = len(word) > 3 and twl.check(word)
    if isValid:
        # print(word)
        with foundLock:
            if word not in foundWords:
                # print(getRank(coords), coords)
                heapq.heappush(foundCoords, (getRank(coords), tuple(coords)))
                # foundCoords.append(tuple(coords))
                foundWords.add(word)

    if (len(coords) == maxlen):
        return


    for di in [-1, 0, 1]:
        ni = i+di
        if ni < 0 or ni >= n:
            continue
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            nj = j+dj
            if nj < 0 or nj >= n:
                continue
            if (ni, nj) in coords:
                continue
            coords.append((ni, nj))
            dfs(grid, coords, maxlen, foundCoords, foundWords,foundLock)
            coords.pop()

def gridSearch(grid, tgtmaxlen, foundCoords, foundWords, foundLock):
    n = len(grid)
    for i in range(n):
        for j in range(n):
            coords = [(i, j)]
            dfs(grid, coords, tgtmaxlen, foundCoords, foundWords, foundLock)

def read_words_freq(file_path="freq.txt"):
    try:
        with open(file_path, 'r') as file:
            word_list = file.read().splitlines()
        return {word_list[i] : i for i in range(len(word_list))}
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

word2freq = read_words_freq()
def getRank(coord):
    word = "".join([grid[i][j] for i, j in coord])
    if word in word2freq:
        return word2freq[word]
    else:
        return len(word2freq)


tgtmaxlen = 7
n = 4
grid = [list(input()) for _ in range(n)]
foundWords = set()
foundCoords = list()
foundLock = threading.Lock()
thread = Thread(target = gridSearch, args=(grid, tgtmaxlen, foundCoords, foundWords,foundLock))
thread.start()

while True:
    _ = input()
    with foundLock:
        if foundCoords:
            # foundCoords.sort(key=lambda coord: getRank(coord))
            item = heapq.heappop(foundCoords)
            # print(item)
            coord = item[-1]
            word = "".join([grid[i][j] for i, j in coord])
            printGrid(grid, coord, word)
        else:
            print("word not found")

thread.join()
