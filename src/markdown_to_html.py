from markdown_to_text import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    text_to_textnodes,
)
from htmlnode import LeafNode, ParentNode
from text_to_html import text_node_to_html_node


def text_to_children(text):
    nodes = text_to_textnodes(text)

    child_nodes = []
    for node in nodes:
        child_nodes.append(text_node_to_html_node(node))

    return child_nodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    node_list = []

    for block in blocks:
        block_type = block_to_block_type(block)

        lines = block.split("\n")

        if block_type == BlockType.PARAGRAPH:
            formatted_lines = block.replace("\n", " ")
            child_nodes = text_to_children(formatted_lines)
            node_list.append(ParentNode(tag="p", children=child_nodes))
        if block_type == BlockType.QUOTE:
            formatted_lines = ""
            for line in lines:
                formatted_lines += line[1:].strip()

            child_nodes = text_to_children(formatted_lines)
            node_list.append(ParentNode(tag="blockquote", children=child_nodes))
        if block_type == BlockType.UNORDERED_LIST:
            formatted_lines = ""
            for line in lines:
                formatted_lines += f"<li>{line[1:].strip()}</li>"

            child_nodes = text_to_children(formatted_lines)
            node_list.append(ParentNode(tag="ul", children=child_nodes))
        if block_type == BlockType.ORDERED_LIST:
            formatted_lines = ""
            for line in lines:
                formatted_lines += f"<li>{line[2:].strip()}</li>"
            child_nodes = text_to_children(formatted_lines)
            node_list.append(ParentNode(tag="ol", children=child_nodes))
        if block_type == BlockType.CODE:
            formatted_line = f"<code>{block[4:-3]}</code>"
            node_list.append(LeafNode("pre", formatted_line))
            continue
        if block_type == BlockType.HEADING:
            heading_level = block.rfind("# ") + 1

            formatted_lines = ""
            for line in lines:
                formatted_lines += line.split(" ", 1)[1]

            child_nodes = text_to_children(formatted_lines)
            node_list.append(ParentNode(tag=f"h{heading_level}", children=child_nodes))

    return ParentNode(tag="div", children=node_list)
