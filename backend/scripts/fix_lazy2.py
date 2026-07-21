import os, re

files = []
for root, dirs, fnames in os.walk('app/modules'):
    for f in fnames:
        if f.endswith('_models.py'):
            files.append(os.path.join(root, f))

for fp in files:
    with open(fp, 'r', encoding='utf-8') as fh:
        content = fh.read()

    old = content

    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if 'back_populates=' in line and 'lazy=' not in line:
            line = line.replace(
                'back_populates=',
                'lazy="selectin", back_populates=',
            )
        new_lines.append(line)

    content = '\n'.join(new_lines)

    if content != old:
        with open(fp, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f'FIXED: {fp}')

print('DONE')
