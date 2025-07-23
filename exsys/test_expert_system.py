"""
Advanced test cases for the Plant Disease Expert System

This script contains test cases to verify the functionality of the
enhanced plant disease diagnosis expert system, including testing
plant-specific diagnoses and environmental factors.
"""

from inference_engine import InferenceEngine
from knowledge_base import SYMPTOM_NAMES, SYMPTOM_SEVERITY

def run_test_case(test_name, symptoms, symptom_severity=None, plant_type=None, 
                environmental_factors=None, expected_top_disease=None):
    """
    Run a test case and print the results.
    
    Args:
        test_name: Name of the test case
        symptoms: List of symptoms to diagnose
        symptom_severity: Dictionary of symptom severity levels (optional)
        plant_type: Type of plant (optional)
        environmental_factors: Dictionary of environmental conditions (optional)
        expected_top_disease: Expected top disease (optional)
    """
    print(f"\n=== Test Case: {test_name} ===")
    
    # Print symptoms with severity if provided
    print("Symptoms:")
    for symptom in symptoms:
        severity = symptom_severity.get(symptom, 3) if symptom_severity else 3
        severity_text = SYMPTOM_SEVERITY[severity]
        print(f"- {SYMPTOM_NAMES[symptom]} (Severity: {severity}/5 - {severity_text})")
    
    # Print plant type if provided
    if plant_type:
        print(f"\nPlant Type: {plant_type}")
    
    # Print environmental factors if provided
    if environmental_factors:
        print("\nEnvironmental Factors:")
        for factor, value in environmental_factors.items():
            print(f"- {factor.replace('_', ' ').title()}: {value.replace('_', ' ').title()}")
    
    # Run diagnosis with all provided information
    engine = InferenceEngine()
    results = engine.diagnose(
        symptoms, 
        symptom_severity, 
        plant_type, 
        environmental_factors
    )
    
    # Print results
    print("\nDiagnosis Results:")
    if not results:
        print("No diseases matched the symptoms.")
    else:
        for i, result in enumerate(results[:3], 1):
            print(f"{i}. {result['name']} (Confidence: {result['confidence']}%)")
    
    # Check if expected disease is in top result
    if expected_top_disease and results:
        top_disease = results[0]['disease']
        if top_disease == expected_top_disease:
            print(f"\nTest PASSED: Expected '{expected_top_disease}' and got '{top_disease}'")
        else:
            print(f"\nTest FAILED: Expected '{expected_top_disease}' but got '{top_disease}'")
    
    print("-" * 50)

def run_all_tests():
    """Run all test cases."""
    print("\n" + "=" * 80)
    print(" " * 25 + "EXPERT SYSTEM ADVANCED TEST CASES")
    print("=" * 80)
    
    # Basic Test Cases
    # Test Case 1: Classic Powdery Mildew
    run_test_case(
        "Classic Powdery Mildew",
        ["white_powdery_patches", "leaf_yellowing", "distorted_growth"],
        expected_top_disease="powdery_mildew"
    )
    
    # Test Case 2: Leaf Spot Disease
    run_test_case(
        "Leaf Spot Disease",
        ["brown_spots", "yellow_halo", "leaf_drop"],
        expected_top_disease="leaf_spot"
    )
    
    # Test Case with Severity
    # Test Case 3: Severe Aphid Infestation
    run_test_case(
        "Severe Aphid Infestation",
        ["sticky_residue", "curled_leaves", "visible_insects"],
        symptom_severity={
            "sticky_residue": 5,
            "curled_leaves": 4,
            "visible_insects": 5
        },
        expected_top_disease="aphid_infestation"
    )
    
    # Test Case 4: Mild Root Rot
    run_test_case(
        "Mild Root Rot",
        ["wilting", "yellow_leaves", "soft_brown_roots"],
        symptom_severity={
            "wilting": 2,
            "yellow_leaves": 2,
            "soft_brown_roots": 1
        },
        expected_top_disease="root_rot"
    )
    
    # Plant-Specific Test Cases
    # Test Case 5: Tomato with Powdery Mildew Symptoms
    run_test_case(
        "Tomato with Powdery Mildew Symptoms",
        ["white_powdery_patches", "leaf_yellowing"],
        plant_type="Tomato",
        expected_top_disease="powdery_mildew"
    )
    
    # Test Case 6: Rose with Black Spot Symptoms
    run_test_case(
        "Rose with Black Spot Symptoms",
        ["black_circular_spots", "yellow_leaf_edges", "leaf_drop"],
        plant_type="Rose",
        expected_top_disease="black_spot"
    )
    
    # Environmental Factor Test Cases
    # Test Case 7: Powdery Mildew in Favorable Conditions
    run_test_case(
        "Powdery Mildew in Favorable Conditions",
        ["white_powdery_patches", "leaf_yellowing"],
        environmental_factors={
            "temperature": "warm",
            "humidity": "low",
            "air_circulation": "poor"
        },
        expected_top_disease="powdery_mildew"
    )
    
    # Test Case 8: Downy Mildew in Favorable Conditions
    run_test_case(
        "Downy Mildew in Favorable Conditions",
        ["yellow_spots_upper_leaves", "fuzzy_growth_under_leaves"],
        environmental_factors={
            "temperature": "cool",
            "humidity": "high",
            "leaf_wetness": "high"
        },
        expected_top_disease="downy_mildew"
    )
    
    # Combined Factors Test Cases
    # Test Case 9: Tomato with Fusarium Wilt - All Factors
    run_test_case(
        "Tomato with Fusarium Wilt - All Factors",
        ["wilting", "yellow_leaves", "vascular_discoloration"],
        symptom_severity={
            "wilting": 4,
            "yellow_leaves": 3,
            "vascular_discoloration": 5
        },
        plant_type="Tomato",
        environmental_factors={
            "temperature": "hot",
            "soil_moisture": "low",
            "plant_stress": "high"
        },
        expected_top_disease="fusarium_wilt"
    )
    
    # Test Case 10: Cucumber with Multiple Possible Diseases
    run_test_case(
        "Cucumber with Multiple Possible Diseases",
        ["leaf_yellowing", "white_powdery_patches", "wilting"],
        plant_type="Cucumber",
        # No expected disease as multiple could match
    )
    
    # Test Case 11: Ambiguous Symptoms
    run_test_case(
        "Ambiguous Symptoms",
        ["leaf_yellowing", "wilting"],
        # No expected disease as many could match
    )
    
    # Test Case 12: No Matching Disease
    run_test_case(
        "No Matching Disease",
        ["foul_odor"],  # Only one symptom that's not specific enough
    )

if __name__ == "__main__":
    run_all_tests()
