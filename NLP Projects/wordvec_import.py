import numpy as np
import json

words = []
vectors = []
idx = 0
word_to_idx = {}

# Data from https://nlp.stanford.edu/projects/glove/

with open("Data/glove_data_50.txt", 'rb') as f:

    for line in f:
        line_dec = line.split()
        word = line_dec[0].decode("utf-8")
        words.append(word)
        word_to_idx[word] = idx

        
        word_vec = np.array(line_dec[1:]).astype(np.float)
        vectors.append(word_vec)
        
        idx += 1
        
vectors = np.asarray(vectors)

np.save('Data/data_vectors.npy', vectors)

with open('Data/data_words.txt', 'w') as f:
    json.dump(words, f)

with open('Data/data_word_to_idx.txt', 'w') as f:
    json.dump(word_to_idx, f, indent = 4)

