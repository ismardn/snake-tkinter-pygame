# Jeu Snake - Tkinter & Pygame

Ce projet propose deux versions du jeu Snake, réalisées avec **Tkinter** et **Pygame**.  
L’objectif était de recréer exactement le même jeu avec ces deux bibliothèques pour m'entraîner à les utiliser en parallèle.

Le meilleur score est automatiquement sauvegardé et **chiffré** dans un fichier texte, ce qui empêche toute modification sans connaître la clé.

## Fonctionnalités
- Deux interfaces graphiques différentes : Tkinter et Pygame
- Gameplay identique dans les deux versions
- Sauvegarde automatique du meilleur score, stocké sous forme chiffrée dans un fichier
- Gestion de la collision, des murs, et de la croissance du serpent

## Fichiers
- `snake_game_with_tkinter.pyw` : version Tkinter
- `snake_game_with_pygame.pyw` : version Pygame
- `high_score_tkinter_game.txt` : score chiffré (Tkinter)
- `high_score_pygame_game.txt` : score chiffré (Pygame)
- `dev/auto_win_test.txt` : script de test pour simuler une victoire automatiquement et vérifier le bon fonctionnement du jeu

## Lancer le jeu

Assurez-vous d’avoir Python 3 d'installé ainsi que la bibliothèque `pygame` si vous utilisez la version Pygame.

```bash
# Pour Tkinter
python snake_game_with_tkinter.pyw

# Pour Pygame
python snake_game_with_pygame.pyw
```

---

*Projet réalisé en juin 2023, mis en ligne ici en juin 2025.*
