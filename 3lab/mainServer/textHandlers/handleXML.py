from xml.etree.ElementTree import tostring, SubElement
import nltk.tree


def saveToFileXML(parsed_sentence):
    root = parsed_sentence["treeXML"]
    sentence_id = parsed_sentence["mainTree"]["id"]

    xml_tree = tostring(root, encoding="unicode")
    with open(f'../assets/trees/parse_tree{sentence_id}', 'w', encoding='utf-8') as file:
        file.write(xml_tree)


def saveAllToFileXML(parsed_sentences):
    for parsed_sentence in parsed_sentences:
        saveToFileXML(parsed_sentence)


def generateTreeXML(tree, parent=None):
    if isinstance(tree, str):
        element = SubElement(parent, "leaf")
        element.text = tree
    else:
        label = tree.label() if isinstance(tree, nltk.tree.Tree) else "word"
        element = SubElement(parent, "node", label=label)
        for child in tree:
            generateTreeXML(child, parent=element)
    return parent

