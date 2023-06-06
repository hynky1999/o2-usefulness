from typing import List
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
import numpy as np
import scipy.sparse as sp


def parse_sparse(sparse_dict):
    return sp.csr_matrix((sparse_dict['values'], sparse_dict['indices'], [0, len(sparse_dict['indices'])]), shape=(1, sparse_dict['size']))

def explode_tfidf(df):
    # get first column of the df (the tfidf column)
    rows = df.iloc[:, 0].values

    sparse_rows = [parse_sparse(row) for row in rows]

    # concatenate the sparse rows
    return sp.vstack(sparse_rows)



def create_preprocessor(num_features: List[str], categorical: List[str], tfidf: List[str], normalize=True):

    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())])

    if not normalize:
        numeric_transformer = "passthrough"

    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    vector_transformer = Pipeline(steps=[
        ('numpify', FunctionTransformer(explode_tfidf, validate=False))])


    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_features),
            ('cat', categorical_transformer, categorical),
            ('tfidf', vector_transformer, tfidf)], remainder="drop")
    return preprocessor