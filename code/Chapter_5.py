# nltk for POS-tagging

import nltk
text = word_tokenize("And now for something completely different")
nltk.pos_tag(text)

bigram_tagger = nltk.BigramTagger(train_sents)
bigram_tagger.tag(text)

import spacy
nlp = spacy.load('en')
sent_0 = nlp(u'Mathieu and I went to the park.')
sent_1 = nlp(u'If Clement was asked to take out the garbage, he would refuse.')
sent_2 = nlp(u'Baptiste was in charge of the refuse treatment center.')
sent_3 = nlp(u'Marie took out her rather suspicious and fishy cat to go fish for fish.')

for token in sent_0:
    print(token.text, token.pos_, token.tag_)

for token in sent_1:
    print(token.text, token.pos_, token.tag_)

for token in sent_2:
    print(token.text, token.pos_, token.tag_)

for token in sent_3:
    print(token.text, token.pos_, token.tag_)

# training NER

TRAIN_DATA = [
     ("Facebook has been accused for leaking personal data of users.", {'entities': [(0, 8, 'ORG')]}),
     ("Tinder uses sophisticated algorithms to find the perfect match.", {'entities': [(0, 6, "ORG")]})]

nlp = spacy.blank('en')
optimizer = nlp.begin_training()
for i in range(20):
    random.shuffle(TRAIN_DATA)
    for text, annotations in TRAIN_DATA:
        nlp.update([text], [annotations], sgd=optimizer)
nlp.to_disk('/model')



## run this code as a seperate file

from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy


# You need to define a mapping from your data's part-of-speech tag names to the
# Universal Part-of-Speech tag set, as spaCy includes an enum of these tags.
# See here for the Universal Tag Set:
# http://universaldependencies.github.io/docs/u/pos/index.html
# You may also specify morphological features for your tags, from the universal
# scheme.
TAG_MAP = {
    'N': {'pos': 'NOUN'},
    'V': {'pos': 'VERB'},
    'J': {'pos': 'ADJ'}
}

# Usually you'll read this in, of course. Data formats vary. Ensure your
# strings are unicode and that the number of tags assigned matches spaCy's
# tokenization. If not, you can always add a 'words' key to the annotations
# that specifies the gold-standard tokenization, e.g.:
# ("Eatblueham", {'words': ['Eat', 'blue', 'ham'] 'tags': ['V', 'J', 'N']})
TRAIN_DATA = [
    ("I like green eggs", {'tags': ['N', 'V', 'J', 'N']}),
    ("Eat blue ham", {'tags': ['V', 'J', 'N']})
]


@plac.annotations(
    lang=("ISO Code of language to use", "option", "l", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))
def main(lang='en', output_dir=None, n_iter=25):
    """Create a new model, set up the pipeline and train the tagger. In order to
    train the tagger with a custom tag map, we're creating a new Language
    instance with a custom vocab.
    """
    nlp = spacy.blank(lang)
    # add the tagger to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    tagger = nlp.create_pipe('tagger')
    # Add the tags. This needs to be done before you start training.
    for tag, values in TAG_MAP.items():
        tagger.add_label(tag, values)
    nlp.add_pipe(tagger)

    optimizer = nlp.begin_training()
    for i in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            nlp.update([text], [annotations], sgd=optimizer, losses=losses)
        print(losses)

    # test the trained model
    test_text = "I like blue eggs"
    doc = nlp(test_text)
    print('Tags', [(t.text, t.tag_, t.pos_) for t in doc])

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the save model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        doc = nlp2(test_text)
        print('Tags', [(t.text, t.tag_, t.pos_) for t in doc])


if __name__ == '__main__':
    plac.call(main)

    # Expected output:
    # [
    #   ('I', 'N', 'NOUN'),
    #   ('like', 'V', 'VERB'),
    #   ('blue', 'J', 'ADJ'),
    #   ('eggs', 'N', 'NOUN')
    # ]