import pandas as pd
from neo4j import GraphDatabase


if __name__ == '__main__':
	files = ['data/negative_triplets.txt', 'data/positive_triplets.txt', 'data/neutral_triplets.txt']
	
	driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "root"))

	session = driver.session()
	words = {}

	for file in files:
		df = pd.read_csv(file, names=['src', 'predicate', 'dst'])
		nodes = df['src'].unique().tolist()
		
		for node in nodes:
			if node not in words:
				words[node] = len(words)
		
		for row in df.itertuples():
			_, src, predicate, dst = row
			src_id = words[src]
			dst_id = words[dst]
			
			session.run("MERGE (a:Concept { id: $id, value: $value }) ", id=src_id, value=src)
			
			session.run("MERGE (a:Concept { id: $id, value: $value })", id=dst_id, value=dst)

			session.run("MATCH (a:Concept), (b:Concept) "
					"WHERE a.id = $src AND b.id = $dst "
					f"MERGE (a)-[r:{predicate}]-(b) "
					"RETURN type(r)", src=src_id, dst=dst_id)
			