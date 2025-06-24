import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import os
from tabulate import tabulate
warnings.filterwarnings('ignore', category=UserWarning, module='skfuzzy')
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
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
        # Fungsi keanggotaan pH - sesuai spesifikasi soal
        self.ph['asam'] = fuzz.trapmf(self.ph.universe, [4, 4, 5.5, 6.0])     # <6.0
        self.ph['normal'] = fuzz.trimf(self.ph.universe, [5.5, 6.5, 7.5])     # 6.0-7.0
        self.ph['basa'] = fuzz.trapmf(self.ph.universe, [6.5, 7.0, 9, 9])     # >7.0
        
        # Fungsi keanggotaan nutrisi
        self.nutrition['rendah'] = fuzz.trimf(self.nutrition.universe, [0, 0, 150])      # <100
        self.nutrition['sedang'] = fuzz.trimf(self.nutrition.universe, [50, 150, 250])   # 100-200
        self.nutrition['tinggi'] = fuzz.trimf(self.nutrition.universe, [150, 350, 350])  # >200
        
        # Fungsi keanggotaan logam berat
        self.heavy_metal['rendah'] = fuzz.trimf(self.heavy_metal.universe, [0, 0, 15])   # <10
        self.heavy_metal['sedang'] = fuzz.trimf(self.heavy_metal.universe, [5, 15, 25])  # 10-20
        self.heavy_metal['tinggi'] = fuzz.trimf(self.heavy_metal.universe, [15, 30, 30]) # >20
        
        # Fungsi keanggotaan bahan organik
        self.organic_matter['rendah'] = fuzz.trimf(self.organic_matter.universe, [0, 0, 3])    # <2
        self.organic_matter['sedang'] = fuzz.trimf(self.organic_matter.universe, [1, 3.5, 6])  # 2-5
        self.organic_matter['tinggi'] = fuzz.trimf(self.organic_matter.universe, [4, 10, 10])  # >5
        
        # Fungsi keanggotaan kualitas output
        self.quality['buruk'] = fuzz.trimf(self.quality.universe, [0, 0, 50])      # 0-40
        self.quality['sedang'] = fuzz.trimf(self.quality.universe, [20, 50, 80])   # 40-70
        self.quality['baik'] = fuzz.trimf(self.quality.universe, [50, 100, 100])   # 70-100
    
    def _create_rules(self):
        """Buat aturan fuzzy sesuai soal"""
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
        
        return ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))
    
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
        """Plot fungsi keanggotaan dengan visualisasi sederhana tapi informatif"""
        
        # Definisi variabel untuk plot
        variables = [
            (self.ph, 'pH Tanah (Asam: <6.0, Normal: 6.0-7.0, Basa: >7.0)', 'Nilai pH', 'ph_membership'),
            (self.nutrition, 'Nutrisi (Rendah: <100, Sedang: 100-200, Tinggi: >200 mg/kg)', 'Nutrisi (mg/kg)', 'nutrition_membership'),
            (self.heavy_metal, 'Logam Berat (Rendah: <10, Sedang: 10-20, Tinggi: >20 mg/kg)', 'Logam Berat (mg/kg)', 'heavy_metal_membership'),
            (self.organic_matter, 'Bahan Organik (Rendah: <2, Sedang: 2-5, Tinggi: >5%)', 'Bahan Organik (%)', 'organic_matter_membership'),
            (self.quality, 'Kualitas Tanah (Buruk: 0-40, Sedang: 40-70, Baik: 70-100)', 'Skor Kualitas', 'quality_membership')
        ]
        
        # Buat plot individual yang simpel
        for var, title, xlabel, filename in variables:
            fig, ax = plt.subplots(figsize=(10, 6))
            var.view(ax=ax)
            ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
            ax.set_xlabel(xlabel, fontsize=12)
            ax.set_ylabel('Derajat Keanggotaan', fontsize=12)
            ax.grid(True, alpha=0.3)
            
            # Hanya tambahkan legend jika ada elemen yang berlabel
            handles, labels = ax.get_legend_handles_labels()
            if handles:
                ax.legend(fontsize=10)
            
            plt.tight_layout()
            plt.savefig(f'output/{filename}.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # Buat gambar ringkasan
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Sistem Fuzzy Mamdani - Evaluasi Kualitas Tanah', fontsize=16, fontweight='bold')
        
        plot_vars = [
            (self.ph, 'pH Tanah', axes[0, 0]),
            (self.nutrition, 'Nutrisi', axes[0, 1]),
            (self.heavy_metal, 'Logam Berat', axes[0, 2]),
            (self.organic_matter, 'Bahan Organik', axes[1, 0]),
            (self.quality, 'Kualitas (Output)', axes[1, 1])
        ]
        
        for var, title, ax in plot_vars:
            var.view(ax=ax)
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            # Hanya tambahkan legend jika ada elemen yang berlabel
            handles, labels = ax.get_legend_handles_labels()
            if handles:
                ax.legend(fontsize=8)
        
        # Sembunyikan subplot kosong dan tambahkan info
        axes[1, 2].axis('off')
        axes[1, 2].text(0.1, 0.5, 
                       'Aturan Fuzzy:\n\n'
                       '1. pH Normal ∧ Nutrisi Tinggi ∧ Logam Rendah → Baik\n'
                       '2. pH (Asam ∨ Basa) ∧ Nutrisi Rendah ∧ Logam Tinggi → Buruk\n'
                       '3. pH Normal ∧ Nutrisi Sedang ∧ Logam Sedang → Sedang\n'
                       '4. Bahan Organik Tinggi → Baik\n'
                       '5. Bahan Organik Rendah ∧ Logam Tinggi → Buruk\n'
                       '6. pH Normal ∧ Nutrisi Tinggi ∧ Logam Sedang → Sedang\n\n'
                       'Agil Ghani Istikmal (5220411040)',
                       fontsize=10, transform=axes[1, 2].transAxes,
                       bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.7))
        
        plt.tight_layout()
        plt.savefig('output/all_membership_functions.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Visualisasi fungsi keanggotaan berhasil dibuat")

def main():
    print()
    print("SISTEM FUZZY MAMDANI - EVALUASI KUALITAS TANAH")
    print()
    
    # Buat sistem
    system = FuzzySoilQuality()
    
    # Tampilkan fungsi keanggotaan
    system.plot_membership_functions()
    
    # Baca dan proses data
    try:
        df = pd.read_csv('data.csv')
        
        # Siapkan data untuk tabel
        table_data = []
        headers = ["No", "pH", "Nutrisi", "Logam Berat", "Bahan Organik", "Skor", "Kualitas"]
        
        for index, row in df.iterrows():
            # Ambil data
            ph, nutrition, heavy_metal, organic_matter = row['pH'], row['Nutrisi'], row['Logam_Berat'], row['Bahan_Organik']
            
            # Evaluasi
            score, category = system.evaluate(ph, nutrition, heavy_metal, organic_matter)
            
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
        
        # Tampilkan hasil
        print(tabulate(table_data, headers=headers, tablefmt="rounded_grid"))
        print()
        print("Dibuat Oleh")
        print("Agil Ghani Istikmal (5220411040)")
        print()
        print("Keterangan Skor")
        print(":: 0-40   => Buruk")
        print(":: 40-70  => Sedang") 
        print(":: 70-100 => Baik")
        print()
        
    except FileNotFoundError:
        print("Error: File data.csv tidak ditemukan!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
