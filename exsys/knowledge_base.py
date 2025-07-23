"""
Knowledge Base for Plant Disease Expert System

This module contains the facts and rules for diagnosing plant diseases
based on observed symptoms.
"""

# Define the knowledge base as a dictionary of rules
# Format: 'disease': {'symptoms': [list of required symptoms], 'description': str, 'treatment': str, 'product_recommendations': list}
KNOWLEDGE_BASE = {
    'powdery_mildew': {
        'symptoms': ['white_powdery_patches', 'leaf_yellowing', 'distorted_growth'],
        'description': 'Powdery mildew is a fungal disease that affects a wide range of plants. '
                      'It appears as white powdery spots on leaves and stems.',
        'treatment': 'Apply fungicide, improve air circulation, and avoid overhead watering.',
        'product_recommendations': [
            {'name': 'Neem Oil Spray', 'type': 'Organic', 'description': 'Natural fungicide that also controls insects'},
            {'name': 'Potassium Bicarbonate', 'type': 'Organic', 'description': 'Effective treatment that also prevents spore germination'},
            {'name': 'Propiconazole Fungicide', 'type': 'Chemical', 'description': 'Systemic fungicide for severe infestations'}
        ],
        'severity_impact': {
            'low': 'Minimal spread, easily controllable with organic treatments',
            'medium': 'Moderate spread affecting multiple leaves, requires consistent treatment',
            'high': 'Severe infection affecting most of the plant, may require chemical treatments'
        },
        'plant_types': ['Rose', 'Cucumber', 'Tomato', 'Grape', 'Squash']
    },
    'leaf_spot': {
        'symptoms': ['brown_spots', 'yellow_halo', 'leaf_drop'],
        'description': 'Leaf spot diseases are caused by fungi and bacteria that cause spots on leaves. '
                      'The spots may be circular or irregular in shape.',
        'treatment': 'Remove affected leaves, apply fungicide, and avoid wetting leaves when watering.',
        'product_recommendations': [
            {'name': 'Copper Fungicide', 'type': 'Chemical/Organic', 'description': 'Broad-spectrum fungicide effective against many leaf spot diseases'},
            {'name': 'Chlorothalonil', 'type': 'Chemical', 'description': 'Protectant fungicide that prevents new infections'},
            {'name': 'Compost Tea', 'type': 'Organic', 'description': 'Introduces beneficial microbes that compete with pathogens'}
        ],
        'severity_impact': {
            'low': 'Few spots on limited number of leaves, minimal defoliation',
            'medium': 'Multiple spots on many leaves, moderate defoliation',
            'high': 'Extensive spotting throughout plant, significant defoliation'
        },
        'plant_types': ['Tomato', 'Pepper', 'Strawberry', 'Bean', 'Apple']
    },
    'aphid_infestation': {
        'symptoms': ['sticky_residue', 'curled_leaves', 'stunted_growth', 'visible_insects'],
        'description': 'Aphids are small sap-sucking insects that can cause significant damage to plants. '
                      'They often cluster on new growth and undersides of leaves.',
        'treatment': 'Spray with insecticidal soap, introduce beneficial insects like ladybugs, '
                    'or use a strong stream of water to knock them off.',
        'product_recommendations': [
            {'name': 'Insecticidal Soap', 'type': 'Organic', 'description': 'Kills aphids on contact while being gentle on plants'},
            {'name': 'Neem Oil', 'type': 'Organic', 'description': 'Disrupts aphid feeding and reproduction'},
            {'name': 'Ladybugs', 'type': 'Biological Control', 'description': 'Natural predators that feed on aphids'},
            {'name': 'Imidacloprid', 'type': 'Chemical', 'description': 'Systemic insecticide for severe infestations'}
        ],
        'severity_impact': {
            'low': 'Small colonies on few leaves, plant growth minimally affected',
            'medium': 'Multiple colonies affecting new growth, moderate distortion',
            'high': 'Large colonies throughout plant, significant damage to growth points'
        },
        'plant_types': ['Rose', 'Tomato', 'Pepper', 'Citrus', 'Bean', 'Hibiscus']
    },
    'root_rot': {
        'symptoms': ['wilting', 'yellow_leaves', 'stunted_growth', 'soft_brown_roots'],
        'description': 'Root rot is a disease that attacks the roots of plants growing in wet soil. '
                      'The roots decay, which prevents the plant from absorbing water and nutrients.',
        'treatment': 'Improve drainage, reduce watering, and repot with fresh soil if possible.',
        'product_recommendations': [
            {'name': 'Hydrogen Peroxide Solution', 'type': 'Home Remedy', 'description': 'Adds oxygen to soil and kills harmful bacteria'},
            {'name': 'Mycorrhizal Fungi', 'type': 'Biological', 'description': 'Beneficial fungi that help roots absorb nutrients and resist pathogens'},
            {'name': 'Fosetyl-Aluminum', 'type': 'Chemical', 'description': 'Systemic fungicide specifically for root diseases'}
        ],
        'severity_impact': {
            'low': 'Few roots affected, plant showing minor stress signs',
            'medium': 'Multiple roots affected, plant showing clear distress',
            'high': 'Majority of root system compromised, plant may not recover'
        },
        'plant_types': ['Tomato', 'Pepper', 'Cucumber', 'Avocado', 'Orchid', 'Succulent']
    },
    'spider_mite_infestation': {
        'symptoms': ['webbing', 'stippled_leaves', 'leaf_drop', 'visible_insects'],
        'description': 'Spider mites are tiny pests that feed on plant tissues. '
                      'They create fine webbing and cause a stippled appearance on leaves.',
        'treatment': 'Increase humidity, spray with water, apply insecticidal soap, '
                    'or introduce predatory mites.',
        'product_recommendations': [
            {'name': 'Predatory Mites', 'type': 'Biological Control', 'description': 'Natural predators that feed on spider mites'},
            {'name': 'Insecticidal Soap', 'type': 'Organic', 'description': 'Disrupts the cell membranes of mites'},
            {'name': 'Neem Oil', 'type': 'Organic', 'description': 'Smothers mites and disrupts their life cycle'},
            {'name': 'Abamectin', 'type': 'Chemical', 'description': 'Effective miticide for severe infestations'}
        ],
        'severity_impact': {
            'low': 'Small areas of stippling, minimal webbing',
            'medium': 'Multiple leaves stippled, visible webbing on several parts',
            'high': 'Extensive stippling and webbing, leaves dying from damage'
        },
        'plant_types': ['Rose', 'Tomato', 'Cucumber', 'Bean', 'Strawberry', 'Houseplants']
    },
    'nutrient_deficiency': {
        'symptoms': ['yellow_leaves', 'stunted_growth', 'leaf_discoloration'],
        'description': 'Nutrient deficiencies occur when plants lack essential nutrients. '
                      'Different deficiencies show different symptoms, often as discoloration patterns.',
        'treatment': 'Apply appropriate fertilizer based on the specific deficiency, '
                    'and ensure proper soil pH.',
        'product_recommendations': [
            {'name': 'Complete Balanced Fertilizer', 'type': 'Chemical/Organic', 'description': 'Provides all essential nutrients in balanced ratios'},
            {'name': 'Liquid Seaweed Extract', 'type': 'Organic', 'description': 'Rich in micronutrients and growth hormones'},
            {'name': 'Chelated Iron', 'type': 'Supplement', 'description': 'Specifically for iron deficiency (chlorosis)'},
            {'name': 'Epsom Salt', 'type': 'Supplement', 'description': 'Provides magnesium for plants with magnesium deficiency'}
        ],
        'severity_impact': {
            'low': 'Mild discoloration of older leaves, growth slightly reduced',
            'medium': 'Obvious discoloration patterns, clearly reduced growth',
            'high': 'Severe discoloration, very stunted growth, plant failing'
        },
        'plant_types': ['All Plants']
    },
    'viral_infection': {
        'symptoms': ['mottled_leaves', 'distorted_growth', 'stunted_growth', 'yellow_rings'],
        'description': 'Viral infections in plants are systemic and often cause mottling, '
                      'distortion, or unusual color patterns on leaves.',
        'treatment': 'Remove and destroy infected plants, control insect vectors, '
                    'and maintain good garden hygiene.',
        'product_recommendations': [
            {'name': 'Insecticides for Vectors', 'type': 'Chemical/Organic', 'description': 'Controls insects that spread viruses'},
            {'name': 'Plant Viricide', 'type': 'Chemical', 'description': 'May slow progression in some cases but doesn\'t cure viral diseases'},
            {'name': 'Resistance Inducer', 'type': 'Biological', 'description': 'Stimulates plant\'s natural defense mechanisms'}
        ],
        'severity_impact': {
            'low': 'Mild symptoms on few leaves, plant growing normally',
            'medium': 'Clear symptoms on multiple leaves, growth somewhat affected',
            'high': 'Severe symptoms throughout plant, growth severely affected'
        },
        'plant_types': ['Tomato', 'Pepper', 'Cucumber', 'Potato', 'Tobacco']
    },
    'bacterial_blight': {
        'symptoms': ['water_soaked_spots', 'leaf_yellowing', 'wilting', 'foul_odor'],
        'description': 'Bacterial blight is characterized by water-soaked spots that '
                      'eventually turn brown. Affected areas may appear greasy.',
        'treatment': 'Remove infected plant parts, avoid overhead watering, '
                    'and apply copper-based bactericides.',
        'product_recommendations': [
            {'name': 'Copper Bactericide', 'type': 'Chemical/Organic', 'description': 'Effective against bacterial diseases'},
            {'name': 'Bacillus subtilis', 'type': 'Biological', 'description': 'Beneficial bacteria that compete with pathogens'},
            {'name': 'Hydrogen Peroxide Solution', 'type': 'Home Remedy', 'description': 'Disinfects plant surfaces and soil'}
        ],
        'severity_impact': {
            'low': 'Few spots on limited leaves, plants otherwise healthy',
            'medium': 'Multiple spots on many leaves, some wilting',
            'high': 'Widespread infection, extensive wilting, plant collapse likely'
        },
        'plant_types': ['Bean', 'Tomato', 'Potato', 'Pepper', 'Soybean']
    },
    'downy_mildew': {
        'symptoms': ['yellow_spots_upper_leaves', 'fuzzy_growth_under_leaves', 'leaf_drop', 'brown_lesions'],
        'description': 'Downy mildew is a fungal-like disease that causes yellowish spots on upper leaf surfaces '
                      'and fuzzy, grayish-purple growth on the undersides of leaves. It thrives in cool, wet conditions.',
        'treatment': 'Improve air circulation, reduce leaf wetness, apply fungicides preventatively, and remove infected plants.',
        'product_recommendations': [
            {'name': 'Copper Fungicide', 'type': 'Chemical/Organic', 'description': 'Preventative treatment for downy mildew'},
            {'name': 'Mancozeb', 'type': 'Chemical', 'description': 'Protective fungicide that prevents infection'},
            {'name': 'Potassium Bicarbonate', 'type': 'Organic', 'description': 'Can help control early infections when used regularly'}
        ],
        'severity_impact': {
            'low': 'Few spots on limited leaves, slow spread',
            'medium': 'Multiple spots with visible fuzzy growth, moderate spread',
            'high': 'Extensive infection, rapid spread, significant defoliation'
        },
        'plant_types': ['Grape', 'Cucumber', 'Basil', 'Lettuce', 'Spinach', 'Squash']
    },
    'botrytis_blight': {
        'symptoms': ['gray_fuzzy_mold', 'brown_spots', 'wilting', 'flower_rot'],
        'description': 'Botrytis blight, also known as gray mold, affects many plants, especially in cool, humid conditions. '
                     'It appears as a fuzzy gray-brown mold on flowers, leaves, and stems, often starting on dying tissue.',
        'treatment': 'Remove infected plant material, improve air circulation, reduce humidity, and apply fungicides.',
        'product_recommendations': [
            {'name': 'Thiophanate-methyl', 'type': 'Chemical', 'description': 'Systemic fungicide effective against Botrytis'},
            {'name': 'Bacillus subtilis', 'type': 'Biological', 'description': 'Beneficial bacteria that suppress fungal growth'},
            {'name': 'Fenhexamid', 'type': 'Chemical', 'description': 'Specific fungicide for Botrytis control'}
        ],
        'severity_impact': {
            'low': 'Small areas of infection on few plant parts',
            'medium': 'Multiple infection sites, flowers and leaves affected',
            'high': 'Widespread infection, plants collapsing from rot'
        },
        'plant_types': ['Strawberry', 'Tomato', 'Rose', 'Peony', 'Grape', 'Lettuce']
    },
    'fusarium_wilt': {
        'symptoms': ['wilting', 'yellow_leaves', 'stunted_growth', 'vascular_discoloration'],
        'description': 'Fusarium wilt is a soil-borne fungal disease that affects the vascular system of plants. '
                     'It causes yellowing of leaves, often starting on one side, wilting, and brown discoloration inside stems.',
        'treatment': 'Use resistant varieties, practice crop rotation, improve soil drainage, and solarize soil in severe cases.',
        'product_recommendations': [
            {'name': 'Trichoderma harzianum', 'type': 'Biological', 'description': 'Beneficial fungus that competes with Fusarium'},
            {'name': 'Mycorrhizal fungi inoculant', 'type': 'Biological', 'description': 'Strengthens root systems against pathogens'},
            {'name': 'Soil Solarization Plastic', 'type': 'Cultural', 'description': 'Clear plastic for soil solarization treatment'}
        ],
        'severity_impact': {
            'low': 'Mild wilting of few leaves, plant recovering during cooler weather',
            'medium': 'Clear wilting pattern, yellowing on one side, plant stressed',
            'high': 'Severe wilting throughout plant, vascular browning, plant collapse'
        },
        'plant_types': ['Tomato', 'Banana', 'Cotton', 'Watermelon', 'Basil', 'Carnation']
    },
    'citrus_greening': {
        'symptoms': ['yellow_mottled_leaves', 'lopsided_fruit', 'bitter_fruit', 'twig_dieback'],
        'description': 'Citrus greening (Huanglongbing) is a serious bacterial disease spread by psyllids. '
                     'It causes mottled yellowing of leaves, misshapen bitter fruit, and eventual tree death.',
        'treatment': 'Control psyllid vectors, remove infected trees, and maintain tree health with proper nutrition.',
        'product_recommendations': [
            {'name': 'Imidacloprid', 'type': 'Chemical', 'description': 'Systemic insecticide that controls psyllids'},
            {'name': 'Mineral Oil Spray', 'type': 'Organic', 'description': 'Helps control psyllid populations'},
            {'name': 'Complete Citrus Fertilizer', 'type': 'Supplement', 'description': 'Maintains tree vigor to better withstand infection'}
        ],
        'severity_impact': {
            'low': 'Few mottled leaves, trees still producing normal fruit',
            'medium': 'Widespread leaf symptoms, some fruit affected, twig dieback beginning',
            'high': 'Severe symptoms throughout tree, most fruit affected, significant dieback'
        },
        'plant_types': ['Citrus']
    },
    'black_spot': {
        'symptoms': ['black_circular_spots', 'yellow_leaf_edges', 'leaf_drop', 'purple_spots_stems'],
        'description': 'Black spot is a fungal disease that commonly affects roses. It appears as circular black spots '
                     'with fringe-like margins on leaves, often surrounded by yellowing tissue.',
        'treatment': 'Remove infected leaves, improve air circulation, avoid wetting foliage, and apply fungicides.',
        'product_recommendations': [
            {'name': 'Chlorothalonil', 'type': 'Chemical', 'description': 'Protectant fungicide for black spot control'},
            {'name': 'Tebuconazole', 'type': 'Chemical', 'description': 'Systemic fungicide effective against black spot'},
            {'name': 'Neem Oil', 'type': 'Organic', 'description': 'Natural fungicide that helps control black spot'}
        ],
        'severity_impact': {
            'low': 'Few spots on limited number of leaves, minimal defoliation',
            'medium': 'Multiple spots on many leaves, moderate defoliation',
            'high': 'Extensive spotting, severe defoliation, plant weakened'
        },
        'plant_types': ['Rose', 'Apple', 'Cherry', 'Pear']
    }
}

# List of all possible symptoms for the user interface
ALL_SYMPTOMS = [
    'white_powdery_patches',
    'leaf_yellowing',
    'distorted_growth',
    'brown_spots',
    'yellow_halo',
    'leaf_drop',
    'sticky_residue',
    'curled_leaves',
    'stunted_growth',
    'visible_insects',
    'wilting',
    'soft_brown_roots',
    'webbing',
    'stippled_leaves',
    'leaf_discoloration',
    'mottled_leaves',
    'yellow_rings',
    'water_soaked_spots',
    'foul_odor',
    'yellow_leaves',
    'yellow_spots_upper_leaves',
    'fuzzy_growth_under_leaves',
    'brown_lesions',
    'gray_fuzzy_mold',
    'flower_rot',
    'vascular_discoloration',
    'yellow_mottled_leaves',
    'lopsided_fruit',
    'bitter_fruit',
    'twig_dieback',
    'black_circular_spots',
    'yellow_leaf_edges',
    'purple_spots_stems'
]

# User-friendly names for symptoms
SYMPTOM_NAMES = {
    'white_powdery_patches': 'White powdery patches on leaves or stems',
    'leaf_yellowing': 'Yellowing of leaves',
    'distorted_growth': 'Distorted or malformed growth',
    'brown_spots': 'Brown spots on leaves',
    'yellow_halo': 'Yellow halo around spots',
    'leaf_drop': 'Premature leaf drop',
    'sticky_residue': 'Sticky residue on leaves or stems',
    'curled_leaves': 'Curling or cupping of leaves',
    'stunted_growth': 'Stunted or slow growth',
    'visible_insects': 'Visible insects on the plant',
    'wilting': 'Wilting despite adequate watering',
    'soft_brown_roots': 'Soft, brown, or decaying roots',
    'webbing': 'Fine webbing on leaves or between stems',
    'stippled_leaves': 'Stippled or speckled appearance on leaves',
    'leaf_discoloration': 'Unusual patterns of leaf discoloration',
    'mottled_leaves': 'Mottled or mosaic pattern on leaves',
    'yellow_rings': 'Yellow rings or patterns on leaves',
    'water_soaked_spots': 'Water-soaked spots on leaves or stems',
    'foul_odor': 'Foul odor from plant or soil',
    'yellow_leaves': 'Yellowing of leaves',
    'yellow_spots_upper_leaves': 'Yellow spots on upper leaf surfaces',
    'fuzzy_growth_under_leaves': 'Fuzzy or downy growth on undersides of leaves',
    'brown_lesions': 'Brown lesions or dead areas on leaves',
    'gray_fuzzy_mold': 'Gray fuzzy mold on plant tissues',
    'flower_rot': 'Flowers turning brown and rotting',
    'vascular_discoloration': 'Brown streaks inside stems when cut',
    'yellow_mottled_leaves': 'Yellow mottling or blotching on leaves',
    'lopsided_fruit': 'Asymmetrical or lopsided fruit',
    'bitter_fruit': 'Bitter or inedible fruit',
    'twig_dieback': 'Twigs or branches dying back from tips',
    'black_circular_spots': 'Black circular spots with defined margins',
    'yellow_leaf_edges': 'Yellow edges around leaf margins',
    'purple_spots_stems': 'Purple or red spots on stems'
}

# Symptom severity descriptions
SYMPTOM_SEVERITY = {
    1: "Very mild - barely noticeable",
    2: "Mild - present but not concerning",
    3: "Moderate - clearly visible symptoms",
    4: "Severe - widespread symptoms",
    5: "Very severe - plant critically affected"
}

# Define plant categories and their associated diseases
PLANT_CATEGORIES = {
    "Vegetable Plants": [
        "Tomato", "Pepper", "Cucumber", "Bean", "Potato", "Lettuce", "Spinach", "Squash", "Watermelon"
    ],
    "Fruit Plants": [
        "Apple", "Strawberry", "Grape", "Citrus", "Cherry", "Pear", "Banana"
    ],
    "Ornamental Plants": [
        "Rose", "Hibiscus", "Peony", "Carnation", "Orchid"
    ],
    "Herbs": [
        "Basil", "Mint", "Rosemary", "Thyme", "Lavender"
    ],
    "Houseplants": [
        "Succulent", "Fern", "Palm", "Pothos", "African Violet"
    ]
}

# Map plant types to common diseases they are susceptible to
PLANT_DISEASE_SUSCEPTIBILITY = {
    "Tomato": ["powdery_mildew", "leaf_spot", "aphid_infestation", "root_rot", "spider_mite_infestation", "viral_infection", "bacterial_blight", "fusarium_wilt", "botrytis_blight"],
    "Pepper": ["leaf_spot", "aphid_infestation", "root_rot", "viral_infection", "bacterial_blight"],
    "Cucumber": ["powdery_mildew", "downy_mildew", "root_rot", "spider_mite_infestation"],
    "Bean": ["bacterial_blight", "aphid_infestation", "spider_mite_infestation", "fusarium_wilt"],
    "Rose": ["powdery_mildew", "aphid_infestation", "spider_mite_infestation", "black_spot", "botrytis_blight"],
    "Citrus": ["aphid_infestation", "nutrient_deficiency", "citrus_greening"],
    "Apple": ["leaf_spot", "black_spot", "nutrient_deficiency"],
    "Grape": ["powdery_mildew", "downy_mildew", "botrytis_blight"],
    "Potato": ["viral_infection", "bacterial_blight", "fusarium_wilt"],
    "Succulent": ["root_rot"],
    "Strawberry": ["leaf_spot", "spider_mite_infestation", "botrytis_blight"],
    "Houseplants": ["spider_mite_infestation", "nutrient_deficiency", "root_rot"]
}
