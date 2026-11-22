with open('h:/Empire web/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

old_css = r'''    /\* Mobile compatibility fixes for Crossword and Ticket overflowing \*/
    @media \(max-width: 1024px\) \{
      \.ticket-wrapper,
      \.cw-grid-wrap \{
        justify-content: flex-start !important;
      \}
      \.ticket-card-horizontal,
      \.cw-grid \{
        margin: 0 auto !important;
      \}
    \}'''

new_css = '''    /* Mobile compatibility fixes for Crossword and Ticket overflowing */
    @media (max-width: 1024px) {
      .ticket-wrapper,
      .cw-grid-wrap {
        justify-content: center !important;
      }
      .ticket-card-horizontal {
        transform: scale(calc((100vw - 2.8rem) / 820));
        transform-origin: top center;
        margin-bottom: calc(-380px * (1 - ((100vw - 2.8rem) / 820))) !important;
      }
      .cw-grid {
        margin: 0 auto !important;
      }
      .cw-cell {
        width: 100% !important;
        height: auto !important;
        aspect-ratio: 1 / 1;
      }
      .cw-cell input {
        font-size: clamp(0.6rem, 3vw, 1.35rem) !important;
      }
    }'''

content = re.sub(old_css, new_css, content)

with open('h:/Empire web/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
