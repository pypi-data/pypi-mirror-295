# -*- coding: utf-8 -*-
"""
Created on Thu May  9 22:05:21 2024

@author: bpatton23
"""
import torch
from pykeen import predict
import pandas as pd

import pandas as pd
import torch
from pykeen import predict

class FDARepurposer:
    def __init__(self, model_path, model2_path):
        """
        Initialize the FDARepurposer class.

        Parameters:
        - model_path (str): Path to the pre-trained embedding model.
        - model2_path (str): Path to the pre-trained knowledge graph model training data.
        """
        self.model = torch.load(model_path)
        self.model2 = torch.load(model2_path)

    def repurpose_by_fda_drug_names(self, fda_drugs=['DB09052','DB05889','DB13881','DB08870','DB08901'], relation="DRUG_DISEASE_ASSOCIATION"):
        """
        Repurpose drugs for given drug IDs.

        Parameters:
        - fda_drugs (list of str, optional): List of drug IDs for which drug repurposing is to be performed.
                                              Default is ['DB09052','DB05889','DB13881','DB08870','DB08901'].
        - relation (str, optional): The relation type between drugs and diseases in the knowledge graph.
                                    Default is "DRUG_DISEASE_ASSOCIATION".

        Returns:
        - pandas.DataFrame: A DataFrame containing predicted drug-disease associations for the given drug IDs.
                            The DataFrame has columns ['head', 'relation', 'tail', 'score'] where
                            'head' represents the drug, 'tail' represents the disease ID,
                            'relation' represents the relation between drug and disease,
                            and 'score' represents the confidence score of the association.
        """
        drugs_fda = []
        for hid in fda_drugs:
            drugs = predict.predict_target(model=self.model, head=hid, relation=relation, triples_factory=self.model2).df 
            drugs_fda.append(drugs) 
        return pd.concat(drugs_fda)

    def main(self):
        # Repurpose drugs for given drug IDs
        fda_drugs = self.repurpose_by_fda_drug_names()
        print(fda_drugs)
        # Save results to CSV
        fda_drugs.to_csv('example3.tsv', index=False, sep='\t')

if __name__ == "__main__":
    repurposer = FDARepurposer('C:/Users/bpatton23/Downloads/Drugrepurposing (1)/Drugrepurposing/complex_model_gene/trained_model.pkl',
                                'C:/Users/bpatton23/Downloads/Drugrepurposing (1)/Drugrepurposing/complex_model_gene/complex_training5')
    repurposer.main()