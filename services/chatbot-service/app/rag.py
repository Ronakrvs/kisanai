import re
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Keyword-based rule engine — works with zero ML models, ~10MB RAM
# ---------------------------------------------------------------------------

RULES_HI = [
    (r"पील|पील|yellow|yelow", "पत्तियों का पीला होना नाइट्रोजन की कमी, जल-जमाव या रोग का संकेत है। यूरिया का छिड़काव (2%) करें और जल निकासी सुनिश्चित करें।"),
    (r"सिंचाई|पानी|water|irrigat", "सिंचाई सुबह या शाम करें। धान को 5-7 सेमी पानी, गेहूं को 20-25 दिन में एक बार, और सब्जियों को हर 3-4 दिन में पानी दें।"),
    (r"खाद|उर्वरक|fertilizer|npk|urea|यूरिया", "फसल के अनुसार खाद दें: गेहूं (N:P:K = 120:60:40 kg/ha), धान (100:50:50), सब्जी (80:40:40)। DAP और यूरिया को बोनी के समय और बाद में दें।"),
    (r"कीट|pest|insect|कीटनाशक|pesticide", "कीट नियंत्रण के लिए नीम का तेल (5 ml/L) या क्लोरपाइरीफॉस का उपयोग करें। जैविक खेती में ट्राइकोडर्मा प्रभावी है।"),
    (r"ब्लाइट|blight|झुलसा|जलन", "ब्लाइट के लिए मैंकोजेब (2.5 g/L) या कॉपर ऑक्सीक्लोराइड का छिड़काव करें। रोगग्रस्त पत्तियां तुरंत हटाएं।"),
    (r"धान|rice|paddy|चावल", "धान की रोपाई जून-जुलाई में करें। जल स्तर 5 सेमी बनाए रखें। DAP + यूरिया का उपयोग करें। कटाई 110-120 दिन में।"),
    (r"गेहूं|wheat", "गेहूं की बुवाई नवंबर में करें। 6 सिंचाई दें (बुवाई, जुताई, जड़, पुष्पन, दाना भरना, पकाव)। MSP 2024-25: ₹2,275/क्विंटल।"),
    (r"टमाटर|tomato", "टमाटर में करपा रोग से बचाव के लिए मैंकोजेब डालें। ड्रिप सिंचाई उत्तम है। फल छेदक के लिए स्पिनोसेड का उपयोग करें।"),
    (r"मक्का|maize|corn|मकई", "मक्का की बुवाई जून में करें। नाइट्रोजन 3 बार में दें (बुवाई, घुटना ऊंचाई, तसेलिंग)। फॉल आर्मीवर्म के लिए इमामेक्टिन बेंजोएट।"),
    (r"सोयाबीन|soybean|soya", "सोयाबीन जुलाई में बोएं। राइजोबियम टीका से 20% अधिक उपज। पीला मोजेक के लिए व्हाइटफ्लाई नियंत्रण जरूरी।"),
    (r"मौसम|बारिश|weather|rain|monsoon|वर्षा", "मानसून जून-सितंबर। खरीफ फसल (धान, मक्का, सोयाबीन) इसी में। अत्यधिक वर्षा में जल निकासी और कम वर्षा में ड्रिप सिंचाई अपनाएं।"),
    (r"soil|मिट्टी|भूमि|ph", "मृदा pH 6-7 आदर्श है। अम्लीय मिट्टी में चूना (2 t/ha) और क्षारीय में जिप्सम डालें। जैविक खाद से मिट्टी की संरचना सुधारें।"),
    (r"जैविक|organic|प्राकृतिक|natural farming", "जैविक खेती में गोबर की खाद (10 t/ha), वर्मीकम्पोस्ट, जीवामृत और नीम का उपयोग करें। ZBNF (सुभाष पालेकर विधि) अपनाएं।"),
    (r"फसल बीमा|insurance|प्रधानमंत्री|pmfby", "PMFBY (प्रधानमंत्री फसल बीमा योजना) से फसल सुरक्षा होती है। प्रीमियम खरीफ 2%, रबी 1.5%। नजदीकी बैंक या CSC से आवेदन करें।"),
    (r"msp|minimum support|न्यूनतम समर्थन", "2024-25 MSP: गेहूं ₹2,275, धान ₹2,300, सोयाबीन ₹4,892, मक्का ₹2,225, कपास ₹7,121 प्रति क्विंटल।"),
]

RULES_EN = [
    (r"yellow|pale|chlorosis", "Yellow leaves often indicate nitrogen deficiency, waterlogging, or disease. Apply 2% urea foliar spray and ensure proper drainage."),
    (r"irrigat|water|drip", "Irrigate early morning or evening. Rice needs 5-7cm water depth; wheat every 20-25 days; vegetables every 3-4 days. Drip irrigation saves 40% water."),
    (r"fertilizer|npk|urea|manure|compost", "Crop-wise NPK (kg/ha): Wheat (120:60:40), Rice (100:50:50), Vegetables (80:40:40). Split nitrogen into 3 doses for best results."),
    (r"pest|insect|bug|aphid|thrip", "For pest control use neem oil (5ml/L water) or chlorpyrifos. Sticky yellow traps for whiteflies. Biological control with Trichoderma/Bacillus."),
    (r"blight|fungus|fungal|rust|mold|rot", "For blight/fungal diseases spray Mancozeb (2.5g/L) or copper oxychloride. Remove infected leaves immediately to stop spread."),
    (r"rice|paddy|wheat|crop recommend", "Rice: transplant June-July, harvest in 110-120 days. Wheat: sow November, 6 irrigations needed. Both respond well to DAP + Urea combination."),
    (r"tomato|potato|onion|vegetable", "Vegetables need balanced nutrition. Tomato: stake plants, control fruit borer with Spinosad. Potato: hilling essential. Onion: stop irrigation 10 days before harvest."),
    (r"organic|natural|bio|vermi", "Organic farming: use FYM 10 t/ha, vermicompost, Jeevamrit, and neem cake. ZBNF method (Subhash Palekar) is very effective and low-cost."),
    (r"soil|ph|sandy|clay|loamy", "Ideal soil pH 6-7. Add lime for acidic soil, gypsum for alkaline. Organic matter improves all soil types. Get soil tested every 3 years."),
    (r"weather|rain|monsoon|drought|flood", "Kharif season (June-Oct): rice, maize, soybean. Rabi (Nov-Mar): wheat, mustard. Climate-smart varieties help manage erratic rainfall."),
    (r"insurance|pmfby|subsidy|scheme|government", "PMFBY crop insurance: 2% premium for kharif, 1.5% for rabi. Apply at nearest bank or CSC center. PM-KISAN gives ₹6,000/year to eligible farmers."),
    (r"msp|minimum support price|market", "2024-25 MSP: Wheat ₹2,275, Paddy ₹2,300, Soybean ₹4,892, Maize ₹2,225, Cotton ₹7,121 per quintal."),
    (r"storage|store|warehouse|silo", "Store grains at <14% moisture. Use hermetic bags or PAU bins. Treat with Celphos tablets for rodent/pest control. Avoid storing near moisture sources."),
    (r"loan|credit|kcc|kisan credit", "Kisan Credit Card (KCC) gives crop loans at 4-7% interest. Apply at any cooperative/nationalized bank with land records and Aadhaar."),
]

FALLBACK_HI = (
    "आपका प्रश्न समझ आया। अधिक जानकारी के लिए कृपया:\n"
    "• KVK (कृषि विज्ञान केंद्र) से संपर्क करें\n"
    "• किसान कॉल सेंटर: 1800-180-1551 (निःशुल्क)\n"
    "• अपनी फसल की जानकारी के लिए ऊपर दिए टूल्स (रोग पहचान, खाद सलाह) का उपयोग करें।"
)

FALLBACK_EN = (
    "I understand your question. For more help:\n"
    "• Contact your local KVK (Krishi Vigyan Kendra)\n"
    "• Kisan Call Centre: 1800-180-1551 (free)\n"
    "• Use the Disease Detection and Fertilizer tools above for specific crop issues."
)


def keyword_answer(question: str, language: str) -> Optional[str]:
    q = question.lower()
    rules = RULES_HI if language == "hi" else RULES_EN
    for pattern, answer in rules:
        if re.search(pattern, q, re.IGNORECASE):
            return answer
    # Cross-check with the other language's patterns (bilingual questions)
    other = RULES_EN if language == "hi" else RULES_HI
    for pattern, _ in other:
        if re.search(pattern, q, re.IGNORECASE):
            rules_map = dict(RULES_HI if language == "hi" else RULES_EN)
            for p2, ans in rules:
                if re.search(p2, q, re.IGNORECASE):
                    return ans
    return None


# ---------------------------------------------------------------------------
# Optional: Groq API (free LLM) — only used if GROQ_API_KEY is set
# ---------------------------------------------------------------------------

async def groq_answer(question: str, language: str) -> Optional[str]:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    try:
        import httpx
        system = (
            "You are KisanAI, an expert agriculture assistant for Indian farmers. "
            + ("Answer in Hindi, be concise and practical." if language == "hi"
               else "Answer in English, be concise and practical.")
        )
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "model": "llama3-8b-8192",
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": question},
                    ],
                    "max_tokens": 300,
                    "temperature": 0.4,
                },
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.warning(f"Groq API failed: {e}")
    return None


async def answer(question: str, language: str = "hi") -> str:
    # 1. Try Groq LLM if available
    llm_resp = await groq_answer(question, language)
    if llm_resp:
        return llm_resp

    # 2. Fall back to keyword rules
    rule_resp = keyword_answer(question, language)
    if rule_resp:
        return rule_resp

    # 3. Generic fallback
    return FALLBACK_HI if language == "hi" else FALLBACK_EN
