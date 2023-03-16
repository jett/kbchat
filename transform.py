from datetime import datetime
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/gtr-t5-large")

texts = [
    """
    The Office of the City Mayor (OCM) enforces all laws and ordinances relative to the governance of the city and implements all approved policies, programs, projects, services, and activities of the city; initiates and maximizes the generation of sources and applies the same to the implementation of development plans, programs, objectives; and ensures the delivery of basic services and the provision of adequate facilities for the city.
    """,
    """
    The Office of the Vice Mayor shall be a model of servant leadership and good governance: serving God by serving others and changing the culture of traditional politics, in order to raise the economic self-sufficiency of strong families in Quezon City.
    """
]

print(datetime.now().isoformat())
embeddings = model.encode(texts)
print(datetime.now().isoformat())

print(embeddings)
