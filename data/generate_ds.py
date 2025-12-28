import pandas as pd
import random

random.seed(42)

# ------------------------
# Expanded topics (MORE TOPICS)
# ------------------------
topics = {
    "AI/ML": [
        "Machine learning enables computers to learn patterns from data.",
        "Deep learning models are effective for text classification tasks.",
        "Neural networks consist of layers of interconnected neurons.",
        "Supervised learning requires labeled training data.",
        "Artificial intelligence automates complex decision making."
    ],
    "NLP": [
        "Natural language processing allows machines to understand human language.",
        "Text similarity techniques compare documents for shared meaning.",
        "Named entity recognition identifies entities in text.",
        "Machine translation converts text between languages.",
        "Information retrieval systems find relevant documents."
    ],
    "Science": [
        "Photosynthesis allows plants to produce their own food.",
        "The water cycle helps regulate Earth's climate.",
        "Gravity attracts objects toward the Earth's center.",
        "Energy cannot be created or destroyed.",
        "Atoms consist of protons, neutrons, and electrons."
    ],
    "History": [
        "The French Revolution began in the late eighteenth century.",
        "World War II ended in 1945 after global conflict.",
        "The Industrial Revolution transformed European economies.",
        "Ancient civilizations developed early writing systems.",
        "Colonialism reshaped global political structures."
    ],
    "Sports": [
        "Football is one of the most popular sports worldwide.",
        "Basketball games are divided into four quarters.",
        "The Olympics are held every four years.",
        "Tennis matches are played on different court surfaces.",
        "Athletes train rigorously to improve performance."
    ],
    "Health": [
        "Vaccination helps prevent infectious diseases.",
        "Regular exercise improves cardiovascular health.",
        "A balanced diet supports proper nutrition.",
        "Mental health is essential for overall well-being.",
        "Sleep is critical for physical recovery."
    ],
    "Environment": [
        "Climate change leads to rising sea levels.",
        "Deforestation negatively impacts biodiversity.",
        "Recycling reduces waste and conserves resources.",
        "Renewable energy reduces carbon emissions.",
        "Pollution affects air and water quality."
    ],
    "Technology": [
        "Blockchain enables secure digital transactions.",
        "Cloud computing allows remote data storage.",
        "Cybersecurity protects systems from cyber attacks.",
        "The Internet connects devices globally.",
        "Artificial intelligence improves automation."
    ],
    "Economics": [
        "Inflation reduces purchasing power over time.",
        "Supply and demand determine market prices.",
        "Gross Domestic Product measures economic output.",
        "Unemployment affects economic growth.",
        "Fiscal policy influences national economies."
    ],
    "Education": [
        "Online learning increases access to education.",
        "Teachers assess student performance regularly.",
        "Curriculum design impacts learning outcomes.",
        "Higher education prepares students for careers.",
        "Examinations evaluate academic achievement."
    ]
}

# ------------------------
# Multiple paraphrases per sentence
# ------------------------
paraphrases = {
    s: [
        f"{s.split('.')[0]} using modern approaches.",
        f"{s.split('.')[0]} through advanced techniques.",
        f"{s.split('.')[0]} in real-world applications."
    ]
    for sentences in topics.values()
    for s in sentences
}

# ------------------------
# Easy unrelated negatives
# ------------------------
unrelated_sentences = [
    "Mount Everest is the tallest mountain on Earth.",
    "The solar system contains eight planets.",
    "Oceans cover most of the Earth's surface.",
    "Cooking pasta requires boiling water.",
    "Music strongly influences emotions.",
    "Birds migrate during seasonal changes.",
    "The moon orbits the Earth."
]

# ------------------------
# Utility function
# ------------------------
def is_safe_negative(a, b):
    overlap = set(a.lower().split()) & set(b.lower().split())
    return len(overlap) < 2

# ------------------------
# Generate dataset
# ------------------------
rows = []
samples_per_sentence = 30

for topic, sentences in topics.items():
    for orig in sentences:
        
        # Positive samples
        for _ in range(samples_per_sentence):
            rows.append([orig, random.choice(paraphrases[orig]), 1])
        
        # Hard negatives (same topic)
        hard_negs = [s for s in sentences if s != orig]
        for _ in range(samples_per_sentence // 2):
            rows.append([orig, random.choice(hard_negs), 0])
        
        # Easy negatives (unrelated)
        for _ in range(samples_per_sentence // 2):
            neg = random.choice(unrelated_sentences)
            while not is_safe_negative(orig, neg):
                neg = random.choice(unrelated_sentences)
            rows.append([orig, neg, 0])

# ------------------------
# Create DataFrame
# ------------------------
df = pd.DataFrame(rows, columns=["text1", "text2", "label"])
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv("plagiarism_dataset.csv", index=False)

print("✅ Dataset with more topics created!")
print(f"Total samples: {len(df)}")