import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update CSS for bigger cells
css_start = ".cw-cell {"
css_end = "position: relative;"
css_replacement = """.cw-cell {
      width: 44px;
      height: 44px;
      background: #0d0b09;
      position: relative;"""
idx1 = content.find(css_start)
idx2 = content.find(css_end)
if idx1 != -1 and idx2 != -1:
    content = content[:idx1] + css_replacement + content[idx2+len(css_end):]

css_input_start = ".cw-cell input {"
css_input_end = "font-weight: 700;"
css_input_replacement = """.cw-cell input {
      width: 100%;
      height: 100%;
      border: none;
      background: transparent;
      text-align: center;
      font-size: 1.5rem;
      font-weight: 700;"""
idx1 = content.find(css_input_start)
idx2 = content.find(css_input_end)
if idx1 != -1 and idx2 != -1:
    content = content[:idx1] + css_input_replacement + content[idx2+len(css_input_end):]

css_num_start = ".cw-number {"
css_num_end = "font-weight: 600;"
css_num_replacement = """.cw-number {
      position: absolute;
      top: 2px;
      left: 3px;
      font-size: 0.75rem;
      font-weight: 600;"""
idx1 = content.find(css_num_start)
idx2 = content.find(css_num_end)
if idx1 != -1 and idx2 != -1:
    content = content[:idx1] + css_num_replacement + content[idx2+len(css_num_end):]


js_start = "// ── Crossword Game Engine ────────────────────────────────────────"
js_end = "// ── Scroll-driven frame sequence (canvas) ─────────────────────"

js_replacement = """// ── Crossword Game Engine ────────────────────────────────────────
    const crosswordLevels = [
      {
        level: 1,
        gridSize: 7,
        words: [
          { word: "STARK", row: 1, col: 1, dir: "H", clue: "[Game of Thrones] The Kings of the North" },
          { word: "SNOW", row: 1, col: 1, dir: "V", clue: "[Game of Thrones] Who tells you know nothing Jon Snow?" }
        ]
      },
      {
        level: 2,
        gridSize: 7,
        words: [
          { word: "CLOUD", row: 1, col: 3, dir: "V", clue: "[Tech] Modern storage in the sky" },
          { word: "CODE", row: 1, col: 3, dir: "H", clue: "[Tech] The language of the web" }
        ]
      },
      {
        level: 3,
        gridSize: 9,
        words: [
          { word: "LION", row: 2, col: 2, dir: "H", clue: "[SL History] The symbol of strength on the flag" },
          { word: "LANKA", row: 2, col: 2, dir: "V", clue: "[SL History] The pearl of the Indian Ocean" },
          { word: "DATA", row: 5, col: 2, dir: "H", clue: "[Tech] The modern gold of the digital age" }
        ]
      },
      {
        level: 4,
        gridSize: 11,
        words: [
          { word: "DRAGON", row: 3, col: 1, dir: "H", clue: "[Game of Thrones] Fire-breathing beast of myth" },
          { word: "BYTE", row: 3, col: 6, dir: "V", clue: "[Tech] 8 bits of information" },
          { word: "COLOMBO", row: 1, col: 8, dir: "V", clue: "[SL History] Commercial capital" },
          { word: "CODE", row: 6, col: 8, dir: "H", clue: "[Tech] Developer's poetry" }
        ]
      },
      {
        level: 5,
        gridSize: 15,
        words: [
          {"word": "TARGARYEN", "row": 10, "col": 5, "dir": "H", "clue": "[Game of Thrones] Blood of old Valyria, riders of the sky"}, 
          {"word": "SIGIRIYA", "row": 3, "col": 6, "dir": "V", "clue": "[SL History] Ancient rock fortress, the Lion Rock"}, 
          {"word": "QUANTUM", "row": 7, "col": 13, "dir": "V", "clue": "[Tech] Mechanics of uncertainty, future of computing"}, 
          {"word": "NETWORK", "row": 7, "col": 1, "dir": "H", "clue": "[Tech] Interconnected computers"}, 
          {"word": "VALYRIA", "row": 7, "col": 11, "dir": "V", "clue": "[Game of Thrones] The doom destroyed this ancient empire"}, 
          {"word": "RAVANA", "row": 10, "col": 7, "dir": "V", "clue": "[SL History] Legendary ancient king, master of ten directions"}, 
          {"word": "DRAGON", "row": 5, "col": 3, "dir": "H", "clue": "[Game of Thrones] Balerion the Black Dread was one"}, 
          {"word": "SERVER", "row": 3, "col": 6, "dir": "H", "clue": "[Tech] Centralized host for applications"}, 
          {"word": "THRONE", "row": 10, "col": 5, "dir": "V", "clue": "[Game of Thrones] The seat of power forged by Balerion's fire"}, 
          {"word": "LANKA", "row": 5, "col": 1, "dir": "V", "clue": "[SL History] The Resplendent Island"}, 
          {"word": "CLOUD", "row": 1, "col": 3, "dir": "V", "clue": "[Tech] Elastic remote computing resources"}, 
          {"word": "BYTE", "row": 0, "col": 7, "dir": "V", "clue": "[Tech] A basic unit of digital information"}, 
          {"word": "IRON", "row": 14, "col": 2, "dir": "H", "clue": "[Game of Thrones] Material of the most uncomfortable chair in Westeros"}, 
          {"word": "VIJAYA", "row": 13, "col": 2, "dir": "V", "clue": "[SL History] First recorded King of Sri Lanka"}
        ]
      }
    ];

    let currentLevelIndex = 0;
    let gridMap = {}; // 'r-c' -> { el, cell, data }
    let activeDirection = 'H';
    let currentCell = null; // 'r-c'

    function initCrosswordLevel() {
      const levelData = crosswordLevels[currentLevelIndex];
      const gridWrap = document.getElementById('cw-grid');
      const cluesAcross = document.getElementById('cw-clues-across');
      const cluesDown = document.getElementById('cw-clues-down');
      const levelInd = document.getElementById('cw-level-indicator');
      const progFill = document.getElementById('cw-progress-fill');
      const feedback = document.getElementById('cw-feedback');
      
      gridWrap.innerHTML = '';
      cluesAcross.innerHTML = '';
      cluesDown.innerHTML = '';
      feedback.textContent = '';
      feedback.className = 'game-feedback';
      
      levelInd.textContent = `Level ${currentLevelIndex + 1} / 5`;
      progFill.style.width = `${((currentLevelIndex + 1) / 5) * 100}%`;
      
      const size = levelData.gridSize;
      gridWrap.style.gridTemplateColumns = `repeat(${size}, 44px)`;
      gridMap = {};
      
      let layout = Array(size).fill(0).map(() => Array(size).fill(null));
      let wordStarts = {};
      let clueNum = 1;
      
      let sortedWords = [...levelData.words].sort((a,b) => {
          if (a.row !== b.row) return a.row - b.row;
          return a.col - b.col;
      });

      sortedWords.forEach(w => {
          let key = `${w.row}-${w.col}`;
          if (!wordStarts[key]) {
              wordStarts[key] = clueNum++;
          }
          w.number = wordStarts[key];
      });

      levelData.words.forEach(w => {
          for(let i=0; i<w.word.length; i++) {
              let r = w.dir === 'H' ? w.row : w.row + i;
              let c = w.dir === 'H' ? w.col + i : w.col;
              if (!layout[r][c]) layout[r][c] = { answers: [] };
              layout[r][c].answers.push({ char: w.word[i], wordIdx: levelData.words.indexOf(w), dir: w.dir });
          }
      });

      for(let r=0; r<size; r++) {
          for(let c=0; c<size; c++) {
              let cell = document.createElement('div');
              cell.className = 'cw-cell';
              
              if (layout[r][c]) {
                  cell.classList.add('input-cell');
                  
                  let key = `${r}-${c}`;
                  if (wordStarts[key]) {
                      let numSpan = document.createElement('span');
                      numSpan.className = 'cw-number';
                      numSpan.textContent = wordStarts[key];
                      cell.appendChild(numSpan);
                  }
                  
                  let input = document.createElement('input');
                  input.maxLength = 1;
                  input.dataset.r = r;
                  input.dataset.c = c;
                  
                  input.addEventListener('focus', () => {
                      currentCell = `${r}-${c}`;
                      highlightActive(r, c);
                  });
                  
                  input.addEventListener('keydown', (e) => handleKey(e, r, c));
                  input.addEventListener('input', (e) => handleInput(e, r, c));
                  input.addEventListener('click', () => {
                      if (currentCell === `${r}-${c}`) {
                          activeDirection = activeDirection === 'H' ? 'V' : 'H';
                          highlightActive(r, c);
                      }
                  });
                  
                  cell.appendChild(input);
                  gridMap[`${r}-${c}`] = { el: input, cell: cell, data: layout[r][c].answers };
              } else {
                  cell.classList.add('empty');
              }
              gridWrap.appendChild(cell);
          }
      }

      levelData.words.forEach((w, i) => {
          let li = document.createElement('li');
          li.className = 'cw-clue-item';
          li.innerHTML = `<span class="cw-clue-num">${w.number}.</span> <span class="cw-clue-text">${w.clue}</span>`;
          li.dataset.idx = i;
          li.addEventListener('click', () => {
              activeDirection = w.dir;
              let firstInput = gridMap[`${w.row}-${w.col}`].el;
              firstInput.focus();
          });
          
          if (w.dir === 'H') cluesAcross.appendChild(li);
          else cluesDown.appendChild(li);
      });
    }

    function getActiveWordData(r, c) {
        if(!gridMap[`${r}-${c}`]) return null;
        let answers = gridMap[`${r}-${c}`].data;
        let target = answers.find(a => a.dir === activeDirection);
        if (!target) {
            target = answers[0];
            activeDirection = target.dir;
        }
        return target;
    }

    function highlightActive(r, c) {
        document.querySelectorAll('.cw-cell').forEach(el => el.classList.remove('active-word', 'active-cell'));
        document.querySelectorAll('.cw-clue-item').forEach(el => el.classList.remove('active'));
        
        let target = getActiveWordData(r, c);
        if (!target) return;
        
        let levelData = crosswordLevels[currentLevelIndex];
        let w = levelData.words[target.wordIdx];
        
        let clueItems = document.querySelectorAll('.cw-clue-item');
        clueItems.forEach(item => {
            if (parseInt(item.dataset.idx) === target.wordIdx) {
                item.classList.add('active');
                item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        });
        
        for(let i=0; i<w.word.length; i++) {
            let tr = w.dir === 'H' ? w.row : w.row + i;
            let tc = w.dir === 'H' ? w.col + i : w.col;
            if (tr === r && tc === c) {
                gridMap[`${tr}-${tc}`].cell.classList.add('active-cell');
            } else {
                gridMap[`${tr}-${tc}`].cell.classList.add('active-word');
            }
        }
    }

    function getNextCell(r, c, d) {
        let nr = d === 'H' ? r : r + 1;
        let nc = d === 'H' ? c + 1 : c;
        let target = getActiveWordData(r, c);
        if(!target) return null;
        let w = crosswordLevels[currentLevelIndex].words[target.wordIdx];
        if (d === 'H' && nc < w.col + w.word.length) return {r: nr, c: nc};
        if (d === 'V' && nr < w.row + w.word.length) return {r: nr, c: nc};
        return null;
    }

    function getPrevCell(r, c, d) {
        let nr = d === 'H' ? r : r - 1;
        let nc = d === 'H' ? c - 1 : c;
        let target = getActiveWordData(r, c);
        if(!target) return null;
        let w = crosswordLevels[currentLevelIndex].words[target.wordIdx];
        if (d === 'H' && nc >= w.col) return {r: nr, c: nc};
        if (d === 'V' && nr >= w.row) return {r: nr, c: nc};
        return null;
    }

    function handleKey(e, r, c) {
        if (e.key === 'Backspace') {
            let val = e.target.value;
            // If empty, immediately jump back and delete
            if (!val) {
                e.preventDefault();
                let prev = getPrevCell(r, c, activeDirection);
                if (prev && gridMap[`${prev.r}-${prev.c}`]) {
                    gridMap[`${prev.r}-${prev.c}`].el.focus();
                    gridMap[`${prev.r}-${prev.c}`].el.value = '';
                }
            }
            // If not empty, it will naturally delete the char because we didn't preventDefault.
            // On input event, it will handle it if needed.
        } else if (e.key === 'ArrowRight') {
            activeDirection = 'H';
            if (gridMap[`${r}-${c+1}`]) { e.preventDefault(); gridMap[`${r}-${c+1}`].el.focus(); }
        } else if (e.key === 'ArrowLeft') {
            activeDirection = 'H';
            if (gridMap[`${r}-${c-1}`]) { e.preventDefault(); gridMap[`${r}-${c-1}`].el.focus(); }
        } else if (e.key === 'ArrowDown') {
            activeDirection = 'V';
            if (gridMap[`${r+1}-${c}`]) { e.preventDefault(); gridMap[`${r+1}-${c}`].el.focus(); }
        } else if (e.key === 'ArrowUp') {
            activeDirection = 'V';
            if (gridMap[`${r-1}-${c}`]) { e.preventDefault(); gridMap[`${r-1}-${c}`].el.focus(); }
        }
    }

    function handleInput(e, r, c) {
        let val = e.target.value.toUpperCase();
        e.target.value = val;
        
        // Only jump to next if a character was actually typed (avoids jumping on non-character keys on some browsers)
        if (val.length === 1 && val.match(/[A-Z]/)) {
            let next = getNextCell(r, c, activeDirection);
            if (next && gridMap[`${next.r}-${next.c}`]) {
                gridMap[`${next.r}-${next.c}`].el.focus();
                gridMap[`${next.r}-${next.c}`].el.select();
            }
        } else if (val.length > 1) {
             // Handle fast typing / paste
             e.target.value = val[val.length-1];
             let next = getNextCell(r, c, activeDirection);
             if (next && gridMap[`${next.r}-${next.c}`]) {
                 gridMap[`${next.r}-${next.c}`].el.focus();
                 gridMap[`${next.r}-${next.c}`].el.select();
             }
        } else if (!val.match(/[A-Z]/)) {
             e.target.value = ''; // Disallow non-letters
        }
    }

    function checkCrossword() {
        const levelData = crosswordLevels[currentLevelIndex];
        let allCorrect = true;
        
        Object.values(gridMap).forEach(g => {
            g.cell.classList.remove('error', 'correct');
        });
        
        levelData.words.forEach(w => {
            let wordCorrect = true;
            for(let i=0; i<w.word.length; i++) {
                let r = w.dir === 'H' ? w.row : w.row + i;
                let c = w.dir === 'H' ? w.col + i : w.col;
                if (gridMap[`${r}-${c}`].el.value.toUpperCase() !== w.word[i]) {
                    wordCorrect = false;
                    allCorrect = false;
                }
            }
            
            for(let i=0; i<w.word.length; i++) {
                let r = w.dir === 'H' ? w.row : w.row + i;
                let c = w.dir === 'H' ? w.col + i : w.col;
                if (!wordCorrect) {
                    if (gridMap[`${r}-${c}`].el.value) {
                         gridMap[`${r}-${c}`].cell.classList.add('error');
                    }
                } else {
                    gridMap[`${r}-${c}`].cell.classList.add('correct');
                }
            }
        });
        
        const feedback = document.getElementById('cw-feedback');
        
        if (allCorrect) {
            feedback.textContent = 'Correct! Advancing...';
            feedback.className = 'game-feedback success';
            setTimeout(() => {
                currentLevelIndex++;
                if (currentLevelIndex < crosswordLevels.length) {
                    initCrosswordLevel();
                } else {
                    document.getElementById('cw-game-area').style.display = 'none';
                    document.getElementById('victory-container').style.display = 'flex';
                }
            }, 1000);
        } else {
            feedback.textContent = 'Some answers are incorrect or incomplete.';
            feedback.className = 'game-feedback error';
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        let checkBtn = document.getElementById('btn-check-crossword');
        if (checkBtn) {
            checkBtn.addEventListener('click', checkCrossword);
        }
        
        let claimBtn = document.getElementById('btn-claim-ticket');
        if (claimBtn) {
            claimBtn.addEventListener('click', () => {
                document.getElementById('input-attendee-name').value = "Crossword Champion";
                document.getElementById('input-attendee-name').scrollIntoView({behavior: 'smooth', block: 'center'});
                document.getElementById('btn-print-ticket').click();
            });
        }

        initCrosswordLevel();
    });

    """

idx1 = content.find(js_start)
idx2 = content.find(js_end)
if idx1 != -1 and idx2 != -1:
    content = content[:idx1] + js_replacement + content[idx2:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
