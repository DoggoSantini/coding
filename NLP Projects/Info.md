#Natural Language Processing projects

This folder is specifically for NLP projects that I'll be working on over the next few weeks. Below I'll give a description of each file:

- wordvec_import.py: a python script to reformat the GloVe word embeddings from https://nlp.stanford.edu/projects/glove/ into python and numpy arrays and using json to save to a folder. In the specific file I used the 50-dim embeddings although this could easily be changed for the larger files. This is a simple script but useful to have the data ready for a variety of future projects involving pretrained word embeddings.

- thesaurus.py: a python script that takes in an input word and finds the closest words to it in the GloVe data use the standard L2 norm on their vector representations. It then returns the specified amount of words in order of "similarity". A future project would be to look at how higher-dimensional embeddings change the results.
