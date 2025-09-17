from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# =============================================
# Full disease database
# =============================================
DISEASE_DATA = {
    "covid-19": {
        "general_info": "COVID-19 is a contagious respiratory illness caused by the SARS-CoV-2 virus. It primarily affects the respiratory tract but can also involve multiple organ systems.",
        "symptoms": "Common symptoms include fever, dry cough, fatigue, loss of taste or smell, sore throat, and difficulty breathing. Some patients may experience muscle aches, headache, and gastrointestinal disturbances.",
        "prevention": "Practice frequent hand hygiene with soap or alcohol-based sanitizers, wear a well-fitted mask in crowded settings, maintain adequate physical distancing, ensure proper ventilation, and stay up-to-date with recommended vaccinations.",
        "treatment": "Mild cases are managed with rest, hydration, and symptomatic relief such as antipyretics. Severe cases may require oxygen therapy, antiviral agents, corticosteroids, or hospitalization under medical supervision.",
        "more_info": "COVID-19 continues to evolve with emerging variants; public health measures and vaccination remain the cornerstone of prevention.",
        "emergency_tips": "Seek immediate medical attention if experiencing severe shortness of breath, persistent chest pain, confusion, or bluish lips or face."
    },
    "malaria": {
        "general_info": "Malaria is a potentially life-threatening disease caused by Plasmodium parasites, transmitted to humans through the bites of infected Anopheles mosquitoes.",
        "symptoms": "Typical symptoms include recurrent high fever, chills, profuse sweating, headache, muscle aches, nausea, vomiting, and general malaise. Severe malaria can lead to anemia, organ dysfunction, or cerebral malaria.",
        "prevention": "Use insecticide-treated bed nets, indoor residual spraying, and personal protective measures such as repellents and appropriate clothing. Travelers to endemic regions should take recommended chemoprophylaxis.",
        "treatment": "Treatment is based on species, severity, and drug-resistance patterns. Common regimens include artemisinin-based combination therapies (ACTs) or other antimalarials as prescribed by a qualified healthcare professional.",
        "more_info": "Prompt diagnosis and early treatment are critical to prevent complications and reduce transmission.",
        "emergency_tips": "Seek urgent medical care if severe symptoms such as altered consciousness, persistent vomiting, jaundice, or respiratory distress develop."
    },
    "cholera": {
        "general_info": "Cholera is an acute, potentially severe diarrheal disease caused by ingestion of food or water contaminated with Vibrio cholerae bacteria.",
        "symptoms": "Hallmark symptoms include sudden onset of profuse watery diarrhea (often described as 'rice-water stools'), vomiting, rapid dehydration, and painful muscle cramps. Severe cases may lead to shock if untreated.",
        "prevention": "Ensure access to safe drinking water, maintain good hand hygiene, practice proper sanitation, and consume properly cooked food. Oral cholera vaccines provide additional protection in high-risk settings.",
        "treatment": "Immediate and aggressive rehydration with oral rehydration solution (ORS) or intravenous fluids is the mainstay. Antibiotics may be used in moderate to severe cases to shorten illness duration under medical guidance.",
        "more_info": "Rapid recognition and treatment are vital to reduce mortality. Community-level interventions to improve water, sanitation, and hygiene significantly lower transmission.",
        "emergency_tips": "Seek emergency care immediately if signs of severe dehydration occur, such as very low urine output, lethargy, sunken eyes, or rapid heartbeat."
    },
    "gastric problems": {
        "general_info": "Gastric problems encompass a range of conditions affecting the stomach and upper digestive tract, including gastritis, acid reflux, peptic ulcers, and functional dyspepsia.",
        "symptoms": "Common manifestations include abdominal pain or burning sensation, bloating, nausea, vomiting, early satiety, indigestion, and heartburn. Severe cases may present with bleeding (black stools or vomiting blood).",
        "prevention": "Maintain a balanced diet, avoid excessive alcohol, caffeine, spicy foods, and NSAIDs. Eat smaller frequent meals and manage stress. Quit smoking.",
        "treatment": "Management depends on cause: antacids or proton pump inhibitors for acid-related disorders, antibiotics for H. pylori infection, and lifestyle modification. Severe or persistent symptoms need gastroenterology review.",
        "more_info": "Timely evaluation helps prevent complications like ulcers or gastrointestinal bleeding. Endoscopy may be recommended for persistent or alarming symptoms.",
        "emergency_tips": "Seek immediate medical care if severe abdominal pain, vomiting blood, black/tarry stools, or unexplained weight loss occurs."
    },
    "uti": {
        "general_info": "Urinary tract infections (UTIs) are infections involving the bladder, urethra, or kidneys, most commonly caused by bacteria such as Escherichia coli.",
        "symptoms": "Typical symptoms include a burning sensation during urination, increased urinary frequency, urgency, cloudy or foul-smelling urine, and lower abdominal discomfort. In upper tract infections, fever, flank pain, and nausea may occur.",
        "prevention": "Maintain good personal hygiene, drink adequate fluids, empty the bladder regularly, especially after intercourse, and avoid unnecessary urinary catheters. Cranberry products may have a preventive role in recurrent cases.",
        "treatment": "Short courses of oral antibiotics are used for uncomplicated cases. Severe or complicated infections may require longer therapy or intravenous antibiotics. Pain relief with urinary analgesics may be prescribed.",
        "more_info": "Prompt treatment prevents progression to kidney infection (pyelonephritis). Recurrent UTIs warrant further evaluation for underlying causes.",
        "emergency_tips": "Seek urgent care if there is high fever, severe flank pain, vomiting, confusion, or signs of sepsis."
    },
    "chronic problems": {
        "general_info": "Chronic health problems refer to long-term conditions such as diabetes, hypertension, asthma, chronic kidney disease, or chronic obstructive pulmonary disease (COPD), which often require ongoing management.",
        "symptoms": "Symptoms vary by condition but may include fatigue, weight changes, persistent pain, shortness of breath, swelling, or functional limitations. Many chronic diseases are initially asymptomatic.",
        "prevention": "Adopt a healthy lifestyle with balanced nutrition, regular exercise, stress management, and avoidance of tobacco or harmful alcohol use. Screen for common chronic conditions as recommended.",
        "treatment": "Management typically involves a combination of medication adherence, lifestyle modification, regular monitoring, and specialist follow-up. Early intervention helps prevent complications.",
        "more_info": "Chronic conditions often coexist and require coordinated, multidisciplinary care to improve quality of life and outcomes.",
        "emergency_tips": "Seek immediate care if experiencing severe chest pain, sudden shortness of breath, altered mental status, or rapid worsening of a known chronic condition."
    },
    "migraine": {
        "general_info": "Migraine is a recurrent neurological disorder characterized by moderate to severe throbbing headaches, often accompanied by nausea, photophobia, or phonophobia. It may be preceded by sensory disturbances known as aura.",
        "symptoms": "Intense, pulsating headache usually on one side of the head, nausea, vomiting, sensitivity to light and sound, and sometimes visual disturbances or tingling sensations before onset.",
        "prevention": "Identify and avoid individual triggers such as certain foods, stress, irregular sleep, or hormonal changes. Maintain a consistent sleep and meal schedule, stay hydrated, and manage stress.",
        "treatment": "Acute attacks are treated with analgesics, NSAIDs, or triptans. Preventive medications such as beta-blockers, anticonvulsants, or CGRP inhibitors may be prescribed for frequent or severe attacks.",
        "more_info": "Lifestyle modifications and early use of medications during the headache onset improve outcomes. Neurological evaluation is recommended for atypical or worsening headaches.",
        "emergency_tips": "Seek immediate medical care if the headache is sudden and severe (‘thunderclap headache’), associated with fever, stiff neck, neurological deficits, or changes in consciousness."
    },
    "cancer": {
        "general_info": "Cancer refers to a group of diseases characterized by uncontrolled growth and spread of abnormal cells. It can arise in virtually any tissue or organ and may metastasize to distant sites.",
        "symptoms": "Symptoms vary widely depending on the organ involved but may include unexplained weight loss, fatigue, lumps or masses, persistent pain, abnormal bleeding, or chronic cough. Early stages may be asymptomatic.",
        "prevention": "Reduce risk by avoiding tobacco, limiting alcohol, maintaining a healthy weight, engaging in regular physical activity, consuming a balanced diet rich in fruits and vegetables, protecting against excessive sun exposure, and getting recommended vaccinations (HPV, Hepatitis B).",
        "treatment": "Management depends on cancer type and stage: may include surgery, chemotherapy, radiation therapy, immunotherapy, targeted therapy, or a combination. Supportive and palliative care are integral parts of treatment.",
        "more_info": "Regular screening and early detection significantly improve survival. Genetic counseling and testing may be indicated for high-risk individuals.",
        "emergency_tips": "Seek urgent care for severe pain, sudden bleeding, signs of obstruction, breathing difficulty, or rapid deterioration in health status."
    },
    "food allergy": {
        "general_info": "Food allergies are immune-mediated reactions to specific foods such as peanuts, tree nuts, shellfish, milk, eggs, soy, or wheat. Even small amounts can trigger symptoms.",
        "symptoms": "Symptoms may include itching or swelling of lips and tongue, hives, abdominal pain, nausea, vomiting, diarrhea, and in severe cases anaphylaxis with breathing difficulty or shock.",
        "prevention": "Strictly avoid known trigger foods. Read ingredient labels carefully and inform restaurants about allergies. Carry an epinephrine auto-injector if at risk of severe reactions.",
        "treatment": "Mild reactions may be treated with oral antihistamines. Severe reactions require prompt administration of epinephrine and emergency care.",
        "more_info": "Food allergies can appear at any age and may coexist with asthma or eczema. Regular follow-up with an allergist is advised.",
        "emergency_tips": "Seek immediate medical care if throat tightness, shortness of breath, or rapid onset of widespread hives occurs."
    },
    "drug allergy": {
        "general_info": "Drug allergies occur when the immune system reacts abnormally to a medication such as antibiotics (penicillin), NSAIDs, or anticonvulsants.",
        "symptoms": "Symptoms range from mild rashes and itching to swelling, wheezing, and severe anaphylaxis. Some reactions may occur days after exposure (delayed hypersensitivity).",
        "prevention": "Inform all healthcare providers of any known drug allergies. Wear a medical alert bracelet and avoid self-medication without advice.",
        "treatment": "Discontinue the offending drug under medical supervision. Mild reactions may need antihistamines; severe reactions require epinephrine and supportive care.",
        "more_info": "Confirming drug allergy with allergy testing or graded challenge under specialist supervision helps prevent unnecessary drug avoidance.",
        "emergency_tips": "Seek emergency care immediately if experiencing difficulty breathing, facial swelling, or signs of anaphylaxis after taking a medication."
    },
    "pollen allergy": {
        "general_info": "Pollen allergy, also known as hay fever or seasonal allergic rhinitis, is triggered by airborne pollen from grasses, trees, or weeds.",
        "symptoms": "Sneezing, runny or blocked nose, itchy eyes, watery eyes, nasal congestion, and sometimes wheezing or cough.",
        "prevention": "Keep windows closed during high pollen seasons, use air purifiers, shower after outdoor exposure, and wear sunglasses or masks outside.",
        "treatment": "Oral antihistamines, intranasal corticosteroid sprays, and allergen immunotherapy for persistent or severe cases.",
        "more_info": "Pollen counts vary seasonally; tracking local forecasts can help minimize exposure.",
        "emergency_tips": "Seek immediate care if severe asthma-like symptoms or breathing difficulties develop during pollen exposure."
    },
    "dust allergy": {
        "general_info": "Dust allergy is typically caused by hypersensitivity to dust mites, microscopic organisms living in household dust, or to other indoor particles.",
        "symptoms": "Sneezing, runny nose, nasal congestion, itchy or watery eyes, coughing, wheezing, and occasionally eczema flare-ups.",
        "prevention": "Reduce dust exposure by using high-efficiency particulate air (HEPA) filters, washing bedding in hot water weekly, using dust-mite-proof covers, and minimizing carpets.",
        "treatment": "Antihistamines, nasal corticosteroids, and allergen immunotherapy may be recommended by an allergist.",
        "more_info": "Symptoms may worsen in humid environments or during cleaning. Consistent environmental control measures improve outcomes.",
        "emergency_tips": "Seek urgent care if severe shortness of breath or asthma attack occurs."
    },
    "insect allergy": {
        "general_info": "Insect allergies arise from stings or bites from bees, wasps, hornets, ants, or other insects, triggering immune reactions.",
        "symptoms": "Pain, redness, swelling at sting site; in sensitive individuals, generalized hives, swelling of lips or tongue, wheezing, and anaphylaxis.",
        "prevention": "Avoid walking barefoot outdoors, wear protective clothing, do not disturb insect nests, and carry an epinephrine auto-injector if allergic.",
        "treatment": "Mild local reactions may respond to cold compresses and oral antihistamines. Severe reactions require epinephrine and emergency care.",
        "more_info": "Allergen immunotherapy (venom immunotherapy) is highly effective for preventing severe reactions in insect-sting allergy.",
        "emergency_tips": "Seek emergency medical attention immediately if generalized hives, difficulty breathing, or dizziness occurs after a sting or bite."
    },
    "skin contact allergy": {
        "general_info": "Skin contact allergies (contact dermatitis) occur when the skin reacts to allergens such as nickel, fragrances, latex, or certain chemicals.",
        "symptoms": "Redness, itching, rash, blisters, or dry, scaly patches at the site of contact. Symptoms may appear hours or days after exposure.",
        "prevention": "Avoid known irritants and allergens, wear protective gloves or clothing, and choose hypoallergenic personal-care products.",
        "treatment": "Topical corticosteroids and oral antihistamines can reduce itching and inflammation. Severe or persistent cases may need dermatology consultation.",
        "more_info": "Patch testing by a dermatologist can identify specific allergens responsible for contact dermatitis.",
        "emergency_tips": "Seek medical care if rash spreads rapidly, becomes infected, or is accompanied by swelling of the face or breathing difficulty."
    }
}

# =============================================
# Action class
# =============================================
class ActionProvideDiseaseInfo(Action):
    def name(self) -> Text:
        return "action_provide_disease_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:


        disease = tracker.get_slot("disease")
        last_intent = tracker.latest_message.get("intent", {}).get("name")

        #  Handle greetings
        if last_intent == "greet":
            dispatcher.utter_message(text="Hi! I’m your health assistant. Please tell me what disease you’d like to know about.")
            return []

        #  Handle goodbye separately
        if last_intent == "goodbye":
            dispatcher.utter_message(text="Goodbye! Take care.")
            return []

        if not disease:
            dispatcher.utter_message(text="Please specify a disease name.")
            return []

        disease_lower = disease.lower()
        

        # Unknown disease
        if disease_lower not in DISEASE_DATA:
            dispatcher.utter_message(
                text=f"I don’t yet have detailed info about {disease.capitalize()}. "
                     f"You can ask me about symptoms, prevention, treatment, or more info of other diseases I know."
            )
            return []

        disease_info = DISEASE_DATA[disease_lower]

        # Respond based on intent
        if last_intent == "ask_symptoms":
            dispatcher.utter_message(
                text=f"Symptoms of {disease.capitalize()}: {disease_info['symptoms']}"
            )
        elif last_intent == "ask_prevention":
            dispatcher.utter_message(
                text=f"Prevention tips for {disease.capitalize()}: {disease_info['prevention']}"
            )
        elif last_intent == "ask_treatment":
            dispatcher.utter_message(
                text=f"Treatment for {disease.capitalize()}: {disease_info['treatment']}"
            )
        elif last_intent == "ask_more_info":
            dispatcher.utter_message(
                text=f"More info about {disease.capitalize()}: {disease_info['more_info']}"
            )
        elif last_intent == "emergency_tips":
            dispatcher.utter_message(
                text=f"Emergency tips for {disease.capitalize()}: {disease_info['emergency_tips']}"
            )
        elif last_intent == "affirm":
            dispatcher.utter_message(text="Great! What would you like to know more about this disease?")
        elif last_intent == "deny":
            dispatcher.utter_message(text="Okay, thanks for chatting!")
        else:
            dispatcher.utter_message(
                text=f"{disease_info['general_info']}\n\nWould you like to know more about this disease?"
            )

        return []
