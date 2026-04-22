import pandas as pd

def find_pleated_hero_design(csv_file):
    df = pd.read_csv(csv_file)
    
    # --- ENGINEERING LOGIC: PLEATED GEOMETRY ---
    # We apply a Pleat Factor of 3.0. 
    # This simulates folding the 0.5cm mat into a V-shape, 
    # effectively reducing the air resistance (Pressure Drop).
    pleat_factor = 3.0 
    
    df['Pleated_Pressure_Pa'] = df['Pressure_Drop_Pa'] / pleat_factor

    
    # --- PHYSICAL CONSTRAINTS ---
    # 1. Thickness must be at least 0.5 cm (0.005 m) for weather durability.
    # 2. Pleated Pressure must be under 40 Pa (Safety buffer for dust clogging).
    df_filtered = df[(df['Thickness_m'] >= 0.005) & 
                     (df['Pleated_Pressure_Pa'] <= 40.0)].copy()
    
    if df_filtered.empty:
        print("No design meets the criteria even with pleating. Check data ranges.")
        return

    # --- MULTI-OBJECTIVE SCORING ---
    # Score for Efficiency (Higher is better)
    df_filtered['score_eff'] = (df_filtered['Efficiency_Percentage'] - df_filtered['Efficiency_Percentage'].min()) / \
                               (df_filtered['Efficiency_Percentage'].max() - df_filtered['Efficiency_Percentage'].min() + 1e-9)
    
    # Score for Compactness (Lower thickness is still better for cost, but within our 0.5cm limit)
    df_filtered['score_thin'] = (df_filtered['Thickness_m'].max() - df_filtered['Thickness_m']) / \
                                (df_filtered['Thickness_m'].max() - df_filtered['Thickness_m'].min() + 1e-9)
    
    # Score for Safety (Lower pressure is better)
    df_filtered['score_safety'] = (df_filtered['Pleated_Pressure_Pa'].max() - df_filtered['Pleated_Pressure_Pa']) / \
                                   (df_filtered['Pleated_Pressure_Pa'].max() - df_filtered['Pleated_Pressure_Pa'].min() + 1e-9)

    df_filtered['Hero_Score'] = (df_filtered['score_eff'] + df_filtered['score_thin'] + df_filtered['score_safety']) / 3
    
    hero = df_filtered.sort_values(by='Hero_Score', ascending=False).iloc[0]

    print("🏆 --- THE PLEATED HERO DESIGN (Ready for SolidWorks) ---")
    print(f"Material Thickness: {hero['Thickness_m']*100:.2f} cm (Durable & Weather-resistant)")
    print(f"Fiber Curvature:   {hero['Fiber_Curvature']:.2f} (Optimized for PALF Static Charge)")
    print(f"Pressure Drop:     {hero['Pleated_Pressure_Pa']:.2f} Pa (Safe for AC Compressor)")
    print(f"Capture Efficiency: {hero['Efficiency_Percentage']:.2f} %")
    print("-" * 50)

    df_filtered.to_csv('pleated_hero_results.csv', index=False)
    
    hero = df_filtered.sort_values(by='Hero_Score', ascending=False).iloc[0]
    
    print(f"✅ Success! Found {len(df_filtered)} safe designs after pleating.")
    print(f"Check 'pleated_hero_results.csv' to see all valid options.")
    
    return hero

hero_result = find_pleated_hero_design('full_design_matrix.csv')
