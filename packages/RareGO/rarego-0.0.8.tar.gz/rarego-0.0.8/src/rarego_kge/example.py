
#Load dataset
from rarego_kge import load_dataset1, load_dataset2

df1 = load_dataset1()
df2 = load_dataset2()



# disease drug repourposer 
from rarego_kge import DiseaseDrugRepurposer

# Instantiate and use the class
repurposer = DiseaseDrugRepurposer()



from rarego_kge import DrugRepurposer

# Instantiate and use the class
repurposer = DrugRepurposer()



from rarego_kge import FDARepurposer

# Instantiate and use the class
repurposer = FDARepurposer()


from rarego_kge import GeneFunctionRepurposer

# Instantiate and use the class
repurposer = GeneFunctionRepurposer()


# Grid search
from rarego_kge import grid_search

# Instantiate and use the class
repurposer = grid_search()

#config
from rarego_kge import config 

# Instantiate and use the class
config = config ()


#config
from rarego_kge import KnowledgeGraphEmbedding

# Instantiate and use the class
train = KnowledgeGraphEmbedding()



#config
from rarego_kge import data_process

# Instantiate and use the class
process_data = data_process()



















