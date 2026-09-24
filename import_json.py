import json
from database import get_connection

with open("data/resultats.json", "r", encoding="utf-8") as fichier:
    interventions = json.load(fichier)
    
conn = get_connection()

try:
    with conn.cursor() as cur:
        for intervention in interventions:
            cur.execute(
                """
                INSERT INTO interventions (
                    id,
                    client,
                    ville,
                    type,
                    priorite,
                    duree,
                    probleme,
                    action
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        intervention["id"],
                        intervention["client"],
                        intervention["ville"],
                        intervention["type"],
                        intervention["priorite"],
                        intervention["duree"],
                        intervention["probleme"],
                        intervention["action"],
                    )   
            )
        
        conn.commit()
        print("import terminé :", len(interventions), "interventions.")
    
except Exception:
    conn.rollback()
    raise
finally:
    conn.close()