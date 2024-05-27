import nltk
import re

nltk.download("punkt")

from nltk.tokenize import word_tokenize, sent_tokenize


def statistical_tokenizer(text):
    return word_tokenize(text)


def hybrid_tokenizer(text):
    sentences = sent_tokenize(text)
    tokens = []
    for sentence in sentences:
        tokens.extend(word_tokenize(sentence))
    return tokens


# Extended list of common abbreviations including personal titles, country names, etc.
abbreviations = {
    "mr",
    "mrs",
    "ms",
    "dr",
    "st",
    "jr",
    "sr",
    "vs",
    "prof",
    "inc",
    "etc",
    "u.s.a",
    "u.k",
    "u.n",
    "e.u",
    "ph.d",
    "m.d",
    "d.c",
    "a.k.a",
    "i.e",
    "e.g",
    "j.p",
    "w.r",
}

# Pattern to match abbreviations, words, numbers (including decimals, negative numbers, fractions), and punctuations
pattern = r"""
    (?x)                             # set flag to allow verbose regex
    (?:[A-Za-z]\.){2,}               # abbreviations with periods, e.g. U.S.A., J.P.
    | \d+/\d+                        # fractions
    | \d+(?:\.\d+)?%?                # numbers, including decimals and percentages
    | -\d+(?:\.\d+)?%?               # negative numbers, including decimals and percentages
    | \w+(?:[-'?!@#^]\w+)*              # words with optional internal hyphens/apostrophes,etc.
    | (?:\w+\.){2,}                  # words with periods, like company and name abbreviations
    | (?:[A-Z][a-z]*\.?){2,}         # common abbreviations like Co., Corp., Inc., etc.
    | [A-Za-z]+(?:\.[A-Za-z]+)?      # words with optional period in between, like Co.
    | \.\.\.                         # ellipsis
    | [.,;"'?():-_`]                 # these are separate tokens; excludes spaces
"""


def is_abbreviation(word):
    # Check if the word (lowercase) is an abbreviation
    return word.lower() in abbreviations


def rule_based_tokenizer(text):
    tokens = re.findall(pattern, text)

    # Post-processing to handle abbreviations and sentence endings
    processed_tokens = []
    for i, token in enumerate(tokens):
        if token.strip():  # Check if the token is not empty after stripping whitespace
            if token == "." or token == "?" or token == "!":
                if i < len(tokens) - 1 and tokens[i + 1] == ",":
                    # Period followed by comma is part of an abbreviation
                    processed_tokens[-1] += token if processed_tokens else token
                elif i > 0 and tokens[i - 1].isupper():
                    # Period preceded by a capital letter is part of an abbreviation
                    processed_tokens[-1] += token if processed_tokens else token
                elif (
                    i < len(tokens) - 2
                    and tokens[i + 1] == " "
                    and tokens[i + 2].isupper()
                ):
                    # Period followed by space and then a capital letter indicates end of sentence
                    processed_tokens.append(token)
                elif i < len(tokens) - 1 and (
                    tokens[i + 1].islower() or tokens[i + 1].isdigit()
                ):
                    # Period followed by lowercase letter or digit is part of abbreviation or number
                    processed_tokens[-1] += token if processed_tokens else token
                else:
                    # Otherwise, treat as end of sentence
                    processed_tokens.append(token)
            else:
                processed_tokens.append(token)

    return processed_tokens


# Sample text
text = (
    "J.P. Bolduc, vice chairman of W.R. Grace & Co., which holds an 83.4% interest in this "
    "energy-services company, was elected a director. Clark J. Vitulli was named senior vice president "
    "and general manager of this U.S. sales and marketing arm of Japanese auto maker Mazda Motor Corp. "
    "The company's stock price increased by 5.75%. Negative growth of -2.5% was observed last quarter. "
    "He sold 1/2 of his shares. He moved to San-Franc?isco  abc@gmail.com ."
)

# Tokenize using the enhanced rule-based approach
statistical_tokens = statistical_tokenizer(text)

hybrid_tokens = hybrid_tokenizer(text)

tokens = rule_based_tokenizer(text)

# Print results

print("Statistical Tokenizer Output:", statistical_tokens)
print()
print()
print("Hybrid Tokenizer Output:", hybrid_tokens)
print()
print()
print("Enhanced Rule-based Tokenizer Output:", tokens)
