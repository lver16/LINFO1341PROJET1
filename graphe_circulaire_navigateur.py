import matplotlib.pyplot as plt

# Données pour chaque navigateur
safari_data = {
    'HTTPS': 112,
    'AAAA': 88,
    'A': 80
}

firefox_data = {
    'AAAA': 62,
    'A': 52
}

chrome_data = {
    'SVCB': 4,
    'PTR': 12,
    'HTTPS': 90,
    'AAAA': 126,
    'A': 114
}

# Fonction pour créer un graphique en camembert
def create_pie_chart(data, title):
    labels = data.keys()
    sizes = data.values()

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 30, 'color': 'black'})  # Augmenter la taille de la police et changer la couleur
    plt.title(title, fontsize=16, fontweight='bold')  # Ajustement de la taille et du style du titre
    plt.axis('equal')

# Ajustement de la taille et du style des étiquettes de catégorie
    plt.tight_layout(pad=2)
    plt.rcParams['font.size'] = 12
    plt.rcParams['font.weight'] = 'bold'
    plt.show()

# Création des graphiques pour chaque navigateur
create_pie_chart(safari_data, 'Safari')
create_pie_chart(firefox_data, 'Firefox')
create_pie_chart(chrome_data, 'Chrome')
