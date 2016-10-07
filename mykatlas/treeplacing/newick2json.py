#! /usr/bin/env python
import sys
# from ete2 import Tree
import random


def newick2json(node):
    node.name = node.name.replace("'", '')
    json = {"name": node.name,
            # "display_label": node.name,
            # "duplication": dup,
            # "branch_length": str(node.dist),
            # "common_name": node.name,
            # "seq_length": 0,
            "type": "node" if node.children else "leaf",
            # "uniprot_name": "Unknown",
            }
    if node.children:
        json["children"] = []
        for ch in node.children:
            json["children"].append(newick2json(ch))
    return json


# if __name__ == '__main__':
# 	t = Tree(sys.argv[1])
#     print str(get_json(t)).replace("'", '"')
