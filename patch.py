import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace CSS
css_start = "/* ─── The Iron Throne Trials Game CSS ────────────────────────── */"
css_end = "/* Victory view */"

css_replacement = """/* ─── The Crossword Game CSS ────────────────────────── */
    .crossword-container {
      display: flex;
      flex-direction: column;
      gap: 2rem;
      max-width: 1080px;
      margin: 0 auto;
      width: 100%;
    }
    
    .crossword-card {
      padding: 2.5rem;
      display: flex;
      flex-direction: column;
    }
    
    .cw-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2rem;
      gap: 1rem;
    }
    
    .cw-level {
      font-family: 'Cinzel', serif;
      font-weight: 700;
      color: var(--accent-soft);
      font-size: 1rem;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }
    
    .cw-progress-bar {
      flex: 1;
      height: 8px;
      background: rgba(255,255,255,0.06);
      border-radius: 10px;
      overflow: hidden;
      margin: 0 1.5rem;
      border: 1px solid rgba(206,176,138,0.15);
    }
    
    .cw-progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #b48e63, #f6e8cd);
      border-radius: 10px;
      width: 20%;
      transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .cw-layout {
      display: grid;
      grid-template-columns: 1fr 300px;
      gap: 2.5rem;
    }
    
    @media (max-width: 900px) {
      .cw-layout { grid-template-columns: 1fr; }
    }
    
    .cw-grid-wrap {
      display: flex;
      justify-content: center;
      align-items: center;
      background: rgba(13,11,9,0.5);
      padding: 1.5rem;
      border-radius: 12px;
      border: 1px solid rgba(206,176,138,0.1);
      overflow: auto;
    }
    
    .cw-grid {
      display: grid;
      gap: 2px;
      background: #000;
      border: 2px solid #000;
      touch-action: none;
    }
    
    .cw-cell {
      width: 34px;
      height: 34px;
      background: #0d0b09;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .cw-cell.input-cell {
      background: #fff;
    }
    .cw-cell.input-cell.active-word {
      background: #f6e8cd;
    }
    .cw-cell.input-cell.active-cell {
      background: #ffd699;
    }
    .cw-cell.input-cell.correct {
      background: #b6f3c5;
    }
    .cw-cell.input-cell.error {
      background: #f3b6b6;
    }
    
    .cw-cell input {
      width: 100%;
      height: 100%;
      border: none;
      background: transparent;
      text-align: center;
      font-size: 1.2rem;
      font-weight: 700;
      text-transform: uppercase;
      color: #000;
      padding: 0;
      outline: none;
      font-family: 'Inter', sans-serif;
      caret-color: transparent;
      cursor: pointer;
    }
    
    .cw-number {
      position: absolute;
      top: 1px;
      left: 2px;
      font-size: 0.6rem;
      font-weight: 600;
      color: #333;
      pointer-events: none;
      line-height: 1;
    }
    
    .cw-clues-wrap {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
      max-height: 500px;
      overflow-y: auto;
      padding-right: 0.5rem;
    }
    
    .cw-clues-wrap::-webkit-scrollbar {
      width: 4px;
    }
    .cw-clues-wrap::-webkit-scrollbar-thumb {
      background: rgba(206,176,138,0.3);
      border-radius: 4px;
    }
    
    .cw-clues-section h4 {
      font-family: 'Cinzel', serif;
      font-size: 1.1rem;
      color: var(--accent);
      margin-bottom: 0.8rem;
      letter-spacing: 0.05em;
      border-bottom: 1px solid rgba(206,176,138,0.2);
      padding-bottom: 0.3rem;
    }
    
    .cw-clues-section ul {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }
    
    .cw-clue-item {
      font-size: 0.82rem;
      color: var(--text-2);
      line-height: 1.4;
      cursor: pointer;
      padding: 0.4rem 0.6rem;
      border-radius: 4px;
      transition: all 0.2s;
      display: flex;
      gap: 0.5rem;
    }
    
    .cw-clue-item:hover {
      background: rgba(255,255,255,0.05);
      color: var(--text-1);
    }
    
    .cw-clue-item.active {
      background: rgba(206,176,138,0.15);
      color: var(--accent-soft);
      border-left: 2px solid var(--accent);
    }
    
    .cw-clue-num {
      font-weight: 700;
      color: var(--accent);
      min-width: 1.2rem;
    }
    
    .cw-footer {
      margin-top: 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid rgba(255,255,255,0.08);
      padding-top: 1.5rem;
    }
    
    .game-feedback {
      font-size: 0.82rem;
      font-weight: 600;
      min-height: 20px;
      transition: color 0.25s;
      letter-spacing: 0.02em;
    }
    .game-feedback.success { color: #7ed89b; }
    .game-feedback.error { color: #d87e7e; }

    """
idx1 = content.find(css_start)
idx2 = content.find(css_end)
if idx1 != -1 and idx2 != -1:
    content = content[:idx1] + css_replacement + content[idx2:]

# Replace HTML
html_start = "<!-- ░░ Game Section: The Royal Cipher ░░ -->"
html_end = "<!-- ░░ Outro ░░ -->"

html_replacement = """<!-- ░░ Game Section: Crossword Puzzle ░░ -->
      <section id="games" class="content-section">
        <p class="section-eyebrow reveal">Empire Secrets &bull; 5 Trials</p>
        <h2 class="section-title reveal reveal-d1">The Grand Cipher</h2>
        <p class="section-sub reveal reveal-d2">
          Solve the interconnected web of Game of Thrones, Sri Lankan History, and Modern Technology. Complete Level 5 to win a Free Ticket.
        </p>

        <div class="crossword-container reveal reveal-d2">
          <div class="glass-card crossword-card" id="crossword-card">
            
            <div id="cw-game-area">
                <div class="cw-header">
                  <div class="cw-level" id="cw-level-indicator">Level 1 / 5</div>
                  <div class="cw-progress-bar">
                    <div class="cw-progress-fill" id="cw-progress-fill" style="width: 20%;"></div>
                  </div>
                </div>

                <div class="cw-layout">
                  <!-- Grid Side -->
                  <div class="cw-grid-wrap">
                    <div id="cw-grid" class="cw-grid"></div>
                  </div>
                  
                  <!-- Clues Side -->
                  <div class="cw-clues-wrap">
                    <div class="cw-clues-section">
                      <h4>Across</h4>
                      <ul id="cw-clues-across"></ul>
                    </div>
                    <div class="cw-clues-section">
                      <h4>Down</h4>
                      <ul id="cw-clues-down"></ul>
                    </div>
                  </div>
                </div>
                
                <div class="cw-footer">
                  <button class="buy-btn" id="btn-check-crossword">Check Answers</button>
                  <div id="cw-feedback" class="game-feedback"></div>
                </div>
            </div>

            <!-- Victory Screen -->
            <div class="victory-container" id="victory-container" style="display: none;">
              <div class="victory-crown">👑</div>
              <h3 class="victory-title">Empire Unlocked</h3>
              <p class="victory-desc">You have conquered the impossible crossword trial. Your reward awaits.</p>
              <button class="buy-btn" id="btn-claim-ticket" style="margin-top: 1rem; box-shadow: 0 0 20px var(--accent);">Claim Free Ticket</button>
            </div>

          </div>
        </div>
      </section>

      """
idx1 = content.find(html_start)
idx2 = content.find(html_end)
if idx1 != -1 and idx2 != -1:
    content = content[:idx1] + html_replacement + content[idx2:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
