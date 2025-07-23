"""
Plant Disease Expert System - Modern GUI

This module provides a modern graphical user interface for the plant disease
diagnosis expert system using Tkinter with a sleek, professional design.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import customtkinter as ctk  # Modern UI toolkit based on tkinter
from PIL import Image, ImageTk  # For handling images
from knowledge_base import ALL_SYMPTOMS, SYMPTOM_NAMES, SYMPTOM_SEVERITY, PLANT_CATEGORIES
from inference_engine import InferenceEngine
import json
import os
import datetime
import re
from functools import partial
import io
import sys
from contextlib import redirect_stdout
import webbrowser  # For opening links to more information
import platform  # For OS detection

# For PDF export
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListItem, ListFlowable, Image as ReportLabImage
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Configure customtkinter appearance
ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"

# Constants
APP_VERSION = "2.0"
APP_NAME = "Plant Disease Expert System"
DEFAULT_FONT = "Segoe UI Variable" if platform.system() == "Windows" else ("SF Pro Text" if platform.system() == "Darwin" else "Ubuntu")
DEFAULT_PADDING = 10
CORNER_RADIUS = 8

# Import required assets
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# UI Color Scheme
UI_COLORS = {
    'primary': "#2E7D32",        # Dark green - primary color
    'primary_light': "#4CAF50",  # Lighter green
    'primary_dark': "#1B5E20",   # Darker green
    'secondary': "#03A9F4",      # Blue - secondary accent
    'secondary_dark': "#0288D1", # Darker blue
    'text_primary': "#212121",   # Very dark gray - primary text
    'text_secondary': "#757575", # Medium gray - secondary text
    'text_light': "#FFFFFF",     # White - text on dark backgrounds
    'bg_light': "#F5F5F5",       # Very light gray - main background
    'card_bg': "#FFFFFF",        # White - card backgrounds
    'divider': "#EEEEEE",        # Light gray - dividers
    'error': "#F44336",          # Red - errors/warnings
    'warning': "#FFC107",        # Amber - warnings
    'success': "#4CAF50",        # Green - success
    'info': "#2196F3",           # Blue - information
    'low_severity': "#81C784",   # Light green for low severity
    'medium_severity': "#FFB74D", # Orange for medium severity
    'high_severity': "#E57373",  # Red for high severity
    'shadow': "#000000",         # Shadow color (alpha applied in code)
    'hover': "#E0E0E0",          # Hover color for elements
    'active': "#BDBDBD",         # Active/pressed color
    'border': "#E0E0E0",         # Border color
    'border_focus': "#2196F3",   # Border color when focused
    'badge_bg': "#E91E63",       # Background for notification badges
    'tooltip_bg': "#333333",     # Tooltip background color
    'tooltip_text': "#FFFFFF",   # Tooltip text color
    'delete': "#FF0000",          # Red - delete button
    'delete_hover': "#CC0000",     # Darker red - hover color for delete button
}

# Advanced settings
SETTINGS = {
    'animations': True,
    'tooltips': True,
    'auto_save': True,
    'expert_mode': False,
    'auto_update_check': True
}

# Add responsive scaling option at the top of the file
# After the DEFAULT_FONT declaration
DEFAULT_SCALING_FACTOR = 1.0  # Base scaling factor
SCALING_ENABLED = True  # Enable responsive scaling

class CreateToolTip:
    """
    Create a tooltip for a given widget with customized appearance.
    """
    def __init__(self, widget, text='Tooltip', bg_color=None, text_color=None, font=None):
        self.widget = widget
        self.text = text
        self.bg_color = bg_color or UI_COLORS.get('tooltip_bg', "#333333")
        self.text_color = text_color or UI_COLORS.get('tooltip_text', "#FFFFFF")
        self.font = font or (DEFAULT_FONT, 10)
        
        # Store the widget's event IDs for later cleanup
        self.widget_enter_id = self.widget.bind("<Enter>", self.on_enter)
        self.widget_leave_id = self.widget.bind("<Leave>", self.on_leave)
        self.tooltip = None
        self.scheduled_id = None
    
    def on_enter(self, event=None):
        # Schedule tooltip display after a small delay
        try:
            if self.scheduled_id:
                self.widget.after_cancel(self.scheduled_id)
            self.scheduled_id = self.widget.after(600, self.show_tooltip)
        except (tk.TclError, AttributeError):
            # Widget might have been destroyed
            self.cleanup()
    
    def on_leave(self, event=None):
        # Cancel scheduled tooltip and hide if shown
        try:
            if self.scheduled_id:
                self.widget.after_cancel(self.scheduled_id)
                self.scheduled_id = None
                
            self.hide_tooltip()
        except (tk.TclError, AttributeError):
            # Widget might have been destroyed
            self.cleanup()
    
    def show_tooltip(self):
        """Display the tooltip with animation."""
        try:
            # Get widget's screen position
            x, y, _, _ = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 25
            
            # Create tooltip window
            self.tooltip = tk.Toplevel(self.widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            # Create tooltip content
            frame = ctk.CTkFrame(
                self.tooltip,
                fg_color=self.bg_color,
                corner_radius=6,
                border_width=0
            )
            frame.pack(ipadx=3, ipady=3)
            
            label = ctk.CTkLabel(
                frame,
                text=self.text,
                text_color=self.text_color,
                font=ctk.CTkFont(family=self.font[0], size=self.font[1]),
                justify=tk.LEFT
            )
            label.pack(padx=8, pady=6)
            
            # Add fade-in effect
            self.tooltip.attributes("-alpha", 0.0)
            self._fade_in()
            
            # Auto-close after 5 seconds
            self.scheduled_id = self.widget.after(5000, self.hide_tooltip)
        except (tk.TclError, AttributeError):
            # Widget might have been destroyed during tooltip creation
            self.cleanup()
    
    def _fade_in(self, alpha=0.0):
        """Animate the tooltip fade-in."""
        try:
            if self.tooltip:
                if alpha < 1.0:
                    alpha += 0.1
                    self.tooltip.attributes("-alpha", alpha)
                    self.tooltip.after(20, lambda: self._fade_in(alpha))
        except (tk.TclError, AttributeError):
            # Widget might have been destroyed during animation
            self.cleanup()
    
    def hide_tooltip(self):
        """Hide and destroy the tooltip."""
        try:
            if self.tooltip:
                self.tooltip.destroy()
                self.tooltip = None
        except (tk.TclError, AttributeError):
            # Widget might have been destroyed during hiding
            self.tooltip = None
    
    def cleanup(self):
        """Clean up all event bindings and destroy tooltip."""
        try:
            # Unbind events if widget still exists
            if self.widget.winfo_exists():
                self.widget.unbind("<Enter>", self.widget_enter_id)
                self.widget.unbind("<Leave>", self.widget_leave_id)
        except (tk.TclError, AttributeError):
            pass
            
        # Destroy tooltip if it exists
        try:
            if self.tooltip and self.tooltip.winfo_exists():
                self.tooltip.destroy()
        except (tk.TclError, AttributeError):
            pass
            
        # Clear scheduled callbacks
        try:
            if self.scheduled_id and self.widget.winfo_exists():
                self.widget.after_cancel(self.scheduled_id)
        except (tk.TclError, AttributeError):
            pass
        
        # Reset all attributes
        self.tooltip = None
        self.scheduled_id = None

class PlantDiseaseExpertGUI:
    """
    Modern GUI application for the Plant Disease Expert System.
    """
    
    def __init__(self, root):
        """Initialize the expert system GUI."""
        # Initialize root window
        self.root = root
        
        # Set window properties
        self.root.title("Plant Disease Expert System")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Initialize engine
        self.engine = InferenceEngine()
        
        # Check dependencies and setup UI
        self.check_dependencies()
        
        # Configuration variables
        self.current_plant_type = tk.StringVar(value="All Plants")
        self.filter_active = False
        
        # Add debounce variables for search performance
        self._search_after_id = None
        self._last_search_time = 0
        self._debounce_delay = 300  # milliseconds
        
        # Create variables for all symptoms
        self.symptom_vars = {symptom: tk.BooleanVar(value=False) for symptom in ALL_SYMPTOMS}
        self.severity_vars = {symptom: tk.StringVar(value="0") for symptom in ALL_SYMPTOMS}
        
        # Add severity descriptions and colors for performance
        self.severity_descriptions = {
            0: "None",
            1: "Very mild",
            2: "Mild",
            3: "Moderate",
            4: "Severe",
            5: "Very severe"
        }
        
        self.severity_colors = {
            0: "gray80",
            1: UI_COLORS['low_severity'],
            2: UI_COLORS['low_severity'],
            3: UI_COLORS['medium_severity'],
            4: UI_COLORS['medium_severity'],
            5: UI_COLORS['high_severity']
        }
        
        # Store diagnosis history
        self.diagnosis_history = []
        
        # Environmental factors (new)
        self.environmental_factors = {
            'temperature': tk.StringVar(value="moderate"),
            'humidity': tk.StringVar(value="moderate"),
            'soil_moisture': tk.StringVar(value="moderate"),
            'light': tk.StringVar(value="full_sun"),
            'air_circulation': tk.StringVar(value="good"),
            'season': tk.StringVar(value="summer")
        }
        
        # Get plant types from categories
        self.plant_types = ["All Plants"]
        for category, plants in PLANT_CATEGORIES.items():
            self.plant_types.extend(plants)
        # Remove duplicates and sort
        self.plant_types = ["All Plants"] + sorted(list(set(self.plant_types) - {"All Plants"}))
        
        # Path for saved data
        self.saved_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_data")
        os.makedirs(self.saved_data_dir, exist_ok=True)
        
        # Track visible/filtered symptoms
        self.visible_symptoms = list(ALL_SYMPTOMS)
        
        # Store current diagnosis results
        self.current_results = []
        
        # Store symptom frames for updating UI
        self.symptom_frames = {}
        
        # Create the main layout
        self.create_layout()
    
    def check_dependencies(self):
        """Check if all required dependencies are installed."""
        missing_dependencies = []
        
        try:
            import customtkinter
        except ImportError:
            missing_dependencies.append("customtkinter")
            
        try:
            from PIL import Image, ImageTk
        except ImportError:
            missing_dependencies.append("pillow")
        
        if not REPORTLAB_AVAILABLE:
            missing_dependencies.append("reportlab (optional, for PDF export)")
        
        if missing_dependencies:
            message = "Some dependencies are missing. Install them for full functionality:\n\n"
            for dep in missing_dependencies:
                message += f"- {dep}\n"
            message += "\nInstall with: pip install package-name"
            messagebox.showwarning("Missing Dependencies", message)
    
    def create_layout(self):
        """Create the main application layout with modern UI components."""
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)  # Header
        self.root.grid_rowconfigure(1, weight=1)  # Content
        self.root.grid_rowconfigure(2, weight=0)  # Footer
        
        # Create header frame with logo and title
        self.create_header()
        
        # Create main content frame
        content_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=UI_COLORS['bg_light'])
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel (symptoms selection)
        self.create_left_panel(content_frame)
        
        # Right panel (results and history)
        self.create_right_panel(content_frame)
        
        # Footer with buttons
        self.create_footer()
    
    def create_header(self):
        """Create application header with logo and title."""
        header_frame = ctk.CTkFrame(self.root, corner_radius=0, height=70, fg_color=UI_COLORS['primary'])
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=0)  # Logo
        header_frame.grid_columnconfigure(1, weight=1)  # Title
        header_frame.grid_columnconfigure(2, weight=0)  # Settings
        
        # Try to load and display logo
        try:
            logo_path = os.path.join(ASSETS_DIR, "plant_logo.png")
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path).resize((50, 50))
                logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = ctk.CTkLabel(header_frame, image=logo_photo, text="")
                logo_label.image = logo_photo  # Keep reference
                logo_label.grid(row=0, column=0, padx=20, pady=10)
            else:
                # If no logo file, use an emoji as a placeholder
                logo_label = ctk.CTkLabel(header_frame, text="🌿", font=ctk.CTkFont(family=DEFAULT_FONT, size=28, weight="bold"))
                logo_label.grid(row=0, column=0, padx=20, pady=10)
        except Exception as e:
            # Fallback to text if image loading fails
            logo_label = ctk.CTkLabel(header_frame, text="🌿", font=ctk.CTkFont(family=DEFAULT_FONT, size=28, weight="bold"))
            logo_label.grid(row=0, column=0, padx=20, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text=APP_NAME,
            font=ctk.CTkFont(family=DEFAULT_FONT, size=22, weight="bold"),
            text_color=UI_COLORS['text_light']
        )
        title_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Settings button
        settings_button = ctk.CTkButton(
            header_frame,
            text="⚙️ Settings",
            command=self.open_settings,
            fg_color="transparent",
            border_width=0,
            hover_color=UI_COLORS['primary_dark'],
            text_color=UI_COLORS['text_light'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        settings_button.grid(row=0, column=2, padx=20, pady=10)
    
    def create_left_panel(self, parent):
        """Create left panel with plant type selection, search, and symptoms."""
        left_frame = ctk.CTkFrame(parent, corner_radius=CORNER_RADIUS, fg_color=UI_COLORS['card_bg'])
        left_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
        # Configure grid
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(0, weight=0)  # Plant selection
        left_frame.grid_rowconfigure(1, weight=0)  # Search
        left_frame.grid_rowconfigure(2, weight=1)  # Symptoms
        left_frame.grid_rowconfigure(3, weight=0)  # Environmental Factors
        
        # Plant Type Selection
        plant_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        plant_frame.grid(row=0, column=0, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky="ew")
        
        plant_label = ctk.CTkLabel(
            plant_frame,
            text="Plant Type:",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=14),
            text_color=UI_COLORS['text_primary']
        )
        plant_label.pack(side=tk.LEFT, padx=(0, 10))
        
        plant_combobox = ctk.CTkComboBox(
            plant_frame,
            values=self.plant_types,
            variable=self.current_plant_type,
            width=200,
            state="readonly",
            command=self.filter_symptoms_by_plant
        )
        plant_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # View by category button
        category_button = ctk.CTkButton(
            plant_frame,
            text="View by Category",
            command=self.view_plant_categories,
            fg_color=UI_COLORS['secondary'],
            hover_color=UI_COLORS['secondary_dark'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        category_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Search bar for symptoms
        self.search_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        self.search_frame.grid(row=1, column=0, padx=DEFAULT_PADDING, pady=(0, DEFAULT_PADDING), sticky="ew")
        
        search_label = ctk.CTkLabel(
            self.search_frame,
            text="Search Symptoms:",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=14),
            text_color=UI_COLORS['text_primary']
        )
        search_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.search_symptoms())
        
        search_entry = ctk.CTkEntry(
            self.search_frame,
            textvariable=self.search_var,
            placeholder_text="Type to search...",
            width=200
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Add a clear button to the right of the search entry
        self.clear_button = ctk.CTkButton(
            self.search_frame,
            text="✕",
            width=30,
            fg_color=UI_COLORS['delete'],
            hover_color=UI_COLORS['delete_hover'],
            command=self.clear_search  # Changed from clear_all_symptoms to clear_search
        )
        self.clear_button.pack(side=tk.RIGHT, padx=5)
        
        # Symptoms container with scrollable frame
        symptoms_frame = ctk.CTkFrame(left_frame)
        symptoms_frame.grid(row=2, column=0, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky="nsew")
        symptoms_frame.grid_columnconfigure(0, weight=1)
        symptoms_frame.grid_rowconfigure(0, weight=1)
        
        # Create scrollable frame for symptoms
        self.symptoms_scrollable = ctk.CTkScrollableFrame(
            symptoms_frame,
            label_text="Symptoms",
            label_font=ctk.CTkFont(family=DEFAULT_FONT, size=14, weight="bold")
        )
        self.symptoms_scrollable.grid(row=0, column=0, sticky="nsew")
        
        # Populate symptoms (will be done in update_symptom_display method)
        self.update_symptom_display()
        
        # Environmental factors frame (collapsible)
        self.env_frame = ctk.CTkFrame(left_frame)
        self.env_frame.grid(row=3, column=0, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky="ew")
        
        # Environmental factors header with toggle button
        env_header = ctk.CTkFrame(self.env_frame, fg_color="transparent")
        env_header.pack(fill=tk.X, padx=5, pady=5)
        
        env_label = ctk.CTkLabel(
            env_header,
            text="Environmental Factors",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=14, weight="bold"),
            text_color=UI_COLORS['text_primary']
        )
        env_label.pack(side=tk.LEFT)
        
        self.env_expanded = tk.BooleanVar(value=False)
        self.env_toggle_btn = ctk.CTkButton(
            env_header,
            text="▼ Show",
            command=self.toggle_env_factors,
            width=80,
            fg_color=UI_COLORS['primary_light'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        self.env_toggle_btn.pack(side=tk.RIGHT)
        
        # Environmental factors content (initially hidden)
        self.env_content = ctk.CTkFrame(self.env_frame, fg_color="transparent")
        
        # Create environmental factor options
        self.create_env_factors()
    
    def create_env_factors(self):
        """Create UI elements for environmental factors."""
        factors = [
            ("Temperature", "temperature", ["cold", "cool", "moderate", "warm", "hot"]),
            ("Humidity", "humidity", ["very_low", "low", "moderate", "high", "very_high"]),
            ("Soil Moisture", "soil_moisture", ["dry", "slightly_moist", "moderate", "moist", "wet"]),
            ("Light Condition", "light", ["deep_shade", "partial_shade", "filtered_light", "full_sun", "intense_sun"]),
            ("Air Circulation", "air_circulation", ["poor", "fair", "good", "excellent"]),
            ("Season", "season", ["spring", "summer", "fall", "winter"])
        ]
        
        for i, (label_text, factor_key, options) in enumerate(factors):
            factor_frame = ctk.CTkFrame(self.env_content, fg_color="transparent")
            factor_frame.pack(fill=tk.X, padx=5, pady=5)
            
            label = ctk.CTkLabel(
                factor_frame,
                text=label_text + ":",
                font=ctk.CTkFont(family=DEFAULT_FONT, size=12),
                width=100,
                anchor="w"
            )
            label.pack(side=tk.LEFT)
            
            # Convert options to more readable format for display
            display_options = [opt.replace('_', ' ').title() for opt in options]
            
            combobox = ctk.CTkComboBox(
                factor_frame,
                values=display_options,
                command=lambda selected, key=factor_key, opts=options: self.set_env_factor(key, selected, opts),
                variable=self.environmental_factors[factor_key],
                width=150,
                state="readonly"
            )
            combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
            combobox.set(display_options[options.index(self.environmental_factors[factor_key].get())])
    
    def set_env_factor(self, key, selected_display, options):
        """Set environmental factor based on selection."""
        # Convert display value back to internal value
        selected_index = [opt.replace('_', ' ').title() for opt in options].index(selected_display)
        self.environmental_factors[key].set(options[selected_index])
    
    def toggle_env_factors(self):
        """Toggle visibility of environmental factors panel."""
        is_expanded = self.env_expanded.get()
        if is_expanded:
            self.env_content.pack_forget()
            self.env_toggle_btn.configure(text="▼ Show")
        else:
            self.env_content.pack(fill=tk.X, padx=5, pady=5)
            self.env_toggle_btn.configure(text="▲ Hide")
        
        self.env_expanded.set(not is_expanded)
    
    def create_right_panel(self, parent):
        """Create right panel with diagnosis results and history."""
        right_frame = ctk.CTkFrame(parent, corner_radius=CORNER_RADIUS, fg_color=UI_COLORS['card_bg'])
        right_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        
        # Configure grid
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=0)  # Actions
        right_frame.grid_rowconfigure(1, weight=1)  # Tabview
        
        # Action buttons
        actions_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=0, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky="ew")
        
        save_button = ctk.CTkButton(
            actions_frame,
            text="Save Session",
            command=self.save_symptom_selection,
            fg_color=UI_COLORS['primary'],
            hover_color=UI_COLORS['primary_dark'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        load_button = ctk.CTkButton(
            actions_frame,
            text="Load Session",
            command=self.load_symptom_selection,
            fg_color=UI_COLORS['primary'],
            hover_color=UI_COLORS['primary_dark'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        load_button.pack(side=tk.LEFT, padx=(0, 10))
        
        export_menu_button = ctk.CTkButton(
            actions_frame,
            text="Export Results",
            command=self.show_export_menu,
            fg_color=UI_COLORS['secondary'],
            hover_color=UI_COLORS['secondary_dark'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        export_menu_button.pack(side=tk.LEFT)
        
        diagnose_button = ctk.CTkButton(
            actions_frame,
            text="Diagnose",
            command=self.diagnose,
            fg_color=UI_COLORS['success'],
            hover_color=UI_COLORS['primary_dark'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=14, weight="bold"),
            height=35
        )
        diagnose_button.pack(side=tk.RIGHT)
        
        # Create tabview for results and history
        self.results_tabview = ctk.CTkTabview(right_frame)
        self.results_tabview.grid(row=1, column=0, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky="nsew")
        
        # Add tabs
        self.results_tabview.add("Diagnosis Results")
        self.results_tabview.add("Diagnosis History")
        self.results_tabview.add("Plant Guide")
        
        # Configure tabs
        self.results_tabview.tab("Diagnosis Results").grid_columnconfigure(0, weight=1)
        self.results_tabview.tab("Diagnosis Results").grid_rowconfigure(0, weight=1)
        
        self.results_tabview.tab("Diagnosis History").grid_columnconfigure(0, weight=1)
        self.results_tabview.tab("Diagnosis History").grid_rowconfigure(0, weight=0)  # History list
        self.results_tabview.tab("Diagnosis History").grid_rowconfigure(1, weight=1)  # History details
        self.results_tabview.tab("Diagnosis History").grid_rowconfigure(2, weight=0)  # History buttons
        
        self.results_tabview.tab("Plant Guide").grid_columnconfigure(0, weight=1)
        self.results_tabview.tab("Plant Guide").grid_rowconfigure(0, weight=1)
        
        # Results textbox
        self.results_text = ctk.CTkTextbox(
            self.results_tabview.tab("Diagnosis Results"),
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12),
            wrap="word",
            padx=15,
            pady=10
        )
        self.results_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # History tab components
        history_list_frame = ctk.CTkFrame(self.results_tabview.tab("Diagnosis History"))
        history_list_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        history_label = ctk.CTkLabel(
            history_list_frame,
            text="Previous Diagnoses:",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=14, weight="bold"),
            anchor="w"
        )
        history_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # History listbox (using standard Listbox as CTk doesn't have an equivalent)
        history_list_frame_inner = tk.Frame(history_list_frame, bg=UI_COLORS['card_bg'])
        history_list_frame_inner.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5, pady=5)
        
        self.history_listbox = tk.Listbox(
            history_list_frame_inner,
            bg=UI_COLORS['card_bg'],
            fg=UI_COLORS['text_primary'],
            font=(DEFAULT_FONT, 12),
            height=6,
            selectbackground=UI_COLORS['primary'],
            selectforeground=UI_COLORS['text_light'],
            relief="flat",
            borderwidth=1
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.history_listbox.bind('<<ListboxSelect>>', self.load_history_item)
        
        history_scrollbar = ttk.Scrollbar(history_list_frame_inner, orient="vertical")
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox.config(yscrollcommand=history_scrollbar.set)
        history_scrollbar.config(command=self.history_listbox.yview)
        
        # History details text
        self.history_text = ctk.CTkTextbox(
            self.results_tabview.tab("Diagnosis History"),
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12),
            wrap="word",
            padx=15,
            pady=10
        )
        self.history_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Add history buttons frame below the text
        self.history_buttons_frame = ctk.CTkFrame(self.results_tabview.tab("Diagnosis History"))
        self.history_buttons_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        # Plant guide tab
        plant_guide_frame = ctk.CTkScrollableFrame(
            self.results_tabview.tab("Plant Guide"),
            fg_color="transparent"
        )
        plant_guide_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        plant_guide_frame.grid_columnconfigure(0, weight=1)
        
        # Plant guide content
        self.create_plant_guide(plant_guide_frame)
    
    def create_plant_guide(self, parent):
        """Create content for the plant guide tab."""
        guide_title = ctk.CTkLabel(
            parent,
            text="Plant Care Guide",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=16, weight="bold"),
            anchor="w"
        )
        guide_title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        guide_desc = ctk.CTkLabel(
            parent,
            text="Basic information about caring for common plants and preventing diseases.",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12),
            anchor="w",
            wraplength=600
        )
        guide_desc.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")
        
        # Plant categories
        row = 2
        for category, plants in PLANT_CATEGORIES.items():
            category_frame = ctk.CTkFrame(parent, fg_color=UI_COLORS['primary_light'])
            category_frame.grid(row=row, column=0, padx=10, pady=(10, 5), sticky="ew")
            
            category_label = ctk.CTkLabel(
                category_frame,
                text=category,
                font=ctk.CTkFont(family=DEFAULT_FONT, size=14, weight="bold"),
                text_color=UI_COLORS['text_light'],
                anchor="w"
            )
            category_label.pack(padx=10, pady=5, fill=tk.X)
            
            row += 1
            
            # Add some plants from this category
            for i, plant in enumerate(plants[:5]):  # Show up to 5 plants per category
                plant_btn = ctk.CTkButton(
                    parent,
                    text=plant,
                    command=lambda p=plant: self.show_plant_info(p),
                    fg_color="transparent",
                    text_color=UI_COLORS['primary'],
                    hover_color=UI_COLORS['divider'],
                    anchor="w",
                    font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
                )
                plant_btn.grid(row=row, column=0, padx=20, pady=2, sticky="w")
                row += 1
            
            if len(plants) > 5:
                more_btn = ctk.CTkButton(
                    parent,
                    text=f"View {len(plants) - 5} more {category.lower()}...",
                    command=lambda cat=category: self.show_plant_category(cat),
                    fg_color="transparent",
                    text_color=UI_COLORS['secondary'],
                    hover_color=UI_COLORS['divider'],
                    anchor="w",
                    font=ctk.CTkFont(family=DEFAULT_FONT, size=12, slant="italic")
                )
                more_btn.grid(row=row, column=0, padx=20, pady=2, sticky="w")
                row += 1
    
    def create_footer(self):
        """Create application footer with status and buttons."""
        footer_frame = ctk.CTkFrame(self.root, corner_radius=0, height=40, fg_color=UI_COLORS['bg_light'])
        footer_frame.grid(row=2, column=0, sticky="ew")
        footer_frame.grid_columnconfigure(0, weight=1)  # Status
        footer_frame.grid_columnconfigure(1, weight=0)  # Buttons
        
        # Status label
        self.status_label = ctk.CTkLabel(
            footer_frame,
            text=f"{APP_NAME} v{APP_VERSION} | Ready",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=10),
            text_color=UI_COLORS['text_secondary']
        )
        self.status_label.grid(row=0, column=0, padx=15, pady=5, sticky="w")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, padx=15, pady=5, sticky="e")
        
        help_button = ctk.CTkButton(
            buttons_frame,
            text="Help",
            command=self.show_help,
            width=80,
            height=25,
            fg_color=UI_COLORS['text_secondary'],
            text_color=UI_COLORS['text_light'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=11)
        )
        help_button.pack(side=tk.LEFT, padx=(0, 10))
        
        about_button = ctk.CTkButton(
            buttons_frame,
            text="About",
            command=self.show_about,
            width=80,
            height=25,
            fg_color=UI_COLORS['text_secondary'],
            text_color=UI_COLORS['text_light'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=11)
        )
        about_button.pack(side=tk.LEFT, padx=(0, 10))
        
        exit_button = ctk.CTkButton(
            buttons_frame,
            text="Exit", 
            command=self.root.destroy,
            width=80,
            height=25,
            fg_color=UI_COLORS['error'],
            text_color=UI_COLORS['text_light'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=11)
        )
        exit_button.pack(side=tk.LEFT)
    
    def open_settings(self):
        """Open settings dialog with improved efficiency."""
        # Check if settings window already exists
        if hasattr(self, 'settings_window') and self.settings_window is not None:
            # Bring existing window to front instead of creating a new one
            self.settings_window.focus_set()
            return
            
        # Create new settings window
        self.settings_window = ctk.CTkToplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("500x400")
        self.settings_window.transient(self.root)
        self.settings_window.grab_set()
        
        # Make window modal
        self.settings_window.focus_set()
        self.settings_window.resizable(False, False)
        
        # Store reference to destroy on window close
        self.settings_window.protocol("WM_DELETE_WINDOW", self._on_settings_close)
        
        # Cache settings values to avoid frequent dictionary lookups
        cached_settings = {k: v for k, v in SETTINGS.items()}
        
        # Settings content
        settings_frame = ctk.CTkFrame(self.settings_window)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            settings_frame,
            text="Application Settings",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=16, weight="bold")
        )
        title_label.pack(pady=(0, 15))
        
        # Settings options - using grid for better performance
        settings_grid = ctk.CTkFrame(settings_frame, fg_color="transparent")
        settings_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Track setting variables for immediate apply
        self.setting_vars = {}
        
        # Create settings grid
        for i, (setting, value) in enumerate(cached_settings.items()):
            self.setting_vars[setting] = tk.BooleanVar(value=value)
            
            # Format setting name for display
            display_name = setting.replace('_', ' ').title()
            
            # Create tooltip descriptions based on setting name
            tooltip_text = {
                'animations': "Enable UI animations for smooth transitions",
                'tooltips': "Show helpful tooltips when hovering over elements",
                'auto_save': "Automatically save your selections",
                'expert_mode': "Enable advanced features for experienced users",
                'auto_update_check': "Check for updates when application starts"
            }.get(setting, f"Toggle {display_name}")
            
            # Create setting row
            setting_frame = ctk.CTkFrame(settings_grid, fg_color="transparent")
            setting_frame.pack(fill=tk.X, pady=5)
            
            # Label with description
            setting_label = ctk.CTkLabel(
                setting_frame,
                text=display_name,
                font=ctk.CTkFont(family=DEFAULT_FONT, size=12),
                anchor="w",
                width=150
            )
            setting_label.pack(side=tk.LEFT, padx=10, fill=tk.X)
            
            # Tooltip for the label
            try:
                CreateToolTip(setting_label, tooltip_text)
            except:
                pass  # Skip tooltip if not supported
            
            # Switch with optimized callback
            setting_switch = ctk.CTkSwitch(
                setting_frame,
                text="",
                variable=self.setting_vars[setting],
                command=lambda s=setting, v=self.setting_vars[setting]: self._fast_update_setting(s, v),
                font=ctk.CTkFont(family=DEFAULT_FONT, size=12),
                width=50,
                progress_color=UI_COLORS['primary_light'],
                button_color=UI_COLORS['primary'],
                button_hover_color=UI_COLORS['primary_dark']
            )
            setting_switch.pack(side=tk.RIGHT, padx=10)
        
        # Apply and Cancel buttons
        button_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        # Reset to defaults button
        reset_button = ctk.CTkButton(
            button_frame,
            text="Reset to Defaults",
            command=self._reset_settings_to_default,
            fg_color=UI_COLORS['secondary'],
            hover_color=UI_COLORS['secondary_dark'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        reset_button.pack(side=tk.LEFT, padx=10)
        
        # Close button
        close_button = ctk.CTkButton(
            button_frame,
            text="Save & Close",
            command=self._on_settings_close,
            fg_color=UI_COLORS['primary'],
            hover_color=UI_COLORS['primary_dark'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        close_button.pack(side=tk.RIGHT, padx=10)
    
    def _on_settings_close(self):
        """Handle settings window close with cleanup."""
        # Apply any pending changes
        self.apply_settings()
        
        # Clear reference and destroy window
        if hasattr(self, 'settings_window') and self.settings_window is not None:
            self.settings_window.destroy()
            self.settings_window = None
    
    def _fast_update_setting(self, setting, var):
        """Update setting with optimized performance."""
        # Get value directly from variable to avoid extra calls
        value = var.get()
        
        # Update the setting in the global settings dict
        SETTINGS[setting] = value
        
        # Apply immediate effect for relevant settings
        if setting == 'animations':
            # Apply animations setting immediately
            if value:
                # Enable animations
                pass  # Animation effects are controlled when triggered
            else:
                # Disable animations
                pass  # Animation effects are controlled when triggered
        elif setting == 'tooltips':
            # Update tooltips visibility
            if not value:
                # Hide any active tooltips
                if hasattr(self, 'current_tooltips'):
                    for tooltip in self.current_tooltips:
                        try:
                            tooltip.hide_tooltip()
                        except:
                            pass
        elif setting == 'auto_save':
            # Apply auto-save setting
            if value and hasattr(self, 'symptoms_scrollable'):
                # Save current state
                self.save_symptom_selection()
        elif setting == 'expert_mode':
            # Toggle expert mode immediately
            if value:
                # Show advanced options
                if hasattr(self, 'expert_options_frame'):
                    self.expert_options_frame.pack(fill=tk.X, padx=10, pady=5)
            else:
                # Hide advanced options
                if hasattr(self, 'expert_options_frame'):
                    self.expert_options_frame.pack_forget()
    
    def _reset_settings_to_default(self):
        """Reset all settings to default values."""
        default_settings = {
            'animations': True,
            'tooltips': True,
            'auto_save': True,
            'expert_mode': False,
            'auto_update_check': True
        }
        
        # Update global settings
        for setting, value in default_settings.items():
            SETTINGS[setting] = value
            
            # Update UI variables if they exist
            if hasattr(self, 'setting_vars') and setting in self.setting_vars:
                self.setting_vars[setting].set(value)
        
        # Apply changes immediately
        self.apply_settings()
    
    def apply_settings(self):
        """Apply all settings changes to the UI."""
        # Apply animations setting
        if not SETTINGS['animations']:
            # Disable animations
            pass
        
        # Apply expert mode setting
        if SETTINGS['expert_mode']:
            # Show advanced options
            if hasattr(self, 'expert_options_frame'):
                self.expert_options_frame.pack(fill=tk.X, padx=10, pady=5)
        else:
            # Hide advanced options
            if hasattr(self, 'expert_options_frame'):
                self.expert_options_frame.pack_forget()
        
        # Apply auto-save setting
        if SETTINGS['auto_save'] and hasattr(self, 'symptoms_scrollable'):
            # Save current state
            self.save_symptom_selection()
    
    def update_setting(self, setting, value):
        """Update a setting value (legacy method maintained for compatibility)."""
        SETTINGS[setting] = value
        
        # Also update through the fast update if possible
        if hasattr(self, 'setting_vars') and setting in self.setting_vars:
            self.setting_vars[setting].set(value)
            self._fast_update_setting(setting, self.setting_vars[setting])
        else:
            # Apply the setting without the UI variables
            self.apply_settings()
    
    def select_plant_from_category(self, plant, window):
        """Select a plant from the category view and close the window."""
        self.current_plant_type.set(plant)
        self.filter_symptoms_by_plant()
        window.destroy()
    
    def show_plant_info(self, plant):
        """Show detailed information about a specific plant."""
        info_window = ctk.CTkToplevel(self.root)
        info_window.title(f"{plant} Information")
        info_window.geometry("600x500")
        info_window.transient(self.root)
        
        # Make window modal
        info_window.focus_set()
        
        # Content frame
        content_frame = ctk.CTkScrollableFrame(info_window)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            content_frame,
            text=plant,
            font=ctk.CTkFont(family=DEFAULT_FONT, size=18, weight="bold")
        )
        title_label.pack(pady=(0, 15))
        
        # Plant image placeholder
        try:
            image_path = os.path.join(ASSETS_DIR, f"{plant.lower().replace(' ', '_')}.png")
            if os.path.exists(image_path):
                plant_img = Image.open(image_path).resize((200, 200))
                photo = ImageTk.PhotoImage(plant_img)
                img_label = ctk.CTkLabel(content_frame, image=photo, text="")
                img_label.image = photo
                img_label.pack(pady=10)
            else:
                # Placeholder text if no image
                img_placeholder = ctk.CTkLabel(
                    content_frame,
                    text="🌱",
                    font=ctk.CTkFont(size=48)
                )
                img_placeholder.pack(pady=10)
        except Exception:
            # Fallback if image loading fails
            img_placeholder = ctk.CTkLabel(
                content_frame,
                text="🌱",
                font=ctk.CTkFont(size=48)
            )
            img_placeholder.pack(pady=10)
        
        # Common diseases section
        diseases_frame = ctk.CTkFrame(content_frame)
        diseases_frame.pack(fill=tk.X, pady=10)
        
        diseases_label = ctk.CTkLabel(
            diseases_frame,
            text="Common Diseases",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=14, weight="bold")
        )
        diseases_label.pack(padx=10, pady=5, anchor="w")
        
        # Get diseases for this plant
        plant_diseases = []
        for disease, data in self.engine.knowledge_base.items():
            if 'plant_types' in data and plant in data['plant_types']:
                disease_name = disease.replace('_', ' ').title()
                plant_diseases.append((disease_name, data['description'][:100] + "..."))
        
        if plant_diseases:
            for disease_name, desc in plant_diseases:
                disease_item = ctk.CTkFrame(diseases_frame, fg_color="transparent")
                disease_item.pack(fill=tk.X, padx=10, pady=5)
                
                disease_title = ctk.CTkLabel(
                    disease_item,
                    text=disease_name,
                    font=ctk.CTkFont(family=DEFAULT_FONT, size=12, weight="bold"),
                    anchor="w"
                )
                disease_title.pack(fill=tk.X)
                
                disease_desc = ctk.CTkLabel(
                    disease_item,
                    text=desc,
                    font=ctk.CTkFont(family=DEFAULT_FONT, size=11),
                    wraplength=500,
                    anchor="w",
                    justify="left"
                )
                disease_desc.pack(fill=tk.X)
        else:
            no_diseases = ctk.CTkLabel(
                diseases_frame,
                text="No specific disease information available for this plant.",
                font=ctk.CTkFont(family=DEFAULT_FONT, size=11, slant="italic"),
                text_color=UI_COLORS['text_secondary']
            )
            no_diseases.pack(padx=10, pady=5)
        
        # Care tips
        care_frame = ctk.CTkFrame(content_frame)
        care_frame.pack(fill=tk.X, pady=10)
        
        care_label = ctk.CTkLabel(
            care_frame,
            text="Care Tips",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=14, weight="bold")
        )
        care_label.pack(padx=10, pady=5, anchor="w")
        
        # Generic care tips
        tips = [
            "Ensure proper watering - check soil moisture before watering",
            "Provide adequate light according to plant needs",
            "Monitor for pests and diseases regularly",
            "Use appropriate fertilizer during growing season",
            "Maintain good air circulation to prevent fungal diseases"
        ]
        
        for tip in tips:
            tip_label = ctk.CTkLabel(
                care_frame,
                text=f"• {tip}",
                font=ctk.CTkFont(family=DEFAULT_FONT, size=11),
                wraplength=500,
                anchor="w",
                justify="left"
            )
            tip_label.pack(fill=tk.X, padx=10, pady=2, anchor="w")
        
        # Select plant button
        select_button = ctk.CTkButton(
            content_frame,
            text=f"Select {plant} for Diagnosis",
            command=lambda: self.select_plant_and_close(plant, info_window),
            fg_color=UI_COLORS['primary'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        select_button.pack(pady=15)
        
        # Close button
        close_button = ctk.CTkButton(
            content_frame,
            text="Close",
            command=info_window.destroy,
            fg_color=UI_COLORS['text_secondary'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        close_button.pack(pady=(0, 15))
    
    def select_plant_and_close(self, plant, window):
        """Select a plant and close the info window."""
        self.current_plant_type.set(plant)
        self.filter_symptoms_by_plant()
        window.destroy()
    
    def show_plant_category(self, category):
        """Show all plants in a specific category."""
        self.view_plant_categories()
    
    def diagnose(self):
        """Diagnose based on selected symptoms with visual feedback."""
        # Get selected symptoms
        selected_symptoms = [s for s in ALL_SYMPTOMS if self.symptom_vars[s].get()]
        
        # Check if any symptoms are selected
        if not selected_symptoms:
            messagebox.showinfo("No Symptoms", "Please select at least one symptom for diagnosis.")
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(tk.END, "No symptoms selected. Please check at least one symptom and try again.", "subtitle")
            return
        
        # Get selected plant type
        plant_type = self.current_plant_type.get()
        
        # Get environmental factors if expanded
        env_factors = None
        if self.env_expanded.get():
            env_factors = {k: v.get() for k, v in self.environmental_factors.items()}
        
        # Show "processing" feedback
        self.status_label.configure(text="Processing diagnosis...")
        
        # Create a progress bar to show diagnosis in progress
        progress_frame = ctk.CTkFrame(self.results_tabview.tab("Diagnosis Results"))
        progress_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        progress_label = ctk.CTkLabel(
            progress_frame,
            text="Analyzing symptoms and environmental factors...",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        progress_label.pack(pady=(10, 5))
        
        progress_bar = ctk.CTkProgressBar(progress_frame, width=300)
        progress_bar.pack(pady=(0, 10), padx=20)
        progress_bar.set(0)
        
        # Prepare the diagnosis data outside of the animation
        severity_data = {s: self.severity_vars[s].get() for s in selected_symptoms}
        results = self.engine.diagnose(selected_symptoms, severity_data, plant_type, env_factors)
        self.current_results = results
        
        # Add to history now
        history_item = {
            "timestamp": datetime.datetime.now(),
            "plant_type": plant_type,
            "symptoms": selected_symptoms,
            "severity": severity_data,
            "environmental_factors": env_factors,
            "results": results
        }
        self.diagnosis_history.append(history_item)
        
        # Animate progress bar
        def update_progress(value):
            progress_bar.set(value)
            if value < 1.0:
                self.root.after(50, update_progress, value + 0.05)
            else:
                # When finished, remove progress frame and show results
                progress_frame.destroy()
                
                # Display results
                self.display_results(results)
                
                # Update history list separately (now that data is already in the list)
                self.update_history_list()
                
                # Switch to results tab
                self.results_tabview.set("Diagnosis Results")
                
                # Show snackbar notification
                self.show_snackbar(f"Diagnosis completed with {len(results)} potential diagnoses")
                
                # Reset status label
                self.status_label.configure(text=f"{APP_NAME} v{APP_VERSION} | Ready")
        
        # Start animation
        self.root.after(100, update_progress, 0)
    
    def show_snackbar(self, message, duration=3000):
        """Show a temporary notification at the bottom of the screen."""
        # Create snackbar frame
        snackbar = ctk.CTkFrame(
            self.root, 
            corner_radius=5,
            fg_color=UI_COLORS['primary_dark'],
        )
        
        # Add drop shadow effect with a slightly larger frame behind it
        shadow = ctk.CTkFrame(
            self.root,
            corner_radius=7,
            fg_color=self.adjust_color_opacity(UI_COLORS['shadow'], 0.2),  # 20% opacity for shadow
        )
        
        # Position the shadow slightly offset
        shadow.place(relx=0.5, rely=0.95, anchor="center", relwidth=0.3, relheight=0.06)
        
        # Position the snackbar over the shadow
        snackbar.place(relx=0.5, rely=0.95, anchor="center", relwidth=0.3, relheight=0.05)
        
        # Add message
        message_label = ctk.CTkLabel(
            snackbar,
            text=message,
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12),
            text_color=UI_COLORS['text_light']
        )
        message_label.pack(pady=8, padx=15)
        
        # Function to destroy snackbar
        def close_snackbar():
            shadow.destroy()
            snackbar.destroy()
        
        # Auto close after duration
        self.root.after(duration, close_snackbar)
    
    def animate_tab_transition(self, tab_name):
        """Animate transition to a new tab."""
        # Get current and target tab
        current_tab = self.results_tabview.get()
        
        # Only animate if changing tabs
        if current_tab != tab_name:
            # Create fade effect
            overlay = ctk.CTkFrame(
                self.results_tabview.tab(current_tab),
                fg_color=self.adjust_color_opacity(UI_COLORS['bg_light'], 0.0)
            )
            overlay.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Fade out current tab
            for alpha in range(0, 10):
                overlay.configure(fg_color=self.adjust_color_opacity(UI_COLORS['bg_light'], alpha/10))
                self.root.update()
                self.root.after(10)
            
            # Change tab
            self.results_tabview.set(tab_name)
            
            # Create overlay on new tab
            new_overlay = ctk.CTkFrame(
                self.results_tabview.tab(tab_name),
                fg_color=self.adjust_color_opacity(UI_COLORS['bg_light'], 1.0)
            )
            new_overlay.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Fade in new tab
            for alpha in range(10, 0, -1):
                new_overlay.configure(fg_color=self.adjust_color_opacity(UI_COLORS['bg_light'], alpha/10))
                self.root.update()
                self.root.after(10)
            
            # Remove overlays
            overlay.destroy()
            new_overlay.destroy()
    
    def display_results(self, results):
        """Display diagnosis results in the text area."""
        # Clear existing content
        self.results_text.delete("1.0", tk.END)
        
        # Get access to the underlying text widget
        text_widget = self.results_text._textbox
        
        # Configure text tags
        text_widget.tag_configure("title", font=(DEFAULT_FONT, 18, "bold"))
        text_widget.tag_configure("subtitle", font=(DEFAULT_FONT, 14, "bold"))
        text_widget.tag_configure("confidence_high", font=(DEFAULT_FONT, 13, "bold"), foreground=UI_COLORS['success'])
        text_widget.tag_configure("confidence_medium", font=(DEFAULT_FONT, 13, "bold"), foreground=UI_COLORS['warning'])
        text_widget.tag_configure("confidence_low", font=(DEFAULT_FONT, 13, "bold"), foreground=UI_COLORS['error'])
        text_widget.tag_configure("normal", font=(DEFAULT_FONT, 12))
        text_widget.tag_configure("bullet", font=(DEFAULT_FONT, 12, "bold"))
        text_widget.tag_configure("italic", font=(DEFAULT_FONT, 12, "italic"))
        text_widget.tag_configure("divider", font=(DEFAULT_FONT, 12), foreground=UI_COLORS['text_secondary'])
        
        if not results:
            self.results_text.insert(tk.END, "No matching diseases found for the selected symptoms.\n\n", "subtitle")
            self.results_text.insert(tk.END, "Try adding more symptoms or adjusting their severity for better results.", "normal")
            return
        
        # Header
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.results_text.insert(tk.END, f"Diagnosis Results - {date_str}\n\n", "title")
        
        # Plant type if specified
        if self.current_plant_type.get() != "All Plants":
            self.results_text.insert(tk.END, f"Plant Type: {self.current_plant_type.get()}\n\n", "subtitle")
        
        # Environmental factors if provided
        if self.env_expanded.get():
            self.results_text.insert(tk.END, "Environmental Conditions:\n", "subtitle")
            for factor, value in self.environmental_factors.items():
                display_factor = factor.replace('_', ' ').title()
                display_value = value.get().replace('_', ' ').title()
                self.results_text.insert(tk.END, f"• {display_factor}: {display_value}\n", "normal")
            self.results_text.insert(tk.END, "\n", "normal")
            
        # Results summary
        self.results_text.insert(tk.END, f"Found {len(results)} potential diagnoses:\n\n", "subtitle")
        
        # Display each result
        for i, result in enumerate(results, 1):
            # Disease name
            self.results_text.insert(tk.END, f"{i}. {result['name']}\n", "title")
            self.results_text.insert(tk.END, "\n", "normal")  # Add extra space after title
            
            # Confidence score with color
            confidence = result['confidence']
            confidence_tag = "confidence_high" if confidence >= 75 else \
                           "confidence_medium" if confidence >= 50 else \
                           "confidence_low"
            confidence_bg = UI_COLORS['success'] if confidence >= 75 else \
                           UI_COLORS['warning'] if confidence >= 50 else \
                           UI_COLORS['error']
            confidence_bg = self.adjust_color_opacity(confidence_bg, 0.2)  # Lighter background
            self.results_text.insert(tk.END, "Confidence: ", "subtitle")
            self.highlight_text(f"{confidence}%\n\n", confidence_tag, confidence_bg)
            
            # Description
            self.results_text.insert(tk.END, "Description:\n", "subtitle")
            self.results_text.insert(tk.END, f"{result['description']}\n\n\n", "normal")  # Extra spacing
            
            # Severity impact
            if 'severity_impact' in result and result['severity_impact']:
                self.results_text.insert(tk.END, "Severity Impact:\n", "subtitle")
                for level, impact in result['severity_impact'].items():
                    level_display = level.title()
                    level_tag = "confidence_low" if level == "low" else \
                               "confidence_medium" if level == "medium" else \
                               "confidence_high"
                    
                    self.results_text.insert(tk.END, f"• {level_display}: ", "bullet")
                    self.results_text.insert(tk.END, f"{impact}\n", level_tag)
            
            # Treatment
            self.results_text.insert(tk.END, "Treatment:\n", "subtitle")
            self.results_text.insert(tk.END, f"{result['treatment']}\n\n", "normal")
            
            # Product Recommendations
            if result['product_recommendations']:
                self.results_text.insert(tk.END, "Recommended Products:\n", "subtitle")
                for product in result['product_recommendations']:
                    # Color-code by product type
                    product_tag = "confidence_high" if product['type'] == 'Organic' else \
                                 "confidence_low" if product['type'] == 'Chemical' else \
                                 "confidence_medium"
                    
                    self.results_text.insert(tk.END, f"• {product['name']} ", "bullet")
                    self.results_text.insert(tk.END, f"({product['type']})\n", product_tag)
                    self.results_text.insert(tk.END, f"  {product['description']}\n", "normal")
                self.results_text.insert(tk.END, "\n", "normal")
            
            # Matching symptoms with severity
            self.results_text.insert(tk.END, "Matching Symptoms:\n", "subtitle")
            for symptom in result['matching_symptoms']:
                severity = self.severity_vars[symptom].get()
                # Convert severity to int if it's a string
                if isinstance(severity, str):
                    try:
                        severity = int(severity)
                    except (ValueError, TypeError):
                        severity = 3  # Default to medium severity
                
                # Ensure severity is within valid range (1-5)
                if severity < 1 or severity > 5:
                    severity = 3  # Default to medium severity
                        
                severity_text = SYMPTOM_SEVERITY[severity]
                severity_tag = "confidence_low" if severity <= 2 else \
                              "confidence_medium" if severity <= 4 else \
                              "confidence_high"
                
                self.results_text.insert(tk.END, f"• {SYMPTOM_NAMES[symptom]}\n", "bullet")
                self.results_text.insert(tk.END, f"  Severity: ", "normal")
                self.results_text.insert(tk.END, f"{severity}/5 - {severity_text}\n", severity_tag)
            
            # Divider between diseases
            if i < len(results):
                self.results_text.insert(tk.END, "\n", "normal")
                divider_str = "•" + "─" * 48 + "•"
                self.results_text.insert(tk.END, divider_str + "\n\n", "divider")
    
    def update_history_list(self):
        """Update the history listbox with all past diagnoses."""
        self.history_listbox.delete(0, tk.END)
        
        for i, item in enumerate(self.diagnosis_history):
            timestamp = item["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            plant_type = item["plant_type"]
            symptom_count = len(item["symptoms"])
            result_count = len(item["results"])
            
            list_text = f"{timestamp} - {plant_type} ({symptom_count} symptoms, {result_count} results)"
            self.history_listbox.insert(tk.END, list_text)
        
        # Select the most recent entry only if we have any items
        if self.diagnosis_history:
            try:
                last_index = len(self.diagnosis_history) - 1
                self.history_listbox.select_set(last_index)
                # Load history item only if it's actually available
                if last_index >= 0:
                    self.load_history_item()
            except Exception as e:
                print(f"Error selecting history item: {e}")
                # Don't try to load history item if selection fails
    
    def load_history_item(self, event=None):
        """Load a selected history item."""
        selection = self.history_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        history_item = self.diagnosis_history[index]
        
        # Clear existing content
        self.history_text.delete("1.0", tk.END)
        
        # Get access to the underlying text widget
        text_widget = self.history_text._textbox
        
        # Configure text tags
        text_widget.tag_configure("title", font=(DEFAULT_FONT, 18, "bold"))
        text_widget.tag_configure("subtitle", font=(DEFAULT_FONT, 14, "bold"))
        text_widget.tag_configure("normal", font=(DEFAULT_FONT, 12))
        text_widget.tag_configure("italic", font=(DEFAULT_FONT, 12, "italic"))
        text_widget.tag_configure("bullet", font=(DEFAULT_FONT, 12, "bold"))
        text_widget.tag_configure("link", font=(DEFAULT_FONT, 12, "underline"), foreground=UI_COLORS['primary'])
        
        # Title with timestamp
        timestamp = history_item["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        self.history_text.insert(tk.END, f"Diagnosis from {timestamp}\n", "title")
        self.history_text.insert(tk.END, f"Plant Type: {history_item['plant_type']}\n\n", "subtitle")
        
        # Symptoms
        self.history_text.insert(tk.END, "Symptoms:\n", "subtitle")
        for symptom in history_item["symptoms"]:
            severity = history_item["severity"][symptom]
            self.history_text.insert(tk.END, f"• {SYMPTOM_NAMES[symptom]} (Severity: {severity}/5)\n", "normal")
        
        # Environmental factors if present
        if history_item.get("environmental_factors"):
            self.history_text.insert(tk.END, "\nEnvironmental Factors:\n", "subtitle")
            for factor, value in history_item["environmental_factors"].items():
                display_factor = factor.replace('_', ' ').title()
                display_value = value.replace('_', ' ').title()
                self.history_text.insert(tk.END, f"• {display_factor}: {display_value}\n", "normal")
        
        # Results summary
        self.history_text.insert(tk.END, "\nResults:\n", "subtitle")
        for result in history_item["results"]:
            self.history_text.insert(tk.END, f"• {result['name']} ({result['confidence']}%)\n", "normal")
        
        # Clear buttons frame first
        for widget in self.history_buttons_frame.winfo_children():
            widget.destroy()
        
        # Add buttons to the buttons frame
        apply_button = ctk.CTkButton(
            self.history_buttons_frame,
            text="Apply This Selection",
            command=lambda: self.apply_history_selection(history_item),
            fg_color=UI_COLORS['primary'],
            hover_color=UI_COLORS['primary_dark'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        apply_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        export_button = ctk.CTkButton(
            self.history_buttons_frame,
            text="Export",
            command=lambda: self.show_export_menu(history_item),
            fg_color=UI_COLORS['secondary'],
            hover_color=UI_COLORS['secondary_dark'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        export_button.pack(side=tk.LEFT, padx=10, pady=5)
    
    def apply_history_selection(self, history_item):
        """Apply a history item's symptom selection and severity to the current view."""
        # Clear current selection
        self.clear_selection()
        
        # Set plant type
        self.current_plant_type.set(history_item["plant_type"])
        self.filter_symptoms_by_plant()
        
        # Set symptoms and severity
        for symptom in history_item["symptoms"]:
            if symptom in self.symptom_vars:
                self.symptom_vars[symptom].set(True)
                if symptom in history_item["severity"]:
                    self.severity_vars[symptom].set(history_item["severity"][symptom])
        
        # Set environmental factors if present
        if history_item.get("environmental_factors") and self.env_expanded.get():
            for factor, value in history_item["environmental_factors"].items():
                if factor in self.environmental_factors:
                    self.environmental_factors[factor].set(value)
        
        # Show a notification
        self.show_snackbar("Applied history selection")
        
        # Diagnose with the loaded selection
        self.diagnose()
    
    def clear_selection(self):
        """Clear all selected symptoms and reset severity values."""
        # Clear symptoms
        for var in self.symptom_vars.values():
            var.set(False)
        
        # Reset severity values
        for var in self.severity_vars.values():
            var.set(3)  # Reset to medium severity
        
        # Reset environmental factors
        for var in self.environmental_factors.values():
            var.set("moderate")
        
        # Clear results
        self.results_text.delete("1.0", tk.END)
        self.current_results = []
        
        # Update UI
        self.update_symptom_display()
        
        # Update status
        self.status_label.configure(text=f"{APP_NAME} v{APP_VERSION} | Ready")
    
    def show_export_menu(self, history_item=None):
        """Show export options menu."""
        # Use either the specified history item or current results
        results_to_export = history_item["results"] if history_item else self.current_results
        
        if not results_to_export:
            messagebox.showinfo("No Results", "Please run a diagnosis first.")
            return
        
        # Create popup menu
        export_menu = ctk.CTkToplevel(self.root)
        export_menu.title("Export Options")
        export_menu.geometry("300x200")
        export_menu.transient(self.root)
        export_menu.grab_set()
        
        # Make window modal
        export_menu.focus_set()
        export_menu.resizable(False, False)
        
        # Export options frame
        options_frame = ctk.CTkFrame(export_menu)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            options_frame,
            text="Export Results",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=16, weight="bold")
        )
        title_label.pack(pady=(0, 15))
        
        # Text option
        text_button = ctk.CTkButton(
            options_frame,
            text="Export as Text File",
            command=lambda: self.export_as_text(history_item),
            fg_color=UI_COLORS['primary'],
            hover_color=UI_COLORS['primary_dark'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        text_button.pack(fill=tk.X, pady=5)
        
        # PDF option if available
        if REPORTLAB_AVAILABLE:
            pdf_button = ctk.CTkButton(
                options_frame,
                text="Export as PDF",
                command=lambda: self.export_as_pdf(history_item),
                fg_color=UI_COLORS['primary'],
                hover_color=UI_COLORS['primary_dark'],
                font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
            )
            pdf_button.pack(fill=tk.X, pady=5)
        else:
            pdf_note = ctk.CTkLabel(
                options_frame,
                text="Install ReportLab package for PDF export",
                font=ctk.CTkFont(family=DEFAULT_FONT, size=11, slant="italic"),
                text_color=UI_COLORS['text_secondary']
            )
            pdf_note.pack(pady=5)
        
        # JSON option
        json_button = ctk.CTkButton(
            options_frame,
            text="Export as JSON",
            command=lambda: self.export_as_json(history_item),
            fg_color=UI_COLORS['primary'],
            hover_color=UI_COLORS['primary_dark'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        json_button.pack(fill=tk.X, pady=5)
        
        # Close button
        close_button = ctk.CTkButton(
            options_frame,
            text="Cancel",
            command=export_menu.destroy,
            fg_color=UI_COLORS['text_secondary'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        close_button.pack(fill=tk.X, pady=(10, 0))
    
    def export_as_text(self, history_item=None):
        """Export diagnosis results as a text file."""
        # Use either the specified history item or current results
        if history_item:
            results = history_item["results"]
            symptoms = history_item["symptoms"]
            severity = history_item["severity"]
            plant_type = history_item["plant_type"]
            env_factors = history_item.get("environmental_factors")
            timestamp = history_item["timestamp"]
        else:
            results = self.current_results
            symptoms = [s for s, v in self.symptom_vars.items() if v.get()]
            severity = {s: self.severity_vars[s].get() for s in symptoms}
            plant_type = self.current_plant_type.get()
            env_factors = {k: v.get() for k, v in self.environmental_factors.items()} if self.env_expanded.get() else None
            timestamp = datetime.datetime.now()
        
        if not results:
            messagebox.showinfo("No Results", "No diagnosis results to export.")
            return
        
        # Ensure we have valid severity values (integers 1-5)
        for s in severity:
            if isinstance(severity[s], str):
                try:
                    severity[s] = int(severity[s])
                except (ValueError, TypeError):
                    severity[s] = 3  # Default to medium severity
            # Ensure value is in valid range
            if severity[s] < 1 or severity[s] > 5:
                severity[s] = 3  # Default to medium severity
        
        filename = filedialog.asksaveasfilename(
            initialdir=self.saved_data_dir,
            title="Export Results as Text",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
            defaultextension=".txt"
        )
        
        if not filename:  # User cancelled
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"{APP_NAME} - DIAGNOSIS RESULTS\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Date: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Plant type
                f.write(f"Plant Type: {plant_type}\n\n")
                
                # Environmental factors if available
                if env_factors:
                    f.write("Environmental Factors:\n")
                    for factor, value in env_factors.items():
                        display_factor = factor.replace('_', ' ').title()
                        display_value = value.replace('_', ' ').title()
                        f.write(f"- {display_factor}: {display_value}\n")
                    f.write("\n")
                
                # Observed symptoms
                f.write("Observed Symptoms:\n")
                for symptom in symptoms:
                    symptom_severity = severity.get(symptom, 3)
                    # Ensure severity is an integer
                    if isinstance(symptom_severity, str):
                        try:
                            symptom_severity = int(symptom_severity)
                        except (ValueError, TypeError):
                            symptom_severity = 3
                    # Ensure severity is in valid range
                    if symptom_severity < 1 or symptom_severity > 5:
                        symptom_severity = 3
                    
                    severity_text = SYMPTOM_SEVERITY[symptom_severity]
                    f.write(f"- {SYMPTOM_NAMES[symptom]} (Severity: {symptom_severity}/5 - {severity_text})\n")
                f.write("\n")
                
                # Write diagnosis results
                f.write(f"Found {len(results)} potential diagnoses:\n\n")
                
                for i, result in enumerate(results, 1):
                    f.write(f"{i}. {result['name']}\n")
                    f.write(f"   Confidence: {result['confidence']}%\n\n")
                    
                    f.write(f"   Description:\n   {result['description']}\n\n")
                    
                    # Severity impact if available
                    if 'severity_impact' in result and result['severity_impact']:
                        f.write(f"   Severity Impact:\n")
                        for level, impact in result['severity_impact'].items():
                            f.write(f"   - {level.title()}: {impact}\n")
                        f.write("\n")
                    
                    f.write(f"   Treatment:\n   {result['treatment']}\n\n")
                    
                    if result['product_recommendations']:
                        f.write(f"   Recommended Products:\n")
                        for product in result['product_recommendations']:
                            f.write(f"   - {product['name']} ({product['type']})\n")
                            f.write(f"     {product['description']}\n")
                        f.write("\n")
                    
                    f.write(f"   Matching Symptoms:\n")
                    for symptom in result['matching_symptoms']:
                        symptom_severity = severity.get(symptom, 3)
                        # Ensure severity is an integer
                        if isinstance(symptom_severity, str):
                            try:
                                symptom_severity = int(symptom_severity)
                            except (ValueError, TypeError):
                                symptom_severity = 3
                        # Ensure severity is in valid range
                        if symptom_severity < 1 or symptom_severity > 5:
                            symptom_severity = 3
                            
                        severity_text = SYMPTOM_SEVERITY[symptom_severity]
                        f.write(f"   - {SYMPTOM_NAMES[symptom]} (Severity: {symptom_severity}/5 - {severity_text})\n")
                    
                    if i < len(results):
                        f.write("\n" + "-" * 50 + "\n\n")
            
            messagebox.showinfo("Success", f"Results exported to {os.path.basename(filename)}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export results: {str(e)}")
    
    def export_as_pdf(self, history_item=None):
        """Export diagnosis results as a PDF file."""
        if not REPORTLAB_AVAILABLE:
            messagebox.showinfo("Feature Not Available", 
                               "PDF export requires the ReportLab library. Please install it with 'pip install reportlab'.")
            return
            
        # Use either the specified history item or current results
        if history_item:
            results = history_item["results"]
            symptoms = history_item["symptoms"]
            severity = history_item["severity"]
            plant_type = history_item["plant_type"]
            env_factors = history_item.get("environmental_factors")
            timestamp = history_item["timestamp"]
        else:
            results = self.current_results
            symptoms = [s for s, v in self.symptom_vars.items() if v.get()]
            severity = {s: self.severity_vars[s].get() for s in symptoms}
            plant_type = self.current_plant_type.get()
            env_factors = {k: v.get() for k, v in self.environmental_factors.items()} if self.env_expanded.get() else None
            timestamp = datetime.datetime.now()
        
        if not results:
            messagebox.showinfo("No Results", "No diagnosis results to export.")
            return
        
        # Ensure we have valid severity values (integers 1-5)
        for s in severity:
            if isinstance(severity[s], str):
                try:
                    severity[s] = int(severity[s])
                except (ValueError, TypeError):
                    severity[s] = 3  # Default to medium severity
            # Ensure value is in valid range
            if severity[s] < 1 or severity[s] > 5:
                severity[s] = 3  # Default to medium severity
        
        filename = filedialog.asksaveasfilename(
            initialdir=self.saved_data_dir,
            title="Export Results as PDF",
            filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")),
            defaultextension=".pdf"
        )
        
        if not filename:  # User cancelled
            return
        
        try:
            # Create document
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []
            
            # Add custom styles
            styles.add(ParagraphStyle(
                name='GreenHeader',
                parent=styles['Heading2'],
                textColor=colors.HexColor(UI_COLORS['primary'].replace('#', '#'))
            ))
            
            styles.add(ParagraphStyle(
                name='SectionHeader',
                parent=styles['Heading3'],
                textColor=colors.HexColor(UI_COLORS['primary_dark'].replace('#', '#'))
            ))
            
            # Title and logo
            title_text = f"{APP_NAME} - Diagnosis Results"
            title = Paragraph(title_text, styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 12))
            
            # Try to add logo if available
            try:
                logo_path = os.path.join(ASSETS_DIR, "plant_logo.png")
                if os.path.exists(logo_path):
                    img = ReportLabImage(logo_path, width=1*inch, height=1*inch)
                    elements.append(img)
                    elements.append(Spacer(1, 12))
            except:
                pass  # Skip if logo can't be added
            
            # Date and plant type
            date_str = f"Date: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
            elements.append(Paragraph(date_str, styles['Normal']))
            elements.append(Spacer(1, 6))
            
            plant_str = f"Plant Type: {plant_type}"
            elements.append(Paragraph(plant_str, styles['Normal']))
            elements.append(Spacer(1, 12))
            
            # Environmental factors if available
            if env_factors:
                elements.append(Paragraph("Environmental Factors:", styles['SectionHeader']))
                env_items = []
                for factor, value in env_factors.items():
                    display_factor = factor.replace('_', ' ').title()
                    display_value = value.replace('_', ' ').title()
                    env_items.append(ListItem(Paragraph(f"{display_factor}: {display_value}", styles['Normal'])))
                if env_items:
                    elements.append(ListFlowable(env_items, bulletType='bullet', start=None))
            elements.append(Spacer(1, 12))
            
            # Observed symptoms
            elements.append(Paragraph("Observed Symptoms:", styles['SectionHeader']))
            symptom_items = []
            for symptom in symptoms:
                symptom_severity = severity.get(symptom, 3)
                # Ensure severity is an integer
                if isinstance(symptom_severity, str):
                    try:
                        symptom_severity = int(symptom_severity)
                    except (ValueError, TypeError):
                        symptom_severity = 3
                # Ensure severity is in valid range
                if symptom_severity < 1 or symptom_severity > 5:
                    symptom_severity = 3
                    
                severity_text = SYMPTOM_SEVERITY[symptom_severity]
                symptom_text = f"{SYMPTOM_NAMES[symptom]} (Severity: {symptom_severity}/5 - {severity_text})"
                symptom_items.append(ListItem(Paragraph(symptom_text, styles['Normal'])))
            if symptom_items:
                elements.append(ListFlowable(symptom_items, bulletType='bullet', start=None))
            elements.append(Spacer(1, 12))
            
            # Diagnoses header
            diagnoses_header = f"Found {len(results)} potential diagnoses:"
            elements.append(Paragraph(diagnoses_header, styles['GreenHeader']))
            elements.append(Spacer(1, 6))
            
            # Each diagnosis
            for i, result in enumerate(results, 1):
                # Create colored style for confidence
                confidence = result['confidence']
                confidence_color = colors.green if confidence >= 75 else \
                                  colors.orange if confidence >= 50 else \
                                  colors.red
                
                confidence_style = ParagraphStyle(
                    name=f'Confidence{i}',
                    parent=styles['Normal'],
                    textColor=confidence_color
                )
                
                # Disease name and confidence
                disease_name = f"{i}. {result['name']}"
                elements.append(Paragraph(disease_name, styles['GreenHeader']))
                elements.append(Paragraph(f"Confidence: {confidence}%", confidence_style))
                elements.append(Spacer(1, 6))
                
                # Description
                elements.append(Paragraph("Description:", styles['SectionHeader']))
                elements.append(Paragraph(result['description'], styles['Normal']))
                elements.append(Spacer(1, 6))
                
                # Severity impact if available
                if 'severity_impact' in result and result['severity_impact']:
                    elements.append(Paragraph("Severity Impact:", styles['SectionHeader']))
                    impact_items = []
                    for level, impact in result['severity_impact'].items():
                        level_text = f"{level.title()}: {impact}"
                        impact_items.append(ListItem(Paragraph(level_text, styles['Normal'])))
                    if impact_items:
                        elements.append(ListFlowable(impact_items, bulletType='bullet', start=None))
                elements.append(Spacer(1, 6))
                
                # Treatment
                elements.append(Paragraph("Treatment:", styles['SectionHeader']))
                elements.append(Paragraph(result['treatment'], styles['Normal']))
                elements.append(Spacer(1, 6))
                
                # Product Recommendations
                if result['product_recommendations']:
                    elements.append(Paragraph("Recommended Products:", styles['SectionHeader']))
                    product_items = []
                    for product in result['product_recommendations']:
                        product_text = f"{product['name']} ({product['type']})"
                        desc_text = f"{product['description']}"
                        
                        product_items.append(ListItem(Paragraph(product_text, styles['Normal'])))
                        product_items.append(ListItem(Paragraph(desc_text, styles['Normal']), leftIndent=20))
                    
                    if product_items:
                        elements.append(ListFlowable(product_items, bulletType='bullet', start=None))
                    elements.append(Spacer(1, 6))
                
                # Matching symptoms
                elements.append(Paragraph("Matching Symptoms:", styles['SectionHeader']))
                matching_items = []
                for symptom in result['matching_symptoms']:
                    symptom_severity = severity.get(symptom, 3)
                    # Ensure severity is an integer
                    if isinstance(symptom_severity, str):
                        try:
                            symptom_severity = int(symptom_severity)
                        except (ValueError, TypeError):
                            symptom_severity = 3
                    # Ensure severity is in valid range
                    if symptom_severity < 1 or symptom_severity > 5:
                        symptom_severity = 3
                        
                    severity_text = SYMPTOM_SEVERITY[symptom_severity]
                    symptom_text = f"{SYMPTOM_NAMES[symptom]} (Severity: {symptom_severity}/5 - {severity_text})"
                    matching_items.append(ListItem(Paragraph(symptom_text, styles['Normal'])))
                
                if matching_items:
                    elements.append(ListFlowable(matching_items, bulletType='bullet', start=None))
                
                # Separator between diseases
                if i < len(results):
                    elements.append(Spacer(1, 12))
                    elements.append(Paragraph("-" * 50, styles['Normal']))
                    elements.append(Spacer(1, 12))
            
            # Build PDF
            doc.build(elements)
            messagebox.showinfo("Success", f"Results exported to {os.path.basename(filename)}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")
    
    def export_as_json(self, history_item=None):
        """Export diagnosis results as a JSON file."""
        # Use either the specified history item or current results
        if history_item:
            export_data = history_item.copy()
            # Convert datetime to string
            export_data["timestamp"] = export_data["timestamp"].strftime('%Y-%m-%d %H:%M:%S')
        else:
            if not self.current_results:
                messagebox.showinfo("No Results", "No diagnosis results to export.")
                return
            
            # Prepare data
            export_data = {
                "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "plant_type": self.current_plant_type.get(),
                "symptoms": [s for s, v in self.symptom_vars.items() if v.get()],
                "severity": {s: self.severity_vars[s].get() for s in [s for s, v in self.symptom_vars.items() if v.get()]},
                "results": self.current_results
            }
            
            # Add environmental factors if available
            if self.env_expanded.get():
                export_data["environmental_factors"] = {k: v.get() for k, v in self.environmental_factors.items()}
        
        filename = filedialog.asksaveasfilename(
            initialdir=self.saved_data_dir,
            title="Export Results as JSON",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
            defaultextension=".json"
        )
        
        if not filename:  # User cancelled
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            messagebox.showinfo("Success", f"Results exported to {os.path.basename(filename)}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export JSON: {str(e)}")
    
    def save_symptom_selection(self):
        """Save the current symptom selection to a file."""
        # Get selected symptoms
        selected_symptoms = [symptom for symptom, var in self.symptom_vars.items() if var.get()]
        
        if not selected_symptoms:
            messagebox.showinfo("No Selection", "Please select at least one symptom to save.")
            return
        
        # Prepare data
        data = {
            "selected_symptoms": selected_symptoms,
            "symptom_severity": {s: self.severity_vars[s].get() for s in selected_symptoms},
            "plant_type": self.current_plant_type.get(),
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add environmental factors if expanded
        if self.env_expanded.get():
            data["environmental_factors"] = {k: v.get() for k, v in self.environmental_factors.items()}
        
        # Ask for filename
        filename = filedialog.asksaveasfilename(
            initialdir=self.saved_data_dir,
            title="Save Symptom Selection",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
            defaultextension=".json"
        )
        
        if not filename:  # User cancelled
            return
        
        # Save to file
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Success", f"Symptom selection saved to {os.path.basename(filename)}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def load_symptom_selection(self):
        """Load a symptom selection from a file."""
        # Ask for file
        filename = filedialog.askopenfilename(
            initialdir=self.saved_data_dir,
            title="Load Symptom Selection",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        
        if not filename:  # User cancelled
            return
        
        # Load from file
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Clear current selection
            self.clear_selection()
            
            # Set plant type if available
            if "plant_type" in data and data["plant_type"] in self.plant_types:
                self.current_plant_type.set(data["plant_type"])
                self.filter_symptoms_by_plant()
            
            # Set loaded symptoms
            for symptom in data.get("selected_symptoms", []):
                if symptom in self.symptom_vars:
                    self.symptom_vars[symptom].set(True)
            
            # Set severity if available
            for symptom, severity in data.get("symptom_severity", {}).items():
                if symptom in self.severity_vars:
                    self.severity_vars[symptom].set(severity)
            
            # Set environmental factors if available
            if "environmental_factors" in data:
                for factor, value in data["environmental_factors"].items():
                    if factor in self.environmental_factors:
                        self.environmental_factors[factor].set(value)
                
                # Show environmental factors panel
                if not self.env_expanded.get():
                    self.toggle_env_factors()
            
            messagebox.showinfo("Success", f"Symptom selection loaded from {os.path.basename(filename)}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def show_help(self):
        """Show help information."""
        help_window = ctk.CTkToplevel(self.root)
        help_window.title("Help")
        help_window.geometry("600x500")
        help_window.transient(self.root)
        
        # Help content
        help_frame = ctk.CTkScrollableFrame(help_window)
        help_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            help_frame,
            text="Plant Disease Expert System - Help",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=16, weight="bold")
        )
        title_label.pack(pady=(0, 15))
        
        # Help sections
        help_sections = [
            ("Getting Started", [
                "1. Select a plant type from the dropdown menu",
                "2. Check the symptoms you observe in your plant",
                "3. Adjust the severity level for each symptom",
                "4. (Optional) Specify environmental conditions",
                "5. Click 'Diagnose' to get results"
            ]),
            ("Understanding Results", [
                "The system will display potential diseases with confidence scores",
                "Higher confidence scores indicate better matches",
                "Each result includes description, treatment, and product recommendations",
                "Severity impact shows how the disease progresses at different severity levels"
            ]),
            ("Advanced Features", [
                "Save and load your symptom selections for future reference",
                "Export results in multiple formats (Text, PDF, JSON)",
                "View diagnosis history to compare different sessions",
                "Access the plant guide for plant-specific information"
            ]),
            ("Tips", [
                "Be as specific as possible when selecting symptoms",
                "Take photos of your plant to reference while using the system",
                "Consider environmental factors for more accurate diagnosis",
                "Export your results to share with plant specialists"
            ])
        ]
        
        for title, items in help_sections:
            section_label = ctk.CTkLabel(
                help_frame,
                text=title,
                font=ctk.CTkFont(family=DEFAULT_FONT, size=14, weight="bold"),
                anchor="w"
            )
            section_label.pack(fill=tk.X, pady=(10, 5))
            
            for item in items:
                item_label = ctk.CTkLabel(
                    help_frame,
                    text=item,
                    font=ctk.CTkFont(family=DEFAULT_FONT, size=12),
                    wraplength=550,
                    anchor="w",
                    justify="left"
                )
                item_label.pack(fill=tk.X, padx=20, pady=2)
        
        # Close button
        close_button = ctk.CTkButton(
            help_frame,
            text="Close",
            command=help_window.destroy,
            fg_color=UI_COLORS['primary'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        close_button.pack(pady=15)
    
    def show_about(self):
        """Show about information."""
        about_window = ctk.CTkToplevel(self.root)
        about_window.title("About")
        about_window.geometry("400x400")
        about_window.transient(self.root)
        
        # About content
        about_frame = ctk.CTkFrame(about_window)
        about_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Logo
        try:
            logo_path = os.path.join(ASSETS_DIR, "plant_logo.png")
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path).resize((100, 100))
                logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = ctk.CTkLabel(about_frame, image=logo_photo, text="")
                logo_label.image = logo_photo
                logo_label.pack(pady=10)
            else:
                # Emoji as fallback
                logo_label = ctk.CTkLabel(about_frame, text="🌿", font=ctk.CTkFont(size=48))
                logo_label.pack(pady=10)
        except Exception:
            # Fallback if image loading fails
            logo_label = ctk.CTkLabel(about_frame, text="🌿", font=ctk.CTkFont(size=48))
            logo_label.pack(pady=10)
        
        # App info
        app_label = ctk.CTkLabel(
            about_frame,
            text=f"{APP_NAME}",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=16, weight="bold")
        )
        app_label.pack(pady=(0, 5))
        
        version_label = ctk.CTkLabel(
            about_frame,
            text=f"Version {APP_VERSION}",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        version_label.pack(pady=(0, 10))
                
                # Description
        description = (
            "An expert system for diagnosing plant diseases based on observed symptoms. "
            "This application uses rule-based reasoning to identify potential diseases "
            "and provide treatment recommendations."
        )
        
        desc_label = ctk.CTkLabel(
            about_frame,
            text=description,
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12),
            wraplength=350,
            justify="center"
        )
        desc_label.pack(pady=10)
        
        # Credits
        credits_label = ctk.CTkLabel(
            about_frame,
            text="Developed as an expert systems project",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=11, slant="italic"),
            text_color=UI_COLORS['text_secondary']
        )
        credits_label.pack(pady=(20, 5))
        
        # Close button
        close_button = ctk.CTkButton(
            about_frame,
            text="Close",
            command=about_window.destroy,
            fg_color=UI_COLORS['primary'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        close_button.pack(pady=15)

    def adjust_color_opacity(self, hex_color, opacity):
        """Convert hex color to RGBA with opacity."""
        # Remove # if present
        hex_color = hex_color.lstrip('#')
        # Convert hex to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        # Calculate the tint (mix with white)
        r = int(r + (255 - r) * (1 - opacity))
        g = int(g + (255 - g) * (1 - opacity))
        b = int(b + (255 - b) * (1 - opacity))
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"

    def highlight_text(self, text, tag, bg_color):
        """Insert text with a highlight background."""
        highlight_tag = f"{tag}_highlight"
        text_widget = self.results_text._textbox
        
        if highlight_tag not in text_widget.tag_names():
            # Get the font from existing tag
            font = text_widget.tag_cget(tag, "font")
            fg = text_widget.tag_cget(tag, "foreground")
            
            text_widget.tag_configure(
                highlight_tag, 
                font=font,
                foreground=fg if fg else UI_COLORS['text_primary'],
                background=bg_color
            )
        
        self.results_text.insert(tk.END, text, highlight_tag)

    def apply_scaling(self, size):
        """Apply scaling factor to a size value."""
        if SCALING_ENABLED:
            return int(size * DEFAULT_SCALING_FACTOR)
        return size

    def update_scaling_factor(self):
        """Update scaling factor based on window size."""
        global DEFAULT_SCALING_FACTOR
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Adjust scaling factor based on window size
        if window_width < 800 or window_height < 600:
            DEFAULT_SCALING_FACTOR = 0.8
        elif window_width > 1600 or window_height > 1000:
            DEFAULT_SCALING_FACTOR = 1.2
        else:
            DEFAULT_SCALING_FACTOR = 1.0
        
        # Update UI elements that need to be scaled
        self.refresh_ui()

    def refresh_ui(self):
        """Refresh UI elements when scaling changes."""
        # Update font sizes
        self.update_font_sizes()
        # Reapply padding
        self.apply_padding()
        # Refresh symptom display
        self.update_symptom_display()

    def update_font_sizes(self):
        """Update font sizes based on scaling factor."""
        # Update text tags in results display
        if hasattr(self, 'results_text'):
            # Define base font sizes
            base_sizes = {
                "title": 18,
                "subtitle": 14,
                "confidence": 13,
                "normal": 12,
                "bullet": 12,
                "italic": 12,
                "divider": 12
            }
            
            # Access the underlying tkinter Text widget
            text_widget = self.results_text._textbox
            
            # Apply scaling to each font
            for tag, base_size in base_sizes.items():
                scaled_size = self.apply_scaling(base_size)
                # Update tags that exist
                if tag == "title":
                    text_widget.tag_configure("title", font=(DEFAULT_FONT, scaled_size, "bold"))
                elif tag == "subtitle":
                    text_widget.tag_configure("subtitle", font=(DEFAULT_FONT, scaled_size, "bold"))
                elif tag == "confidence":
                    text_widget.tag_configure("confidence_high", font=(DEFAULT_FONT, scaled_size, "bold"), foreground=UI_COLORS['success'])
                    text_widget.tag_configure("confidence_medium", font=(DEFAULT_FONT, scaled_size, "bold"), foreground=UI_COLORS['warning'])
                    text_widget.tag_configure("confidence_low", font=(DEFAULT_FONT, scaled_size, "bold"), foreground=UI_COLORS['error'])
                elif tag == "normal":
                    text_widget.tag_configure("normal", font=(DEFAULT_FONT, scaled_size))
                elif tag == "bullet":
                    text_widget.tag_configure("bullet", font=(DEFAULT_FONT, scaled_size, "bold"))
                elif tag == "italic":
                    text_widget.tag_configure("italic", font=(DEFAULT_FONT, scaled_size, "italic"))
                elif tag == "divider":
                    text_widget.tag_configure("divider", font=(DEFAULT_FONT, scaled_size), foreground=UI_COLORS['text_secondary'])

    def apply_padding(self):
        """Apply appropriate padding based on scaling factor."""
        # Can be used to adjust padding in different widgets based on scale
        pass

    def on_window_resize(self, event):
        """Handle window resize event to update UI scaling."""
        # Only respond to root window resizing
        if event.widget == self.root:
            # Avoid responding to minor size changes
            if (hasattr(self, 'last_width') and hasattr(self, 'last_height') and
                abs(self.last_width - self.root.winfo_width()) < 50 and
                abs(self.last_height - self.root.winfo_height()) < 50):
                return
            
            # Update last known dimensions
            self.last_width = self.root.winfo_width()
            self.last_height = self.root.winfo_height()
            
            # Update scaling and refresh UI
            self.update_scaling_factor()

    def filter_symptoms_by_plant(self, plant_type=None):
        """Filter symptoms based on selected plant type."""
        # Update search to apply plant-based filtering
        self.search_symptoms()

    def search_symptoms(self):
        """Filter symptoms based on search query using debounce for better performance."""
        # Cancel any pending search update
        if self._search_after_id:
            self.root.after_cancel(self._search_after_id)
            self._search_after_id = None
            
        # Schedule a new search with delay (debounce)
        self._search_after_id = self.root.after(
            self._debounce_delay, 
            lambda: self._perform_search()
        )
    
    def _perform_search(self):
        """Actual search implementation, called after debounce delay."""
        self._search_after_id = None
        
        search_query = self.search_var.get().strip().lower()
        plant_type = self.current_plant_type.get()
        
        # Get symptoms for current plant type
        if plant_type == "All Plants":
            plant_symptoms = ALL_SYMPTOMS
        else:
            # Use cached plant symptoms if available
            if hasattr(self, '_cached_plant_symptoms') and plant_type in self._cached_plant_symptoms:
                plant_symptoms = self._cached_plant_symptoms[plant_type]
            else:
                # Filter symptoms based on plant type from knowledge base
                plant_diseases = []
                for disease, data in self.engine.knowledge_base.items():
                    if 'plant_types' in data and plant_type in data['plant_types']:
                        plant_diseases.append(disease)
                
                # Get all symptoms for these diseases
                plant_symptoms = []
                for disease in plant_diseases:
                    plant_symptoms.extend(self.engine.knowledge_base[disease]['symptoms'])
                
                # Remove duplicates
                plant_symptoms = list(set(plant_symptoms))
                
                # If no plant-specific symptoms found, show all
                if not plant_symptoms:
                    plant_symptoms = ALL_SYMPTOMS
                
                # Cache the result
                if not hasattr(self, '_cached_plant_symptoms'):
                    self._cached_plant_symptoms = {}
                self._cached_plant_symptoms[plant_type] = plant_symptoms
        
        if search_query:
            # Use more efficient search algorithm
            self.visible_symptoms = []
            
            # For very short queries, require exact match to avoid too many results
            if len(search_query) < 3:
                self.visible_symptoms = [
                    s for s in plant_symptoms 
                    if search_query in SYMPTOM_NAMES[s].lower().split()
                ]
            else:
                # For longer queries, use more flexible matching
                for s in plant_symptoms:
                    symptom_name = SYMPTOM_NAMES[s].lower()
                    # Add symptom if search term is found in the symptom name
                    if search_query in symptom_name:
                        self.visible_symptoms.append(s)
                    # Also add symptom if individual words in search query match
                    elif any(word in symptom_name for word in search_query.split() if len(word) > 2):
                        self.visible_symptoms.append(s)
        else:
            # No search query, show all symptoms for current plant type
            self.visible_symptoms = plant_symptoms.copy()
        
        # Remove duplicates that might have been added
        self.visible_symptoms = list(dict.fromkeys(self.visible_symptoms))
        
        # Update the display
        self.update_symptom_display()

    def update_symptom_display(self):
        """Efficiently refreshes the symptoms display with filtered symptoms."""
        # Keep track of displayed symptoms for managing UI elements
        if not hasattr(self, '_displayed_symptoms'):
            self._displayed_symptoms = set()
        
        # Get the list of currently displayed symptom widgets
        existing_widgets = {}
        for widget in self.symptoms_scrollable.winfo_children():
            if hasattr(widget, 'symptom_id'):
                existing_widgets[widget.symptom_id] = widget
        
        # Get the sorted list of symptoms to display
        filtered_symptoms = sorted(self.visible_symptoms, 
                                 key=lambda s: SYMPTOM_NAMES[s].lower())
        
        # Remove header if it exists
        header_widgets = [w for w in self.symptoms_scrollable.winfo_children() 
                         if hasattr(w, 'is_header') and w.is_header]
        for widget in header_widgets:
            widget.destroy()
        
        # Add header with symptoms count and clear all button
        header_frame = ctk.CTkFrame(self.symptoms_scrollable, fg_color="transparent")
        header_frame.is_header = True  # Mark as header
        header_frame.pack(fill="x", padx=10, pady=(5, 0))
        
        symptoms_count = ctk.CTkLabel(
            header_frame,
            text=f"{len(filtered_symptoms)} symptoms",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        symptoms_count.pack(side="left", padx=5)
        
        clear_all_button = ctk.CTkButton(
            header_frame,
            text="Clear All",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12),
            width=80,
            height=25,
            command=self.clear_all_symptoms
        )
        clear_all_button.pack(side="right", padx=5)
        
        # Keep track of symptoms to keep
        symptoms_to_keep = set()
        
        # Add or update symptoms
        for i, symptom in enumerate(filtered_symptoms):
            symptoms_to_keep.add(symptom)
            
            if symptom in existing_widgets:
                # Widget exists, just make sure it's visible and in the right order
                widget = existing_widgets[symptom]
                widget.pack(fill=tk.X, padx=5, pady=5)
            else:
                # Create new widget
                self.create_symptom_row(self.symptoms_scrollable, symptom, i)
        
        # Hide widgets for symptoms that shouldn't be displayed
        for symptom, widget in existing_widgets.items():
            if symptom not in symptoms_to_keep:
                widget.pack_forget()
        
        # Update the displayed symptoms set
        self._displayed_symptoms = symptoms_to_keep

    def clear_all_symptoms(self):
        """Clear all selected symptoms"""
        # Clear the search box
        self.search_var.set("")
        
        # Clear selected symptoms
        for symptom in list(self.symptom_vars.keys()):
            if self.symptom_vars[symptom].get():
                self.symptom_vars[symptom].set(False)
                self.on_symptom_toggle(symptom)
        
        # Reset all severity sliders to 0
        for symptom in list(self.severity_vars.keys()):
            self.severity_vars[symptom].set("0")
            
        self.show_snackbar("All symptoms cleared")

    def create_symptom_row(self, parent, symptom, row_index):
        """Create a row for a symptom with checkbox and severity buttons."""
        # Base frame with improved styling
        symptom_frame = ctk.CTkFrame(parent, fg_color="transparent")
        symptom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Store the symptom id and reference to find it later
        symptom_frame.symptom_id = symptom
        self.symptom_frames[symptom] = symptom_frame
        
        # Create an inner frame with hover effect
        inner_frame = ctk.CTkFrame(symptom_frame, fg_color=UI_COLORS['card_bg'], corner_radius=10, border_width=1, border_color=UI_COLORS['border'])
        inner_frame.pack(fill=tk.X, padx=2, pady=2)
        
        # Simplified hover effect with less overhead
        inner_frame.bind("<Enter>", lambda e, frame=inner_frame: frame.configure(
            fg_color=UI_COLORS['hover'], 
            border_color=UI_COLORS['primary_light']
        ))
        inner_frame.bind("<Leave>", lambda e, frame=inner_frame: frame.configure(
            fg_color=UI_COLORS['card_bg'], 
            border_color=UI_COLORS['border']
        ))
        
        # Top section with checkbox and severity button
        top_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Checkbox with improved styling
        checkbox = ctk.CTkCheckBox(
            top_frame,
            text=SYMPTOM_NAMES[symptom],
            variable=self.symptom_vars[symptom],
            command=lambda s=symptom: self.on_symptom_toggle(s),
            fg_color=UI_COLORS['primary'],
            hover_color=UI_COLORS['primary_dark'],
            border_color=UI_COLORS['border'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=13, weight="bold")
        )
        checkbox.pack(side=tk.LEFT, anchor="w")
        
        # Skip tooltips for performance
        
        # Add a show severity button
        severity_button = ctk.CTkButton(
            top_frame,
            text="⚙️ Symptom Severity",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12),
            width=90,
            height=25,
            fg_color=UI_COLORS['secondary'],
            hover_color=UI_COLORS['secondary_dark'],
            command=lambda s=symptom: self.toggle_severity_view(s)
        )
        severity_button.pack(side=tk.RIGHT, padx=5)
        
        # Severity frame (BELOW instead of RIGHT side)
        severity_frame = ctk.CTkFrame(inner_frame, fg_color="transparent", corner_radius=5)
        symptom_frame.severity_frame = severity_frame  # Store reference for toggling
        
        # Only show severity if symptom is checked
        if self.symptom_vars[symptom].get():
            severity_frame.pack(side=tk.TOP, fill=tk.X, padx=15, pady=10)
        
        # Get current severity value
        current_value = int(self.severity_vars[symptom].get() or 0)
        if current_value == 0:
            current_value = 1  # Set a minimum value of 1 for display
            
        # Define colors for severity levels
        value_color = UI_COLORS['low_severity'] if current_value <= 2 else \
                    UI_COLORS['medium_severity'] if current_value <= 4 else \
                    UI_COLORS['high_severity']
                    
        # Horizontal separator
        separator = ctk.CTkFrame(severity_frame, height=1, fg_color=UI_COLORS['border'])
        separator.pack(fill=tk.X, pady=(0, 10))
        
        # Severity buttons in a clean layout
        buttons_container = ctk.CTkFrame(severity_frame, fg_color="transparent")
        buttons_container.pack(fill=tk.X, padx=5, pady=5)
        
        # Title and current level
        severity_header = ctk.CTkFrame(buttons_container, fg_color="transparent")
        severity_header.pack(fill=tk.X, pady=(0, 10))
        
        level_title = ctk.CTkLabel(
            severity_header,
            text="Severity level:",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12, weight="bold"),
            text_color=UI_COLORS['text_primary']
        )
        level_title.pack(side=tk.LEFT)
        
        current_level_text = SYMPTOM_SEVERITY.get(current_value, "Not specified")
        level_desc = ctk.CTkLabel(
            severity_header,
            text=current_level_text,
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12),
            text_color=value_color
        )
        level_desc.pack(side=tk.RIGHT)
        severity_frame.desc_label = level_desc

        # Severity buttons
        buttons_frame = ctk.CTkFrame(buttons_container, fg_color="transparent")
        buttons_frame.pack(fill=tk.X, pady=5)
        
        # Create simple number buttons
        level_buttons = []
        for i in range(1, 6):
            # Determine if this button is selected
            is_selected = i == current_value
            
            # Get color based on severity level
            button_color = UI_COLORS['low_severity'] if i <= 2 else \
                        UI_COLORS['medium_severity'] if i <= 4 else \
                        UI_COLORS['high_severity']
            
            # Create the button
            level_button = ctk.CTkButton(
                buttons_frame,
                text=str(i),
                width=35,
                height=35,
                corner_radius=5,
                fg_color=button_color if is_selected else "transparent",
                border_width=1,
                border_color=button_color,
                hover_color=self.adjust_color_opacity(button_color, 0.8),
                text_color=UI_COLORS['text_light'] if is_selected else button_color,
                font=ctk.CTkFont(family=DEFAULT_FONT, size=12, weight="bold"),
                command=lambda val=i, s=symptom: self.set_severity_direct(s, val)
            )
            level_button.pack(side=tk.LEFT, expand=True, padx=3)
            level_buttons.append({"button": level_button, "level": i})
        
        # Store buttons for updates
        severity_frame.level_buttons = level_buttons
        
        # Simple update function
        def update_severity_visuals(*args):
            try:
                if not severity_frame.winfo_exists():
                    return
                    
                # Get current severity value
                severity_str = self.severity_vars[symptom].get()
                
                # Convert to integer
                try:
                    severity = int(float(severity_str))
                except (ValueError, TypeError):
                    severity = 0
                
                # Get appropriate color and text
                if severity == 0:
                    severity_text = "Not present"
                    new_color = UI_COLORS['text_secondary']
                else:
                    new_color = UI_COLORS['low_severity'] if severity <= 2 else \
                               UI_COLORS['medium_severity'] if severity <= 4 else \
                               UI_COLORS['high_severity']
                    severity_text = SYMPTOM_SEVERITY.get(severity, "Not specified")
                
                # Update buttons
                for button_data in severity_frame.level_buttons:
                    button = button_data["button"]
                    level = button_data["level"]
                    
                    # Get color for this level
                    level_color = UI_COLORS['low_severity'] if level <= 2 else \
                               UI_COLORS['medium_severity'] if level <= 4 else \
                               UI_COLORS['high_severity']
                    
                    # Is this the current selected level?
                    is_selected = level == severity
                    
                    # Update button appearance
                    button.configure(
                        fg_color=level_color if is_selected else "transparent",
                        text_color=UI_COLORS['text_light'] if is_selected else level_color
                    )
                
                # Update description
                severity_frame.desc_label.configure(text=severity_text, text_color=new_color)
                
            except Exception as e:
                print(f"Error updating severity visuals: {e}")
                try:
                    self.severity_vars[symptom].trace_remove("write", *args)
                except:
                    pass
        
        # Call once to set initial state
        update_severity_visuals()
        
        # Attach trace for updates
        try:
            trace_id = self.severity_vars[symptom].trace("w", update_severity_visuals)
            if not hasattr(self, '_traces'):
                self._traces = {}
            self._traces[symptom] = trace_id
        except Exception as e:
            print(f"Error setting trace: {e}")
        
        return symptom_frame

    def on_symptom_toggle(self, symptom):
        """Handle symptom checkbox toggle with improved efficiency."""
        # Get the direct reference to the symptom frame
        symptom_frame = self.symptom_frames.get(symptom)
        if not symptom_frame or not hasattr(symptom_frame, 'severity_frame'):
            return
        
        # Check if widget still exists
        if not symptom_frame.winfo_exists():
            return
            
        # Get the checked state
        is_checked = self.symptom_vars[symptom].get()
        
        # Show or hide severity frame based on checked state
        try:
            if is_checked:
                # Show severity frame when checked
                if symptom_frame.severity_frame.winfo_exists():
                    symptom_frame.severity_frame.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)
            else:
                # Hide severity frame when unchecked
                if symptom_frame.severity_frame.winfo_exists():
                    symptom_frame.severity_frame.pack_forget()
                    # Reset severity to default
                    self.severity_vars[symptom].set(3)
        except Exception as e:
            # Log error but don't crash
            print(f"Error in on_symptom_toggle: {e}")

    def view_plant_categories(self):
        """Open dialog to view plants by category."""
        category_window = ctk.CTkToplevel(self.root)
        category_window.title("Plant Categories")
        category_window.geometry("500x600")
        category_window.transient(self.root)
        category_window.grab_set()
        
        # Make window modal
        category_window.focus_set()
        category_window.resizable(False, False)
        
        # Create scrollable frame for categories
        category_frame = ctk.CTkScrollableFrame(category_window)
        category_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            category_frame,
            text="Select Plant by Category",
            font=ctk.CTkFont(family=DEFAULT_FONT, size=16, weight="bold")
        )
        title_label.pack(pady=(0, 15))
        
        # List categories and plants
        for category, plants in PLANT_CATEGORIES.items():
            # Category header
            category_header = ctk.CTkFrame(category_frame, fg_color=UI_COLORS['primary'])
            category_header.pack(fill=tk.X, pady=(10, 5))
            
            category_label = ctk.CTkLabel(
                category_header,
                text=category,
                font=ctk.CTkFont(family=DEFAULT_FONT, size=14, weight="bold"),
                text_color=UI_COLORS['text_light']
            )
            category_label.pack(padx=10, pady=5)
            
            # Plants in this category
            plants_frame = ctk.CTkFrame(category_frame, fg_color=UI_COLORS['bg_light'])
            plants_frame.pack(fill=tk.X, pady=(0, 10))
            
            for plant in sorted(plants):
                plant_button = ctk.CTkButton(
                    plants_frame,
                    text=plant,
                    command=lambda p=plant: self.select_plant_from_category(p, category_window),
                    fg_color="transparent",
                    text_color=UI_COLORS['text_primary'],
                    hover_color=UI_COLORS['divider'],
                    anchor="w",
                    height=30
                )
                plant_button.pack(fill=tk.X, padx=5, pady=2)
        
        # Close button
        close_button = ctk.CTkButton(
            category_frame,
            text="Close",
            command=category_window.destroy,
            fg_color=UI_COLORS['text_secondary'],
            font=ctk.CTkFont(family=DEFAULT_FONT, size=12)
        )
        close_button.pack(pady=15)

    def clear_search(self):
        """Clear only the search box without affecting selected symptoms."""
        self.search_var.set("")
        # Update the symptom display to show all symptoms
        self.update_symptom_display()
        self.show_snackbar("Search cleared")

    def update_severity_visuals(self, symptom, severity_value=None):
        """Updates the visual elements based on severity value"""
        try:
            if severity_value is None:
                severity_value = self.severity_vars.get(symptom, tk.StringVar(value="0")).get()
            
            # Convert string to integer (safely)
            try:
                severity_int = int(float(severity_value))
            except (ValueError, TypeError):
                severity_int = 0
            
            # Get the severity row container
            symptom_frame = self.symptom_frames.get(symptom)
            if not symptom_frame:
                return
            
            # Update description label
            severity_desc = self.severity_descriptions.get(severity_int, "Not specified")
            
            # More robust way to find the label
            try:
                # Try to find the desc_label that was stored
                if hasattr(symptom_frame, 'severity_frame') and hasattr(symptom_frame.severity_frame, 'desc_label'):
                    severity_label = symptom_frame.severity_frame.desc_label
                    if hasattr(severity_label, 'configure'):
                        severity_label.configure(text=severity_desc)
            except Exception:
                pass  # Skip if we can't update the label
            
            # Update button colors if applicable
            try:
                if hasattr(symptom_frame, 'severity_frame') and hasattr(symptom_frame.severity_frame, 'level_buttons'):
                    for button_data in symptom_frame.severity_frame.level_buttons:
                        button = button_data["button"]
                        level = button_data["level"]
                        
                        # Get color for this level
                        level_color = self.severity_colors.get(level, "gray80")
                        
                        # Is this the current selected level?
                        is_selected = level == severity_int
                        
                        # Update button appearance
                        button.configure(
                            fg_color=level_color if is_selected else "transparent",
                            text_color=UI_COLORS['text_light'] if is_selected else level_color
                        )
            except Exception:
                pass  # Skip if we can't update buttons
                
        except Exception as e:
            print(f"Error updating severity visuals: {e}")

    def set_severity_direct(self, symptom, value):
        """Sets the severity directly from button clicks"""
        if symptom in self.severity_vars:
            # Convert to integer if needed
            if isinstance(value, str):
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    value = 3  # Default to medium severity
                
            # Set the severity value - store as integer
            self.severity_vars[symptom].set(value)
            
            # Make sure the symptom is checked
            if not self.symptom_vars[symptom].get():
                self.symptom_vars[symptom].set(True)
                self.on_symptom_toggle(symptom)
            
            # Update the visual elements based on severity value
            self.update_severity_visuals(symptom, value)
            
            # Update the severity slider if it exists
            symptom_frame = self.symptom_frames.get(symptom)
            if symptom_frame and hasattr(symptom_frame, 'severity_frame'):
                # Show the severity frame if it's not visible
                if not symptom_frame.severity_frame.winfo_ismapped():
                    symptom_frame.severity_frame.pack(side=tk.TOP, fill=tk.X, padx=15, pady=10)
            
            self.show_snackbar(f"Severity for {SYMPTOM_NAMES.get(symptom, symptom)} set to {value}")

    def toggle_severity_view(self, symptom):
        """Toggle the visibility of severity controls for a symptom"""
        # Find the symptom frame
        symptom_frame = self.symptom_frames.get(symptom)
        if not symptom_frame:
            return
            
        # If symptom isn't selected, select it first
        if not self.symptom_vars[symptom].get():
            self.symptom_vars[symptom].set(True)
            
        # Toggle the severity frame
        if hasattr(symptom_frame, 'severity_frame'):
            severity_frame = symptom_frame.severity_frame
            if severity_frame.winfo_exists():
                if severity_frame.winfo_ismapped():
                    severity_frame.pack_forget()
                else:
                    severity_frame.pack(side=tk.RIGHT, padx=15, pady=10, fill=tk.X)


def main():
    """Run the expert system GUI."""
    try:
        # Check if customtkinter is available
        import customtkinter
        
        # Create root window with customtkinter
        root = customtkinter.CTk()
        app = PlantDiseaseExpertGUI(root)
        root.mainloop()
    except ImportError:
        # If customtkinter is not available, fall back to standard tkinter
        print("\nTrying to continue with standard tkinter instead...")
        root = tk.Tk()
        messagebox.showerror(
            "Missing Dependencies",
            "The customtkinter library is required for the modern UI.\n\n"
            "Please install it with: pip install customtkinter\n\n"
            "The application will continue with a basic UI."
        )
        # Try to create a basic version without customtkinter
        try:
            # Basic version implementation would go here
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Could not initialize the application: {str(e)}")
        finally:
            root.destroy()


if __name__ == "__main__":
    main() 