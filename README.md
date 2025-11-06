Analyseur de Stratégie de Roulette
(Pensez à remplacer cette URL par une capture d'écran de votre propre application)

Ce projet est un outil d'assistance à la décision pour la roulette, développé en Python avec une interface graphique moderne grâce à CustomTkinter.

L'application suit les numéros sortis et suggère des opportunités de mise basées sur la stratégie de l'écart (absence prolongée d'un événement). Elle suit les chances simples (Rouge/Noir, Pair/Impair, 1-18/19-36) ainsi que les douzaines et les colonnes.

⚠️ Avertissement Légal et sur les Jeux d'Argent
Ce logiciel est fourni à des fins éducatives et de divertissement uniquement.

Il n'existe aucune stratégie "infaillible" à la roulette. La roulette est un jeu de hasard pur avec un avantage mathématique fixe pour le casino (le "zéro").

Cet outil ne garantit aucun gain et ne peut pas prédire l'avenir. Les séries d'absences (écarts) n'ont aucune influence statistique sur le prochain tirage.

L'auteur de ce programme ne peut être tenu responsable d'éventuelles pertes financières résultant de l'utilisation de cet outil.

Ne jouez jamais d'argent que vous ne pouvez pas vous permettre de perdre. Si vous pensez avoir un problème de jeu, cherchez de l'aide auprès d'organismes spécialisés.

🚀 Fonctionnalités
Suivi en temps réel : Entrez les numéros au fur et à mesure qu'ils sortent.

Suggestions intelligentes : L'outil vous alerte lorsque les seuils d'absence sont atteints pour :

Chances simples (Rouge, Noir, Pair, Impair, Manque, Passe)

Douzaines (1ère, 2ème, 3ème)

Colonnes (1ère, 2ème, 3ème)

Stop Loss Intégré : Pour limiter les pertes sur une martingale, l'outil cesse de suggérer une mise après 2 échecs consécutifs sur cette même mise.

Suivi des Gains/Pertes : Calcule automatiquement votre solde (en unités de mise) si vous suivez toutes les suggestions non bloquées par le stop loss.

Indicateurs : Affiche le temps de jeu et le nombre de tours écoulés depuis le dernier zéro.

Interface Moderne : Construit avec CustomTkinter pour un look agréable et un mode sombre.

🛠️ Installation
Ce projet nécessite Python 3 et la bibliothèque customtkinter.

Clonez le dépôt :

Bash

git clone https://github.com/VOTRE_NOM/analyseur-roulette-python.git
cd analyseur-roulette-python
Installez les dépendances :

Bash

pip install customtkinter
🏃 Comment Lancer l'Application
Une fois les dépendances installées, exécutez simplement le script principal :

Bash

python votre_script.py
(Remplacez votre_script.py par le nom de votre fichier .py principal)

⚖️ Licence
Ce projet est publié sous la Licence MIT.

Cela signifie que vous êtes libre de l'utiliser, de le copier, de le modifier, de le fusionner, de le publier, de le distribuer, de le sous-licencier et/ou de le vendre, à condition d'inclure la notice de copyright et de permission (le fichier LICENSE) dans toutes les copies ou parties substantielles du logiciel.

Pour plus de détails, consultez le fichier LICENSE inclus dans ce dépôt.
