from repository import lister_interventions

interventions = lister_interventions()

print("Nombre :", len(interventions))
print("Premier ID :", interventions[0]["id"])
print("Dernier ID :", interventions[-1]["id"])