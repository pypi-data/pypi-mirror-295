# -*- coding: utf-8 -*-
"""
Created on Thu May  9 21:52:31 2024

@author: bpatton23
"""
import pandas as pd
import torch
from pykeen import predict 


import pandas as pd
import torch
from pykeen import predict

class GeneFunctionRepurposer:
    def __init__(self, model_path, model2_path):
        """
        Initialize the GeneFunctionRepurposer class.

        Parameters:
        - model_path (str): Path to the pre-trained embedding model.
        - model2_path (str): Path to the pre-trained knowledge graph model training data.
        """
        self.model = torch.load(model_path)
        self.model2 = torch.load(model2_path)

    def repurpose_by_gene_ids(self, targets=['Q14865'], relation="GO_MF"):
        """
        Repurpose GeneID for given protein ID.

        Parameters:
        - targets (list of str, optional): A single protein ID for which protein function prediction is to be performed.
                                           Default is ['Q14865'] for leukemia.
        - relation (str, optional): The relation type between protein and gene ontology molecular function terms in the knowledge graph.
                                    Default is "GO_MF".

        Returns:
        - pandas.DataFrame: A DataFrame containing predicted molecular function for the given protein ID.
                            The DataFrame has columns ['head', 'relation', 'tail', 'score'] where
                            'head' represents the protein, 'tail' represents the Gene ID,
                            'relation' represents the relation between protein and gene ID,
                            and 'score' represents the confidence score of the association.
        """
        drug_list = []
        for hid in targets:
            drugs = predict.predict_target(model=self.model, head=hid, relation=relation, triples_factory=self.model2).df 
            drug_list.append(drugs)
        return pd.concat(drug_list)

    def repurpose_by_gene_ids_bp(self, targets=['Q14865'], relation="GO_BP"):
        """
        Repurpose GeneID for given protein ID.

        Parameters:
        - targets (list of str, optional): A single protein ID for which protein function prediction is to be performed.
                                           Default is ['Q14865'] for leukemia.
        - relation (str, optional): The relation type between protein and gene ontology Biological processes terms in the knowledge graph.
                                    Default is "GO_BP".

        Returns:
        - pandas.DataFrame: A DataFrame containing predicted Gene biological processes for the given protein ID.
                            The DataFrame has columns ['head', 'relation', 'tail', 'score'] where
                            'head' represents the protein, 'tail' represents the Gene ID,
                            'relation' represents the relation between protein and gene ID,
                            and 'score' represents the confidence score of the association.
        """
        drug_list = []
        for hid in targets:
            drugs = predict.predict_target(model=self.model, head=hid, relation=relation, triples_factory=self.model2).df 
            drug_list.append(drugs)
        return pd.concat(drug_list)

    def repurpose_by_gene_ids_cc(self, targets=['Q14865'], relation="GO_CC"):
        """
        Repurpose GeneID for given protein ID.

        Parameters:
        - targets (list of str, optional): A single protein ID for which protein function prediction is to be performed.
                                           Default is ['Q14865'] for leukemia.
        - relation (str, optional): The relation type between protein and gene ontology cellular components terms in the knowledge graph.
                                    Default is "GO_CC".

        Returns:
        - pandas.DataFrame: A DataFrame containing predicted cellular components for the given protein ID.
                            The DataFrame has columns ['head', 'relation', 'tail', 'score'] where
                            'head' represents the protein, 'tail' represents the Gene ID,
                            'relation' represents the relation between protein and gene ID,
                            and 'score' represents the confidence score of the association.
        """
        drug_list = []
        for hid in targets:
            drugs = predict.predict_target(model=self.model, head=hid, relation=relation, triples_factory=self.model2).df 
            drug_list.append(drugs)
        return pd.concat(drug_list)

    def main(self):
        # Predict GenID for given protein ID
        gene = self.repurpose_by_gene_ids()
        gene_bp = self.repurpose_by_gene_ids_bp()
        gene_cc = self.repurpose_by_gene_ids_cc()
        print(gene)
        print(gene_bp)
        print(gene_cc)
        # Save results to CSV
        gene.to_csv('Gene_IDMF_lukemia.tsv', index=False, sep='\t')
        gene_bp.to_csv('Gene_IDBP_lukemia.tsv', index=False, sep='\t')
        gene_cc.to_csv('Gene_IDCC_lukemia.tsv', index=False, sep='\t')

if __name__ == "__main__":
    repurposer = GeneFunctionRepurposer('C:/Users/bpatton23/Downloads/Drugrepurposing/complex_model_gene/trained_model.pkl',
                                         'C:/Users/bpatton23/Downloads/Drugrepurposing/complex_model_gene/complex_training5')
    repurposer.main()









