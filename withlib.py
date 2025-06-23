import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyMamdaniSoilQualityWithLib:
    def __init__(self):
        # Define universe of discourse
        self.ph = ctrl.Antecedent(np.arange(4, 10, 0.1), 'pH')
        self.nutrition = ctrl.Antecedent(np.arange(0, 351, 1), 'nutrition')
        self.heavy_metal = ctrl.Antecedent(np.arange(0, 31, 0.1), 'heavy_metal')
        self.organic_matter = ctrl.Antecedent(np.arange(0, 11, 0.1), 'organic_matter')
        
        # Define output
        self.quality = ctrl.Consequent(np.arange(0, 101, 0.1), 'quality')
        
        # Define membership functions for pH
        self.ph['asam'] = fuzz.trimf(self.ph.universe, [4, 4, 6])
        self.ph['normal'] = fuzz.trimf(self.ph.universe, [5.5, 6.5, 7.5])
        self.ph['basa'] = fuzz.trimf(self.ph.universe, [6.5, 9, 9])
        
        # Define membership functions for nutrition
        self.nutrition['rendah'] = fuzz.trimf(self.nutrition.universe, [0, 0, 150])
        self.nutrition['sedang'] = fuzz.trimf(self.nutrition.universe, [50, 150, 250])
        self.nutrition['tinggi'] = fuzz.trimf(self.nutrition.universe, [150, 350, 350])
        
        # Define membership functions for heavy metal
        self.heavy_metal['rendah'] = fuzz.trimf(self.heavy_metal.universe, [0, 0, 15])
        self.heavy_metal['sedang'] = fuzz.trimf(self.heavy_metal.universe, [5, 15, 25])
        self.heavy_metal['tinggi'] = fuzz.trimf(self.heavy_metal.universe, [15, 30, 30])
        
        # Define membership functions for organic matter
        self.organic_matter['rendah'] = fuzz.trimf(self.organic_matter.universe, [0, 0, 3])
        self.organic_matter['sedang'] = fuzz.trimf(self.organic_matter.universe, [1, 3.5, 6])
        self.organic_matter['tinggi'] = fuzz.trimf(self.organic_matter.universe, [4, 10, 10])
        
        # Define membership functions for quality output
        self.quality['buruk'] = fuzz.trimf(self.quality.universe, [0, 0, 50])
        self.quality['sedang'] = fuzz.trimf(self.quality.universe, [20, 50, 80])
        self.quality['baik'] = fuzz.trimf(self.quality.universe, [50, 100, 100])
        
        # Create fuzzy control system
        self.control_system = self._create_control_system()
        
    def _create_control_system(self):
        """Create fuzzy control system with rules"""
        
        # Rule 1: Jika pH normal dan kandungan nutrisi tinggi dan kandungan logam berat rendah, maka kualitas tanah baik
        rule1 = ctrl.Rule(
            self.ph['normal'] & self.nutrition['tinggi'] & self.heavy_metal['rendah'],
            self.quality['baik']
        )
        
        # Rule 2: Jika pH asam atau basa dan kandungan nutrisi rendah dan kandungan logam berat tinggi, maka kualitas tanah buruk
        rule2 = ctrl.Rule(
            (self.ph['asam'] | self.ph['basa']) & self.nutrition['rendah'] & self.heavy_metal['tinggi'],
            self.quality['buruk']
        )
        
        # Rule 3: Jika pH normal dan kandungan nutrisi sedang dan kandungan logam berat sedang, maka kualitas tanah sedang
        rule3 = ctrl.Rule(
            self.ph['normal'] & self.nutrition['sedang'] & self.heavy_metal['sedang'],
            self.quality['sedang']
        )
        
        # Rule 4: Jika kandungan bahan organik tinggi, maka kualitas tanah baik
        rule4 = ctrl.Rule(
            self.organic_matter['tinggi'],
            self.quality['baik']
        )
        
        # Rule 5: Jika kandungan bahan organik rendah dan kandungan logam berat tinggi, maka kualitas tanah buruk
        rule5 = ctrl.Rule(
            self.organic_matter['rendah'] & self.heavy_metal['tinggi'],
            self.quality['buruk']
        )
        
        # Rule 6: Jika pH normal dan kandungan nutrisi tinggi dan kandungan logam berat sedang, maka kualitas tanah sedang
        rule6 = ctrl.Rule(
            self.ph['normal'] & self.nutrition['tinggi'] & self.heavy_metal['sedang'],
            self.quality['sedang']
        )
        
        # Create control system
        control_system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
        return ctrl.ControlSystemSimulation(control_system)
    
    def evaluate_soil_quality(self, ph, nutrition, heavy_metal, organic_matter):
        """Evaluate soil quality using fuzzy Mamdani system with library"""
        try:
            # Set input values
            self.control_system.input['pH'] = ph
            self.control_system.input['nutrition'] = nutrition
            self.control_system.input['heavy_metal'] = heavy_metal
            self.control_system.input['organic_matter'] = organic_matter
            
            # Compute result
            self.control_system.compute()
            
            # Get output
            quality_score = self.control_system.output['quality']
            
            # Determine quality category
            if quality_score < 40:
                quality_category = "Buruk"
            elif quality_score < 70:
                quality_category = "Sedang"
            else:
                quality_category = "Baik"
            
            return quality_score, quality_category
            
        except Exception as e:
            print(f"Error in fuzzy computation: {e}")
            return 50.0, "Sedang"  # Default values

def main():
    # Create fuzzy system with library
    fuzzy_system = FuzzyMamdaniSoilQualityWithLib()
    
    # Read test cases from CSV file
    try:
        df = pd.read_csv('data.csv')
        print("SISTEM FUZZY MAMDANI DENGAN LIBRARY UNTUK EVALUASI KUALITAS TANAH")
        print("=" * 70)
        print("No | pH | Nutrisi | Logam Berat | Bahan Organik | Skor | Kualitas")
        print("-" * 70)
        
        for index, row in df.iterrows():
            ph = row['pH']
            nutrition = row['Nutrisi']
            heavy_metal = row['Logam_Berat']
            organic_matter = row['Bahan_Organik']
            case_num = row['No']
            
            quality_score, quality_category = fuzzy_system.evaluate_soil_quality(
                ph, nutrition, heavy_metal, organic_matter
            )
            
            print(f"{case_num:2} | {ph:4.1f} | {nutrition:7.0f} | {heavy_metal:11.0f} | {organic_matter:14.0f} | {quality_score:4.1f} | {quality_category}")
        
        print("=" * 70)
        print("\nKeterangan:")
        print("- Skor 0-40: Buruk")
        print("- Skor 40-70: Sedang") 
        print("- Skor 70-100: Baik")
        print("\nMenggunakan library: scikit-fuzzy")
        
    except FileNotFoundError:
        print("Error: File data.csv tidak ditemukan!")
        print("Pastikan file data.csv ada di direktori yang sama dengan withlib.py")
    except Exception as e:
        print(f"Error membaca file CSV: {e}")

if __name__ == "__main__":
    main()
