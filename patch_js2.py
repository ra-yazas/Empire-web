with open('h:/Empire web/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'gridWrap.style.gridTemplateColumns = `repeat(${size}, 42px)`;',
    'gridWrap.style.gridTemplateColumns = `repeat(${size}, min(42px, calc((100vw - 4rem) / ${size})))`;'
)

with open('h:/Empire web/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
