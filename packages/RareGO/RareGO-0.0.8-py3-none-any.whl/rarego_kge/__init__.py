import os
import pandas as pd

# Define the path to the data directory
data_dir = os.path.join(os.path.dirname(__file__), 'data')

# Function to load dataset1
def load_R25KG_Rare():
    dataset1_path = os.path.join(data_dir, 'R25KG-Rare.csv')
    return pd.read_csv(dataset1_path)

# Function to load dataset2
def load_R25KG_Rare_Gene():
    dataset2_path = os.path.join(data_dir, 'R25KG-Rare-Gene.csv')
    return pd.read_csv(dataset2_path)


# Load each dataset
from .data import load_R25KG_Rare, load_R25KG_Rare_Gene

# Load the datasets
#dataset1 = load_R25KG_Rare()
#dataset2 = load_R25KG_Rare_Gene()


from .repurpose_by_disease_id import DiseaseDrugRepurposer
from .repurpose_by_drug_ids import DrugRepurposer
from .repurpose_by_fda_drug_names import FDARepurposer
from .repurpose_by_gene_ids import GeneFunctionRepurposer
from .gridsearch import grid_search
from .config import config 
from .KGEtrainclass import KnowledgeGraphEmbedding
from .kgio import data_process
