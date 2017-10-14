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


def combine_sentences(subs):
    skip_next = False
    total = len(subs)

    for i, sub in enumerate(subs):
        if skip_next:
            skip_next = False
            continue

        if i == (total - 1):
            yield sub
            break

        next_sub = subs[i + 1]
        if (
            i != (total - 1) and
            sub and next_sub and
            sub[-1] not in ('.', '?', '!') and
            next_sub[0] != next_sub[0].upper()
        ):
            yield '{} {}'.format(sub, next_sub)
            skip_next = True
        else:
            yield sub


def remove_empty(subs):
    return (s for s in subs if s)


def remove_credits(subs):
    return (s for s in subs if not s.startswith('Subtitles by'))


def get_raw_lines():
    subdir = os.path.join(HERE, 'subs')

    for sfn in os.listdir(subdir):
        if not re.match(r'^\d+$', sfn):
            continue

        reader = SAMIReader()

        with open(os.path.join(subdir, sfn)) as sf:
            tree = reader.read(sf.read())

        lang, = tree.get_languages()
        for caption in tree.get_captions(lang):
            sub = ' '.join((
                n.content.strip() for n in
                _nodes_that_are_ayoade(caption)
            ))

            yield sub

        yield ''


def get_lines():
    subs = list(get_raw_lines())
    length = len(subs)

    # keep combining sentences until doing so changes nothing
    # (this is comically inefficient, i know)
    while True:
        subs = list(combine_sentences(subs))
        _length = len(subs)

        if _length == length:
            break
        else:
            length = _length

    return list(remove_credits(remove_empty(subs)))


LINES = tuple(get_lines())


def get_line():
    return choice(LINES)


if __name__ == '__main__':
    print(get_line())
