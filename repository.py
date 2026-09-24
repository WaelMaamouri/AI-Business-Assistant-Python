from database import get_connection

def enregistrer_intervention(intervention):
    conn = get_connection()
    
    try:
        with conn.cursor() as cur:
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
                    action)
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )
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
        
    finally:
        conn.close()
        
def lister_interventions():
    conn = get_connection()
    
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    id,
                    client,
                    ville,
                    type,
                    priorite,
                    duree,
                    probleme,
                    action
                FROM interventions
                ORDER BY id
                """
            )
            
            rows = cur.fetchall()
                   
            return  [
                {       "id": row[0],
                        "client": row[1],
                        "ville": row[2],
                        "type": row[3],
                        "priorite": row[4],
                        "duree": row[5],
                        "probleme": row[6],
                        "action": row[7],
                }
                for row in rows
            ]
            
        conn.commit()
        
    finally:
        conn.close()
        
def trouver_intervention(id):
    conn = get_connection()
    
    try:
        with conn.cursor() as cur:
            cur.execute(            
                """
                SELECT 
                    id,
                    client,
                    ville,
                    type,
                    priorite,
                    duree,
                    probleme,
                    action
                FROM interventions
                WHERE id = %s
                """,
                (id,)
            )
            
            row = cur.fetchone()
            
            if row is None:
                return None
        
            return {
                "id": row[0],
                "client": row[1],
                "ville": row[2],
                "type": row[3],
                "priorite": row[4],
                "duree": row[5],
                "probleme": row[6],
                "action": row[7],
                }
            
    finally:
        conn.close()
        
def generate_id():
    conn = get_connection()
    
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COALESCE(MAX(id), 0) + 1
                FROM interventions
                """
            )
            
            return cur.fetchone()[0]
    finally:
        conn.close()