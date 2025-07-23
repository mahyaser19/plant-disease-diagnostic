# Plant Disease Diagnosis Expert System (v2.0)

![Plant Disease Expert System](assets/plant_logo.png)

An advanced expert system for diagnosing plant diseases based on observed symptoms and environmental factors. The system uses a sophisticated rule-based approach with weighted inference to provide accurate diagnoses and treatment recommendations.

## 🌟 Features

- **Comprehensive Knowledge Base**: Information on 12+ common plant diseases with detailed symptoms, descriptions, and treatments
- **Advanced Inference Engine**: Uses multiple factors for diagnosis including symptom severity, plant type susceptibility, and environmental conditions
- **Modern User Interface**: Sleek, intuitive design with customizable themes and responsive layout
- **Plant-Specific Diagnosis**: Targeted diagnosis based on plant type for more accurate results
- **Environmental Factor Analysis**: Takes into account environmental conditions that affect disease development
- **Severity Impact Assessment**: Understand how diseases progress at different severity levels
- **Multiple Export Options**: Save results as Text, PDF, or JSON for easy sharing and record-keeping
- **Diagnosis History**: Keep track of previous diagnoses and compare results
- **Plant Guide**: Reference information for common plants and their care requirements

## 📋 Requirements

- Python 3.6 or higher
- Required packages: `customtkinter`, `pillow`
- Optional packages: `reportlab` (for PDF export)

## 🚀 Installation

1. Clone the repository or download the source code
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## 📊 Usage

Run the graphical user interface:
```
python plant_disease_gui.py
```

Or use the command-line interface:
```
python plant_disease_expert.py
```

## 🔍 Diagnosis Process

1. Select the plant type from the dropdown menu
2. Check the symptoms you observe in your plant
3. Adjust the severity level for each symptom
4. (Optional) Specify environmental conditions
5. Click "Diagnose" to get results
6. View treatment recommendations and product suggestions
7. Export or save your results as needed

## 📁 Project Structure

- `plant_disease_gui.py`: Modern graphical user interface using customtkinter
- `plant_disease_expert.py`: Command-line interface
- `knowledge_base.py`: Expert knowledge about plant diseases, symptoms, and treatments
- `inference_engine.py`: Advanced inference mechanism with weighted factors
- `assets/`: Contains images and icons for the application
- `saved_data/`: Directory for saved sessions and exported results

## ✨ New in Version 2.0

- Completely redesigned modern UI with customtkinter
- Enhanced knowledge base with 4 additional diseases
- Advanced inference engine with environmental factor analysis
- Plant-specific diagnosis capabilities
- Severity impact assessment for better treatment planning
- Improved export options including PDF with formatting
- Plant guide with care tips and common diseases
- Dark mode and theme customization

## 📷 Screenshots

[Screenshots placeholder]

## 🔧 Customization

The system can be extended with new diseases and symptoms by modifying the `knowledge_base.py` file. The user interface can be customized by changing the color scheme in the `UI_COLORS` dictionary in `plant_disease_gui.py`.

## 📚 Documentation

For detailed information about the system's architecture and functionality, refer to the documentation in the `Plant_Disease_Expert_System_Documentation.md` file.
