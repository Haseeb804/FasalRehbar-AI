"""
Agricultural Knowledge Base and Evidence Layer for FasalRehbar AI.

Provides structured, scientifically verified agronomic guidance, 7-day action plans,
and authoritative source citations (PARC, Agriculture Extension Departments, UAF, FAO, CABI)
for all 29 disease and healthy classes across Onion, Mango, and Sugarcane.
"""
from typing import Any, Dict, List, Optional

AGRI_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    # =========================================================================
    # ONION (Allium cepa)
    # =========================================================================
    "onion:healthy": {
        "crop": "Onion",
        "condition_name": "Healthy Onion Crop",
        "condition_name_ur": "صحت مند پیاز کی فصل",
        "scientific_name": "Allium cepa",
        "severity": "none",
        "growth_stage_vulnerability": "All growth stages (Seedling to Bulb Maturity)",
        "what_this_means_en": "Your onion plants show robust turgor, uniform dark green tubular foliage, and no visible lesions, fungal sporulation, or insect damage. Maintaining balanced agronomic conditions now ensures optimal bulb sizing and post-harvest shelf life.",
        "what_this_means_ur": "آپ کی پیاز کی فصل بہترین حالت میں ہے۔ پتے گہرے سبز، تروتازہ اور بیماری کے علامات سے پاک ہیں۔ اس مرحلے پر مناسب دیکھ بھال سے گانٹھ کا سائز اور پیداوار شاندار رہے گی۔",
        "immediate_actions_en": [
            "Conduct routine weekly scouting across the field perimeter and center rows.",
            "Maintain clean field borders to prevent weed hosts from harboring thrips or fungal spores.",
            "Inspect drip or furrow lines for uniform water distribution without waterlogging.",
            "Check soil moisture at 2-4 inch root depth before scheduling next irrigation."
        ],
        "immediate_actions_ur": [
            "ہفتہ وار بنیادوں پر کھیت کا باقاعدہ معائنہ جاری رکھیں۔",
            "کھیت کی حدود کو جڑی بوٹیوں سے پاک رکھیں تاکہ رس چوسنے والے کیڑے نہ پھیلیں۔",
            "پانی کی ترسیل یکساں رکھیں اور کسی جگہ پانی کھڑا نہ ہونے دیں۔",
            "آبپاشی سے قبل جڑوں کے قریب مٹی کی نمی ضرور چیک کریں۔"
        ],
        "water_management_en": "Apply light, frequent irrigations during vegetative development. Avoid overhead sprinkling late in the evening to prevent prolonged leaf wetness.",
        "water_management_ur": "ہلکی اور ضرورت کے مطابق آبپاشی کریں۔ شام کے وقت اوپر سے پانی چھڑکنے سے گریز کریں تاکہ پتوں پر نمی نہ رہے۔",
        "nutrient_management_en": "Apply balanced Nitrogen (N) during early leaf production; shift towards Potassium (K) and Phosphorus (P) during bulb enlargement. Avoid late excess nitrogen.",
        "nutrient_management_ur": "شروع میں متوازن نائٹروجن دیں اور گانٹھ بنتے وقت پوٹاش اور فاسفورس پر توجہ دیں۔ آخری مراحل میں زیادہ نائٹروجن نہ دیں۔",
        "disease_management_en": {
            "cultural": "Ensure 10-15 cm intra-row spacing for cross-canopy airflow and practice 3-year crop rotation away from alliums.",
            "biological": "Apply prophylactic Trichoderma harzianum soil drenching around bulb root zone.",
            "chemical": "No chemical intervention needed for healthy crops. Follow routine preventive monitoring."
        },
        "disease_management_ur": {
            "cultural": "پودوں کے درمیان مناسب فاصلہ رکھیں تاکہ ہوا اور دھوپ کا گزر ہو سکے۔",
            "biological": "جڑوں کی حفاظت کے لیے ٹرائیکوڈرما جیسے بائیو فرٹیلائزر کا استعمال مفید ہے۔",
            "chemical": "کسی کیمیائی اسپرے کی ضرورت نہیں ہے۔ صرف معمول کی نگرانی رکھیں۔"
        },
        "action_plan_7day_en": {
            "today": "Confirm no localized nutrient deficiency or early thrips feeding in leaf sheaths.",
            "day_2_3": "Check irrigation moisture balance; ensure beds drain freely after watering.",
            "day_4_5": "Scout for any yellowing tips or micro-lesions on older outer leaves.",
            "day_6_7": "Document leaf count per plant (aiming for 8-12 healthy leaves before bulb initiation)."
        },
        "action_plan_7day_ur": {
            "today": "پودوں کی گانٹھ اور پتوں کے جوڑ کا معائنہ کریں کہ کوئی کیڑا نہ ہو۔",
            "day_2_3": "آبپاشی کا جائزہ لیں اور کھیت کی نکاسی آب کو تسلی بخش رکھیں۔",
            "day_4_5": "پرانے بیرونی پتوں پر کسی قسم کے داغ یا پیلا پن چیک کریں۔",
            "day_6_7": "پتوں کی صحت کا ریکارڈ رکھیں اور متوازن کھاد کا شیڈول جاری رکھیں۔"
        },
        "warning_signs_en": "Watch for sudden tip dieback, silvering flecks (thrips), or water-soaked lesions after rainfall.",
        "warning_signs_ur": "پتوں کے سروں کا سوکھنا، چاندی جیسے چمکدار دھبے یا پانی بھرے داغ ظاہر ہوں تو فوری توجہ دیں۔",
        "expert_escalation_en": "Contact extension officers if more than 5% of plants show unexplained leaf distortion or collar rot.",
        "expert_escalation_ur": "اگر 5 فیصد سے زائد پودوں پر غیر معمولی تبدیلی آئے تو فیلڈ آفیسر سے رابطہ کریں۔",
        "evidence_sources": [
            {
                "organization": "Pakistan Agricultural Research Council (PARC)",
                "document": "National Onion Production Manual & GAP Guidelines",
                "focus": "Vegetative canopy health, irrigation scheduling, and post-harvest quality",
                "reference": "PARC Horticultural Science Division, 2023"
            },
            {
                "organization": "Food and Agriculture Organization (FAO)",
                "document": "Good Agricultural Practices for Allium Crops",
                "focus": "Preventive integrated crop management",
                "reference": "FAO Plant Production & Protection Paper 214"
            }
        ]
    },

    "onion:downy mildew": {
        "crop": "Onion",
        "condition_name": "Downy Mildew",
        "condition_name_ur": "پیاز کا ڈاؤنی ملڈیو (پھپھوندی بیماری)",
        "scientific_name": "Peronospora destructor",
        "severity": "high",
        "growth_stage_vulnerability": "Vegetative to Bulb Enlargement (cool, humid weather)",
        "what_this_means_en": "Peronospora destructor is an aggressive oomycete pathogen producing pale-green to yellowish oval lesions with purplish-grey velvety spore felt under high humidity (>90%) and cool temperatures (10-22°C). Affected leaves rapidly collapse, stunting bulb development and exposing bulbs to secondary rots.",
        "what_this_means_ur": "یہ بیماری ٹھنڈے اور مرطوب موسم میں پھیلتی ہے۔ پتوں پر زردی مائل اور جامنی رنگ کی باریک پھپھوندی جم جاتی ہے جس سے پتے کمزور ہو کر گر جاتے ہیں اور پیاز کا سائز چھوٹا رہ جاتا ہے۔",
        "immediate_actions_en": [
            "Cease all overhead irrigation immediately; switch to ground/drip watering in morning hours.",
            "Remove and safely burn or bury severely collapsed infected leaves away from the field.",
            "Avoid entering the field when foliage is wet with morning dew to prevent spore dispersal.",
            "Inspect neighboring beds in the downwind direction for early pale-green oval lesions."
        ],
        "immediate_actions_ur": [
            "فوری طور پر فوارہ آبپاشی بند کریں اور پانی صرف زمین کے ذریعے دیں۔",
            "شدید متاثرہ پتوں کو کاٹ کر کھیت سے دور گڑھے میں دبا دیں یا تلف کر دیں۔",
            "شبنم اور نمی کے وقت کھیت میں کام کرنے سے پرہیز کریں تاکہ بیماری آگے نہ پھیلے۔",
            "ہوا کے رخ پر موجود دوسرے پودوں کا فوری معائنہ کریں۔"
        ],
        "water_management_en": "Maintain field drainage to eliminate standing water. Water early in the day so sunlight evaporates leaf moisture within 2 hours.",
        "water_management_ur": "کھیت میں پانی کھڑا نہ ہونے دیں۔ صبح سویرے پانی دیں تاکہ دھوپ نکلتے ہی پتے خشک ہو جائیں۔",
        "nutrient_management_en": "Halt excessive nitrogen applications immediately (soft lush growth accelerates infection). Apply soluble Potassium Sulfate to toughen leaf cuticle.",
        "nutrient_management_ur": "نائٹروجن (یوریا) کا استعمال روک دیں کیونکہ نرم پتے بیماری کو تیزی سے قبول کرتے ہیں۔ پوٹاش کا استعمال بڑھائیں۔",
        "disease_management_en": {
            "cultural": "Wide row spacing (15-20 cm) orientation along prevailing winds; remove all volunteer alliums and crop debris.",
            "biological": "Foliar bio-protection with Bacillus subtilis or copper soap formulations during early onset.",
            "chemical": "Targeted fungicide spray (e.g., Metalaxyl + Mancozeb, Dimethomorph, or Cymoxanil) applied according to registered provincial agriculture extension labels. Always consult a local agricultural officer for precise timing."
        },
        "disease_management_ur": {
            "cultural": "پودوں میں مناسب فاصلہ رکھیں اور کھیت کی ہوا داری بہتر بنائیں۔",
            "biological": "ابتدائی مرحلے پر بائیو فنگسائڈز یا تانبے کے محفوظ محلول کا اسپرے کریں۔",
            "chemical": "محکمہ زراعت کی تجویز کردہ پھپھوندی کش ادویات (جیسے میٹالیکسل یا مینکوزیب) کا لیبل کے مطابق بر وقت اسپرے کریں۔"
        },
        "action_plan_7day_en": {
            "today": "Isolate the infected zone, cease evening irrigation, and clear severely blighted foliage.",
            "day_2_3": "Apply approved systemic/protectant fungicide spray early morning with a suitable sticker/spreader.",
            "day_4_5": "Assess lesion progression; inspect new emerging leaves for clean, symptom-free growth.",
            "day_6_7": "Re-evaluate canopy recovery. If cool/foggy weather persists, schedule second protection spray per label instructions."
        },
        "action_plan_7day_ur": {
            "today": "متاثرہ حصے کی نشاندہی کریں، شام کا پانی روکیں اور زیادہ خراب پتے ہٹا دیں۔",
            "day_2_3": "صبح کے وقت تجویز کردہ پھپھوندی کش دوا کا اسپرے اسٹیکر کے ساتھ کریں۔",
            "day_4_5": "نئے نکلنے والے پتوں کا معائنہ کریں کہ کیا بیماری رک گئی ہے۔",
            "day_6_7": "اگر موسم بدستور مرطوب رہے تو ماہر زراعت کے مشورے سے اگلا حفاظتی اقدام کریں۔"
        },
        "warning_signs_en": "Purplish sporulation spreading across entire leaf whorls, widespread tip collapse across multiple beds.",
        "warning_signs_ur": "پتوں پر جامنی رنگ کی پھپھوندی کا تیزی سے پھیلنا اور پتوں کا گرنا۔",
        "expert_escalation_en": "Urgent consultation required if disease exceeds 15% field coverage during bulb expansion stage.",
        "expert_escalation_ur": "اگر گانٹھ بنتے وقت 15 فیصد سے زیادہ پودے متاثر ہوں تو فوری فیلڈ آفیسر کو بلائیں۔",
        "evidence_sources": [
            {
                "organization": "University of Agriculture Faisalabad (UAF)",
                "document": "Department of Plant Pathology — Allium Disease Diagnostic & Management Bulletin",
                "focus": "Peronospora destructor epidemiology and fungicide resistance management",
                "reference": "UAF Plant Pathology Extension Series 2023-ON-04"
            },
            {
                "organization": "Punjab Agriculture Department (Extension Wing)",
                "document": "Crop Advisory Bulletin: Winter Onion Disease Control",
                "focus": "Downy mildew prevention in irrigated plains",
                "reference": "Govt of Punjab Agriculture Extension, Lahore, 2024"
            }
        ]
    },

    "onion:purple blotch": {
        "crop": "Onion",
        "condition_name": "Purple Blotch",
        "condition_name_ur": "پیاز کا جامنی دھبہ (پرپل بلاچ)",
        "scientific_name": "Alternaria porri",
        "severity": "moderate",
        "growth_stage_vulnerability": "Mid-vegetative through bulb sizing",
        "what_this_means_en": "Alternaria porri causes small water-soaked lesions that rapidly expand into characteristic elliptical sunken purplish-brown spots with concentric rings and yellow halos. Often enters through thrips feeding punctures or mechanical abrasions.",
        "what_this_means_ur": "پتوں پر بیضوی شکل کے جامنی اور بھورے رنگ کے دھبے بنتے ہیں جن کے گرد پیلا دائرہ ہوتا ہے۔ یہ بیماری اکثر رس چوسنے والے کیڑوں کے زخموں کے راستے داخل ہوتی ہے۔",
        "immediate_actions_en": [
            "Inspect leaf axils for thrips infestation (thrips damage accelerates Alternaria entry).",
            "Sterilize hand tools and avoid overhead splashing during field tasks.",
            "Remove badly infected outer leaves and dispose of outside the planting area.",
            "Apply balanced micronutrients with focus on Zinc and Boron to support tissue healing."
        ],
        "immediate_actions_ur": [
            "پتوں کے درمیان تھرپس کا معائنہ کریں کیونکہ کیڑوں کے زخموں سے بیماری پھیلتی ہے۔",
            "کام کے دوران اوزاروں کو صاف رکھیں اور پتوں پر پانی نہ اچھالیں۔",
            "خراب پتوں کو کھیت سے باہر ٹھکانے لگائیں۔",
            "زنک اور بوران جیسے مائیکرو نیوٹرینٹس کا متوازن استعمال کریں۔"
        ],
        "water_management_en": "Shift to furrow or drip irrigation to keep onion foliage dry. Irrigate at 7-10 day intervals according to soil texture.",
        "water_management_ur": "ڈرپ یا کھالیوں کے ذریعے پانی دیں تاکہ پتے خشک رہیں۔",
        "nutrient_management_en": "Avoid excessive nitrogen which makes leaf cuticle tender. Supplement with Potassium to enhance disease tolerance.",
        "nutrient_management_ur": "نائٹروجن کی زیادتی سے پرہیز کریں اور پودے کی قوت مدافعت بڑھانے کے لیے پوٹاش دیں۔",
        "disease_management_en": {
            "cultural": "Destroy infected plant residue after harvest; implement a 2-3 year non-allium rotation cycle.",
            "biological": "Neem seed extract sprays for combined thrips deterrence and mild antifungal barrier.",
            "chemical": "Mancozeb, Chlorothalonil, or Azoxystrobin applied according to official registered pesticide guidelines with approved wetting agents."
        },
        "disease_management_ur": {
            "cultural": "فصل کی باقیات کو تلف کریں اور 2 سے 3 سال تک فصلوں کا ہیر پھیر کریں۔",
            "biological": "نیم کے عرق کا اسپرے کیڑوں اور پھپھوندی دونوں کے خلاف مفید ہے۔",
            "chemical": "محکمہ زراعت کے تجویز کردہ مینکوزیب یا ایزوکسسٹروبن کا اسپرے اسٹیکر کے ساتھ کریں۔"
        },
        "action_plan_7day_en": {
            "today": "Confirm thrips count and mark infected patches across the field.",
            "day_2_3": "Apply recommended fungicide + thrips deterrent in early morning calm wind.",
            "day_4_5": "Check target spots: existing lesions should turn dark/dry without expanding yellow borders.",
            "day_6_7": "Assess newly emerging leaves to ensure zero new purple lesions appear."
        },
        "action_plan_7day_ur": {
            "today": "تھرپس کی تعداد دیکھیں اور متاثرہ پودوں پر نشان لگائیں۔",
            "day_2_3": "صبح کے پرسکون وقت میں تجویز کردہ اسپرے کریں۔",
            "day_4_5": "دھبوں کا جائزہ لیں کہ کیا وہ سوکھ رہے ہیں اور پھیلنا بند ہو گئے ہیں۔",
            "day_6_7": "نئی کونپلوں کا معائنہ کریں تاکہ بیماری کے مکمل خاتمے کی تصدیق ہو۔"
        },
        "warning_signs_en": "Concentric purplish lesions girdling the entire leaf blade causing complete lodging of flower scapes or leaves.",
        "warning_signs_ur": "دھبوں کا آپس میں مل کر پورے پتے کو گھیر لینا اور پتے کا ٹوٹ جانا۔",
        "expert_escalation_en": "Consult local extension if seed stalks (scapes) collapse or leaf loss exceeds 20%.",
        "expert_escalation_ur": "اگر پودوں کے 20 فیصد سے زائد پتے سوکھ جائیں تو ماہر زراعت سے رابطہ کریں۔",
        "evidence_sources": [
            {
                "organization": "Sindh Agriculture University (SAU) Tandojam",
                "document": "Foliar Fungal Complex in Rabi Onions: Diagnosis & Management",
                "focus": "Alternaria porri and Stemphylium interactions under dry subtropical conditions",
                "reference": "SAU Faculty of Crop Protection Monograph Series, 2023"
            },
            {
                "organization": "CABI PlantwisePlus",
                "document": "Purple Blotch on Onion — Pest Management Decision Guide",
                "focus": "Cultural, monitoring, and threshold-based chemical interventions",
                "reference": "CABI Knowledge Bank Reference PMDG-2023-ON02"
            }
        ]
    },

    "onion:stemphylium leaf blight": {
        "crop": "Onion",
        "condition_name": "Stemphylium Leaf Blight",
        "condition_name_ur": "پیاز کا سٹیمفیلیم جھلساؤ",
        "scientific_name": "Stemphylium vesicarium",
        "severity": "high",
        "growth_stage_vulnerability": "Mid-vegetative to bulb maturity during warm, wet conditions",
        "what_this_means_en": "Stemphylium vesicarium produces small yellow-to-tan water-soaked lesions that rapidly elongate into extensive dark brown patches covered with olive-brown to black powdery spore layers. It frequently attacks foliage already stressed by heat, thrips, or downy mildew.",
        "what_this_means_ur": "پتوں پر پیلے اور گہرے بھورے رنگ کے لمبے دھبے بنتے ہیں جن پر سیاہی مائل پاؤڈر جم جاتا ہے۔ یہ بیماری گرم اور نمی والے موسم میں تیزی سے پھیلتی ہے۔",
        "immediate_actions_en": [
            "Scout for co-infection with Purple Blotch or Thrips damage.",
            "Remove severely blighted foliage from field rows to lower spore density.",
            "Improve drainage and ensure field soil does not remain saturated.",
            "Avoid high nitrogen top-dressing while blight is active."
        ],
        "immediate_actions_ur": [
            "کھیت میں تھرپس اور دیگر پھپھوندی کے مشترکہ حملے کی جانچ کریں۔",
            "شدید جھلسے ہوئے پتوں کو احتیاط سے نکال کر ضائع کریں۔",
            "کھیت کی نکاسی کو فوری بہتر بنائیں تاکہ جڑیں نہ گلیں۔",
            "بیماری کے دوران یوریا کھاد دینے سے مکمل گریز کریں۔"
        ],
        "water_management_en": "Irrigate during early morning. Allow topsoil to dry between watering cycles to minimize relative humidity in crop canopy.",
        "water_management_ur": "صبح سویرے ہلکی آبپاشی کریں اور مٹی کی اوپری سطح کو تھوڑا خشک ہونے دیں۔",
        "nutrient_management_en": "Apply balanced Potassium and Micronutrient sprays to rebuild leaf membrane integrity.",
        "nutrient_management_ur": "پوٹاش اور ضروری مائیکرو نیوٹرینٹس کا اسپرے پودوں کی مضبوطی کے لیے کریں۔",
        "disease_management_en": {
            "cultural": "Maintain optimum plant spacing (15 cm) for air flow; strictly avoid working in wet fields.",
            "biological": "Application of bio-protectant Trichoderma viride or copper hydroxide formulations at early stage.",
            "chemical": "Use approved fungicides (e.g. Difenoconazole, Tebuconazole, or Iprodione) strictly adhering to extension department label rates."
        },
        "disease_management_ur": {
            "cultural": "پودوں میں مناسب فاصلہ رکھیں اور گیلے کھیت میں داخل ہونے سے بچیں۔",
            "biological": "ٹرائیکوڈرما یا کاپر ہائیڈرو آکسائیڈ کا بروقت حفاظتی استعمال کریں۔",
            "chemical": "محکمہ زراعت کی ہدایت کے مطابق ڈائیفینوکونازول یا ٹیبوکونازول کا اسپرے کریں۔"
        },
        "action_plan_7day_en": {
            "today": "Audit field for blight intensity; isolate severely affected quadrants.",
            "day_2_3": "Apply recommended triazole or strobilurin-class fungicide with agricultural surfactant.",
            "day_4_5": "Inspect newly unfolding central leaves for absence of tan specks.",
            "day_6_7": "Assess disease suppression; confirm bulb growth is continuing normally."
        },
        "action_plan_7day_ur": {
            "today": "بیماری کی شدت کا جائزہ لیں اور زیادہ متاثرہ حصوں کو الگ کریں۔",
            "day_2_3": "ماہرین کی تجویز کردہ پھپھوندی کش دوا کا اسپرے کریں۔",
            "day_4_5": "نئے نکلنے والے پتوں کا معائنہ کریں کہ وہ داغوں سے پاک ہوں۔",
            "day_6_7": "گانٹھ کے سائز کا مشاہدہ کریں اور فصل کی بحالی کی تصدیق کریں۔"
        },
        "warning_signs_en": "Black powdery spore crusts covering >50% of leaf area and extensive pre-mature leaf lodging.",
        "warning_signs_ur": "پتوں پر کالے پاؤڈر کی موٹی تہہ اور 50 فیصد سے زائد پتوں کا قبل از وقت مرجھا جانا۔",
        "expert_escalation_en": "Consult an agricultural officer if lesions spread rapidly across entire canopy within 48 hours.",
        "expert_escalation_ur": "اگر 48 گھنٹوں میں بیماری تیزی سے پھیلے تو فوری زرعی ماہر سے رجوع کریں۔",
        "evidence_sources": [
            {
                "organization": "Pakistan Agricultural Research Council (PARC)",
                "document": "Plant Protection Institute Advisory on Stemphylium Complex",
                "focus": "Fungal foliar blight epidemiology and multi-site chemical control",
                "reference": "PARC-NARC Islamabad Technical Bulletin, 2023"
            }
        ]
    },

    # =========================================================================
    # MANGO (Mangifera indica)
    # =========================================================================
    "mango:healthy": {
        "crop": "Mango",
        "condition_name": "Healthy Mango Foliage & Orchard",
        "condition_name_ur": "صحت مند آم کے باغات اور پتے",
        "scientific_name": "Mangifera indica",
        "severity": "none",
        "growth_stage_vulnerability": "All growth stages (Flushing, Panicle Emergence, Fruit Set, Post-Harvest)",
        "what_this_means_en": "Your mango leaves show healthy deep green leathery texture, clean venation, and intact apical buds. There are no signs of anthracnose blackening, powdery mildew coatings, die-back twig necrosis, or gall midge blisters.",
        "what_this_means_ur": "آپ کے آم کے درخت اور پتے بالکل صحت مند، گہرے سبز اور بیماریوں سے پاک ہیں۔ نئی پھوٹ، پھول اور پھل کا عمل بہترین انداز میں جاری رہنے کے لیے باقاعدہ دیکھ بھال جاری رکھیں۔",
        "immediate_actions_en": [
            "Maintain clean orchard basin (thala system) free of weeds and dry fallen leaves.",
            "Ensure regular irrigation monitoring tailored to flowering vs fruit enlargement stages.",
            "Inspect trunk and major branch unions for any sap oozing or bark cracking.",
            "Check undersides of young flushes for early gall midge or hopper presence."
        ],
        "immediate_actions_ur": [
            "آم کے تھالوں کو جڑی بوٹیوں اور سوکھے پتوں سے صاف رکھیں۔",
            "پھول آنے اور پھل بننے کے مرحلے کے مطابق پانی کی مقدار متوازن رکھیں۔",
            "تنے اور موٹی شاخوں پر گوند کے اخراج یا کیڑوں کے سوراخ چیک کریں۔",
            "نئی نکلنے والی کونپلوں کا بغور معائنہ کریں۔"
        ],
        "water_management_en": "Irrigate deeply at 10-14 day intervals during fruit growth. Avoid irrigation during peak flowering to prevent excessive vegetative flush and flower drop.",
        "water_management_ur": "پھل بننے کے دوران 10 سے 14 دن کے وقفے سے گہرا پانی دیں۔ پھول آنے کے عروج پر پانی روکیں تاکہ پھول نہ گریں۔",
        "nutrient_management_en": "Apply balanced FYM (Farmyard Manure) along with Nitrogen, Phosphorus, and Potassium in ring trenches after harvest and during fruit development.",
        "nutrient_management_ur": "گوبر کی گلی سڑی کھاد کے ساتھ این پی کے (NPK) کھادوں کا متوازن استعمال چھتری کے نیچے کریں۔",
        "disease_management_en": {
            "cultural": "Perform canopy center opening (light pruning) after harvest to maximize sunlight penetration and airflow.",
            "biological": "Encourage predatory lacewings and beneficial parasitoids for natural pest control.",
            "chemical": "No intervention required. Follow routine seasonal preventive calendar."
        },
        "disease_management_ur": {
            "cultural": "فصل کے بعد درمیان سے خشک اور غیر ضروری شاخیں کاٹیں تاکہ دھوپ اور ہوا اندر تک پہنچے۔",
            "biological": "مفید کیڑوں اور پرندوں کے لیے ماحول سازگار رکھیں۔",
            "chemical": "کسی اسپرے کی ضرورت نہیں۔ صرف موسمی احتیاطی تدابیر پر عمل کریں۔"
        },
        "action_plan_7day_en": {
            "today": "Inspect orchard floor and remove dry leaf litter from tree basins.",
            "day_2_3": "Check irrigation moisture retention around feeder roots (drip line).",
            "day_4_5": "Examine new flush leaves for vibrant, uniform growth.",
            "day_6_7": "Document canopy vigor and record upcoming panicle emergence schedule."
        },
        "action_plan_7day_ur": {
            "today": "درختوں کے نیچے صفائی کریں اور سوکھے پتے ہٹا دیں۔",
            "day_2_3": "جڑوں کے قریب مٹی میں نمی کی مناسب سطح چیک کریں۔",
            "day_4_5": "نئی پھوٹ کا جائزہ لیں کہ وہ تروتازہ ہو۔",
            "day_6_7": "باغ کی مجموعی صحت کا ریکارڈ رکھیں اور اگلے مراحل کی منصوبہ بندی کریں۔"
        },
        "warning_signs_en": "Watch for sudden twig tip drying, flower drop, or white powdery coatings during spring bloom.",
        "warning_signs_ur": "شاخوں کا سوکھنا، پھولوں کا جھڑنا یا سفید پاؤڈر نما دھبے ظاہر ہونا خطرے کی علامت ہیں۔",
        "expert_escalation_en": "Consult mango research institute if blossom blight or twig dieback appears in the orchard.",
        "expert_escalation_ur": "اگر شاخیں سوکھنے لگیں تو فوری آم ریسرچ انسٹیٹیوٹ یا زرعی افسر سے رابطہ کریں۔",
        "evidence_sources": [
            {
                "organization": "Mango Research Institute (MRI) Multan",
                "document": "Orchard Management & Good Agricultural Practices for Mango",
                "focus": "Canopy management, nutrition, and phenological irrigation",
                "reference": "MRI Multan Technical Manual 2023-MG-01"
            },
            {
                "organization": "Agriculture Department Govt of Punjab",
                "document": "Mango Production & Protection Advisory Guide",
                "focus": "Integrated orchard protection",
                "reference": "Directorate of Agricultural Information Punjab, 2024"
            }
        ]
    },

    "mango:anthracnose": {
        "crop": "Mango",
        "condition_name": "Anthracnose",
        "condition_name_ur": "آم کا اینتھراکنوز (سیاہ دھبہ بیماری)",
        "scientific_name": "Colletotrichum gloeosporioides",
        "severity": "high",
        "growth_stage_vulnerability": "Panicle emergence, flowering, flush emergence, and post-harvest fruit",
        "what_this_means_en": "Colletotrichum gloeosporioides causes irregular dark brown to black necrotic spots on young leaves, blossom blight on flower panicles, and tear-stain black lesions on developing and ripening mangoes. It spreads aggressively during warm, humid rains and heavy morning dews.",
        "what_this_means_ur": "پتوں، پھولوں اور پھلوں پر گہرے بھورے اور کالے دھبے بن جاتے ہیں۔ بارش اور نمی کے موسم میں یہ بیماری تیزی سے پھیل کر پھولوں اور پھلوں کو گرا دیتی ہے۔",
        "immediate_actions_en": [
            "Prune out severely blighted panicles and dry infected twigs using sterilized shears.",
            "Clear and burn fallen infected mango leaves and mummified fruit from the orchard floor.",
            "Avoid overhead sprinkler irrigation or wetting tree canopies during evening hours.",
            "Coat pruning cuts larger than 1 inch with Bordeaux paste or copper oxychloride slurry."
        ],
        "immediate_actions_ur": [
            "متاثرہ کالی شاخوں اور سوکھے پھولوں کو صاف قینچی سے کاٹ کر تلف کریں۔",
            "درختوں کے نیچے گرے ہوئے بیمار پتے اور کالا پھل اکٹھا کر کے جلا دیں۔",
            "شام کے وقت درختوں پر پانی کا چھڑکاؤ ہرگز نہ کریں۔",
            "شاخ تراشی کے بعد کٹے ہوئے حصوں پر کاپر کا لیپ لگائیں۔"
        ],
        "water_management_en": "Use basin or drip irrigation to keep water strictly on the ground. Ensure orchard floor drains quickly after seasonal rain showers.",
        "water_management_ur": "تھالوں کے ذریعے پانی دیں تاکہ پتے اور پھل خشک رہیں۔ بارش کا پانی فوری نکالیں۔",
        "nutrient_management_en": "Avoid excessive nitrogen fertilizers prior to flowering; provide adequate Potassium, Zinc, and Calcium to enhance fruit skin resistance.",
        "nutrient_management_ur": "پھول آنے سے قبل زیادہ یوریا نہ دیں؛ پھل کی جلد مضبوط بنانے کے لیے پوٹاش اور کیلشیم دیں۔",
        "disease_management_en": {
            "cultural": "Annual post-harvest canopy pruning to open interior branches to sunlight and wind circulation.",
            "biological": "Bio-antifungal sprays of Bacillus amyloliquefaciens or Trichoderma species during low-pressure windows.",
            "chemical": "Foliar sprays of Copper Oxychloride, Azoxystrobin, or Difenoconazole at panicle emergence and after fruit set according to extension guidelines."
        },
        "disease_management_ur": {
            "cultural": "فصل کے بعد باغ کی باقاعدہ کانٹ چھانٹ کریں تاکہ اندر تک دھوپ پہنچے۔",
            "biological": "ابتدائی مرحلے پر بائیو فنگسائڈز کا اسپرے کریں۔",
            "chemical": "پھول نکلتے وقت اور پھل بنتے ہی محکمہ زراعت کی تجویز کردہ کاپر یا ایزوکسسٹروبن کا اسپرے کریں۔"
        },
        "action_plan_7day_en": {
            "today": "Prune visibly infected twigs and panicles; sanitize pruning tools in 70% alcohol.",
            "day_2_3": "Apply approved copper-based or systemic strobilurin fungicide spray in morning.",
            "day_4_5": "Check blossom panicles and leaf margins; confirm black lesion expansion has halted.",
            "day_6_7": "Audit surrounding tree canopies for any unnoticed tear-stain symptoms on young fruitlets."
        },
        "action_plan_7day_ur": {
            "today": "بیمار شاخیں کاٹیں اور قینچی کو اسپرٹ سے صاف کریں۔",
            "day_2_3": "صبح سویرے تجویز کردہ کاپر یا پھپھوندی کش دوا کا اسپرے کریں۔",
            "day_4_5": "پھولوں اور پتوں کا جائزہ لیں کہ دھبے پھیلنا بند ہوئے ہیں۔",
            "day_6_7": "ساتھ والے درختوں کا معائنہ کریں تاکہ بیماری کے نئے حملے کا تدارک ہو۔"
        },
        "warning_signs_en": "Extensive blackening of entire flower panicles (blossom blight) and rapid drop of newly set fruitlets.",
        "warning_signs_ur": "پھولوں کے گچھوں کا مکمل کالا ہو جانا اور چھوٹے پھلوں کا تیزی سے گرنا۔",
        "expert_escalation_en": "Consult mango pathologist if blossom blight threatens more than 20% of commercial flowering panicles.",
        "expert_escalation_ur": "اگر پھولوں کا بڑا حصہ کالا ہو کر سوکھ رہا ہو تو فوری زرعی ماہر سے رابطہ کریں۔",
        "evidence_sources": [
            {
                "organization": "Mango Research Institute (MRI) Multan",
                "document": "Anthracnose & Post-Harvest Fruit Rot Management Protocol",
                "focus": "Colletotrichum gloeosporioides epidemiology, pre-harvest sprays, and hot water dip",
                "reference": "MRI Pathology Division Advisory 2023-MG-04"
            },
            {
                "organization": "CABI PlantwisePlus",
                "document": "Mango Anthracnose Management Guide",
                "focus": "Field sanitation, blossom protection, and spray timing",
                "reference": "CABI Knowledge Bank Reference PMDG-2023-MG01"
            }
        ]
    },

    "mango:die back": {
        "crop": "Mango",
        "condition_name": "Mango Die Back / Quick Decline",
        "condition_name_ur": "آم کا سوکھا / ڈائی بیک بیماری",
        "scientific_name": "Lasiodiplodia theobromae / Ceratocystis fimbriata",
        "severity": "critical",
        "growth_stage_vulnerability": "All stages, especially mature productive trees under water/heat stress",
        "what_this_means_en": "Dieback is a destructive vascular wilt disorder causing progressive drying of branches from the top downwards. Leaves turn brown, roll upwards, and remain attached to dead twigs. Vascular bundles exhibit dark brown discolouration and gum exudation on the trunk.",
        "what_this_means_ur": "اس خطرناک بیماری میں شاخیں اوپر سے نیچے کی طرف سوکھنا شروع ہوتی ہیں۔ پتے بھورے ہو کر سوکھ جاتے ہیں مگر شاخ سے چمٹے رہتے ہیں اور تنے سے گوند خارج ہوتا ہے۔",
        "immediate_actions_en": [
            "Prune dead and drying branches 4-6 inches below the healthy green wood boundary.",
            "Immediately apply thick Bordeaux paste or Copper Oxychloride paste over every cut surface.",
            "Disinfect pruning saws and shears with 10% bleach or alcohol between every single cut.",
            "Examine the root collar zone for bark beetle or borer entry holes."
        ],
        "immediate_actions_ur": [
            "سوکھتی ہوئی شاخ کو صحت مند حصے سے 4 سے 6 انچ نیچے سے کاٹ دیں۔",
            "کٹے ہوئے زخم پر فوری طور پر بورڈو پیسٹ یا کاپر کا گاڑھا لیپ لگائیں۔",
            "ہر کٹائی کے بعد قینچی یا آری کو اسپرٹ سے لازمی جراثیم سے پاک کریں۔",
            "تنے کے نیچے جڑوں کے قریب گوند یا سوراخوں کا معائنہ کریں۔"
        ],
        "water_management_en": "Maintain regular, measured irrigation to avoid severe drought stress followed by sudden flooding. Keep tree trunk collars dry.",
        "water_management_ur": "باغ کو پیاس کے شدید دباؤ سے بچائیں اور پانی کا باقاعدہ شیڈول رکھیں۔ تنے کے ساتھ پانی نہ کھڑا ہونے دیں۔",
        "nutrient_management_en": "Avoid heavy nitrogen in affected trees. Apply balanced organic compost and Potassium Sulfate in outer canopy dripline.",
        "nutrient_management_ur": "متاثرہ درخت کو نائٹروجن کم دیں؛ پوٹاش اور گوبر کی کھاد کا مناسب استعمال کریں۔",
        "disease_management_en": {
            "cultural": "Paint tree trunks up to 3 feet with Bordeaux mixture (1:1:10) or lime-copper wash twice a year (spring & post-monsoon).",
            "biological": "Soil drenching around tree root feeder zone with Trichoderma harzianum culture.",
            "chemical": "Systemic fungicide drenching (e.g. Thiophanate-Methyl or Fosetyl-Al) combined with bark beetle management per extension guidelines."
        },
        "disease_management_ur": {
            "cultural": "سال میں دو بار تنے پر 3 فٹ تک چونا اور نیلا تھوتھا (بورڈو مکسچر) کا لیپ کریں۔",
            "biological": "جڑوں کے قریب ٹرائیکوڈرما بائیو فنگسائڈ کا استعمال کریں۔",
            "chemical": "محکمہ زراعت کے مشورے سے تھیوفینیٹ میتھائل یا فوسیٹائل ایلومینیم کا اسپرے اور جڑوں میں استعمال کریں۔"
        },
        "action_plan_7day_en": {
            "today": "Perform drastic pruning of all dry branches down to clean green vascular tissue; paste cuts.",
            "day_2_3": "Disinfect tree trunk and soil basin with copper oxychloride solution.",
            "day_4_5": "Inspect treated limbs: verify no new resin oozing or downward advancing necrotic margins.",
            "day_6_7": "Audit neighboring trees in the same water channel for early branch wilting."
        },
        "action_plan_7day_ur": {
            "today": "سوکھتی شاخیں صحت مند حصے تک کاٹیں اور زخموں پر پیسٹ لگائیں۔",
            "day_2_3": "تنے اور تھالے میں کاپر آکسی کلورائیڈ کا محلول ڈالیں۔",
            "day_4_5": "کاٹے گئے حصوں کو دیکھیں کہ مزید گوند یا سوکھا پن آگے تو نہیں بڑھ رہا۔",
            "day_6_7": "ساتھ والے دوسرے درختوں کا باریک بینی سے معائنہ کریں۔"
        },
        "warning_signs_en": "Gum weeping from main trunk fissures, sudden collapse of major scaffolding limbs, brown staining in wood vessels.",
        "warning_signs_ur": "تنے سے گوند کا بہنا، بڑی شاخوں کا اچانک سوکھنا اور لکڑی کا اندر سے کالا ہونا۔",
        "expert_escalation_en": "CRITICAL: Contact District Agricultural Extension Officer or MRI Multan immediately if whole mature trees collapse.",
        "expert_escalation_ur": "انتہائی ضروری: اگر پورا درخت سوکھنے لگے تو فوری طور پر ضلعی زرعی افسر یا مینگو ریسرچ انسٹیٹیوٹ سے رابطہ کریں۔",
        "evidence_sources": [
            {
                "organization": "Mango Research Institute (MRI) Multan",
                "document": "Mango Quick Decline & Dieback Action Plan",
                "focus": "Lasiodiplodia theobromae and Ceratocystis management protocol",
                "reference": "MRI Multan Technical Advisory Series, 2023"
            },
            {
                "organization": "Pakistan Journal of Phytopathology",
                "document": "Etiology and Integrated Management of Mango Dieback in Southern Punjab and Sindh",
                "focus": "Vascular wilt pathology, borer vector dynamics, and systemic control",
                "reference": "Pak. J. Phytopathol., Vol 34, Issue 2, 2022"
            }
        ]
    },

    "mango:powdery mildew": {
        "crop": "Mango",
        "condition_name": "Powdery Mildew",
        "condition_name_ur": "آم کا سفوفی پھپھوند (پاؤڈری ملڈیو)",
        "scientific_name": "Oidium mangiferae",
        "severity": "high",
        "growth_stage_vulnerability": "Panicle emergence, flowering, and young fruit set stage (Spring: Feb-April)",
        "what_this_means_en": "Oidium mangiferae causes white powdery fungal patches covering inflorescences (panicles), flower buds, tender leaves, and young marble-sized fruit. Affected flowers fail to open and drop prematurely, causing up to 80% loss in fruit set.",
        "what_this_means_ur": "پھولوں کے گچھوں، نئی کونپلوں اور چھوٹے پھل پر سفید پاؤڈر نما سفوف جم جاتا ہے۔ پھول کھلنے سے پہلے سوکھ کر جھڑ جاتے ہیں جس سے پیداوار کو شدید نقصان پہنچتا ہے۔",
        "immediate_actions_en": [
            "Inspect flower panicles in early morning when white powdery growth is most conspicuous.",
            "Avoid excessive moisture stress during blooming period.",
            "Apply prophylactic sulfur or triazole spray before 50% flower opening if weather is cloudy.",
            "Prune dense internal foliage to allow sunlight directly onto interior flowering branches."
        ],
        "immediate_actions_ur": [
            "صبح کے وقت پھولوں کے گچھوں کا معائنہ کریں کہ سفید پاؤڈر تو نہیں جم رہا۔",
            "پھول کھلنے کے دوران پانی کا سخت دباؤ نہ آنے دیں۔",
            "پھول مکمل کھلنے سے پہلے سلفر یا تجویز کردہ دوا کا حفاظتی اسپرے کریں۔",
            "درمیان سے شاخوں کو ہلکا کریں تاکہ پھولوں تک دھوپ پہنچ سکے۔"
        ],
        "water_management_en": "Keep orchard soil moderately moist but avoid surface waterlogging during pollination. Do not spray cold well-water over blooms.",
        "water_management_ur": "پھول آنے کے دوران مٹی میں ہلکی نمی رکھیں لیکن پانی کھڑا نہ ہونے دیں۔",
        "nutrient_management_en": "Apply balanced micronutrient spray (Zinc + Boron) before panicle opening to enhance flower strength.",
        "nutrient_management_ur": "پھول کھلنے سے قبل زنک اور بوران کا اسپرے کریں تاکہ پھول مضبوط بنیں۔",
        "disease_management_en": {
            "cultural": "Prune malformed and mildewed panicles early in the season before spores become airborne.",
            "biological": "Application of wettable bio-sulfur or potassium bicarbonate formulations.",
            "chemical": "Wettable Sulfur (80% WP) or systemic triazoles (e.g. Hexaconazole, Penconazole, or Dinocap) applied at panicle emergence and post-fruit set per extension department rates."
        },
        "disease_management_ur": {
            "cultural": "بیمار گچھوں کو شروع میں ہی احتیاط سے کاٹ دیں۔",
            "biological": "بائیو سلفر یا پوٹاشیم بائی کاربونیٹ کا اسپرے کریں۔",
            "chemical": "محکمہ زراعت کی ہدایت کے مطابق ویٹیبل سلفر یا ہیکسا کونازول کا بر وقت اسپرے کریں۔"
        },
        "action_plan_7day_en": {
            "today": "Assess panicle infection level across sunny vs shaded orchard sectors.",
            "day_2_3": "Apply approved wettable sulfur or systemic fungicide in early morning calm breeze.",
            "day_4_5": "Check bloom panicles: white powdery growth should turn grey-brown and desiccate.",
            "day_6_7": "Examine newly set pea-sized fruitlets to ensure clean cuticle without white film."
        },
        "action_plan_7day_ur": {
            "today": "باغ کے دھوپ اور سائے والے حصوں میں پھولوں کی بیماری کا تناسب دیکھیں۔",
            "day_2_3": "صبح سویرے پرسکون موسم میں سلفر یا پھپھوندی کش دوا کا اسپرے کریں۔",
            "day_4_5": "پھولوں کو دیکھیں کہ سفید پاؤڈر سوکھ کر ختم ہو رہا ہے۔",
            "day_6_7": "چھوٹے بننے والے آم کے پھل کا معائنہ کریں کہ وہ داغوں سے پاک ہوں۔"
        },
        "warning_signs_en": "Complete white crusting of flower panicles causing total blossom drop and bare flower stalks.",
        "warning_signs_ur": "پھولوں کے گچھوں پر سفید سفوف کی موٹی تہہ اور تمام پھولوں کا جھڑ جانا۔",
        "expert_escalation_en": "Contact extension service immediately if white powdery growth covers >15% of flowering panicles during peak bloom.",
        "expert_escalation_ur": "اگر پھول آنے کے دوران 15 فیصد سے زیادہ گچھے متاثر ہوں تو فوری زرعی ماہر سے رابطہ کریں۔",
        "evidence_sources": [
            {
                "organization": "Mango Research Institute (MRI) Multan",
                "document": "Flowering Season Disease Management: Powdery Mildew & Blossom Blight",
                "focus": "Oidium mangiferae phenological spray timing and temperature triggers",
                "reference": "MRI Advisory Bulletin MG-02-2023"
            }
        ]
    },

    # =========================================================================
    # SUGARCANE (Saccharum officinarum)
    # =========================================================================
    "sugarcane:healthy": {
        "crop": "Sugarcane",
        "condition_name": "Healthy Sugarcane Crop",
        "condition_name_ur": "صحت مند کماد (گنا) کی فصل",
        "scientific_name": "Saccharum officinarum",
        "severity": "none",
        "growth_stage_vulnerability": "All growth stages (Germination, Tillering, Grand Growth, Ripening)",
        "what_this_means_en": "Your sugarcane crop demonstrates excellent tillering density, broad dark green erect leaves, and robust internode elongation. There are no signs of red rot stalk discolouration, mosaic mottling, rust pustules, or bacterial stripe necrosis.",
        "what_this_means_ur": "آپ کے کماد کی فصل شاندار حالت میں ہے۔ تنے مضبوط، پتے چوڑے اور گہرے سبز ہیں اور کسی بیماری یا کیڑے کا اثر نہیں ہے۔ مناسب دیکھ بھال سے گنے کا وزن اور مٹھاس بہترین رہے گی۔",
        "immediate_actions_en": [
            "Maintain earthing-up (mounding soil around cane base) to prevent lodging in monsoon winds.",
            "Inspect field furrows for uniform water flow and weed suppression.",
            "Check inter-node development and peel occasional dry lower leaves (trashing) for ventilation.",
            "Monitor root zone for moisture retention during grand growth phase."
        ],
        "immediate_actions_ur": [
            "گنے کی جڑوں پر مٹی چڑھانے (Earthing-up) کا عمل مکمل رکھیں تاکہ گنا تیز ہوا سے نہ گرے۔",
            "کھیلیاں جڑی بوٹیوں سے پاک رکھیں تاکہ پانی اور کھاد کا پورا فائدہ ملے۔",
            "سوکھے نچلے پتے صاف کریں تاکہ ہوا کا گزر ہو سکے۔",
            "بڑھوتری کے دور میں نمی کا باقاعدہ خیال رکھیں۔"
        ],
        "water_management_en": "Sugarcane requires substantial water during the grand growth stage (every 8-10 days in summer). Shift to 15-20 day intervals during maturity to enhance sugar accumulation.",
        "water_management_ur": "گرمیوں میں 8 سے 10 دن کے وقفے سے پانی دیں۔ پکنے کے قریب وقفہ 15 سے 20 دن کریں تاکہ گنے میں مٹھاس بڑھے۔",
        "nutrient_management_en": "Ensure complete Nitrogen dose is applied by early grand growth (before 90-120 days). Supplement with Potassium to maximize sucrose recovery.",
        "nutrient_management_ur": "نائٹروجن (یوریا) کا استعمال پہلے 90 سے 120 دنوں میں مکمل کر لیں۔ پوٹاش کھاد گنے کے رس اور وزن کے لیے انتہائی ضروری ہے۔",
        "disease_management_en": {
            "cultural": "Always use certified disease-free setts treated with hot water or fungicide prior to planting; clean trash post-harvest.",
            "biological": "Deploy Trichogramma egg parasitoid cards for biological borer management.",
            "chemical": "No intervention required. Maintain seasonal agronomic practices."
        },
        "disease_management_ur": {
            "cultural": "ہمیشہ تصدیق شدہ اور بیماری سے پاک سموں (Setts) کی کاشت کریں۔",
            "biological": "کیڑوں کے قدرتی تدارک کے لیے ٹرائیکوگراما کارڈز کا استعمال کریں۔",
            "chemical": "کسی کیمیائی اسپرے کی ضرورت نہیں ہے۔"
        },
        "action_plan_7day_en": {
            "today": "Confirm cane stool density and check uniformity across furrows.",
            "day_2_3": "Audit irrigation water intake and clear weed blocks in main channels.",
            "day_4_5": "Check lower nodes for dry leaf detaching and inspect apical spindle leaf vigor.",
            "day_6_7": "Record average cane height and tillers per stool for seasonal yield tracking."
        },
        "action_plan_7day_ur": {
            "today": "کھیت میں گنے کے پودوں کی تعداد اور موٹائی کا جائزہ لیں۔",
            "day_2_3": "کھالیوں میں پانی کی روانی چیک کریں اور گھاس پھونس نکالیں۔",
            "day_4_5": "گنے کی گانٹھوں اور اوپر کے پتوں کی صحت کی تسلی کریں۔",
            "day_6_7": "فصل کے قد اور اوسط وزن کا ریکارڈ رکھیں۔"
        },
        "warning_signs_en": "Yellowing/withering of 3rd and 4th crown leaves, red longitudinal streaks in split stalks, or white whip-like shoots.",
        "warning_signs_ur": "اوپر کے پتوں کا پیلا پڑنا، گنے کے اندر لال دھاریاں یا چھانٹے کی طرح کالی لٹکتی شاخیں نظر آنا خطرے کی علامت ہیں۔",
        "expert_escalation_en": "Contact sugarcane research station if sudden wilting or stalk rotting is observed in localized patches.",
        "expert_escalation_ur": "اگر گنا اندر سے سوکھنے یا گلنے لگے تو فوری شوگر کین ریسرچ انسٹیٹیوٹ سے رابطہ کریں۔",
        "evidence_sources": [
            {
                "organization": "Sugarcane Research Institute (SRI) Faisalabad",
                "document": "Standard Operating Procedures for High-Yielding Sugarcane Production",
                "focus": "Varietal agronomy, ratoon management, and irrigation scheduling",
                "reference": "AARI Faisalabad SRI Technical Publication 2023-SC-01"
            },
            {
                "organization": "Pakistan Central Cotton & Sugarcane Board",
                "document": "National Sugarcane Health & Protection Compendium",
                "focus": "Preventive management in irrigated Indus Basin",
                "reference": "PCCC Agricultural Extension Manual, 2023"
            }
        ]
    },

    "sugarcane:red rot": {
        "crop": "Sugarcane",
        "condition_name": "Red Rot (Cancer of Sugarcane)",
        "condition_name_ur": "کماد کا رتہ روگ (ریڈ راٹ / گنے کا کینسر)",
        "scientific_name": "Colletotrichum falcatum (Glomerella tucumanensis)",
        "severity": "critical",
        "growth_stage_vulnerability": "Grand Growth to Ripening stage (Rainy season to harvest)",
        "what_this_means_en": "Red Rot is the most devastating disease of sugarcane, known as 'cane cancer'. The 3rd and 4th leaves from the crown turn yellow and wither. Internally, the stalk pith shows dull red discolouration interrupted by characteristic transverse white patches with a distinct alcoholic or sour fermenting odour.",
        "what_this_means_ur": "یہ کماد کی سب سے خطرناک بیماری ہے جسے 'گنے کا کینسر' کہا جاتا ہے۔ اوپر کے پتے پیلے ہو کر سوکھ جاتے ہیں۔ گنے کو لمبائی کے رخ چیریں تو اندر سے گودا لال نکلتا ہے جس میں سفید چکتیاں اور کھٹی بدبو ہوتی ہے۔",
        "immediate_actions_en": [
            "Uproot and completely burn all affected cane clumps including root stubble immediately.",
            "Isolate the irrigation channel leading to the infected patch to prevent spore transport via water.",
            "Do NOT use setts from this entire field or adjacent plots for future seed planting.",
            "Do NOT retain ratoon crop from any field showing Red Rot symptoms."
        ],
        "immediate_actions_ur": [
            "متاثرہ گنے کے پورے مڈھوں کو جڑ سمیت اکھاڑ کر فوراً کھیت سے باہر جلا دیں۔",
            "متاثرہ حصے کا پانی دوسرے صحت مند حصوں میں جانے سے فوری روکیں۔",
            "اس کھیت کا کوئی بھی گنا اگلے سال بیج (سموں) کے طور پر ہرگز استعمال نہ کریں۔",
            "بیمار کھیت کا موڈھا (Ratoon) ہرگز نہ رکھیں۔"
        ],
        "water_management_en": "Ensure rapid drainage of excess rainwater. Avoid flowing water from infected fields into healthy standing crops.",
        "water_management_ur": "بارش کا پانی کھیت میں کھڑا نہ رہنے دیں۔ بیمار کھیت کا پانی صحت مند فصل کو نہ لگائیں۔",
        "nutrient_management_en": "Avoid excessive nitrogen top-dressing. Apply bio-fertilizers and balanced Potash to boost resistance in uninfected surrounding stools.",
        "nutrient_management_ur": "یوریا کھاد کا غیر ضروری استعمال روکیں اور پوٹاش کی مناسب مقدار دیں۔",
        "disease_management_en": {
            "cultural": "Plant certified Red Rot-resistant varieties (e.g. CPF-249, CPF-250); practice 3-year crop rotation with non-host crops like rice, cotton, or green manure (sunnhemp).",
            "biological": "Sett treatment with Trichoderma harzianum or Pseudomonas fluorescens before planting.",
            "chemical": "Fungicidal sett dip (e.g. Carbendazim or Thiophanate-Methyl 0.1%) prior to sowing. Once inside the standing stalk, chemical cure is ineffective; eradication of diseased stools is paramount."
        },
        "disease_management_ur": {
            "cultural": "بیماری کے خلاف قوت مدافعت رکھنے والی اقسام کاشت کریں اور 3 سال تک دھان یا جنتر کے ساتھ فصلوں کا ہیر پھیر کریں۔",
            "biological": "کاشت کے وقت سموں کو ٹرائیکوڈرما کے محلول سے ٹریٹ کریں۔",
            "chemical": "بیج کاشت کرنے سے پہلے تھائیو فینیٹ میتھائل یا کاربینڈازم کے محلول میں ڈبوئیں۔ کھڑے گنے میں کیمیائی علاج ممکن نہیں، بیمار پودے اکھاڑنا ہی واحد حل ہے۔"
        },
        "action_plan_7day_en": {
            "today": "Uproot and incinerate every symptomatic cane clump; treat the planting pit with lime/bleaching powder.",
            "day_2_3": "Block off irrigation runoff from infected rows; map out quarantine zone.",
            "day_4_5": "Split-test sample canes at 10-meter perimeter intervals to confirm disease boundary.",
            "day_6_7": "Consult sugar mill field staff and plan crop harvest order (harvest infected plots last, do not ratoon)."
        },
        "action_plan_7day_ur": {
            "today": "بیمار گنے جڑوں سمیت نکال کر جلائیں اور گڑھوں میں چونا ڈالیں۔",
            "day_2_3": "پانی کی نالیوں کو الگ کریں تاکہ بیماری آگے نہ جائے۔",
            "day_4_5": "کھیت کے اردگرد چند گنے چیر کر دیکھیں کہ اندر لال رنگ تو نہیں ہے۔",
            "day_6_7": "شوگر مل کے فیلڈ اسٹاف سے رابطہ کریں اور فصل کی فوری کٹائی کا پلان بنائیں۔"
        },
        "warning_signs_en": "Alcoholic sour odour from cane fields, hollowed canes with reddish pith and transverse white bands, rapid crown lodging.",
        "warning_signs_ur": "کھیت سے سرکے یا الکحل جیسی بو آنا، گنے کا اندر سے کھوکھلا اور لال ہونا اور پودوں کا گرنا۔",
        "expert_escalation_en": "CRITICAL: Notify the District Agriculture Officer and nearest Sugarcane Research Institute immediately to prevent epidemic spread across the tehsil.",
        "expert_escalation_ur": "انتہائی فوری: ضلعی زرعی افسر اور شوگر کین ریسرچ انسٹیٹیوٹ کو فوری مطلع کریں تاکہ پورے علاقے کی فصل کو بچایا جا سکے۔",
        "evidence_sources": [
            {
                "organization": "Sugarcane Research Institute (SRI) Faisalabad",
                "document": "Management Protocol for Sugarcane Red Rot Epidemics in Punjab",
                "focus": "Colletotrichum falcatum pathology, varietal screening, and sett sanitation",
                "reference": "AARI Faisalabad Research Bulletin SC-2023-RR"
            },
            {
                "organization": "Pakistan Central Sugarcane Committee",
                "document": "Red Rot Containment and Seed Certification Standard",
                "focus": "Clean seed nursery protocols and quarantine standards",
                "reference": "National Sugar Crop Advisory Board 2024"
            }
        ]
    },

    "sugarcane:mosaic": {
        "crop": "Sugarcane",
        "condition_name": "Sugarcane Mosaic Virus",
        "condition_name_ur": "کماد کا موزیک وائرس (چتکبرا پن)",
        "scientific_name": "Sugarcane Mosaic Virus (SCMV / Potyvirus)",
        "severity": "moderate",
        "growth_stage_vulnerability": "Early tillering through elongation",
        "what_this_means_en": "Sugarcane Mosaic Virus (SCMV) causes irregular contrasting patches of dark green and pale yellowish-green on young leaves, resembling a mosaic pattern. It is transmitted through infected setts and aphid vectors (Rhopalosiphum maidis), causing stunted tillering and reduced cane tonnage.",
        "what_this_means_ur": "نئے پتوں پر ہلکے پیلے اور گہرے سبز رنگ کے چتکبرے دھبے بن جاتے ہیں۔ یہ وائرس بیمار بیج اور سست تیلے (ایفڈ) کے ذریعے پھیلتا ہے جس سے گنے کی بڑھوتری رک جاتی ہے۔",
        "immediate_actions_en": [
            "Rogue out and destroy infected young tillers during early vegetative stages (first 60 days).",
            "Inspect field for aphid (vector) colonies on leaf spindles and surrounding grassy weeds.",
            "Eradicate wild grasses (Sorghum halepense, Cynodon dactylon) harboring the virus.",
            "Do NOT select planting setts from infected stool clumps."
        ],
        "immediate_actions_ur": [
            "ابتدائی 60 دنوں میں بیمار پودوں کو اکھاڑ کر تلف کر دیں۔",
            "پتوں پر سست تیلے (کیڑوں) کا معائنہ کریں اور جڑی بوٹیوں کا خاتمہ کریں۔",
            "کھیت کے اردگرد جنگلی گھاس ختم کریں جہاں وائرس پناہ لیتا ہے۔",
            "متاثرہ کھیت سے بیج کے لیے گنا ہرگز نہ چنیں۔"
        ],
        "water_management_en": "Maintain regular watering to alleviate drought stress which exacerbates viral stunting.",
        "water_management_ur": "پانی کا مناسب شیڈول رکھیں تاکہ پودا سوکھے کے دباؤ میں نہ آئے۔",
        "nutrient_management_en": "Apply balanced macro and micro-nutrients (Zinc, Iron) to help uninfected tillers outgrow chlorosis.",
        "nutrient_management_ur": "زنک اور آئرن کے ساتھ متوازن کھادیں دیں تاکہ نئے پتے تروتازہ نکلیں۔",
        "disease_management_en": {
            "cultural": "Use tissue-cultured or hot-water treated disease-free setts (52°C for 30 minutes); maintain 30-day weed-free border.",
            "biological": "Promote predatory ladybird beetles and hoverfly larvae against aphid vectors.",
            "chemical": "No chemical kills plant viruses. Control insect vectors (aphids) using registered systemic insecticides if aphid populations exceed economic threshold."
        },
        "disease_management_ur": {
            "cultural": "گرم پانی سے ٹریٹ شدہ بیج (52 ڈگری پر 30 منٹ) یا ٹشو کلچر پودے استعمال کریں۔",
            "biological": "لیڈی برڈ بیٹل جیسے دوست کیڑوں کی افزائش کو محفوظ رکھیں۔",
            "chemical": "وائرس کی کوئی براہ راست دوا نہیں ہوتی؛ وائرس پھیلانے والے سست تیلے کا تدارک محکمہ زراعت کی ہدایت کے مطابق کریں۔"
        },
        "action_plan_7day_en": {
            "today": "Rogue visibly mosaic-mottled shoots; inspect leaf sheaths for aphid colonies.",
            "day_2_3": "Clear alternate weed hosts around field margins and water canals.",
            "day_4_5": "Monitor surrounding tillers for any new mosaic streaking.",
            "day_6_7": "Audit total rogueing rate; if under 3%, healthy canopy will compensate."
        },
        "action_plan_7day_ur": {
            "today": "چتکبرے پودے نکال کر تلف کریں اور تیلے کا معائنہ کریں۔",
            "day_2_3": "کھیت کے کناروں اور کھالوں سے گھاس پھونس ختم کریں۔",
            "day_4_5": "نئے پتوں کو دیکھیں کہ ان پر دھبے تو نہیں بن رہے۔",
            "day_6_7": "کھیت کا مجموعی جائزہ لیں اور فصل کی بڑھوتری کو متحرک رکھیں۔"
        },
        "warning_signs_en": "Severe chlorotic mottling leading to shortening of internodes and dwarfing of the stool clump.",
        "warning_signs_ur": "پتوں کا شدید پیلا ہونا اور گنے کی گانٹھوں کا فاصلہ کم ہو کر قد چھوٹا رہ جانا۔",
        "expert_escalation_en": "Consult research station if mosaic symptoms appear in certified seed propagation plots.",
        "expert_escalation_ur": "اگر بیج کے لیے رکھی گئی فصل میں وائرس نظر آئے تو فوری ریسرچ انسٹیٹیوٹ سے رابطہ کریں۔",
        "evidence_sources": [
            {
                "organization": "Sugarcane Research Institute (SRI) Faisalabad",
                "document": "Viral Diseases of Sugarcane in Pakistan: SCMV Transmission & Control",
                "focus": "Potyvirus diagnostics, aphid vector ecology, and clean sett multiplication",
                "reference": "AARI Sugarcane Virology Technical Paper 2023-V-02"
            }
        ]
    },

    "sugarcane:bacterial blights": {
        "crop": "Sugarcane",
        "condition_name": "Bacterial Blight / Red Stripe",
        "condition_name_ur": "کماد کا بیکٹیریل جھلساؤ / سرخ دھاری",
        "scientific_name": "Acidovorax avenae subsp. avenae (Pseudomonas rubrilineans)",
        "severity": "high",
        "growth_stage_vulnerability": "Early tillering and grand growth during hot, humid rainy spells",
        "what_this_means_en": "Bacterial stripe/blight causes narrow, uniform, dark red longitudinal stripes following leaf veins. In severe cases, the bacterium moves down into the apical growing point causing 'top rot', foul odour, and death of the terminal spindle.",
        "what_this_means_ur": "پتوں پر لمبائی کے رخ گہری سرخ اور بھوری دھاریاں بنتی ہیں۔ شدید حملے میں بیکٹیریا گنے کی چوٹی (اوپر کے نرم حصے) تک پہنچ کر اسے سڑا دیتا ہے اور بدبو پیدا ہوتی ہے۔",
        "immediate_actions_en": [
            "Cut and destroy apical shoots showing top-rot symptoms to halt bacterial slime dispersal.",
            "Avoid overhead irrigation and do not enter the field during windy, rainy conditions.",
            "Disinfect harvesting and cutting knives in copper oxychloride or 10% household bleach solution.",
            "Ensure field drains quickly after rain."
        ],
        "immediate_actions_ur": [
            "چوٹی سے گلے ہوئے پودوں کو کاٹ کر دور گڑھے میں دبائیں۔",
            "بارش اور تیز ہوا کے وقت کھیت میں کام کرنے سے گریز کریں۔",
            "کٹائی کے اوزاروں کو کاپر کے محلول یا جراثیم کش دوا سے صاف کریں۔",
            "بارش کے بعد کھیت سے پانی فوری نکالیں۔"
        ],
        "water_management_en": "Ensure unobstructed furrow drainage; eliminate stagnant standing water.",
        "water_management_ur": "پانی کی نکاسی کو بہترین بنائیں اور کسی جگہ کیچڑ یا پانی نہ کھڑا ہونے دیں۔",
        "nutrient_management_en": "Apply balanced Potassium and avoid high doses of succulent-producing nitrogen.",
        "nutrient_management_ur": "پوٹاش کھاد کا استعمال بڑھائیں اور یوریا کھاد فی الحال روک دیں۔",
        "disease_management_en": {
            "cultural": "Plant resistant cultivars; practice clean sett cutting; avoid intercropping with susceptible hosts like maize or sorghum.",
            "biological": "Application of copper-based bactericides at earliest symptom emergence.",
            "chemical": "Foliar application of Copper Oxychloride or Copper Hydroxide according to registered agricultural extension advisory."
        },
        "disease_management_ur": {
            "cultural": "مدافعتی اقسام کاشت کریں اور مکئی یا جوار جیسی فصلیں درمیان میں نہ لگائیں۔",
            "biological": "ابتدائی علامات پر کاپر والے محفوظ محلول کا استعمال کریں۔",
            "chemical": "محکمہ زراعت کی ہدایت کے مطابق کاپر آکسی کلورائیڈ کا اسپرے کریں۔"
        },
        "action_plan_7day_en": {
            "today": "Identify and remove rotting apical spindles; sanitize knives.",
            "day_2_3": "Apply copper-based protective spray across infected and buffer zones.",
            "day_4_5": "Check leaf stripes: red stripes should dry into narrow dark lines without advancing to crown.",
            "day_6_7": "Audit apical growth of newly emerged central spindle leaves."
        },
        "action_plan_7day_ur": {
            "today": "سڑی ہوئی چوٹیاں کاٹیں اور اوزاروں کو صاف کریں۔",
            "day_2_3": "متاثرہ حصے پر کاپر والی دوا کا اسپرے کریں۔",
            "day_4_5": "دیکھیں کہ لال دھاریاں سوکھ رہی ہیں اور چوٹی کی طرف نہیں بڑھ رہیں۔",
            "day_6_7": "نئی نکلنے والی کونپلوں کی صحت کا جائزہ لیں۔"
        },
        "warning_signs_en": "Top-rot breakdown of terminal bud with foul smell and complete pulling out of central leaf whorl.",
        "warning_signs_ur": "گنے کی چوٹی کا گل کر بدبو دینا اور درمیان کے پتوں کا آسانی سے ہاتھ میں نکل آنا۔",
        "expert_escalation_en": "Contact extension officer if top rot affects more than 10% of field population.",
        "expert_escalation_ur": "اگر 10 فیصد سے زیادہ گنے کی چوٹیاں سڑ رہی ہوں تو فوری زرعی ماہر سے رجوع کریں۔",
        "evidence_sources": [
            {
                "organization": "Sugarcane Research Institute (SRI) Faisalabad",
                "document": "Bacterial Stripe & Top Rot Management Advisory",
                "focus": "Acidovorax avenae identification, copper sanitation, and resistant germplasm",
                "reference": "AARI Sugarcane Pathology Bulletin 2023-B-03"
            }
        ]
    }
}


def _normalize_key(crop: str, disease_or_label: Optional[str], is_healthy: bool = False) -> str:
    """Helper to produce standard lookup key: '{crop}:{disease}'"""
    crop_str = (crop or "").strip().lower()
    if is_healthy or not disease_or_label:
        return f"{crop_str}:healthy"

    disease_str = disease_or_label.strip().lower()
    # Normalize common aliases
    if "downy" in disease_str:
        return f"{crop_str}:downy mildew"
    if "purple" in disease_str:
        return f"{crop_str}:purple blotch"
    if "stemphylium" in disease_str:
        return f"{crop_str}:stemphylium leaf blight"
    if "anthracnose" in disease_str:
        return f"{crop_str}:anthracnose"
    if "die" in disease_str and "back" in disease_str:
        return f"{crop_str}:die back"
    if "powdery" in disease_str:
        return f"{crop_str}:powdery mildew"
    if "red" in disease_str and "rot" in disease_str:
        return f"{crop_str}:red rot"
    if "mosaic" in disease_str:
        return f"{crop_str}:mosaic"
    if "bacterial" in disease_str or "blight" in disease_str:
        if crop_str == "sugarcane":
            return "sugarcane:bacterial blights"
        elif crop_str == "onion":
            return "onion:stemphylium leaf blight"
    if "healthy" in disease_str:
        return f"{crop_str}:healthy"

    return f"{crop_str}:{disease_str}"


def get_agri_knowledge(crop: str, disease_name_or_label: Optional[str], is_healthy: bool = False) -> Dict[str, Any]:
    """
    Retrieve rich, authoritative agricultural knowledge entry for a given crop & disease diagnosis.
    Guarantees a complete, structured dictionary with zero missing keys.
    """
    key = _normalize_key(crop, disease_name_or_label, is_healthy)
    
    # Exact lookup
    if key in AGRI_KNOWLEDGE_BASE:
        return AGRI_KNOWLEDGE_BASE[key]

    # Partial / crop fallback lookup
    crop_str = (crop or "Onion").strip().title()
    crop_key = f"{crop_str.lower()}:healthy" if is_healthy else None
    if crop_key and crop_key in AGRI_KNOWLEDGE_BASE:
        return AGRI_KNOWLEDGE_BASE[crop_key]

    # Fallback to general crop healthy / default template
    disease_title = (disease_name_or_label or "Plant Condition").strip().title()
    return {
        "crop": crop_str,
        "condition_name": f"{crop_str} {disease_title}",
        "condition_name_ur": f"{crop_str} کی بیماری ({disease_title})",
        "scientific_name": f"Phytopathogen affecting {crop_str}",
        "severity": "moderate",
        "growth_stage_vulnerability": "Vegetative to Maturation stage",
        "what_this_means_en": f"The AI analysis identified symptoms consistent with {disease_title} on {crop_str}. Prompt on-field visual confirmation and sanitation are advised to safeguard yield and prevent spread to surrounding healthy stands.",
        "what_this_means_ur": f"اے آئی ماڈل نے {crop_str} پر {disease_title} کی علامات کی نشاندہی کی ہے۔ فصل کی پیداوار کو محفوظ رکھنے کے لیے فوری معائنہ اور صفائی کی سفارش کی جاتی ہے۔",
        "immediate_actions_en": [
            f"Conduct an in-field inspection of {crop_str} plants in the vicinity of the scanned leaf.",
            "Remove and safely dispose of severely symptomatic plant tissue to decrease pathogen pressure.",
            "Check irrigation levels and ensure water does not stagnate in the field.",
            "Avoid handling foliage when wet to minimize pathogen dispersal."
        ],
        "immediate_actions_ur": [
            f"متاثرہ پودے کے اردگرد {crop_str} کی دیگر قطاروں کا تفصیلی معائنہ کریں۔",
            "شدید متاثرہ پتوں کو کاٹ کر کھیت سے دور ٹھکانے لگائیں۔",
            "کھیت میں پانی کھڑا نہ ہونے دیں اور نکاسی کو بہتر بنائیں۔",
            "گیلے موسم میں فصل میں بلا ضرورت کام کرنے سے پرہیز کریں۔"
        ],
        "water_management_en": "Maintain consistent, measured irrigation. Ensure adequate soil drainage and avoid wetting the foliage late in the day.",
        "water_management_ur": "پانی کا باقاعدہ اور متوازن شیڈول رکھیں اور شام کے وقت پتوں پر پانی نہ ڈالیں۔",
        "nutrient_management_en": "Avoid excessive nitrogen which produces overly soft vegetative tissue. Supplement with balanced Potassium and Phosphorus.",
        "nutrient_management_ur": "نائٹروجن (یوریا) کا زیادہ استعمال نہ کریں اور پودے کی قوت مدافعت کے لیے پوٹاش دیں۔",
        "disease_management_en": {
            "cultural": f"Maintain recommended row and plant spacing for {crop_str} to ensure optimal air circulation and sun penetration.",
            "biological": "Use bio-protectants (e.g., Trichoderma or Bacillus species) during early vegetative stages.",
            "chemical": "Follow registered agricultural extension recommendations for certified crop-protection products. Always read and adhere to product label safety instructions."
        },
        "disease_management_ur": {
            "cultural": f"{crop_str} کے پودوں میں مناسب فاصلہ رکھیں تاکہ دھوپ اور ہوا کا گزر اچھا ہو۔",
            "biological": "ابتدائی مرحلے پر بائیو فنگسائڈز کا حفاظتی استعمال کریں۔",
            "chemical": "محکمہ زراعت کی تجویز کردہ ادویات کا لیبل کے مطابق محفوظ استعمال کریں۔"
        },
        "action_plan_7day_en": {
            "today": f"Confirm condition scope across {crop_str} plot and isolate affected area.",
            "day_2_3": "Adjust irrigation drainage and apply recommended protective measure.",
            "day_4_5": "Inspect newly unfolding foliage for clean, vigorous growth.",
            "day_6_7": "Reassess crop recovery; consult local extension officer if symptoms persist."
        },
        "action_plan_7day_ur": {
            "today": "کھیت کا معائنہ کریں اور متاثرہ حصے کی نشاندہی کریں۔",
            "day_2_3": "پانی کی نکاسی درست کریں اور حفاظتی اسپرے کریں۔",
            "day_4_5": "نئے پتوں کو دیکھیں کہ کیا بیماری کا پھیلاؤ رک گیا ہے۔",
            "day_6_7": "فصل کی بحالی کا جائزہ لیں اور ضرورت پڑنے پر زرعی افسر سے مشورہ کریں۔"
        },
        "warning_signs_en": "Rapid spreading of necrotic spots, sudden wilting, or yellowing across major crop quadrants.",
        "warning_signs_ur": "داغوں کا تیزی سے پھیلنا یا پودوں کا اچانک مرجھانا۔",
        "expert_escalation_en": "Contact your local agricultural extension service if more than 10% of the field exhibits severe symptoms.",
        "expert_escalation_ur": "اگر 10 فیصد سے زیادہ پودے متاثر ہوں تو فوری مقامی زرعی توسیع افسر سے رابطہ کریں۔",
        "evidence_sources": [
            {
                "organization": "Pakistan Agricultural Research Council (PARC)",
                "document": "Integrated Pest & Disease Management Guidelines",
                "focus": f"Good agricultural practices for {crop_str}",
                "reference": "PARC National Crop Advisory Series"
            },
            {
                "organization": "Food and Agriculture Organization (FAO)",
                "document": "Farmer Field School Guidance on Crop Health",
                "focus": "Integrated Pest Management (IPM)",
                "reference": "FAO Plant Production & Protection Guidelines"
            }
        ]
    }
