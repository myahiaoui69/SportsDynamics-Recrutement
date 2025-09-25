import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pydeck as pdk
import random
import os
# Configuration de la page
st.set_page_config(
    page_title="DataScience Mercato - SportsDynamics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === TOUT LE CSS CORRIGÉ ===
st.markdown("""
<style>
    /* Reset et styles généraux */
    * {
        margin: 0;
        padding: 0;
        -webkit-box-sizing: border-box;
        box-sizing: border-box;
    }

    .stApp {
        font-family: 'Saira Semi Condensed', sans-serif;
        font-weight: 400;
        background: linear-gradient(135deg, #0a0a2a 0%, #15133E 50%, #2d1b4e 100%);
        min-height: 100vh;
    }
   /* Pour Chrome, Edge, Safari */
        ::-webkit-scrollbar {
            width: 12px;
        }

        ::-webkit-scrollbar-track {
            background: #15133E;
            border-radius: 6px;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #E16136;
            border-radius: 6px;
            border: 3px solid #15133E;
        }

        ::-webkit-scrollbar-thumb:hover {
            background-color: #FF6B35;
        }

        /* Pour Firefox */
        * {
            scrollbar-width: thin;
            scrollbar-color: #E16136 #15133E;
        }

        /* Hack @supports pour forcer Firefox à appliquer couleur au hover */
        @supports (scrollbar-color: auto) {
            *:hover {
                scrollbar-color: #FF6B35 #15133E;
            }
        }

    .main-header {
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        background: linear-gradient(90deg, #E16136, #E16136, #E16136);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Saira Semi Condensed', sans-serif;
        padding: 20px 0;
    }

    .h3
            {
            color: #E16136
            }

    /* === CARTE FIFA AVEC FORME SVG - CORRIGÉ === */
    .fut-card-svg {
        position: relative;
        width: 270px;
        height: 400px;
        margin: 20px auto;
        clip-path: url("#svgPath");
        background: linear-gradient(135deg, #d7d7d9  0%, #d7d7d9 50%, #d7d7d9 100%);
        box-shadow: 0 20px 40px rgb(204 196 193), 
                    0 0 0 2px rgba(255, 215, 0, 0.3); /* Contour interne doré */
        font-family: 'Saira Semi Condensed', sans-serif;
        /* Ajustement pour éviter la coupure */
        padding-bottom: 20px;
    }

    .card-inner {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        /* Ajustement pour la forme */
        padding: 15px 10px 25px 10px;
        box-sizing: border-box;
    }

    /* Partie supérieure de la carte - CORRIGÉ */
    .card-top {
        position: absolute;
        top: 15px;
        left: 10px;
        width: calc(100% - 20px);
        height: 50%;  /* Réduit pour laisser de la place en bas */
        background: linear-gradient(135deg, #E16136 0%, #FF6B35 100%);
        overflow: hidden;
        border-radius: 10px 10px 0 0;
    }
    .player-initials {
    font-size: 4rem;
    font-weight: bold;
    color: #FFD700;
    text-shadow: 3px 3px 6px rgba(0,0,0,0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 100%;
    background: linear-gradient(135deg, rgba(225, 97, 54, 0.3) 0%, rgba(255, 107, 53, 0.2) 100%);
    border-radius: 50%;
    margin: 0 auto;
    }   

    .player-image {
    position: absolute;
    right: 5px;
    bottom: 0;
    z-index: 2;
    height: 85%;
    width: 65%;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    }

            
    .player-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 5px;
    }

    .player-info {
        position: absolute;
        left: 10px;
        bottom: 10px;
        z-index: 3;
        height: 80%;
        width: 30%;
        padding: 0 10px;
        text-align: center;
        text-transform: uppercase;
    }

    .player-rating {
        font-size: 35px;  /* Ajusté */
        font-weight: bold;
        color: #FFD700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        margin-bottom: 8px;
    }

    .player-position {
        font-size: 18px;  /* Ajusté */
        color: #FFFFFF;
        font-weight: bold;
        padding-bottom: 3px;
        margin-bottom: 3px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
    }

    .player-badge {
        font-size: 14px;  /* Ajusté */
        color: #FFFFFF;
        background: #15133E;
        padding: 2px 6px;
        border-radius: 8px;
        margin: 3px 0;
        border: 1px solid #FFD700;
    }

    /* Partie inférieure de la carte - CORRIGÉ */
    .card-bottom {
        position: absolute;
        bottom: 20px;  /* Remonté pour éviter la coupure */
        left: 10px;
        width: calc(100% - 20px);
        height: 42%;  /* Ajusté */
        background: linear-gradient(135deg, #2A2565 0%, #15133E 100%);
        border-radius: 0 0 10px 10px;
        padding: 5px;
        box-sizing: border-box;
    }

    .player-name {
        text-align: center;
        font-size: 20px;  /* Ajusté */
        text-transform: uppercase;
        font-weight: bold;
        color: #FFD700;
        margin: 2px 0 2px 0;  /* Marge réduite */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        line-height: 1.1;
    }

    .player-stats {
        display: flex;
        justify-content: space-around;
        margin: 0 10px;  /* Marge réduite */
        padding-top: 5px;
        border-top: 2px solid #E16136;
    }

    .stats-column {
        width: 48%;
    }

    /* Amélioration de l'affichage des KPI */
    .stat-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 3px;
        padding: 2px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
    }
            
    .stat-item::after {
        content: "";
        position: absolute;
        right: -5px;
        top: 0;
        height: 100%;
        width: 1px;
        background: rgba(255, 255, 255, 0.2);
    }

    .stats-column:last-child .stat-item::after {
        display: none; /* Pas de trait sur la dernière colonne */
    }

    .stat-value {
        font-size: 18px;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
        min-width: 25px;
        text-align: center;
        flex-shrink: 0;
        margin-right: 5px;
        padding: 2px 6px;
        border-radius: 4px;
        background: linear-gradient(135deg, #FF6B35, #E16136);
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

            




    /* Variation de couleur selon le score */
    .stat-value.high { background: linear-gradient(135deg, #FF6B35, #E16136); }
    .stat-value.medium { background: linear-gradient(135deg, #FF8C42, #FF6B35); }
    .stat-value.low { background: linear-gradient(135deg, #FFA500, #FF8C42); }

    .stat-label {
        font-size: 10px;
        color: #FFFFFF;
        text-transform: uppercase;
        font-weight: 600;
        text-align: left;
        flex-grow: 1;
        padding-left: 8px;
    }

    /* Amélioration de la séparation */
    .stat-item::before {
        content: "•";
        color: #FFD700;
        margin-right: 5px;
        font-weight: bold;
    }

    /* SVG caché pour la forme */
    .svg-container {
        position: absolute;
        top: 0;
        left: 0;
        width: 0;
        height: 0;
        overflow: hidden;
    }

    /* Indicateur visuel pour la zone safe */
    .safe-zone {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 30px;
        background: linear-gradient(to top, rgba(21, 19, 62, 0.8), transparent);
        pointer-events: none;
        z-index: 10;
    }
</style>

<!-- SVG POUR LA FORME DE BOUCLIER -->
<svg class="svg-container" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 267.3 427.3">
    <clipPath id="svgPath">
        <path fill="#000" d="M265.3 53.9a33.3 33.3 0 0 1-17.8-5.5 32 32 0 0 1-13.7-22.9c-.2-1.1-.4-2.3-.4-3.4 0-1.3-1-1.5-1.8-1.9a163 163 0 0 0-31-11.6A257.3 257.3 0 0 0 133.7 0a254.9 254.9 0 0 0-67.1 8.7 170 170 0 0 0-31 11.6c-.8.4-1.8.6-1.8 1.9 0 1.1-.2 2.3-.4 3.4a32.4 32.4 0 0 1-13.7 22.9A33.8 33.8 0 0 1 2 53.9c-1.5.1-2.1.4-2 2v293.9c0 3.3 0 6.6.4 9.9a22 22 0 0 0 7.9 14.4c3.8 3.2 8.3 5.3 13 6.8 12.4 3.9 24.8 7.5 37.2 11.5a388.7 388.7 0 0 1 50 19.4 88.7 88.7 0 0 1 25 15.5v.1-.1c7.2-7 16.1-11.3 25-15.5a427 427 0 0 1 50-19.4l37.2-11.5c4.7-1.5 9.1-3.5 13-6.8 4.5-3.8 7.2-8.5 7.9-14.4.4-3.3.4-6.6.4-9.9V231.6 60.5v-4.6c.4-1.6-.3-1.9-1.7-2z"/>
    </clipPath>
</svg>
""", unsafe_allow_html=True)

# === FONCTIONS (identique) ===
def calculate_education_score(education_level):
    levels = {'Bac': 1, 'Bac+2': 2, 'Bac+3': 3, 'Bac+4': 4, 'Bac+5': 5, 'Doctorat': 6}
    return levels.get(education_level, 3)

def calculate_language_score(languages):
    score = 0
    level_bonus = {'A1': 0.1, 'A2': 0.25, 'B1': 0.5, 'B2': 0.75, 'C1': 1, 'C2': 1.5}  # C2 bonus augmenté
    language_weights = {
        'français': 2.0, 'french': 2.0,  # Langue maternelle bonus
        'anglais': 1.5, 'english': 1.5, 
        'espagnol': 1.2, 'spanish': 1.2, 
        'allemand': 1.1, 'german': 1.1
    }
    
    for lang, level in languages.items():
        weight = language_weights.get(lang.lower(), 1.0)
        bonus = level_bonus.get(level, 0.5)
        score += (1 + bonus) * weight
    return min(score, 15)  # Plage étendue pour les multilingues

def calculate_experience_score(experiences):
    total_score = 0
    for exp in experiences:
        duration = exp.get('duration', 0)
        if exp.get('type') == 'alternance':
            total_score += duration / 2
        elif exp.get('type') == 'emploi':
            total_score += duration / 6  # Normalisé pour que 6 ans = 10 points
        else:
            total_score += duration / 12  # Stages normalisés
    return min(total_score, 10)

def calculate_skills_score(skills, weights):
    total = sum(skills[skill] * weight for skill, weight in weights.items() if skill in skills)
    max_possible = sum(100 * weight for weight in weights.values())
    return (total / max_possible) * 100 if max_possible > 0 else 0

# === FONCTION load_extended_data CORRIGÉE ===
def load_extended_data():
    # NOUVEAUX POIDS DES COMPÉTENCES adaptés à votre profil
    skills_weights = {
        'python': 0.15, 'sql': 0.08, 'ml': 0.12, 'deep_learning': 0.10,
        'computer_vision': 0.08, 'nlp': 0.08, 'quantum_computing': 0.06,
        'streamlit': 0.05, 'dash': 0.04, 'qlik_sense': 0.04, 'knime': 0.04,
        'qgis': 0.03, 'postgresql': 0.03, 'sql_server': 0.03, 
        'azure_data_lake': 0.04, 'combinatorial_optimization': 0.03
    }

    positions = ['Data Scientist', 'ML Engineer', 'Data Analyst', 'BI Analyst', 'Data Engineer']
    locations = ['Paris', 'Lyon', 'Lille', 'Marseille', 'Toulouse', 'Remote']
    education_levels = ['Bac+3', 'Bac+4', 'Bac+5', 'Doctorat']
    noms = ['MARTIN', 'DUBOIS', 'CHEN', 'LEROY', 'ROUSSEAU',
            'GARCIA', 'BERTRAND', 'MOREAU', 'FOURNIER', 'LAMBERT']
    prenoms = ['Alex', 'Sarah', 'Thomas', 'Laura', 'Kevin',
               'Marie', 'David', 'Julie', 'Michael', 'Sophie']

    
    candidates = []
    used_names = set()

    for i in range(30):
        # Nom unique
        while True:
            nom = random.choice(noms)
            prenom = random.choice(prenoms)
            fullname = f"{prenom} {nom}"
            if fullname not in used_names:
                used_names.add(fullname)
                break

        position = random.choice(positions)
        location = random.choice(locations)
        education = random.choice(education_levels)

        # PROFILS RÉALISTES POUR LES AUTRES CANDIDATS (2-3 ans d'expérience max)
        if i < 10:  # Juniors
            skills = {
                'python': 70 + (i % 20), 'sql': 65 + (i % 25), 'ml': 60 + (i % 30),
                'deep_learning': 40 + (i % 40), 'computer_vision': 30 + (i % 35),
                'nlp': 35 + (i % 30), 'quantum_computing': 10 + (i % 20),
                'streamlit': 50 + (i % 40), 'dash': 40 + (i % 35), 'qlik_sense': 30 + (i % 40),
                'knime': 45 + (i % 35), 'qgis': 20 + (i % 30), 'postgresql': 60 + (i % 30),
                'sql_server': 55 + (i % 35), 'azure_data_lake': 35 + (i % 40),
                'combinatorial_optimization': 25 + (i % 30)
            }
            sports = 60 + (i * 2)
            experience_duration = random.randint(6, 24)  # 6 mois à 2 ans
        elif i < 25:  # Intermédiaires
            skills = {
                'python': 75 + (i % 15), 'sql': 70 + (i % 20), 'ml': 65 + (i % 25),
                'deep_learning': 50 + (i % 30), 'computer_vision': 45 + (i % 25),
                'nlp': 50 + (i % 20), 'quantum_computing': 20 + (i % 25),
                'streamlit': 60 + (i % 30), 'dash': 50 + (i % 25), 'qlik_sense': 40 + (i % 35),
                'knime': 55 + (i % 25), 'qgis': 30 + (i % 25), 'postgresql': 65 + (i % 25),
                'sql_server': 60 + (i % 30), 'azure_data_lake': 45 + (i % 35),
                'combinatorial_optimization': 35 + (i % 25)
            }
            sports = 70 + (i * 1)
            experience_duration = random.randint(24, 36)  # 2 à 3 ans
        else:  # Seniors légers
            skills = {
                'python': 80 + (i % 10), 'sql': 75 + (i % 15), 'ml': 70 + (i % 20),
                'deep_learning': 60 + (i % 20), 'computer_vision': 55 + (i % 15),
                'nlp': 60 + (i % 15), 'quantum_computing': 30 + (i % 20),
                'streamlit': 70 + (i % 20), 'dash': 60 + (i % 15), 'qlik_sense': 50 + (i % 25),
                'knime': 65 + (i % 15), 'qgis': 40 + (i % 20), 'postgresql': 70 + (i % 20),
                'sql_server': 65 + (i % 25), 'azure_data_lake': 55 + (i % 25),
                'combinatorial_optimization': 45 + (i % 20)
            }
            sports = 80 + (i * 1)
            experience_duration = random.randint(36, 48)  # 3 à 4 ans

        # Limiter les scores à 95 maximum
        skills = {k: min(v, 95) for k, v in skills.items()}

       

        candidate = {
            'id': i + 1,
            'name': fullname,
            'position': position,
            'location': location,
            'education': education,
            'education_score': calculate_education_score(education),
            'languages': {'anglais': random.choice(['B1', 'B2', 'C1'])},  # Pas de C2 pour les autres
            'experiences': [{'type': 'emploi', 'duration': experience_duration}],
            'skills': skills,
            'sports_interest': min(sports, 95),  # Limité à 95
            'description': f'Profil {position} passionné de data et sports'
        }

        candidate['language_score'] = calculate_language_score(candidate['languages'])
        candidate['experience_score'] = calculate_experience_score(candidate['experiences'])
        candidate['skills_score'] = calculate_skills_score(candidate['skills'], skills_weights)

        candidate['overall_score'] = int(
            0.30 * candidate['skills_score'] +
            0.25 * min(candidate['experience_score'] * 10, 100) +
            0.20 * candidate['sports_interest'] +
            0.15 * min(candidate['language_score'] * 10, 100) +
            0.10 * min(candidate['education_score'] * 20, 100)
        )

        candidates.append(candidate)

    # VOTRE PROFIL SURDIMENSIONNÉ
    my_profile = {
        'id': len(candidates) + 1,
        'name': 'Mohamed Yahiaoui',  # Remplacez par votre vrai nom
        'position': 'Data Scientist',
        'location': 'Paris',
        'education': 'Bac+5',
        'education_score': calculate_education_score('Bac+5'),
        'languages': {
            'français': 'C2',  # Langue maternelle
            'anglais': 'B2', 
            'espagnol': 'A2'
        },
        'experiences': [
            {'type': 'emploi', 'duration': 72}  # 6 ANS d'expérience
        ],
        'skills': {
            'python': 90, 'sql': 85, 'ml': 85, 'deep_learning': 80,
            'computer_vision': 75, 'nlp': 90, 'quantum_computing': 60,
            'streamlit': 85, 'dash': 75, 'qlik_sense': 85, 'knime': 95,
            'qgis': 75, 'postgresql': 85, 'sql_server': 70, 
            'azure_data_lake': 70, 'combinatorial_optimization': 70
        },
        'sports_interest': 90,  # Très passionné de sports
        'description': 'Data Scientist passionné avec 6 ans d\'expérience en IA, machine learning et analyse de données. Expert en développement d\'applications data et passionné de sports analytics.',
        'photo': '🧑‍💻',
        'lat': 48.85,
        'lon': 2.35
    }

    my_profile['language_score'] = calculate_language_score(my_profile['languages'])
    my_profile['experience_score'] = calculate_experience_score(my_profile['experiences'])
    my_profile['skills_score'] = calculate_skills_score(my_profile['skills'], skills_weights)
    
    # SCORE SURDIMENSIONNÉ - Votre profil doit dominer
    my_profile['overall_score'] = int(
        0.30 * my_profile['skills_score'] +
        0.30 * min(my_profile['experience_score'] * 10, 100) +  # Poids augmenté pour l'expérience
        0.20 * my_profile['sports_interest'] +
        0.15 * min(my_profile['language_score'] * 10, 100) +
        0.05 * min(my_profile['education_score'] * 20, 100)
    )

    # Garantir que votre score est le plus élevé
    my_profile['overall_score'] = max(95, my_profile['overall_score'])

    candidates.append(my_profile)

    df = pd.DataFrame(candidates).sort_values('overall_score', ascending=False).reset_index(drop=True)
    return df
    
    

# === FONCTION CORRIGÉE POUR LA CARTE ===
# === FONCTION AMÉLIORÉE POUR LES KPI ===
import random

def create_svg_fut_card(candidate):
    """Crée une carte FIFA avec image du candidat - VERSION SIMPLIFIÉE"""

    def get_score_class(score):
        if score >= 80: return "high"
        elif score >= 65: return "medium"
        else: return "low"

    # CORRECTION : Gestion simple des images
    if candidate["photo"].startswith('🧑') or candidate["photo"] == '🧑‍💻':
        # C'est un emoji
        img_content = f'<div style="font-size: 70px; text-align: center; padding-top: 30px;">{candidate["photo"]}</div>'
    else:
        # C'est un chemin d'image - utilisation directe
        img_content = f'<img src="{candidate["photo"]}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 5px;" alt="{candidate["name"]}" />'

    return f"""
    <div class="fut-card-svg">
        <div class="card-inner">
            <div class="card-top">
                <div class="player-image">{img_content}</div>
                <div class="player-info">
                    <div class="player-rating">{candidate['overall_score']}</div>
                    <div class="player-position">DS</div>
                </div>
            </div>
            <div class="card-bottom">
                <div class="player-name">{candidate['name']}</div>
                <div class="player-stats">
                    <div class="stats-column">
                        <div class="stat-item">
                            <span class="stat-value {get_score_class(candidate['skills_score'])}">{candidate['skills_score']:.0f}</span>
                            <span class="stat-label">SKILLS</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-value {get_score_class(candidate['experience_score'] * 10)}">{candidate['experience_score'] * 10:.0f}</span>
                            <span class="stat-label">EXP</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-value {get_score_class(candidate['sports_interest'])}">{candidate['sports_interest']}</span>
                            <span class="stat-label">SPORTS</span>
                        </div>
                    </div>
                    <div class="stats-column">
                        <div class="stat-item">
                            <span class="stat-value {get_score_class(candidate['language_score'] * 10)}">{candidate['language_score'] * 10:.0f}</span>
                            <span class="stat-label">LANG</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-value {get_score_class(candidate['skills']['python'])}">{candidate['skills']['python']}</span>
                            <span class="stat-label">PYTHON</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-value {get_score_class(candidate['skills']['ml'])}">{candidate['skills']['ml']}</span>
                            <span class="stat-label">ML</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """


# Initialisation du session state pour la stabilité des données
if 'stable_data' not in st.session_state:
    # Appeler sans paramètre
    st.session_state.stable_data = load_extended_data()
    st.session_state.stable_data['stable_id'] = range(len(st.session_state.stable_data))

df = st.session_state.stable_data




# === INTERFACE STREAMLIT ===
st.markdown('<div class="main-header">⚽ DATASCIENCE MERCATO 2025 ⚽</div>', unsafe_allow_html=True)
st.markdown('<div class="h3">**SportsDynamics** - Dénichez la prochaine pépite Data Science"</div>', unsafe_allow_html=True)




# === SIDEBAR AMÉLIORÉ ===
st.sidebar.header("🔍 Centre de Recrutement")




# Petite explication simple
st.sidebar.markdown("""
*Utilisez les filtres pour affiner votre recherche de candidats Data Science.*
""")



# Filtres principaux
min_score = st.sidebar.slider("Score global minimum", 0, 100, 0)
sports_interest = st.sidebar.slider("Passion sports minimum", 0, 100, 0)

# Nouveaux filtres
st.sidebar.markdown("---")
st.sidebar.subheader("Filtres avancés")

min_skills = st.sidebar.slider("Compétences techniques minimum", 0, 100, 0)
min_experience = st.sidebar.slider("Expérience minimum", 0, 100, 0)
min_languages = st.sidebar.slider("Langues minimum", 0, 100, 0)



location_filter = st.sidebar.selectbox("Localisation", ['Toutes', 'Paris', 'Lyon', 'Lille', 'Remote'])
position_filter = st.sidebar.multiselect(
    "Poste recherché", 
    ['Data Scientist', 'ML Engineer', 'Data Analyst', 'BI Analyst'],
    default=['Data Scientist', 'ML Engineer']
)

# Filtrage amélioré
# === CORRECTION DU FILTRE ===
# Filtrage amélioré - CORRECTION
filtered_df = df[
    (df['overall_score'] >= min_score) & 
    (df['sports_interest'] >= sports_interest) &
    (df['skills_score'] >= min_skills) &
    ((df['experience_score'] * 10) >= min_experience) &  # CORRECTION : parenthèses
    ((df['language_score'] * 10) >= min_languages)       # CORRECTION : parenthèses
]

if location_filter != 'Toutes':
    filtered_df = filtered_df[filtered_df['location'] == location_filter]

if position_filter:
    filtered_df = filtered_df[filtered_df['position'].isin(position_filter)]




# Afficher le nombre de résultats
st.sidebar.markdown(f"**{len(filtered_df)} candidats trouvés**")



# CORRECTION de la ligne problématique (vers la fin du code) :
tab1, tab2 = st.tabs(["🎴 Cartes des Pépites", "📊 Analyse Comparative",])

with tab1:
    st.markdown("""
    <h2 style="font-size: 3.5rem; text-align: center; margin-bottom: 2rem; font-weight: bold; background: linear-gradient(90deg, #E16136, #E16136, #E16136); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: 'Saira Semi Condensed', sans-serif; padding: 20px 0;">
    🛡️ Cartes des Pépites
    </h2>
    """, unsafe_allow_html=True)
    
    # CSS pour la superposition
    st.markdown("""
    <style>
    .composite-card {
        position: relative;
        width: 270px;
        height: 400px;
        margin: 20px auto;
    }
    .card-base {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
    }
    .image-overlay {
        position: absolute;
        top: 60px;
        right: 20px;
        width: 140px;
        height: 160px;
        z-index: 2;
        border-radius: 8px;
        overflow: hidden;
        border: 2px solid #FFD700;
        box-shadow: 0 5px 20px rgba(0,0,0,0.5);
    }
    .image-overlay img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .fallback-initials {
        background: linear-gradient(135deg, #E16136, #FF6B35);
        color: white;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, (_, candidate) in enumerate(filtered_df.iterrows()):
        with cols[idx % 2]:
            # Initiales pour fallback
            name_parts = candidate['name'].split()
            initials = name_parts[0][0].upper() + (name_parts[1][0].upper() if len(name_parts) > 1 else '')
            
          
            
            # Carte composite
            st.markdown(f"""
            <div class="composite-card">
                <!-- Base de la carte -->
                <div class="card-base">
                    <div class="fut-card-svg">
                        <div class="card-inner">
                            <div class="card-top">
                                <div class="player-image">
                                    <div class="player-initials" style="opacity:0.3;">{initials}</div>
                                </div>
                                <div class="player-info">
                                    <div class="player-rating">{candidate['overall_score']}</div>
                                    <div class="player-position">DS</div>
                                </div>
                            </div>
                            <div class="card-bottom">
                                <div class="player-name">{candidate['name']}</div>
                                <div class="player-stats">
                                    <div class="stats-column">
                                        <div class="stat-item">
                                            <span class="stat-value">{candidate['skills_score']:.0f}</span>
                                            <span class="stat-label">SKILLS</span>
                                        </div>
                                        <div class="stat-item">
                                            <span class="stat-value">{candidate['experience_score'] * 10:.0f}</span>
                                            <span class="stat-label">EXP</span>
                                        </div>
                                        <div class="stat-item">
                                            <span class="stat-value">{candidate['sports_interest']}</span>
                                            <span class="stat-label">SPORTS</span>
                                        </div>
                                    </div>
                                    <div class="stats-column">
                                        <div class="stat-item">
                                            <span class="stat-value">{candidate['language_score'] * 10:.0f}</span>
                                            <span class="stat-label">LANG</span>
                                        </div>
                                        <div class="stat-item">
                                            <span class="stat-value">{candidate['skills']['python']}</span>
                                            <span class="stat-label">PYTHON</span>
                                        </div>
                                        <div class="stat-item">
                                            <span class="stat-value">{candidate['skills']['ml']}</span>
                                            <span class="stat-label">ML</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)



# === MODIFIER UNIQUEMENT LA PARTIE tab3 ===

with tab2:
    st.header("📊 Analyse Comparative - Radar Chart")
    
    # Initialisation du session state pour la sélection
    if 'selected_candidates' not in st.session_state:
        st.session_state.selected_candidates = df['name'].tolist()[:2]
    
    # Créer des IDs stables basés sur l'index du DataFrame
    df_display = df.copy()
    df_display['display_id'] = df_display.index.astype(str) + "_" + df_display['name']
    
    # Options pour le multiselect avec IDs stables
    candidate_options = df_display['display_id'].tolist()
    display_to_name = dict(zip(df_display['display_id'], df_display['name']))
    name_to_display = dict(zip(df_display['name'], df_display['display_id']))
    
    # Convertir la sélection actuelle en format display_id
    current_selection = [name_to_display[name] for name in st.session_state.selected_candidates 
                        if name in name_to_display]
    
    # Container pour stabiliser l'interface
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Multiselect avec key unique pour éviter les conflits
            selected_display_ids = st.multiselect(
                "Choisissez 2 à 3 candidats à comparer",
                options=candidate_options,
                default=current_selection,
                max_selections=3,
                key="candidate_selector",  # Key unique pour cet élément
                help="💡 Sélectionnez jusqu'à 3 candidats. Cliquez une fois pour ajouter/retirer."
            )
        
    
    # Convertir les display_ids en noms
    new_selection = [display_to_name[display_id] for display_id in selected_display_ids 
                    if display_id in display_to_name]
    
    # Mettre à jour le session state seulement si la sélection a changé
    if set(new_selection) != set(st.session_state.selected_candidates):
        st.session_state.selected_candidates = new_selection
        st.rerun()  # Forcer le rerun pour synchroniser l'état
    
    # Afficher la sélection actuelle
    st.info(f"**Candidats sélectionnés ({len(st.session_state.selected_candidates)}/3) :** " +
            ", ".join(st.session_state.selected_candidates))
    
    # Récupérer les données des candidats sélectionnés
    compare_df = df[df['name'].isin(st.session_state.selected_candidates)].copy()
    
    # Affichage conditionnel
    if len(compare_df) >= 2:
        # Radar chart
        fig = go.Figure()
        colors = ['#E16136', '#4ECDC4', '#FFD700']
        
        for i, (_, candidate) in enumerate(compare_df.iterrows()):
            values = [
                candidate['skills_score'],                                           # Déjà entre 0-100
                min(candidate['experience_score'] * 10, 100),                       # Limiter à 100
                candidate['sports_interest'],                                        # Déjà entre 0-100
                min(candidate['language_score'] * 10, 100),                         # Limiter à 100
                min(candidate['education_score'] * 20, 100)                         # Limiter à 100
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=['Compétences', 'Expérience', 'Sports', 'Langues', 'Éducation'] + ['Compétences'],
                fill='toself',
                name=candidate['name'],
                line=dict(color=colors[i], width=3),
                opacity=0.7
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], showline=False, showticklabels=False)
            ),
            showlegend=True,
            height=500,
            legend=dict(bgcolor='rgba(255,255,255,0.9)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau comparatif
        st.subheader("📋 Tableau Comparatif Détaillé")
        comparison_data = []
        for _, candidate in compare_df.iterrows():
            comparison_data.append({
                'Candidat': candidate['name'],
                'Score Global': candidate['overall_score'],
                'Compétences': f"{candidate['skills_score']:.0f}/100",
                'Expérience': f"{candidate['experience_score'] * 10:.0f}/100",
                'Sports': f"{candidate['sports_interest']}/100",
                'Langues': f"{candidate['language_score'] * 10:.0f}/100",
                'Python': f"{candidate['skills']['python']}/100",
                'Machine Learning': f"{candidate['skills']['ml']}/100",
                'Position': candidate['position']
            })
        
        # Afficher le tableau avec style
        st.dataframe(
            pd.DataFrame(comparison_data),
            use_container_width=True,
            hide_index=True
        )
        
    elif len(compare_df) == 1:
        st.warning("⚠️ Sélectionnez au moins un candidat supplémentaire pour la comparaison")
        st.info("💡 La comparaison radar nécessite au moins 2 candidats.")
        
    else:
        st.info("👆 Sélectionnez 2 ou 3 candidats dans la liste déroulante ci-dessus pour commencer la comparaison.")


# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #E16136; font-size: 1.1rem;'>"
           "**SportsDynamics Mercato 2025** - *Votre recrutement, notre science* ⚽</div>", unsafe_allow_html=True)