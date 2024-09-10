import numpy as np
from scipy.spatial.distance import pdist, squareform

# todo pd.unique kullan
def find_distinct_elements(frame):
    # y = set(pd.unique(frame))
    y = set()
    for x in frame:
        if x is not None:
            for k in x:
                #     if type(k) == list:
                #         for i in k:
                #             y.add(i)
                #     else:
                y.add(k)
    return y


def find_distinct_elements_count(frame):
    y = set()
    for x in frame:
        if x is not None:
            y.update(x)
    return len(y)


class SimilarityMatrixGenerator:
    def __init__(self):
        pass

    def create_jaccard_similarity_matrices_ex(self, array):
        jaccard_sim = 1 - pdist(array, metric='jaccard')
        jaccard_sim_matrix = squareform(jaccard_sim)
        return jaccard_sim_matrix

    # https://github.com/YifanDengWHU/DDIMDL/blob/master/DDIMDL.py , def Jaccard(matrix):
    def create_jaccard_similarity_matrices(self, matrix):
        matrix = np.mat(matrix)
        numerator = matrix * matrix.T
        denominator = np.ones(np.shape(matrix)) * matrix.T + \
            matrix * np.ones(np.shape(matrix.T)) - matrix * matrix.T
        matrix = numerator / denominator
        np.nan_to_num(matrix, nan=0.0)
        return matrix


class VectorGenerator:
    def __init__(self, df):
        self.df = df

    def generate_feature_vector(self, column):
        bit_vectors = []
        map = dict()
        idx = 0
        count = find_distinct_elements_count(self.df[column])
        print(f"find_distinct_elements_count bitti, boyut: {count}")
        for ind in self.df.index:
            e = self.df[column][ind]
            # vector = np.zeros(len(sorted_features))
            vector = np.zeros(count)
            if e is not None:
                for item in e:
                    if item in map:
                        vector[map[item]] = 1
                    else:
                        vector[idx]=1
                        map[item] = idx
                        idx += 1 
 
            bit_vectors.append(vector)
        print("array oluşturuldu")
        return np.array(bit_vectors)
    
    # def generate_feature_vector(self, column):
    #     bit_vectors = []
    #     distinct_feature = find_distinct_elements(self.df[column])
    #     sorted_features = sorted(distinct_feature)
    #     for ind in self.df.index:
    #         e = self.df[column][ind]
    #         vector = np.zeros(len(sorted_features))
    #         if e is not None:
    #             indexes = [i for i, x in enumerate(sorted_features) if x in e]
    #             np.put(vector, indexes, np.ones(len(indexes)))
    #         bit_vectors.append(vector)
    #     return bit_vectors

# bit_vectors ndarray olacak
    def generate_feature_vectors(self, columns):
        vectors = dict()
        for column in columns:
            bit_vectors = self.generate_feature_vector(column)
            vectors[column] = bit_vectors
        return vectors


# generate feature vector
# np.hstack

# https://www.datasciencelearner.com/how-to-create-an-array-of-bits-in-python/
#
