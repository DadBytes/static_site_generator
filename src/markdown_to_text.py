import re
from enum import Enum

from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text.split(delimiter)
        node_sections = []

        if len(node_text) % 2 == 0:
            raise ValueError(f"not valid markdown, missing closing {delimiter}")

        for i in range(len(node_text)):
            if node_text[i] == "":
                continue
            if i % 2 == 0:
                node_sections.append(TextNode(node_text[i], TextType.TEXT))
            else:
                node_sections.append(TextNode(node_text[i], text_type))

        new_nodes.extend(node_sections)

    return new_nodes


def extract_markdown_images(text):
    pattern = r"\!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    images = []
    for match in matches:
        images.append((match[0], match[1]))
    return images


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    links = []
    for match in matches:
        links.append((match[0], match[1]))
    return links


def split_nodes_image(old_nodes: list):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        for image in images:
            node_sections = original_text.split(f"![{image[0]}]({image[1]})", 1)

            if len(node_sections) != 2:
                raise ValueError("invalid markdown, missing closing tags")

            if node_sections[0] != "":
                new_nodes.append(TextNode(node_sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            original_text = node_sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        for link in links:
            node_sections = original_text.split(f"[{link[0]}]({link[1]})", 1)

            if len(node_sections) != 2:
                raise ValueError("invalid markdown, missing closing tags")

            if node_sections[0] != "":
                new_nodes.append(TextNode(node_sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            original_text = node_sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown: str) -> list:
    blocks = markdown.split("\n\n")

    formattted_blocks = []

    for block in blocks:
        block = block.strip()

        if block == "":
            continue

        formattted_blocks.append(block)

    return formattted_blocks


def check_ordered_block(block):
    list_items = block.split("\n")
    count = 1
    for item in list_items:
        if item.startswith(f"{count}. "):
            count += 1
            continue
        else:
            return False

    return True


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.rfind("# ") >= 0 and block.rfind("# ") < 6:
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if block.startswith("> "):
        for line in lines:
            if not line.startswith("> "):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        count = 1
        for line in lines:
            if line.startswith(f"{count}. "):
                count += 1
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
