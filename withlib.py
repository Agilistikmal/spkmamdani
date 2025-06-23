import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='skfuzzy')
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzySoilQuality:
    def __init__(self):
        # Define variables
        self.ph = ctrl.Antecedent(np.arange(4, 10, 0.1), 'pH')
        self.nutrition = ctrl.Antecedent(np.arange(0, 351, 1), 'nutrition')
        self.heavy_metal = ctrl.Antecedent(np.arange(0, 31, 0.1), 'heavy_metal')
        self.organic_matter = ctrl.Antecedent(np.arange(0, 11, 0.1), 'organic_matter')
        self.quality = ctrl.Consequent(np.arange(0, 101, 0.1), 'quality')
        
        # Setup membership functions
        self._setup_membership_functions()
        
        # Create control system
        self.control_system = self._create_rules()
    
    def _setup_membership_functions(self):
        """Setup all membership functions"""
        # pH membership functions
        self.ph['asam'] = fuzz.trimf(self.ph.universe, [4, 4, 6])
        self.ph['normal'] = fuzz.trimf(self.ph.universe, [5.5, 6.5, 7.5])
        self.ph['basa'] = fuzz.trimf(self.ph.universe, [6.5, 9, 9])
        
        # Nutrition membership functions
        self.nutrition['rendah'] = fuzz.trimf(self.nutrition.universe, [0, 0, 150])
        self.nutrition['sedang'] = fuzz.trimf(self.nutrition.universe, [50, 150, 250])
        self.nutrition['tinggi'] = fuzz.trimf(self.nutrition.universe, [150, 350, 350])
        
        # Heavy metal membership functions
        self.heavy_metal['rendah'] = fuzz.trimf(self.heavy_metal.universe, [0, 0, 15])
        self.heavy_metal['sedang'] = fuzz.trimf(self.heavy_metal.universe, [5, 15, 25])
        self.heavy_metal['tinggi'] = fuzz.trimf(self.heavy_metal.universe, [15, 30, 30])
        
        # Organic matter membership functions
        self.organic_matter['rendah'] = fuzz.trimf(self.organic_matter.universe, [0, 0, 3])
        self.organic_matter['sedang'] = fuzz.trimf(self.organic_matter.universe, [1, 3.5, 6])
        self.organic_matter['tinggi'] = fuzz.trimf(self.organic_matter.universe, [4, 10, 10])
        
        # Quality output membership functions
        self.quality['buruk'] = fuzz.trimf(self.quality.universe, [0, 0, 50])
        self.quality['sedang'] = fuzz.trimf(self.quality.universe, [20, 50, 80])
        self.quality['baik'] = fuzz.trimf(self.quality.universe, [50, 100, 100])
    
    def _create_rules(self):
        """Create fuzzy rules"""
        rules = [
            # Rule 1: pH normal + nutrisi tinggi + logam rendah → baik
            ctrl.Rule(self.ph['normal'] & self.nutrition['tinggi'] & self.heavy_metal['rendah'], self.quality['baik']),
            
            # Rule 2: pH asam/basa + nutrisi rendah + logam tinggi → buruk
            ctrl.Rule((self.ph['asam'] | self.ph['basa']) & self.nutrition['rendah'] & self.heavy_metal['tinggi'], self.quality['buruk']),
            
            # Rule 3: pH normal + nutrisi sedang + logam sedang → sedang
            ctrl.Rule(self.ph['normal'] & self.nutrition['sedang'] & self.heavy_metal['sedang'], self.quality['sedang']),
            
            # Rule 4: Bahan organik tinggi → baik
            ctrl.Rule(self.organic_matter['tinggi'], self.quality['baik']),
            
            # Rule 5: Bahan organik rendah + logam tinggi → buruk
            ctrl.Rule(self.organic_matter['rendah'] & self.heavy_metal['tinggi'], self.quality['buruk']),
            
            # Rule 6: pH normal + nutrisi tinggi + logam sedang → sedang
            ctrl.Rule(self.ph['normal'] & self.nutrition['tinggi'] & self.heavy_metal['sedang'], self.quality['sedang'])
        ]
        
        control_system = ctrl.ControlSystem(rules)
        return ctrl.ControlSystemSimulation(control_system)
    
    def evaluate(self, ph, nutrition, heavy_metal, organic_matter):
        """Evaluate soil quality"""
        try:
            # Set inputs
            self.control_system.input['pH'] = ph
            self.control_system.input['nutrition'] = nutrition
            self.control_system.input['heavy_metal'] = heavy_metal
            self.control_system.input['organic_matter'] = organic_matter
            
            # Compute
            self.control_system.compute()
            
            # Get result
            score = self.control_system.output['quality']
            
            # Determine category
            if score < 40:
                category = "Buruk"
            elif score < 70:
                category = "Sedang"
            else:
                category = "Baik"
            
            return score, category
            
        except Exception as e:
            print(f"Error: {e}")
            return 50.0, "Sedang"
    
    def plot_membership_functions(self):
        """Plot membership functions"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Membership Functions - Sistem Fuzzy Mamdani Kualitas Tanah', fontsize=16, fontweight='bold')
        
        # Plot each variable
        variables = [
            (self.ph, 'pH Tanah', 'pH', axes[0, 0]),
            (self.nutrition, 'Kandungan Nutrisi', 'Nutrisi (mg/kg)', axes[0, 1]),
            (self.heavy_metal, 'Kandungan Logam Berat', 'Logam Berat (mg/kg)', axes[0, 2]),
            (self.organic_matter, 'Kandungan Bahan Organik', 'Bahan Organik (%)', axes[1, 0]),
            (self.quality, 'Kualitas Tanah (Output)', 'Skor Kualitas', axes[1, 1])
        ]
        
        for var, title, xlabel, ax in variables:
            var.view(ax=ax)
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel('Membership Degree')
            ax.grid(True)
        
        # Hide unused subplot
        axes[1, 2].set_visible(False)
        
        plt.tight_layout()
        plt.savefig('membership_functions.png', dpi=300, bbox_inches='tight')
        print("✅ Membership functions: membership_functions.png")
        plt.close()
    
    def plot_inference(self, ph, nutrition, heavy_metal, organic_matter):
        """Plot fuzzy inference for given inputs"""
        try:
            # Compute result
            score, category = self.evaluate(ph, nutrition, heavy_metal, organic_matter)
            
            # Create plot
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle(f'Fuzzy Inference - pH:{ph}, Nutrisi:{nutrition}, Logam:{heavy_metal}, Organik:{organic_matter}%', 
                        fontsize=14, fontweight='bold')
            
            # Plot inputs with vertical lines
            inputs = [
                (self.ph, f'pH = {ph}', axes[0, 0]),
                (self.nutrition, f'Nutrisi = {nutrition} mg/kg', axes[0, 1]),
                (self.heavy_metal, f'Logam Berat = {heavy_metal} mg/kg', axes[1, 0]),
                (self.quality, f'Kualitas = {score:.2f}', axes[1, 1])
            ]
            
            for var, title, ax in inputs:
                var.view(ax=ax)
                ax.set_title(title)
                ax.grid(True)
                
                # Add vertical line for input values
                if var == self.quality:
                    ax.axvline(x=score, color='red', linestyle='--', linewidth=2)
                else:
                    value = ph if var == self.ph else nutrition if var == self.nutrition else heavy_metal
                    ax.axvline(x=value, color='red', linestyle='--', linewidth=2)
            
            plt.tight_layout()
            filename = f'inference_ph{ph}_nut{nutrition}_metal{heavy_metal}_org{organic_matter}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Fuzzy inference: {filename}")
            plt.close()
            
        except Exception as e:
            print(f"Error plotting inference: {e}")

def main():
    # Create system
    system = FuzzySoilQuality()
    
    # Show membership functions
    print("📊 Menampilkan Membership Functions...")
    system.plot_membership_functions()
    
    # Read and process data
    try:
        df = pd.read_csv('data.csv')
        print("\n🌱 SISTEM FUZZY MAMDANI - EVALUASI KUALITAS TANAH")
        print("=" * 70)
        print("No | pH | Nutrisi | Logam Berat | Bahan Organik | Skor | Kualitas")
        print("-" * 70)
        
        for index, row in df.iterrows():
            # Get data
            ph, nutrition, heavy_metal, organic_matter = row['pH'], row['Nutrisi'], row['Logam_Berat'], row['Bahan_Organik']
            
            # Evaluate
            score, category = system.evaluate(ph, nutrition, heavy_metal, organic_matter)
            
            # Show inference plot for first case
            if index == 0:
                system.plot_inference(ph, nutrition, heavy_metal, organic_matter)
            
            # Print result
            print(f"{row['No']:2} | {ph:4.1f} | {nutrition:7.0f} | {heavy_metal:11.0f} | {organic_matter:14.0f} | {score:4.1f} | {category}")
        
        print("=" * 70)
        print("\n📋 Keterangan:")
        print("• Skor 0-40: Buruk")
        print("• Skor 40-70: Sedang") 
        print("• Skor 70-100: Baik")
        print("\n🔧 Library: scikit-fuzzy")
        print("📁 Output: membership_functions.png + inference_*.png")
        
    except FileNotFoundError:
        print("❌ Error: data.csv tidak ditemukan!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
