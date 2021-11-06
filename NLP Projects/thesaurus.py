import numpy as np
import json

vectors = np.load("Data/data_vectors.npy")

with open("Data/data_words.txt", 'r') as f_word, open("Data/data_word_to_idx.txt", 'r') as f_dict:
    words = json.load(f_word)
    word_to_idx = json.load(f_dict)

word_input = input('What word would you like to replace? ')
num_outputs = int(input('How many words would you like to see? ')) + 1
word_idx = word_to_idx[word_input]
word_vec = vectors[word_idx]

dist_vec = np.zeros(len(words))
dist_idx = 0

for vec in vectors:
    disp_vec = vec - word_vec
    dist = np.linalg.norm(disp_vec)
    dist_vec[dist_idx] = dist

    dist_idx += 1

smallest_idxs = np.argsort(dist_vec)[:num_outputs]

for i in range(1, num_outputs):
    curr_idx = smallest_idxs[i]
    word_output = words[curr_idx]

    print(word_output)