"""
Seeds the knowledge base with agriculture documents.
Run once: python -m app.seed_knowledge
"""

import os
import psycopg2
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer

DOCUMENTS = [
    "पाउडरी मिल्ड्यू (Powdery Mildew) एक फफूंद रोग है जो पत्तियों पर सफेद पाउडर जैसे धब्बे बनाता है। "
    "उपचार: सल्फर आधारित फफूंदनाशक का छिड़काव करें।",

    "Tomato late blight is caused by Phytophthora infestans. It spreads rapidly in cool, wet weather. "
    "Treatment: Apply metalaxyl + mancozeb fungicide immediately.",

    "गेहूं में करनाल बंट रोग Tilletia indica फफूंद के कारण होता है। "
    "बचाव: प्रमाणित बीज का उपयोग करें। बुवाई से पहले बीजोपचार करें।",

    "Nitrogen deficiency in crops causes yellowing of lower leaves (chlorosis). "
    "Apply urea at 50 kg/hectare as a top dressing.",

    "धान की फसल में भूरा धब्बा रोग Helminthosporium oryzae के कारण होता है। "
    "उपचार: मैन्कोजेब 2.5 ग्राम प्रति लीटर पानी में घोलकर छिड़काव करें।",

    "Drip irrigation saves 30-50% water compared to flood irrigation. "
    "It is especially effective for vegetables, fruits and sugarcane.",

    "सिंचाई कब करें: मिट्टी में नमी कम होने पर, पत्तियां मुरझाने से पहले सिंचाई करें। "
    "सुबह या शाम को सिंचाई करना सबसे अच्छा है।",

    "Crop rotation helps break pest and disease cycles. "
    "Rotate cereals with legumes to improve soil nitrogen.",

    "जैविक खाद (Organic manure) जैसे गोबर की खाद, वर्मीकम्पोस्ट मिट्टी की उर्वरता बढ़ाती है। "
    "प्रति एकड़ 5-10 टन गोबर की खाद डालें।",

    "Potassium deficiency causes brown scorching of leaf margins and poor fruit quality. "
    "Apply MOP (Muriate of Potash) at 50 kg/hectare.",

    "PM Kisan Samman Nidhi: सभी किसानों को प्रति वर्ष ₹6000 तीन किश्तों में दिए जाते हैं। "
    "pmkisan.gov.in पर पंजीकरण करें।",

    "Soil pH between 6.0 and 7.0 is ideal for most crops. "
    "Apply lime to raise pH and sulfur to lower pH.",
]


def seed():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not set")
        return

    conn = psycopg2.connect(db_url)
    register_vector(conn)

    model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                embedding vector(384)
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS kb_embedding_idx ON knowledge_base USING ivfflat (embedding vector_cosine_ops)")

        for doc in DOCUMENTS:
            emb = model.encode(doc, normalize_embeddings=True).tolist()
            cur.execute(
                "INSERT INTO knowledge_base (content, embedding) VALUES (%s, %s)",
                (doc, emb),
            )

    conn.commit()
    conn.close()
    print(f"Seeded {len(DOCUMENTS)} documents into knowledge_base")


if __name__ == "__main__":
    seed()
