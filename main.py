import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class FuzzyMamdaniSoilQuality:
    def __init__(self):
        # Define universe of discourse for each parameter
        self.ph_range = np.arange(4.0, 9.1, 0.1)
        self.nutrition_range = np.arange(0, 351, 1)
        self.heavy_metal_range = np.arange(0, 31, 0.1)
        self.organic_matter_range = np.arange(0, 11, 0.1)
        self.quality_range = np.arange(0, 101, 0.1)
        
    def ph_membership(self, ph_value):
        """Calculate membership values for pH"""
        asam = np.zeros_like(self.ph_range)
        normal = np.zeros_like(self.ph_range)
        basa = np.zeros_like(self.ph_range)
        
        # Asam: < 6.0 (triangular: 4.0-6.0)
        for i, ph in enumerate(self.ph_range):
            if ph <= 4.0:
                asam[i] = 1.0
            elif 4.0 < ph <= 6.0:
                asam[i] = (6.0 - ph) / 2.0
            else:
                asam[i] = 0.0
                
        # Normal: 6.0-7.0 (triangular: 5.5-7.5)
        for i, ph in enumerate(self.ph_range):
            if ph <= 5.5:
                normal[i] = 0.0
            elif 5.5 < ph <= 6.5:
                normal[i] = (ph - 5.5) / 1.0
            elif 6.5 < ph <= 7.5:
                normal[i] = (7.5 - ph) / 1.0
            else:
                normal[i] = 0.0
                
        # Basa: > 7.0 (triangular: 6.5-9.0)
        for i, ph in enumerate(self.ph_range):
            if ph <= 6.5:
                basa[i] = 0.0
            elif 6.5 < ph <= 9.0:
                basa[i] = (ph - 6.5) / 2.5
            else:
                basa[i] = 1.0
                
        # Find membership value for input
        ph_idx = np.argmin(np.abs(self.ph_range - ph_value))
        return asam[ph_idx], normal[ph_idx], basa[ph_idx]
    
    def nutrition_membership(self, nutrition_value):
        """Calculate membership values for nutrition content"""
        rendah = np.zeros_like(self.nutrition_range)
        sedang = np.zeros_like(self.nutrition_range)
        tinggi = np.zeros_like(self.nutrition_range)
        
        # Rendah: < 100 (triangular: 0-150)
        for i, nut in enumerate(self.nutrition_range):
            if nut <= 0:
                rendah[i] = 1.0
            elif 0 < nut <= 100:
                rendah[i] = (100 - nut) / 100
            elif 100 < nut <= 150:
                rendah[i] = (150 - nut) / 50
            else:
                rendah[i] = 0.0
                
        # Sedang: 100-200 (triangular: 50-250)
        for i, nut in enumerate(self.nutrition_range):
            if nut <= 50:
                sedang[i] = 0.0
            elif 50 < nut <= 150:
                sedang[i] = (nut - 50) / 100
            elif 150 < nut <= 250:
                sedang[i] = (250 - nut) / 100
            else:
                sedang[i] = 0.0
                
        # Tinggi: > 200 (triangular: 150-350)
        for i, nut in enumerate(self.nutrition_range):
            if nut <= 150:
                tinggi[i] = 0.0
            elif 150 < nut <= 200:
                tinggi[i] = (nut - 150) / 50
            elif 200 < nut <= 350:
                tinggi[i] = 1.0
            else:
                tinggi[i] = 1.0
                
        # Find membership value for input
        nut_idx = np.argmin(np.abs(self.nutrition_range - nutrition_value))
        return rendah[nut_idx], sedang[nut_idx], tinggi[nut_idx]
    
    def heavy_metal_membership(self, metal_value):
        """Calculate membership values for heavy metal content"""
        rendah = np.zeros_like(self.heavy_metal_range)
        sedang = np.zeros_like(self.heavy_metal_range)
        tinggi = np.zeros_like(self.heavy_metal_range)
        
        # Rendah: < 10 (triangular: 0-15)
        for i, metal in enumerate(self.heavy_metal_range):
            if metal <= 0:
                rendah[i] = 1.0
            elif 0 < metal <= 10:
                rendah[i] = (10 - metal) / 10
            elif 10 < metal <= 15:
                rendah[i] = (15 - metal) / 5
            else:
                rendah[i] = 0.0
                
        # Sedang: 10-20 (triangular: 5-25)
        for i, metal in enumerate(self.heavy_metal_range):
            if metal <= 5:
                sedang[i] = 0.0
            elif 5 < metal <= 15:
                sedang[i] = (metal - 5) / 10
            elif 15 < metal <= 25:
                sedang[i] = (25 - metal) / 10
            else:
                sedang[i] = 0.0
                
        # Tinggi: > 20 (triangular: 15-30)
        for i, metal in enumerate(self.heavy_metal_range):
            if metal <= 15:
                tinggi[i] = 0.0
            elif 15 < metal <= 20:
                tinggi[i] = (metal - 15) / 5
            elif 20 < metal <= 30:
                tinggi[i] = 1.0
            else:
                tinggi[i] = 1.0
                
        # Find membership value for input
        metal_idx = np.argmin(np.abs(self.heavy_metal_range - metal_value))
        return rendah[metal_idx], sedang[metal_idx], tinggi[metal_idx]
    
    def organic_matter_membership(self, organic_value):
        """Calculate membership values for organic matter content"""
        rendah = np.zeros_like(self.organic_matter_range)
        sedang = np.zeros_like(self.organic_matter_range)
        tinggi = np.zeros_like(self.organic_matter_range)
        
        # Rendah: < 2 (triangular: 0-3)
        for i, org in enumerate(self.organic_matter_range):
            if org <= 0:
                rendah[i] = 1.0
            elif 0 < org <= 2:
                rendah[i] = (2 - org) / 2
            elif 2 < org <= 3:
                rendah[i] = (3 - org) / 1
            else:
                rendah[i] = 0.0
                
        # Sedang: 2-5 (triangular: 1-6)
        for i, org in enumerate(self.organic_matter_range):
            if org <= 1:
                sedang[i] = 0.0
            elif 1 < org <= 3.5:
                sedang[i] = (org - 1) / 2.5
            elif 3.5 < org <= 6:
                sedang[i] = (6 - org) / 2.5
            else:
                sedang[i] = 0.0
                
        # Tinggi: > 5 (triangular: 4-10)
        for i, org in enumerate(self.organic_matter_range):
            if org <= 4:
                tinggi[i] = 0.0
            elif 4 < org <= 5:
                tinggi[i] = (org - 4) / 1
            elif 5 < org <= 10:
                tinggi[i] = 1.0
            else:
                tinggi[i] = 1.0
                
        # Find membership value for input
        org_idx = np.argmin(np.abs(self.organic_matter_range - organic_value))
        return rendah[org_idx], sedang[org_idx], tinggi[org_idx]
    
    def quality_membership_functions(self):
        """Define membership functions for soil quality output"""
        buruk = np.zeros_like(self.quality_range)
        sedang = np.zeros_like(self.quality_range)
        baik = np.zeros_like(self.quality_range)
        
        # Buruk: 0-40 (triangular: 0-50)
        for i, qual in enumerate(self.quality_range):
            if qual <= 0:
                buruk[i] = 1.0
            elif 0 < qual <= 25:
                buruk[i] = (25 - qual) / 25
            elif 25 < qual <= 50:
                buruk[i] = (50 - qual) / 25
            else:
                buruk[i] = 0.0
                
        # Sedang: 30-70 (triangular: 20-80)
        for i, qual in enumerate(self.quality_range):
            if qual <= 20:
                sedang[i] = 0.0
            elif 20 < qual <= 50:
                sedang[i] = (qual - 20) / 30
            elif 50 < qual <= 80:
                sedang[i] = (80 - qual) / 30
            else:
                sedang[i] = 0.0
                
        # Baik: 60-100 (triangular: 50-100)
        for i, qual in enumerate(self.quality_range):
            if qual <= 50:
                baik[i] = 0.0
            elif 50 < qual <= 75:
                baik[i] = (qual - 50) / 25
            elif 75 < qual <= 100:
                baik[i] = 1.0
            else:
                baik[i] = 1.0
                
        return buruk, sedang, baik
    
    def apply_fuzzy_rules(self, ph_asam, ph_normal, ph_basa, 
                         nut_rendah, nut_sedang, nut_tinggi,
                         metal_rendah, metal_sedang, metal_tinggi,
                         org_rendah, org_sedang, org_tinggi):
        """Apply fuzzy rules and get output membership values"""
        buruk, sedang, baik = self.quality_membership_functions()
        
        # Initialize output membership arrays
        output_buruk = np.zeros_like(self.quality_range)
        output_sedang = np.zeros_like(self.quality_range)
        output_baik = np.zeros_like(self.quality_range)
        
        # Rule 1: Jika pH normal dan kandungan nutrisi tinggi dan kandungan logam berat rendah, maka kualitas tanah baik
        rule1_strength = min(ph_normal, nut_tinggi, metal_rendah)
        output_baik = np.maximum(output_baik, np.minimum(rule1_strength, baik))
        
        # Rule 2: Jika pH asam atau basa dan kandungan nutrisi rendah dan kandungan logam berat tinggi, maka kualitas tanah buruk
        rule2_strength = min(max(ph_asam, ph_basa), nut_rendah, metal_tinggi)
        output_buruk = np.maximum(output_buruk, np.minimum(rule2_strength, buruk))
        
        # Rule 3: Jika pH normal dan kandungan nutrisi sedang dan kandungan logam berat sedang, maka kualitas tanah sedang
        rule3_strength = min(ph_normal, nut_sedang, metal_sedang)
        output_sedang = np.maximum(output_sedang, np.minimum(rule3_strength, sedang))
        
        # Rule 4: Jika kandungan bahan organik tinggi, maka kualitas tanah baik
        rule4_strength = org_tinggi
        output_baik = np.maximum(output_baik, np.minimum(rule4_strength, baik))
        
        # Rule 5: Jika kandungan bahan organik rendah dan kandungan logam berat tinggi, maka kualitas tanah buruk
        rule5_strength = min(org_rendah, metal_tinggi)
        output_buruk = np.maximum(output_buruk, np.minimum(rule5_strength, buruk))
        
        # Rule 6: Jika pH normal dan kandungan nutrisi tinggi dan kandungan logam berat sedang, maka kualitas tanah sedang
        rule6_strength = min(ph_normal, nut_tinggi, metal_sedang)
        output_sedang = np.maximum(output_sedang, np.minimum(rule6_strength, sedang))
        
        return output_buruk, output_sedang, output_baik
    
    def defuzzify(self, output_buruk, output_sedang, output_baik):
        """Defuzzify using Center of Gravity method"""
        # Combine all output membership functions
        combined_output = np.maximum.reduce([output_buruk, output_sedang, output_baik])
        
        # Calculate center of gravity
        numerator = np.sum(self.quality_range * combined_output)
        denominator = np.sum(combined_output)
        
        if denominator == 0:
            return 50.0  # Default to middle value if no rules fired
        
        return numerator / denominator
    
    def evaluate_soil_quality(self, ph, nutrition, heavy_metal, organic_matter):
        """Evaluate soil quality using fuzzy Mamdani system"""
        # Get membership values for inputs
        ph_asam, ph_normal, ph_basa = self.ph_membership(ph)
        nut_rendah, nut_sedang, nut_tinggi = self.nutrition_membership(nutrition)
        metal_rendah, metal_sedang, metal_tinggi = self.heavy_metal_membership(heavy_metal)
        org_rendah, org_sedang, org_tinggi = self.organic_matter_membership(organic_matter)
        
        # Apply fuzzy rules
        output_buruk, output_sedang, output_baik = self.apply_fuzzy_rules(
            ph_asam, ph_normal, ph_basa,
            nut_rendah, nut_sedang, nut_tinggi,
            metal_rendah, metal_sedang, metal_tinggi,
            org_rendah, org_sedang, org_tinggi
        )
        
        # Defuzzify to get crisp output
        quality_score = self.defuzzify(output_buruk, output_sedang, output_baik)
        
        # Determine quality category
        if quality_score < 40:
            quality_category = "Buruk"
        elif quality_score < 70:
            quality_category = "Sedang"
        else:
            quality_category = "Baik"
        
        return quality_score, quality_category

def main():
    # Create fuzzy system
    fuzzy_system = FuzzyMamdaniSoilQuality()
    
    # Read test cases from CSV file
    try:
        df = pd.read_csv('data.csv')
        print("SISTEM FUZZY MAMDANI UNTUK EVALUASI KUALITAS TANAH")
        print("=" * 60)
        print("No | pH | Nutrisi | Logam Berat | Bahan Organik | Skor | Kualitas")
        print("-" * 60)
        
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
        
        print("=" * 60)
        print("\nKeterangan:")
        print("- Skor 0-40: Buruk")
        print("- Skor 40-70: Sedang") 
        print("- Skor 70-100: Baik")
        
    except FileNotFoundError:
        print("Error: File data.csv tidak ditemukan!")
        print("Pastikan file data.csv ada di direktori yang sama dengan main.py")
    except Exception as e:
        print(f"Error membaca file CSV: {e}")

if __name__ == "__main__":
    main()
