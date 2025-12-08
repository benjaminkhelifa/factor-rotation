# create_annexe.py
import os
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether,Table, TableStyle, Flowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import cm, mm



styles = getSampleStyleSheet()

style_normal = ParagraphStyle(
    'normal_link',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=11,
    textColor=colors.HexColor("#003366"),
)

style_heading = ParagraphStyle(
    'heading_link',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=11,
    textColor=colors.HexColor("#001F3F"),
    spaceBefore=6,
    spaceAfter=4,
)

style_table_header = ParagraphStyle(
    'table_header',
    parent=styles['Heading3'],
    fontSize=10,
    leading=12,
    textColor=colors.white,
    backColor=colors.HexColor("#003366"),
    alignment=1,  # centered
)

style_bold = ParagraphStyle(
    'GlossaryBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9,
    leading=11,
)
style_normalG = ParagraphStyle(
    'GlossaryNormal',
    parent=styles['Normal'],
    fontSize=9,
    leading=11,
)


REPORT_DIR = "/Users/benjaminvissac/Documents/GitHub/factor-rotation/report"
os.makedirs(REPORT_DIR, exist_ok=True)

glossary_data = [
    ["<b>Analyse de portefeuille</b> ", "Étude globale d’un ensemble d’actifs visant à évaluer la diversification, la corrélation et le profil de risque global."],
    ["<b>Analyse sectorielle ciblée</b> ", "Analyse restreinte à un groupe d’actifs appartenant à un même secteur économique (ex. technologies, énergie), afin d’en mesurer la rotation interne et la cohérence de performance."],
    ["<b>Choppy</b> ", "Terme anglophone désignant un marché irrégulier, sans direction claire, marqué par des variations rapides et contradictoires."],
    ["<b>Divergence prix/momentum</b> ", "Situation où le prix d’un actif continue d’évoluer dans une direction alors que le momentum (vitesse de mouvement) faiblit ou s’inverse, souvent signe de retournement potentiel."],
    ["<b>Effet de short-covering</b> ", "Hausse rapide des prix provoquée par la fermeture simultanée de positions vendeuses, forçant les vendeurs à racheter leurs titres pour limiter leurs pertes."],
    ["<b>Fichier CSV</b>", "Fichier texte structuré contenant des données tabulaires séparées par des virgules. Utilisé ici pour stocker les métadonnées descriptives des actifs (symbole, secteur, etc.). Il est possible dans ce cas d'éditer le fichier directment."],
    ["<b>Fichier Parquet</b>", "Format de fichier binaire optimisé pour le stockage et la lecture rapide de grandes tables de données. Utilisé pour les séries historiques de prix et les profils de volatilité. On passe obligatoirement par pandas pour l'éditer ou équivalent."],
    ["<b>Indice de référence</b>", "Benchmark servant à comparer la performance d’un actif ou d’un portefeuille. Exemples : S&amp;P 500 pour les actions US, MSCI World pour l’allocation globale, Bloomberg Barclays Aggregate pour les obligations, ou CRB Index pour les matières premières."],
    ["<b>Liquidité opérationnelle d’un titre</b>", "Capacité d’un actif à absorber des volumes d’échanges importants sans provoquer de variations excessives de prix. Mesurée par l’indicateur ADV10USD."],
    ["<b>Mean-reversion</b>", "Stratégie consistant à parier sur un retour du prix vers sa moyenne après un excès haussier ou baissier. Opposée aux stratégies de suivi de tendance."],
    ["<b>Newsflow</b>", "Flux d’informations et de publications (résultats, annonces macro, décisions politiques, etc.) susceptibles d’influencer les prix à court terme."],
    ["<b>Over-trading</b>", "Pratique consistant à multiplier les transactions sans justification fondamentale, souvent sous l’effet d’une volatilité excessive ou d’une perte de discipline."],
    ["<b>Pics de volatilité</b>", "Hausse brutale et ponctuelle de la volatilité, souvent liée à un événement exogène (résultats, crise, annonce inattendue)."],
    ["<b>Pullback</b>", "Mouvement de retour temporaire d’un prix vers un ancien niveau de support ou de résistance après une cassure, souvent interprété comme un test de validation du mouvement initial."],
    ["<b>Ratio de Sharpe</b>", "Mesure classique de la performance ajustée du risque : (rendement du portefeuille – taux sans risque) / volatilité. Plus il est élevé, plus le rendement est efficient."],
    ["<b>Rebond technique</b>", "Hausse temporaire d’un actif après une forte baisse, sans changement fondamental de tendance. Résulte souvent d’excès vendeurs ou d’ajustements techniques."],
    ["<b>Réaction sur supports clés</b>", "Comportement des prix autour de niveaux techniques ou psychologiques majeurs (supports ou résistances), souvent utilisés pour détecter un renversement de tendance."],
    ["<b>Risque de breakout</b>", "Risque qu’une cassure de prix au-delà d’un niveau clé échoue ou s’inverse rapidement, provoquant un faux signal et un retour brutal dans le range initial."],
    ["<b>Risque de consolidation / rotation</b>", "Phase durant laquelle les gains se stabilisent ou se redistribuent entre secteurs. Peut précéder une reprise, une correction ou un changement de leadership."],
    ["<b>Risque de retournement imminent</b>", "Situation où plusieurs signaux (momentum, volatilité, signal stability) convergent pour indiquer une probabilité élevée de renversement de tendance à court terme."],
    ["<b>Risques idiosyncratiques</b>", "Risques spécifiques à un actif ou une entreprise, indépendants du marché global (ex. problème de gouvernance, résultat inattendu, événement juridique)."],
    ["<b>Rupture de support</b>", "Cassure d’un niveau technique inférieur important, souvent interprétée comme un signal de faiblesse et de poursuite baissière."],
    ["<b>Secteurs GICS</b>", "Classification mondiale des entreprises selon le Global Industry Classification Standard (GICS), organisée en 11 secteurs principaux (énergie, finance, santé, etc.)."],
    ["<b>Scénario CT</b>", "Configuration de marché à court terme identifiée par le moteur du rapport (ex. Capitulation, Stress, Rally under tension). Basée sur la combinaison Return / Momentum / Volatility."],
    ["<b>Setup de breakout</b>", "Configuration technique annonçant une probable cassure de range ou de résistance, souvent précédée d’une compression de volatilité."],
    ["<b>Squeeze</b>", "Phase où les vendeurs à découvert sont forcés de racheter massivement, entraînant une hausse rapide et auto-entretenue du prix."],
    ["<b>Stock-picking</b>", "Sélection individuelle d’actions sur des critères spécifiques (valeur, croissance, momentum), par opposition à l’investissement indiciel."],
    ["<b>Whipsaws</b>", "Allers-retours rapides de prix invalidant successivement plusieurs signaux techniques, typiques des marchés instables ou latéraux."],
]

glossary_data_en = [
    ["<b>Portfolio analysis</b>", "Comprehensive study of a set of assets aimed at evaluating diversification, correlation, and overall risk profile."],
    ["<b>Targeted sector analysis</b>", "Analysis limited to a group of assets belonging to the same economic sector (e.g., technology, energy) in order to assess internal rotation and performance consistency."],
    ["<b>Choppy</b>", "A term describing an irregular market with no clear direction, marked by fast and contradictory price movements."],
    ["<b>Price/momentum divergence</b>", "A situation where an asset’s price continues to move in one direction while momentum (speed of movement) weakens or reverses; often a sign of a potential trend reversal."],
    ["<b>Short-covering effect</b>", "Rapid price increase caused by the simultaneous closing of short positions, forcing sellers to buy back shares to limit their losses."],
    ["<b>CSV file</b>", "Structured text file containing tabular data separated by commas. Used here to store descriptive metadata about assets (symbol, sector, etc.). In this case, the file can be edited directly."],
    ["<b>Parquet file</b>", "Binary file format optimized for fast storage and reading of large data tables. Used for historical price series and volatility profiles. Must be edited through pandas or an equivalent tool."],
    ["<b>Benchmark index</b>", "Reference index used to compare the performance of an asset or portfolio. Examples: S&amp;P 500 for U.S. equities, MSCI World for global allocation, Bloomberg Barclays Aggregate for bonds, or the CRB Index for commodities."],
    ["<b>Operational liquidity of a security</b>", "An asset’s ability to absorb large trading volumes without causing excessive price variations. Measured by the ADV10USD indicator."],
    ["<b>Mean reversion</b>", "Strategy based on the assumption that prices tend to revert to their mean after excessive upward or downward moves. Opposite of trend-following strategies."],
    ["<b>Newsflow</b>", "Stream of news and announcements (earnings, macro releases, policy decisions, etc.) likely to influence short-term prices."],
    ["<b>Overtrading</b>", "Excessive trading activity without fundamental justification, often driven by high volatility or loss of discipline."],
    ["<b>Volatility spikes</b>", "Sudden and temporary surges in volatility, often triggered by exogenous events (earnings releases, crises, unexpected announcements)."],
    ["<b>Pullback</b>", "Temporary price move back toward a former support or resistance level after a breakout, often interpreted as a test of the initial move."],
    ["<b>Sharpe ratio</b>", "Classic measure of risk-adjusted performance: (portfolio return – risk-free rate) / volatility. The higher it is, the more efficient the return."],
    ["<b>Technical rebound</b>", "Temporary upward movement following a sharp decline, without any fundamental trend change. Often driven by short-term overselling or technical adjustments."],
    ["<b>Reaction on key supports</b>", "Price behavior around major technical or psychological levels (supports or resistances), often used to detect potential reversals."],
    ["<b>Breakout risk</b>", "Risk that a price breakout beyond a key level fails or reverses quickly, producing a false signal and a sharp return to the previous range."],
    ["<b>Consolidation/rotation risk</b>", "Phase during which gains stabilize or rotate between sectors. May precede a rebound, correction, or change in leadership."],
    ["<b>Imminent reversal risk</b>", "Situation where multiple indicators (momentum, volatility, signal stability) converge to signal a high probability of short-term trend reversal."],
    ["<b>Idiosyncratic risks</b>", "Risks specific to an individual asset or company, independent of the overall market (e.g., governance issue, unexpected results, legal event)."],
    ["<b>Support break</b>", "Breakdown below a key technical level, often interpreted as a sign of weakness and continuation of the downward trend."],
    ["<b>GICS sectors</b>", "Global Industry Classification Standard: categorization of companies into 11 main sectors (energy, finance, healthcare, etc.)."],
    ["<b>CT scenario</b>", "Short-term market configuration identified by the report engine (e.g., Capitulation, Stress, Rally under tension). Based on the combination of Return / Momentum / Volatility."],
    ["<b>Breakout setup</b>", "Technical configuration indicating a likely breakout from a range or resistance, often preceded by volatility compression."],
    ["<b>Squeeze</b>", "Phase where short sellers are forced to buy back massively, triggering a fast and self-reinforcing price increase."],
    ["<b>Stock picking</b>", "Selection of individual stocks based on specific criteria (value, growth, momentum), as opposed to index-based investing."],
    ["<b>Whipsaws</b>", "Rapid back-and-forth price swings invalidating multiple technical signals in a row, typical of sideways or unstable markets."],
]

glossary_table = Table(
    [
        [Paragraph(f"<b>{term}</b>", style_bold), Paragraph(definition, style_normalG)]
        for term, definition in glossary_data
    ],
    colWidths=[180, 330],
)
ROW_ALT_1   = colors.Color(1, 1, 1)
ROW_ALT_2   = colors.Color(0.98, 0.98, 0.98)
    
glossary_table.setStyle(TableStyle([
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [ROW_ALT_1, ROW_ALT_2]),
    ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 2),
]))

glossary_table_en = Table(
    [
        [Paragraph(f"<b>{term}</b>", style_bold), Paragraph(definition, style_normalG)]
        for term, definition in glossary_data_en
    ],
    colWidths=[180, 330],
)
ROW_ALT_1   = colors.Color(1, 1, 1)
ROW_ALT_2   = colors.Color(0.98, 0.98, 0.98)
    
glossary_table_en.setStyle(TableStyle([
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [ROW_ALT_1, ROW_ALT_2]),
    ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 2),
]))

data = [
    [Paragraph('<b><a href="#section_objectif">1. Objectif et périmètre</a></b>', style_normal), "1"],
    [Paragraph('<a href="#section_objectifs">1.1 Objectifs</a>', style_normal), "1"],
    [Paragraph('<a href="#section_fichiers_utilises">1.2 Fichiers utilisés</a>', style_normal), "1"],

    [Paragraph('<b><a href="#section_fenetres_frequence">2. Fenêtres & fréquence</a></b>', style_normal), "4"],
    [Paragraph('<a href="#section_fenetres_dynamiques">2.1 Fenêtres dynamiques</a>', style_normal), "4"],
    [Paragraph('<a href="#section_fenetres_objectif">2.2 Objectif</a>', style_normal), "4"],
    [Paragraph('<a href="#section_fenetres_fonctionnement">2.3 Fonctionnement</a>', style_normal), "4"],
    [Paragraph('<a href="#section_fenetres_distinction">2.4 Distinction entre indicateurs</a>', style_normal), "4"],

    [Paragraph('<b><a href="#structure_portfolio">3. Structure de portefeuille et profil macroéconomique</a></b>', style_normal), "5"],
    [Paragraph('<a href="#structure_objectif">3.1 Objectif</a>', style_normal), "5"],
    [Paragraph('<a href="#structure_fonctionnement">3.2 Fonctionnement</a>', style_normal), "5"],
    [Paragraph('<a href="#structure_utilite">3.3 Utilité analytique</a>', style_normal), "5"],
    [Paragraph('<a href="#structure_profile">3.4 Fonctionnement du module Macro Profile Insight</a>', style_normal), "5"],


    [Paragraph('<b><a href="#section_indicateurs">4. Indicateurs clés</a></b>', style_normal), "7"],
    [Paragraph('<a href="#section_return">4.1 Return / R (%)</a>', style_normal), "7"],
    [Paragraph('<a href="#section_volatility">4.2 Volatility / V (%)</a>', style_normal), "8"],
    [Paragraph('<a href="#section_momentum">4.3 Momentum / M (%)</a>', style_normal), "8"],
    [Paragraph('<a href="#section_rar">4.4 Risk-Adjusted Return / RAR</a>', style_normal), "9"],
    [Paragraph('<a href="#section_signal">4.5 Signal stability</a>', style_normal), "10"],
    [Paragraph('<a href="#section_regime">4.6 Volatility regime</a>', style_normal), "10"],
    [Paragraph('<a href="#section_adv10">4.7 ADV10USD (Average Daily Dollar Volume – 10 jours)</a>', style_normal), "11"],

    [Paragraph('<b><a href="#section_comparaison">5. Comparaison CT↔LT</a></b>', style_normal), "12"],
    [Paragraph('<a href="#section_dreturn">5.1 ∆Return (pp) / Variation de rendement</a>', style_normal), "12"],
    [Paragraph('<a href="#section_momentum_ratio">5.2 Momentum Ratio</a>', style_normal), "13"],
    [Paragraph('<a href="#section_volatility_ratio">5.3 Volatility Ratio</a>', style_normal), "14"],
    [Paragraph('<a href="#section_beta">5.4 Bêta</a>', style_normal), "14"],

    [Paragraph('<b><a href="#section_scenarios">6. Scénarios CT</a></b>', style_normal), "16"],
    [Paragraph('<a href="#section_scenarios_objectif">6.1 Objectifs</a>', style_normal), "16"],
    [Paragraph('<a href="#section_scenarios_fonctionnement">6.2 Fonctionnement</a>', style_normal), "16"],
    [Paragraph('<a href="#section_scenarios_classification">6.3 Logique de classification d\'importance</a>', style_normal), "16"],
    [Paragraph('<a href="#section_scenarios_variables">6.4 Valeurs possibles parmi les variables</a>', style_normal), "16"],

    [Paragraph('<b><a href="#section_catalogue">7. Catalogue des scénarios</a></b>', style_normal), "17"],
    [Paragraph('<a href="#section_capitulation">7.1 Capitulation</a>', style_normal), "17"],
    [Paragraph('<a href="#section_stress">7.2 Stress</a>', style_normal), "17"],
    [Paragraph('<a href="#section_squeeze">7.3 Momentum squeeze</a>', style_normal), "17"],
    [Paragraph('<a href="#section_rally">7.4 Rally under tension</a>', style_normal), "17"],
    [Paragraph('<a href="#section_uptrend">7.5 Regular uptrend</a>', style_normal), "17"],
    [Paragraph('<a href="#section_loss_momentum">7.6 Loss of momentum</a>', style_normal), "18"],
    [Paragraph('<a href="#section_rebound">7.7 Technical rebound</a>', style_normal), "18"],
    [Paragraph('<a href="#section_gradual_decline">7.8 Gradual decline</a>', style_normal), "18"],
    [Paragraph('<a href="#section_vol_compress">7.9 Volatility compression</a>', style_normal), "18"],
    [Paragraph('<a href="#section_vol_expand">7.10 Volatility expansion</a>', style_normal), "18"],
    [Paragraph('<a href="#section_stabilizing">7.11 Stabilization after shock</a>', style_normal), "20"],
    [Paragraph('<a href="#section_distribution">7.12 Distribution</a>', style_normal), "20"],
    [Paragraph('<a href="#section_range">7.13 Range / noise</a>', style_normal), "20"],

    [Paragraph('<b><a href="#section_visualisations">8. Visualisations & limites</a></b>', style_normal), "21"],
    [Paragraph('<a href="#section_tickers">8.1 Nombre de tickers</a>', style_normal), "21"],
    [Paragraph('<a href="#section_fenetres_reco">8.2 Recommandations sur les dimensions des fenêtres d\'observation</a>', style_normal), "21"],
    [Paragraph('<a href="#section_resolution">8.3 Résolution temporelle et qualité des données</a>', style_normal), "21"],
    [Paragraph('<a href="#section_biais_frequence">8.4 Biais de fréquence et agrégation</a>', style_normal), "21"],
    [Paragraph('<a href="#section_extremes">8.5 Sensibilité aux valeurs extrêmes</a>', style_normal), "22"],

    [Paragraph('<b><a href="#section_mentions">9. Mentions et précisions</a></b>', style_normal), "22"],
    [Paragraph('<a href="#section_facteurs_echelle">9.1 Facteurs d\'échelle par classe d\'actif</a>', style_normal), "22"],
    [Paragraph('<a href="#section_glossaire">9.2 Glossaire des termes techniques</a>', style_normal), "22"],
]

data_en = [
    [Paragraph('<b><a href="#section_objective_en">1. Objective & Scope</a></b>', style_normal), "1"],
    [Paragraph('<a href="#section_goals_en">1.1 Objectives</a>', style_normal), "1"],
    [Paragraph('<a href="#section_datafiles_en">1.2 Data Files Used</a>', style_normal), "1"],

    [Paragraph('<b><a href="#section_windows_frequency_en">2. Windows & Frequency</a></b>', style_normal), "4"],
    [Paragraph('<a href="#section_dynamic_windows_en">2.1 Dynamic Windows</a>', style_normal), "4"],
    [Paragraph('<a href="#section_windows_goal_en">2.2 Purpose</a>', style_normal), "4"],
    [Paragraph('<a href="#section_windows_mechanics_en">2.3 Functioning</a>', style_normal), "4"],
    [Paragraph('<a href="#section_windows_distinction_en">2.4 Distinction Between Indicators</a>', style_normal), "4"],

    [Paragraph('<b><a href="#section_portfolio_structure_en">3. Portfolio Structure & Macro Profile</a></b>', style_normal), "5"],
    [Paragraph('<a href="#section_structure_goal_en">3.1 Purpose</a>', style_normal), "5"],
    [Paragraph('<a href="#section_structure_mechanics_en">3.2 Functioning</a>', style_normal), "5"],
    [Paragraph('<a href="#section_structure_usefulness_en">3.3 Analytical Usefulness</a>', style_normal), "5"],
    [Paragraph('<a href="#section_macro_profile_insight_en">3.4 How the Macro Profile Insight Module Works</a>', style_normal), "5"],

    [Paragraph('<b><a href="#section_indicators_en">4. Key Indicators</a></b>', style_normal), "7"],
    [Paragraph('<a href="#section_return_en">4.1 Return / R (%)</a>', style_normal), "7"],
    [Paragraph('<a href="#section_volatility_en">4.2 Volatility / V (%)</a>', style_normal), "8"],
    [Paragraph('<a href="#section_momentum_en">4.3 Momentum / M (%)</a>', style_normal), "8"],
    [Paragraph('<a href="#section_rar_en">4.4 Risk-Adjusted Return / RAR</a>', style_normal), "9"],
    [Paragraph('<a href="#section_signal_stability_en">4.5 Signal Stability</a>', style_normal), "10"],
    [Paragraph('<a href="#section_volatility_regime_en">4.6 Volatility Regime</a>', style_normal), "10"],
    [Paragraph('<a href="#section_adv10_en">4.7 ADV10USD (Average Daily Dollar Volume – 10 days)</a>', style_normal), "11"],

    [Paragraph('<b><a href="#section_comparison_en">5. Short-Term vs Long-Term Comparison</a></b>', style_normal), "12"],
    [Paragraph('<a href="#section_delta_return_en">5.1 ∆Return (pp) / Return Variation</a>', style_normal), "12"],
    [Paragraph('<a href="#section_momentum_ratio_en">5.2 Momentum Ratio</a>', style_normal), "13"],
    [Paragraph('<a href="#section_volatility_ratio_en">5.3 Volatility Ratio</a>', style_normal), "14"],
    [Paragraph('<a href="#section_beta_en">5.4 Beta</a>', style_normal), "14"],

    [Paragraph('<b><a href="#section_scenarios_en">6. Short-Term Scenarios</a></b>', style_normal), "16"],
    [Paragraph('<a href="#section_scenarios_goal_en">6.1 Objectives</a>', style_normal), "16"],
    [Paragraph('<a href="#section_scenarios_mechanics_en">6.2 Functioning</a>', style_normal), "16"],
    [Paragraph('<a href="#section_scenarios_classification_en">6.3 Classification Logic</a>', style_normal), "16"],
    [Paragraph('<a href="#section_scenarios_variables_en">6.4 Possible Variable Values</a>', style_normal), "16"],

    [Paragraph('<b><a href="#section_catalogue_en">7. Scenario Catalogue</a></b>', style_normal), "17"],
    [Paragraph('<a href="#section_capitulation_en">7.1 Capitulation</a>', style_normal), "17"],
    [Paragraph('<a href="#section_stress_en">7.2 Stress</a>', style_normal), "17"],
    [Paragraph('<a href="#section_squeeze_en">7.3 Momentum Squeeze</a>', style_normal), "17"],
    [Paragraph('<a href="#section_rally_en">7.4 Rally Under Tension</a>', style_normal), "17"],
    [Paragraph('<a href="#section_uptrend_en">7.5 Regular Uptrend</a>', style_normal), "17"],
    [Paragraph('<a href="#section_loss_momentum_en">7.6 Loss of Momentum</a>', style_normal), "18"],
    [Paragraph('<a href="#section_rebound_en">7.7 Technical Rebound</a>', style_normal), "18"],
    [Paragraph('<a href="#section_gradual_decline_en">7.8 Gradual Decline</a>', style_normal), "18"],
    [Paragraph('<a href="#section_vol_compress_en">7.9 Volatility Compression</a>', style_normal), "18"],
    [Paragraph('<a href="#section_vol_expand_en">7.10 Volatility Expansion</a>', style_normal), "18"],
    [Paragraph('<a href="#section_stabilizing_en">7.11 Stabilization After Shock</a>', style_normal), "20"],
    [Paragraph('<a href="#section_distribution_en">7.12 Distribution</a>', style_normal), "20"],
    [Paragraph('<a href="#section_range_en">7.13 Range / Noise</a>', style_normal), "20"],

    [Paragraph('<b><a href="#section_visualizations">8. Visualizations & Limitations</a></b>', style_normal), "21"],
    [Paragraph('<a href="#section_tickers_en">8.1 Number of Tickers</a>', style_normal), "21"],
    [Paragraph('<a href="#section_window_recommendations">8.2 Recommendations on Observation Window Dimensions</a>', style_normal), "21"],
    [Paragraph('<a href="#section_resolution_en">8.3 Temporal Resolution & Data Quality</a>', style_normal), "21"],
    [Paragraph('<a href="#section_frequency_bias">8.4 Frequency & Aggregation Biases</a>', style_normal), "21"],
    [Paragraph('<a href="#section_extremes_en">8.5 Sensitivity to Extreme Values</a>', style_normal), "22"],

    [Paragraph('<b><a href="#section_disclaimers">9. Notes & Clarifications</a></b>', style_normal), "22"],
    [Paragraph('<a href="#section_scaling_factors">9.1 Scaling Factors by Asset Class</a>', style_normal), "22"],
    [Paragraph('<a href="#section_glossary">9.2 Glossary of Technical Terms</a>', style_normal), "22"],
]

table = Table(data, colWidths=[12*cm, 3*cm])
table.setStyle(TableStyle([
    ("ALIGN", (1,0), (1,-1), "RIGHT"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#003366")),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("BOTTOMPADDING", (0,0), (-1,-1), 2),
]))

table_en = Table(data_en, colWidths=[12*cm, 3*cm])
table.setStyle(TableStyle([
    ("ALIGN", (1,0), (1,-1), "RIGHT"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#003366")),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("BOTTOMPADDING", (0,0), (-1,-1), 2),
]))

def make_styles():
    styles = getSampleStyleSheet()
    title = ParagraphStyle("TitleCenter", parent=styles["Title"], alignment=TA_CENTER, spaceAfter=12)
    h1    = ParagraphStyle("H1", parent=styles["Heading2"], fontSize=13, leading=16,
                           textColor=colors.HexColor("#004d80"), spaceBefore=12, spaceAfter=6)
    body  = ParagraphStyle("Body", parent=styles["BodyText"], alignment=TA_JUSTIFY, leading=14, spaceAfter=6)
    bullet= ParagraphStyle("Bullet", parent=body, leftIndent=0.5*cm, bulletIndent=0.3*cm, spaceAfter=3)
    return title, h1, body, bullet

def add_page_number(canvas, doc):
    """
    Ajoute le numéro de page en bas à droite de chaque page.
    """
    page_num = canvas.getPageNumber()
    text = f"{page_num}"
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(10.5*cm, 1*cm, text)

def make_annualisation_table():

    # Données
    headers = ["Fréquence", "Rendement annualisé", "Volatilité annualisée"]
    data = [
        [
            "Daily",
            "R<sub>ann</sub> = R<sub>daily</sub> × 252",
            "σ<sub>ann</sub> = σ<sub>daily</sub> × √252"
        ],
        [
            "Weekly",
            "R<sub>ann</sub> = R<sub>weekly</sub> × 52",
            "σ<sub>ann</sub> = σ<sub>weekly</sub> × √52"
        ],
        [
            "Monthly",
            "R<sub>ann</sub> = R<sub>monthly</sub> × 12",
            "σ<sub>ann</sub> = σ<sub>monthly</sub> × √12"
        ],
        [
            "Yearly",
            "— (déjà annualisé)",
            "— (déjà annualisée)"
        ],
    ]

    # Styles de texte
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 9
    base.leading = 12
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    freq_style   = ParagraphStyle("Freq", parent=base, alignment=1, fontName="Helvetica-Bold")
    math_style   = ParagraphStyle("Math", parent=base, alignment=1, fontName="Helvetica-Oblique")

    # Conversion Paragraph
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([
            Paragraph(row[0], freq_style),
            Paragraph(row[1], math_style),
            Paragraph(row[2], math_style),
        ])

    # Largeurs
    col_widths = [30*mm, 70*mm, 70*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Couleurs
    BLUE_HEADER = colors.HexColor("#004d80")
    ALT_BG_1    = colors.Color(0.93, 0.97, 1.00)
    ALT_BG_2    = colors.Color(0.98, 0.98, 0.98)
    TEXT_DARK   = colors.Color(0.20, 0.20, 0.20)

    # Style visuel
    table.setStyle(TableStyle([
        # En-tête
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Bordures
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alternance de couleurs
        ("BACKGROUND", (0,1), (-1,1), ALT_BG_1),
        ("BACKGROUND", (0,2), (-1,2), ALT_BG_2),
        ("BACKGROUND", (0,3), (-1,3), ALT_BG_1),
        ("BACKGROUND", (0,4), (-1,4), ALT_BG_2),

        ("TEXTCOLOR",  (0,1), (-1,-1), TEXT_DARK),
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Marges
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_annualisation_table_en():
    # Data
    headers = ["Frequency", "Annualized Return", "Annualized Volatility"]
    data = [
        [
            "Daily",
            "R<sub>ann</sub> = R<sub>daily</sub> × 252",
            "σ<sub>ann</sub> = σ<sub>daily</sub> × √252"
        ],
        [
            "Weekly",
            "R<sub>ann</sub> = R<sub>weekly</sub> × 52",
            "σ<sub>ann</sub> = σ<sub>weekly</sub> × √52"
        ],
        [
            "Monthly",
            "R<sub>ann</sub> = R<sub>monthly</sub> × 12",
            "σ<sub>ann</sub> = σ<sub>monthly</sub> × √12"
        ],
        [
            "Yearly",
            "— (already annualized)",
            "— (already annualized)"
        ],
    ]

    # Text styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 9
    base.leading = 12
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    freq_style   = ParagraphStyle("Freq", parent=base, alignment=1, fontName="Helvetica-Bold")
    math_style   = ParagraphStyle("Math", parent=base, alignment=1, fontName="Helvetica-Oblique")

    # Convert to Paragraphs
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([
            Paragraph(row[0], freq_style),
            Paragraph(row[1], math_style),
            Paragraph(row[2], math_style),
        ])

    # Column widths
    col_widths = [30*mm, 70*mm, 70*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Colors
    BLUE_HEADER = colors.HexColor("#004d80")
    ALT_BG_1    = colors.Color(0.93, 0.97, 1.00)
    ALT_BG_2    = colors.Color(0.98, 0.98, 0.98)
    TEXT_DARK   = colors.Color(0.20, 0.20, 0.20)

    # Visual style
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Borders
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alternating background
        ("BACKGROUND", (0,1), (-1,1), ALT_BG_1),
        ("BACKGROUND", (0,2), (-1,2), ALT_BG_2),
        ("BACKGROUND", (0,3), (-1,3), ALT_BG_1),
        ("BACKGROUND", (0,4), (-1,4), ALT_BG_2),

        ("TEXTCOLOR",  (0,1), (-1,-1), TEXT_DARK),
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Padding
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_dynamic_windows_table():

    # Données
    headers = ["Fréquence d’analyse", "Fenêtre minimale conseillée", "Fenêtre maximale conseillée", "Justification"]
    data = [
        ["Daily", "15 à 25 observations", "60 à 100 observations", "En deçà de 15 jours, le bruit domine la tendance ; au-delà de 100, la réactivité diminue."],
        ["Weekly", "4 à 8 observations", "20 à 30 observations", "Permet d’observer les cycles intermédiaires sans lisser excessivement les signaux."],
        ["Monthly", "3 à 6 observations", "12 à 18 observations", "Suffisant pour capter les changements de régime macro sans diluer la dynamique."],
        ["Yearly", "2 à 3 observations", "5 à 8 observations", "Destiné aux analyses structurelles de long terme ; au-delà, la réactivité devient trop faible."],
    ]

    # Styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    freq_style   = ParagraphStyle("Freq",   parent=base, alignment=1, fontName="Helvetica-Bold")
    min_style    = ParagraphStyle("Min",    parent=base, alignment=1)
    max_style    = ParagraphStyle("Max",    parent=base, alignment=1)
    just_style   = ParagraphStyle("Just",   parent=base, alignment=0)

    # Conversion Paragraph
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([
            Paragraph(row[0], freq_style),
            Paragraph(row[1], min_style),
            Paragraph(row[2], max_style),
            Paragraph(row[3], just_style),
        ])

    # Largeurs
    col_widths = [25*mm, 38*mm, 38*mm, 90*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Couleurs
    BLUE_HEADER = colors.HexColor("#004d80")
    GREY_LIGHT  = colors.Color(0.96, 0.96, 0.96)
    GREY_DARK   = colors.Color(0.25, 0.25, 0.25)
    ALT_BG_1    = colors.Color(0.93, 0.97, 1.00)
    ALT_BG_2    = colors.Color(0.98, 0.98, 0.98)

    # Style visuel
    table.setStyle(TableStyle([
        # En-tête
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Bordures
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignements
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Alternance de couleurs
        ("BACKGROUND", (0,1), (-1,1), ALT_BG_1),
        ("BACKGROUND", (0,2), (-1,2), ALT_BG_2),
        ("BACKGROUND", (0,3), (-1,3), ALT_BG_1),
        ("BACKGROUND", (0,4), (-1,4), ALT_BG_2),

        ("TEXTCOLOR",  (0,1), (-1,-1), GREY_DARK),

        # Marges
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_dynamic_windows_table_en():
    # Data
    headers = ["Analysis Frequency", "Recommended Minimum Window", "Recommended Maximum Window", "Rationale"]
    data = [
        ["Daily", "15 to 25 observations", "60 to 100 observations", "Below 15 days, noise dominates the trend; beyond 100, responsiveness decreases."],
        ["Weekly", "4 to 8 observations", "20 to 30 observations", "Captures intermediate cycles without over-smoothing signals."],
        ["Monthly", "3 to 6 observations", "12 to 18 observations", "Sufficient to detect macro regime shifts without diluting dynamics."],
        ["Yearly", "2 to 3 observations", "5 to 8 observations", "Intended for long-term structural analyses; beyond this range, responsiveness becomes too low."],
    ]

    # Styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    freq_style   = ParagraphStyle("Freq",   parent=base, alignment=1, fontName="Helvetica-Bold")
    min_style    = ParagraphStyle("Min",    parent=base, alignment=1)
    max_style    = ParagraphStyle("Max",    parent=base, alignment=1)
    just_style   = ParagraphStyle("Just",   parent=base, alignment=0)

    # Conversion Paragraph
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([
            Paragraph(row[0], freq_style),
            Paragraph(row[1], min_style),
            Paragraph(row[2], max_style),
            Paragraph(row[3], just_style),
        ])

    # Column widths
    col_widths = [25*mm, 38*mm, 38*mm, 90*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Colors
    BLUE_HEADER = colors.HexColor("#004d80")
    GREY_LIGHT  = colors.Color(0.96, 0.96, 0.96)
    GREY_DARK   = colors.Color(0.25, 0.25, 0.25)
    ALT_BG_1    = colors.Color(0.93, 0.97, 1.00)
    ALT_BG_2    = colors.Color(0.98, 0.98, 0.98)

    # Visual style
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Borders
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignment
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Alternating colors
        ("BACKGROUND", (0,1), (-1,1), ALT_BG_1),
        ("BACKGROUND", (0,2), (-1,2), ALT_BG_2),
        ("BACKGROUND", (0,3), (-1,3), ALT_BG_1),
        ("BACKGROUND", (0,4), (-1,4), ALT_BG_2),

        ("TEXTCOLOR",  (0,1), (-1,-1), GREY_DARK),

        # Padding
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table


def make_beta_table():

    # Données
    headers = ["Valeur du β", "Label utilisé dans le rapport", "Interprétation"]
    data = [
        ["> 1.5", "very_high-beta", "Actif ultra-sensible au marché, amplifie les mouvements dans les deux sens."],
        ["1.2 – 1.5", "high-beta", "Actif offensif, participe pleinement aux cycles haussiers mais plus vulnérable en correction."],
        ["0.8 – 1.2", "neutral", "Réagit globalement comme le marché, sans biais majeur."],
        ["0.6 – 0.8", "low-beta", "Actif modérément défensif, réagit partiellement aux variations globales."],
        ["< 0.6", "defensive", "Actif protecteur, faible sensibilité aux cycles économiques."],
        ["< 0", "inverse", "Corrélation négative avec le marché, rôle de couverture possible."],
    ]

    # Styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    beta_style   = ParagraphStyle("Beta",   parent=base, alignment=1, fontName="Helvetica-Bold")
    label_style  = ParagraphStyle("Label",  parent=base, alignment=1, fontName="Helvetica-Oblique")
    desc_style   = ParagraphStyle("Desc",   parent=base, alignment=0)

    # Conversion Paragraph
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([
            Paragraph(row[0], beta_style),
            Paragraph(row[1], label_style),
            Paragraph(row[2], desc_style),
        ])

    # Largeurs
    col_widths = [25*mm, 40*mm, 115*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Couleurs
    BLUE_HEADER   = colors.HexColor("#004d80")
    VERY_HIGH_BG  = colors.Color(0.98, 0.88, 0.88)
    VERY_HIGH_TX  = colors.Color(0.70, 0.10, 0.10)
    HIGH_BG       = colors.Color(0.98, 0.93, 0.93)
    HIGH_TX       = colors.Color(0.60, 0.20, 0.20)
    NEUTRAL_BG    = colors.Color(0.96, 0.96, 0.96)
    NEUTRAL_TX    = colors.Color(0.25, 0.25, 0.25)
    LOW_BG        = colors.Color(0.92, 0.98, 0.92)
    LOW_TX        = colors.Color(0.12, 0.45, 0.12)
    DEF_BG        = colors.Color(0.88, 0.96, 0.88)
    DEF_TX        = colors.Color(0.05, 0.45, 0.05)
    INV_BG        = colors.Color(0.90, 0.90, 0.98)
    INV_TX        = colors.Color(0.10, 0.10, 0.60)

    # Styles visuels
    table.setStyle(TableStyle([
        # En-tête
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Bordures
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignements
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Couleurs ligne par ligne
        ("BACKGROUND", (0,1), (-1,1), VERY_HIGH_BG),
        ("TEXTCOLOR",  (0,1), (-1,1), VERY_HIGH_TX),

        ("BACKGROUND", (0,2), (-1,2), HIGH_BG),
        ("TEXTCOLOR",  (0,2), (-1,2), HIGH_TX),

        ("BACKGROUND", (0,3), (-1,3), NEUTRAL_BG),
        ("TEXTCOLOR",  (0,3), (-1,3), NEUTRAL_TX),

        ("BACKGROUND", (0,4), (-1,4), LOW_BG),
        ("TEXTCOLOR",  (0,4), (-1,4), LOW_TX),

        ("BACKGROUND", (0,5), (-1,5), DEF_BG),
        ("TEXTCOLOR",  (0,5), (-1,5), DEF_TX),

        ("BACKGROUND", (0,6), (-1,6), INV_BG),
        ("TEXTCOLOR",  (0,6), (-1,6), INV_TX),

        # Marges
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_beta_table_en():
    # Data
    headers = ["β Value", "Label Used in Report", "Interpretation"]
    data = [
        ["> 1.5", "very_high-beta", "Highly market-sensitive asset; amplifies movements in both directions."],
        ["1.2 – 1.5", "high-beta", "Offensive asset; fully participates in bull cycles but more vulnerable during corrections."],
        ["0.8 – 1.2", "neutral", "Moves broadly in line with the market, with no major bias."],
        ["0.6 – 0.8", "low-beta", "Moderately defensive asset; reacts partially to broad market swings."],
        ["< 0.6", "defensive", "Protective asset with low sensitivity to economic cycles."],
        ["< 0", "inverse", "Negatively correlated with the market; can serve as a potential hedge."],
    ]

    # Styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    beta_style   = ParagraphStyle("Beta",   parent=base, alignment=1, fontName="Helvetica-Bold")
    label_style  = ParagraphStyle("Label",  parent=base, alignment=1, fontName="Helvetica-Oblique")
    desc_style   = ParagraphStyle("Desc",   parent=base, alignment=0)

    # Paragraph conversion
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([
            Paragraph(row[0], beta_style),
            Paragraph(row[1], label_style),
            Paragraph(row[2], desc_style),
        ])

    # Column widths
    col_widths = [25*mm, 40*mm, 115*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Colors
    BLUE_HEADER   = colors.HexColor("#004d80")
    VERY_HIGH_BG  = colors.Color(0.98, 0.88, 0.88)
    VERY_HIGH_TX  = colors.Color(0.70, 0.10, 0.10)
    HIGH_BG       = colors.Color(0.98, 0.93, 0.93)
    HIGH_TX       = colors.Color(0.60, 0.20, 0.20)
    NEUTRAL_BG    = colors.Color(0.96, 0.96, 0.96)
    NEUTRAL_TX    = colors.Color(0.25, 0.25, 0.25)
    LOW_BG        = colors.Color(0.92, 0.98, 0.92)
    LOW_TX        = colors.Color(0.12, 0.45, 0.12)
    DEF_BG        = colors.Color(0.88, 0.96, 0.88)
    DEF_TX        = colors.Color(0.05, 0.45, 0.05)
    INV_BG        = colors.Color(0.90, 0.90, 0.98)
    INV_TX        = colors.Color(0.10, 0.10, 0.60)

    # Visual style
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Borders
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignment
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Row colors
        ("BACKGROUND", (0,1), (-1,1), VERY_HIGH_BG),
        ("TEXTCOLOR",  (0,1), (-1,1), VERY_HIGH_TX),

        ("BACKGROUND", (0,2), (-1,2), HIGH_BG),
        ("TEXTCOLOR",  (0,2), (-1,2), HIGH_TX),

        ("BACKGROUND", (0,3), (-1,3), NEUTRAL_BG),
        ("TEXTCOLOR",  (0,3), (-1,3), NEUTRAL_TX),

        ("BACKGROUND", (0,4), (-1,4), LOW_BG),
        ("TEXTCOLOR",  (0,4), (-1,4), LOW_TX),

        ("BACKGROUND", (0,5), (-1,5), DEF_BG),
        ("TEXTCOLOR",  (0,5), (-1,5), DEF_TX),

        ("BACKGROUND", (0,6), (-1,6), INV_BG),
        ("TEXTCOLOR",  (0,6), (-1,6), INV_TX),

        # Padding
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table


def make_volatility_ratio_table():

    # Données
    headers = ["Ratio", "Interprétation", "Description du contexte"]
    data = [
        ["< 0.5", "Volatility collapsing", "Forte contraction du risque — marché calme ou compression de volatilité."],
        ["0.5 – 0.8", "Volatility compressing", "Réduction progressive de la dispersion — souvent avant un breakout."],
        ["0.8 – 1.2", "Volatility normalizing", "Volatilité stable — marché équilibré."],
        ["1.2 – 1.5", "Volatility expanding", "Hausse de la dispersion — tensions ou stress modéré."],
        ["> 1.5", "Volatility spiking", "Forte expansion — panique, turbulence, ou choc macro."],
    ]

    # Styles de texte
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    ratio_style  = ParagraphStyle("Ratio",  parent=base, alignment=1, fontName="Helvetica-Bold")
    interp_style = ParagraphStyle("Interp", parent=base, alignment=1)
    desc_style   = ParagraphStyle("Desc",   parent=base, alignment=0)

    # Conversion Paragraph
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([
            Paragraph(row[0], ratio_style),
            Paragraph(row[1], interp_style),
            Paragraph(row[2], desc_style),
        ])

    # Largeurs des colonnes
    col_widths = [25*mm, 45*mm, 110*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Couleurs
    BLUE_HEADER   = colors.HexColor("#004d80")
    STRONG_NEG_BG = colors.Color(0.98, 0.88, 0.88)
    STRONG_NEG_TX = colors.Color(0.70, 0.10, 0.10)
    MILD_NEG_BG   = colors.Color(0.98, 0.93, 0.93)
    MILD_NEG_TX   = colors.Color(0.60, 0.20, 0.20)
    NEUTRAL_BG    = colors.Color(0.96, 0.96, 0.96)
    NEUTRAL_TX    = colors.Color(0.25, 0.25, 0.25)
    MILD_POS_BG   = colors.Color(0.92, 0.98, 0.92)
    MILD_POS_TX   = colors.Color(0.12, 0.45, 0.12)
    STRONG_POS_BG = colors.Color(1.00, 0.97, 0.85)
    STRONG_POS_TX = colors.Color(0.55, 0.40, 0.00)

    # Style visuel
    table.setStyle(TableStyle([
        # En-tête
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Bordures
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignements
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Couleurs ligne par ligne
        ("BACKGROUND", (0,1), (-1,1), STRONG_NEG_BG),
        ("TEXTCOLOR",  (0,1), (-1,1), STRONG_NEG_TX),

        ("BACKGROUND", (0,2), (-1,2), MILD_NEG_BG),
        ("TEXTCOLOR",  (0,2), (-1,2), MILD_NEG_TX),

        ("BACKGROUND", (0,3), (-1,3), NEUTRAL_BG),
        ("TEXTCOLOR",  (0,3), (-1,3), NEUTRAL_TX),

        ("BACKGROUND", (0,4), (-1,4), MILD_POS_BG),
        ("TEXTCOLOR",  (0,4), (-1,4), MILD_POS_TX),

        ("BACKGROUND", (0,5), (-1,5), STRONG_POS_BG),
        ("TEXTCOLOR",  (0,5), (-1,5), STRONG_POS_TX),

        # Marges
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_volatility_ratio_table_en():
    # Data
    headers = ["Ratio", "Interpretation", "Context Description"]
    data = [
        ["< 0.5", "Volatility collapsing", "Sharp contraction in risk — calm market or volatility compression."],
        ["0.5 – 0.8", "Volatility compressing", "Gradual reduction in dispersion — often a precursor to a breakout."],
        ["0.8 – 1.2", "Volatility normalizing", "Stable volatility — balanced market conditions."],
        ["1.2 – 1.5", "Volatility expanding", "Increasing dispersion — signs of tension or moderate stress."],
        ["> 1.5", "Volatility spiking", "Strong expansion — panic, turbulence, or macro shock."],
    ]

    # Text styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    ratio_style  = ParagraphStyle("Ratio",  parent=base, alignment=1, fontName="Helvetica-Bold")
    interp_style = ParagraphStyle("Interp", parent=base, alignment=1)
    desc_style   = ParagraphStyle("Desc",   parent=base, alignment=0)

    # Paragraph conversion
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([
            Paragraph(row[0], ratio_style),
            Paragraph(row[1], interp_style),
            Paragraph(row[2], desc_style),
        ])

    # Column widths
    col_widths = [25*mm, 45*mm, 110*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Colors
    BLUE_HEADER   = colors.HexColor("#004d80")
    STRONG_NEG_BG = colors.Color(0.98, 0.88, 0.88)
    STRONG_NEG_TX = colors.Color(0.70, 0.10, 0.10)
    MILD_NEG_BG   = colors.Color(0.98, 0.93, 0.93)
    MILD_NEG_TX   = colors.Color(0.60, 0.20, 0.20)
    NEUTRAL_BG    = colors.Color(0.96, 0.96, 0.96)
    NEUTRAL_TX    = colors.Color(0.25, 0.25, 0.25)
    MILD_POS_BG   = colors.Color(0.92, 0.98, 0.92)
    MILD_POS_TX   = colors.Color(0.12, 0.45, 0.12)
    STRONG_POS_BG = colors.Color(1.00, 0.97, 0.85)
    STRONG_POS_TX = colors.Color(0.55, 0.40, 0.00)

    # Visual style
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Borders
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignment
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Row colors
        ("BACKGROUND", (0,1), (-1,1), STRONG_NEG_BG),
        ("TEXTCOLOR",  (0,1), (-1,1), STRONG_NEG_TX),

        ("BACKGROUND", (0,2), (-1,2), MILD_NEG_BG),
        ("TEXTCOLOR",  (0,2), (-1,2), MILD_NEG_TX),

        ("BACKGROUND", (0,3), (-1,3), NEUTRAL_BG),
        ("TEXTCOLOR",  (0,3), (-1,3), NEUTRAL_TX),

        ("BACKGROUND", (0,4), (-1,4), MILD_POS_BG),
        ("TEXTCOLOR",  (0,4), (-1,4), MILD_POS_TX),

        ("BACKGROUND", (0,5), (-1,5), STRONG_POS_BG),
        ("TEXTCOLOR",  (0,5), (-1,5), STRONG_POS_TX),

        # Padding
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table


def make_momentum_ratio_table():

    # Données
    headers = ["Valeur du ratio", "Interprétation", "Description du contexte"]
    data = [
        ["< 0.5", "Effondrement du momentum", "La tendance se retourne ou perd complètement sa force."],
        ["0.5 – 0.8", "Fading momentum", "Le mouvement s’essouffle, la tendance devient fragile."],
        ["0.8 – 1.2", "Momentum stable", "La dynamique reste cohérente avec la tendance long terme."],
        ["1.2 – 1.5", "Momentum renforcé", "Le mouvement s’accélère, signe de consolidation ou de reprise."],
        ["> 1.5", "Momentum surpuissant", "Accélération rapide, souvent associée à un rallye ou à un squeeze."],
    ]

    # Styles de texte
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    ratio_style  = ParagraphStyle("Ratio",  parent=base, alignment=1, fontName="Helvetica-Bold")
    interp_style = ParagraphStyle("Interp", parent=base, alignment=1)
    desc_style   = ParagraphStyle("Desc",   parent=base, alignment=0)

    # Conversion Paragraph
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([
            Paragraph(row[0], ratio_style),
            Paragraph(row[1], interp_style),
            Paragraph(row[2], desc_style),
        ])

    # Largeurs des colonnes
    col_widths = [25*mm, 45*mm, 110*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Couleurs
    BLUE_HEADER   = colors.HexColor("#004d80")
    STRONG_NEG_BG = colors.Color(0.98, 0.88, 0.88)
    STRONG_NEG_TX = colors.Color(0.70, 0.10, 0.10)
    MILD_NEG_BG   = colors.Color(0.98, 0.93, 0.93)
    MILD_NEG_TX   = colors.Color(0.60, 0.20, 0.20)
    NEUTRAL_BG    = colors.Color(0.96, 0.96, 0.96)
    NEUTRAL_TX    = colors.Color(0.25, 0.25, 0.25)
    MILD_POS_BG   = colors.Color(0.92, 0.98, 0.92)
    MILD_POS_TX   = colors.Color(0.12, 0.45, 0.12)
    STRONG_POS_BG = colors.Color(1.00, 0.97, 0.85)
    STRONG_POS_TX = colors.Color(0.55, 0.40, 0.00)

    # Styles visuels
    table.setStyle(TableStyle([
        # En-tête
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Bordures
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignements
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Couleurs ligne par ligne
        ("BACKGROUND", (0,1), (-1,1), STRONG_NEG_BG),
        ("TEXTCOLOR",  (0,1), (-1,1), STRONG_NEG_TX),

        ("BACKGROUND", (0,2), (-1,2), MILD_NEG_BG),
        ("TEXTCOLOR",  (0,2), (-1,2), MILD_NEG_TX),

        ("BACKGROUND", (0,3), (-1,3), NEUTRAL_BG),
        ("TEXTCOLOR",  (0,3), (-1,3), NEUTRAL_TX),

        ("BACKGROUND", (0,4), (-1,4), MILD_POS_BG),
        ("TEXTCOLOR",  (0,4), (-1,4), MILD_POS_TX),

        ("BACKGROUND", (0,5), (-1,5), STRONG_POS_BG),
        ("TEXTCOLOR",  (0,5), (-1,5), STRONG_POS_TX),

        # Marges
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_momentum_ratio_table_en():
    # Data
    headers = ["Ratio Value", "Interpretation", "Context Description"]
    data = [
        ["< 0.5", "Momentum collapse", "The trend is reversing or has completely lost its strength."],
        ["0.5 – 0.8", "Fading momentum", "The move is losing steam — trend becomes fragile or uncertain."],
        ["0.8 – 1.2", "Stable momentum", "Momentum remains consistent with the long-term trend."],
        ["1.2 – 1.5", "Strengthened momentum", "Acceleration of the move — sign of consolidation or recovery."],
        ["> 1.5", "Overpowered momentum", "Rapid acceleration, often associated with a rally or short squeeze."],
    ]

    # Text styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    ratio_style  = ParagraphStyle("Ratio",  parent=base, alignment=1, fontName="Helvetica-Bold")
    interp_style = ParagraphStyle("Interp", parent=base, alignment=1)
    desc_style   = ParagraphStyle("Desc",   parent=base, alignment=0)

    # Paragraph conversion
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([
            Paragraph(row[0], ratio_style),
            Paragraph(row[1], interp_style),
            Paragraph(row[2], desc_style),
        ])

    # Column widths
    col_widths = [25*mm, 45*mm, 110*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Colors
    BLUE_HEADER   = colors.HexColor("#004d80")
    STRONG_NEG_BG = colors.Color(0.98, 0.88, 0.88)
    STRONG_NEG_TX = colors.Color(0.70, 0.10, 0.10)
    MILD_NEG_BG   = colors.Color(0.98, 0.93, 0.93)
    MILD_NEG_TX   = colors.Color(0.60, 0.20, 0.20)
    NEUTRAL_BG    = colors.Color(0.96, 0.96, 0.96)
    NEUTRAL_TX    = colors.Color(0.25, 0.25, 0.25)
    MILD_POS_BG   = colors.Color(0.92, 0.98, 0.92)
    MILD_POS_TX   = colors.Color(0.12, 0.45, 0.12)
    STRONG_POS_BG = colors.Color(1.00, 0.97, 0.85)
    STRONG_POS_TX = colors.Color(0.55, 0.40, 0.00)

    # Visual style
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Borders
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignment
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Row colors
        ("BACKGROUND", (0,1), (-1,1), STRONG_NEG_BG),
        ("TEXTCOLOR",  (0,1), (-1,1), STRONG_NEG_TX),

        ("BACKGROUND", (0,2), (-1,2), MILD_NEG_BG),
        ("TEXTCOLOR",  (0,2), (-1,2), MILD_NEG_TX),

        ("BACKGROUND", (0,3), (-1,3), NEUTRAL_BG),
        ("TEXTCOLOR",  (0,3), (-1,3), NEUTRAL_TX),

        ("BACKGROUND", (0,4), (-1,4), MILD_POS_BG),
        ("TEXTCOLOR",  (0,4), (-1,4), MILD_POS_TX),

        ("BACKGROUND", (0,5), (-1,5), STRONG_POS_BG),
        ("TEXTCOLOR",  (0,5), (-1,5), STRONG_POS_TX),

        # Padding
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table


def make_return_delta_table():
    """Tableau d’interprétation de ∆Return (pp) — adapté selon la fréquence"""

    # Données
    headers = [
        "Horizon",
        "∆Return (pp) — Très négatif",
        "∆Return (pp) — Négatif modéré",
        "∆Return (pp) — Stable",
        "∆Return (pp) — Positif modéré",
        "∆Return (pp) — Fortement positif"
    ]

    # Seuils cohérents par fréquence :
    # Daily : ±2 pp significatifs
    # Weekly : ±1 pp
    # Monthly : ±0.5 pp
    # Yearly : ±0.2 pp
    data = [
        ["Daily",   "< -2",   "-2 à -0.5",   "-0.5 à +0.5",   "+0.5 à +2",   "> +2"],
        ["Weekly",  "< -1",   "-1 à -0.25",  "-0.25 à +0.25", "+0.25 à +1",  "> +1"],
        ["Monthly", "< -0.5", "-0.5 à -0.15","-0.15 à +0.15", "+0.15 à +0.5","> +0.5"],
        ["Yearly",  "< -0.2", "-0.2 à -0.1", "-0.1 à +0.1",   "+0.1 à +0.2", "> +0.2"],
    ]

    interp = [
        ["Forte dégradation", "Détérioration", "Stable", "Accélération", "Forte accélération"]
    ]

    # Fusion des deux (horizon + interprétation qualitative)
    table_data = []
    table_data.append([Paragraph(h, ParagraphStyle("Header", fontName="Helvetica-Bold", alignment=1, textColor=colors.white)) for h in headers])

    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    row_header = ParagraphStyle("RowHeader", parent=base, fontName="Helvetica-Bold", alignment=1)
    cell_style = ParagraphStyle("Cell", parent=base, alignment=1)

    for i, row in enumerate(data):
        row_cells = [Paragraph(row[0], row_header)]
        for j in range(1, len(row)):
            txt = f"{row[j]}<br/><i>{interp[0][j-1]}</i>"
            row_cells.append(Paragraph(txt, cell_style))
        table_data.append(row_cells)

    # Largeur des colonnes
    col_widths = [25*mm, 33*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Couleurs
    BLUE_HEADER = colors.HexColor("#004d80")
    STRONG_NEG_BG = colors.Color(0.98, 0.88, 0.88)
    STRONG_NEG_TX = colors.Color(0.70, 0.10, 0.10)
    MILD_NEG_BG   = colors.Color(0.98, 0.93, 0.93)
    MILD_NEG_TX   = colors.Color(0.60, 0.20, 0.20)
    NEUTRAL_BG    = colors.Color(0.96, 0.96, 0.96)
    NEUTRAL_TX    = colors.Color(0.25, 0.25, 0.25)
    MILD_POS_BG   = colors.Color(0.92, 0.98, 0.92)
    MILD_POS_TX   = colors.Color(0.12, 0.45, 0.12)
    STRONG_POS_BG = colors.Color(0.88, 0.96, 0.88)
    STRONG_POS_TX = colors.Color(0.05, 0.45, 0.05)

    # Style visuel
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        ("BACKGROUND", (1,1), (1,-1), STRONG_NEG_BG),
        ("TEXTCOLOR",  (1,1), (1,-1), STRONG_NEG_TX),

        ("BACKGROUND", (2,1), (2,-1), MILD_NEG_BG),
        ("TEXTCOLOR",  (2,1), (2,-1), MILD_NEG_TX),

        ("BACKGROUND", (3,1), (3,-1), NEUTRAL_BG),
        ("TEXTCOLOR",  (3,1), (3,-1), NEUTRAL_TX),

        ("BACKGROUND", (4,1), (4,-1), MILD_POS_BG),
        ("TEXTCOLOR",  (4,1), (4,-1), MILD_POS_TX),

        ("BACKGROUND", (5,1), (5,-1), STRONG_POS_BG),
        ("TEXTCOLOR",  (5,1), (5,-1), STRONG_POS_TX),

        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_return_delta_table_en():
    """Tableau d’interprétation de ∆Return (pp) — adapté selon la fréquence"""

        # Données
    headers = [
        "Horizon",
        "∆Return (pp) — Strongly negative",
        "∆Return (pp) — Moderately negative",
        "∆Return (pp) — Stable",
        "∆Return (pp) — Moderately positive",
        "∆Return (pp) — Strongly positive"
    ]

    # Seuils cohérents par fréquence :
    # Daily : ±2 pp significatifs
    # Weekly : ±1 pp
    # Monthly : ±0.5 pp
    # Yearly : ±0.2 pp
    data = [
        ["Daily",   "< -2",   "-2 to -0.5",   "-0.5 to +0.5",   "+0.5 to +2",   "> +2"],
        ["Weekly",  "< -1",   "-1 to -0.25",  "-0.25 to +0.25", "+0.25 to +1",  "> +1"],
        ["Monthly", "< -0.5", "-0.5 to -0.15","-0.15 to +0.15", "+0.15 to +0.5","> +0.5"],
        ["Yearly",  "< -0.2", "-0.2 to -0.1", "-0.1 to +0.1",   "+0.1 to +0.2", "> +0.2"],
    ]

    interp = [
        ["Sharp deterioration", "Weakening", "Stable", "Acceleration", "Strong acceleration"]
    ]

    # Fusion des deux (horizon + interprétation qualitative)
    table_data = []
    table_data.append([Paragraph(h, ParagraphStyle("Header", fontName="Helvetica-Bold", alignment=1, textColor=colors.white)) for h in headers])

    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    row_header = ParagraphStyle("RowHeader", parent=base, fontName="Helvetica-Bold", alignment=1)
    cell_style = ParagraphStyle("Cell", parent=base, alignment=1)

    for i, row in enumerate(data):
        row_cells = [Paragraph(row[0], row_header)]
        for j in range(1, len(row)):
            txt = f"{row[j]}<br/><i>{interp[0][j-1]}</i>"
            row_cells.append(Paragraph(txt, cell_style))
        table_data.append(row_cells)

    # Largeur des colonnes
    col_widths = [25*mm, 33*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Couleurs
    BLUE_HEADER = colors.HexColor("#004d80")
    STRONG_NEG_BG = colors.Color(0.98, 0.88, 0.88)
    STRONG_NEG_TX = colors.Color(0.70, 0.10, 0.10)
    MILD_NEG_BG   = colors.Color(0.98, 0.93, 0.93)
    MILD_NEG_TX   = colors.Color(0.60, 0.20, 0.20)
    NEUTRAL_BG    = colors.Color(0.96, 0.96, 0.96)
    NEUTRAL_TX    = colors.Color(0.25, 0.25, 0.25)
    MILD_POS_BG   = colors.Color(0.92, 0.98, 0.92)
    MILD_POS_TX   = colors.Color(0.12, 0.45, 0.12)
    STRONG_POS_BG = colors.Color(0.88, 0.96, 0.88)
    STRONG_POS_TX = colors.Color(0.05, 0.45, 0.05)

    # Style visuel
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        ("BACKGROUND", (1,1), (1,-1), STRONG_NEG_BG),
        ("TEXTCOLOR",  (1,1), (1,-1), STRONG_NEG_TX),

        ("BACKGROUND", (2,1), (2,-1), MILD_NEG_BG),
        ("TEXTCOLOR",  (2,1), (2,-1), MILD_NEG_TX),

        ("BACKGROUND", (3,1), (3,-1), NEUTRAL_BG),
        ("TEXTCOLOR",  (3,1), (3,-1), NEUTRAL_TX),

        ("BACKGROUND", (4,1), (4,-1), MILD_POS_BG),
        ("TEXTCOLOR",  (4,1), (4,-1), MILD_POS_TX),

        ("BACKGROUND", (5,1), (5,-1), STRONG_POS_BG),
        ("TEXTCOLOR",  (5,1), (5,-1), STRONG_POS_TX),

        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table


def make_liquidity_table():

    # Données
    headers = ["Market Cap (indicatif)", "very_liquid", "liquid", "market", "thin", "illiquid"]
    data = [
        ["Mega (>$200B)",  "≥ $200M", "$75–200M", "$30–75M", "$10–30M", "< $10M"],
        ["Large ($10–200B)", "≥ $100M", "$40–100M", "$15–40M", "$5–15M", "< $5M"],
        ["Mid ($2–10B)",   "≥ $50M", "$20–50M", "$8–20M", "$3–8M", "< $3M"],
        ["Small ($300M–$2B)", "≥ $25M", "$10–25M", "$4–10M", "$1–4M", "< $1M"],
        ["Micro (<$300M)", "≥ $10M", "$4–10M", "$1.5–4M", "$0.5–1.5M", "< $0.5M"],
    ]

    # Styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.6
    base.leading = 10.5
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    cap_style    = ParagraphStyle("Cap", parent=base, alignment=0, fontName="Helvetica-Bold")
    cell_style   = ParagraphStyle("Cell", parent=base, alignment=1)

    # Conversion Paragraph
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([Paragraph(row[0], cap_style)] + [Paragraph(v, cell_style) for v in row[1:]])

    # Dimensions
    col_widths = [40*mm, 28*mm, 28*mm, 28*mm, 28*mm, 28*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Couleurs
    BLUE_HEADER   = colors.HexColor("#004d80")
    VERY_LIQ_BG   = colors.Color(0.88, 0.96, 0.88)
    VERY_LIQ_TX   = colors.Color(0.05, 0.45, 0.05)
    LIQ_BG        = colors.Color(0.92, 0.98, 0.92)
    LIQ_TX        = colors.Color(0.12, 0.45, 0.12)
    MARKET_BG     = colors.Color(0.96, 0.96, 0.96)
    MARKET_TX     = colors.Color(0.25, 0.25, 0.25)
    THIN_BG       = colors.Color(0.98, 0.94, 0.90)
    THIN_TX       = colors.Color(0.55, 0.35, 0.10)
    ILLIQ_BG      = colors.Color(0.98, 0.90, 0.90)
    ILLIQ_TX      = colors.Color(0.70, 0.10, 0.10)

    # Style
    table.setStyle(TableStyle([
        # En-tête
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Cadre
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignements
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Couleurs colonnes par niveau de liquidité
        ("BACKGROUND", (1,1), (1,-1), VERY_LIQ_BG),
        ("TEXTCOLOR",  (1,1), (1,-1), VERY_LIQ_TX),

        ("BACKGROUND", (2,1), (2,-1), LIQ_BG),
        ("TEXTCOLOR",  (2,1), (2,-1), LIQ_TX),

        ("BACKGROUND", (3,1), (3,-1), MARKET_BG),
        ("TEXTCOLOR",  (3,1), (3,-1), MARKET_TX),

        ("BACKGROUND", (4,1), (4,-1), THIN_BG),
        ("TEXTCOLOR",  (4,1), (4,-1), THIN_TX),

        ("BACKGROUND", (5,1), (5,-1), ILLIQ_BG),
        ("TEXTCOLOR",  (5,1), (5,-1), ILLIQ_TX),

        # Espacement
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_liquidity_table_en():
    # Data
    headers = ["Market Cap (indicative)", "very_liquid", "liquid", "market", "thin", "illiquid"]
    data = [
        ["Mega (>$200B)",  "≥ $200M", "$75–200M", "$30–75M", "$10–30M", "< $10M"],
        ["Large ($10–200B)", "≥ $100M", "$40–100M", "$15–40M", "$5–15M", "< $5M"],
        ["Mid ($2–10B)",   "≥ $50M", "$20–50M", "$8–20M", "$3–8M", "< $3M"],
        ["Small ($300M–$2B)", "≥ $25M", "$10–25M", "$4–10M", "$1–4M", "< $1M"],
        ["Micro (<$300M)", "≥ $10M", "$4–10M", "$1.5–4M", "$0.5–1.5M", "< $0.5M"],
    ]

    # Styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.6
    base.leading = 10.5
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    cap_style    = ParagraphStyle("Cap", parent=base, alignment=0, fontName="Helvetica-Bold")
    cell_style   = ParagraphStyle("Cell", parent=base, alignment=1)

    # Paragraph conversion
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([Paragraph(row[0], cap_style)] + [Paragraph(v, cell_style) for v in row[1:]])

    # Dimensions
    col_widths = [40*mm, 28*mm, 28*mm, 28*mm, 28*mm, 28*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Colors
    BLUE_HEADER   = colors.HexColor("#004d80")
    VERY_LIQ_BG   = colors.Color(0.88, 0.96, 0.88)
    VERY_LIQ_TX   = colors.Color(0.05, 0.45, 0.05)
    LIQ_BG        = colors.Color(0.92, 0.98, 0.92)
    LIQ_TX        = colors.Color(0.12, 0.45, 0.12)
    MARKET_BG     = colors.Color(0.96, 0.96, 0.96)
    MARKET_TX     = colors.Color(0.25, 0.25, 0.25)
    THIN_BG       = colors.Color(0.98, 0.94, 0.90)
    THIN_TX       = colors.Color(0.55, 0.35, 0.10)
    ILLIQ_BG      = colors.Color(0.98, 0.90, 0.90)
    ILLIQ_TX      = colors.Color(0.70, 0.10, 0.10)

    # Visual style
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Borders
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignment
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Column colors by liquidity level
        ("BACKGROUND", (1,1), (1,-1), VERY_LIQ_BG),
        ("TEXTCOLOR",  (1,1), (1,-1), VERY_LIQ_TX),

        ("BACKGROUND", (2,1), (2,-1), LIQ_BG),
        ("TEXTCOLOR",  (2,1), (2,-1), LIQ_TX),

        ("BACKGROUND", (3,1), (3,-1), MARKET_BG),
        ("TEXTCOLOR",  (3,1), (3,-1), MARKET_TX),

        ("BACKGROUND", (4,1), (4,-1), THIN_BG),
        ("TEXTCOLOR",  (4,1), (4,-1), THIN_TX),

        ("BACKGROUND", (5,1), (5,-1), ILLIQ_BG),
        ("TEXTCOLOR",  (5,1), (5,-1), ILLIQ_TX),

        # Padding
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table


def make_volatility_regimes_table():
    # Données
    headers = ["Régime", "Description synthétique", "Signification de marché"]
    data = [
        ["Subdued (Calme)", "Volatilité anormalement faible, marché calme", "Phase de consolidation, complaisance ou attente. Risque de breakout."],
        ["Normal", "Volatilité conforme à sa moyenne historique", "Marché équilibré, conditions stables, bonne visibilité."],
        ["Elevated", "Volatilité supérieure à la moyenne", "Nervosité croissante, incertitude accrue, phase de tension."],
        ["Turbulent", "Volatilité très élevée, extrême instabilité", "Panique, désordre de marché, stress systémique ou capitulation."],
    ]

    # Styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    regime_style = ParagraphStyle("Regime", parent=base, alignment=1, fontName="Helvetica-Bold")
    desc_style   = ParagraphStyle("Desc",   parent=base, alignment=0)
    signif_style = ParagraphStyle("Signif", parent=base, alignment=0)

    # Conversion Paragraph
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([
            Paragraph(row[0], regime_style),
            Paragraph(row[1], desc_style),
            Paragraph(row[2], signif_style),
        ])

    # Dimensions
    col_widths = [38*mm, 65*mm, 90*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Couleurs
    BLUE_HEADER = colors.HexColor("#004d80")
    SUBDUED_BG  = colors.Color(0.92, 0.97, 0.92)
    SUBDUED_TX  = colors.Color(0.08, 0.40, 0.08)
    NORMAL_BG   = colors.Color(0.96, 0.96, 0.96)
    NORMAL_TX   = colors.Color(0.25, 0.25, 0.25)
    ELEV_BG     = colors.Color(0.99, 0.95, 0.88)
    ELEV_TX     = colors.Color(0.55, 0.30, 0.00)
    TURB_BG     = colors.Color(0.98, 0.90, 0.90)
    TURB_TX     = colors.Color(0.70, 0.10, 0.10)

    # Style
    table.setStyle(TableStyle([
        # En-tête
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Cadre
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignements
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Couleurs par ligne
        ("BACKGROUND", (0,1), (-1,1), SUBDUED_BG),
        ("TEXTCOLOR",  (0,1), (-1,1), SUBDUED_TX),

        ("BACKGROUND", (0,2), (-1,2), NORMAL_BG),
        ("TEXTCOLOR",  (0,2), (-1,2), NORMAL_TX),

        ("BACKGROUND", (0,3), (-1,3), ELEV_BG),
        ("TEXTCOLOR",  (0,3), (-1,3), ELEV_TX),

        ("BACKGROUND", (0,4), (-1,4), TURB_BG),
        ("TEXTCOLOR",  (0,4), (-1,4), TURB_TX),

        # Espacements
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table


def make_volatility_regimes_table_en():
    # Data
    headers = ["Regime", "Brief Description", "Market Meaning"]
    data = [
        ["Subdued", "Abnormally low volatility, calm market", "Consolidation phase, complacency, or waiting period. Potential breakout risk."],
        ["Normal", "Volatility aligned with historical average", "Balanced market conditions, stability, and clear visibility."],
        ["Elevated", "Above-average volatility", "Rising nervousness and uncertainty — tension or mild stress phase."],
        ["Turbulent", "Extremely high volatility, severe instability", "Panic, market disorder, systemic stress, or capitulation."],
    ]

    # Styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    regime_style = ParagraphStyle("Regime", parent=base, alignment=1, fontName="Helvetica-Bold")
    desc_style   = ParagraphStyle("Desc",   parent=base, alignment=0)
    signif_style = ParagraphStyle("Signif", parent=base, alignment=0)

    # Paragraph conversion
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([
            Paragraph(row[0], regime_style),
            Paragraph(row[1], desc_style),
            Paragraph(row[2], signif_style),
        ])

    # Dimensions
    col_widths = [38*mm, 65*mm, 90*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Colors
    BLUE_HEADER = colors.HexColor("#004d80")
    SUBDUED_BG  = colors.Color(0.92, 0.97, 0.92)
    SUBDUED_TX  = colors.Color(0.08, 0.40, 0.08)
    NORMAL_BG   = colors.Color(0.96, 0.96, 0.96)
    NORMAL_TX   = colors.Color(0.25, 0.25, 0.25)
    ELEV_BG     = colors.Color(0.99, 0.95, 0.88)
    ELEV_TX     = colors.Color(0.55, 0.30, 0.00)
    TURB_BG     = colors.Color(0.98, 0.90, 0.90)
    TURB_TX     = colors.Color(0.70, 0.10, 0.10)

    # Visual style
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Borders
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignment
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Row colors
        ("BACKGROUND", (0,1), (-1,1), SUBDUED_BG),
        ("TEXTCOLOR",  (0,1), (-1,1), SUBDUED_TX),

        ("BACKGROUND", (0,2), (-1,2), NORMAL_BG),
        ("TEXTCOLOR",  (0,2), (-1,2), NORMAL_TX),

        ("BACKGROUND", (0,3), (-1,3), ELEV_BG),
        ("TEXTCOLOR",  (0,3), (-1,3), ELEV_TX),

        ("BACKGROUND", (0,4), (-1,4), TURB_BG),
        ("TEXTCOLOR",  (0,4), (-1,4), TURB_TX),

        # Padding
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_signal_table():
    """Tableau d'interprétation du signal de cohérence Momentum CT↔LT"""

    # Données
    headers = ["Valeur", "État du signal", "Interprétation"]
    data = [
        ["> +0.6", "Parfaitement aligné / Cohérence forte", "Le momentum court terme confirme pleinement la tendance long terme. Signal robuste et fiable."],
        ["+0.2 à +0.6", "Partiellement aligné / Cohérence modérée", "La direction reste globalement alignée, mais le signal perd un peu de force."],
        ["−0.2 à +0.2", "Neutre / indéterminé", "Pas de tendance nette : possible phase de latéralisation ou d’attente avant un nouveau mouvement."],
        ["−0.6 à −0.2", "Renversement naissant / Début de retournement", "Début de retournement : le momentum court terme s’oppose faiblement à la tendance de fond."],
        ["< −0.6", "Renversement marqué / Inversion confirmée", "Inversion marquée : signal de retournement confirmé, souvent en phase de correction ou de capitulation."],
    ]

    # Styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    value_style  = ParagraphStyle("Value",  parent=base, alignment=1, fontName="Helvetica-Bold")
    state_style  = ParagraphStyle("State",  parent=base, alignment=1)
    interp_style = ParagraphStyle("Interp", parent=base, alignment=0, leftIndent=2, rightIndent=2)

    # Conversion Paragraph
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([
            Paragraph(row[0], value_style),
            Paragraph(row[1], state_style),
            Paragraph(row[2], interp_style),
        ])

    # Dimensions
    col_widths = [25*mm, 40*mm, 105*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Couleurs
    BLUE_HEADER   = colors.HexColor("#004d80")
    STRONG_POS_BG = colors.Color(0.88, 0.96, 0.88)
    STRONG_POS_TX = colors.Color(0.10, 0.45, 0.10)
    MILD_POS_BG   = colors.Color(0.93, 0.98, 0.93)
    MILD_POS_TX   = colors.Color(0.18, 0.50, 0.18)
    NEUTRAL_BG    = colors.Color(0.96, 0.96, 0.96)
    NEUTRAL_TX    = colors.Color(0.25, 0.25, 0.25)
    MILD_NEG_BG   = colors.Color(0.98, 0.93, 0.93)
    MILD_NEG_TX   = colors.Color(0.60, 0.20, 0.20)
    STRONG_NEG_BG = colors.Color(0.98, 0.88, 0.88)
    STRONG_NEG_TX = colors.Color(0.70, 0.10, 0.10)

    # Style visuel
    table.setStyle(TableStyle([
        # En-tête
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Cadre
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignements
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Couleurs ligne par ligne
        ("BACKGROUND", (0,1), (-1,1), STRONG_POS_BG),
        ("TEXTCOLOR",  (0,1), (-1,1), STRONG_POS_TX),

        ("BACKGROUND", (0,2), (-1,2), MILD_POS_BG),
        ("TEXTCOLOR",  (0,2), (-1,2), MILD_POS_TX),

        ("BACKGROUND", (0,3), (-1,3), NEUTRAL_BG),
        ("TEXTCOLOR",  (0,3), (-1,3), NEUTRAL_TX),

        ("BACKGROUND", (0,4), (-1,4), MILD_NEG_BG),
        ("TEXTCOLOR",  (0,4), (-1,4), MILD_NEG_TX),

        ("BACKGROUND", (0,5), (-1,5), STRONG_NEG_BG),
        ("TEXTCOLOR",  (0,5), (-1,5), STRONG_NEG_TX),

        # Espacement
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_signal_table_en():
    """Interpretation table for the Momentum CT↔LT coherence signal"""

    # Data
    headers = ["Value", "Signal state", "Interpretation"]
    data = [
        ["> +0.6", "Perfectly aligned / Strong coherence", "Short-term momentum fully confirms the long-term trend. Robust and reliable signal."],
        ["+0.2 to +0.6", "Partially aligned / Moderate coherence", "The direction remains broadly aligned, but the signal shows some loss of strength."],
        ["−0.2 to +0.2", "Neutral / Indeterminate", "No clear trend: possible sideways phase or pause before a new movement."],
        ["−0.6 to −0.2", "Emerging reversal / Early turning point", "Early stage of reversal: short-term momentum starts opposing the underlying trend."],
        ["< −0.6", "Strong reversal / Confirmed inversion", "Clear inversion: reversal confirmed, often seen in correction or capitulation phases."],
    ]

    # Styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    value_style  = ParagraphStyle("Value",  parent=base, alignment=1, fontName="Helvetica-Bold")
    state_style  = ParagraphStyle("State",  parent=base, alignment=1)
    interp_style = ParagraphStyle("Interp", parent=base, alignment=0, leftIndent=2, rightIndent=2)

    # Paragraph conversion
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([
            Paragraph(row[0], value_style),
            Paragraph(row[1], state_style),
            Paragraph(row[2], interp_style),
        ])

    # Dimensions
    col_widths = [25*mm, 40*mm, 105*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Colors
    BLUE_HEADER   = colors.HexColor("#004d80")
    STRONG_POS_BG = colors.Color(0.88, 0.96, 0.88)
    STRONG_POS_TX = colors.Color(0.10, 0.45, 0.10)
    MILD_POS_BG   = colors.Color(0.93, 0.98, 0.93)
    MILD_POS_TX   = colors.Color(0.18, 0.50, 0.18)
    NEUTRAL_BG    = colors.Color(0.96, 0.96, 0.96)
    NEUTRAL_TX    = colors.Color(0.25, 0.25, 0.25)
    MILD_NEG_BG   = colors.Color(0.98, 0.93, 0.93)
    MILD_NEG_TX   = colors.Color(0.60, 0.20, 0.20)
    STRONG_NEG_BG = colors.Color(0.98, 0.88, 0.88)
    STRONG_NEG_TX = colors.Color(0.70, 0.10, 0.10)

    # Visual style
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Borders
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignment
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Row colors
        ("BACKGROUND", (0,1), (-1,1), STRONG_POS_BG),
        ("TEXTCOLOR",  (0,1), (-1,1), STRONG_POS_TX),

        ("BACKGROUND", (0,2), (-1,2), MILD_POS_BG),
        ("TEXTCOLOR",  (0,2), (-1,2), MILD_POS_TX),

        ("BACKGROUND", (0,3), (-1,3), NEUTRAL_BG),
        ("TEXTCOLOR",  (0,3), (-1,3), NEUTRAL_TX),

        ("BACKGROUND", (0,4), (-1,4), MILD_NEG_BG),
        ("TEXTCOLOR",  (0,4), (-1,4), MILD_NEG_TX),

        ("BACKGROUND", (0,5), (-1,5), STRONG_NEG_BG),
        ("TEXTCOLOR",  (0,5), (-1,5), STRONG_NEG_TX),

        # Padding
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_efficiency_table():
    """Tableau des régimes d'efficacité (Return / Volatility ratio)"""

    # Données
    headers = ["Horizon", "Défavorable", "Neutre", "Efficace", "Exceptionnel"]
    data = [
        ["Daily",   "< 0.5", "0.5 – 1.0", "1.0 – 2.0", "> 2.0"],
        ["Weekly",  "< 0.5", "0.5 – 1.0", "1.0 – 2.0", "> 2.0"],
        ["Monthly", "< 0.4", "0.4 – 0.8", "0.8 – 1.5", "> 1.5"],
        ["Yearly",  "< 0.3", "0.3 – 0.6", "0.6 – 1.2", "> 1.2"],
    ]

    # Styles de texte
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"  # Passe à DejaVuSans si tu veux garder le vrai tiret “–”

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    row_header   = ParagraphStyle("RowHeader", parent=base, fontName="Helvetica-Bold", alignment=1)
    cell_style   = ParagraphStyle("Cell", parent=base, alignment=1)

    # Conversion Paragraph
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([Paragraph(row[0], row_header)] + [Paragraph(val, cell_style) for val in row[1:]])

    # Dimensions
    col_widths = [25*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Couleurs
    BLUE_HEADER  = colors.HexColor("#004d80")
    BAD_BG        = colors.Color(0.98, 0.90, 0.90)
    BAD_TX        = colors.Color(0.70, 0.10, 0.10)
    NEUTRAL_BG    = colors.Color(0.96, 0.96, 0.96)
    NEUTRAL_TX    = colors.Color(0.25, 0.25, 0.25)
    GOOD_BG       = colors.Color(0.90, 0.97, 0.90)
    GOOD_TX       = colors.Color(0.10, 0.45, 0.10)
    EXCELLENT_BG  = colors.Color(1.00, 0.96, 0.80)  # doré clair
    EXCELLENT_TX  = colors.Color(0.55, 0.40, 0.00)

    # Style visuel
    table.setStyle(TableStyle([
        # En-tête
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Cadre et grille
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignements
        ("ALIGN",      (0,1), (-1,-1), "CENTER"),
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Couleurs par régime
        ("BACKGROUND", (1,1), (1,-1), BAD_BG),
        ("TEXTCOLOR",  (1,1), (1,-1), BAD_TX),

        ("BACKGROUND", (2,1), (2,-1), NEUTRAL_BG),
        ("TEXTCOLOR",  (2,1), (2,-1), NEUTRAL_TX),

        ("BACKGROUND", (3,1), (3,-1), GOOD_BG),
        ("TEXTCOLOR",  (3,1), (3,-1), GOOD_TX),

        ("BACKGROUND", (4,1), (4,-1), EXCELLENT_BG),
        ("TEXTCOLOR",  (4,1), (4,-1), EXCELLENT_TX),

        # Espacement
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_efficiency_table_en():
    """Efficiency regimes table (Return / Volatility ratio)"""

    # Data
    headers = ["Horizon", "Unfavorable", "Neutral", "Efficient", "Exceptional"]
    data = [
        ["Daily",   "< 0.5", "0.5 – 1.0", "1.0 – 2.0", "> 2.0"],
        ["Weekly",  "< 0.5", "0.5 – 1.0", "1.0 – 2.0", "> 2.0"],
        ["Monthly", "< 0.4", "0.4 – 0.8", "0.8 – 1.5", "> 1.5"],
        ["Yearly",  "< 0.3", "0.3 – 0.6", "0.6 – 1.2", "> 1.2"],
    ]

    # Text styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1,
                                  fontName="Helvetica-Bold", textColor=colors.white)
    row_header   = ParagraphStyle("RowHeader", parent=base,
                                  fontName="Helvetica-Bold", alignment=1)
    cell_style   = ParagraphStyle("Cell", parent=base, alignment=1)

    # Paragraph conversion
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([Paragraph(row[0], row_header)] +
                          [Paragraph(val, cell_style) for val in row[1:]])

    # Dimensions
    col_widths = [25*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Colors
    BLUE_HEADER  = colors.HexColor("#004d80")
    BAD_BG        = colors.Color(0.98, 0.90, 0.90)
    BAD_TX        = colors.Color(0.70, 0.10, 0.10)
    NEUTRAL_BG    = colors.Color(0.96, 0.96, 0.96)
    NEUTRAL_TX    = colors.Color(0.25, 0.25, 0.25)
    GOOD_BG       = colors.Color(0.90, 0.97, 0.90)
    GOOD_TX       = colors.Color(0.10, 0.45, 0.10)
    EXCELLENT_BG  = colors.Color(1.00, 0.96, 0.80)  # light gold
    EXCELLENT_TX  = colors.Color(0.55, 0.40, 0.00)

    # Visual style
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Border and grid
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignment
        ("ALIGN",      (0,1), (-1,-1), "CENTER"),
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Regime colors
        ("BACKGROUND", (1,1), (1,-1), BAD_BG),
        ("TEXTCOLOR",  (1,1), (1,-1), BAD_TX),

        ("BACKGROUND", (2,1), (2,-1), NEUTRAL_BG),
        ("TEXTCOLOR",  (2,1), (2,-1), NEUTRAL_TX),

        ("BACKGROUND", (3,1), (3,-1), GOOD_BG),
        ("TEXTCOLOR",  (3,1), (3,-1), GOOD_TX),

        ("BACKGROUND", (4,1), (4,-1), EXCELLENT_BG),
        ("TEXTCOLOR",  (4,1), (4,-1), EXCELLENT_TX),

        # Padding
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table


def make_momentum_table():

    # Données
    headers = ["Horizon", "Faible", "Modéré", "Fort", "Extrême"]
    data = [
        ["Daily",   "< 0.5 %",  "0.5 – 1.5 %",  "1.5 – 3.0 %",  "> 3.0 %"],
        ["Weekly",  "< 1.5 %",  "1.5 – 4.0 %",  "4.0 – 8.0 %",  "> 8.0 %"],
        ["Monthly", "< 3.0 %",  "3.0 – 6.0 %",  "6.0 – 12.0 %", "> 12.0 %"],
        ["Yearly",  "< 8.0 %",  "8.0 – 15.0 %", "15.0 – 30.0 %","> 30.0 %"],
    ]

    # Styles de texte
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"  # ou "DejaVuSans" si besoin du vrai tiret “–”

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    row_header   = ParagraphStyle("RowHeader", parent=base, fontName="Helvetica-Bold", alignment=1)
    cell_style   = ParagraphStyle("Cell", parent=base, alignment=1)

    # Construction du tableau
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([Paragraph(row[0], row_header)] + [Paragraph(val, cell_style) for val in row[1:]])

    col_widths = [25*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Couleurs
    BLUE_HEADER = colors.HexColor("#004d80")
    WEAK_BG     = colors.Color(0.94, 0.97, 0.94)   # vert très clair
    WEAK_TX     = colors.Color(0.10, 0.45, 0.10)
    MOD_BG      = colors.Color(0.97, 0.97, 0.97)   # neutre
    MOD_TX      = colors.Color(0.25, 0.25, 0.25)
    STRONG_BG   = colors.Color(0.98, 0.94, 0.85)   # amber clair
    STRONG_TX   = colors.Color(0.55, 0.35, 0.00)
    EXTREME_BG  = colors.Color(0.98, 0.90, 0.90)   # rouge clair
    EXTREME_TX  = colors.Color(0.70, 0.10, 0.10)

    # Style visuel
    table.setStyle(TableStyle([
        # En-tête
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Cadre
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignements
        ("ALIGN",      (0,1), (-1,-1), "CENTER"),
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Couleurs par régime
        ("BACKGROUND", (1,1), (1,-1), WEAK_BG),
        ("TEXTCOLOR",  (1,1), (1,-1), WEAK_TX),

        ("BACKGROUND", (2,1), (2,-1), MOD_BG),
        ("TEXTCOLOR",  (2,1), (2,-1), MOD_TX),

        ("BACKGROUND", (3,1), (3,-1), STRONG_BG),
        ("TEXTCOLOR",  (3,1), (3,-1), STRONG_TX),

        ("BACKGROUND", (4,1), (4,-1), EXTREME_BG),
        ("TEXTCOLOR",  (4,1), (4,-1), EXTREME_TX),

        # Espacement
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_momentum_table_en():
    """Momentum regimes table (percentage thresholds by horizon)"""

    # Data
    headers = ["Horizon", "Weak", "Moderate", "Strong", "Extreme"]
    data = [
        ["Daily",   "< 0.5%",  "0.5 – 1.5%",  "1.5 – 3.0%",  "> 3.0%"],
        ["Weekly",  "< 1.5%",  "1.5 – 4.0%",  "4.0 – 8.0%",  "> 8.0%"],
        ["Monthly", "< 3.0%",  "3.0 – 6.0%",  "6.0 – 12.0%", "> 12.0%"],
        ["Yearly",  "< 8.0%",  "8.0 – 15.0%", "15.0 – 30.0%","> 30.0%"],
    ]

    # Text styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1,
                                  fontName="Helvetica-Bold", textColor=colors.white)
    row_header   = ParagraphStyle("RowHeader", parent=base,
                                  fontName="Helvetica-Bold", alignment=1)
    cell_style   = ParagraphStyle("Cell", parent=base, alignment=1)

    # Build table
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([Paragraph(row[0], row_header)] +
                          [Paragraph(val, cell_style) for val in row[1:]])

    col_widths = [25*mm, 33*mm, 33*mm, 33*mm, 33*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Colors
    BLUE_HEADER = colors.HexColor("#004d80")
    WEAK_BG     = colors.Color(0.94, 0.97, 0.94)   # very light green
    WEAK_TX     = colors.Color(0.10, 0.45, 0.10)
    MOD_BG      = colors.Color(0.97, 0.97, 0.97)   # neutral
    MOD_TX      = colors.Color(0.25, 0.25, 0.25)
    STRONG_BG   = colors.Color(0.98, 0.94, 0.85)   # light amber
    STRONG_TX   = colors.Color(0.55, 0.35, 0.00)
    EXTREME_BG  = colors.Color(0.98, 0.90, 0.90)   # light red
    EXTREME_TX  = colors.Color(0.70, 0.10, 0.10)

    # Visual style
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Frame and grid
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignment
        ("ALIGN",      (0,1), (-1,-1), "CENTER"),
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Colors by regime
        ("BACKGROUND", (1,1), (1,-1), WEAK_BG),
        ("TEXTCOLOR",  (1,1), (1,-1), WEAK_TX),

        ("BACKGROUND", (2,1), (2,-1), MOD_BG),
        ("TEXTCOLOR",  (2,1), (2,-1), MOD_TX),

        ("BACKGROUND", (3,1), (3,-1), STRONG_BG),
        ("TEXTCOLOR",  (3,1), (3,-1), STRONG_TX),

        ("BACKGROUND", (4,1), (4,-1), EXTREME_BG),
        ("TEXTCOLOR",  (4,1), (4,-1), EXTREME_TX),

        # Padding
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_asset_classes_table():

    headers = ["Classe d’actif", "Return", "Volatility", "Momentum", "Commentaire synthétique"]
    rows = [
        ["Devises (FX)",                      "× 0.3", "× 0.5", "× 0.7", "Faible amplitude et rendement structurel bas ; marché très réversif."],
        ["Obligations (Fixed Income)",        "× 0.5", "× 0.6", "× 0.8", "Stabilité des flux, volatilité limitée ; sensibilité accrue aux taux."],
        ["Actions / ETF / Indices",           "× 1.0", "× 1.0", "× 1.0", "Classe de référence ; dynamique équilibrée entre rendement et risque."],
        ["Matières premières (Commodities)",  "× 1.2", "× 1.3", "× 1.3", "Actifs cycliques sensibles à la conjoncture et aux chocs d’offre/demande."],
        ["Immobilier coté (REITs)",           "× 0.9", "× 1.1", "× 1.0", "Corrélé partiellement aux taux ; tendance plus lissée dans le temps."],
        ["Cryptomonnaies (Crypto)",           "× 2.5", "× 2.0", "× 1.8", "Extrême volatilité ; mouvements directionnels marqués et discontinus."],
        ["Actifs alternatifs (PE, Hedge Funds)","× 0.8", "× 0.8", "× 1.0", "Rendements lissés ; volatilité souvent sous-estimée par manque de liquidité."],
    ]

    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading  = 11
    base.fontName = "Helvetica"  # Passe à "DejaVuSans" si besoin du glyphe × partout

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    first_col     = ParagraphStyle("FirstCol", parent=base, fontName="Helvetica-Bold", alignment=0)
    mid_col       = ParagraphStyle("MidCol",   parent=base, alignment=1)  # centré pour × 0.x
    comment_col   = ParagraphStyle("Comment",  parent=base, alignment=0)

    # Build data
    data = [[Paragraph(h, header_style) for h in headers]]
    for r in rows:
        data.append([
            Paragraph(r[0], first_col),
            Paragraph(r[1], mid_col),
            Paragraph(r[2], mid_col),
            Paragraph(r[3], mid_col),
            Paragraph(r[4], comment_col),
        ])

    # Largeurs (total ≈ 190 mm avec tes marges 1 cm)
    col_widths = [46*mm, 22*mm, 24*mm, 24*mm, 74*mm]
    table = Table(data, colWidths=col_widths, hAlign="LEFT")

    BLUE_HEADER = colors.HexColor("#004d80")
    ROW_ALT_1   = colors.Color(1, 1, 1)
    ROW_ALT_2   = colors.Color(0.98, 0.98, 0.98)

    table.setStyle(TableStyle([
        # En-tête
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Cadre & grille
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignements
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Zebra rows
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [ROW_ALT_1, ROW_ALT_2]),

        # Padding
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))
    return table

def make_asset_classes_table_en():
    """Scale factors by asset class (Return, Volatility, Momentum)"""

    headers = ["Asset class", "Return", "Volatility", "Momentum", "Summary comment"]
    rows = [
        ["Currencies (FX)",                     "× 0.3", "× 0.5", "× 0.7", "Low amplitude and structurally weak returns; highly mean-reverting market."],
        ["Bonds (Fixed Income)",                "× 0.5", "× 0.6", "× 0.8", "Stable cash flows, limited volatility; increased sensitivity to interest rates."],
        ["Equities / ETFs / Indices",           "× 1.0", "× 1.0", "× 1.0", "Reference asset class; balanced dynamics between risk and return."],
        ["Commodities",                         "× 1.2", "× 1.3", "× 1.3", "Cyclical assets sensitive to macro cycles and supply-demand shocks."],
        ["Listed Real Estate (REITs)",          "× 0.9", "× 1.1", "× 1.0", "Partially rate-sensitive; tends to smooth trends over time."],
        ["Cryptocurrencies (Crypto)",           "× 2.5", "× 2.0", "× 1.8", "Extremely volatile; directional moves are sharp and discontinuous."],
        ["Alternative assets (PE, Hedge Funds)", "× 0.8", "× 0.8", "× 1.0", "Smoothed returns; volatility often underestimated due to illiquidity."],
    ]

    # Styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading  = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1,
                                  fontName="Helvetica-Bold", textColor=colors.white)
    first_col   = ParagraphStyle("FirstCol", parent=base, fontName="Helvetica-Bold", alignment=0)
    mid_col     = ParagraphStyle("MidCol",   parent=base, alignment=1)
    comment_col = ParagraphStyle("Comment",  parent=base, alignment=0)

    # Build table data
    data = [[Paragraph(h, header_style) for h in headers]]
    for r in rows:
        data.append([
            Paragraph(r[0], first_col),
            Paragraph(r[1], mid_col),
            Paragraph(r[2], mid_col),
            Paragraph(r[3], mid_col),
            Paragraph(r[4], comment_col),
        ])

    # Widths (≈190 mm total)
    col_widths = [46*mm, 22*mm, 24*mm, 24*mm, 74*mm]
    table = Table(data, colWidths=col_widths, hAlign="LEFT")

    # Colors
    BLUE_HEADER = colors.HexColor("#004d80")
    ROW_ALT_1   = colors.Color(1, 1, 1)
    ROW_ALT_2   = colors.Color(0.98, 0.98, 0.98)

    # Visual style
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Borders & grid
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignment
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Row alternation
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [ROW_ALT_1, ROW_ALT_2]),

        # Padding
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_volatility_table():
    """Tableau des régimes de volatilité (D/W/M/Y)"""

    # Entêtes et données
    headers = ["Horizon", "Atténuée", "Normale", "Élevée", "Turbulente"]
    data = [
        ["Daily", "< 0.3 %",  "0.3 – 0.8 %",  "0.8 – 1.5 %",  "> 1.5 %"],
        ["Weekly", "< 1.0 %",  "1.0 – 2.5 %",  "2.5 – 4.5 %",  "> 4.5 %"],
        ["Monthly", "< 3.0 %",  "3.0 – 6.0 %",  "6.0 – 10.0 %", "> 10.0 %"],
        ["Yearly", "< 8.0 %",  "8.0 – 15.0 %", "15.0 – 25.0 %","> 25.0 %"],
    ]

    # Styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"  # passe à DejaVuSans si tu utilises des glyphes étendus

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    row_header   = ParagraphStyle("RowHeader", parent=base, fontName="Helvetica-Bold", alignment=1)

    # Conversion en Paragraph
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        # horizon (D/W/M/Y) en gras centré
        row_cells = [Paragraph(row[0], row_header)]
        # colonnes de régimes
        row_cells += [Paragraph(c, base) for c in row[1:]]
        table_data.append(row_cells)

    # Largeurs colonnes
    col_widths = [20*mm, 34*mm, 34*mm, 34*mm, 34*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Couleurs
    BLUE_HEADER = colors.HexColor("#004d80")
    # Palette "calme -> tempête"
    SUBDUED_BG  = colors.Color(0.92, 0.97, 0.92)  # vert pâle
    SUBDUED_TX  = colors.Color(0.08, 0.40, 0.08)
    NORMAL_BG   = colors.Color(0.96, 0.96, 0.96)  # gris très clair
    NORMAL_TX   = colors.Color(0.25, 0.25, 0.25)
    ELEV_BG     = colors.Color(0.99, 0.95, 0.88)  # amber clair
    ELEV_TX     = colors.Color(0.55, 0.30, 0.00)
    TURB_BG     = colors.Color(0.98, 0.90, 0.90)  # rouge clair
    TURB_TX     = colors.Color(0.70, 0.10, 0.10)

    table.setStyle(TableStyle([
        # En-tête
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Bordures
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignements
        ("ALIGN",      (0,1), (0,-1), "CENTER"),   # Horizon
        ("ALIGN",      (1,1), (-1,-1), "CENTER"),
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Bandes de fond par régime
        ("BACKGROUND", (1,1), (1,-1), SUBDUED_BG),
        ("TEXTCOLOR",  (1,1), (1,-1), SUBDUED_TX),

        ("BACKGROUND", (2,1), (2,-1), NORMAL_BG),
        ("TEXTCOLOR",  (2,1), (2,-1), NORMAL_TX),

        ("BACKGROUND", (3,1), (3,-1), ELEV_BG),
        ("TEXTCOLOR",  (3,1), (3,-1), ELEV_TX),

        ("BACKGROUND", (4,1), (4,-1), TURB_BG),
        ("TEXTCOLOR",  (4,1), (4,-1), TURB_TX),

        # Padding
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))
    return table

def make_volatility_table_en():
    """Volatility regimes table (D/W/M/Y)"""

    # Headers and data
    headers = ["Horizon", "Subdued", "Normal", "Elevated", "Turbulent"]
    data = [
        ["Daily",   "< 0.3%",  "0.3 – 0.8%",  "0.8 – 1.5%",  "> 1.5%"],
        ["Weekly",  "< 1.0%",  "1.0 – 2.5%",  "2.5 – 4.5%",  "> 4.5%"],
        ["Monthly", "< 3.0%",  "3.0 – 6.0%",  "6.0 – 10.0%", "> 10.0%"],
        ["Yearly",  "< 8.0%",  "8.0 – 15.0%", "15.0 – 25.0%","> 25.0%"],
    ]

    # Styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1,
                                  fontName="Helvetica-Bold", textColor=colors.white)
    row_header   = ParagraphStyle("RowHeader", parent=base,
                                  fontName="Helvetica-Bold", alignment=1)

    # Convert to Paragraphs
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        cells = [Paragraph(row[0], row_header)]
        cells += [Paragraph(c, base) for c in row[1:]]
        table_data.append(cells)

    # Column widths
    col_widths = [20*mm, 34*mm, 34*mm, 34*mm, 34*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Colors
    BLUE_HEADER = colors.HexColor("#004d80")
    # “Calm → Storm” palette
    SUBDUED_BG  = colors.Color(0.92, 0.97, 0.92)
    SUBDUED_TX  = colors.Color(0.08, 0.40, 0.08)
    NORMAL_BG   = colors.Color(0.96, 0.96, 0.96)
    NORMAL_TX   = colors.Color(0.25, 0.25, 0.25)
    ELEV_BG     = colors.Color(0.99, 0.95, 0.88)
    ELEV_TX     = colors.Color(0.55, 0.30, 0.00)
    TURB_BG     = colors.Color(0.98, 0.90, 0.90)
    TURB_TX     = colors.Color(0.70, 0.10, 0.10)

    # Visual style
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,0), "MIDDLE"),
        ("FONTSIZE",   (0,0), (-1,0), 9),

        # Borders
        ("BOX",        (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.black),

        # Alignment
        ("ALIGN",      (0,1), (0,-1), "CENTER"),   # Horizon column
        ("ALIGN",      (1,1), (-1,-1), "CENTER"),
        ("VALIGN",     (0,1), (-1,-1), "MIDDLE"),

        # Background by regime
        ("BACKGROUND", (1,1), (1,-1), SUBDUED_BG),
        ("TEXTCOLOR",  (1,1), (1,-1), SUBDUED_TX),

        ("BACKGROUND", (2,1), (2,-1), NORMAL_BG),
        ("TEXTCOLOR",  (2,1), (2,-1), NORMAL_TX),

        ("BACKGROUND", (3,1), (3,-1), ELEV_BG),
        ("TEXTCOLOR",  (3,1), (3,-1), ELEV_TX),

        ("BACKGROUND", (4,1), (4,-1), TURB_BG),
        ("TEXTCOLOR",  (4,1), (4,-1), TURB_TX),

        # Padding
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    return table

def make_thresholds_table():
    """Tableau des seuils de performance (Daily/Weekly/Monthly/Yearly)"""

    # Données
    headers = ["Horizon", "Hausse très marquée", "Hausse notable", "Neutre", "Léger recul", "Baisse marquée"]
    data = [
        ["Daily",   "> +1.5 %", "+0.8 → +1.5 %", "−0.2 → +0.2 %", "−1.0 → −0.2 %", "< −1.0 %"],
        ["Weekly",  "> +4.0 %", "+2.0 → +4.0 %", "−0.5 → +0.5 %", "−2.0 → −0.5 %", "< −2.0 %"],
        ["Monthly", "> +8.0 %", "+4.0 → +8.0 %", "−1.0 → +1.0 %", "−5.0 → −1.0 %", "< −5.0 %"],
        ["Yearly",  "> +25.0 %","+15.0 → +25.0 %","−5.0 → +5.0 %", "−15.0 → −5.0 %","< −15.0 %"],
    ]

    # Styles de base
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1, fontName="Helvetica-Bold", textColor=colors.white)
    row_header   = ParagraphStyle("RowHeader", parent=base, fontName="Helvetica-Bold", alignment=0)

    # Conversion en Paragraph
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([Paragraph(row[0], row_header)] + [Paragraph(c, base) for c in row[1:]])

    # Tableau
    col_widths = [25*mm, 32*mm, 32*mm, 30*mm, 32*mm, 35*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Couleurs
    BLUE_HEADER = colors.HexColor("#004d80")
    GREEN_LIGHT = colors.Color(0.88, 0.96, 0.88)
    GREY_LIGHT  = colors.Color(0.95, 0.95, 0.95)
    RED_LIGHT   = colors.Color(0.98, 0.90, 0.90)
    GREEN_DARK  = colors.Color(0.05, 0.45, 0.05)
    RED_DARK    = colors.Color(0.70, 0.10, 0.10)

    table.setStyle(TableStyle([
        # En-tête
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("ALIGN", (0,0), (-1,0), "CENTER"),
        ("VALIGN", (0,0), (-1,0), "MIDDLE"),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTSIZE", (0,0), (-1,0), 9),
        # Bordures
        ("BOX", (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID", (0,0), (-1,-1), 0.3, colors.black),
        # Alignements
        ("ALIGN", (0,1), (-1,-1), "CENTER"),
        ("VALIGN", (0,1), (-1,-1), "MIDDLE"),
        ("ALIGN", (0,1), (0,-1), "LEFT"),
        # Couleurs par zone
        ("BACKGROUND", (1,1), (2,-1), GREEN_LIGHT),
        ("TEXTCOLOR",  (1,1), (2,-1), GREEN_DARK),
        ("BACKGROUND", (3,1), (3,-1), GREY_LIGHT),
        ("TEXTCOLOR",  (3,1), (3,-1), colors.Color(0.25,0.25,0.25)),
        ("BACKGROUND", (4,1), (5,-1), RED_LIGHT),
        ("TEXTCOLOR",  (4,1), (5,-1), RED_DARK),
        # Padding
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))
    return table

def make_thresholds_table_en():
    """Performance thresholds table (Daily / Weekly / Monthly / Yearly)"""

    # Data
    headers = ["Horizon", "Sharp rise", "Moderate rise", "Neutral", "Mild drop", "Sharp fall"]
    data = [
        ["Daily",   "> +1.5%", "+0.8 → +1.5%", "−0.2 → +0.2%", "−1.0 → −0.2%", "< −1.0%"],
        ["Weekly",  "> +4.0%", "+2.0 → +4.0%", "−0.5 → +0.5%", "−2.0 → −0.5%", "< −2.0%"],
        ["Monthly", "> +8.0%", "+4.0 → +8.0%", "−1.0 → +1.0%", "−5.0 → −1.0%", "< −5.0%"],
        ["Yearly",  "> +25.0%", "+15.0 → +25.0%", "−5.0 → +5.0%", "−15.0 → −5.0%", "< −15.0%"],
    ]

    # Base styles
    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontSize = 8.8
    base.leading = 11
    base.fontName = "Helvetica"

    header_style = ParagraphStyle("Header", parent=base, alignment=1,
                                  fontName="Helvetica-Bold", textColor=colors.white)
    row_header   = ParagraphStyle("RowHeader", parent=base,
                                  fontName="Helvetica-Bold", alignment=0)

    # Convert to Paragraphs
    table_data = [[Paragraph(h, header_style) for h in headers]]
    for row in data:
        table_data.append([Paragraph(row[0], row_header)] + [Paragraph(c, base) for c in row[1:]])

    # Table
    col_widths = [25*mm, 32*mm, 32*mm, 30*mm, 32*mm, 35*mm]
    table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

    # Colors
    BLUE_HEADER = colors.HexColor("#004d80")
    GREEN_LIGHT = colors.Color(0.88, 0.96, 0.88)
    GREY_LIGHT  = colors.Color(0.95, 0.95, 0.95)
    RED_LIGHT   = colors.Color(0.98, 0.90, 0.90)
    GREEN_DARK  = colors.Color(0.05, 0.45, 0.05)
    RED_DARK    = colors.Color(0.70, 0.10, 0.10)

    # Style
    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0,0), (-1,0), BLUE_HEADER),
        ("ALIGN", (0,0), (-1,0), "CENTER"),
        ("VALIGN", (0,0), (-1,0), "MIDDLE"),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTSIZE", (0,0), (-1,0), 9),

        # Borders
        ("BOX", (0,0), (-1,-1), 0.6, colors.black),
        ("INNERGRID", (0,0), (-1,-1), 0.3, colors.black),

        # Alignment
        ("ALIGN", (0,1), (-1,-1), "CENTER"),
        ("VALIGN", (0,1), (-1,-1), "MIDDLE"),
        ("ALIGN", (0,1), (0,-1), "LEFT"),

        # Color zones
        ("BACKGROUND", (1,1), (2,-1), GREEN_LIGHT),
        ("TEXTCOLOR",  (1,1), (2,-1), GREEN_DARK),

        ("BACKGROUND", (3,1), (3,-1), GREY_LIGHT),
        ("TEXTCOLOR",  (3,1), (3,-1), colors.Color(0.25,0.25,0.25)),

        ("BACKGROUND", (4,1), (5,-1), RED_LIGHT),
        ("TEXTCOLOR",  (4,1), (5,-1), RED_DARK),

        # Padding
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))

    return table

def build_annex(path_pdf, language, blocks):
    title, h1, body, bullet = make_styles()
    doc = SimpleDocTemplate(
        path_pdf, pagesize=portrait(A4),
        leftMargin=1*cm, rightMargin=1*cm, topMargin=1*cm, bottomMargin=1*cm
    )
    story = [Paragraph("Annexe technique - Portfolio rotation report" if language=="fr" else "Annex — How to read this report", title),
             Spacer(1, 0.2*cm)]

    for section_title, paragraphs in blocks:
        items = [Paragraph(section_title, h1)]
        for p in paragraphs:
            if isinstance(p, str):
                if p.lstrip().startswith("* "):
                    items.append(Paragraph(p[2:], bullet, bulletText="•"))
                else:
                    items.append(Paragraph(p, body))
            elif isinstance(p, Flowable):
                # on insère directement les flowables (Table, Spacer, etc.)
                items.append(p)
            else:
                # fallback : cast en string proprement
                items.append(Paragraph(str(p), body))
        story.append(KeepTogether(items))
        story.append(Spacer(1, 0.2*cm))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)

# ---- Contenus (exemple — remplace par tes textes complets) ----
BLOCKS_FR = [
    ("Introduction", [
        "Cette annexe accompagne le rapport Portfolio rotation et présente les fondements techniques, méthodologiques et interprétatifs du modèle. Elle décrit la structure des fichiers de données, le fonctionnement des fenêtres dynamiques, les formules de calcul des indicateurs clés, ainsi que la logique d’interprétation utilisée dans les tableaux et scénarios du rapport principal. L’objectif est de garantir la transparence méthodologique, la reproductibilité des résultats et la bonne compréhension des signaux produits par le programme, quel que soit le type d’actif ou l’horizon d’analyse.",
    ]),
    ("1. Objectif & périmètre<a name='section_objectif'/>", [
        "L’objectif du rapport est de <b>décrire et interpréter l’état d’un univers d’actifs donné </b>, qu’il s’agisse d'equity, d’indices, d'ETF ou de tout autre support. Il vise à <b>identifier les phases de rotation, de tension ou de stabilisation</b> à travers l’analyse combinée des rendements, de la volatilité, du momentum et de leur cohérence entre horizons court et long terme. Le rapport fournit ainsi une <b>lecture synthétique, structurée et interprétable</b> des régimes de marché, des biais de composition et des conditions de risque, afin de faciliter le <b>diagnostic global et la prise de décision</b>.<a name='section_objectifs'/>",
        "* Sources : <i>sectors.parquet</i>, <i>vol_profiles.parquet</i>, <i>constituents.csv</i>.",
        "<u>sectors.parquet:</u> Le fichier sectors.parquet contient l’historique des prix des actifs utilisés pour l’analyse. Le programme l’exploite pour calculer les rendements, la volatilité et le momentum sur différentes fenêtres de temps (court et long terme). En pratique, c’est la base de données principale à partir de laquelle sont dérivés tous les indicateurs, corrélations et classements présentés dans le rapport.<a name='section_fichiers_utilises'/>",
        "<u>vol_profiles.parquet:</u> Le fichier vol_profiles.parquet contient des informations structurelles et qualitatives sur chaque actif : profil de volatilité, régime de marché, liquidité, levier, bêta, type d’actif, capitalisation, etc. Ces données ne sont pas issues du calcul des séries temporelles, mais d’une analyse statistique préalable ou d’un profilage structurel réalisé sur des périodes plus longues. En complément de sectors.parquet, il apporte donc une couche d’interprétation macro et de contexte, utile pour comprendre le comportement attendu de chaque actif (par exemple “dynamic”, “speculative”, “defensive”). Les deux fichiers sont séparés pour distinguer la donnée brute (historique de prix) de la métadonnée descriptive (profil de risque). Cette séparation rend le modèle plus modulaire, lisible et réutilisable, tout en évitant de recalculer ou de dupliquer ces informations à chaque mise à jour des données de marché. ",
        "<u>constituents.csv:</u> Le fichier constituents.csv contient la liste de référence des actifs analysés avec leurs symboles, noms complets et classifications GICS (secteur, industrie, etc.). Il ne fournit pas de données de marché ni de métriques calculées, mais une cartographie descriptive permettant d’identifier chaque ligne de sectors.parquet et de relier les tickers à leur secteur économique ou thématique. Ce fichier sert donc de pont entre les données chiffrées et leur contexte économique, indispensable pour produire les commentaires sur la diversification, les biais sectoriels et la couverture macro. Il est séparé du reste pour garder une structure claire et actualisable indépendamment (par exemple, si une entreprise change de secteur ou de ticker, sans toucher aux séries temporelles).",
        "<b>AVERTISSEMENT</b> — constituents.csv a été créé manuellement et n’est pas automatiquement mis à jour. Avant toute exécution du programme, l’utilisateur doit vérifier que tous les actifs inclus dans son analyse sont bien présents dans ce fichier, avec un symbole exact et une classification correcte (secteur GICS, sous-industrie, etc.). En cas d’absence, il est nécessaire de ajouter manuellement les lignes manquantes afin d’assurer la cohérence du rapport et la génération correcte des commentaires sectoriels.",
    ]),
    ("Sommaire", [
        table,
        PageBreak()
    ]),
    ("2. Fenêtres & fréquence<a name='section_fenetres_frequence'/>", [
        "<b>2.1 Fenêtres dynamiques</b>.<a name='section_fenetres_dynamiques'/>",
        "Les fenêtres dynamiques constituent un élément central du projet : elles permettent d’adapter automatiquement la taille des périodes d’analyse (volatilité, rendement, momentum) à la fréquence et à la profondeur du jeu de données.",
        "<b>2.2 Objectif</b><a name='section_fenetres_objectif'/>",
        "L’idée est d’éviter un calibrage fixe (ex. 20 jours pour tout) qui deviendrait incohérent selon qu’on travaille sur des données journalières, hebdomadaires ou mensuelles. Ainsi, le programme calcule des fenêtres proportionnelles au nombre total d’observations, garantissant que les indicateurs restent comparables et économiquement cohérents quel que soit l’horizon.",
        "<b>2.3 Fonctionnement</b><a name='section_fenetres_fonctionnement'/>",
        "1.	La fréquence est d’abord détectée automatiquement (Daily, Weekly, Monthly, etc.).",
        "2.	Selon cette fréquence, une fenêtre de base est fixée (ex. 20 pour du daily, 4 pour du weekly, 3 pour du monthly).",
        "3.	Cette base est ensuite ajustée dynamiquement en fonction du nombre total de points disponibles :",
        "* Les fenêtres court terme (CT) couvrent environ 10 % à 30 % de l’historique.",
        "* Les fenêtres long terme (LT) s’étendent jusqu’à 85 % à 90 % de la série.",
        "4.	Des garde-fous empêchent d’utiliser des fenêtres trop courtes ou trop longues (min 3 points, max n points - 5).",
        "<b>2.4 Fenêtres distinctes pour chaque indicateur</b>.<a name='section_fenetres_distinction'/>",
        "•	Volatility : nécessite une fenêtre plus courte et réactive, car elle mesure la dispersion instantanée des rendements.",
        "•	Return : utilise une fenêtre intermédiaire, représentative du comportement moyen sur une période significative.",
        "•	Momentum : requiert une fenêtre plus longue, car il reflète une tendance cumulative et doit éviter les signaux trop bruités.",
        "<b>AVERTISSEMENT</b> — Sur des jeux de données trop courts, les fenêtres dynamiques deviennent mécaniquement trop petites, ce qui augmente la volatilité des indicateurs. Elles ne remplacent pas une analyse économique experte : des fenêtres “idéales” peuvent varier selon la nature des actifs (ex. crypto vs obligations). Enfin, l’approche dynamique garantit la robustesse structurelle du modèle, mais au prix d’une comparabilité limitée entre plusieurs études si la profondeur des données diffère fortement."
    ]),
    ("3. Structure de portefeuille et profil macroéconomique<a name='structure_portfolio'/>", [
        "<b>3.1 Objectif</b><a name='structure_objectif'/>",
        "La section Portfolio Composition a pour but de présenter la structure initiale du portefeuille analysé, en identifiant la répartition sectorielle, les biais de capitalisation, et les principales zones de concentration. Elle fournit un contexte statique et macroéconomique à partir duquel les dynamiques ultérieures (rendements, volatilité, régimes) seront interprétées.",
        "<b>3.2 Fonctionnement</b><a name='structure_fonctionnement'/>",
        "Le bloc Portfolio Composition s’appuie sur les métadonnées contenues dans constituents.csv et les profils structurels issus de vol_profiles.parquet. Chaque ligne du portefeuille est rattachée à une catégorie sectorielle (GICS), puis agrégée en pondération relative, soit :",
        "* également pondérée (weight = 1/n),",
        "* ou pondérée par la capitalisation de marché si disponible.",
        "<b>3.3 Utilité analytique</b><a name='structure_utilite'/>",
        "Avant de commenter les performances ou signaux, il est indispensable de savoir dans quoi le portefeuille est investi (secteurs, biais défensifs, surpondérations). En effet, un portefeuille très concentré sur 3–4 secteurs ou dominé par des méga-cap n’a pas la même sensibilité qu’un panier équilibré. cette section permet d’évaluer si les dynamiques de marché observées ensuite (momentum, volatilité, rotation) découlent de la construction du portefeuille ou d’événements externes.",
        "<b>3.4 Fonctionnement du module Macro Profile Insight</b><a name='structure_profile'/>",
        "Le commentaire automatique Macro Profile Insight repose sur une logique d’analyse multi-niveaux qui combine des informations descriptives (sectorielles) et des profils structurels (quantitatifs) pour produire une synthèse cohérente de la posture du portefeuille. Ce moteur interprétatif s’exécute à partir de deux jeux de données principaux :",
        "* constituents.csv : classification GICS et composition nominale du portefeuille ;",
        "* vol_profiles.parquet : métadonnées structurelles (volatilité, bêta, liquidité, capitalisation, effet de levier, type d’actif, etc.).",
        "Le module commence par analyser la diversification sectorielle à partir des libellés GICS. Le nombre de secteurs distincts détermine le niveau de couverture macroéconomique :",
        "* Un seul secteur → concentration extrême, dépendance à un seul moteur macro ;",
        "* Trois à cinq secteurs → couverture partielle, biais thématique marqué ;",
        "* Huit à dix secteurs → diversification équilibrée proche d’un benchmark global.",
        "Les secteurs absents sont ensuite identifiés pour déduire les biais implicites :",
        "* Absence d’énergie ou de matières premières → manque de couverture inflationniste ;",
        "* Absence de santé ou de consommation de base → faible composante défensive ;",
        "* Absence de technologies ou de communication → biais anti-croissance.",
        "Le moteur analyse ensuite les profils structurels présents dans vol_profiles.parquet pour compléter l’interprétation :",
        "* Market Cap Label : repère les tilts mega/large-cap (stabilité, faible idiosyncrasie) ou small/micro-cap (convexité plus forte, volatilité accrue).",
        "* Asset Type : mesure la part d’ETF, REIT ou ADR afin d’identifier la nature de l’exposition (indirecte, immobilière, géographique).",
        "* Liquidity Label & ADV10USD : qualifie la posture de liquidité (ex. ample trading liquidity, pockets of thin/illiquid names).",
        "* Beta Label & Leverage Label : décrit la sensibilité systématique et la présence éventuelle d’effet de levier.",
        "* Volatility Profile : définit le style global du portefeuille (équilibré, défensif ou spéculatif).",
        "L’objectif de Macro Profile Insight n’est pas de juger la performance, mais de caractériser la posture du portefeuille avant toute interprétation dynamique.",
        "<b>AVERTISSEMENT</b> — Les informations présentées dans cette section reposent sur la composition déclarée du portefeuille au moment de l’analyse et sur les catégorisations issues de constituents.csv et vol_profiles.parquet. Elles ne reflètent pas nécessairement les pondérations réelles, les expositions économiques indirectes ni les ajustements récents du portefeuille.",
    ]),
    ("4. Indicateurs clés<a name='section_indicateurs'/>", [
        "Cette section présente les indicateurs fondamentaux utilisés dans le modèle: Return, Volatility, Momentum, Risk-Adjusted Return, Signal Stability, Volatility Regime et ADV10USD. Chacun d’eux mesure une dimension spécifique de la dynamique de marché : performance, risque, cohérence ou liquidité. Ensemble, ils constituent la base analytique sur laquelle reposent les interprétations et scénarios du rapport principal.",
        "<b>4.1 Return / R (%)</b><a name='section_return'/>",
        "Le Return mesure la performance moyenne d’un actif sur une période donnée. C’est la base de toute lecture de marché, car il indique dans quelle direction le prix évolue, et avec quelle intensité. Il permet de comparer des actifs ou des secteurs entre eux sur un pied d’égalité temporelle, quel que soit leur niveau de volatilité ou de momentum.",
        "Le rendement moyen (AvgReturn %) est calculé sur une fenêtre glissante dynamique, dont la taille dépend de la fréquence détectée dans les données. Cette approche vise à adapter la sensibilité du calcul à la profondeur historique disponible et à la volatilité typique du marché.",
        "* Le programme calcule les rendements logarithmiques entre deux observations successives (ce qui rend les variations additives dans le temps).",
        "* Ces rendements sont ensuite agrégés sur une fenêtre mobile : la taille de cette fenêtre varie selon la fréquence d’analyse (ex. environ 20 jours pour du daily, 4 semaines pour du weekly, etc.). plus la fréquence est longue, plus la fenêtre est élargie, afin de lisser le bruit et capturer la tendance dominante.",
        "* Le rendement total sur la fenêtre est ensuite converti en pourcentage moyen par période. Cela permet d’obtenir un indicateur lisible : combien l’actif progresse ou recule, en moyenne, par période d’observation.",
        "<i>Interprétation de rendement par horizon(*)</i>",
        make_thresholds_table(),
        "Le Return est le pivot du rapport : Il alimente les autres indicateurs (momentum, ratios, scénarios), il structure la lecture économique des cycles (rallye, correction, rebond technique,etc.) et sert de référence comparative dans la détection de phases de stress ou de rotation sectorielle. Sans le Return, il serait impossible d’évaluer la direction du marché, ni d’analyser la cohérence ou la divergence avec le momentum et la volatilité.",
        "<b>AVERTISSEMENT</b> — Le Return ne dit rien sur le risque : un rendement élevé peut s’accompagner d’une forte volatilité. Il peut être trompeur sur de courtes périodes, en particulier après des événements ponctuels (news, earnings, etc.). Il n’intègre pas la persistance des mouvements : une succession d’allers-retours peut donner un rendement moyen nul, alors que le marché est très actif. Le rendement moyen n’est pas annualisé : il mesure la dynamique locale, pas la performance sur un an. ",
        PageBreak(),
        "<b>4.2 Volatility / V (%)</b><a name='section_volatility'/>",
        "La volatilité mesure l’amplitude moyenne des fluctuations de prix sur une période donnée. C’est un indicateur de risque et d’instabilité, complémentaire au rendement : alors que le Return indique la direction du marché, la Volatility en exprime la nervosité. Elle permet d’évaluer la régularité du comportement d’un actif, sa sensibilité aux chocs et sa capacité à maintenir une tendance stable. Dans le rapport, la volatilité joue un rôle central dans l’interprétation des régimes de marché (subdued, normal, elevated, turbulent).",
        "Le calcul de la volatilité suit le même principe de fenêtre glissante dynamique que pour le rendement et le momentum :",
        "* Le programme calcule la dispersion statistique (écart-type) des rendements logarithmiques sur une fenêtre mobile.",
        "* La taille de cette fenêtre dépend de la fréquence d’analyse : plus la fréquence est élevée, plus la fenêtre est courte (ex. 20 jours pour du daily, 4 semaines pour du weekly, 3 mois pour du monthly, etc.).",
        "* Cette mesure est ensuite exprimée en pourcentage moyen par période, afin d’obtenir une échelle comparable entre actifs et horizons.",
        "L’approche dynamique garantit que la volatilité reste réactive à court terme, tout en préservant la lisibilité structurelle à long terme.Elle s’adapte automatiquement à la profondeur historique disponible, ce qui évite d’utiliser des fenêtres arbitraires trop longues ou trop courtes selon les actifs.",
        "<i>Interprétation de volatilité par horizon(*)</i>",
        make_volatility_table(),
        "La volatilité permet d’identifier le régime de risque global dans lequel s’inscrit le portefeuille : elle détermine la probabilité d’un changement de tendance, la stabilité du momentum et la cohérence du signal à court terme. Elle sert aussi de base au calcul du Risk-Adjusted Return et oriente directement la classification des scénarios de marché (capitulation, stress, uptrend, etc.).",
        "<b>AVERTISSEMENT</b> — La volatilité ne mesure ni la direction, ni la performance future : un marché haussier peut être très volatil, tout comme un marché baissier peut être stable. Une baisse temporaire de volatilité ne signifie pas nécessairement une réduction du risque: elle peut précéder une rupture de tendance. Enfin, sur des séries trop courtes, la mesure peut être statistiquement instable, en particulier lorsque les rendements présentent des sauts extrêmes ou irréguliers.",
        "<b>4.3 Momentum / M (%)</b><a name='section_momentum'/>",
        "Le Momentum mesure la persistance directionnelle du mouvement des prix sur une période donnée. Alors que le Return capture la performance moyenne, le Momentum décrit la cohérence et la vitesse du mouvement : il permet de savoir si le marché avance régulièrement dans une direction, ou s’il oscille sans conviction. C’est un indicateur essentiel pour détecter les phases d’accélération, d’essoufflement ou de retournement de tendance.",
        "Le Momentum (M %) est calculé sur une fenêtre glissante dynamique, adaptée à la fréquence des données :",
        "* Lorsque la fenêtre contient 4 points ou moins (typiquement en daily ou weekly), le nombre d’observations est trop faible pour qu’une moyenne soit statistiquement représentative. Dans ce cas, le programme calcule simplement la somme glissante des rendements logarithmiques, c’est-à-dire l’accumulation brute des variations successives sur la fenêtre. Ce choix permet de préserver la réactivité du signal : sur des horizons très courts, chaque variation individuelle a un poids significatif, et la normalisation (division par w) atténuerait inutilement l’amplitude du mouvement.",
        "* Lorsque la fenêtre dépasse 4 points, la somme brute perd de sa pertinence, car les rendements individuels tendent à s’équilibrer. Le programme utilise alors la moyenne géométrique des rendements logarithmiques. Cette approche exprime la vitesse moyenne de progression du prix par unité de temps, en neutralisant les effets de la longueur de la fenêtre.",
        "* Le résultat est ensuite normalisé par la taille de la fenêtre afin d’obtenir une mesure moyenne par unité de temps.",
        "Cette approche hybride permet de garder une lecture homogène du momentum sur différents horizons sans perdre en précision sur les courtes périodes.",
        "<i>Interprétation du momentum par horizon(*)</i>",
        make_momentum_table(),
        "Le Momentum est complémentaire du Return : il n’indique pas la direction absolue mais la force relative du mouvement. Un actif peut avoir un rendement positif avec un momentum faible (fatigue de tendance), ou un rendement négatif avec un momentum qui se redresse (rebond technique).",
        "<b>AVERTISSEMENT</b> — Le Momentum est sensible au timing : une fenêtre trop courte amplifie le bruit, une fenêtre trop longue masque les signaux récents. Il ne tient pas compte du niveau de volatilité: un mouvement rapide peut être lié à la panique autant qu’à la conviction. Enfin, un momentum très élevé ne signifie pas forcément un signal d’achat : il peut indiquer une surchauffe ou un risque de retournement imminent. C’est pourquoi le Momentum doit toujours être lu conjointement avec la Volatility et le Return, pour confirmer la cohérence ou détecter les divergences de marché.",
        "<b>4.4 Risk-Adjusted Return / RAR</b><a name='section_rar'/>",
        "Le Risk-Adjusted Return (RAR) mesure la performance moyenne d’un actif rapportée à son niveau de risque, représenté ici par la volatilité. C’est une version simplifiée et intuitive du ratio de Sharpe, utilisée pour évaluer l’efficacité de la performance : combien l’actif génère de rendement pour chaque unité de volatilité. Il permet de comparer des actifs de profils très différents sur une base homogène. Un RAR élevé indique que le rendement compense largement le risque pris ; un RAR faible ou négatif traduit une performance inefficace ou risquée.",
        "Dans le programme, le RAR est calculé selon la formule :",
        "<i> RAR = AvgReturn(%) / Volatility(%) </i>",
        "* Les deux valeurs proviennent des mêmes fenêtres dynamiques que celles utilisées pour les indicateurs bruts.",
        "* Le calcul n’est pas annualisé : il mesure une efficience instantanée plutôt qu’un ratio de performance long terme.",
        "* Le résultat est sans unité (ratio pur), centré autour de zéro.",
        "<i>Interprétation du Risk Adjusted Return</i>",
        make_efficiency_table(),
        "Le RAR permet une lecture directe de l’équilibre rendement/risque, s’adapte automatiquement à la fréquence et à la profondeur des données et est indépendant de l’échelle des rendements absolus : il exprime la qualité plutôt que la quantité.",
        "<b>AVERTISSEMENT</b> — Ignore la corrélation avec d’autres actifs, il reste individuel (non « portefeuille »), est insensible aux rendements asymétriques ou aux queues de distribution et peut être trompeur en période de faible volatilité si la performance est temporairement élevée. Le Risk-Adjusted Return doit être interprété avec prudence. Un actif à fort bêta peut afficher un RAR élevé sans être réellement efficient, car il bénéficie d’un effet d’amplification lié au marché. Pour une lecture plus juste, il convient de pondérer son interprétation par la sensibilité au marché (β) et le profil de volatilité de l’actif.",
        PageBreak(),
        "<b>4.5 Signal stability</b><a name='section_signal'/>",
        "Le Signal Stability (ou stabilité du signal) mesure la cohérence entre la tendance de court terme (momentum actuel) et la tendance de long terme (momentum structurel). Il indique dans quelle mesure la dynamique récente confirme ou contredit la direction dominante du marché. Cet indicateur sert à qualifier la fiabilité du mouvement en cours, c’est-à-dire si le signal est cohérent, fragile ou en phase de retournement.",
        "Dans le programme, le Signal Stability est calculé ainsi :",
        "<i>Signal = (Momentum × Momentum_LT) / (|Momentum| + |Momentum_LT| + ε) </i>",
        "<i> (avec ε ≈ 10e-6 pour éviter la division par zéro)</i>",
        "Le résultat est un indice normalisé entre -1 et +1, où :",
        "* +1 → parfaite cohérence (le momentum court et long terme vont dans le même sens)",
        "* 0 → absence de relation claire ou signaux contradictoires faibles",
        "* -1 → divergence totale (retournement de tendance fort)",
        "<i>Interprétation du signal</i>",
        make_signal_table(),
        "Le signal aide à détecter les changements de phase de marché (passage haussier → baissier, ou inversement), fournit une validation qualitative du momentum et du rendement observé et sert de pivot dans la lecture du scénario courant (cohérence, distribution, stress, etc.).",
        "<b>AVERTISSEMENT</b> — Peut devenir instable sur des séries très courtes (peu de points pour calculer le momentum LT), ne distingue pas aussi les fortes variations volatiles de vraies inversions de tendance (il faut croiser avec la volatilité) et sa plage de valeurs [-1, +1] est qualitative, pas probabiliste : ce n’est pas un indicateur de prévision, mais de structure du signal.",
        "<b>4.6 Volatility regime</b><a name='section_regime'/>",
        "Le régime reflète l’état global du marché à travers le niveau et la dynamique de la volatilité. C’est une typologie qualitative qui décrit le contexte de risque dans lequel évolue l’actif ou le portefeuille : calme, normal, tendu ou chaotique. L’objectif du Regime est d’offrir une lecture intuitive de la phase de volatilité dominante, plutôt que de se limiter à une valeur chiffrée.",
        "Le régime est dérivé du fichier vol_profiles.parquet, alimenté par l’analyse historique de la volatilité moyenne de chaque actif. Chaque ligne du fichier contient :",
        "Le calcul du Regime repose sur le rapport entre deux horizons de volatilité :",
        "* vol_short : volatilité calculée sur la fenêtre de court terme (par exemple, 20 jours pour du daily, 4 semaines pour du weekly),",
        "* vol_long : volatilité lissée sur la fenêtre longue (par exemple, 6 à 10 fois plus large).",
        "À partir du résultat, on effectue une classification automatique en profils de volatilité (défensive, équilibrée, dynamique, spéculative).",
        PageBreak(),
        "<i>Interprétation du signal</i>",
        make_volatility_regimes_table(),
        "Le signal sert de socle à la lecture des scénarios dynamiques, permet de pondérer les autres indicateurs (Return, Momentum, Signal) selon le contexte de volatilité et aide à détecter les changements de régimes, souvent annonciateurs de retournements majeurs.",
        "<b>AVERTISSEMENT</b> — 	Le Regime ne prédit pas l’avenir : il décrit l’état courant du risque, pas son évolution future. Il dépend de la qualité du profil historique (vol_profiles.parquet). Un échantillon trop court ou atypique peut biaiser le classement. Des actifs structurellement volatils (crypto, small caps) peuvent rester longtemps en “élevated” sans que ce soit anormal. Les transitions entre régimes peuvent être retardées par lissage (rolling window).",
        "<b>4.7 ADV10USD (Average Daily Dollar Volume – 10 jours)</b><a name='section_adv10'/>",
        "L’ADV10USD (Average Daily Dollar Volume sur 10 jours) représente la moyenne du montant en dollars réellement échangé chaque jour sur un actif au cours des dix dernières séances. Autrement dit, il mesure la liquidité opérationnelle d’un titre, c’est-à-dire sa capacité à absorber des volumes d’achat ou de vente sans provoquer de variation excessive de prix.",
        "Ce champ n’est pas calculé par le programme. En effet, il est récupéré depuis Yahoo Finance et stocké dans vol_profiles.parquet. Quand l’actif est coté dans une autre devise, le fournisseur calcule ou expose un équivalent en USD (via le FX du jour).",
        "<i>Interprétation de l'ADV10USD</i>",
        make_liquidity_table(),
        "C’est un indicateur essentiel pour évaluer la profondeur de marché et le risque d’exécution. Plus l’ADV est élevé, plus l’actif est liquide : il est alors possible de passer des ordres importants sans impact significatif. À l’inverse, un ADV faible traduit un marché étroit, où chaque transaction influence davantage le prix.",
         "<b>AVERTISSEMENT</b> — Cet indicateur ne reflète pas la liquidité “structurelle” à long terme : il est sensible aux événements récents (résultats d’entreprise, annonces macroéconomiques, nouvelles sectorielles) et doit être interprété avec prudence sur des périodes calmes ou atypiques.	L’ADV10 ne regarde que 10 séances, soit deux semaines de marché. Cela en fait un indicateur très réactif mais aussi instable : un seul jour de volume exceptionnel (par exemple à cause d’une publication de résultats ou d’une annonce de fusion) peut gonfler artificiellement la moyenne et donner une impression de liquidité durable alors qu’il s’agit d’un pic ponctuel.",
    ]),
    ("5. Comparaison CT↔LT<a name='section_comparaison'/>", [
        "Cette section compare les dynamiques de court terme (CT) et de long terme (LT) afin d’évaluer la cohérence ou la divergence des signaux de marché. L’objectif est d’identifier si un actif se situe dans une phase d’accélération, de stabilisation, ou au contraire de retournement.",
        "Les indicateurs mobilisés ici (∆Return (pp), Momentum Ratio, Volatility Ratio et Signal Stability) sont des mesures relatives, c’est-à-dire qu’ils normalisent les valeurs CT par rapport aux valeurs LT. Ils ne dépendent donc ni de l’unité de temps absolue, ni du type d’actif, et peuvent être comparés entre actions, indices, matières premières ou devises.",
        "Une cohérence CT↔LT traduit une tendance structurelle claire, tandis qu’une divergence prolongée peut signaler une rotation sectorielle, un épuisement de cycle ou un début de correction.",
        "<b>5.1 ∆Return (pp) — Variation de rendement</b><a name='section_dreturn'/>",
         "La variable ∆Return (pp) (delta return, en points de pourcentage) mesure l’écart entre le rendement moyen à court terme et le rendement moyen à long terme d’un actif. Autrement dit, elle capture l’accélération ou le ralentissement récent de la performance par rapport à la tendance de fond.",
         "C’est un indicateur différentiel de tendance :",
         "* un ∆Return positif indique que la performance récente s’est améliorée par rapport au régime de long terme (accélération du prix, reprise ou rallye) ;",
         "* un ∆Return négatif traduit au contraire un essoufflement ou une détérioration récente (correction, inversion, consolidation).",
         "La formule est simple et directe :",
         "<i> Delta Return(pp) = AvgReturn(%){CT} - AvgReturn(%){LT}</i>",
         "Autrement dit, la différence entre le rendement moyen court terme et le rendement moyen long terme, chacun calculé sur des fenêtres dynamiques distinctes définies plus haut dans le rapport",
         "<i>Interprétation de delta return</i>",
         make_return_delta_table(),
         "Cette approche assure que la comparaison reste cohérente avec la structure temporelle des données (qu’elles soient daily, weekly ou monthly) et que le signal s’adapte automatiquement à la longueur du jeu de données sans paramétrage manuel.",
         "Très visuel et intuitif : montre immédiatement si un actif est en phase d’accélération ou de décélération. L'indicateur permet également de valider la cohérence du momentum : si le momentum est positif mais que ∆Return est négatif, la tendance s’essouffle.",
         "<b>AVERTISSEMENT</b> — Sensible aux pics de volatilité ponctuels : un événement isolé peut artificiellement gonfler la variation à court terme. De plus, l'indicateur ne capture pas la persistance du mouvement (une forte hausse puis une forte baisse sur une courte période peut annuler le signal). La pertinence dépend de la profondeur de l’historique disponible : si la fenêtre long terme est trop courte, le contraste perd son sens.",
         PageBreak(),
         "<b>5.2 Momentum Ratio</b><a name='section_momentum_ratio'/>",
         "Le Momentum Ratio compare la force du momentum actuel à celle observée sur une période plus longue. C’est un indicateur relatif, qui permet de déterminer si la dynamique récente est en accélération, en stabilisation ou en perte de vitesse.",
         "Le momentum mesure la vitesse du mouvement des prix : c’est le rythme auquel un actif progresse ou recule. Le Momentum Ratio exprime donc le rapport de cette vitesse actuelle à celle du passé récent, permettant de voir si le mouvement s’amplifie ou s’épuise.",
         "* Un ratio supérieur à 1 indique une accélération du momentum : la tendance récente devient plus forte que la tendance de fond.",
         "* Un ratio inférieur à 1 indique une décélération : la dynamique faiblit par rapport au long terme.",
         "La formule utilisé dans le programme est la suivante:",
         "<i> Momentum ratio = Momentum{CT} / Momentum{LT}</i>",
         "Les deux valeurs de momentum (court terme et long terme) sont calculées dans le script à partir de fenêtres glissantes dynamiques, adaptées automatiquement à la fréquence détectée dans le jeu de données ",
         "<i> Interprétation du momentum ratio</i>",
         make_momentum_ratio_table(),
         "C'est un indicateur robuste et universel : fonctionne sur tous types d’actifs et toutes fréquences. Il permet de détecter les divergences : si le ratio s’effondre alors que le rendement reste positif, la tendance est en train de s’épuiser.",
         "Bien qu’il repose sur les mêmes variables de calcul que le Signal Stability (momentums court et long terme), le Momentum Ratio s’en distingue par son objectif : il mesure l’intensité relative du mouvement, là où le Signal Stability évalue la cohérence directionnelle entre horizons. Ces deux indicateurs sont donc complémentaires, car le premier renseigne sur la vitesse du changement et le second sur sa consistance structurelle.",
         "<b>AVERTISSEMENT</b> — Il est fortement influencé par la volatilité du momentum lui-même : des pics très courts peuvent fausser le ratio. De plus, si la tendance long terme est plate (momentum LT proche de zéro), le ratio peut être instable En outre, il ne permet pas de savoir dans quel sens (haussier ou baissier) le momentum s’accélère : il mesure uniquement l’intensité relative.",
         PageBreak(),
         "<b>5.3 Volatility Ratio</b><a name='section_volatility_ratio'/>",
         "Le Volatility Ratio mesure la variation relative du niveau de volatilité à court terme par rapport à son niveau de long terme. Une mesure de changement d’état du marché, indiquant si l’environnement devient plus instable ou au contraire plus apaisé.",
         "La volatilité traduit l’amplitude moyenne des variations de prix. En comparant la volatilité de court terme (V_CT) et de long terme (V_LT), on obtient une vision claire du regime shift :",
         "* Si le ratio augmente, le marché devient plus nerveux, plus réactif ;",
         "* S’il baisse, le marché revient à une phase de calme ou de compression.",
         "Cet indicateur est central pour identifier les quatre régimes utilisés ailleurs dans le rapport : subdued → normal → elevated → turbulent. La formule utilisé dans le programme est la suivante:",
         "<i> Volatility ratio = Volatility{CT} / Volatility{LT}</i>",
         "<i> Interprétation du volatility ratio</i>",
         make_volatility_ratio_table(),
         "C'est un indicateur structurel du régime de marché : il sert de base à la classification automatique (subdued, normal, elevated, turbulent). Il permet également de détecter les transitions avant qu’elles ne se matérialisent sur les prix (hausse de la volatilité → stress imminent).",
         "<b>AVERTISSEMENT</b> — Ne mesure que la variation relative de la volatilité, pas son niveau absolu : un ratio > 1 sur un actif peu volatil reste parfois insignifiant. Il est également important de noter qu'il peut être biaisé sur des historiques trop courts (si la volatilité LT est sous-estimée). Enfin, Sur des actifs illiquides, la volatilité CT peut être erratique et fausser le ratio. ",
         "<b>5.4 Bêta</b><a name='section_beta'/>",
         "Le Bêta (β) mesure la sensibilité du rendement d’un actif par rapport à un indice de référence (souvent le marché global). C’est un indicateur de corrélation directionnelle pondérée par la volatilité, qui exprime dans quelle mesure un actif amplifie ou atténue les mouvements du marché.",
         "Le bêta répond à une question simple :",
         "<i> « Si le marché bouge de 1 %, de combien mon actif bouge-t-il en moyenne ? »</i>",
         "* Un β > 1 indique que l’actif amplifie les mouvements du marché : il est plus volatil et réagit plus fortement aux fluctuations globales. ",
         "* Un β < 1 signifie que l’actif bouge moins que le marché : il est défensif ou faiblement corrélé.",
         "* Un β négatif traduit une corrélation inverse : l’actif évolue souvent en sens opposé du marché (cas rares, typiques des hedges ou de certaines matières premières).",
         PageBreak(),
         "Pour obtenir cet indicateur 2 options s'offrent à nous:",
         "* Le bêta n’est pas calculé directement dans le progranne, mais récupéré depuis le fichier vol_profiles.parquet, qui lui-même l’extrait via Yahoo Finance.",
         "* Quand Yahoo ne fournit pas de bêta (par exemple pour des actifs récents, des ETF exotiques ou des titres non US), le programme le calcule lui-même à partir des données de prix présentes dans sectors.parquet.",
         "Lorsqu’aucune valeur n’est disponible, le programme applique la formule statistique classique directement sur les rendements normalisés de l’actif et du benchmark choisi (souvent un indice large comme le S&amp;P 500 ou le MSCI World) :",
         "<i>β = Cov(R^actif, R^benchmark) / Var(R^benchmark) </i>",
         "où:",
         "* R^actif et R^benchmark sont les rendements logarithmiques sur une même période,",
         "* les deux séries sont alignées temporellement,",
         "* la covariance et la variance sont calculées sur la fenêtre dynamique correspondant au long terme (ex. window_vol_L).",
         "Cette approche permet d’obtenir un bêta cohérent avec la profondeur effective des données, tout en restant comparable aux valeurs issues de Yahoo.",
         "<i> Interprétation du bêta</i>",
         make_beta_table(),
         "C'est un indicateur universellement compris et comparable entre classes d’actifs. Non seulement il sert à pondérer le risque systémique et à ajuster la lecture du Risk-Adjusted Return, mais également d’identifier les biais structurels d’un portefeuille (défensif, offensif, neutre).",
         "<b>AVERTISSEMENT</b> — Le bêta dépend fortement de la période de calcul et de l’indice choisi : un même actif peut avoir un bêta différent selon le benchmark. Dans le cadre du marché equity, il ne capture pas les risques idiosyncratiques (internes à l’entreprise ou à l’actif). De plus, en phase de crise, les corrélations augmentent mécaniquement : les betas tendent à converger vers 1, réduisant leur pouvoir discriminant.",
    ]),
    ("6. Scénarios CT<a name='section_scenarios'/>", [
        "<b>6.1 Objectifs</b><a name='section_scenarios_objectif'/>",
        "Les scénarios CT (court terme) ont été introduits pour donner une lecture synthétique et narrative de l’état du marché, au-delà des chiffres bruts. Ils traduisent en langage analytique la combinaison dynamique entre rendement, momentum et volatilité, en identifiant des phases de marché typiques (ex. “rally sous tension”, “capitulation”, “rebond technique”…).",
        "Chaque scénario vise donc à rendre le diagnostic visuel et intuitif, tout en restant objectivement basé sur les données. L’intérêt est double :",
        "* fournir un contexte économique et comportemental à la situation actuelle du portefeuille ou de l’actif ;",
        "* aider à prioriser les observations (high impact, moderate impact, light impact) selon le niveau de risque et la robustesse du mouvement.",
        "<b>6.2 Principe de fonctionnement</b><a name='section_scenarios_fonctionnement'/>",
        "Les scénarios sont déterminés automatiquement à partir de trois dimensions clés :",
        "1. Return (R_label) : direction et intensité de la performance moyenne ;",
        "2. Momentum (M_label) : rythme d’évolution et cohérence de la tendance ;",
        "3. Volatility Regime (V_regime) : état du risque de marché (subdued → turbulent).",
        "Le moteur confronte ces trois axes via une série de règles hiérarchisées. La première condition rencontrée détermine le scénario principal, tandis que le niveau d’impact (light, moderate, high) est ajusté selon des facteurs de risque additionnels :",
        "* Liquidité (Liquidity_Label)",
        "* Effet de levier (Leverage_Label)",
        "* Sensibilité au marché (Beta_Label)",
        "La force des scénarios sont d'abord d’interpréter les chiffres (retour, volatilité, momentum) à travers des phénomènes concrets de marché, d'offrir une grille de lecture homogène entre actifs très différents (actions, ETF, matières premières, taux…) et ainsi détecter des phases critiques (stress, capitulation) et la confirmation des cycles haussiers (uptrend, compression de volatilité).",
        "<b>6.3 Logique de classification d'importance:</b><a name='section_scenarios_classification'/>",
        "* Liquidité thin / illiquid → tendance à déclasser un cran (high→moderate)",
        "* Leverage → tendance à hausser le risque (light→moderate, moderate→high)",
        "* Beta_Label très élevé → peut hausser le risque (moderate→high) ; defensive → peut baisser (high→moderate)",
        "<b>6.4 Valeurs possibles parmi les variables:</b><a name='section_scenarios_variables'/>",
        "* R_label (Return court terme) ∈ {strongly negative, negative, neutral, moderately positive, strong, very strong}",
        "* M_label (Momentum) ∈ {bearish, neutral, bullish, accelerating, accelerating+}",
        "* V_regime (Régime de volatilité) ∈ {subdued, normal, elevated, turbulent} <i>(Les labels dépendent des fenêtres dynamiques et de la fréquence détectée dans les données.)</i>",
        PageBreak(),
        "<b>7. Catalogue des scénarios </b><a name='section_catalogue'/>",
        "1. <b><i>Capitulation — [high]</i></b><a name='section_capitulation'/> ",
        "<u>Déclencheur</u>: R_label = strongly negative et V_regime = turbulent et M_label contient bearish.",
        "<u>Définition</u> : Vente panique avec volatilité extrême ; les flux se défont vite, la profondeur de carnet s’assèche.",
        "<u>À surveiller :</u>",
        "* Volatility Ratio en forte hausse ; ΔReturn très négatif",
        "* Signal_Stability souvent en reversal (divergence LT/CT)",
        "* Liquidité réelle (ADV10USD) pour éviter les pièges d’exécution",
        "2. <b><i>Stress — [high]</i></b><a name='section_stress'/>",
        "<u>Déclencheur</u>: R_label ∈ {strongly negative, negative} et V_regime ∈ {elevated, turbulent}.",
        "<u>Définition</u> : Dégâts marqués, mais pas nécessairement panique totale. Risque de prolongation.",
        "<u>À surveiller :</u>",
        "* Momentum Ratio < 1 (affaiblissement)",
        "* Volatility Ratio > 1.2 (expansion)",
        "* Réaction sur supports clés / newsflow",
        "3. <b><i>Momentum squeeze — [high]</i></b><a name='section_squeeze'/>",
        "<u>Déclencheur</u>: R_label = very strong et M_label ∈ {accelerating, accelerating+} et V_regime ∈ {elevated, turbulent}.",
        "<u>Définition</u> : Hausse explosive pilotée par le momentum sous forte volatilité ; sensible aux whipsaws.",
        "<u>À surveiller :</u>",
        "* Volatility Ratio élevé ; risques de short-covering",
        "* Signal_Stability cohérent mais fragile au retournement",
        "* Liquidité suffisante pour entrer/sortir",
        "4. <b><i>Rally under tension — [high]</i></b><a name='section_rally'/>",
        "<u>Déclencheur</u>: R_label ∈ {strong, very strong} et V_regime ∈ {elevated, turbulent}.",
        "<u>Définition</u> : Rally puissant mais nerveux ; la volatilité menace la pérennité du mouvement.",
        "<u>À surveiller :</u>",
        "* Momentum Ratio ≥ 1 (sinon “rally fatigué”)",
        "* Pullbacks violents possibles → gestion du risque stricte",
        "5. <b><i>Regular uptrend — [moderate]</i></b><a name='section_uptrend'/>",
        "<u>Déclencheur</u>: R_label ∈ {strong, very strong} et M_label ∈ {bullish, accelerating, accelerating+} et V_regime ∈ {subdued, normal}.",
        "<u>Définition</u> : Tendance haussière saine : gains, momentum porteur, volatilité contenue.",
        "<u>À surveiller :</u>",
        "* Signal_Stability “coherent” idéalement fort",
        "* Volatility Ratio ~ 1 (pas d’échauffement",
        PageBreak(),
        "6. <b><i>Loss of momentum — [moderate]</i></b><a name='section_loss_momentum'/>",
        "<u>Déclencheur</u>: “bearish” dans M_label et R_label ∉ {negative, strongly negative} et V_regime ∈ {normal, elevated}.",
        "<u>Définition</u> : Perte progressive d’élan ; risque de consolidation/rotation.",
        "<u>À surveiller :</u>",
        "* Momentum Ratio < 1 ; ΔReturn qui s’érode",
        "* Possibles divergences prix/momentum",
        "7. <b><i>Technical rebound — [moderate]</i></b><a name='section_rebound'/>",
        "<u>Déclencheur</u>: M_label ∈ {bullish, accelerating, accelerating+} et R_label ∈ {negative, neutral}.",
        "<u>Définition</u> : Rebond technique sans validation des rendements ; phase de test.",
        "<u>À surveiller :</u>",
        "* Signal_Stability (cohérence CT/LT ?)",
        "* Besoin de passage de R_label en positif pour confirmation",
        "8. <b><i>Gradual decline — [moderate]</i></b><a name='section_gradual_decline'/>",
        "<u>Déclencheur</u>: R_label = negative et V_regime ∈ {subdued, normal} et M_label contient bearish.",
        "<u>Définition</u> : Baisse “en marche” sans panique ; pressions persistantes.",
        "<u>À surveiller :</u>",
        "* Volatility Ratio ≤ 1.0 (baisse “ordonnée”)",
        "* Ruptures de supports progressives",
        "9. <b><i>Volatility compression — [light]</i></b><a name='section_vol_compress'/>",
        "<u>Déclencheur</u>: V_regime = subdued et M_label ∈ {neutral, bullish} et R_label ∈ {neutral, moderately positive}.",
        "<u>Définition</u> : Compression de volatilité ; potentiel “setup” de breakout.",
        "<u>À surveiller :</u>",
        "* Cassure de range ; Signal_Stability en amélioration",
        "* Saut du Volatility Ratio post-break (volatilité peut augmenter fortement juste après que le prix ait franchi un niveau clé)",
        "10. <b><i>Volatility expansion — [moderate]</i></b><a name='section_vol_expand'/>",
        "<u>Déclencheur</u>: V_regime ∈ {elevated, turbulent} et |AvgReturn(%)| < 0.2 et M_label = neutral.",
        "<u>Définition</u> : Volatilité qui s’ouvre sans direction (choppy) ; faux signaux fréquents.",
        "<u>À surveiller :</u>",
        "* Attendre un biais clair via R_label/M_label",
        "* Éviter l’over-trading",
        PageBreak(),
        "11. <b><i>Stabilization after shock — [moderate]</i></b><a name='section_stabilizing'/>",
        "<u>Déclencheur</u>: V_regime = elevated et R_label = neutral et M_label ∈ {neutral, bullish}.",
        "<u>Définition</u> : Décrue de la nervosité après choc ; phase de respiration",
        "<u>À surveiller :</u>",
        "* Volatility Ratio qui reflue vers 1",
        "* Confirmation par ΔReturn redevenant positif",
        "12. <b><i>Distribution — [moderate]</i></b><a name='section_distribution'/>",
        "<u>Déclencheur</u>: R_label ∈ {strong, moderately positive} et M_label contient bearish et V_regime ∈ {normal, elevated}.",
        "<u>Définition</u> : Prise de profits / essoufflement de tendance ; risque de rotation.",
        "<u>À surveiller :</u>",
        "* Momentum Ratio < 1 ; divergences",
        "* Passage de R_label vers neutral puis negative",
        "13. <b><i>Range / noise — [light]</i></b><a name='section_range'/>",
        "<u>Déclencheur</u>: (aucune règle précédente ne s’applique).",
        "<u>Définition</u> : Marché latéral / bruit ; alternance de micro-mouvements sans tendance claire.",
        "<u>À surveiller :</u>",
        "* Volatility Ratio proche de 1 ; Signal_Stability souvent neutre",
        "* Stratégies adaptées (mean-reversion, stock-picking)",
        "",
        "",
        "Les treize scénarios CT définis dans le moteur constituent une cartographie complète et équilibrée des régimes de marché. Ils couvrent toutes les configurations pertinentes issues de la combinaison du rendement (Return), du momentum et du régime de volatilité, depuis les phases de panique (capitulation, stress) jusqu’aux phases de reprise ou de neutralité (uptrend, range). Ce nombre a été choisi pour assurer un équilibre entre précision analytique et lisibilité : chaque scénario reste distinct et interprétable, sans redondance ni complexité excessive. Au-delà de ce seuil, la multiplication des cas n’apporterait qu’une fausse granularité, au détriment de la clarté et de la cohérence globale du diagnostic.",
    ]),
    ("8. Visualisations & limites<a name='section_visualisations'/>", [
        "<b>8.1 Nombre de tickers </b><a name='section_tickers'/>",
        "Le rapport s’adapte dynamiquement au nombre d’actifs sélectionnés : toutes les visualisations, analyses et interprétations sont générées automatiquement, sans limite technique prédéfinie. Cependant, dans un souci de lisibilité et de cohérence graphique, il est recommandé de limiter le nombre de tickers à 10 à 20 pour une analyse sectorielle ciblée, et à 40 à 50 pour une analyse de portefeuille complète. Au-delà de ces seuils, la qualité visuelle et la clarté de lecture peuvent se dégrader, sans pour autant empêcher la génération du rapport.",
        "<b>8.2 Recommandations sur les dimensions des fenêtres d'observations </b><a name='section_fenetres_reco'/>",
        "Les fenêtres dynamiques s’ajustent automatiquement selon la fréquence d’analyse (daily, weekly, monthly, yearly). Cependant, afin de garantir la stabilité statistique des indicateurs (Return, Momentum, Volatility), certaines bornes sont recommandées :",
        "<i>Recommandation des bornes selon la fréquences d'analyse</i>",
        make_dynamic_windows_table(),
        "<b>8.3 Résolution temporelle et qualité des données </b><a name='section_resolution'/>",
        "Les prix utilisés dans le rapport proviennent de Yahoo Finance, une source fiable et largement reconnue pour les grandes capitalisations et les ETF liquides.Pour ces actifs, la précision des ajustements (dividendes, splits, variations de clôture) est considérée comme excellente et adaptée à une analyse quantitative.",
        "Cependant, pour les petites capitalisations (inférieures à 2 milliards USD) ou les actifs récents et faiblement échangés, des irrégularités ponctuelles peuvent apparaître (valeurs manquantes, ajustements retardés, dates décalées). Ces anomalies n’affectent pas la structure du rapport mais peuvent altérer légèrement certains indicateurs glissants (volatilité, momentum court terme, ΔReturn).",
        "<i> Recommandation : effectuer un contrôle visuel préalable des séries de prix pour tout actif dont la capitalisation est inférieure à 2 milliards USD, avant intégration dans le rapport.</i>",
        "<b>8.4 Biais de fréquence et agrégation</b><a name='section_biais_frequence'/>",
        "Les indicateurs sont recalculés pour chaque fréquence (Daily, Weekly, Monthly, Yearly). → Un changement de fréquence modifie mécaniquement les rendements, les volatilités et les corrélations, car les fenêtres d’observation et la granularité temporelle ne sont plus comparables.",
        "<i>Recommandation : ne pas comparer directement deux rapports de fréquences différentes sans annualisation préalable des indicateurs, afin de ramener toutes les mesures à une base temporelle commune. </i>",
        "<i> Formules d’annualisation par fréquence </i>",
        make_annualisation_table(),
        PageBreak(),
        "<b>8.5 Sensibilité aux valeurs extrêmes</b><a name='section_extremes'/>",
        "Certains indicateurs (comme le Momentum ou le ΔReturn) peuvent être fortement influencés par des variations ponctuelles sur de très courtes périodes. → Cela peut fausser la perception d’un scénario si un événement exceptionnel (earnings, news, crise) intervient dans la fenêtre d’analyse.",
        "<i> Recommandation : interpréter les résultats récents avec prudence et croiser avec d’autres horizons.</i>"
    ]),
     ("9. Mentions et précisions<a name='section_mentions'/>", [
      "<b>9.1 Facteurs d'échelle par classe d’actif (*)</b><a name='section_facteurs_echelle'/>",
      "Ce tableau présente les facteurs de mise à l’échelle appliqués aux principaux indicateurs dynamiques (Return, Volatility, Momentum) selon la nature de l’actif analysé. L’objectif est de garantir une lecture cohérente et comparable des indicateurs entre classes d’actifs hétérogènes : une variation de ±1 % n’a pas la même portée économique sur une paire de devises que sur un indice actions ou une matière première. Ces coefficients multiplicatifs permettent donc de ramener chaque mesure à une base “actions/indices”, utilisée comme référence (facteur = 1.0).",
      "Les indicateurs conncernés:",
      "* Return (%)",
      "* Volatility (%)",
      "* Momentum (%)",
      "* ∆Return (pp)",
      "",
      make_asset_classes_table(),
      "<b>AVERTISSEMENT</b> — Le tableau d’échelle ci-dessous ne doit pas être appliqué aux produits à levier (ETF x2, x3, etc.), ni aux instruments dérivés dont le levier structurel modifie la volatilité ou le rendement. Dans ces cas, la pondération du levier doit primer sur le facteur d’échelle associé à la classe d’actif. Par exemple, un ETF x3 sur le Nasdaq conservera le facteur d’échelle “Actions = 1.0”, mais son levier effectif multipliera par 3 les valeurs de Return et de Volatility.",
      "",
      "<b>9.2 Glossaire des termes techniques</b><a name='section_glossaire'/>",
      "Ce glossaire regroupe les principaux termes techniques et expressions utilisés dans le rapport. Il vise à clarifier les notions financières et comportementales associées aux dynamiques de marché, afin de faciliter la lecture et l’interprétation des indicateurs.",
      "",
      glossary_table
    ]),
]

BLOCKS_EN = [
    ("Introduction", [
    "This appendix accompanies the Portfolio rotation report and presents the technical, methodological, and interpretive foundations of the model. It describes the structure of the data files, the functioning of dynamic windows, the calculation formulas of key indicators, and the interpretive logic used in the tables and scenarios of the main report. The objective is to ensure methodological transparency, reproducibility of results, and a clear understanding of the signals generated by the program, regardless of the asset type or time horizon considered.",
    ]),
    ("1. Objective & Scope<a name='section_objective_en'/>", [
        "The purpose of this report is to <b>describe and interpret the state of a given asset universe</b>, whether equities, indices, ETFs, or other instruments. It aims to <b>identify phases of rotation, tension, or stabilization</b> through the combined analysis of returns, volatility, momentum, and their coherence across short- and long-term horizons. The report therefore provides a <b>synthetic, structured, and interpretable overview</b> of market regimes, composition biases, and risk conditions, facilitating <b>global diagnosis and decision-making</b>.<a name='section_goals_en'/>",
        "* Sources: <i>sectors.parquet</i>, <i>vol_profiles.parquet</i>, <i>constituents.csv</i>.",
        "<u>sectors.parquet:</u> The <i>sectors.parquet</i> file contains the historical prices of the assets used in the analysis. The program uses it to compute returns, volatility, and momentum over different time windows (short- and long-term). In practice, this is the primary database from which all indicators, correlations, and rankings presented in the report are derived.<a name='section_datafiles_en'/>",
        "<u>vol_profiles.parquet:</u> The <i>vol_profiles.parquet</i> file contains structural and qualitative information for each asset: volatility profile, market regime, liquidity, leverage, beta, asset class, market capitalization, etc. These data are not derived from time-series calculations but from prior statistical profiling or long-term structural analysis. Complementing <i>sectors.parquet</i>, it provides a macro and contextual interpretation layer useful for understanding the expected behavior of each asset (e.g., “dynamic,” “speculative,” “defensive”). The two files are kept separate to distinguish raw data (price history) from descriptive metadata (risk profile). This separation makes the model more modular, readable, and reusable while avoiding unnecessary recalculation or duplication of information during market data updates.",
        "<u>constituents.csv:</u> The <i>constituents.csv</i> file contains the reference list of analyzed assets, including their symbols, full names, and GICS classifications (sector, industry, etc.). It does not provide market data or computed metrics, but rather a descriptive mapping that identifies each entry in <i>sectors.parquet</i> and links tickers to their corresponding economic or thematic sector. This file therefore acts as a bridge between numerical data and their economic context, essential for generating comments on diversification, sector bias, and macro coverage. It is kept separate to maintain a clear and easily updatable structure (e.g., when a company changes sector or ticker symbol without affecting its historical series).",
        "<b>WARNING</b> — <i>constituents.csv</i> file: This file was created manually and is not automatically updated. Before running the program, the user must verify that all assets included in the analysis are properly listed in this file with the correct symbol and classification (GICS sector, sub-industry, etc.). If any assets are missing, they must be added manually to ensure the consistency of the report and the correct generation of sector-related comments.",
    ]),
    ("Summary", [
        table_en,
        PageBreak()
    ]),
    ("2. Windows & Frequency<a name='section_windows_frequency_en'/>", [
        "<b>2.1 Dynamic Windows</b>.<a name='section_dynamic_windows_en'/>",
        "Dynamic windows are a central component of the project: they allow the analysis periods (volatility, return, momentum) to automatically adjust to the dataset’s frequency and depth.",
        
        "<b>2.2 Purpose</b><a name='section_windows_goal_en'/>",
        "The goal is to avoid a fixed calibration (e.g., 20 days for everything), which would be inconsistent when switching between daily, weekly, or monthly data. The program instead computes window sizes proportional to the total number of available observations, ensuring that indicators remain comparable and economically coherent across all horizons.",
        
        "<b>2.3 Functioning</b><a name='section_windows_mechanics_en'/>",
        "1. The data frequency is first detected automatically (Daily, Weekly, Monthly, etc.).",
        "2. Based on this frequency, a base window size is set (e.g., 20 for daily, 4 for weekly, 3 for monthly).",
        "3. This base is then dynamically adjusted according to the total number of data points:",
        "* Short-term (CT) windows typically cover about 10% to 30% of the historical series.",
        "* Long-term (LT) windows extend up to roughly 85% to 90% of the series.",
        "4. Safeguards prevent the use of excessively short or long windows (minimum 3 points, maximum n−5).",
        
        "<b>2.4 Distinct Windows per Indicator</b>.<a name='section_windows_distinction_en'/>",
        "•  Volatility: requires a shorter, more reactive window since it measures the instantaneous dispersion of returns.",
        "•  Return: uses an intermediate window, representative of the average behavior over a meaningful period.",
        "•  Momentum: requires a longer window, as it reflects cumulative trends and must avoid overly noisy signals.",
        
        "<b>WARNING</b> — For datasets that are too short, dynamic windows mechanically become too small, increasing the volatility of computed indicators. They do not replace expert economic judgment: 'optimal' windows may vary depending on the nature of the assets (e.g., crypto vs. bonds). Finally, while the dynamic approach ensures structural robustness, it limits cross-study comparability if the underlying data depth differs significantly."
    ]),
    ("3. Portfolio Structure & Macroeconomic Profile<a name='section_portfolio_structure_en'/>", [
        "<b>3.1 Purpose</b><a name='section_structure_goal_en'/>",
        "The <i>Portfolio Composition</i> section aims to present the initial structure of the analyzed portfolio by identifying its sector allocation, capitalization biases, and main areas of concentration. It provides a static and macroeconomic context from which subsequent dynamics (returns, volatility, regimes) will be interpreted.",
        
        "<b>3.2 Functioning</b><a name='section_structure_mechanics_en'/>",
        "The <i>Portfolio Composition</i> block relies on metadata from <i>constituents.csv</i> and structural profiles from <i>vol_profiles.parquet</i>. Each portfolio line is mapped to a sectoral category (GICS), then aggregated as a relative weight, either:",
        "* equally weighted (weight = 1/n),",
        "* or weighted by market capitalization when available.",
        
        "<b>3.3 Analytical usefulness</b><a name='section_structure_usefulness_en'/>",
        "Before analyzing performance or signals, it is essential to understand what the portfolio is invested in sectors, defensive biases, or overweight exposures. Indeed, a portfolio highly concentrated in three or four sectors, or dominated by mega-caps, does not react the same way as a balanced basket. This section allows assessment of whether the observed market dynamics (momentum, volatility, rotation) stem from the portfolio’s construction or from external macro factors.",
        
        "<b>3.4 Functioning of the Macro Profile Insight Module</b><a name='section_macro_profile_insight_en'/>",
        "The automatic <i>Macro Profile Insight</i> commentary relies on a multi-level analytical logic combining descriptive (sectoral) information with structural (quantitative) profiles to produce a coherent synthesis of the portfolio’s stance. This interpretative engine operates from two main datasets:",
        "* <i>constituents.csv</i>: GICS classification and nominal composition of the portfolio;",
        "* <i>vol_profiles.parquet</i>: structural metadata (volatility, beta, liquidity, market capitalization, leverage, asset type, etc.).",
        
        "The module first analyzes sector diversification based on GICS labels. The number of distinct sectors determines the degree of macroeconomic coverage:",
        "* A single sector → extreme concentration, dependency on a single macro driver;",
        "* Three to five sectors → partial coverage, strong thematic bias;",
        "* Eight to ten sectors → balanced diversification, close to a global benchmark.",
        
        "Absent sectors are then identified to infer implicit biases:",
        "* Absence of Energy or Commodities → lack of inflation protection;",
        "* Absence of Healthcare or Consumer Staples → weak defensive component;",
        "* Absence of Technology or Communication → anti-growth bias.",
        
        "The engine then analyzes structural profiles from <i>vol_profiles.parquet</i> to complete the interpretation:",
        "* <b>Market Cap Label:</b> detects mega/large-cap tilts (stability, low idiosyncrasy) or small/micro-cap tilts (higher convexity, increased volatility).",
        "* <b>Asset Type:</b> measures the proportion of ETFs, REITs, or ADRs to identify the nature of exposure (indirect, real estate, geographic).",
        "* <b>Liquidity Label & ADV10USD:</b> assesses the liquidity stance (e.g., ample trading liquidity, pockets of thin/illiquid names).",
        "* <b>Beta Label & Leverage Label:</b> describes systematic sensitivity and any leverage effects present.",
        "* <b>Volatility Profile:</b> defines the portfolio’s overall style (balanced, defensive, or speculative).",
        
        "The purpose of <i>Macro Profile Insight</i> is not to assess performance but to characterize the portfolio’s structural stance prior to any dynamic interpretation.",
        
        "<b>WARNING</b> — The information presented in this section is based on the portfolio composition as declared at the time of analysis and on categorizations from <i>constituents.csv</i> and <i>vol_profiles.parquet</i>. It does not necessarily reflect real-time weights, indirect economic exposures, or recent portfolio adjustments.",
    ]),
    ("4. Key Indicators<a name='section_indicators_en'/>", [
        "This section presents the core indicators used in the model, which are Return, Volatility, Momentum, Risk-Adjusted Return, Signal Stability, Volatility Regime, and ADV10USD. Each captures a specific dimension of market dynamics: performance, risk, consistency, or liquidity. Together, they form the analytical foundation on which the report’s interpretations and scenarios are built.",

        "<b>4.1 Return / R (%)</b><a name='section_return_en'/>",
        "Return measures the average performance of an asset over a given period. It is the foundation of all market analysis, indicating both direction and intensity of price movement. It enables time-normalized comparison of assets or sectors regardless of volatility or momentum levels.",
        "The average return (AvgReturn %) is computed over a dynamic rolling window whose size depends on the detected data frequency. This ensures that calculation sensitivity adapts to historical depth and typical market volatility.",
        "* The program first computes logarithmic returns between two consecutive observations (making variations additive over time).",
        "* These returns are then aggregated over a moving window; its size varies by frequency (≈ 20 days for daily, ≈ 4 weeks for weekly, etc.). The longer the frequency, the wider the window, smoothing noise while capturing dominant trends.",
        "* The total return over the window is converted into an average percentage per period, providing an intuitive measure of how much the asset gains or loses on average per observation period.",
        "<i>Return interpretation by horizon (*)</i>",
        make_thresholds_table_en(),
        "Return is the report’s pivot: it feeds the other indicators (momentum, ratios, scenarios), frames the economic reading of cycles (rally, correction, rebound, etc.), and serves as a comparative benchmark in identifying stress phases or sector rotation. Without Return, directionality and consistency analysis would be impossible.",
        "<b>WARNING</b> — Return says nothing about risk: a high return may come with high volatility. It can be misleading over short horizons, especially after one-off events (earnings, news, etc.). It does not reflect persistence: frequent back-and-forth swings can yield a near-zero average return even in a very active market. The mean return is not annualized, as it captures local dynamics, not one-year performance.",
        PageBreak(),

        "<b>4.2 Volatility / V (%)</b><a name='section_volatility_en'/>",
        "Volatility measures the average amplitude of price fluctuations over a given period. It is an indicator of risk and instability, complementary to return: while Return shows direction, Volatility reflects nervousness. It helps assess an asset’s regularity, shock sensitivity, and ability to sustain a stable trend. In this report, volatility plays a central role in interpreting market regimes (subdued, normal, elevated, turbulent).",
        "Volatility is computed using the same dynamic rolling-window logic as Return and Momentum:",
        "* The program computes the statistical dispersion (standard deviation) of logarithmic returns over a moving window.",
        "* Window length depends on analysis frequency: the higher the frequency, the shorter the window (≈ 20 days daily, ≈ 4 weeks weekly, ≈ 3 months monthly, etc.).",
        "* The result is expressed as an average percentage per period, providing comparable scales across assets and horizons.",
        "This dynamic approach keeps short-term volatility reactive while preserving long-term structural readability. It adapts automatically to available historical depth, preventing arbitrary fixed windows from distorting comparability across assets.",
        "<i>Volatility interpretation by horizon (*)</i>",
        make_volatility_table_en(),
        "Volatility identifies the overall risk regime in which the portfolio operates; it determines the likelihood of trend change, momentum stability, and short-term signal coherence. It also underpins Risk-Adjusted Return and drives the classification of market scenarios (capitulation, stress, uptrend, etc.).",
        "<b>WARNING</b> — Volatility measures neither direction nor future performance: a bullish market can be highly volatile, and a bearish one can be stable. A temporary decline in volatility does not always mean reduced risk, and it may precede a breakout. Over short series, statistical instability may occur, especially when returns show jumps or irregular extremes.",

        "<b>4.3 Momentum / M (%)</b><a name='section_momentum_en'/>",
        "Momentum measures the directional persistence of price movement over a given period. While Return captures average performance, Momentum describes the coherence and speed of the move whether the market advances steadily or oscillates indecisively. It is key to detecting acceleration, exhaustion, or trend reversal phases.",
        "Momentum (M %) is computed over a dynamic rolling window adjusted to data frequency:",
        "* When the window has 4 points or fewer (typically daily / weekly), sample size is too small for a meaningful average. In this case, the program sums the logarithmic returns, a raw accumulation of consecutive variations. This keeps the signal responsive: on very short horizons, each individual change carries weight, and normalizing by w would dampen true amplitude.",
        "* When the window exceeds 4 points, raw summation loses relevance as returns offset each other. The program then uses the geometric mean of logarithmic returns, expressing the average rate of price progression per time unit while neutralizing window-length effects.",
        "* The result is normalized by window size to yield an average per time unit.",
        "This hybrid approach preserves consistency of momentum across horizons without sacrificing precision on short ones.",
        PageBreak(),
        "<i>Momentum interpretation by horizon (*)</i>",
        make_momentum_table_en(),
        "Momentum complements Return: it indicates not absolute direction but relative strength. An asset may show positive return yet weak momentum (trend fatigue) or negative return with improving momentum (technical rebound).",
        "<b>WARNING</b> — Momentum is timing-sensitive: too short a window amplifies noise; too long a window hides fresh signals. It ignores volatility level and a fast move may reflect panic as much as conviction. A very high momentum is not automatically bullish: it can mean overheating or imminent reversal. Momentum should therefore always be read together with Volatility and Return to confirm consistency or detect divergences.",
        
        "<b>4.4 Risk-Adjusted Return / RAR</b><a name='section_rar_en'/>",
        "The Risk-Adjusted Return (RAR) measures average performance relative to risk level, represented here by volatility. It is a simplified, intuitive Sharpe-ratio-type metric assessing efficiency: how much return an asset generates per unit of volatility. It enables comparison across very different profiles on a homogeneous basis. A high RAR means strong compensation for risk; a low or negative RAR implies inefficient or risky performance.",
        "In the program, RAR is computed as:",
        "<i>RAR = AvgReturn (%)  /  Volatility (%)</i>",
        "* Both values use the same dynamic windows as the base indicators.",
        "* It is not annualized and it reflects instantaneous efficiency rather than long-term performance ratio.",
        "* The result is unit-free (pure ratio) and centered around 0.",
        "<i>Risk-Adjusted Return interpretation</i>",
        make_efficiency_table_en(),
        "RAR provides a direct reading of return-to-risk balance, automatically adapting to frequency and data depth. It is independent of absolute return scale: it expresses quality rather than quantity.",
        "<b>WARNING</b> — RAR ignores correlations with other assets (it is not a portfolio metric), is insensitive to asymmetric or fat-tailed distributions, and can be misleading in low-volatility phases when performance is temporarily high. An asset with high β may show strong RAR simply due to market amplification. For a fairer view, interpret RAR in light of beta sensitivity (β) and the asset’s volatility profile.",
        PageBreak(),

        "<b>4.5 Signal Stability</b><a name='section_signal_stability_en'/>",
        "Signal Stability measures the consistency between short-term momentum and long-term momentum. It indicates to what extent recent dynamics confirm or contradict the dominant market direction. This indicator qualifies the reliability of the ongoing move whether the signal is coherent, fragile, or reversing.",
        "In the program, Signal Stability is computed as:",
        "<i>Signal = (Momentum × Momentum_LT) / (|Momentum| + |Momentum_LT| + ε)</i>",
        "<i>(with ε ≈ 10e-6 to avoid division by zero)</i>",
        "The result is a normalized index between −1 and +1:",
        "* +1 → perfect coherence (short- and long-term momentum aligned)",
        "* 0 → no clear relation or weak contradictory signals",
        "* −1 → full divergence (strong trend reversal)",
        "<i>Signal interpretation</i>",
        make_signal_table_en(),
        "This signal helps detect market phase transitions (bull → bear or vice versa), validates momentum / return consistency, and anchors scenario classification (coherence, distribution, stress, etc.).",
        "<b>WARNING</b> — May become unstable on very short series (insufficient points for LT momentum), cannot distinguish volatile spikes from genuine reversals (cross-check with volatility), and its [−1, +1] range is qualitative rather than probabilistic, it is structural, not predictive.",

        "<b>4.6 Volatility Regime</b><a name='section_volatility_regime_en'/>",
        "The Regime reflects the market’s overall state through the level and dynamics of volatility. It is a qualitative typology describing the risk environment in which the asset or portfolio evolves (calm, normal, tense, or chaotic). Its purpose is to provide an intuitive reading of dominant volatility phases rather than a raw numeric value.",
        "The Regime is derived from <i>vol_profiles.parquet</i>, which aggregates the historical analysis of each asset’s average volatility. Each record contains structural information used to classify its profile.",
        "Computation of Regime relies on the ratio between two volatility horizons:",
        "* vol_short – volatility on the short-term window (e.g. 20 days daily, 4 weeks weekly);",
        "* vol_long – smoothed volatility on the long window (e.g. 6–10 × longer).",
        "The resulting ratio produces automatic classification into volatility profiles (defensive, balanced, dynamic, speculative).",
        PageBreak(),
        "<i>Volatility regime interpretation</i>",
        make_volatility_regimes_table_en(),
        "This signal forms the foundation for dynamic scenario analysis, weighting the other indicators (Return, Momentum, Signal) according to the volatility context and helping detect regime shifts often preceding major reversals.",
        "<b>WARNING</b> — The Regime is descriptive, not predictive: it captures current risk conditions, not future changes. It depends on the quality of historical profiling (<i>vol_profiles.parquet</i>). A short or biased sample may distort classification. Structurally volatile assets (e.g. crypto, small caps) may stay in “elevated” for extended periods without being abnormal. Regime transitions may lag due to window smoothing.",

        "<b>4.7 ADV10USD (Average Daily Dollar Volume – 10 days)</b><a name='section_adv10_en'/>",
        "ADV10USD represents the average dollar amount traded daily over the last ten sessions. In other words, it measures an asset’s operational liquidity and its ability to absorb buy / sell volumes without causing excessive price impact.",
        "This field is not computed by the program; it is retrieved from Yahoo Finance and stored in <i>vol_profiles.parquet</i>. For non-USD listings, the provider converts or exposes an equivalent in USD using the current FX rate.",
        "<i>ADV10USD interpretation</i>",
        make_liquidity_table(),
        "It is a key indicator for assessing market depth and execution risk. The higher the ADV, the more liquid the asset with large orders can be executed with limited impact. Conversely, a low ADV indicates a thin market where each transaction influences price more heavily.",
        "<b>WARNING</b> — This metric does not reflect long-term structural liquidity: it is sensitive to recent events (earnings, macro announcements, sector news) and should be interpreted cautiously in quiet or atypical periods. ADV10 covers only ten sessions (~ two weeks of trading). It is highly reactive but also unstable, as a single exceptional volume day (e.g. earnings release or merger news) can inflate the average and create a false impression of lasting liquidity.",
    ]),
    ("5. Short-Term vs Long-Term Comparison<a name='section_comparison_en'/>", [
        "This section compares short-term (CT) and long-term (LT) dynamics to evaluate the coherence or divergence of market signals. The goal is to determine whether an asset is in a phase of acceleration, stabilization, or reversal.",
        "The indicators used here (∆Return (pp), Momentum Ratio, Volatility Ratio, and Signal Stability) are relative measures: they normalize CT values against LT values. As a result, they are independent of absolute time units or asset types and can be compared across equities, indices, commodities, or currencies.",
        "CT↔LT coherence indicates a clear structural trend, while prolonged divergence may reveal sector rotation, cycle exhaustion, or the onset of a correction.",

        "<b>5.1 ∆Return (pp) — Return Variation</b><a name='section_delta_return_en'/>",
        "The ∆Return (pp) variable (delta return, in percentage points) measures the gap between an asset’s short-term and long-term average returns. In other words, it captures the recent acceleration or slowdown in performance relative to the broader trend.",
        "It is a differential trend indicator:",
        "* A positive ∆Return indicates improved recent performance versus the long-term regime (price acceleration, rebound, or rally).",
        "* A negative ∆Return indicates deterioration or loss of momentum (correction, pullback, consolidation).",
        "The formula is straightforward:",
        "<i>∆Return (pp) = AvgReturn(%) {CT} − AvgReturn(%) {LT}</i>",
        "That is, the difference between short-term and long-term average returns, each computed over distinct dynamic windows defined earlier in the report.",
        "<i>∆Return interpretation</i>",
        make_return_delta_table_en(),
        "This approach ensures that comparisons remain coherent with the dataset’s temporal structure (daily, weekly, or monthly) and that the signal automatically adapts to sample length without manual tuning.",
        "Highly visual and intuitive, it immediately shows whether an asset is accelerating or decelerating. It also validates momentum consistency: if momentum is positive but ∆Return is negative, the trend is weakening.",
        "<b>WARNING</b> — Sensitive to short-lived volatility spikes: a single event may artificially inflate short-term variation. The indicator also ignores persistence (a sharp rise followed by a sharp drop may cancel out the signal). Its relevance depends on historical depth, as if the LT window is too short, the contrast loses meaning.",
        PageBreak(),

        "<b>5.2 Momentum Ratio</b><a name='section_momentum_ratio_en'/>",
        "The Momentum Ratio compares current momentum strength to that observed over a longer period. It is a relative indicator showing whether recent dynamics are accelerating, stabilizing, or weakening.",
        "Momentum measures the speed of price movement, the pace at which an asset rises or falls. The Momentum Ratio therefore expresses the relationship between present and past speed, highlighting whether motion is intensifying or fading.",
        "* A ratio > 1 indicates accelerating momentum, the recent trend is stronger than the long-term one.",
        "* A ratio < 1 indicates deceleration, the current dynamic is weaker than the historical baseline.",
        "The formula used in the program is:",
        "<i>Momentum Ratio = Momentum {CT} / Momentum {LT}</i>",
        "Both momentum values (short- and long-term) are computed from dynamic rolling windows automatically adjusted to detected frequency.",
        "<i>Momentum ratio interpretation</i>",
        make_momentum_ratio_table_en(),
        "This is a robust, universal indicator that works across all asset classes and frequencies. It reveals divergences: if the ratio collapses while return remains positive, the trend is losing strength.",
        "Although it relies on the same variables as Signal Stability (short- and long-term momentum), its purpose differs: the Momentum Ratio measures <i>relative intensity</i> of motion, whereas Signal Stability evaluates <i>directional coherence</i> across horizons. The two are therefore complementary: one describes speed, the other consistency.",
        "<b>WARNING</b> — Strongly influenced by momentum volatility itself: brief spikes may distort the ratio. If long-term momentum is flat (near zero), the ratio becomes unstable. It also provides no directional information (bullish vs bearish); it only measures relative strength.",
        PageBreak(),

        "<b>5.3 Volatility Ratio</b><a name='section_volatility_ratio_en'/>",
        "The Volatility Ratio measures the relative change in short-term versus long-term volatility levels. It is a gauge of market-state transition, showing whether the environment is becoming more unstable or calming down.",
        "Volatility reflects the average amplitude of price movements. Comparing short-term volatility (V_CT) with long-term volatility (V_LT) reveals regime shifts:",
        "* When the ratio rises, the market grows more nervous and reactive.",
        "* When it falls, the market re-enters a calm or compressed phase.",
        "This indicator is central to identifying the four regimes used elsewhere in the report: subdued → normal → elevated → turbulent. The program uses the following formula:",
        "<i>Volatility Ratio = Volatility {CT} / Volatility {LT}</i>",
        "<i>Volatility ratio interpretation</i>",
        make_volatility_ratio_table_en(),
        "It is a structural indicator of the market’s risk regime and forms the basis of the automatic classification (subdued, normal, elevated, turbulent). It can also anticipate transitions before they appear in prices (rising volatility → incoming stress).",
        "<b>WARNING</b> — Measures only relative change, not absolute level: a ratio > 1 on a low-volatility asset may be insignificant. It can be biased on short histories (if LT volatility is underestimated). On illiquid assets, short-term volatility can behave erratically and distort the ratio.",

        "<b>5.4 Beta (β)</b><a name='section_beta_en'/>",
        "Beta (β) measures an asset’s sensitivity to a reference index (usually the overall market). It is a directionally weighted correlation indicator expressing how much an asset amplifies or dampens market movements.",
        "Beta answers a simple question:",
        "<i>“If the market moves 1 %, by how much does my asset move on average?”</i>",
        "* β > 1 → the asset amplifies market moves: more volatile and reactive to global fluctuations;",
        "* β < 1 → the asset moves less than the market: defensive or weakly correlated;",
        "* β < 0 → inverse correlation: the asset often moves opposite to the market (rare; typical of hedges or some commodities).",
        PageBreak(),
        "There are two ways to obtain this indicator:",
        "* Beta is not always computed directly by the program but can be retrieved from <i>vol_profiles.parquet</i>, which itself sources it from Yahoo Finance.",
        "* When Yahoo does not provide a beta (e.g. for recent assets, exotic ETFs, or non-US listings), the program computes it from price data in <i>sectors.parquet</i>.",
        "When no external value is available, the program applies the standard statistical formula directly to normalized returns of the asset and its chosen benchmark (commonly S&amp;P 500 or MSCI World):",
        "<i>β = Cov(R_asset, R_benchmark) / Var(R_benchmark)</i>",
        "where:",
        "* R_asset and R_benchmark are logarithmic returns over the same period,",
        "* both series are time-aligned,",
        "* covariance and variance are computed on the long-term dynamic window (e.g. window_vol_L).",
        "This ensures beta values consistent with actual data depth and comparable to those retrieved from Yahoo.",
        "<i>Beta interpretation</i>",
        make_beta_table_en(),
        "Beta is a universally understood, cross-asset indicator. It not only helps weight systemic risk and refine Risk-Adjusted Return interpretation, but also highlights structural portfolio biases (defensive, aggressive, neutral).",
        "<b>WARNING</b> — Beta depends heavily on both calculation period and chosen benchmark: the same asset may display different betas against different indices. In equity markets, it does not capture idiosyncratic risk (firm-specific factors). During crises, correlations rise mechanically and betas tend to converge toward 1, reducing discriminative power.",
    ]),
    ("6. Short-Term Scenarios<a name='section_scenarios_en'/>", [
        "<b>6.1 Objectives</b><a name='section_scenarios_goal_en'/>",
        "Short-Term (CT) Scenarios were introduced to provide a synthetic and narrative reading of the market state, beyond raw figures. They translate into analytical language the dynamic combination between return, momentum, and volatility, identifying typical market phases (e.g. “stressed rally,” “capitulation,” “technical rebound,” etc.).",
        "Each scenario is designed to make the diagnosis visual and intuitive while remaining objectively data-driven. The approach serves two main purposes:",
        "* to provide an economic and behavioral context for the current position of the asset or portfolio;",
        "* to help prioritize observations (high impact, moderate impact, light impact) according to risk level and movement robustness.",

        "<b>6.2 Operating Principle</b><a name='section_scenarios_mechanics_en'/>",
        "Scenarios are automatically determined from three key dimensions:",
        "1. Return (<i>R_label</i>): direction and intensity of average performance;",
        "2. Momentum (<i>M_label</i>): pace and consistency of the trend;",
        "3. Volatility Regime (<i>V_regime</i>): market risk state (subdued → turbulent).",
        "The engine cross-analyzes these three axes through a hierarchical set of rules. The first condition met defines the primary scenario, while the impact level (light, moderate, high) is then adjusted based on additional risk factors:",
        "* Liquidity (<i>Liquidity_Label</i>)",
        "* Leverage (<i>Leverage_Label</i>)",
        "* Market sensitivity (<i>Beta_Label</i>)",
        "The strength of the scenario framework lies in its ability to interpret figures (return, volatility, momentum) through concrete market behaviors, offering a unified analytical lens across very different asset types (equities, ETFs, commodities, rates, etc.), thereby helping to identify critical phases (stress, capitulation) or confirm bullish cycles (uptrend, volatility compression).",

        "<b>6.3 Classification Logic for Impact Level</b><a name='section_scenarios_classification_en'/>",
        "* Thin / illiquid liquidity → tends to downgrade one level (high → moderate)",
        "* Presence of leverage → tends to increase risk (light → moderate, moderate → high)",
        "* Very high Beta_Label → may raise risk (moderate → high); defensive → may lower it (high → moderate)",

        "<b>6.4 Possible Values Among Variables</b><a name='section_scenarios_variables_en'/>",
        "* <i>R_label</i> (Short-term return) ∈ {strongly negative, negative, neutral, moderately positive, strong, very strong}",
        "* <i>M_label</i> (Momentum) ∈ {bearish, neutral, bullish, accelerating, accelerating+}",
        "* <i>V_regime</i> (Volatility regime) ∈ {subdued, normal, elevated, turbulent} <i>(Labels depend on dynamic windows and detected data frequency.)</i>",
        PageBreak(),
        "<b>7. Scenario Catalogue</b><a name='section_catalogue_en'/>",
        "1. <b><i>Capitulation — [high]</i></b><a name='section_capitulation_en'/>",
        "<u>Trigger</u>: R_label = strongly negative and V_regime = turbulent and M_label contains bearish.",
        "<u>Definition</u>: Panic selling with extreme volatility; order books thin out rapidly as liquidity evaporates.",
        "<u>Watch for:</u>",
        "* Volatility Ratio sharply rising; ∆Return deeply negative",
        "* Signal_Stability often showing reversal (LT/CT divergence)",
        "* Actual liquidity (ADV10USD) to avoid execution traps",

        "2. <b><i>Stress — [high]</i></b><a name='section_stress_en'/>",
        "<u>Trigger</u>: R_label ∈ {strongly negative, negative} and V_regime ∈ {elevated, turbulent}.",
        "<u>Definition</u>: Significant damage but not full panic; potential for continuation.",
        "<u>Watch for:</u>",
        "* Momentum Ratio < 1 (weakening)",
        "* Volatility Ratio > 1.2 (expansion)",
        "* Reactions on key supports / newsflow sensitivity",

        "3. <b><i>Momentum squeeze — [high]</i></b><a name='section_squeeze_en'/>",
        "<u>Trigger</u>: R_label = very strong and M_label ∈ {accelerating, accelerating+} and V_regime ∈ {elevated, turbulent}.",
        "<u>Definition</u>: Explosive momentum-driven rally under high volatility; prone to whipsaws and short-covering.",
        "<u>Watch for:</u>",
        "* Elevated Volatility Ratio; possible short squeezes",
        "* Signal_Stability consistent but fragile to reversals",
        "* Ensure sufficient liquidity for entries/exits",

        "4. <b><i>Rally under tension — [high]</i></b><a name='section_rally_en'/>",
        "<u>Trigger</u>: R_label ∈ {strong, very strong} and V_regime ∈ {elevated, turbulent}.",
        "<u>Definition</u>: Strong rally with underlying nervousness; volatility threatens trend durability.",
        "<u>Watch for:</u>",
        "* Momentum Ratio ≥ 1 (otherwise “fatigued rally”)",
        "* Sharp pullbacks possible → apply strict risk control",

        "5. <b><i>Regular uptrend — [moderate]</i></b><a name='section_uptrend_en'/>",
        "<u>Trigger</u>: R_label ∈ {strong, very strong} and M_label ∈ {bullish, accelerating, accelerating+} and V_regime ∈ {subdued, normal}.",
        "<u>Definition</u>: Healthy bullish trend: gains supported by positive momentum and contained volatility.",
        "<u>Watch for:</u>",
        "* Signal_Stability ideally strong and coherent",
        "* Volatility Ratio ≈ 1 (no overheating)",
        PageBreak(),

        "6. <b><i>Loss of momentum — [moderate]</i></b><a name='section_loss_momentum_en'/>",
        "<u>Trigger</u>: M_label contains bearish and R_label ∉ {negative, strongly negative} and V_regime ∈ {normal, elevated}.",
        "<u>Definition</u>: Gradual loss of traction; potential consolidation or sector rotation phase.",
        "<u>Watch for:</u>",
        "* Momentum Ratio < 1; declining ∆Return",
        "* Possible price/momentum divergences",

        "7. <b><i>Technical rebound — [moderate]</i></b><a name='section_rebound_en'/>",
        "<u>Trigger</u>: M_label ∈ {bullish, accelerating, accelerating+} and R_label ∈ {negative, neutral}.",
        "<u>Definition</u>: Technical rebound without confirmed returns; test phase following a drop.",
        "<u>Watch for:</u>",
        "* Signal_Stability (is CT/LT coherence improving?)",
        "* R_label needs to turn positive for full confirmation",

        "8. <b><i>Gradual decline — [moderate]</i></b><a name='section_gradual_decline_en'/>",
        "<u>Trigger</u>: R_label = negative and V_regime ∈ {subdued, normal} and M_label contains bearish.",
        "<u>Definition</u>: Controlled decline without panic; sustained downward pressure.",
        "<u>Watch for:</u>",
        "* Volatility Ratio ≤ 1.0 (orderly selloff)",
        "* Progressive break of support levels",

        "9. <b><i>Volatility compression — [light]</i></b><a name='section_vol_compress_en'/>",
        "<u>Trigger</u>: V_regime = subdued and M_label ∈ {neutral, bullish} and R_label ∈ {neutral, moderately positive}.",
        "<u>Definition</u>: Volatility compression; potential breakout setup.",
        "<u>Watch for:</u>",
        "* Range break; improving Signal_Stability",
        "* Post-break jump in Volatility Ratio (volatility may surge right after a key breakout)",

        "10. <b><i>Volatility expansion — [moderate]</i></b><a name='section_vol_expand_en'/>",
        "<u>Trigger</u>: V_regime ∈ {elevated, turbulent} and |AvgReturn(%)| < 0.2 and M_label = neutral.",
        "<u>Definition</u>: Expanding volatility without directional bias (choppy market); frequent false signals.",
        "<u>Watch for:</u>",
        "* Wait for directional bias via R_label / M_label",
        "* Avoid overtrading",
        PageBreak(),

        "11. <b><i>Stabilization after shock — [moderate]</i></b><a name='section_stabilizing_en'/>",
        "<u>Trigger</u>: V_regime = elevated and R_label = neutral and M_label ∈ {neutral, bullish}.",
        "<u>Definition</u>: Decrease in nervousness after a shock; breathing phase.",
        "<u>Watch for:</u>",
        "* Volatility Ratio reverting toward 1",
        "* Confirmation via ∆Return turning positive again",

        "12. <b><i>Distribution — [moderate]</i></b><a name='section_distribution_en'/>",
        "<u>Trigger</u>: R_label ∈ {strong, moderately positive} and M_label contains bearish and V_regime ∈ {normal, elevated}.",
        "<u>Definition</u>: Profit-taking / trend fatigue; risk of rotation.",
        "<u>Watch for:</u>",
        "* Momentum Ratio < 1; emerging divergences",
        "* R_label shifting from positive to neutral, then negative",

        "13. <b><i>Range / noise — [light]</i></b><a name='section_range_en'/>",
        "<u>Trigger</u>: (no previous rule applies).",
        "<u>Definition</u>: Sideways / noisy market; alternating micro-movements without a clear trend.",
        "<u>Watch for:</u>",
        "* Volatility Ratio ≈ 1; Signal_Stability often neutral",
        "* Suitable strategies: mean reversion, stock-picking",
        "",
        "",
        "The thirteen CT scenarios defined in the engine form a complete and balanced mapping of market regimes. They cover all relevant configurations derived from the combination of Return, Momentum, and Volatility Regime from panic phases (capitulation, stress) to recovery or neutral phases (uptrend, range).",
        "This number was deliberately chosen to balance analytical precision and readability: each scenario remains distinct and interpretable, without redundancy or excessive complexity. Beyond this threshold, additional cases would only add false granularity at the expense of clarity and overall diagnostic coherence.",
    ]),
    ("8. Visualizations & Limitations<a name='section_visualizations'/>", [
        "<b>8.1 Number of tickers</b><a name='section_tickers_en'/>",
        "The report dynamically adapts to the number of selected assets: all visualizations, analyses, and interpretations are automatically generated without any predefined technical limit. However, for readability and graphical coherence, it is recommended to limit the number of tickers to 10–20 for a focused sectoral analysis, and to 40–50 for a full portfolio review. Beyond these thresholds, visual clarity and interpretability may degrade, although report generation remains fully functional.",

        "<b>8.2 Recommended observation window sizes</b><a name='section_window_recommendations'/>",
        "Dynamic windows automatically adjust to the chosen frequency (daily, weekly, monthly, yearly). However, to ensure statistical stability of key indicators (Return, Momentum, Volatility), certain bounds are recommended:",
        "<i>Recommended bounds by analysis frequency</i>",
        make_dynamic_windows_table_en(),

        "<b>8.3 Temporal resolution and data quality</b><a name='section_resolution_en'/>",
        "All prices used in the report come from Yahoo Finance, a reliable and widely recognized source for large-cap equities and liquid ETFs. For these assets, price adjustments (dividends, splits, closing variations) are considered accurate and fully suitable for quantitative analysis.",
        "However, for small-cap stocks (below USD 2 billion) or for recent and thinly traded assets, occasional irregularities may appear (missing values, delayed adjustments, or offset timestamps). These anomalies do not affect the structure of the report but can slightly distort rolling indicators such as volatility, short-term momentum, or ∆Return.",
        "<i>Recommendation: perform a quick visual check of price series for any asset with a market capitalization below USD 2 billion before including it in the report.</i>",

        "<b>8.4 Frequency bias and aggregation</b><a name='section_frequency_bias'/>",
        "Indicators are recalculated separately for each frequency (Daily, Weekly, Monthly, Yearly). → A frequency change mechanically alters returns, volatility, and correlations because observation windows and time granularity are no longer comparable.",
        "<i>Recommendation: avoid directly comparing reports of different frequencies without prior annualization of indicators, in order to normalize all measures to a common time base.</i>",
        "<i>Annualization formulas by frequency</i>",
        make_annualisation_table_en(),
        PageBreak(),

        "<b>8.5 Sensitivity to outliers</b><a name='section_extremes_en'/>",
        "Some indicators (such as Momentum or ∆Return) can be heavily influenced by short-term spikes or exceptional variations. → This may distort scenario perception if an unusual event (earnings release, major news, or crisis) occurs within the analysis window.",
        "<i>Recommendation: interpret recent results with caution and always cross-check with other time horizons.</i>",
    ]),


    ("9. Notes and Clarifications<a name='section_disclaimers'/>", [
        "<b>9.1 Scaling factors by asset class (*)</b><a name='section_scaling_factors'/>",
        "This table provides the scaling coefficients applied to dimensioned indicators (Return, Volatility, Momentum, ∆Return) depending on the asset class. Its goal is to ensure a consistent and comparable interpretation across heterogeneous assets: a ±1 % move does not carry the same economic weight for a currency pair as for a commodity or an equity index. These multiplicative factors normalize each measure to the “equity baseline” (factor = 1.0), which serves as the interpretive reference throughout the report.",
        "Indicators affected:",
        "* Return (%)",
        "* Volatility (%)",
        "* Momentum (%)",
        "* ∆Return (pp)",
        "",
        make_asset_classes_table_en(),
        "<b>WARNING</b> — The scaling table below should not be applied to leveraged products (e.g. ETF x2, x3, etc.) or to derivatives whose structural leverage amplifies both return and volatility. In such cases, the leverage factor takes precedence over the asset class scaling. For example, a 3x leveraged Nasdaq ETF should retain the “Equity = 1.0” scaling baseline but have its Return and Volatility values multiplied by 3 to reflect the true exposure.",
        "",
        "<b>9.2 Glossary of technical terms</b><a name='section_glossary'/>",
        "This glossary compiles the main technical terms and expressions used throughout the report. It aims to clarify the financial and behavioral concepts underlying market dynamics, making the indicators easier to read and interpret.",
        glossary_table_en
    ]),
]

if __name__ == "__main__":
    fr_pdf = os.path.join(REPORT_DIR, "annexe_fr.pdf")
    en_pdf = os.path.join(REPORT_DIR, "annexe_en.pdf")
    build_annex(fr_pdf, "fr", BLOCKS_FR)
    build_annex(en_pdf, "en", BLOCKS_EN)
    print("✅ Generated:", fr_pdf)
    print("✅ Generated:", en_pdf)