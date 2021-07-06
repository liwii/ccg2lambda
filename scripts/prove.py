#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  Copyright 2015 Pascual Martinez-Gomez
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import print_function

import argparse
import codecs
import logging
from lxml import etree
import os
import sys
import textwrap
import json

from semantic_tools import prove_doc
from visualization_tools import convert_doc_to_mathml

def main(args = None):
    DESCRIPTION=textwrap.dedent("""\
            The input file sem should contain the parsed sentences. All CCG trees correspond
            to the premises, except the last one, which is the hypothesis.
      """)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=DESCRIPTION)
    parser.add_argument("sem", help="XML input filename with semantics")
    parser.add_argument("--graph_out", nargs='?', type=str, default="",
        help="HTML graphical output filename.")
    parser.add_argument("--coref", type=str, default="")
    parser.add_argument("--replacements", type=str, default="")
    parser.add_argument("--abduction", action="store_true", default=False)
    parser.add_argument("--gold_trees", action="store_true", default=False)
    args = parser.parse_args()

    coref, replacements = None, None
    if args.coref != "":
        with open(args.coref, 'r') as f:
            coref = json.load(f)
    if args.replacements != "":
        with open(args.replacements, 'r') as f:
            replacements = json.load(f)

    if not os.path.exists(args.sem):
        print('File does not exist: {0}'.format(args.sem), file=sys.stderr)
        parser.print_help(file=sys.stderr)
        sys.exit(1)

    logging.basicConfig(level=logging.WARNING)

    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(args.sem, parser)

    inference_result, coq_scripts = prove_doc(doc, args.abduction, coref, replacements)
    print(inference_result, file=sys.stdout)

    if args.graph_out:
        html_str = convert_doc_to_mathml(doc, coq_scripts, args.gold_trees)
        with codecs.open(args.graph_out, 'w', 'utf-8') as fout:
            fout.write(html_str)

if __name__ == '__main__':
    main()
