import pykeen
from pykeen.triples import TriplesFactory
from pykeen.datasets import PathDataset



#print(torch.cuda.is_available())


def triple_factory_from_csv(csvpath):
    return TriplesFactory.from_path(csvpath, create_inverse_triples=False)

"""
Saving dataset as triples factory

Args:
    csvpath(str) : the file path of the dataset

Returns:
    triples factory dataset from csv path.
    create_inverse_triples(str): Either true or False the default is False
    
"""

def pykeen_dataset_from_csv(csvpath):
    return PathDataset.from_path(csvpath)

"""
Loading own dataset for grid search process

Args:
    csvpath(str) : the file path of the dataset
Returns:
      Pathset dataset from csv path.  
"""

def train_test_val_split_from_csv(csvpath, splits_ratio=[0.8, 0.1, 0.1]):
    kg=triple_factory_from_csv(csvpath)
    train, test, val=kg.split(splits_ratio)
    return train, test, val

"""
The splitting process of dataset for training

Args:
    csvpath(str) : the file path of the dataset
    splits_ratio: The splitting of 80,10,10 which is default.
Returns:
      test, train, val sets.  
"""

def data_process(csvpath, splits_ratio=[0.8, 0.1, 0.1]):
    # Load the dataset as a TriplesFactory
    triples_factory = triple_factory_from_csv(csvpath)
    
    # Load the dataset for grid search
    dataset = pykeen_dataset_from_csv(csvpath)
    
    # Split the dataset
    train, test, val = train_test_val_split_from_csv(csvpath, splits_ratio)
    
    return triples_factory, dataset, train, test, val





