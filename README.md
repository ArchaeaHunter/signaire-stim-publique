<div align="center">

# Figures Signaire STIM

<br />

</div>

Ce dépôt contient le code utilisé pour permettre au public d'avoir une idée claire du contenu de la base de données du lexique scientifique en LSF de [STIM Sourd France](https://www.stimsourdfrance.org/). Le code utilise module [plotly](https://plotly.com/) pour produire des figures interactives permettant de retracer l'évolution du lexique scientifique en LSF au cours du temps et de leur répartition suivant les domaines. 


## Pour démarrer

### Modules

* plotly
* pandas

### Exécution

Pour exécuter le script automatisé pour sauvegarder les figure dans un dossier :

Cloner le dépôt
```
# Requiert Python 3.11+
git clone git@github.com:ArchaeaHunter/signaire-stim-publique.git
cd signaire-stim-publique
```

Lancer la commande avec [uv](https://docs.astral.sh/uv/)
```
uv run python3 src/script_figures.py --csv data/database_without_names.csv --dir figures
```

## Notebook

Il y a un notebook analyse_bdd.ipynb disponible dans le dépôt pour tout les efforts de développement, avec toutes les figures. 

## Contact

Pour toute amélioration ou informations, contacter STIM Sourd France par mail : stimsourdfr@gmail.com

## Licence

Le projet est licencié sous CC BY-NC-SA 4.0 License - voir le fichier LICENSE pour détails

