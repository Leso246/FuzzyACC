import pandas as pd

# =============================
# Definizione delle variabili linguistiche
# =============================

weather_conditions = ["bad", "good"];
time_headways = ["dangerous", "short", "adequate", "long", "very_long"];
relative_velocities = [
  "approaching_fast",
  "approaching",
  "steady",
  "moving_away",
  "moving_away_fast",
];

# Termini linguistici possibili per l'accelerazione (elencati a scopo informativo)
# Il campo 'acceleration' andrà compilato manualmente nel CSV generato
acceleration = ["strong_deceleration", 
                "medium_deceleration", 
                "light_deceleration", 
                "zero_acceleration", 
                "light_acceleration", 
                "medium_acceleration", 
                "strong_acceleration"]


# =============================
# Generazione di tutte le combinazioni degli antecedenti
# =============================

combinations = [];

for weather in weather_conditions:
    for time in time_headways:
        for rel in relative_velocities:
            combinations.append(
                {
                    'weather_conditions': weather,
                    'time_headways': time,
                    'relative_velocities': rel,
                    'acceleration': '',
                }
            )

# =============================
# Salvataggio in CSV
# =============================

df = pd.DataFrame(combinations)
df.to_csv("./modello_python/rules.csv", index=False)

print("✅ CSV generato con successo: './modello_python/rules.csv'")
print("👉 Compilare la colonna 'acceleration' scegliendo uno dei seguenti termini:")
for term in acceleration:
    print("   -", term)