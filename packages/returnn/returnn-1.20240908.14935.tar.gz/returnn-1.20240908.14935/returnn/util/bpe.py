"""
Provide basic Byte-Pair-Encoding (BPE) utilities.
"""

from __future__ import annotations
from typing import Optional, List, Dict, Callable
from dataclasses import dataclass
import re
import numpy


BpePostMergeSymbol = "@@"


class StandardBytePairEncoder:
    """
    Code is partly taken from subword-nmt/apply_bpe.py.
    Author: Rico Sennrich, code under MIT license.

    Use operations learned with learn_bpe.py to encode a new text.
    The text will not be smaller, but use only a fixed vocabulary, with rare words
    encoded as variable-length sequences of subword units.

    Reference:
    Rico Sennrich, Barry Haddow and Alexandra Birch (2016). Neural Machine Translation of Rare Words with Subword Units.
    Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (ACL 2016). Berlin, Germany.

    """

    def __init__(self, bpe_codes_file, labels=None):
        """
        :param str bpe_codes_file: codes file
        :param list[str]|None labels: vocab
        """
        self.labels = labels
        self._load(bpe_codes_file)
        self._bpe_encode_cache = {}
        self._bpe_separator = BpePostMergeSymbol

    _file_cache = {}  # filename -> bpe_file_version, bpe_codes, bpe_codes_reverse

    def _load(self, bpe_codes_file):
        """
        Load BPE codes from file

        :param str bpe_codes_file: codes file
        """
        if bpe_codes_file in self._file_cache:
            self._bpe_file_version, self._bpe_codes, self._bpe_codes_reverse = self._file_cache[bpe_codes_file]
            return
        # check version information
        bpe_file_first_line = open(bpe_codes_file, "r").readline()
        if bpe_file_first_line.startswith("#version:"):
            self._bpe_file_version = tuple(
                [int(x) for x in re.sub(r"(\.0+)*$", "", bpe_file_first_line.split()[-1]).split(".")]
            )
        else:
            self._bpe_file_version = (0, 1)
        self._bpe_codes = [
            tuple(item.split()) for item in open(bpe_codes_file, "rb").read().decode("utf8").splitlines()
        ]
        # some hacking to deal with duplicates (only consider first instance)
        self._bpe_codes = dict([(code, i) for (i, code) in reversed(list(enumerate(self._bpe_codes)))])
        self._bpe_codes_reverse = dict([(pair[0] + pair[1], pair) for pair, i in self._bpe_codes.items()])
        self._file_cache[bpe_codes_file] = (self._bpe_file_version, self._bpe_codes, self._bpe_codes_reverse)

    @staticmethod
    def _get_pairs(word):
        """
        :param tuple[str] word: represented as tuple of symbols (symbols being variable-length strings)
        :return: set of symbol pairs in a word
        :rtype: set[(str,str)]
        """
        pairs = set()
        prev_char = word[0]
        for char in word[1:]:
            pairs.add((prev_char, char))
            prev_char = char
        return pairs

    def _encode_word(self, orig):
        """
        Encode word based on list of BPE merge operations, which are applied consecutively.
        :param str orig:
        :rtype: tuple[str]
        """

        if orig in self._bpe_encode_cache:
            return self._bpe_encode_cache[orig]

        if self._bpe_file_version == (0, 1):
            word = tuple(orig) + ("</w>",)
        elif self._bpe_file_version == (0, 2):  # more consistent handling of word-final segments
            word = tuple(orig[:-1]) + (orig[-1] + "</w>",)
        else:
            raise NotImplementedError

        pairs = self._get_pairs(word)
        if not pairs:
            return orig

        while True:
            bigram = min(pairs, key=lambda pair: self._bpe_codes.get(pair, float("inf")))
            if bigram not in self._bpe_codes:
                break
            first, second = bigram
            new_word = []
            i = 0
            while i < len(word):
                try:
                    j = word.index(first, i)
                    new_word.extend(word[i:j])
                    i = j
                except ValueError:
                    new_word.extend(word[i:])
                    break

                if word[i] == first and i < len(word) - 1 and word[i + 1] == second:
                    new_word.append(first + second)
                    i += 2
                else:
                    new_word.append(word[i])
                    i += 1
            new_word = tuple(new_word)
            word = new_word
            if len(word) == 1:
                break
            else:
                pairs = self._get_pairs(word)

        # don't print end-of-word symbols
        if word[-1] == "</w>":
            word = word[:-1]
        elif word[-1].endswith("</w>"):
            word = word[:-1] + (word[-1].replace("</w>", ""),)

        if self.labels:
            word = self._check_vocab_and_split(word, self._bpe_codes_reverse, self.labels, self._bpe_separator)

        self._bpe_encode_cache[orig] = word
        return word

    def _check_vocab_and_split(self, orig, bpe_codes, vocab, separator):
        """
        Check for each segment in word if it is in-vocabulary,
        and segment OOV segments into smaller units by reversing the BPE merge operations
        """

        out = []

        for segment in orig[:-1]:
            if segment + separator in vocab:
                out.append(segment)
            else:
                # sys.stderr.write('OOV: {0}\n'.format(segment))
                for item in self._recursive_split(segment, bpe_codes, vocab, separator, False):
                    out.append(item)

        segment = orig[-1]
        if segment in vocab:
            out.append(segment)
        else:
            # sys.stderr.write('OOV: {0}\n'.format(segment))
            for item in self._recursive_split(segment, bpe_codes, vocab, separator, True):
                out.append(item)

        return out

    def _recursive_split(self, segment, bpe_codes, vocab, separator, final=False):
        """Recursively split segment into smaller units (by reversing BPE merges)
        until all units are either in-vocabulary, or cannot be split further."""

        # noinspection PyBroadException
        try:
            if final:
                left, right = bpe_codes[segment + "</w>"]
                right = right[:-4]
            else:
                left, right = bpe_codes[segment]
        except Exception:  # TODO fix
            # sys.stderr.write('cannot split {0} further.\n'.format(segment))
            yield segment
            return

        if left + separator in vocab:
            yield left
        else:
            for item in self._recursive_split(left, bpe_codes, vocab, separator, False):
                yield item

        if (final and right in vocab) or (not final and right + separator in vocab):
            yield right
        else:
            for item in self._recursive_split(right, bpe_codes, vocab, separator, final):
                yield item

    def segment_sentence(self, sentence):
        """
        Segment single sentence (whitespace-tokenized string) with BPE encoding.

        :param str sentence:
        :rtype: list[str]
        """

        output = []

        found_category = False
        skip_category = False

        for word in sentence.split():
            if word[0] == "$" and len(word) > 1:
                found_category = True
                output.append(word)
            elif found_category is True and word[0] == "{":
                skip_category = True
                output.append(word)
            elif skip_category is True and word[0] != "}":
                output.append(word)
            else:
                found_category = False
                skip_category = False
                new_word = self._encode_word(word)

                for item in new_word[:-1]:
                    output.append(item + self._bpe_separator)
                output.append(new_word[-1])

        return output


@dataclass
class BpeOpts:
    """
    Options, should allow for both subword-nmt BPE and SentencePiece BPE/Unigram.
    """

    label_postfix_merge_symbol: Optional[str] = None  # eg. "@@"
    word_prefix_symbol: Optional[str] = None  # eg. "▁"


class PrefixTree:
    """
    Prefix tree / trie.
    This class represents both a single node and the tree.
    """

    def __init__(self, *, prefix: str = "", opts: BpeOpts):
        """
        :param prefix: if this is not the root, the prefix to get here
        """
        self.prefix = prefix
        self.arcs: Dict[str, PrefixTree] = {}  # single char (or BpePostMergeSymbol) -> sub tree
        self.finished = False  # label finished here
        self.bpe_finished = False  # partial word finished here with BpePostMergeSymbol at end
        self.opts = opts

    def add(self, postfix: str) -> PrefixTree:
        """
        :param postfix:
        """
        self_ = self
        opts = self.opts
        label_postfix_merge_symbol = self.opts.label_postfix_merge_symbol
        while True:
            if self_ is self and opts.word_prefix_symbol and postfix.startswith(opts.word_prefix_symbol):
                arc = opts.word_prefix_symbol
            elif postfix == label_postfix_merge_symbol:
                arc = postfix
            else:
                arc = postfix[:1]
            postfix_ = postfix[len(arc) :]
            if arc in self_.arcs:
                child = self_.arcs[arc]
            else:
                child = PrefixTree(prefix=self_.prefix + arc, opts=opts)
                self_.arcs[arc] = child
            if arc == label_postfix_merge_symbol and not postfix_:
                self_.bpe_finished = True
            if not postfix_:
                child.finished = True
                return child
            self_ = child
            postfix = postfix_


@dataclass
class Hyp:
    """
    Represents a hypothesis in the search.
    """

    bpe_sym_history: List[str]
    cur_node: PrefixTree


class CharSyncSearch:
    """
    Covers the search hyps and the search itself.
    """

    def __init__(self, bpe: PrefixTree, word: str, word_pos: int = 0):
        """
        :param bpe:
        :param word:
        :param word_pos:
        """
        self.bpe = bpe
        self.opts = bpe.opts
        self.word = word
        self.word_pos = word_pos
        self.hyps: List[Hyp] = [
            Hyp(
                bpe_sym_history=[],
                cur_node=bpe if self.opts.word_prefix_symbol is None else bpe.arcs[self.opts.word_prefix_symbol],
            )
        ]
        self.final_bpe_seqs: Optional[List[List[str]]] = None

    def _get_finished(self):
        assert self.word_pos == len(self.word)
        finals: List[List[str]] = []
        for hyp in self.hyps:
            if hyp.cur_node.finished:
                finals.append(hyp.bpe_sym_history + [hyp.cur_node.prefix])
        self.final_bpe_seqs = finals

    def _expand(self):
        assert self.word_pos < len(self.word)
        char = self.word[self.word_pos]
        new_hyps: List[Hyp] = []
        for hyp in self.hyps:
            if hyp.cur_node.bpe_finished:
                # Start again from root node.
                next_node = self.bpe.arcs.get(char)
                if next_node:
                    new_hyps.append(
                        Hyp(
                            bpe_sym_history=hyp.bpe_sym_history
                            + [hyp.cur_node.prefix + self.opts.label_postfix_merge_symbol],
                            cur_node=next_node,
                        )
                    )
            if self.opts.word_prefix_symbol is not None and hyp.cur_node.finished:
                next_node = self.bpe.arcs.get(char)
                if next_node:
                    new_hyps.append(
                        Hyp(bpe_sym_history=hyp.bpe_sym_history + [hyp.cur_node.prefix], cur_node=next_node)
                    )
            next_node = hyp.cur_node.arcs.get(char)
            if next_node:
                new_hyps.append(Hyp(bpe_sym_history=hyp.bpe_sym_history, cur_node=next_node))
        self.hyps = new_hyps

    def search(self) -> List[List[str]]:
        """
        :return: collection of possible BPE symbol seqs
        """
        while self.word_pos < len(self.word):
            self._expand()
            self.word_pos += 1
        self._get_finished()
        return self.final_bpe_seqs


@dataclass
class HypInPos:
    """
    Represents a hypothesis in the search.
    """

    bpe_sym_history: List[str]
    cur_node: PrefixTree
    pos: int


class DepthFirstSearch:
    """
    Depth-first search.
    """

    def __init__(self, bpe: PrefixTree, word: str, sampler: Optional[Callable[[], bool]] = None):
        """
        :param bpe:
        :param word:
        :param sampler:
        """
        self.bpe = bpe
        self.opts = bpe.opts
        self.word = word
        self.sampler = sampler
        self.hyps: List[HypInPos] = []
        self.final_bpe_seq: Optional[List[str]] = None
        self._add_hyp(
            HypInPos(
                bpe_sym_history=[],
                cur_node=bpe if self.opts.word_prefix_symbol is None else bpe.arcs[self.opts.word_prefix_symbol],
                pos=0,
            )
        )

    def _add_hyp(self, hyp: HypInPos):
        if hyp.pos >= len(self.word):
            if hyp.cur_node.finished:
                self.final_bpe_seq = hyp.bpe_sym_history + [hyp.cur_node.prefix]
        else:
            self.hyps.append(hyp)

    def _expand(self):
        hyp = self.hyps.pop(-1)

        # Now check for possible further hyps.
        char = self.word[hyp.pos]
        new_hyps: List[HypInPos] = []
        if hyp.cur_node.bpe_finished:
            # Start again from root node.
            next_node = self.bpe.arcs.get(char)
            if next_node:
                new_hyps.append(
                    HypInPos(
                        bpe_sym_history=hyp.bpe_sym_history
                        + [hyp.cur_node.prefix + self.opts.label_postfix_merge_symbol],
                        cur_node=next_node,
                        pos=hyp.pos + 1,
                    )
                )
        if self.opts.word_prefix_symbol is not None and hyp.cur_node.finished:
            next_node = self.bpe.arcs.get(char)
            if next_node:
                new_hyps.append(
                    HypInPos(
                        bpe_sym_history=hyp.bpe_sym_history + [hyp.cur_node.prefix], cur_node=next_node, pos=hyp.pos + 1
                    )
                )
        next_node = hyp.cur_node.arcs.get(char)
        if next_node:
            new_hyps.append(HypInPos(bpe_sym_history=hyp.bpe_sym_history, cur_node=next_node, pos=hyp.pos + 1))

        # Note that the order we check them will make this a depth-first or breadth-first search.
        # We pop(-1) from the hyps list. So the last entry we add here will be the next one we expand.
        if self.sampler and self.sampler():
            new_hyps = list(reversed(new_hyps))
        for hyp in new_hyps:
            self._add_hyp(hyp)

    def search(self) -> Optional[List[str]]:
        """
        :return: BPE symbol seq if one is found
        """
        while self.hyps and self.final_bpe_seq is None:
            self._expand()
        return self.final_bpe_seq


class SamplingBytePairEncoder:
    """
    Will randomly sample from any possible BPE split.
    """

    def __init__(
        self,
        *,
        labels: List[str],
        breadth_prob: float,
        rnd: numpy.random.RandomState,
        unknown_label: Optional[str] = None,
        opts: BpeOpts,
    ):
        """
        :param labels: vocab
        :param breadth_prob: 1.0 will lead to breadth-first search, 0.0 to depth-first search.
            other values are stochastic.
        :param rnd:
        :param unknown_label:
        :param opts:
        """
        self.labels = labels
        self.unknown_label = unknown_label
        if unknown_label:
            assert unknown_label in self.labels
        self.breadth_prob = breadth_prob
        self.rnd = rnd
        self.opts = opts

        # build prefix tree
        bpe = PrefixTree(opts=opts)
        for bpe_sym in labels:
            bpe.add(bpe_sym)
        self._bpe_prefix_tree = bpe

    def _sampler(self) -> bool:
        # When this returns true, it will differ from depth-first search.
        return self.rnd.random_sample() <= self.breadth_prob

    def get_bpe_split_for_word(self, word: str) -> Optional[List[str]]:
        """
        :param word:
        """
        return DepthFirstSearch(bpe=self._bpe_prefix_tree, word=word, sampler=self._sampler).search()

    def segment_sentence(self, sentence: str) -> List[str]:
        """
        Segment single sentence (whitespace-tokenized string) with BPE encoding.

        :param sentence:
        """
        output = []
        for word in sentence.split():
            bpe_sym_seq = self.get_bpe_split_for_word(word)
            if bpe_sym_seq is None:
                if self.unknown_label:
                    output.append(self.unknown_label)
                    continue
                else:
                    raise Exception("no BPE-split for word %r" % word)
            output.extend(bpe_sym_seq)
        return output


def _demo():
    import sys
    import os

    my_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(my_dir))
    assert os.path.exists("%s/returnn/__init__.py" % root_dir)
    sys.path.insert(0, root_dir)

    from returnn.util import better_exchook

    better_exchook.install()

    import argparse

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--vocab", required=True)
    arg_parser.add_argument("--unk")
    arg_parser.add_argument("--input", help="text. if not given, will read from stdin")
    arg_parser.add_argument("--seed", type=int, default=0)
    arg_parser.add_argument("--all", action="store_true")
    arg_parser.add_argument(
        "--breadth-prob",
        type=float,
        default=0.0,
        help="1.0 will lead to breadth-first search, 0.0 to depth-first search. other values are stochastic.",
    )
    args = arg_parser.parse_args()

    from returnn.datasets.util.vocabulary import Vocabulary

    vocab = Vocabulary(vocab_file=args.vocab, unknown_label=None)
    rnd = numpy.random.RandomState(args.seed)
    opts = BpeOpts(label_postfix_merge_symbol=BpePostMergeSymbol)

    if args.input:
        bpe_prefix_tree = PrefixTree(opts=opts)
        for bpe_sym in vocab.labels:
            bpe_prefix_tree.add(bpe_sym)

        def _sampler():
            # When this returns true, it will differ from depth-first search.
            return rnd.random_sample() <= args.breadth_prob

        for word in args.input.split():
            if args.all:
                bpe_sym_seqs = CharSyncSearch(bpe=bpe_prefix_tree, word=word).search()
                print("%s: %s" % (word, bpe_sym_seqs))
            else:
                greedy = DepthFirstSearch(bpe=bpe_prefix_tree, word=word, sampler=_sampler).search()
                print("%s: %s" % (word, " ".join(greedy)))
        return

    bpe = SamplingBytePairEncoder(
        labels=vocab.labels, breadth_prob=args.breadth_prob, rnd=rnd, unknown_label=args.unk, opts=opts
    )
    print("Reading from stdin:")
    while True:
        try:
            line = sys.stdin.readline()
            if line == "":  # EOF
                return
        except KeyboardInterrupt:
            return
        line = line.strip()
        print(" ".join(bpe.segment_sentence(line)))


if __name__ == "__main__":
    _demo()
