# -*- coding: utf-8 -*-

import pandas as pd
import torch
from pykeen import predict

class DiseaseDrugRepurposer:
    def __init__(self, model_path, model2_path):
        """
        Initialize the DiseaseDrugRepurposer class.

        Parameters:
        - model_path (str): Path to the pre-trained embedding model.
        - model2_path (str): Path to the pre-trained knowledge graph model training data.
        """
        self.model = torch.load(model_path)
        self.model2 = torch.load(model2_path)

    def repurpose_by_disease_id(self, disease_id=['D010051'], relation="DRUG_DISEASE_ASSOCIATION"):
        """
        Repurpose drugs for given disease IDs.

        Parameters:
        - disease_id (list of str, optional): List of disease IDs for which drug repurposing is to be performed.
                                              Default is ['D010051'].
        - relation (str, optional): The relation type between drugs and diseases in the knowledge graph.
                                    Default is "DRUG_DISEASE_ASSOCIATION".

        Returns:
        - pandas.DataFrame: A DataFrame containing predicted drug-disease associations for the given disease IDs.
                            The DataFrame has columns ['head', 'relation', 'tail', 'score'] where
                            'head' represents the drug, 'tail' represents the disease ID,
                            'relation' represents the relation between drug and disease,
                            and 'score' represents the confidence score of the association.
        """
        disease_drug = []
        for tid in disease_id:
            drugs = predict.predict_target(model=self.model, tail=tid, relation=relation, triples_factory=self.model2).df 
            disease_drug.append(drugs)
        return pd.concat(disease_drug)

    def main(self):
        # Repurpose drugs for given disease IDs
        disease_drug = self.repurpose_by_disease_id()
        print(disease_drug)
        # Save results to CSV
        disease_drug.to_csv('example2.tsv', index=False, sep='\t')

if __name__ == "__main__":
    repurposer = DiseaseDrugRepurposer('C:/Users/bpatton23/Downloads/Drugrepurposing (1)/Drugrepurposing/complex_model_gene/trained_model.pkl',
                                'C:/Users/bpatton23/Downloads/Drugrepurposing (1)/Drugrepurposing/complex_model_gene/complex_training5')
    repurposer.main()
