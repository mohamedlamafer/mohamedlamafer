import tkinter as tk
from tkinter import messagebox
import datetime

class Livre:
    def __init__(self, id, titre, auteur, genre, disponible=True):
        self.id = id
        self.titre = titre
        self.auteur = auteur
        self.genre = genre
        self.disponible = disponible

class Etudiant:
    def __init__(self, nom, cne):
        self.nom = nom
        self.cne = cne

class Emprunt:
    def __init__(self, livre, etudiant, date_emprunt):
        self.livre = livre
        self.etudiant = etudiant
        self.date_emprunt = date_emprunt

class Bibliotheque:
    def __init__(self):
        self.livres = []
        self.emprunts = []

    def ajouter_livre(self, livre):
        self.livres.append(livre)

    def supprimer_livre(self, id):
        self.livres = [livre for livre in self.livres if livre.id != id]

    def chercher_livre(self, mot_cle):
        return [livre for livre in self.livres if mot_cle.lower() in livre.titre.lower() or mot_cle.lower() in livre.auteur.lower()]

    def emprunter_livre(self, id_livre, etudiant):
        for livre in self.livres:
            if livre.id == id_livre and livre.disponible:
                livre.disponible = False
                self.emprunts.append(Emprunt(livre, etudiant, datetime.date.today()))
                return True
        return False

    def retourner_livre(self, id_livre):
        for emprunt in self.emprunts:
            if emprunt.livre.id == id_livre:
                emprunt.livre.disponible = True
                self.emprunts.remove(emprunt)
                return True
        return False

class ApplicationTkinter:
    def __init__(self, root):
        self.biblio = Bibliotheque()
        self.root = root
        self.root.title("📚 Système de Gestion de Bibliothèque")
        self.root.geometry("500x400")
        self.menu_principal()

    def menu_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Système de Gestion de Bibliothèque", font=("Helvetica", 16, "bold"),bg="blanched almond").pack(pady=20)

        tk.Button(self.root, text="📖 Ajouter un Livre", command=self.page_ajouter).pack(pady=5)
        tk.Button(self.root, text="🔍 Rechercher un Livre", command=self.page_chercher).pack(pady=5)
        tk.Button(self.root, text="📤 Emprunter un Livre", command=self.page_emprunter).pack(pady=5)
        tk.Button(self.root, text="📥 Retourner un Livre", command=self.page_retourner).pack(pady=5)
        tk.Button(self.root, text="📋 Voir tous les Livres", command=self.afficher_livres).pack(pady=5)

    def page_ajouter(self):
        self.clear_window()

        tk.Label(self.root, text="Ajouter un Livre", font=("Helvetica", 14, "bold")).pack(pady=10)
        entries = {}
        for champ in ["ID", "Titre", "Auteur", "Genre"]:
            tk.Label(self.root, text=champ).pack()
            entries[champ] = tk.Entry(self.root)
            entries[champ].pack()

        def ajouter():
            livre = Livre(
                entries["ID"].get(),
                entries["Titre"].get(),
                entries["Auteur"].get(),
                entries["Genre"].get()
            )
            self.biblio.ajouter_livre(livre)
            messagebox.showinfo("Succès", "Le livre a été ajouté avec succès !")
            self.menu_principal()

        tk.Button(self.root, text="Ajouter", command=ajouter).pack(pady=10)
        tk.Button(self.root, text="Retour", command=self.menu_principal).pack()

    def page_chercher(self):
        self.clear_window()

        tk.Label(self.root, text="Rechercher un Livre", font=("Helvetica", 14, "bold")).pack(pady=10)
        entry = tk.Entry(self.root)
        entry.pack()

        resultats = tk.Text(self.root, height=10)
        resultats.pack()

        def chercher():
            resultats.delete(1.0, tk.END)
            livres = self.biblio.chercher_livre(entry.get())
            for l in livres:
                dispo = "✅" if l.disponible else "❌"
                resultats.insert(tk.END, f"{l.id} - {l.titre} - {l.auteur} [{dispo}]\n")

        tk.Button(self.root, text="Rechercher", command=chercher).pack(pady=5)
        tk.Button(self.root, text="Retour", command=self.menu_principal).pack()

    def page_emprunter(self):
        self.clear_window()

        tk.Label(self.root, text="Emprunter un Livre", font=("Helvetica", 14, "bold")).pack(pady=10)

        entry_id = tk.Entry(self.root)
        entry_nom = tk.Entry(self.root)
        entry_cne = tk.Entry(self.root)

        for label, entry in [("ID du Livre", entry_id), ("Nom de l'Étudiant", entry_nom), ("CNE", entry_cne)]:
            tk.Label(self.root, text=label).pack()
            entry.pack()

        def emprunter():
            etu = Etudiant(entry_nom.get(), entry_cne.get())
            ok = self.biblio.emprunter_livre(entry_id.get(), etu)
            if ok:
                messagebox.showinfo("Succès", "Livre emprunté avec succès.")
            else:
                messagebox.showerror("Erreur", "Le livre n'est pas disponible.")
            self.menu_principal()

        tk.Button(self.root, text="Emprunter", command=emprunter).pack(pady=5)
        tk.Button(self.root, text="Retour", command=self.menu_principal).pack()

    def page_retourner(self):
        self.clear_window()
        tk.Label(self.root, text="Retourner un Livre", font=("Helvetica", 14, "bold")).pack(pady=10)

        entry = tk.Entry(self.root)
        tk.Label(self.root, text="ID du Livre").pack()
        entry.pack()

        def retourner():
            ok = self.biblio.retourner_livre(entry.get())
            if ok:
                messagebox.showinfo("Succès", "Livre retourné avec succès.")
            else:
                messagebox.showerror("Erreur", "Ce livre n’est pas emprunté.")
            self.menu_principal()

        tk.Button(self.root, text="Retourner", command=retourner).pack(pady=5)
        tk.Button(self.root, text="Retour", command=self.menu_principal).pack()

    def afficher_livres(self):
        self.clear_window()
        tk.Label(self.root, text="Liste des Livres", font=("Helvetica", 14, "bold")).pack(pady=10)

        zone = tk.Text(self.root, height=15)
        zone.pack()
        for l in self.biblio.livres:
            dispo = "✅" if l.disponible else "❌"
            zone.insert(tk.END, f"{l.id} - {l.titre} - {l.auteur} - {l.genre} [{dispo}]\n")

        tk.Button(self.root, text="Retour", command=self.menu_principal).pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root["bg"] = "blanched almond"
    app = ApplicationTkinter(root)
    root.mainloop()
