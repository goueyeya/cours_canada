import sqlite3



conn = sqlite3.connect('database.db')
c = conn.cursor()

# Insertion des articles
articles = [
    ('Comment devenir un expert en programmation', 'devenir-un-expert-en-programmation', 'Paul Dupont', '2023-03-15', 'Si vous voulez devenir un expert en programmation, il est important de suivre une formation complète et de pratiquer régulièrement. Commencez par apprendre les bases de la programmation, puis plongez-vous dans des projets pratiques pour mettre en pratique vos compétences. Trouvez une communauté de programmeurs avec laquelle vous pourrez échanger et obtenir des conseils. Enfin, tenez-vous informé des dernières tendances et technologies en programmation pour rester à la pointe du domaine..'),
    ('Les avantages de la méditation quotidienne', 'avantages-meditation-quotidienne', 'Sophie Martin', '2023-04-02', 'La méditation quotidienne peut apporter de nombreux avantages pour la santé mentale et physique. Elle peut aider à réduire le stress, améliorer la concentration et la créativité, et renforcer le système immunitaire. Pour commencer à méditer, trouvez un endroit calme et confortable où vous pourrez vous détendre. Concentrez-vous sur votre respiration et essayez de calmer votre esprit en observant vos pensées sans les juger.'),
    ('Les bienfaits du yoga sur la santé', 'bienfaits-yoga-sante', 'Marc Rousseau', '2023-05-01', "Le yoga est une pratique qui peut apporter de nombreux bienfaits pour la santé physique et mentale. Il peut aider à améliorer la souplesse, renforcer les muscles et réduire le stress et l'anxiété. Pour commencer à pratiquer le yoga, trouvez un cours ou un instructeur qualifié pour vous guider dans les poses et les techniques de respiration. Pratiquez régulièrement pour en tirer les bienfaits maximum."),
    ('Les meilleurs conseils pour un régime alimentaire équilibré', 'conseils-regime-alimentaire-equilibre', 'Alice Girard', '2023-06-12', "Pour maintenir un régime alimentaire équilibré, il est important de consommer une variété d'aliments sains dans les bonnes proportions. Les fruits et légumes frais, les protéines maigres et les grains entiers devraient constituer la majeure partie de votre alimentation, tandis que les aliments transformés et riches en matières grasses et en sucre devraient être consommés avec modération. Évitez les régimes à la mode qui promettent des résultats rapides et optez pour une alimentation saine et équilibrée à long terme."),
    ('Les secrets pour améliorer votre mémoire', 'secrets-ameliorer-memoire', 'David Leclerc', '2023-07-20', 'Si vous voulez améliorer votre mémoire, il est important de pratiquer des exercices mentaux régulièrement.')
]

for article in articles:
    conn.execute("INSERT INTO article (titre, identifiant, auteur, date_publication, paragraphe) VALUES (?, ?, ?, ?, ?)", article)

conn.commit()
conn.close()