# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 09:45:27 2025

@author: DELL
"""
import streamlit as st
import pandas as pd
import os

# Nom du fichier CSV
FICHIER = "memorypiece.csv"

# Charger les données si le fichier existe
if os.path.exists(FICHIER):
    st.session_state["memorypiece"] = pd.read_csv(FICHIER)
else:
    st.session_state["memorypiece"] = pd.DataFrame(columns=["Nom", "Prix", "Quantité"])

st.title("📦 Gestion de pièces détachées")

# Formulaire pour ajouter une pièce
with st.form("ajout_piece"):
    nom = st.text_input("Nom de la pièce")
    prix = st.number_input("Prix de la pièce (DA)", min_value=0.0, format="%.2f")
    quantite = st.number_input("Quantité en stock", min_value=0, step=1)
    submit = st.form_submit_button("➕ Ajouter")

    if submit and nom:
        nouvelle_piece = pd.DataFrame([[nom, prix, quantite]], columns=["Nom", "Prix", "Quantité"])
        st.session_state["memorypiece"] = pd.concat([st.session_state["memorypiece"], nouvelle_piece], ignore_index=True)
        st.session_state["memorypiece"].to_csv(FICHIER, index=False)  # 🔹 Sauvegarde automatique
        st.success(f"✅ {nom} ajouté avec succès !")

# Afficher toutes les pièces
st.subheader("📋 Inventaire")
st.dataframe(st.session_state["memorypiece"], use_container_width=True)

# Suppression d'une pièce
st.subheader("🗑️ Supprimer une pièce")
piece_suppr = st.selectbox("Choisir une pièce à supprimer", st.session_state["memorypiece"]["Nom"].unique())

if st.button("Supprimer"):
    st.session_state["memorypiece"] = st.session_state["memorypiece"][st.session_state["memorypiece"]["Nom"] != piece_suppr]
    st.session_state["memorypiece"].to_csv(FICHIER, index=False)  # 🔹 Mise à jour du CSV
    st.success(f"❌ {piece_suppr} a été supprimée avec succès !")


# Recherche du prix d'une pièce
st.subheader("🔍 Rechercher une pièce")
recherche = st.text_input("Nom de la pièce à rechercher")
if recherche:
    resultats = st.session_state["memorypiece"][st.session_state["memorypiece"]["Nom"].str.contains(recherche, case=False, na=False)]
    if not resultats.empty:
        st.write(resultats)
    else:
        st.warning("❌ Pièce non trouvée.")
