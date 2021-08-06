import pandas as pd
import numpy as np
import math

class KNearestNeighbour:
    def train(self, data, input_cols, output_cols):
        self.trained_data = data
        self.input_cols = input_cols
        self.output_cols = output_cols

    def predict(self, k, inputs, discrete = False):

        pred_outputs = inputs

        outputs = []

        for input in inputs.iloc:
            # for each input we need to find all distances to the training set
            trained_outputs = self.trained_data[self.output_cols]
            distances = []

            # loop over training data
            for trained_data in self.trained_data.iloc:
                # separate trained data into inputs
                trained_input = trained_data[self.input_cols]

                # calculate distance based on the metric function
                temp_dist = metric(input.values, trained_input.values)

                # append distance to array
                distances.append(temp_dist)

            # append distance array to output dataframe
            trained_outputs['Distance'] = distances

            # sort outputs by distance
            trained_outputs = trained_outputs.sort_values('Distance', 0, ascending = True)

            # initialise output array
            temp_output = [0]*len(self.output_cols)

            # average each output one column at a time
            for i in range(0, len(self.output_cols)):
                for j in range(0, k):
                    delta_output = trained_outputs[self.output_cols].values[j]
                    temp_output[i] = temp_output[i] + delta_output[i]
                temp_output[i] = temp_output[i]/k

            # append outputs to a 2D array
            outputs.append(temp_output)

        # append outputs to original dataframe
        pred_outputs[self.output_cols] = outputs

        # output
        return pred_outputs



# Euclidean distance (TEMP)
def metric(x, y):
    if (len(x) != len(y)):
        print('Error in dimensions while calculating distances')

    distance = 0

    for i in range(0, len(x)):
        x_val = x[i]
        y_val = y[i]

        delta_dist = (x_val - y_val) ** 2
        distance = distance + delta_dist

    distance = math.sqrt(distance)

    return distance
