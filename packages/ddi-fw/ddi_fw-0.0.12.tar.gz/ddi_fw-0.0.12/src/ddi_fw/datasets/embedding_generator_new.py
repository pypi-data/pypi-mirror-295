# !pip install -U sentence-transformers

# from transformers import BertTokenizer,BertForPreTraining,BertModel
# from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
from nltk import sent_tokenize
import torch
from tqdm import tqdm


from collections import defaultdict
from functools import partial
from abc import ABC, abstractmethod
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer, util


class EmbeddingGenerator(ABC):

    def __init__(self):
        self.shape = None

    @abstractmethod
    def generate(self, text):
        pass

# https://github.com/huggingface/transformers/issues/1791
class PretrainedEmbeddingGenerator(EmbeddingGenerator):
    def __init__(self, model_name, split_text=True):
        self.model_name = model_name
        self.model = AutoModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.shape = self.model.get_input_embeddings().weight.shape
        self.split_text = split_text

    def generate(self, text):
        if self.split_text:
            sentences = sent_tokenize(text)
            output_embeddings = None
            for sentence in sentences:
                input_ids  = self.tokenizer.encode(sentence, return_tensors='pt', padding=True)
                if output_embeddings == None:
                    output_embeddings = self.model(input_ids).last_hidden_state.mean(dim=1)
                else:
                    output_embeddings += self.model(input_ids).last_hidden_state.mean(dim=1)
            if output_embeddings == None:
                output_embeddings = torch.empty((1,self.model.get_input_embeddings().weight.shape[1]))
        else:
            encoded_input = self.tokenizer(text, return_tensors='pt')
            input_ids = self.tokenizer.encode(text, add_special_tokens=True, max_length=self.tokenizer.model_max_length, return_tensors='pt')
            # input_ids  = encoded_input.input_ids[:self.tokenizer.model_max_length]
            output_embeddings = self.model(input_ids)
            # output_embeddings = self.model(**encoded_input)
            # sentence embedding
            output_embeddings = output_embeddings.last_hidden_state.mean(dim=1)
        return torch.flatten(output_embeddings).detach().numpy()


class LLMEmbeddingGenerator(EmbeddingGenerator):
    pass


class SBertEmbeddingGenerator(PretrainedEmbeddingGenerator):
    def __init__(self, model_name, split_text=True):
        self.model = SentenceTransformer(model_name)
        self.shape = self.model._modules['0'].get_word_embedding_dimension()
        self.split_text = split_text

    def generate(self, text):
        if text == None or type(text) != str:
            embeddings = None
        else:
            if self.split_text:
                sentences = sent_tokenize(text)
                embeddings = self.model.encode(sentences)
            else:
                embeddings = self.model.encode(text)
        return embeddings


# NOT modelden input size'ı anlama,
def create_embeddings_new(generator: EmbeddingGenerator, data, column, drop_column=True):
    column_embeddings_dict = defaultdict(lambda: np.zeros(generator.shape))
    for index, row in tqdm(data.iterrows()):
        # if index == 10:
        #   break
        text = data[column][index]
        embeddings = generator.generate(text)

    # TODO benzer olan ilacın embedding değerini vererek dene
        # embedding check none type
        if embeddings is None or len(embeddings) == 0:
            sum_of_embeddings = np.zeros(generator.shape)
        else:
            sum_of_embeddings = np.sum(embeddings, axis=0)
        # column_embeddings_dict[row['id']] = sum_of_embeddings.reshape(1, -1) # 2d
        column_embeddings_dict[row['id']] = sum_of_embeddings
        # data.iloc[index][column+'_embedding']=sum_of_embeddings

    data[column+'_embedding'] = pd.Series(column_embeddings_dict.values())
    if (drop_column):
        data.drop([column], axis=1, inplace=True)
    # data[column+'_embedding'] = [column_embeddings_dict[row['name']] for index, row in data.iterrows()]
    return column_embeddings_dict
