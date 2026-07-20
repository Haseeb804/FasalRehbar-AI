"""
Fills in DRAFT knowledge-base content (description/symptoms/causes/treatment/
prevention/severity) for commonly-known disease names, so the admin panel isn't
completely blank after `sync_ml_metadata` creates the Disease rows.

Only fills rows that are currently blank / flagged needs_content=True — never
overwrites content an admin has already written. Matches by (crop, disease name)
case-insensitively, so it's safe to re-run any time.

IMPORTANT: this is a reasonable starting draft, not verified agricultural
advice — review and edit every entry (ideally with an agronomist) before
relying on it in production. Farmers may act on this directly.

Usage:
    python manage.py seed_disease_content
"""
from django.core.management.base import BaseCommand

from core.models import Crop, Disease

# crop_name -> { disease display name (case-insensitive match) -> content dict }
DRAFT_CONTENT = {
    "Mango": {
        "anthracnose": dict(
            description="Fungal disease affecting mango fruits, leaves, and twigs, one of the most common and destructive mango diseases.",
            symptoms="Dark, sunken lesions on fruits and leaves; premature fruit drop; leaf spots that merge into larger blighted areas; twig dieback.",
            causes="Caused by the fungus Colletotrichum gloeosporioides, spread by rain splash and high humidity.",
            treatment="Remove and destroy infected plant material. Apply copper-based fungicide sprays at flowering and fruit development stages. In severe cases, systemic fungicides (e.g. carbendazim) may be used under expert guidance.",
            prevention="Prune for good air circulation, avoid overhead irrigation, remove fallen infected leaves/fruit, use disease-free planting material.",
            severity=Disease.Severity.HIGH,
        ),
        "bacterial canker": dict(
            description="Bacterial disease causing raised, corky lesions on leaves, stems, and fruit.",
            symptoms="Water-soaked, angular leaf spots that turn dark brown/black; raised corky lesions on fruit; stem cankers with gum exudation.",
            causes="Caused by Xanthomonas campestris pv. mangiferaeindicae, spread by wind-driven rain and contaminated tools.",
            treatment="Prune and destroy infected branches (disinfect tools between cuts). Apply copper-based bactericides. Avoid working in the orchard during wet weather to limit spread.",
            prevention="Use disease-free planting material, avoid overhead irrigation, disinfect pruning tools, apply preventive copper sprays before the rainy season.",
            severity=Disease.Severity.HIGH,
        ),
        "cutting weevil": dict(
            description="Insect pest (not a fungal/bacterial disease) whose larvae bore into mango stems and shoots.",
            symptoms="Wilting and drying of shoot tips; small entry holes in stems/twigs; sawdust-like frass near boreholes; dieback of affected shoots.",
            causes="Larvae of the mango stem borer/cutting weevil tunneling inside young shoots and stems.",
            treatment="Prune and destroy infested shoots below the boring point. Apply recommended insecticide (e.g. based on local agricultural extension guidance) to new growth during the pest's active season.",
            prevention="Regular orchard monitoring for wilting shoots, prompt removal of infested material, maintaining tree vigor.",
            severity=Disease.Severity.MEDIUM,
        ),
        "die back": dict(
            description="Progressive drying and death of branches starting from the tip, usually fungal in origin.",
            symptoms="Twig and branch tips dry out and turn brown/black, progressing backward toward the trunk; gum exudation; leaf drop on affected branches.",
            causes="Commonly associated with Botryodiplodia theobromae and other fungi, often following stress, injury, or waterlogging.",
            treatment="Prune well below the visibly affected area and destroy prunings. Apply fungicide paste to cut surfaces. Improve tree vigor with balanced fertilization.",
            prevention="Avoid mechanical injury and waterlogging, maintain balanced nutrition, remove dead wood promptly.",
            severity=Disease.Severity.HIGH,
        ),
        "gall midge": dict(
            description="Insect pest causing gall formation on mango leaves, shoots, and inflorescences.",
            symptoms="Small raised galls on leaves and young shoots; distorted or stunted growth; premature leaf/flower drop in heavy infestations.",
            causes="Larvae of mango gall midge species developing inside plant tissue, inducing gall formation.",
            treatment="Remove and destroy heavily galled leaves/shoots. Insecticide application timed to adult emergence, per local agricultural extension recommendations.",
            prevention="Orchard sanitation (removing fallen infested leaves), monitoring during flowering/flushing periods.",
            severity=Disease.Severity.MEDIUM,
        ),
        "healthy": dict(
            description="No disease detected — the plant tissue appears healthy.",
            symptoms="No visible symptoms of disease or pest damage.",
            causes="Not applicable.",
            treatment="No treatment needed. Continue regular monitoring and good agricultural practices.",
            prevention="Maintain proper irrigation, balanced fertilization, and regular pest/disease scouting.",
            severity=Disease.Severity.LOW,
        ),
        "powdery mildew": dict(
            description="Fungal disease producing a white powdery coating on leaves, flowers, and young fruit.",
            symptoms="White powdery patches on leaves and inflorescences; leaf curling and distortion; flower and young fruit drop.",
            causes="Caused by Oidium mangiferae, favored by cool nights and high humidity during flowering.",
            treatment="Apply sulfur-based or systemic fungicides at early flowering. Neem oil spray can help in mild cases.",
            prevention="Ensure good canopy ventilation, avoid dense planting, monitor closely during flowering season.",
            severity=Disease.Severity.MEDIUM,
        ),
        "sooty mould": dict(
            description="Fungal growth forming a black sooty coating on leaves, usually secondary to sap-sucking insect infestation.",
            symptoms="Black, soot-like coating on leaf and fruit surfaces; reduced photosynthesis; sticky honeydew residue underneath the mould.",
            causes="Grows on honeydew excreted by sap-sucking insects (e.g. mealybugs, scale insects, hoppers); the mould itself is secondary to the pest issue.",
            treatment="Control the underlying sap-sucking insect population (insecticidal soap or recommended insecticide). Wash affected leaves; the mould itself typically clears once honeydew source is controlled.",
            prevention="Regular monitoring and control of sap-sucking insects, maintaining orchard hygiene.",
            severity=Disease.Severity.LOW,
        ),
    },
    "Sugarcane": {
        "healthy": dict(
            description="No disease detected — the plant tissue appears healthy.",
            symptoms="No visible symptoms of disease.",
            causes="Not applicable.",
            treatment="No treatment needed. Continue regular monitoring and good agricultural practices.",
            prevention="Maintain proper irrigation, balanced fertilization, and regular field scouting.",
            severity=Disease.Severity.LOW,
        ),
        "bacterial blights": dict(
            description="Bacterial disease causing elongated water-soaked lesions on sugarcane leaves.",
            symptoms="Long, narrow, water-soaked streaks on leaves that turn brown/necrotic with a yellow halo; lesions may merge and cause leaf blighting.",
            causes="Caused by Xanthomonas species, spread by rain splash, contaminated tools, and infected planting material.",
            treatment="Remove and destroy severely affected leaves. Apply copper-based bactericide in outbreak conditions. Use disease-free seed cane for future planting.",
            prevention="Use certified disease-free seed cane, disinfect cutting tools between plants, avoid working fields during wet weather, ensure good field drainage.",
            severity=Disease.Severity.MEDIUM,
        ),
        "mosaic": dict(
            description="Viral disease causing a characteristic mosaic pattern of light and dark green patches on leaves.",
            symptoms="Irregular light-green/yellow and dark-green mottled patches on leaves; stunted growth in severe infections; reduced cane yield.",
            causes="Caused by Sugarcane mosaic virus (SCMV), spread mainly by aphids and infected planting material.",
            treatment="No cure once infected — remove and destroy severely infected plants to reduce spread. Use certified virus-free seed cane for future planting.",
            prevention="Plant only certified disease-free seed cane, control aphid vectors, rogue out infected plants early in the season.",
            severity=Disease.Severity.HIGH,
        ),
        "red rot": dict(
            description="One of the most destructive sugarcane diseases, causing internal reddening and rotting of the stalk.",
            symptoms="Red discoloration with white cross-bands inside the stalk when cut open; drying of leaves (top downward); alcohol-like smell from rotting tissue.",
            causes="Caused by the fungus Colletotrichum falcatum, spreads through infected seed cane and soil, favored by waterlogging.",
            treatment="No effective in-season cure. Remove and burn severely infected clumps. Use resistant varieties for replanting; treat seed cane with fungicide before planting.",
            prevention="Use certified disease-resistant varieties, treat seed sets with fungicide, avoid waterlogging, practice crop rotation.",
            severity=Disease.Severity.CRITICAL,
        ),
        "rust": dict(
            description="Fungal disease producing rust-colored pustules on sugarcane leaves.",
            symptoms="Orange-brown elongated pustules on leaf surfaces, mainly on the underside; premature leaf drying in severe cases.",
            causes="Caused by Puccinia melanocephala or P. kuehnii, favored by high humidity and moderate temperatures.",
            treatment="Fungicide application (e.g. propiconazole-based) in severe outbreaks. Usually manageable through resistant varieties rather than chemical control alone.",
            prevention="Plant rust-resistant varieties, avoid excessive nitrogen fertilization, ensure adequate field spacing for airflow.",
            severity=Disease.Severity.MEDIUM,
        ),
        "yellow": dict(
            description="Yellow leaf disease/discoloration, associated with Sugarcane yellow leaf virus or nutrient-related yellowing.",
            symptoms="Yellowing of the midrib on the underside of leaves, progressing to overall leaf yellowing and reddening; stunted growth.",
            causes="Commonly associated with Sugarcane yellow leaf virus (ScYLV), transmitted by aphids; can also reflect nutrient deficiency in some cases.",
            treatment="No direct cure for viral cases — remove severely affected stools. Confirm whether nutrient deficiency is a contributing factor and correct fertilization accordingly.",
            prevention="Use certified virus-free seed cane, control aphid vectors, maintain balanced soil nutrition.",
            severity=Disease.Severity.MEDIUM,
        ),
    },
    "Onion": {
        "healthy": dict(
            description="No disease detected — the plant tissue appears healthy.",
            symptoms="No visible symptoms of disease.",
            causes="Not applicable.",
            treatment="No treatment needed. Continue regular monitoring and good agricultural practices.",
            prevention="Maintain proper irrigation, balanced fertilization, and regular field scouting.",
            severity=Disease.Severity.LOW,
        ),
        "alternaria": dict(
            description="Fungal leaf blight caused by Alternaria species, common in humid conditions.",
            symptoms="Small water-soaked lesions that enlarge into concentric brown/purple rings on leaves; leaf tip dieback.",
            causes="Caused by Alternaria porri, favored by high humidity and leaf wetness.",
            treatment="Apply appropriate fungicide (e.g. mancozeb or chlorothalonil-based) at first sign of lesions; remove severely affected leaves.",
            prevention="Avoid overhead irrigation, ensure good field drainage and spacing, rotate crops.",
            severity=Disease.Severity.HIGH,
        ),
        "botrytis leaf blight": dict(
            description="Fungal disease causing blighting of onion leaves, especially in cool, wet conditions.",
            symptoms="Small white flecks on leaves that expand into blighted, water-soaked patches; leaf tip collapse in severe cases.",
            causes="Caused by Botrytis species, favored by cool temperatures and prolonged leaf wetness.",
            treatment="Fungicide application at early symptom onset; remove and destroy heavily blighted foliage.",
            prevention="Improve field air circulation, avoid excess nitrogen, avoid overhead irrigation during cool weather.",
            severity=Disease.Severity.MEDIUM,
        ),
        "bulb rot": dict(
            description="Post-harvest or field bulb rot, often fungal or bacterial in origin.",
            symptoms="Soft, discolored, foul-smelling bulb tissue; watery rot starting at the neck or base of the bulb.",
            causes="Multiple possible pathogens (e.g. Fusarium, bacterial soft rot organisms), often following injury, excess moisture, or poor curing.",
            treatment="Remove and discard affected bulbs immediately to prevent spread in storage. No treatment reverses rot once established.",
            prevention="Cure bulbs properly before storage, avoid bulb injury during harvest, ensure good field drainage, store in cool/dry, well-ventilated conditions.",
            severity=Disease.Severity.CRITICAL,
        ),
        "bulb blight": dict(
            description="Fungal blight affecting onion bulbs and neck tissue.",
            symptoms="Water-soaked lesions on the neck/bulb, progressing to soft rot; discoloration of internal bulb scales.",
            causes="Commonly fungal in origin, favored by wet conditions at harvest and poor curing.",
            treatment="Remove affected bulbs from storage; fungicide seed/soil treatment for future plantings.",
            prevention="Proper curing and drying after harvest, avoid mechanical damage, ensure good storage ventilation.",
            severity=Disease.Severity.HIGH,
        ),
        "caterpillar": dict(
            description="Insect pest damage from caterpillar larvae feeding on onion leaves.",
            symptoms="Irregular chewed patches or holes in leaves; visible larvae or frass on foliage; leaf tip damage.",
            causes="Feeding damage from lepidopteran larvae (various species depending on region).",
            treatment="Hand-picking larvae in small plots; recommended insecticide application for larger infestations, following local agricultural extension guidance.",
            prevention="Regular field scouting, encourage natural predators, remove crop debris that harbors larvae/pupae.",
            severity=Disease.Severity.MEDIUM,
        ),
        "downy mildew": dict(
            description="Oomycete disease causing grayish-purple fuzzy growth on onion leaves, especially in cool, humid weather.",
            symptoms="Pale green to yellow oval lesions on leaves; grayish-purple fuzzy growth on the surface during humid mornings; leaf collapse in severe cases.",
            causes="Caused by Peronospora destructor, favored by cool temperatures, high humidity, and leaf wetness.",
            treatment="Fungicide application (e.g. mancozeb-based) at first symptoms; remove and destroy infected leaves.",
            prevention="Avoid overhead irrigation, ensure good field drainage and spacing, use resistant varieties where available.",
            severity=Disease.Severity.HIGH,
        ),
        "fusarium": dict(
            description="Fusarium basal rot, a serious soil-borne fungal disease of onion bulbs and roots.",
            symptoms="Yellowing and dieback of leaf tips progressing downward; brown, water-soaked rot at the bulb base; root decay.",
            causes="Caused by Fusarium oxysporum f. sp. cepae, persists in soil and spreads via infected sets/transplants.",
            treatment="Remove and destroy infected plants; no effective in-season chemical cure. Use resistant varieties and treated, disease-free seed/sets for future planting.",
            prevention="Crop rotation (avoid replanting onions in the same soil for several years), improve field drainage, use certified disease-free planting material.",
            severity=Disease.Severity.CRITICAL,
        ),
        "iris yellow virus": dict(
            description="Viral disease transmitted by thrips, causing characteristic straw-colored lesions on onion leaves and scapes.",
            symptoms="Straw-colored to yellow diamond-shaped or elongated lesions on leaves and flower stalks; scape collapse in severe infections.",
            causes="Caused by Iris yellow spot virus (IYSV), transmitted by onion thrips.",
            treatment="No direct cure — manage the thrips vector population with recommended insecticides to limit further spread.",
            prevention="Thrips control (monitoring and timely insecticide application), remove volunteer onions and weed hosts, avoid planting near infected fields.",
            severity=Disease.Severity.HIGH,
        ),
        "purple blotch": dict(
            description="Common fungal foliar disease of onion causing purple-brown lesions with concentric rings.",
            symptoms="Small whitish sunken spots that enlarge into purple-brown lesions with concentric zonation; leaf tip dieback and lodging.",
            causes="Caused by Alternaria porri, favored by warm, humid weather and leaf wetness.",
            treatment="Apply fungicide (e.g. mancozeb or chlorothalonil-based) at early symptoms; remove severely infected leaves.",
            prevention="Avoid overhead irrigation, maintain adequate plant spacing for airflow, rotate crops, avoid excess nitrogen.",
            severity=Disease.Severity.HIGH,
        ),
        "rust": dict(
            description="Fungal disease producing orange rust pustules on onion leaves.",
            symptoms="Small orange to brown raised pustules on leaves, may merge in severe infections; premature leaf drying.",
            causes="Caused by Puccinia species, favored by cool, humid conditions.",
            treatment="Fungicide application in severe cases; usually a secondary concern compared to other onion diseases.",
            prevention="Adequate field spacing, avoid excess nitrogen, remove volunteer onion plants that can harbor the fungus between seasons.",
            severity=Disease.Severity.LOW,
        ),
        "stemphylium leaf blight": dict(
            description="Fungal leaf blight, often appearing alongside or following purple blotch/downy mildew infections.",
            symptoms="Yellow to brown spindle-shaped lesions on leaves, often starting at leaf tips; premature leaf collapse.",
            causes="Caused by Stemphylium vesicarium, frequently a secondary invader following other leaf damage or infections.",
            treatment="Fungicide application at early symptoms; addressing any underlying primary infection (e.g. purple blotch) is important.",
            prevention="Avoid leaf wetness/overhead irrigation, ensure good airflow, manage other foliar diseases promptly.",
            severity=Disease.Severity.MEDIUM,
        ),
        "virosis": dict(
            description="General viral disease symptoms in onion (species/strain not always specified).",
            symptoms="Leaf mottling, yellowing, stunted growth, and distorted foliage.",
            causes="One or more onion-infecting viruses, often transmitted by insect vectors (aphids/thrips) or infected planting material.",
            treatment="No direct chemical cure — remove severely affected plants and manage the relevant insect vector.",
            prevention="Use certified virus-free planting material, control aphid/thrips populations, remove volunteer onions and weeds that host viruses.",
            severity=Disease.Severity.HIGH,
        ),
        "xanthomonas leaf blight": dict(
            description="Bacterial leaf blight affecting onion foliage.",
            symptoms="Water-soaked streaks or lesions on leaves that turn brown/necrotic; leaf tip dieback in severe cases.",
            causes="Caused by Xanthomonas species, spread by rain splash, irrigation water, and contaminated tools.",
            treatment="Copper-based bactericide application at early symptoms; remove severely affected leaves.",
            prevention="Avoid overhead irrigation, disinfect tools between fields, use disease-free planting material.",
            severity=Disease.Severity.MEDIUM,
        ),
    },
}


class Command(BaseCommand):
    help = "Fill in draft knowledge-base content for commonly-known disease names (non-destructive)."

    def handle(self, *args, **options):
        filled, skipped, unmatched = 0, 0, 0

        for crop_name, disease_map in DRAFT_CONTENT.items():
            crop = Crop.objects.filter(name__iexact=crop_name).first()
            if not crop:
                self.stdout.write(self.style.WARNING(f"Crop '{crop_name}' not found — run sync_ml_metadata first."))
                continue

            for key, content in disease_map.items():
                disease = Disease.objects.filter(crop=crop, name__iexact=key).first()
                if not disease:
                    continue  # this disease name isn't in your actual trained class list — fine, skip it

                if disease.description.strip():
                    skipped += 1
                    continue  # already has content — never overwrite

                for field, value in content.items():
                    setattr(disease, field, value)
                disease.needs_content = False
                disease.save()
                filled += 1
                self.stdout.write(f"  + Filled draft content for {crop_name}: {disease.name}")

        remaining = Disease.objects.filter(needs_content=True).count()
        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {filled} disease row(s) filled with draft content, {skipped} already had content."
        ))
        if remaining:
            self.stdout.write(self.style.WARNING(
                f"{remaining} disease row(s) still need content (no draft available for their exact name) — "
                f"fill these in manually via the admin panel."
            ))
