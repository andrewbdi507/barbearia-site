import os, re

files = []
for root, dirs, fnames in os.walk('app/modules'):
    for f in fnames:
        if f.endswith('_models.py'):
            files.append(os.path.join(root, f))

count = 0
for fp in files:
    with open(fp, 'r', encoding='utf-8') as fh:
        content = fh.read()

    old = content

    # Fix relationships without explicit lazy parameter
    # Pattern 1: relationship("Model", back_populates="field")
    content = re.sub(
        r'relationship\(\s*"([^"]+)"\s*,\s*back_populates\s*=\s*"([^"]+)"\s*\)',
        r'relationship("\1", back_populates="\2", lazy="selectin")',
        content,
    )

    # Pattern 2: relationship("Model", back_populates="field", foreign_keys=...)
    content = re.sub(
        r'relationship\(\s*"([^"]+)"\s*,\s*back_populates\s*=\s*"([^"]+)"\s*,\s*foreign_keys\s*=',
        r'relationship("\1", back_populates="\2", lazy="selectin", foreign_keys=',
        content,
    )

    # Pattern 3: relationship("Model", back_populates="field", uselist=False)
    content = re.sub(
        r'relationship\(\s*"([^"]+)"\s*,\s*back_populates\s*=\s*"([^"]+)"\s*,\s*uselist\s*=\s*False\s*\)',
        r'relationship("\1", back_populates="\2", lazy="selectin", uselist=False)',
        content,
    )

    if content != old:
        with open(fp, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f'FIXED: {fp}')
        count += 1

print(f'DONE - {count} files fixed')
