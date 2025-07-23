"""
Plant Disease Expert System

This is the main module for the plant disease diagnosis expert system.
It provides a command-line interface for users to input symptoms and
receive diagnoses.
"""

import os
from knowledge_base import ALL_SYMPTOMS, SYMPTOM_NAMES
from inference_engine import InferenceEngine

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    print("\n" + "=" * 80)
    print(" " * 25 + "PLANT DISEASE EXPERT SYSTEM")
    print("=" * 80 + "\n")
    print("This system helps diagnose plant diseases based on observed symptoms.\n")

def get_user_symptoms():
    """
    Present a menu of symptoms and let the user select which ones they observe.
    
    Returns:
        List of selected symptom codes
    """
    selected_symptoms = []
    
    print("\nPlease indicate which symptoms you observe in your plant:")
    print("Select symptoms by entering their numbers (separated by spaces).")
    print("Enter 'done' when finished.\n")
    
    # Display symptoms in groups of 5 for readability
    for i, symptom_code in enumerate(ALL_SYMPTOMS, 1):
        print(f"{i:2}. {SYMPTOM_NAMES[symptom_code]}")
    
    while True:
        print("\nCurrently selected symptoms:", end=" ")
        if selected_symptoms:
            selected_names = [SYMPTOM_NAMES[s] for s in selected_symptoms]
            print(", ".join(selected_names))
        else:
            print("None")
            
        choice = input("\nEnter symptom numbers or 'done': ").strip().lower()
        
        if choice == 'done':
            break
            
        try:
            # Parse multiple numbers separated by spaces
            selections = [int(x) for x in choice.split()]
            
            for selection in selections:
                if 1 <= selection <= len(ALL_SYMPTOMS):
                    symptom_code = ALL_SYMPTOMS[selection - 1]
                    if symptom_code not in selected_symptoms:
                        selected_symptoms.append(symptom_code)
                else:
                    print(f"Invalid selection: {selection}. Please enter numbers between 1 and {len(ALL_SYMPTOMS)}.")
        except ValueError:
            print("Invalid input. Please enter numbers or 'done'.")
    
    return selected_symptoms

def display_diagnosis(results):
    """
    Display the diagnosis results to the user.
    
    Args:
        results: List of dictionaries containing disease information and confidence
    """
    if not results:
        print("\nNo diseases match the symptoms you provided.")
        print("Consider adding more symptoms or consulting with a plant specialist.")
        return
    
    print("\n" + "=" * 80)
    print(" " * 30 + "DIAGNOSIS RESULTS")
    print("=" * 80 + "\n")
    
    # Display top 3 matches or fewer if less available
    for i, result in enumerate(results[:3], 1):
        print(f"Diagnosis #{i}: {result['name']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"\nDescription: {result['description']}")
        print(f"\nRecommended Treatment: {result['treatment']}")
        print("\nMatching Symptoms:")
        for symptom in result['matching_symptoms']:
            print(f"- {SYMPTOM_NAMES[symptom]}")
        print("\n" + "-" * 80 + "\n")
    
    # If there are more results, mention them
    if len(results) > 3:
        print(f"There are {len(results) - 3} more potential diagnoses with lower confidence.")

def main():
    """Main application function."""
    clear_screen()
    print_header()
    
    # Create inference engine
    engine = InferenceEngine()
    
    while True:
        # Get symptoms from user
        user_symptoms = get_user_symptoms()
        
        if not user_symptoms:
            print("\nNo symptoms selected. Please select at least one symptom.")
            continue
        
        # Run diagnosis
        diagnosis_results = engine.diagnose(user_symptoms)
        
        # Display results
        display_diagnosis(diagnosis_results)
        
        # Ask if user wants to try again
        choice = input("\nWould you like to diagnose another plant? (y/n): ").strip().lower()
        if choice != 'y':
            break
        
        clear_screen()
        print_header()
    
    print("\nThank you for using the Plant Disease Expert System!")

if __name__ == "__main__":
    main()
