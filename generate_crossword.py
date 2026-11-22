import json
import random

def generate_crossword(words, grid_size=20):
    words = sorted(words, key=len, reverse=True)
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    placements = []
    
    def can_place(word, row, col, d):
        if d == 'H':
            if col + len(word) > grid_size: return False
            for i, char in enumerate(word):
                r, c = row, col + i
                if grid[r][c] not in (' ', char): return False
                if grid[r][c] == ' ':
                    if r > 0 and grid[r-1][c] != ' ': return False
                    if r < grid_size-1 and grid[r+1][c] != ' ': return False
                if i == 0 and c > 0 and grid[r][c-1] != ' ': return False
                if i == len(word)-1 and c < grid_size-1 and grid[r][c+1] != ' ': return False
        else:
            if row + len(word) > grid_size: return False
            for i, char in enumerate(word):
                r, c = row + i, col
                if grid[r][c] not in (' ', char): return False
                if grid[r][c] == ' ':
                    if c > 0 and grid[r][c-1] != ' ': return False
                    if c < grid_size-1 and grid[r][c+1] != ' ': return False
                if i == 0 and r > 0 and grid[r-1][c] != ' ': return False
                if i == len(word)-1 and r < grid_size-1 and grid[r+1][c] != ' ': return False
        return True

    def place_word(word, row, col, d):
        if d == 'H':
            for i, char in enumerate(word):
                grid[row][col + i] = char
        else:
            for i, char in enumerate(word):
                grid[row + i][col] = char
        placements.append({'word': word, 'row': row, 'col': col, 'dir': d})

    first = words[0]
    place_word(first, grid_size//2, (grid_size - len(first))//2, 'H')
    
    placed_words = [first]
    unplaced = words[1:]
    
    for _ in range(len(words)):
        for word in list(unplaced):
            placed = False
            for placed_w in placed_words:
                if placed: break
                for p_char in placed_w:
                    if placed: break
                    if p_char in word:
                        for i, char in enumerate(word):
                            if char == p_char:
                                p_info = next(p for p in placements if p['word'] == placed_w)
                                if p_info['dir'] == 'H':
                                    r = p_info['row'] - i
                                    c = p_info['col'] + placed_w.index(p_char)
                                    if r >= 0 and can_place(word, r, c, 'V'):
                                        place_word(word, r, c, 'V')
                                        placed_words.append(word)
                                        if word in unplaced: unplaced.remove(word)
                                        placed = True
                                        break
                                else:
                                    r = p_info['row'] + placed_w.index(p_char)
                                    c = p_info['col'] - i
                                    if c >= 0 and can_place(word, r, c, 'H'):
                                        place_word(word, r, c, 'H')
                                        placed_words.append(word)
                                        if word in unplaced: unplaced.remove(word)
                                        placed = True
                                        break
            
    return placements, grid

level5_words = [
    "TARGARYEN", "SIGIRIYA", "QUANTUM", "RAVANA", "DRAGON",
    "NETWORK", "LANKA", "BYTE", "VALYRIA", "VIJAYA",
    "SERVER", "THRONE", "CLOUD", "KANDY", "IRON", "CODE"
]

placements, grid = generate_crossword(level5_words, 20)
print("Level 5 Words Placed:", len(placements), "/", len(level5_words))
for r in grid:
    print(' '.join(c if c != ' ' else '.' for c in r))

print(json.dumps(placements))
