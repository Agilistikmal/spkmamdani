import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import os
from tabulate import tabulate
warnings.filterwarnings('ignore', category=UserWarning, module='skfuzzy')
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzySoilQuality:
    def __init__(self):
        # Definisikan variabel
        self.ph = ctrl.Antecedent(np.arange(4, 10, 0.1), 'pH')
        self.nutrition = ctrl.Antecedent(np.arange(0, 351, 1), 'nutrition')
        self.heavy_metal = ctrl.Antecedent(np.arange(0, 31, 0.1), 'heavy_metal')
        self.organic_matter = ctrl.Antecedent(np.arange(0, 11, 0.1), 'organic_matter')
        self.quality = ctrl.Consequent(np.arange(0, 101, 0.1), 'quality')
        
        # Setup fungsi keanggotaan
        self._setup_membership_functions()
        
        # Buat sistem kontrol
        self.control_system = self._create_rules()
        
        # Buat folder output jika belum ada
        if not os.path.exists('output'):
            os.makedirs('output')
    
    def _setup_membership_functions(self):
        """Setup semua fungsi keanggotaan"""
        # Fungsi keanggotaan pH - DIPERBAIKI sesuai spesifikasi
        # pH Asam: <6.0 (shoulder kiri)
        self.ph['asam'] = fuzz.trapmf(self.ph.universe, [4, 4, 5.5, 6.0])
        # pH Normal: 6.0-7.0 (triangular)  
        self.ph['normal'] = fuzz.trimf(self.ph.universe, [5.5, 6.5, 7.5])
        # pH Basa: >7.0 (shoulder kanan)
        self.ph['basa'] = fuzz.trapmf(self.ph.universe, [6.5, 7.0, 9, 9])
        
        # Fungsi keanggotaan nutrisi
        self.nutrition['rendah'] = fuzz.trimf(self.nutrition.universe, [0, 0, 150])
        self.nutrition['sedang'] = fuzz.trimf(self.nutrition.universe, [50, 150, 250])
        self.nutrition['tinggi'] = fuzz.trimf(self.nutrition.universe, [150, 350, 350])
        
        # Fungsi keanggotaan logam berat
        self.heavy_metal['rendah'] = fuzz.trimf(self.heavy_metal.universe, [0, 0, 15])
        self.heavy_metal['sedang'] = fuzz.trimf(self.heavy_metal.universe, [5, 15, 25])
        self.heavy_metal['tinggi'] = fuzz.trimf(self.heavy_metal.universe, [15, 30, 30])
        
        # Fungsi keanggotaan bahan organik
        self.organic_matter['rendah'] = fuzz.trimf(self.organic_matter.universe, [0, 0, 3])
        self.organic_matter['sedang'] = fuzz.trimf(self.organic_matter.universe, [1, 3.5, 6])
        self.organic_matter['tinggi'] = fuzz.trimf(self.organic_matter.universe, [4, 10, 10])
        
        # Fungsi keanggotaan kualitas output
        self.quality['buruk'] = fuzz.trimf(self.quality.universe, [0, 0, 50])
        self.quality['sedang'] = fuzz.trimf(self.quality.universe, [20, 50, 80])
        self.quality['baik'] = fuzz.trimf(self.quality.universe, [50, 100, 100])
    
    def _create_rules(self):
        """Buat aturan fuzzy"""
        rules = [
            # Aturan 1: pH normal + nutrisi tinggi + logam rendah -> baik
            ctrl.Rule(self.ph['normal'] & self.nutrition['tinggi'] & self.heavy_metal['rendah'], self.quality['baik']),
            
            # Aturan 2: pH asam/basa + nutrisi rendah + logam tinggi -> buruk
            ctrl.Rule((self.ph['asam'] | self.ph['basa']) & self.nutrition['rendah'] & self.heavy_metal['tinggi'], self.quality['buruk']),
            
            # Aturan 3: pH normal + nutrisi sedang + logam sedang -> sedang
            ctrl.Rule(self.ph['normal'] & self.nutrition['sedang'] & self.heavy_metal['sedang'], self.quality['sedang']),
            
            # Aturan 4: Bahan organik tinggi -> baik
            ctrl.Rule(self.organic_matter['tinggi'], self.quality['baik']),
            
            # Aturan 5: Bahan organik rendah + logam tinggi -> buruk
            ctrl.Rule(self.organic_matter['rendah'] & self.heavy_metal['tinggi'], self.quality['buruk']),
            
            # Aturan 6: pH normal + nutrisi tinggi + logam sedang -> sedang
            ctrl.Rule(self.ph['normal'] & self.nutrition['tinggi'] & self.heavy_metal['sedang'], self.quality['sedang'])
        ]
        
        control_system = ctrl.ControlSystem(rules)
        return ctrl.ControlSystemSimulation(control_system)
    
    def evaluate(self, ph, nutrition, heavy_metal, organic_matter):
        """Evaluasi kualitas tanah"""
        try:
            # Set input
            self.control_system.input['pH'] = ph
            self.control_system.input['nutrition'] = nutrition
            self.control_system.input['heavy_metal'] = heavy_metal
            self.control_system.input['organic_matter'] = organic_matter
            
            # Hitung
            self.control_system.compute()
            
            # Ambil hasil
            score = self.control_system.output['quality']
            
            # Tentukan kategori
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
        """Plot fungsi keanggotaan secara terpisah"""
        
        # Data parameter untuk setiap variabel
        parameters = {
            'pH': {
                'asam': [4, 4, 5.5, 6.0],     # trapezoid: [a, b, c, d]
                'normal': [5.5, 6.5, 7.5],     # triangular: [a, b, c]
                'basa': [6.5, 7.0, 9, 9]      # trapezoid: [a, b, c, d]
            },
            'nutrition': {
                'rendah': [0, 0, 150],
                'sedang': [50, 150, 250],
                'tinggi': [150, 350, 350]
            },
            'heavy_metal': {
                'rendah': [0, 0, 15],
                'sedang': [5, 15, 25],
                'tinggi': [15, 30, 30]
            },
            'organic_matter': {
                'rendah': [0, 0, 3],
                'sedang': [1, 3.5, 6],
                'tinggi': [4, 10, 10]
            },
            'quality': {
                'buruk': [0, 0, 50],
                'sedang': [20, 50, 80],
                'baik': [50, 100, 100]
            }
        }
        
        # Definisi variabel untuk plot terpisah
        variables = [
            (self.ph, 'Fungsi Keanggotaan pH Tanah', 'pH', 'pH', 'ph_membership'),
            (self.nutrition, 'Fungsi Keanggotaan Kandungan Nutrisi', 'Nutrisi (mg/kg)', 'nutrition', 'nutrition_membership'),
            (self.heavy_metal, 'Fungsi Keanggotaan Kandungan Logam Berat', 'Logam Berat (mg/kg)', 'heavy_metal', 'heavy_metal_membership'),
            (self.organic_matter, 'Fungsi Keanggotaan Kandungan Bahan Organik', 'Bahan Organik (%)', 'organic_matter', 'organic_matter_membership'),
            (self.quality, 'Fungsi Keanggotaan Kualitas Tanah (Output)', 'Skor Kualitas', 'quality', 'quality_membership')
        ]
        
        # Buat plot terpisah untuk setiap variabel
        for var, title, xlabel, param_key, filename in variables:
            fig, ax = plt.subplots(1, 1, figsize=(10, 6))
            
            # Plot fungsi keanggotaan
            var.view(ax=ax)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.set_xlabel(xlabel, fontsize=12)
            ax.set_ylabel('Derajat Keanggotaan', fontsize=12)
            ax.grid(True, alpha=0.3)
            
            # Tambahkan label parameter pada setiap fungsi keanggotaan
            for label, params in parameters[param_key].items():
                if len(params) == 4:  # Trapezoid function [a, b, c, d]
                    a, b, c, d = params
                    # Label untuk trapezoid
                    if a == b:  # Left shoulder
                        ax.annotate(f'{a}', xy=(a, 1), xytext=(a, 1.1), 
                                   ha='center', va='bottom', fontsize=10, fontweight='bold',
                                   bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
                    else:
                        ax.annotate(f'{a}', xy=(a, 0), xytext=(a, -0.15), 
                                   ha='center', va='top', fontsize=10, fontweight='bold',
                                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
                    
                    if b != c:  # Peak start
                        ax.annotate(f'{b}', xy=(b, 1), xytext=(b, 1.1), 
                                   ha='center', va='bottom', fontsize=10, fontweight='bold',
                                   bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
                        # Peak end
                        ax.annotate(f'{c}', xy=(c, 1), xytext=(c, 1.1), 
                                   ha='center', va='bottom', fontsize=10, fontweight='bold',
                                   bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
                    
                    if c == d:  # Right shoulder
                        if b != c:  # Only add d label if not already added as c
                            ax.annotate(f'{d}', xy=(d, 1), xytext=(d, 1.1), 
                                       ha='center', va='bottom', fontsize=10, fontweight='bold',
                                       bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
                    else:
                        ax.annotate(f'{d}', xy=(d, 0), xytext=(d, -0.15), 
                                   ha='center', va='top', fontsize=10, fontweight='bold',
                                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
                        
                elif len(params) == 3:  # Triangular function [a, b, c]
                    a, b, c = params
                    # Label untuk triangular (kode lama)
                    if a == b:  # Left shoulder
                        ax.annotate(f'{a}', xy=(a, 1), xytext=(a, 1.1), 
                                   ha='center', va='bottom', fontsize=10, fontweight='bold',
                                   bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
                    else:
                        ax.annotate(f'{a}', xy=(a, 0), xytext=(a, -0.15), 
                                   ha='center', va='top', fontsize=10, fontweight='bold',
                                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
                    
                    if b != c:  # Peak point
                        ax.annotate(f'{b}', xy=(b, 1), xytext=(b, 1.1), 
                                   ha='center', va='bottom', fontsize=10, fontweight='bold',
                                   bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
                    
                    if b == c:  # Right shoulder
                        ax.annotate(f'{c}', xy=(c, 1), xytext=(c, 1.1), 
                                   ha='center', va='bottom', fontsize=10, fontweight='bold',
                                   bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
                    else:
                        ax.annotate(f'{c}', xy=(c, 0), xytext=(c, -0.15), 
                                   ha='center', va='top', fontsize=10, fontweight='bold',
                                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
            
            # Atur batas y untuk memberikan ruang untuk label
            ax.set_ylim(-0.25, 1.25)
            
            # Tambahkan legend yang lebih baik
            ax.legend(loc='upper right', framealpha=0.9)
            
            plt.tight_layout()
            plt.savefig(f'output/{filename}.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # Buat juga gambar gabungan untuk referensi
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Ringkasan Semua Fungsi Keanggotaan - Sistem Fuzzy Mamdani', fontsize=16, fontweight='bold')
        
        # Plot gabungan dengan layout 2x3
        combined_vars = [
            (self.ph, 'pH Tanah', 'pH', axes[0, 0]),
            (self.nutrition, 'Kandungan Nutrisi', 'Nutrisi (mg/kg)', axes[0, 1]),
            (self.heavy_metal, 'Kandungan Logam Berat', 'Logam Berat (mg/kg)', axes[0, 2]),
            (self.organic_matter, 'Kandungan Bahan Organik', 'Bahan Organik (%)', axes[1, 0]),
            (self.quality, 'Kualitas Tanah (Output)', 'Skor Kualitas', axes[1, 1])
        ]
        
        for var, title, xlabel, ax in combined_vars:
            var.view(ax=ax)
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.set_xlabel(xlabel, fontsize=10)
            ax.set_ylabel('Derajat Keanggotaan', fontsize=10)
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=8)
        
        # Sembunyikan subplot yang tidak digunakan
        axes[1, 2].set_visible(False)
        
        plt.tight_layout()
        plt.savefig('output/all_membership_functions.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Gambar fungsi keanggotaan telah dibuat:")
        print("- output/ph_membership.png")
        print("- output/nutrition_membership.png") 
        print("- output/heavy_metal_membership.png")
        print("- output/organic_matter_membership.png")
        print("- output/quality_membership.png")
        print("- output/all_membership_functions.png (ringkasan)")
        print()
    
    def plot_inference(self, ph, nutrition, heavy_metal, organic_matter):
        """Plot inferensi fuzzy untuk input tertentu"""
        try:
            # Hitung hasil
            score, category = self.evaluate(ph, nutrition, heavy_metal, organic_matter)
            
            # Buat plot
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle(f'Inferensi Fuzzy - pH:{ph}, Nutrisi:{nutrition}, Logam:{heavy_metal}, Organik:{organic_matter}%', 
                        fontsize=14, fontweight='bold')
            
            # Plot input dengan garis vertikal
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
                
                # Tambah garis vertikal untuk nilai input
                if var == self.quality:
                    ax.axvline(x=score, color='red', linestyle='--', linewidth=2)
                else:
                    value = ph if var == self.ph else nutrition if var == self.nutrition else heavy_metal
                    ax.axvline(x=value, color='red', linestyle='--', linewidth=2)
            
            plt.tight_layout()
            filename = f'output/inference_ph{ph}_nut{nutrition}_metal{heavy_metal}_org{organic_matter}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            print(f"Error saat plotting inferensi: {e}")

def main():
    # Buat sistem
    system = FuzzySoilQuality()
    
    # Tampilkan fungsi keanggotaan
    system.plot_membership_functions()
    
    # Baca dan proses data
    try:
        df = pd.read_csv('data.csv')
        print("\nSISTEM FUZZY MAMDANI - EVALUASI KUALITAS TANAH")
        
        # Siapkan data untuk tabel
        table_data = []
        headers = ["No", "pH", "Nutrisi", "Logam Berat", "Bahan Organik", "Skor", "Kualitas"]
        
        for index, row in df.iterrows():
            # Ambil data
            ph, nutrition, heavy_metal, organic_matter = row['pH'], row['Nutrisi'], row['Logam_Berat'], row['Bahan_Organik']
            
            # Evaluasi
            score, category = system.evaluate(ph, nutrition, heavy_metal, organic_matter)
            
            # Tampilkan plot inferensi untuk kasus pertama
            if index == 0:
                system.plot_inference(ph, nutrition, heavy_metal, organic_matter)
            
            # Tambahkan ke data tabel
            table_data.append([
                row['No'],
                f"{ph:.1f}",
                f"{nutrition:.0f}",
                f"{heavy_metal:.0f}",
                f"{organic_matter:.0f}",
                f"{score:.1f}",
                category
            ])
        
        # Tampilkan tabel dengan tabulate
        print(tabulate(table_data, headers=headers, tablefmt="rounded_grid"))
        print()

        print("Dibuat Oleh")
        print(":: Agil Ghani Istikmal (5220411040)")
        print()
        
        print("Keterangan:")
        print(":: Skor 0-40: Buruk")
        print(":: Skor 40-70: Sedang") 
        print(":: Skor 70-100: Baik")
        print()
        
    except FileNotFoundError:
        print("Error: data.csv tidak ditemukan!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
