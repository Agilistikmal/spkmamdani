import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def trimf(x, a, b, c):
    """Triangular membership function"""
    if x <= a or x >= c: return 0
    if x < b: return (x - a) / (b - a)
    return (c - x) / (c - b)

def trapmf(x, a, b, c, d):
    """Trapezoidal membership function"""
    if x <= a or x >= d: return 0
    if x < b: return (x - a) / (b - a)
    if x <= c: return 1
    return (d - x) / (d - c)

def fuzzify(ph, nutrition, heavy_metal, organic_matter):
    """Fuzzification - calculate membership degrees"""
    return {
        'ph': {
            'asam': trapmf(ph, 4, 4, 5.5, 6.0),
            'normal': trimf(ph, 5.5, 6.5, 7.5),
            'basa': trapmf(ph, 6.5, 7.0, 9, 9)
        },
        'nutrition': {
            'rendah': trimf(nutrition, 0, 0, 150),
            'sedang': trimf(nutrition, 50, 150, 250),
            'tinggi': trimf(nutrition, 150, 350, 350)
        },
        'heavy_metal': {
            'rendah': trimf(heavy_metal, 0, 0, 15),
            'sedang': trimf(heavy_metal, 5, 15, 25),
            'tinggi': trimf(heavy_metal, 15, 30, 30)
        },
        'organic_matter': {
            'rendah': trimf(organic_matter, 0, 0, 3),
            'sedang': trimf(organic_matter, 1, 3.5, 6),
            'tinggi': trimf(organic_matter, 4, 10, 10)
        }
    }

def inference(md):
    """Inference - apply fuzzy rules"""
    rules = [
        min(md['ph']['normal'], md['nutrition']['tinggi'], md['heavy_metal']['rendah']),  # R1: baik
        min(max(md['ph']['asam'], md['ph']['basa']), md['nutrition']['rendah'], md['heavy_metal']['tinggi']),  # R2: buruk
        min(md['ph']['normal'], md['nutrition']['sedang'], md['heavy_metal']['sedang']),  # R3: sedang
        md['organic_matter']['tinggi'],  # R4: baik
        min(md['organic_matter']['rendah'], md['heavy_metal']['tinggi']),  # R5: buruk
        min(md['ph']['normal'], md['nutrition']['tinggi'], md['heavy_metal']['sedang'])  # R6: sedang
    ]
    return {
        'buruk': max(rules[1], rules[4]),
        'sedang': max(rules[2], rules[5]),
        'baik': max(rules[0], rules[3])
    }

def defuzzify(alpha):
    """Defuzzification using centroid method"""
    # Centroid points for each quality category
    centroids = {'buruk': 25, 'sedang': 50, 'baik': 75}
    
    numerator = sum(alpha[k] * centroids[k] for k in alpha)
    denominator = sum(alpha.values())
    
    return numerator / denominator if denominator > 0 else 50

def evaluate(ph, nutrition, heavy_metal, organic_matter):
    """Complete fuzzy evaluation"""
    md = fuzzify(ph, nutrition, heavy_metal, organic_matter)
    alpha = inference(md)
    score = defuzzify(alpha)
    
    category = "Buruk" if score < 40 else "Sedang" if score < 70 else "Baik"
    return score, category

def plot_membership_functions():
    """Plot dan simpan gambar membership functions"""
    plt.ioff()
    
    # Parameter membership functions
    mf_params = [
        {
            'name': 'pH', 'range': (4, 9), 'mfs': [
                ('Asam', lambda x: [trapmf(xi, 4, 4, 5.5, 6.0) for xi in x]),
                ('Normal', lambda x: [trimf(xi, 5.5, 6.5, 7.5) for xi in x]),
                ('Basa', lambda x: [trapmf(xi, 6.5, 7.0, 9, 9) for xi in x])
            ], 'title': 'pH Tanah', 'xlabel': 'Nilai pH', 'filename': 'ph_membership'
        },
        {
            'name': 'Nutrition', 'range': (0, 350), 'mfs': [
                ('Rendah', lambda x: [trimf(xi, 0, 0, 150) for xi in x]),
                ('Sedang', lambda x: [trimf(xi, 50, 150, 250) for xi in x]),
                ('Tinggi', lambda x: [trimf(xi, 150, 350, 350) for xi in x])
            ], 'title': 'Nutrisi', 'xlabel': 'Nutrisi (mg/kg)', 'filename': 'nutrition_membership'
        },
        {
            'name': 'Heavy Metal', 'range': (0, 30), 'mfs': [
                ('Rendah', lambda x: [trimf(xi, 0, 0, 15) for xi in x]),
                ('Sedang', lambda x: [trimf(xi, 5, 15, 25) for xi in x]),
                ('Tinggi', lambda x: [trimf(xi, 15, 30, 30) for xi in x])
            ], 'title': 'Logam Berat', 'xlabel': 'Logam Berat (mg/kg)', 'filename': 'heavy_metal_membership'
        },
        {
            'name': 'Organic Matter', 'range': (0, 10), 'mfs': [
                ('Rendah', lambda x: [trimf(xi, 0, 0, 3) for xi in x]),
                ('Sedang', lambda x: [trimf(xi, 1, 3.5, 6) for xi in x]),
                ('Tinggi', lambda x: [trimf(xi, 4, 10, 10) for xi in x])
            ], 'title': 'Bahan Organik', 'xlabel': 'Bahan Organik (%)', 'filename': 'organic_matter_membership'
        },
        {
            'name': 'Quality', 'range': (0, 100), 'mfs': [
                ('Buruk', lambda x: [trimf(xi, 0, 0, 50) for xi in x]),
                ('Sedang', lambda x: [trimf(xi, 20, 50, 80) for xi in x]),
                ('Baik', lambda x: [trimf(xi, 50, 100, 100) for xi in x])
            ], 'title': 'Kualitas Tanah', 'xlabel': 'Skor Kualitas', 'filename': 'quality_membership'
        }
    ]
    
    # Plot individual membership functions
    for param in mf_params:
        x = np.linspace(param['range'][0], param['range'][1], 1000)
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for label, mf_func in param['mfs']:
            y = mf_func(x)
            ax.plot(x, y, label=label, linewidth=2)
        
        ax.set_title(param['title'], fontsize=14, fontweight='bold')
        ax.set_xlabel(param['xlabel'], fontsize=12)
        ax.set_ylabel('Derajat Keanggotaan', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        plt.tight_layout()
        plt.savefig(f"output/manual/{param['filename']}.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    # Plot summary
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Sistem Fuzzy Mamdani - Evaluasi Kualitas Tanah (Manual)', fontsize=16, fontweight='bold')
    
    for i, param in enumerate(mf_params):
        row, col = i // 3, i % 3
        x = np.linspace(param['range'][0], param['range'][1], 1000)
        
        for label, mf_func in param['mfs']:
            y = mf_func(x)
            axes[row, col].plot(x, y, label=label, linewidth=2)
        
        axes[row, col].set_title(param['title'], fontsize=12, fontweight='bold')
        axes[row, col].grid(True, alpha=0.3)
        axes[row, col].legend(fontsize=8)
    
    # Add rules info
    axes[1, 2].axis('off')
    axes[1, 2].text(0.1, 0.5, 
                   'Aturan Fuzzy:\n\n'
                   '1. pH Normal ∧ Nutrisi Tinggi ∧ Logam Rendah → Baik\n'
                   '2. pH (Asam ∨ Basa) ∧ Nutrisi Rendah ∧ Logam Tinggi → Buruk\n'
                   '3. pH Normal ∧ Nutrisi Sedang ∧ Logam Sedang → Sedang\n'
                   '4. Bahan Organik Tinggi → Baik\n'
                   '5. Bahan Organik Rendah ∧ Logam Tinggi → Buruk\n'
                   '6. pH Normal ∧ Nutrisi Tinggi ∧ Logam Sedang → Sedang\n\n'
                   'Implementasi Manual\n'
                   'Agil Ghani Istikmal (5220411040)',
                   fontsize=10, transform=axes[1, 2].transAxes,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('output/manual/all_membership_functions.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Gambar membership functions berhasil disimpan di output/manual/")

def main():
    print("SISTEM FUZZY MAMDANI - EVALUASI KUALITAS TANAH")
    print("Implementasi Manual (Tanpa Library)")
    print()
    
    # Create output folder
    if not os.path.exists('output/manual'):
        os.makedirs('output/manual')
    
    # Plot membership functions
    plot_membership_functions()
    
    # Read data
    try:
        df = pd.read_csv('data.csv')
        results = []
        
        for idx, row in df.iterrows():
            score, category = evaluate(row['pH'], row['Nutrisi'], row['Logam_Berat'], row['Bahan_Organik'])
            results.append([row['No'], f"{row['pH']:.1f}", f"{row['Nutrisi']:.0f}", 
                          f"{row['Logam_Berat']:.0f}", f"{row['Bahan_Organik']:.0f}", 
                          f"{score:.1f}", category])
        
        # Display results
        headers = ["No", "pH", "Nutrisi", "Logam Berat", "Bahan Organik", "Skor", "Kualitas"]
        print(pd.DataFrame(results, columns=headers).to_string(index=False))
        
        print(f"\nDibuat Oleh: Agil Ghani Istikmal (5220411040)")
        print("Keterangan: 0-40=Buruk, 40-70=Sedang, 70-100=Baik")
        print("Gambar tersimpan di folder output/manual/")
        
    except FileNotFoundError:
        print("Error: File data.csv tidak ditemukan!")

if __name__ == "__main__":
    main()
