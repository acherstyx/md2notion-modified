from notion.client import NotionClient
from notion.block import PageBlock
from md2notion.upload import uploadBlock, convert
from md2notion.upload import addLatexExtension, NotionPyRenderer  # latex support
from md2notion.NotionPyRenderer import EquationBlock
from preprocess import preprocess_list
from config import *

import os

# fix latex import error
class ModifiedNotionPyRenderer(NotionPyRenderer):

    def __init__(self, *extraExtensions):
        super(ModifiedNotionPyRenderer, self).__init__(*extraExtensions)

    def render_block_equation(self, token):
        def blockFunc(blockStr):
            return {
                'type': EquationBlock,
                'title_plaintext': blockStr.replace('\\', '\\')  # \\\\ not work correctly on my system
            }

        return self.renderMultipleToStringAndCombine(token.children, blockFunc)


def get_md(root_dir):
    f_list = []
    for r, d, f in os.walk(root_dir):
        for file in f:
            if file.endswith(".md"):
                # print(os.path.join(r, file))
                f_list.append(os.path.join(r, file))
    return f_list


# default
def upload2notion(local_md, token_v2, block_url, title):
    # Follow the instructions at https://github.com/jamalex/notion-py#quickstart to setup Notion.py
    client = NotionClient(token_v2=token_v2)
    page = client.get_block(block_url)

    with open(local_md, "r", encoding="UTF-8") as mdFile:
        newPage = page.children.add_new(PageBlock, title=title)
        # upload(mdFile, newPage, notionPyRendererCls=addLatexExtension(
        #     NotionPyRenderer))  # Appends the converted contents of TestMarkdown.md to newPage
        lines = mdFile.readlines()
        rendered = convert(lines, addLatexExtension(ModifiedNotionPyRenderer))
        for blockDesc in rendered:
            uploadBlock(blockDesc, newPage, mdFile.name)


if __name__ == "__main__":
    md_files = get_md(md_dir)
    for md_file in md_files:
        for action in preprocess_list:
            md_file = action(md_file)

        upload2notion(local_md=md_file,
                      token_v2=token,
                      block_url=block,
                      title=md_file.split("\\")[-1].split(".")[-2])
