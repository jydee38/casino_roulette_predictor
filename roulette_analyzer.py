import customtkinter as ctk
from datetime import datetime

# AJOUT : Définir la mise de base pour chaque pari suggéré
MISE_DE_BASE = 1  # En unités

# --- Logique du jeu ---
ROUGE = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
NOIR = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
COLONNE_1 = {1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34}
COLONNE_2 = {2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35}
COLONNE_3 = {3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36}

MISES_A_SURVEILLER = {
    'Rouge': {'type': 'couleur', 'gain': 1, 'absences_requises': 5},
    'Noir': {'type': 'couleur', 'gain': 1, 'absences_requises': 5},
    'Pair': {'type': 'parite', 'gain': 1, 'absences_requises': 5},
    'Impair': {'type': 'parite', 'gain': 1, 'absences_requises': 5},
    '1-18': {'type': 'moitie', 'gain': 1, 'absences_requises': 5},
    '19-36': {'type': 'moitie', 'gain': 1, 'absences_requises': 5},
    '1ère Douzaine (1-12)': {'type': 'douzaine', 'gain': 2, 'absences_requises': 9},
    '2ème Douzaine (13-24)': {'type': 'douzaine', 'gain': 2, 'absences_requises': 9},
    '3ème Douzaine (25-36)': {'type': 'douzaine', 'gain': 2, 'absences_requises': 9},
    '1ère Colonne': {'type': 'colonne', 'gain': 2, 'absences_requises': 9},
    '2ème Colonne': {'type': 'colonne', 'gain': 2, 'absences_requises': 9},
    '3ème Colonne': {'type': 'colonne', 'gain': 2, 'absences_requises': 9},
}

def obtenir_proprietes(numero):
    if not 0 <= numero <= 36: return None
    proprietes = {}
    if numero in ROUGE: proprietes['couleur'] = 'Rouge'
    elif numero in NOIR: proprietes['couleur'] = 'Noir'
    else: proprietes['couleur'] = 'Zéro'
    if numero == 0: return proprietes
    proprietes['parite'] = 'Pair' if numero % 2 == 0 else 'Impair'
    proprietes['moitie'] = '1-18' if 1 <= numero <= 18 else '19-36'
    if 1 <= numero <= 12: proprietes['douzaine'] = '1ère Douzaine (1-12)'
    elif 13 <= numero <= 24: proprietes['douzaine'] = '2ème Douzaine (13-24)'
    else: proprietes['douzaine'] = '3ème Douzaine (25-36)'
    if numero in COLONNE_1: proprietes['colonne'] = '1ère Colonne'
    elif numero in COLONNE_2: proprietes['colonne'] = '2ème Colonne'
    elif numero in COLONNE_3: proprietes['colonne'] = '3ème Colonne'
    return proprietes

def suggerer_mises_strategie(tirages):
    suggestions_potentielles = []
    for nom_mise, regle in MISES_A_SURVEILLER.items():
        absences_requises, type_mise = regle['absences_requises'], regle['type']
        compteur_absences_reelles = 0
        for numero in reversed(tirages):
            props = obtenir_proprietes(numero)
            if props and props.get(type_mise) == nom_mise:
                break
            else:
                compteur_absences_reelles += 1
        if compteur_absences_reelles >= absences_requises:
            suggestions_potentielles.append({
                "nom": nom_mise,
                "texte": f"Miser sur '{nom_mise}' (absent depuis {compteur_absences_reelles} tours)"
            })
    return suggestions_potentielles

# --- Classe pour l'Interface Graphique (CustomTkinter) ---
class RouletteApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configuration de la fenêtre ---
        self.title("Analyseur de Roulette Pro")
        self.geometry("550x620")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Données de l'application ---
        self.numeros_sortis = []
        self.echecs_suggestions = {}
        self.start_time = None
        self.timer_id = None
        self.gain_total = 0.0
        self.suggestions_precedentes_jouees = []

        # --- Widgets ---
        self.label_titre = ctk.CTkLabel(self, text="Entrez le numéro sorti :", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_titre.pack(pady=(20, 10))

        self.entry_numero = ctk.CTkEntry(self, width=120, height=35, font=ctk.CTkFont(size=16), justify='center')
        self.entry_numero.pack(pady=5)
        self.entry_numero.bind("<Return>", self.ajouter_numero_event)

        self.bouton_ajouter = ctk.CTkButton(self, text="Ajouter Numéro", command=self.ajouter_numero, height=35, font=ctk.CTkFont(size=14, weight="bold"))
        self.bouton_ajouter.pack(pady=10)

        # --- Frame pour les stats (Temps & Gain) ---
        frame_stats = ctk.CTkFrame(self, fg_color="transparent")
        frame_stats.pack(pady=10, fill="x", padx=20)
        # CORRECTION : 'column_configure' devient 'columnconfigure'
        frame_stats.columnconfigure((0, 1), weight=1)

        self.label_temps_jeu = ctk.CTkLabel(frame_stats, text="Temps: 00:00:00", font=ctk.CTkFont(size=14))
        self.label_temps_jeu.grid(row=0, column=0, sticky="w")
        
        self.label_gain = ctk.CTkLabel(frame_stats, text="Gain: 0.00 unités", font=ctk.CTkFont(size=14, weight="bold"))
        self.label_gain.grid(row=0, column=1, sticky="e")

        # --- Affichage des numéros (plus gros) ---
        self.text_numeros = ctk.CTkTextbox(self, height=120, font=ctk.CTkFont(family="Courier", size=26, weight="bold"), wrap="word")
        self.text_numeros.pack(pady=10, padx=20, fill="x")
        self.text_numeros.tag_config("rouge", foreground="#e74c3c")
        self.text_numeros.tag_config("noir", foreground="#d3d3d3")
        self.text_numeros.tag_config("zero", foreground="#2ecc71")
        self.text_numeros.configure(state="disabled")

        # --- Compteur Zéro ---
        self.label_compteur_zero = ctk.CTkLabel(self, text="Tours sans Zéro : 0", font=ctk.CTkFont(size=14))
        self.label_compteur_zero.pack()

        # --- Suggestions ---
        self.label_resultat_titre = ctk.CTkLabel(self, text="Suggestions de mise :", font=ctk.CTkFont(size=16, weight="bold", underline=True))
        self.label_resultat_titre.pack(pady=(20, 5))
        self.label_resultat = ctk.CTkLabel(self, text="En attente de numéros...", font=ctk.CTkFont(size=16), wraplength=480, height=80, justify="left")
        self.label_resultat.pack(pady=5)
        
        # --- Label pour les erreurs ---
        self.label_erreur = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12))
        self.label_erreur.pack()

        # --- Bouton Réinitialiser ---
        self.bouton_reinitialiser = ctk.CTkButton(self, text="Réinitialiser", command=self.reinitialiser, fg_color="#d35400", hover_color="#e67e22")
        self.bouton_reinitialiser.pack(side="bottom", pady=20)

    def ajouter_numero(self):
        if self.start_time is None:
            self.start_time = datetime.now()
            self.mettre_a_jour_temps()

        num_str = self.entry_numero.get()
        try:
            numero = int(num_str)
            if 0 <= numero <= 36:
                self.calculer_gain_perte(numero)
                self.numeros_sortis.append(numero)
                self.mettre_a_jour_affichage()
                self.label_erreur.configure(text="") 
            else:
                self.label_erreur.configure(text="Erreur : Le numéro doit être entre 0 et 36.", text_color="red")
        except ValueError:
            self.label_erreur.configure(text="Erreur : Veuillez entrer un chiffre valide.", text_color="red")
        self.entry_numero.delete(0, ctk.END)
        self.entry_numero.focus_set()

    def calculer_gain_perte(self, numero_sorti):
        if not self.suggestions_precedentes_jouees:
            return

        props_numero = obtenir_proprietes(numero_sorti)
        
        for suggestion in self.suggestions_precedentes_jouees:
            nom_mise = suggestion["nom"]
            regle = MISES_A_SURVEILLER[nom_mise]
            type_mise, gain_multiplicateur = regle['type'], regle['gain']

            if props_numero and props_numero.get(type_mise) == nom_mise:
                self.gain_total += MISE_DE_BASE * gain_multiplicateur
            else:
                self.gain_total -= MISE_DE_BASE
        
        couleur_texte = "lightgreen" if self.gain_total > 0 else "#e74c3c" if self.gain_total < 0 else "white"
        self.label_gain.configure(text=f"Gain: {self.gain_total:.2f} unités", text_color=couleur_texte)

    def mettre_a_jour_temps(self):
        if self.start_time:
            delta = datetime.now() - self.start_time
            total_seconds = int(delta.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            temps_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.label_temps_jeu.configure(text=f"Temps: {temps_str}")
            self.timer_id = self.after(1000, self.mettre_a_jour_temps)

    def ajouter_numero_event(self, event):
        self.ajouter_numero()

    def mettre_a_jour_affichage(self):
        self.text_numeros.configure(state="normal")
        self.text_numeros.delete('1.0', ctk.END)
        for numero in self.numeros_sortis:
            tag = "zero" if numero == 0 else "rouge" if numero in ROUGE else "noir"
            self.text_numeros.insert(ctk.END, f"{numero} ", tag)
        self.text_numeros.see(ctk.END)
        self.text_numeros.configure(state="disabled")

        tours_sans_zero = 0
        for numero in reversed(self.numeros_sortis):
            if numero == 0: break
            tours_sans_zero += 1
        self.label_compteur_zero.configure(text=f"Tours sans Zéro : {tours_sans_zero}")

        suggestions_potentielles = suggerer_mises_strategie(self.numeros_sortis)
        
        suggestions_a_afficher = []
        prochains_echecs = self.echecs_suggestions.copy()
        suggestions_pour_prochain_tour = []
        
        dernier_numero = self.numeros_sortis[-1]
        props_dernier_numero = obtenir_proprietes(dernier_numero)

        for nom_mise in list(prochains_echecs.keys()):
            type_mise = MISES_A_SURVEILLER[nom_mise]['type']
            if props_dernier_numero and props_dernier_numero.get(type_mise) == nom_mise:
                del prochains_echecs[nom_mise]

        for suggestion in suggestions_potentielles:
            nom_mise = suggestion["nom"]
            nb_echecs_actuels = prochains_echecs.get(nom_mise, 0)

            if nb_echecs_actuels < 2:
                suggestions_a_afficher.append(suggestion["texte"])
                suggestions_pour_prochain_tour.append(suggestion)

            prochains_echecs[nom_mise] = nb_echecs_actuels + 1
        
        self.echecs_suggestions = prochains_echecs
        self.suggestions_precedentes_jouees = suggestions_pour_prochain_tour

        if suggestions_a_afficher:
            self.label_resultat.configure(text="\n".join(suggestions_a_afficher), text_color="lightgreen")
        else:
            texte_resultat = "Stop Loss Actif" if suggestions_potentielles else "Aucune opportunité détectée"
            couleur_resultat = "orange" if suggestions_potentielles else "white"
            self.label_resultat.configure(text=texte_resultat, text_color=couleur_resultat)

    def reinitialiser(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.start_time = None
        self.label_temps_jeu.configure(text="Temps: 00:00:00")
        
        self.gain_total = 0.0
        self.suggestions_precedentes_jouees = []
        self.label_gain.configure(text="Gain: 0.00 unités", text_color="white")
        
        self.numeros_sortis, self.echecs_suggestions = [], {}
        self.text_numeros.configure(state="normal")
        self.text_numeros.delete('1.0', ctk.END)
        self.text_numeros.configure(state="disabled")
        self.label_compteur_zero.configure(text="Tours sans Zéro : 0")
        self.label_resultat.configure(text="Réinitialisé. En attente de numéros...", text_color="lightblue")
        self.label_erreur.configure(text="")
        self.entry_numero.focus_set()

# --- Démarrage de l'application ---
if __name__ == "__main__":
    app = RouletteApp()
    app.mainloop()