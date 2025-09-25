import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import random

# Configuration de la page
st.set_page_config(
    page_title="SportsDynamics - Mercato Recrutement",
    page_icon="⚽",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.golden-card {
    background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
    padding: 1.5rem;
    border-radius: 15px;
    color: #333;
    margin: 1rem 0;
    box-shadow: 0 8px 32px rgba(255,215,0,0.3);
    border: 3px solid #ff6b35;
}

.regular-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 15px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    text-align: center;
    border-left: 4px solid #1e3c72;
}
</style>
""", unsafe_allow_html=True)

# Données des candidats
@st.cache_data
def get_candidates():
    return pd.DataFrame([
        {
            "nom": "Candidat Star", "prenom": "TOI", "age": 23, "ville": "Paris",
            "formation": "Master Data Science", "ecole": "École d'Ingénieur",
            "python": 90, "ml": 85, "sports_analytics": 95, "aws": 80, "anglais": 88,
            "football_passion": 98, "experience": 75, "overall": 87,
            "poste": "Data Scientist", "specialite": "Sports Analytics", "is_you": True
        },
        {
            "nom": "Dupont", "prenom": "Alexandre", "age": 24, "ville": "Lyon",
            "formation": "Master IA", "ecole": "Université Lyon 1",
            "python": 82, "ml": 78, "sports_analytics": 70, "aws": 75, "anglais": 82,
            "football_passion": 85, "experience": 65, "overall": 76,
            "poste": "Data Scientist", "specialite": "Machine Learning", "is_you": False
        },
        {
            "nom": "Martin", "prenom": "Sophie", "age": 22, "ville": "Marseille",
            "formation": "Master Statistiques", "ecole": "Aix-Marseille Université",
            "python": 88, "ml": 82, "sports_analytics": 65, "aws": 70, "anglais": 90,
            "football_passion": 75, "experience": 68, "overall": 77,
            "poste": "Data Analyst", "specialite": "Statistiques", "is_you": False
        },
        {
            "nom": "Leroy", "prenom": "Julien", "age": 25, "ville": "Lille",
            "formation": "Master Informatique", "ecole": "Centrale Lille",
            "python": 85, "ml": 80, "sports_analytics": 85, "aws": 85, "anglais": 78,
            "football_passion": 92, "experience": 72, "overall": 82,
            "poste": "Data Engineer", "specialite": "Cloud & Analytics", "is_you": False
        }
    ])

# Navigation principale
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏆 SPORTSDYNAMICS - MERCATO RECRUTEMENT 🏆</h1>
        <h3>⚽ Centre de Recrutement des Talents Data Science ⚽</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 Accueil", 
        "🗺️ Scouting", 
        "⚖️ Comparaison", 
        "🏆 Classement", 
        "📊 Analytics"
    ])
    
    df = get_candidates()
    
    with tab1:
        accueil_page(df)
    
    with tab2:
        scouting_page(df)
    
    with tab3:
        comparaison_page(df)
    
    with tab4:
        classement_page(df)
        
    with tab5:
        analytics_page(df)

def accueil_page(df):
    st.markdown("## 🎯 Tableau de Bord - Mercato SportsDynamics")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊</h3>
            <h2>5</h2>
            <p>Candidats Analysés</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⭐</h3>
            <h2>{df['overall'].mean():.1f}</h2>
            <p>Note Moyenne</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        experts = len(df[df['sports_analytics'] >= 85])
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯</h3>
            <h2>{experts}</h2>
            <p>Experts Sports Analytics</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        max_passion = df['football_passion'].max()
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚽</h3>
            <h2>{max_passion}</h2>
            <p>Max Passion Football</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Top 3 candidats
    st.markdown("### ⭐ Podium des Meilleurs Candidats")
    
    top3 = df.nlargest(3, 'overall')
    cols = st.columns(3)
    
    medals = ["🥇", "🥈", "🥉"]
    
    for i, (_, candidate) in enumerate(top3.iterrows()):
        with cols[i]:
            card_type = "golden-card" if candidate['is_you'] else "regular-card"
            
            st.markdown(f"""
            <div class="{card_type}">
                <h3 style="text-align: center;">{medals[i]} {candidate['prenom']} {candidate['nom']}</h3>
                <h1 style="text-align: center; font-size: 48px; margin: 10px 0;">{candidate['overall']}</h1>
                <p style="text-align: center;"><strong>{candidate['specialite']}</strong></p>
                <p style="text-align: center;">{candidate['ville']} • {candidate['age']} ans</p>
                
                <div style="margin-top: 15px;">
                    <p><strong>🐍 Python:</strong> {candidate['python']}/100</p>
                    <p><strong>🎯 Sports Analytics:</strong> {candidate['sports_analytics']}/100</p>
                    <p><strong>⚽ Passion Football:</strong> {candidate['football_passion']}/100</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

def scouting_page(df):
    st.markdown("## 🗺️ Scouting Géographique")
    
    # Filtres interactifs
    st.markdown("### 🔍 Filtres de Recherche")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        villes_selected = st.multiselect(
            "🏙️ Ville:",
            options=df['ville'].unique(),
            default=df['ville'].unique()
        )
    
    with col2:
        min_overall = st.slider(
            "📊 Note minimum:",
            min_value=0,
            max_value=100,
            value=70
        )
    
    with col3:
        specialites_selected = st.multiselect(
            "🎯 Spécialité:",
            options=df['specialite'].unique(),
            default=df['specialite'].unique()
        )
    
    # Filtrage des données
    df_filtered = df[
        (df['ville'].isin(villes_selected)) &
        (df['overall'] >= min_overall) &
        (df['specialite'].isin(specialites_selected))
    ]
    
    st.markdown(f"### 📋 {len(df_filtered)} Candidat(s) Trouvé(s)")
    
    # Affichage des candidats filtrés
    for _, candidate in df_filtered.iterrows():
        card_type = "golden-card" if candidate['is_you'] else "regular-card"
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div class="{card_type}">
                <h4>{'🌟 ' if candidate['is_you'] else ''}👤 {candidate['prenom']} {candidate['nom']}</h4>
                <p><strong>📍</strong> {candidate['ville']} | <strong>🎓</strong> {candidate['formation']}</p>
                <p><strong>🏫</strong> {candidate['ecole']}</p>
                <p><strong>⚽</strong> Passion Football: {candidate['football_passion']}/100 | <strong>🎯</strong> Sports Analytics: {candidate['sports_analytics']}/100</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric("Overall", f"{candidate['overall']}/100")

def comparaison_page(df):
    st.markdown("## ⚖️ Comparaison des Candidats")
    
    # Sélection des candidats
    col1, col2 = st.columns(2)
    
    candidates_list = [f"{row['prenom']} {row['nom']}" for _, row in df.iterrows()]
    
    with col1:
        candidat1 = st.selectbox("👤 Candidat 1:", candidates_list, index=0)
    
    with col2:
        candidat2 = st.selectbox("👤 Candidat 2:", candidates_list, index=1)
    
    # Récupération des données
    c1 = df[df.apply(lambda x: f"{x['prenom']} {x['nom']}" == candidat1, axis=1)].iloc[0]
    c2 = df[df.apply(lambda x: f"{x['prenom']} {x['nom']}" == candidat2, axis=1)].iloc[0]
    
    # Cartes des candidats
    col1, col2 = st.columns(2)
    
    with col1:
        card_type1 = "golden-card" if c1['is_you'] else "regular-card"
        st.markdown(f"""
        <div class="{card_type1}" style="text-align: center;">
            <h3>{c1['prenom']} {c1['nom']}</h3>
            <h1 style="font-size: 48px; margin: 10px 0;">{c1['overall']}</h1>
            <p><strong>{c1['poste']}</strong></p>
            <p>{c1['ville']} • {c1['age']} ans</p>
            <hr>
            <p><strong>🐍 Python:</strong> {c1['python']}</p>
            <p><strong>🤖 ML:</strong> {c1['ml']}</p>
            <p><strong>🎯 Sports Analytics:</strong> {c1['sports_analytics']}</p>
            <p><strong>☁️ AWS:</strong> {c1['aws']}</p>
            <p><strong>🗣️ Anglais:</strong> {c1['anglais']}</p>
            <p><strong>⚽ Passion:</strong> {c1['football_passion']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        card_type2 = "golden-card" if c2['is_you'] else "regular-card"
        st.markdown(f"""
        <div class="{card_type2}" style="text-align: center;">
            <h3>{c2['prenom']} {c2['nom']}</h3>
            <h1 style="font-size: 48px; margin: 10px 0;">{c2['overall']}</h1>
            <p><strong>{c2['poste']}</strong></p>
            <p>{c2['ville']} • {c2['age']} ans</p>
            <hr>
            <p><strong>🐍 Python:</strong> {c2['python']}</p>
            <p><strong>🤖 ML:</strong> {c2['ml']}</p>
            <p><strong>🎯 Sports Analytics:</strong> {c2['sports_analytics']}</p>
            <p><strong>☁️ AWS:</strong> {c2['aws']}</p>
            <p><strong>🗣️ Anglais:</strong> {c2['anglais']}</p>
            <p><strong>⚽ Passion:</strong> {c2['football_passion']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphique radar
    st.markdown("### 📊 Comparaison Radar")
    
    skills = ['python', 'ml', 'sports_analytics', 'aws', 'anglais', 'football_passion']
    skill_labels = ['Python', 'ML', 'Sports Analytics', 'AWS', 'Anglais', 'Passion Football']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[c1[skill] for skill in skills],
        theta=skill_labels,
        fill='toself',
        name=f"{c1['prenom']} {c1['nom']}",
        line_color='orange' if c1['is_you'] else 'blue'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[c2[skill] for skill in skills],
        theta=skill_labels,
        fill='toself',
        name=f"{c2['prenom']} {c2['nom']}",
        line_color='orange' if c2['is_you'] else 'red'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def classement_page(df):
    st.markdown("## 🏆 Classement Général")
    
    # Classement par overall
    df_sorted = df.sort_values('overall', ascending=False).reset_index(drop=True)
    
    st.markdown("### 🎖️ Ranking Officiel SportsDynamics")
    
    for i, (_, candidate) in enumerate(df_sorted.iterrows()):
        rang = i + 1
        
        # Définir les couleurs et icônes
        if rang == 1:
            icon = "🥇"
            color = "#FFD700"
        elif rang == 2:
            icon = "🥈"
            color = "#C0C0C0"
        elif rang == 3:
            icon = "🥉"
            color = "#CD7F32"
        else:
            icon = f"#{rang}"
            color = "#666"
        
        card_type = "golden-card" if candidate['is_you'] else "regular-card"
        
        st.markdown(f"""
        <div class="{card_type}">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center;">
                    <div style="background: {color}; color: {'black' if rang <= 3 else 'white'}; 
                         width: 50px; height: 50px; border-radius: 50%; 
                         display: flex; align-items: center; justify-content: center; 
                         font-weight: bold; font-size: 18px; margin-right: 20px;">
                        {icon}
                    </div>
                    <div>
                        <h4 style="margin: 0;">{'🌟 ' if candidate['is_you'] else ''}{candidate['prenom']} {candidate['nom']}</h4>
                        <p style="margin: 0;">{candidate['specialite']} • {candidate['ville']}</p>
                    </div>
                </div>
                <div style="text-align: center;">
                    <h2 style="margin: 0; font-size: 32px;">{candidate['overall']}</h2>
                    <p style="margin: 0; font-size: 12px;">OVERALL</p>
                </div>
                <div style="display: flex; gap: 20px;">
                    <div style="text-align: center;">
                        <div style="font-weight: bold;">{candidate['sports_analytics']}</div>
                        <div style="font-size: 10px;">SPORTS</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-weight: bold;">{candidate['python']}</div>
                        <div style="font-size: 10px;">PYTHON</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-weight: bold;">{candidate['football_passion']}</div>
                        <div style="font-size: 10px;">PASSION</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def analytics_page(df):
    st.markdown("## 📊 Analytics Avancées")
    
    # Métriques avancées
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🏆 Podium Overall")
        top3 = df.nlargest(3, 'overall')
        for i, (_, c) in enumerate(top3.iterrows()):
            medal = ["🥇", "🥈", "🥉"][i]
            st.write(f"{medal} {c['prenom']} {c['nom']} ({c['overall']})")
    
    with col2:
        st.markdown("#### 🎯 Top Sports Analytics")
        top_sports = df.nlargest(3, 'sports_analytics')
        for _, c in top_sports.iterrows():
            st.write(f"⚽ {c['prenom']} {c['nom']} ({c['sports_analytics']})")
    
    with col3:
        st.markdown("#### 💚 Plus Passionnés")
        top_passion = df.nlargest(3, 'football_passion')
        for _, c in top_passion.iterrows():
            st.write(f"❤️ {c['prenom']} {c['nom']} ({c['football_passion']})")
    
    # Distribution des compétences
    st.markdown("### 📊 Distribution des Compétences")
    
    skills_data = []
    skills = ['python', 'ml', 'sports_analytics', 'aws', 'anglais', 'football_passion']
    
    for skill in skills:
        for _, candidate in df.iterrows():
            skills_data.append({
                'Compétence': skill.replace('_', ' ').title(),
                'Score': candidate[skill],
                'Candidat': f"{candidate['prenom']} {candidate['nom']}",
                'IsYou': candidate['is_you']
            })
    
    skills_df = pd.DataFrame(skills_data)
    
    fig = px.box(skills_df, x='Compétence', y='Score', 
                 color='IsYou',
                 color_discrete_map={True: 'orange', False: 'blue'})
    fig.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommandation finale
    st.markdown("---")
    st.markdown("### 🎯 Recommandation Système SportsDynamics")
    
    # Calcul score pondéré pour SportsDynamics
    weights = {
        'sports_analytics': 0.3,
        'python': 0.25,
        'football_passion': 0.2,
        'ml': 0.15,
        'aws': 0.1
    }
    
    df['score_sportsdynamics'] = (
        df['sports_analytics'] * weights['sports_analytics'] +
        df['python'] * weights['python'] +
        df['football_passion'] * weights['football_passion'] +
        df['ml'] * weights['ml'] +
        df['aws'] * weights['aws']
    ).round(1)
    
    best_candidate = df.loc[df['score_sportsdynamics'].idxmax()]
    
    st.markdown(f"""
    <div class="{'golden-card' if best_candidate['is_you'] else 'regular-card'}" style="text-align: center; padding: 2rem;">
        <h3>🏆 CANDIDAT RECOMMANDÉ POUR SPORTSDYNAMICS</h3>
        <h2>{'🌟 ' if best_candidate['is_you'] else ''}{best_candidate['prenom']} {best_candidate['nom']}</h2>
        <div style="font-size: 48px; font-weight: bold; margin: 1rem 0;">
            {best_candidate['score_sportsdynamics']:.1f}/100
        </div>
        <p style="font-size: 18px;">
            <strong>Spécialité:</strong> {best_candidate['specialite']}<br>
            <strong>Ville:</strong> {best_candidate['ville']}<br>
            <strong>Formation:</strong> {best_candidate['formation']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    ---
    ## 📞 Prêt pour l'entretien ?
    
    **Cette application de recrutement interactive vous a convaincus ?**
    
    🎯 **Objectif :** Démontrer ma capacité à créer des solutions innovantes  
    ⚽ **Passion :** Sports Analytics et Football  
    💻 **Compétences :** Python, Streamlit, Data Viz, et plus !
    
    **Contactez-moi pour un entretien :**
    - 📧 [votre.email@example.com]
    - 🔗 [LinkedIn]
    - 💼 [Portfolio GitHub]
    
    *Application développée spécialement pour SportsDynamics - Mercato 2025* ⚽
    """)

if __name__ == "__main__":
    main()