import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

js_start = "// ── Riddle Game Engine ────────────────────────────────────────"
js_end = "// ── Scroll-driven frame sequence (canvas) ─────────────────────"

js_replacement = """// ── Crossword Game Engine ────────────────────────────────────────
    const crosswordLevels = [
      {
        level: 1,
        gridSize: 7,
        words: [
          { word: "STARK", row: 1, col: 1, dir: "H", clue: "The Kings of the North (GoT)" },
          { word: "SNOW", row: 1, col: 1, dir: "V", clue: "He knows nothing (GoT)" }
        ]
      },
      {
        level: 2,
        gridSize: 7,
        words: [
          { word: "CLOUD", row: 1, col: 3, dir: "V", clue: "Modern storage in the sky (Tech)" },
          { word: "CODE", row: 1, col: 3, dir: "H", clue: "The language of the web (Tech)" }
        ]
      },
      {
        level: 3,
        gridSize: 9,
        words: [
          { word: "LION", row: 2, col: 2, dir: "H", clue: "The symbol of strength on the flag (SL)" },
          { word: "LANKA", row: 2, col: 2, dir: "V", clue: "The pearl of the Indian Ocean (SL)" },
          { word: "DATA", row: 5, col: 2, dir: "H", clue: "The modern gold of the digital age (Tech)" }
        ]
      },
      {
        level: 4,
        gridSize: 11,
        words: [
          { word: "DRAGON", row: 3, col: 1, dir: "H", clue: "Fire-breathing beast of myth (GoT)" },
          { word: "BYTE", row: 3, col: 6, dir: "V", clue: "8 bits of information (Tech)" },
          { word: "COLOMBO", row: 1, col: 8, dir: "V", clue: "Commercial capital (SL)" },
          { word: "CODE", row: 6, col: 8, dir: "H", clue: "Developer's poetry (Tech)" }
        ]
      },
      {
        level: 5,
        gridSize: 15,
        words: [
          {"word": "TARGARYEN", "row": 10, "col": 5, "dir": "H", "clue": "Blood of old Valyria, riders of the sky (GoT)"}, 
          {"word": "SIGIRIYA", "row": 3, "col": 6, "dir": "V", "clue": "Ancient rock fortress, the Lion Rock (SL)"}, 
          {"word": "QUANTUM", "row": 7, "col": 13, "dir": "V", "clue": "Mechanics of uncertainty, future of computing (Tech)"}, 
          {"word": "NETWORK", "row": 7, "col": 1, "dir": "H", "clue": "Interconnected computers (Tech)"}, 
          {"word": "VALYRIA", "row": 7, "col": 11, "dir": "V", "clue": "The doom destroyed this ancient empire (GoT)"}, 
          {"word": "RAVANA", "row": 10, "col": 7, "dir": "V", "clue": "Legendary ancient king, master of ten directions (SL)"}, 
          {"word": "DRAGON", "row": 5, "col": 3, "dir": "H", "clue": "Balerion the Black Dread was one (GoT)"}, 
          {"word": "SERVER", "row": 3, "col": 6, "dir": "H", "clue": "Centralized host for applications (Tech)"}, 
          {"word": "THRONE", "row": 10, "col": 5, "dir": "V", "clue": "The seat of power forged by Balerion's fire (GoT)"}, 
          {"word": "LANKA", "row": 5, "col": 1, "dir": "V", "clue": "The Resplendent Island (SL)"}, 
          {"word": "CLOUD", "row": 1, "col": 3, "dir": "V", "clue": "Elastic remote computing resources (Tech)"}, 
          {"word": "BYTE", "row": 0, "col": 7, "dir": "V", "clue": "A basic unit of digital information (Tech)"}, 
          {"word": "IRON", "row": 14, "col": 2, "dir": "H", "clue": "Material of the most uncomfortable chair in Westeros (GoT)"}, 
          {"word": "VIJAYA", "row": 13, "col": 2, "dir": "V", "clue": "First recorded King of Sri Lanka (SL)"}
        ]
      }
    ];

    let currentLevelIndex = 0;
    let gridMap = {}; // 'r-c' -> { inputEl, answers: [], numbers: [] }
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
      gridWrap.style.gridTemplateColumns = `repeat(${size}, 34px)`;
      gridMap = {};
      
      // Calculate intersection matrix
      let layout = Array(size).fill(0).map(() => Array(size).fill(null));
      let wordStarts = {}; // 'r-c' -> number
      let clueNum = 1;
      
      // Sort words to find starting positions correctly
      let sortedWords = [...levelData.words].sort((a,b) => {
          if (a.row !== b.row) return a.row - b.row;
          return a.col - b.col;
      });

      // Assign numbers to starting cells
      sortedWords.forEach(w => {
          let key = `${w.row}-${w.col}`;
          if (!wordStarts[key]) {
              wordStarts[key] = clueNum++;
          }
          w.number = wordStarts[key];
      });

      // Map grid
      levelData.words.forEach(w => {
          for(let i=0; i<w.word.length; i++) {
              let r = w.dir === 'H' ? w.row : w.row + i;
              let c = w.dir === 'H' ? w.col + i : w.col;
              if (!layout[r][c]) layout[r][c] = { answers: [] };
              layout[r][c].answers.push({ char: w.word[i], wordIdx: levelData.words.indexOf(w), dir: w.dir });
          }
      });

      // Render Grid
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
                          // Toggle direction if clicked again
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

      // Render Clues
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
        // Prefer active direction, otherwise fallback
        let target = answers.find(a => a.dir === activeDirection);
        if (!target) {
            target = answers[0];
            activeDirection = target.dir;
        }
        return target;
    }

    function highlightActive(r, c) {
        // Clear all
        document.querySelectorAll('.cw-cell').forEach(el => el.classList.remove('active-word', 'active-cell'));
        document.querySelectorAll('.cw-clue-item').forEach(el => el.classList.remove('active'));
        
        let target = getActiveWordData(r, c);
        if (!target) return;
        
        let levelData = crosswordLevels[currentLevelIndex];
        let w = levelData.words[target.wordIdx];
        
        // Highlight clue
        let clueItems = document.querySelectorAll('.cw-clue-item');
        clueItems.forEach(item => {
            if (parseInt(item.dataset.idx) === target.wordIdx) {
                item.classList.add('active');
                item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        });
        
        // Highlight word cells
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

    function handleKey(e, r, c) {
        let target = getActiveWordData(r, c);
        if (!target) return;
        
        let levelData = crosswordLevels[currentLevelIndex];
        let w = levelData.words[target.wordIdx];
        
        if (e.key === 'Backspace' && e.target.value === '') {
            e.preventDefault();
            // Move backward
            let nextR = activeDirection === 'H' ? r : r - 1;
            let nextC = activeDirection === 'H' ? c - 1 : c;
            
            // Check if within bounds of the word
            let inBounds = false;
            if (activeDirection === 'H' && nextC >= w.col) inBounds = true;
            if (activeDirection === 'V' && nextR >= w.row) inBounds = true;
            
            if (inBounds && gridMap[`${nextR}-${nextC}`]) {
                gridMap[`${nextR}-${nextC}`].el.focus();
                gridMap[`${nextR}-${nextC}`].el.value = '';
            }
        } else if (e.key === 'ArrowRight') {
            activeDirection = 'H';
            if (gridMap[`${r}-${c+1}`]) gridMap[`${r}-${c+1}`].el.focus();
        } else if (e.key === 'ArrowLeft') {
            activeDirection = 'H';
            if (gridMap[`${r}-${c-1}`]) gridMap[`${r}-${c-1}`].el.focus();
        } else if (e.key === 'ArrowDown') {
            activeDirection = 'V';
            if (gridMap[`${r+1}-${c}`]) gridMap[`${r+1}-${c}`].el.focus();
        } else if (e.key === 'ArrowUp') {
            activeDirection = 'V';
            if (gridMap[`${r-1}-${c}`]) gridMap[`${r-1}-${c}`].el.focus();
        }
    }

    function handleInput(e, r, c) {
        e.target.value = e.target.value.toUpperCase();
        
        let target = getActiveWordData(r, c);
        if (!target || !e.target.value) return;
        
        let levelData = crosswordLevels[currentLevelIndex];
        let w = levelData.words[target.wordIdx];
        
        // Move forward
        let nextR = activeDirection === 'H' ? r : r + 1;
        let nextC = activeDirection === 'H' ? c + 1 : c;
        
        let inBounds = false;
        if (activeDirection === 'H' && nextC < w.col + w.word.length) inBounds = true;
        if (activeDirection === 'V' && nextR < w.row + w.word.length) inBounds = true;
        
        if (inBounds && gridMap[`${nextR}-${nextC}`]) {
            gridMap[`${nextR}-${nextC}`].el.focus();
        }
    }

    function checkCrossword() {
        const levelData = crosswordLevels[currentLevelIndex];
        let allCorrect = true;
        
        // Clear previous error states
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
            
            // Mark cells
            for(let i=0; i<w.word.length; i++) {
                let r = w.dir === 'H' ? w.row : w.row + i;
                let c = w.dir === 'H' ? w.col + i : w.col;
                if (!wordCorrect) {
                    if (gridMap[`${r}-${c}`].el.value) {
                         // Only mark error if they typed something
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
                    // VICTORY!
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

