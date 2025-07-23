"""
Inference Engine for Plant Disease Expert System

This module implements the inference mechanism for diagnosing plant diseases
based on observed symptoms and environmental factors.
"""

from knowledge_base import KNOWLEDGE_BASE, PLANT_DISEASE_SUSCEPTIBILITY

class InferenceEngine:
    """
    Advanced inference engine that uses multiple factors to diagnose plant diseases:
    - Observed symptoms and their severity
    - Plant type susceptibility
    - Environmental conditions
    - Symptom patterns and progression
    """
    
    def __init__(self, knowledge_base=None):
        """
        Initialize the inference engine with a knowledge base.
        
        Args:
            knowledge_base: Dictionary containing disease rules and information
        """
        self.knowledge_base = knowledge_base or KNOWLEDGE_BASE
    
    def diagnose(self, observed_symptoms, symptom_severity=None, plant_type=None, environmental_factors=None):
        """
        Diagnose potential diseases based on observed symptoms and additional factors.
        
        Args:
            observed_symptoms: List of symptoms observed in the plant
            symptom_severity: Dictionary mapping symptoms to severity levels (1-5)
            plant_type: Type of plant (e.g., 'Tomato', 'Rose')
            environmental_factors: Dictionary with environmental conditions
                (e.g., {'temperature': 'high', 'humidity': 'high'})
            
        Returns:
            List of dictionaries containing disease information and confidence score
        """
        if not observed_symptoms:
            return []
        
        # Default severity if not provided
        if symptom_severity is None:
            symptom_severity = {symptom: 3 for symptom in observed_symptoms}  # Default to medium severity
        
        # Default environmental factors if not provided
        if environmental_factors is None:
            environmental_factors = {}
        
        results = []
        
        # Filter diseases based on plant type if provided
        candidate_diseases = self._filter_by_plant_type(plant_type) if plant_type else self.knowledge_base
        
        for disease, data in candidate_diseases.items():
            required_symptoms = data['symptoms']
            
            # Count how many of the required symptoms are present
            matching_symptoms = [s for s in required_symptoms if s in observed_symptoms]
            
            # If no symptoms match, skip this disease
            if not matching_symptoms:
                continue
                
            # Calculate confidence score using multiple weighted factors
            confidence = self._calculate_confidence(
                disease, 
                matching_symptoms, 
                required_symptoms, 
                observed_symptoms, 
                symptom_severity,
                plant_type,
                environmental_factors
            )
            
            # Only include diseases with at least some confidence
            if confidence > 0:
                results.append({
                    'disease': disease,
                    'name': disease.replace('_', ' ').title(),
                    'confidence': round(confidence * 100, 1),
                    'matching_symptoms': matching_symptoms,
                    'description': data['description'],
                    'treatment': data['treatment'],
                    'product_recommendations': data.get('product_recommendations', []),
                    'severity_impact': data.get('severity_impact', {})
                })
        
        # Sort results by confidence score (highest first)
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        return results
    
    def _filter_by_plant_type(self, plant_type):
        """
        Filter diseases based on plant type susceptibility.
        
        Args:
            plant_type: Type of plant
            
        Returns:
            Dictionary of diseases that can affect this plant type
        """
        # If plant type is 'All Plants' or not recognized, return all diseases
        if plant_type == 'All Plants' or plant_type not in PLANT_DISEASE_SUSCEPTIBILITY:
            return self.knowledge_base
        
        # Get diseases that commonly affect this plant type
        susceptible_diseases = PLANT_DISEASE_SUSCEPTIBILITY.get(plant_type, [])
        
        # Include diseases that list this plant type specifically
        for disease, data in self.knowledge_base.items():
            if 'plant_types' in data and plant_type in data['plant_types']:
                susceptible_diseases.append(disease)
        
        # Remove duplicates
        susceptible_diseases = list(set(susceptible_diseases))
        
        # Filter knowledge base to only include relevant diseases
        return {disease: data for disease, data in self.knowledge_base.items() 
                if disease in susceptible_diseases}
    
    def _calculate_confidence(self, disease, matching_symptoms, required_symptoms, 
                             observed_symptoms, symptom_severity, plant_type,
                             environmental_factors):
        """
        Calculate a weighted confidence score based on multiple factors.
        
        Args:
            disease: Disease being evaluated
            matching_symptoms: List of symptoms matching between observed and required
            required_symptoms: List of symptoms required for this disease
            observed_symptoms: List of symptoms observed in the plant
            symptom_severity: Dictionary mapping symptoms to severity levels
            plant_type: Type of plant
            environmental_factors: Dictionary with environmental conditions
            
        Returns:
            Confidence score between 0 and 1
        """
        # Calculate basic match percentage (symptoms matched / symptoms required)
        match_percentage = len(matching_symptoms) / len(required_symptoms)
        
        # Calculate coverage percentage (symptoms matched / symptoms observed)
        coverage_percentage = len(matching_symptoms) / len(observed_symptoms)
        
        # Calculate severity factor - higher severity gives higher confidence
        # For symptoms that match this disease, get their average severity (normalized to 0-1 scale)
        # Convert string values to integers to avoid type errors
        severity_values = []
        for s in matching_symptoms:
            severity = symptom_severity.get(s, 3)
            # Convert to integer if it's a string
            if isinstance(severity, str):
                try:
                    severity = int(float(severity))
                except (ValueError, TypeError):
                    severity = 3  # Default to medium severity if conversion fails
            severity_values.append(severity)
            
        avg_severity = sum(severity_values) / len(severity_values) if severity_values else 3
        severity_factor = avg_severity / 5.0  # Normalize to 0-1 range
        
        # Calculate symptom specificity weight
        # Some symptoms are more specific to certain diseases
        specificity_factor = self._calculate_symptom_specificity(matching_symptoms, disease)
        
        # Calculate plant type susceptibility weight
        plant_factor = self._calculate_plant_susceptibility(disease, plant_type)
        
        # Calculate environmental condition match
        env_factor = self._calculate_environmental_match(disease, environmental_factors)
        
        # Weighted score combining all factors
        # 30% match, 20% coverage, 20% severity, 15% specificity, 10% plant susceptibility, 5% environment
        confidence = (
            (match_percentage * 0.30) + 
            (coverage_percentage * 0.20) + 
            (severity_factor * 0.20) + 
            (specificity_factor * 0.15) + 
            (plant_factor * 0.10) + 
            (env_factor * 0.05)
        )
        
        return confidence
    
    def _calculate_symptom_specificity(self, symptoms, disease):
        """
        Calculate how specific the matching symptoms are to this disease.
        Some symptoms are very common across many diseases, while others are more specific.
        
        Args:
            symptoms: List of matching symptoms
            disease: Disease being evaluated
            
        Returns:
            Specificity factor between 0 and 1
        """
        if not symptoms:
            return 0
            
        # Count how many other diseases have each symptom
        specificity_scores = []
        
        for symptom in symptoms:
            # Count diseases that include this symptom
            disease_count = sum(1 for d, data in self.knowledge_base.items() 
                              if symptom in data['symptoms'])
            
            # Calculate symptom specificity (inverse of how common it is)
            # A symptom that appears in only one disease has highest specificity (1.0)
            # A symptom that appears in all diseases has lowest specificity
            max_diseases = max(len(self.knowledge_base), 1)  # Avoid division by zero
            symptom_specificity = 1 - ((disease_count - 1) / max_diseases)
            specificity_scores.append(symptom_specificity)
        
        # Average specificity across all matching symptoms
        return sum(specificity_scores) / len(specificity_scores) if specificity_scores else 0
    
    def _calculate_plant_susceptibility(self, disease, plant_type):
        """
        Calculate how susceptible the plant type is to this disease.
        
        Args:
            disease: Disease being evaluated
            plant_type: Type of plant
            
        Returns:
            Plant susceptibility factor between 0 and 1
        """
        if not plant_type or plant_type == 'All Plants':
            return 0.5  # Neutral if no plant type specified
        
        # Check if this plant type is specifically listed for this disease
        disease_data = self.knowledge_base.get(disease, {})
        if 'plant_types' in disease_data and plant_type in disease_data['plant_types']:
            return 1.0  # Highest susceptibility if specifically listed
        
        # Check if disease is in the susceptibility list for this plant type
        if plant_type in PLANT_DISEASE_SUSCEPTIBILITY and disease in PLANT_DISEASE_SUSCEPTIBILITY[plant_type]:
            return 0.8  # High susceptibility if in the general list
        
        # Lower susceptibility if not specifically listed
        return 0.3
    
    def _calculate_environmental_match(self, disease, environmental_factors):
        """
        Calculate how well the environmental conditions match this disease.
        
        Args:
            disease: Disease being evaluated
            environmental_factors: Dictionary with environmental conditions
            
        Returns:
            Environmental match factor between 0 and 1
        """
        if not environmental_factors:
            return 0.5  # Neutral if no environmental factors provided
            
        # Ideal environmental conditions for each disease (simplified)
        disease_environmental_preferences = {
            'powdery_mildew': {'temperature': 'warm', 'humidity': 'low', 'air_circulation': 'poor'},
            'downy_mildew': {'temperature': 'cool', 'humidity': 'high', 'leaf_wetness': 'high'},
            'botrytis_blight': {'temperature': 'cool', 'humidity': 'high', 'air_circulation': 'poor'},
            'bacterial_blight': {'temperature': 'warm', 'humidity': 'high', 'leaf_wetness': 'high'},
            'root_rot': {'soil_moisture': 'high', 'drainage': 'poor'},
            'fusarium_wilt': {'temperature': 'hot', 'soil_moisture': 'low', 'plant_stress': 'high'},
            'spider_mite_infestation': {'temperature': 'hot', 'humidity': 'low'},
            'aphid_infestation': {'temperature': 'moderate', 'new_growth': 'yes'}
        }
        
        # Get the preferred conditions for this disease
        preferred_conditions = disease_environmental_preferences.get(disease, {})
        
        # If no preferred conditions defined for this disease
        if not preferred_conditions:
            return 0.5
            
        # Count how many environmental factors match
        matching_factors = 0
        total_factors = len(preferred_conditions)
        
        for factor, preferred_value in preferred_conditions.items():
            if factor in environmental_factors and environmental_factors[factor] == preferred_value:
                matching_factors += 1
        
        # Calculate match percentage
        return matching_factors / total_factors if total_factors > 0 else 0.5
