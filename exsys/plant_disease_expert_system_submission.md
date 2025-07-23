# Plant Disease Expert System

## Selected Topic
For this assignment, I have developed an expert system for diagnosing plant diseases based on observed symptoms. This topic was chosen because:

1. Plant diseases are a significant concern for gardeners, farmers, and plant enthusiasts
2. Diseases often present with distinct visual symptoms that can be codified into rules
3. Early diagnosis can lead to more effective treatment and plant recovery
4. The domain knowledge can be structured in a way that follows IF-THEN rule patterns

## Knowledge Base Structure

The knowledge base is structured as a dictionary in Python, where:
- Each disease is represented as a key
- Each disease has associated symptoms, description, and treatment information
- Symptoms are represented as codes that map to user-friendly descriptions

### Example Rule Structure:
```python
'powdery_mildew': {
    'symptoms': ['white_powdery_patches', 'leaf_yellowing', 'distorted_growth'],
    'description': 'Powdery mildew is a fungal disease that affects a wide range of plants. '
                  'It appears as white powdery spots on leaves and stems.',
    'treatment': 'Apply fungicide, improve air circulation, and avoid overhead watering.'
}
```

## Defined Rules

The system includes rules for diagnosing the following plant diseases:

1. **Powdery Mildew**
   - IF plant has white powdery patches AND leaf yellowing AND distorted growth
   - THEN plant likely has powdery mildew

2. **Leaf Spot**
   - IF plant has brown spots AND yellow halo around spots AND premature leaf drop
   - THEN plant likely has leaf spot disease

3. **Aphid Infestation**
   - IF plant has sticky residue AND curled leaves AND visible insects
   - THEN plant likely has aphid infestation

4. **Root Rot**
   - IF plant has wilting despite adequate watering AND yellow leaves AND soft brown roots
   - THEN plant likely has root rot

5. **Spider Mite Infestation**
   - IF plant has webbing AND stippled leaves AND leaf drop AND visible insects
   - THEN plant likely has spider mite infestation

6. **Nutrient Deficiency**
   - IF plant has yellow leaves AND stunted growth AND leaf discoloration
   - THEN plant likely has nutrient deficiency

7. **Viral Infection**
   - IF plant has mottled leaves AND distorted growth AND stunted growth AND yellow rings
   - THEN plant likely has viral infection

8. **Bacterial Blight**
   - IF plant has water-soaked spots AND leaf yellowing AND wilting AND foul odor
   - THEN plant likely has bacterial blight

## Inference Engine

The inference engine uses a forward-chaining approach with a confidence scoring mechanism:

1. The user inputs observed symptoms
2. The system matches these symptoms against the knowledge base rules
3. For each disease, a confidence score is calculated based on:
   - Match percentage: How many of the required symptoms for this disease are present
   - Coverage percentage: How many of the observed symptoms are explained by this disease
4. Diseases are ranked by confidence score
5. The top matches are presented to the user with descriptions and treatment recommendations

## Test Cases

The system was tested with the following scenarios:

1. **Classic Powdery Mildew**
   - Symptoms: White powdery patches, leaf yellowing, distorted growth
   - Expected diagnosis: Powdery mildew (100% confidence)
   - Result: PASSED

2. **Leaf Spot Disease**
   - Symptoms: Brown spots, yellow halo, leaf drop
   - Expected diagnosis: Leaf spot (100% confidence)
   - Result: PASSED

3. **Aphid Infestation**
   - Symptoms: Sticky residue, curled leaves, visible insects
   - Expected diagnosis: Aphid infestation (85% confidence)
   - Result: PASSED

4. **Root Rot**
   - Symptoms: Wilting, yellow leaves, soft brown roots
   - Expected diagnosis: Root rot (85% confidence)
   - Result: PASSED

5. **Mixed Symptoms - Nutrient Deficiency**
   - Symptoms: Yellow leaves, stunted growth, leaf discoloration
   - Expected diagnosis: Nutrient deficiency (100% confidence)
   - Result: PASSED

6. **Ambiguous Case**
   - Symptoms: Leaf yellowing, stunted growth
   - Expected diagnosis: Multiple potential matches with similar confidence
   - Result: System correctly identified multiple possible diseases

7. **Minimal Symptoms**
   - Symptoms: Yellow leaves only
   - Expected diagnosis: Multiple potential matches
   - Result: System correctly identified multiple possible diseases

8. **No Matching Disease**
   - Symptoms: Foul odor only
   - Expected diagnosis: Low confidence matches
   - Result: System provided best guess with appropriate low confidence

## User Interface

The system provides a command-line interface that:
1. Presents a list of possible symptoms to the user
2. Allows the user to select multiple symptoms
3. Processes the symptoms and displays diagnosis results
4. Shows confidence levels, descriptions, and treatment recommendations
5. Allows the user to diagnose multiple plants in one session

## Conclusion

This expert system demonstrates how rule-based systems can be used to diagnose plant diseases based on observable symptoms. The system uses a forward-chaining inference mechanism with confidence scoring to provide useful diagnoses even with incomplete or ambiguous information.

The modular design allows for easy extension of the knowledge base with additional diseases and symptoms. The confidence scoring system helps users understand the reliability of the diagnosis and consider alternative possibilities when symptoms are ambiguous.
