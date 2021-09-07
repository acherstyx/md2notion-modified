import re
import itertools


def replace_html_img_tag(file_path):
    with open(file_path, "r", encoding="UTF-8") as f:
        content = f.read()

    reg = '<img.*?src="(.*?\.(jpg|png))".*?>'
    while re.search(reg, content) is not None:
        m = re.search(reg, content)
        imgName = m.group(1).split('/')[-1]
        res = re.sub(reg, "![" + imgName.strip().split(".")[0] + "](" + m.group(1) + ")", content, count=1)
        # print(res)
        content = res

    with open(file_path, "w", encoding="UTF-8") as f:
        f.write(content)
    return file_path


def fix_block_equation(file_path):
    with open(file_path, "r", encoding="UTF-8") as f:
        lines = f.readlines()

    new_lines = []
    for (i, line) in enumerate(lines):
        new_line = [None, line, None]
        if i > 0 and i < len(lines) - 2:
            if line == '$$\n' and lines[i - 1][0] != '\n':
                new_line[0] = '\n'
            if line == '$$\n' and lines[i + 1][0] != '\n':
                new_line[2] = '\n'
        new_lines.append(new_line)
    new_lines = list(itertools.chain(*new_lines))
    new_lines = list(filter(lambda x: x is not None, new_lines))
    new_lines = ''.join(new_lines)
    lines = new_lines.splitlines(keepends=True)
    lines = [line if line.endswith('\n') else '{}\n'.format(line) for line in lines]

    with open(file_path, "w", encoding="UTF-8") as f:
        f.writelines(lines)
        # print(new_lines)
    return file_path


preprocess_list = [replace_html_img_tag, fix_block_equation]
