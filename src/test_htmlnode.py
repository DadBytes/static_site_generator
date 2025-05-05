import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_eq(self):
        node = HTMLNode("p", "This is a text node")
        node2 = HTMLNode("p", "This is a text node")
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.value, node2.value)
        self.assertEqual(node.children, node2.children)
        self.assertEqual(node.props, node2.props)

    def test_not_eq(self):
        node = HTMLNode("p", "This is a text node")
        node2 = HTMLNode("div", "This is a text node")
        self.assertNotEqual(node.tag, node2.tag)
        self.assertEqual(node.value, node2.value)

    def test_repr(self):
        node = HTMLNode("p", "This is a text node")
        expected_output = "HTMLNode(p, This is a text node, children: None, None)"
        self.assertEqual(node.__repr__(), expected_output)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_no_tag(self):
        node = LeafNode(tag=None, value="This is a text node")
        self.assertEqual(node.to_html(), "This is a text node")

    def test_leaf_no_value(self):
        node = LeafNode(tag=None, value=None)
        self.assertRaises(ValueError, node.to_html)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        node = ParentNode("div", None)
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()
