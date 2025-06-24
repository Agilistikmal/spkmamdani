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
        """Plot fungsi keanggotaan dengan kode yang sangat ringkas, tanpa mengubah hasil visual maupun output print."""
        plt.ioff()
        def plot_mf(ax, universe, mfs):
            for func, params, label in mfs:
                ax.plot(universe, func(universe, params), label=label)
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=10)
        # Semua parameter membership function
        mf_params = [
            dict(var=self.ph, mfs=[(fuzz.trapmf, [4, 4, 5.5, 6.0], 'Asam'), (fuzz.trimf, [5.5, 6.5, 7.5], 'Normal'), (fuzz.trapmf, [6.5, 7.0, 9, 9], 'Basa')], title='pH Tanah (Asam: <6.0, Normal: 6.0-7.0, Basa: >7.0)', xlabel='Nilai pH', filename='ph_membership'),
            dict(var=self.nutrition, mfs=[(fuzz.trimf, [0, 0, 150], 'Rendah'), (fuzz.trimf, [50, 150, 250], 'Sedang'), (fuzz.trimf, [150, 350, 350], 'Tinggi')], title='Nutrisi (Rendah: <100, Sedang: 100-200, Tinggi: >200 mg/kg)', xlabel='Nutrisi (mg/kg)', filename='nutrition_membership'),
            dict(var=self.heavy_metal, mfs=[(fuzz.trimf, [0, 0, 15], 'Rendah'), (fuzz.trimf, [5, 15, 25], 'Sedang'), (fuzz.trimf, [15, 30, 30], 'Tinggi')], title='Logam Berat (Rendah: <10, Sedang: 10-20, Tinggi: >20 mg/kg)', xlabel='Logam Berat (mg/kg)', filename='heavy_metal_membership'),
            dict(var=self.organic_matter, mfs=[(fuzz.trimf, [0, 0, 3], 'Rendah'), (fuzz.trimf, [1, 3.5, 6], 'Sedang'), (fuzz.trimf, [4, 10, 10], 'Tinggi')], title='Bahan Organik (Rendah: <2, Sedang: 2-5, Tinggi: >5%)', xlabel='Bahan Organik (%)', filename='organic_matter_membership'),
            dict(var=self.quality, mfs=[(fuzz.trimf, [0, 0, 50], 'Buruk'), (fuzz.trimf, [20, 50, 80], 'Sedang'), (fuzz.trimf, [50, 100, 100], 'Baik')], title='Kualitas Tanah (Buruk: 0-40, Sedang: 40-70, Baik: 70-100)', xlabel='Skor Kualitas', filename='quality_membership')
        ]
        # Plot individual
        for p in mf_params:
            fig, ax = plt.subplots(figsize=(10, 6))
            plot_mf(ax, p['var'].universe, p['mfs'])
            ax.set_title(p['title'], fontsize=14, fontweight='bold', pad=15)
            ax.set_xlabel(p['xlabel'], fontsize=12)
            ax.set_ylabel('Derajat Keanggotaan', fontsize=12)
            plt.tight_layout()
            plt.savefig(f"output/{p['filename']}.png", dpi=300, bbox_inches='tight')
            plt.close()
        # Ringkasan
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Sistem Fuzzy Mamdani - Evaluasi Kualitas Tanah', fontsize=16, fontweight='bold')
        for i, (p, ax) in enumerate(zip(mf_params, [axes[0,0], axes[0,1], axes[0,2], axes[1,0], axes[1,1]])):
            plot_mf(ax, p['var'].universe, p['mfs'])
            ax.set_title(p['title'].split('(')[0].strip(), fontsize=12, fontweight='bold')
            ax.legend(fontsize=8)
        axes[1,2].axis('off')
        axes[1,2].text(0.1, 0.5, \
                       'Aturan Fuzzy:\n\n'
                       '1. pH Normal ∧ Nutrisi Tinggi ∧ Logam Rendah → Baik\n'
                       '2. pH (Asam ∨ Basa) ∧ Nutrisi Rendah ∧ Logam Tinggi → Buruk\n'
                       '3. pH Normal ∧ Nutrisi Sedang ∧ Logam Sedang → Sedang\n'
                       '4. Bahan Organik Tinggi → Baik\n'
                       '5. Bahan Organik Rendah ∧ Logam Tinggi → Buruk\n'
                       '6. pH Normal ∧ Nutrisi Tinggi ∧ Logam Sedang → Sedang\n\n'
                       'Agil Ghani Istikmal (5220411040)',
                       fontsize=10, transform=axes[1,2].transAxes,
                       bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.7))
        plt.tight_layout()
        plt.savefig('output/all_membership_functions.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Visualisasi fungsi keanggotaan berhasil dibuat")

    # Fungsi utilitas untuk manual membership degree
    def _trimf(self, x, params):
        a, b, c = params
        if x <= a or x >= c:
            return 0.0
        elif a < x < b:
            return (x - a) / (b - a)
        elif b <= x < c:
            return (c - x) / (c - b)
        elif x == b:
            return 1.0
        return 0.0

    def _trapmf(self, x, params):
        a, b, c, d = params
        if x <= a or x >= d:
            return 0.0
        elif a < x < b:
            return (x - a) / (b - a)
        elif b <= x <= c:
            return 1.0
        elif c < x < d:
            return (d - x) / (d - c)
        return 0.0

    def _get_membership_degrees(self, ph, nutrition, heavy_metal, organic_matter):
        """Hitung derajat keanggotaan semua input pada setiap label"""
        ph_degrees = {
            'asam': self._trapmf(ph, [4, 4, 5.5, 6.0]),
            'normal': self._trimf(ph, [5.5, 6.5, 7.5]),
            'basa': self._trapmf(ph, [6.5, 7.0, 9, 9])
        }
        nutrition_degrees = {
            'rendah': self._trimf(nutrition, [0, 0, 150]),
            'sedang': self._trimf(nutrition, [50, 150, 250]),
            'tinggi': self._trimf(nutrition, [150, 350, 350])
        }
        heavy_metal_degrees = {
            'rendah': self._trimf(heavy_metal, [0, 0, 15]),
            'sedang': self._trimf(heavy_metal, [5, 15, 25]),
            'tinggi': self._trimf(heavy_metal, [15, 30, 30])
        }
        organic_matter_degrees = {
            'rendah': self._trimf(organic_matter, [0, 0, 3]),
            'sedang': self._trimf(organic_matter, [1, 3.5, 6]),
            'tinggi': self._trimf(organic_matter, [4, 10, 10])
        }
        return {
            'ph': ph_degrees,
            'nutrition': nutrition_degrees,
            'heavy_metal': heavy_metal_degrees,
            'organic_matter': organic_matter_degrees
        }

    def explain(self, ph, nutrition, heavy_metal, organic_matter):
        """Tampilkan step-by-step perhitungan fuzzy untuk satu data input, termasuk detail perhitungan membership degree."""
        from tabulate import tabulate
        print("\n:: DETAIL FUZZIFIKASI")
        print("[PH]")
        ph_asam = self._explain_trapmf(ph, [4, 4, 5.5, 6.0], 'Asam')
        ph_normal = self._explain_trimf(ph, [5.5, 6.5, 7.5], 'Normal')
        ph_basa = self._explain_trapmf(ph, [6.5, 7.0, 9, 9], 'Basa')
        print("\n[NUTRISI]")
        nut_rendah = self._explain_trimf(nutrition, [0, 0, 150], 'Rendah')
        nut_sedang = self._explain_trimf(nutrition, [50, 150, 250], 'Sedang')
        nut_tinggi = self._explain_trimf(nutrition, [150, 350, 350], 'Tinggi')
        print("\n[LOGAM BERAT]")
        metal_rendah = self._explain_trimf(heavy_metal, [0, 0, 15], 'Rendah')
        metal_sedang = self._explain_trimf(heavy_metal, [5, 15, 25], 'Sedang')
        metal_tinggi = self._explain_trimf(heavy_metal, [15, 30, 30], 'Tinggi')
        print("\n[BAHAN ORGANIK]")
        org_rendah = self._explain_trimf(organic_matter, [0, 0, 3], 'Rendah')
        org_sedang = self._explain_trimf(organic_matter, [1, 3.5, 6], 'Sedang')
        org_tinggi = self._explain_trimf(organic_matter, [4, 10, 10], 'Tinggi')
        # Tabel ringkasan
        md = {
            'ph': {'asam': ph_asam, 'normal': ph_normal, 'basa': ph_basa},
            'nutrition': {'rendah': nut_rendah, 'sedang': nut_sedang, 'tinggi': nut_tinggi},
            'heavy_metal': {'rendah': metal_rendah, 'sedang': metal_sedang, 'tinggi': metal_tinggi},
            'organic_matter': {'rendah': org_rendah, 'sedang': org_sedang, 'tinggi': org_tinggi}
        }
        table = [
            ["pH", ph, md['ph']['asam'], md['ph']['normal'], md['ph']['basa']],
            ["Nutrisi", nutrition, md['nutrition']['rendah'], md['nutrition']['sedang'], md['nutrition']['tinggi']],
            ["Logam Berat", heavy_metal, md['heavy_metal']['rendah'], md['heavy_metal']['sedang'], md['heavy_metal']['tinggi']],
            ["Bahan Organik", organic_matter, md['organic_matter']['rendah'], md['organic_matter']['sedang'], md['organic_matter']['tinggi']]
        ]
        print("\nRingkasan Derajat Keanggotaan:")
        print(tabulate(table, headers=["Variabel", "Nilai", "Rendah/Asam", "Sedang/Normal", "Tinggi/Basa"], floatfmt=".3f", tablefmt="rounded_grid"))
        # 2. Firing strength rules
        rules = []
        # Aturan 1
        r1 = min(md['ph']['normal'], md['nutrition']['tinggi'], md['heavy_metal']['rendah'])
        rules.append(("pH normal ∧ nutrisi tinggi ∧ logam rendah → Baik", r1, "Baik"))
        # Aturan 2
        r2 = min(max(md['ph']['asam'], md['ph']['basa']), md['nutrition']['rendah'], md['heavy_metal']['tinggi'])
        rules.append(("(pH asam ∨ basa) ∧ nutrisi rendah ∧ logam tinggi → Buruk", r2, "Buruk"))
        # Aturan 3
        r3 = min(md['ph']['normal'], md['nutrition']['sedang'], md['heavy_metal']['sedang'])
        rules.append(("pH normal ∧ nutrisi sedang ∧ logam sedang → Sedang", r3, "Sedang"))
        # Aturan 4
        r4 = md['organic_matter']['tinggi']
        rules.append(("bahan organik tinggi → Baik", r4, "Baik"))
        # Aturan 5
        r5 = min(md['organic_matter']['rendah'], md['heavy_metal']['tinggi'])
        rules.append(("bahan organik rendah ∧ logam tinggi → Buruk", r5, "Buruk"))
        # Aturan 6
        r6 = min(md['ph']['normal'], md['nutrition']['tinggi'], md['heavy_metal']['sedang'])
        rules.append(("pH normal ∧ nutrisi tinggi ∧ logam sedang → Sedang", r6, "Sedang"))
        print("\nFiring Strength (α) Setiap Aturan:")
        rule_table = [[i+1, desc, f"{alpha:.3f}", out] for i, (desc, alpha, out) in enumerate(rules)]
        print(tabulate(rule_table, headers=["No", "Rule", "α", "Output"], tablefmt="rounded_grid"))
        # 3. Agregasi
        a_buruk = max(rules[1][1], rules[4][1])
        a_sedang = max(rules[2][1], rules[5][1])
        a_baik = max(rules[0][1], rules[3][1])
        print(f"\nAgregasi α:")
        print(f"  α_buruk  = max({rules[1][1]:.3f}, {rules[4][1]:.3f}) = {a_buruk:.3f}")
        print(f"  α_sedang = max({rules[2][1]:.3f}, {rules[5][1]:.3f}) = {a_sedang:.3f}")
        print(f"  α_baik   = max({rules[0][1]:.3f}, {rules[3][1]:.3f}) = {a_baik:.3f}")
        # 4. Tampilkan rumus defuzzifikasi saja (tanpa perhitungan manual)
        print(f"\nDefuzzifikasi (Metode Centroid):")
        print(f"  Skor akhir = (α_buruk × z_buruk + α_sedang × z_sedang + α_baik × z_baik) / (α_buruk + α_sedang + α_baik)")
        # 5. Defuzzifikasi (pakai library agar konsisten)
        score, category = self.evaluate(ph, nutrition, heavy_metal, organic_matter)
        print(f"\nDefuzzifikasi (skor akhir dari library): {score:.2f}")
        print(f"Kategori: {category}\n")

    def _explain_trimf(self, x, params, label):
        a, b, c = params
        print(f"  - {label} (triangular [{a}, {b}, {c}]):")
        print(f"    x = {x}")
        if x <= a or x >= c:
            print(f"    Karena x <= {a} atau x >= {c}, maka μ = 0.0")
            return 0.0
        elif a < x < b:
            val = (x - a) / (b - a)
            print(f"    Karena {a} < x < {b}, maka μ = (x - {a}) / ({b} - {a}) = ({x} - {a}) / {b - a} = {val:.3f}")
            return val
        elif b <= x < c:
            val = (c - x) / (c - b)
            print(f"    Karena {b} <= x < {c}, maka μ = ({c} - x) / ({c} - {b}) = ({c} - {x}) / {c - b} = {val:.3f}")
            return val
        elif x == b:
            print(f"    Karena x == {b}, maka μ = 1.0")
            return 1.0
        print(f"    (Tidak terdefinisi, μ = 0.0)")
        return 0.0

    def _explain_trapmf(self, x, params, label):
        a, b, c, d = params
        print(f"  - {label} (trapezoid [{a}, {b}, {c}, {d}]):")
        print(f"    x = {x}")
        if x <= a or x >= d:
            print(f"    Karena x <= {a} atau x >= {d}, maka μ = 0.0")
            return 0.0
        elif a < x < b:
            val = (x - a) / (b - a)
            print(f"    Karena {a} < x < {b}, maka μ = (x - {a}) / ({b} - {a}) = ({x} - {a}) / {b - a} = {val:.3f}")
            return val
        elif b <= x <= c:
            print(f"    Karena {b} <= x <= {c}, maka μ = 1.0")
            return 1.0
        elif c < x < d:
            val = (d - x) / (d - c)
            print(f"    Karena {c} < x < {d}, maka μ = ({d} - x) / ({d} - {c}) = ({d} - {x}) / {d - c} = {val:.3f}")
            return val
        print(f"    (Tidak terdefinisi, μ = 0.0)")
        return 0.0

    def plot_input_membership_for_data(self, no, ph, nutrition, heavy_metal, organic_matter):
        """Plot membership function tiap variabel dengan garis vertikal pada nilai input, simpan ke output/{no}/"""
        import matplotlib.pyplot as plt
        import os
        # Siapkan folder
        folder = f"output/{no}"
        if not os.path.exists(folder):
            os.makedirs(folder)
        # Daftar parameter
        mf_params = [
            dict(var=self.ph, mfs=[(fuzz.trapmf, [4, 4, 5.5, 6.0], 'Asam'), (fuzz.trimf, [5.5, 6.5, 7.5], 'Normal'), (fuzz.trapmf, [6.5, 7.0, 9, 9], 'Basa')], title='pH Tanah', xlabel='Nilai pH', filename='ph', value=ph),
            dict(var=self.nutrition, mfs=[(fuzz.trimf, [0, 0, 150], 'Rendah'), (fuzz.trimf, [50, 150, 250], 'Sedang'), (fuzz.trimf, [150, 350, 350], 'Tinggi')], title='Nutrisi', xlabel='Nutrisi (mg/kg)', filename='nutrition', value=nutrition),
            dict(var=self.heavy_metal, mfs=[(fuzz.trimf, [0, 0, 15], 'Rendah'), (fuzz.trimf, [5, 15, 25], 'Sedang'), (fuzz.trimf, [15, 30, 30], 'Tinggi')], title='Logam Berat', xlabel='Logam Berat (mg/kg)', filename='heavy_metal', value=heavy_metal),
            dict(var=self.organic_matter, mfs=[(fuzz.trimf, [0, 0, 3], 'Rendah'), (fuzz.trimf, [1, 3.5, 6], 'Sedang'), (fuzz.trimf, [4, 10, 10], 'Tinggi')], title='Bahan Organik', xlabel='Bahan Organik (%)', filename='organic_matter', value=organic_matter),
            dict(var=self.quality, mfs=[(fuzz.trimf, [0, 0, 50], 'Buruk'), (fuzz.trimf, [20, 50, 80], 'Sedang'), (fuzz.trimf, [50, 100, 100], 'Baik')], title='Kualitas Tanah', xlabel='Skor Kualitas', filename='quality', value=None)
        ]
        for p in mf_params:
            fig, ax = plt.subplots(figsize=(8, 5))
            for func, params, label in p['mfs']:
                ax.plot(p['var'].universe, func(p['var'].universe, params), label=label)
            # Garis vertikal pada nilai input (kecuali quality)
            if p['value'] is not None:
                ax.axvline(p['value'], color='red', linestyle='--', label=f"Input: {p['value']}")
            ax.set_title(p['title'], fontsize=13, fontweight='bold')
            ax.set_xlabel(p['xlabel'])
            ax.set_ylabel('Derajat Keanggotaan')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=9)
            plt.tight_layout()
            plt.savefig(f"{folder}/{p['filename']}.png", dpi=200, bbox_inches='tight')
            plt.close()

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
        
        # Tampilkan step-by-step untuk semua data
        for idx, row in df.iterrows():
            print(f"\n:: STEP-BY-STEP PERHITUNGAN DATA {row['No']}")
            system.explain(row['pH'], row['Nutrisi'], row['Logam_Berat'], row['Bahan_Organik'])
            # Plot membership function untuk data ini
            system.plot_input_membership_for_data(
                row['No'], row['pH'], row['Nutrisi'], row['Logam_Berat'], row['Bahan_Organik']
            )
        
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
