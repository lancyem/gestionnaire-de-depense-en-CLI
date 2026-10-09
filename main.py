import csv
import os
from datetime import datetime

# Nom du fichier de sauvegarde par défaut
FILE_NAME = "expenses.csv"

# Structure du fichier CSV (En-tête)
FIELDNAMES = ["Date", "Categorie", "Montant", "Description"]


def initialiser_fichier():
    """Crée le fichier CSV avec son en-tête s'il n'existe pas déjà."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def ajouter_depense():
    """Demande les informations à l'utilisateur et enregistre la dépense dans le CSV."""
    print("\n--- Ajouter une nouvelle dépense ---")
    
    # Saisie du montant avec validation
    while True:
        try:
            montant = float(input("Montant (F CFA) : "))
            if montant <= 0:
                print("Le montant doit être supérieur à 0.")
                continue
            break
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    # Choix de la catégorie
    categories = ["Alimentation", "Transport", "Loisirs", "Santé", "Logement", "Autre"]
    print("Catégories disponibles :")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    
    while True:
        try:
            choix_cat = int(input("Choix de la catégorie (numéro) : "))
            if 1 <= choix_cat <= len(categories):
                categorie = categories[choix_cat - 1]
                break
            else:
                print("Numéro invalide.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")

    description = input("Description (optionnel) : ").strip()
    if not description:
        description = "Aucune description"

    date_courante = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Écriture dans le fichier CSV
    with open(FILE_NAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow({
            "Date": date_courante,
            "Categorie": categorie,
            "Montant": f"{montant:.2f}",
            "Description": description
        })

    print(f"✅ Dépense de {montant:.2f} F CFA dans '{categorie}' ajoutée avec succès !")


def charger_depenses():
    """Lit toutes les dépenses sauvegardées dans le fichier CSV."""
    if not os.path.exists(FILE_NAME):
        return []
    
    depenses = []
    with open(FILE_NAME, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            depenses.append({
                "Date": row["Date"],
                "Categorie": row["Categorie"],
                "Montant": float(row["Montant"]),
                "Description": row["Description"]
            })
    return depenses


def afficher_depenses(depenses=None):
    """Affiche une liste de dépenses sous forme de tableau formaté."""
    if depenses is None:
        depenses = charger_depenses()

    if not depenses:
        print("\nℹ️ Aucune dépense enregistrée.")
        return

    print("\n" + "=" * 65)
    print(f"{'Date':<20} | {'Catégorie':<12} | {'Montant (F CFA)':<10} | {'Description'}")
    print("=" * 65)

    total = 0.0
    for d in depenses:
        print(f"{d['Date']:<20} | {d['Categorie']:<12} | {d['Montant']:<10.2f} | {d['Description']}")
        total += d['Montant']

    print("=" * 65)
    print(f"TOTAL : {total:.2f} F CFA\n")


def filtrer_par_categorie():
    """Affiche les dépenses d'une catégorie spécifique choisie par l'utilisateur."""
    depenses = charger_depenses()
    if not depenses:
        print("\nℹ️ Aucune dépense enregistrée.")
        return

    categorie_recherchee = input("\nEntrez la catégorie à filtrer (ex: Alimentation) : ").strip()
    resultats = [d for d in depenses if d['Categorie'].lower() == categorie_recherchee.lower()]

    if resultats:
        print(f"\n🔍 Résultats pour la catégorie '{categorie_recherchee}' :")
        afficher_depenses(resultats)
    else:
        print(f"\n⚠️ Aucune dépense trouvée pour la catégorie '{categorie_recherchee}'.")


def menu_principal():
    """Gère la boucle d'interaction utilisateur."""
    initialiser_fichier()

    while True:
        print("\n" + "—" * 30)
        print("  GESTIONNAIRE DE DÉPENSES ")
        print("—" * 30)
        print("1. Ajouter une dépense")
        print("2. Afficher toutes les dépenses")
        print("3. Filtrer par catégorie")
        print("4. Quitter")

        choix = input("\nChoisissez une option (1-4) : ").strip()

        if choix == "1":
            ajouter_depense()
        elif choix == "2":
            afficher_depenses()
        elif choix == "3":
            filtrer_par_categorie()
        elif choix == "4":
            print("\n👋 Merci d'avoir utilisé le gestionnaire de dépenses. À bientôt !")
            break
        else:
            print("❌ Option invalide, veuillez réessayer.")


if __name__ == "__main__":
    menu_principal()