import os
import nltk
import argparse
import random


def read_lexicon(path):
    lexicon = {}
    with open(path, "r") as f:
        for i, line in enumerate(f.readlines()):
            split = line.replace("  ", "\t").replace("\t\t", "\t").split("\t")
            if len(split) == 1 and " " in split[0]:
                split = [line[: line.index(" ")], line[line.index(" ") :]]
            if len(split) != 2:
                raise Exception(
                    "Cannot parse lexicon " + path + " at line " + str(i + 1)
                )
            key = split[0].strip().upper()
            if key not in lexicon:
                lexicon[key] = "{" + split[1].strip() + "}"
            else:
                pass  # TODO: Some language model stuff to pick the right version?
    return lexicon


def words_to_arpabet(
    path, lexicon, newline_symbol=False, keep_graphemes=False, allow_unknown=False
):
    output = []
    t = nltk.tokenize.TweetTokenizer()
    with open(path, "r") as f:
        for line in [x.split("|") for x in f.readlines()]:
            did_anything = False
            if len(line) != 2 and len(line) != 3:
                raise Exception(
                    "Cannot parse transcript "
                    + path
                    + " at line "
                    + str(len(output) + 1)
                )
            words = t.tokenize(line[-1].strip())
            for j in range(len(words)):
                w = words[j].upper()
                if w.replace("'", "").isalnum() and w in lexicon:
                    words[j] = lexicon[w]
                    did_anything = True
                elif w.isalnum() and w not in lexicon:
                    e = str(
                        "Word "
                        + w
                        + " is not in lexicon; present on line "
                        + str(len(output) + 1)
                    )
                    if allow_unknown:
                        print("Warning: " + e)
                    else:
                        raise Exception(e)
            output.append(line[0] + "|" + " ".join(words))
            if newline_symbol:
                output[-1] += "␤\n"
            else:
                output[-1] += "\n"
            if keep_graphemes:
                output.append(line[0] + "|" + line[-1].strip())
                if newline_symbol:
                    output[-1] += "␤\n"
                else:
                    output[-1] += "\n"
            if not did_anything:
                print("Warning: Tokenized no words on line " + str(len(output)))
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Converts LJSpeech format transcripts to ARPAbet.
        Results are saved next to the input with a .arpa.txt extension."""
    )
    parser.add_argument("lexicon_path", type=str, help="path to ARPAbet dictionary")
    parser.add_argument("transcript_path", type=str, help="path to transcript")
    parser.add_argument(
        "-n", "--newline", action="store_true", help="add trailing newline symbols (␤)",
    )
    parser.add_argument(
        "-k",
        "--keepboth",
        action="store_true",
        help="write both graphemes and ARPAbet to the output",
    )
    parser.add_argument(
        "-u",
        "--unknown",
        action="store_true",
        help="allow unknown words (not recommended)",
    )
    parser.add_argument(
        "-s", "--shuffle", action="store_true", help="shuffle the output",
    )

    args = parser.parse_args()
    lexicon = read_lexicon(args.lexicon_path)
    output = words_to_arpabet(
        args.transcript_path,
        lexicon,
        newline_symbol=args.newline,
        keep_graphemes=args.keepboth,
        allow_unknown=args.unknown,
    )
    if args.shuffle:
        random.shuffle(output)
    output_path = os.path.splitext(args.transcript_path)[0] + ".arpa.txt"
    with open(output_path, "w") as f:
        f.writelines(output)
    print("Saved output to " + output_path)
