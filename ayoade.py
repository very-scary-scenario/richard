import os
from random import choice
import re

from pycaption import SAMIReader, CaptionNode


HERE = os.path.realpath(os.path.dirname(__file__))


def _nodes_that_are_ayoade(caption):
    for i, node in enumerate(caption.nodes[:-2]):
        if (
            node.type_ == CaptionNode.STYLE and
            node.content['color'] == 'white'
        ):
            next_node = caption.nodes[i+1]

            if (
                next_node.type_ == CaptionNode.TEXT and
                next_node.content != next_node.content.upper()
            ):
                yield next_node


def get_lines():
    subdir = os.path.join(HERE, 'subs')

    for sfn in os.listdir(subdir):
        if not re.match(r'^\d+$', sfn):
            continue

        reader = SAMIReader()

        with open(os.path.join(subdir, sfn)) as sf:
            tree = reader.read(sf.read())

        lang, = tree.get_languages()
        for caption in tree.get_captions(lang):
            ayoade_content = ' '.join((
                n.content.strip() for n in
                _nodes_that_are_ayoade(caption)
            ))

            if (
                ayoade_content and
                not ayoade_content.startswith('Subtitles by')
            ):
                yield ayoade_content


LINES = tuple(get_lines())

if __name__ == '__main__':
    print(choice(LINES))
