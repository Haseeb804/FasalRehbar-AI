from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Crop, Disease


class Command(BaseCommand):
    help = 'Populate database with Mango, Onion, and Sugarcane crops with their diseases'

    def handle(self, *args, **options):
        # Define crops and their diseases
        crops_data = {
            'Mango': {
                'scientific_name': 'Mangifera indica',
                'description': 'Mango is a tropical fruit tree widely cultivated in Pakistan.',
                'diseases': [
                    {
                        'name': 'Anthracnose',
                        'description': 'Fungal disease affecting mango fruits and leaves',
                        'symptoms': 'Dark, sunken lesions on fruits and leaves; premature fruit drop; twig dieback',
                        'causes': 'Colletotrichum gloeosporioides fungus',
                        'prevention': 'Remove infected plant parts; improve air circulation; use resistant varieties',
                        'treatment': 'Apply copper fungicides; prune affected branches; maintain proper canopy management',
                        'severity': 'high',
                    },
                    {
                        'name': 'Powdery Mildew',
                        'description': 'Fungal disease causing white powder on leaves',
                        'symptoms': 'White powdery coating on leaves and fruits; leaf curling; fruit spotting',
                        'causes': 'Oidium mangferae fungus',
                        'prevention': 'Ensure good ventilation; avoid overhead irrigation; plant in sunny locations',
                        'treatment': 'Apply sulfur-based fungicides; use neem oil spray; remove infected leaves',
                        'severity': 'medium',
                    },
                    {
                        'name': 'Stem Canker',
                        'description': 'Fungal disease causing cankers on stems and branches',
                        'symptoms': 'Sunken cankers on stems; gum oozing; branch dieback; tree decline',
                        'causes': 'Botryodiplodia theobromae fungus',
                        'prevention': 'Remove dead branches; avoid tree injuries; improve drainage',
                        'treatment': 'Prune infected branches; apply fungicide to cut surfaces; sterilize tools',
                        'severity': 'high',
                    },
                ]
            },
            'Onion': {
                'scientific_name': 'Allium cepa',
                'description': 'Onion is a widely cultivated bulb crop in Pakistan.',
                'diseases': [
                    {
                        'name': 'Fusarium Basal Rot',
                        'description': 'Fungal disease causing bulb rot at the base',
                        'symptoms': 'Brown rot at bulb base; wilting of foliage; root decay; bulb discoloration',
                        'causes': 'Fusarium oxysporum f.sp. cepae fungus',
                        'prevention': 'Use disease-free seeds; improve soil drainage; crop rotation; avoid waterlogging',
                        'treatment': 'Remove infected plants; use resistant varieties; apply fungicides to soil',
                        'severity': 'critical',
                    },
                    {
                        'name': 'Purple Blotch',
                        'description': 'Fungal disease causing purple spots on leaves',
                        'symptoms': 'Purple or brown concentric rings on leaves; leaf necrosis; premature leaf death',
                        'causes': 'Alternaria porri fungus',
                        'prevention': 'Maintain proper spacing; improve air circulation; avoid excessive nitrogen',
                        'treatment': 'Apply copper-based fungicides; remove infected leaves; use resistant varieties',
                        'severity': 'high',
                    },
                    {
                        'name': 'Downy Mildew',
                        'description': 'Oomycete disease causing gray mold on leaves',
                        'symptoms': 'Gray or white mold on leaf surface; leaf yellowing; distorted growth',
                        'causes': 'Peronospora destructor oomycete',
                        'prevention': 'Improve air circulation; avoid overhead watering; maintain proper spacing',
                        'treatment': 'Apply mancozeb fungicide; remove infected leaves; improve drainage',
                        'severity': 'medium',
                    },
                ]
            },
            'Sugarcane': {
                'scientific_name': 'Saccharum officinarum',
                'description': 'Sugarcane is an important cash crop grown in Pakistan.',
                'diseases': [
                    {
                        'name': 'Red Rot',
                        'description': 'Fungal disease causing internal cane rot',
                        'symptoms': 'Red discoloration inside cane; foul smell; tiller wilting; leaf yellowing',
                        'causes': 'Colletotrichum falcatum fungus',
                        'prevention': 'Use disease-free seed cane; practice crop rotation; control insects',
                        'treatment': 'Remove infected plants; use resistant varieties; apply fungicides to seed cane',
                        'severity': 'critical',
                    },
                    {
                        'name': 'Wilt Disease',
                        'description': 'Bacterial disease causing vascular wilt',
                        'symptoms': 'Yellowing of leaves; wilting of shoots; stunted growth; red vascular discoloration',
                        'causes': 'Xanthomonas campestris bacteria',
                        'prevention': 'Use resistant varieties; avoid contaminated tools; practice sanitation',
                        'treatment': 'Remove infected tillers; disinfect equipment; improve field drainage',
                        'severity': 'high',
                    },
                    {
                        'name': 'Leaf Scald',
                        'description': 'Bacterial disease causing leaf scald symptoms',
                        'symptoms': 'White, narrow lines along leaf veins; leaf yellowing; reduced growth',
                        'causes': 'Xanthomonas albilineans bacteria',
                        'prevention': 'Use disease-free seed cane; control insects; practice crop sanitation',
                        'treatment': 'Remove infected plants; apply copper fungicides; use resistant varieties',
                        'severity': 'high',
                    },
                ]
            }
        }

        # Create crops and diseases
        for crop_name, crop_info in crops_data.items():
            crop, created = Crop.objects.get_or_create(
                name=crop_name,
                defaults={
                    'scientific_name': crop_info['scientific_name'],
                    'description': crop_info['description'],
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created crop: {crop_name}'))
            else:
                self.stdout.write(f'→ Crop already exists: {crop_name}')

            # Create diseases for this crop
            for disease_data in crop_info['diseases']:
                disease, disease_created = Disease.objects.get_or_create(
                    name=disease_data['name'],
                    defaults={
                        'crop': crop,
                        'slug': slugify(disease_data['name']),
                        'description': disease_data['description'],
                        'symptoms': disease_data['symptoms'],
                        'causes': disease_data['causes'],
                        'prevention': disease_data['prevention'],
                        'treatment': disease_data['treatment'],
                        'severity': disease_data['severity'],
                        'is_active': True,
                    }
                )
                
                if disease_created:
                    self.stdout.write(f'  ✓ Added disease: {disease_data["name"]}')
                else:
                    self.stdout.write(f'  → Disease already exists: {disease_data["name"]}')

        self.stdout.write(self.style.SUCCESS('\n✓ Database seeding completed successfully!'))
