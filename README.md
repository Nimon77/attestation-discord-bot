# Bot discord generateur d'attestaion
Ce bot discord utilise le [générateur d'attestation de sortie](https://github.com/nirae/generateur_attestation_sortie) de [@nirae](https://github.com/nirae) qui utilise le site officiel du gouvernement `media.interieur.gouv.fr/deplacement-covid-19/` pour générer des attestations

Si vous souhaitez utiliser le bot sans l’héberger vous-même vous pouvez me contacter sur discord : Nimon#0077

Ou utiliser ce lien d'invitation pour bot pour le mettre sur votre serveur : https://discord.com/oauth2/authorize?client_id=773161125230805002&scope=bot&permissions=257088

## Utilisation
### Usage

#### CLI
```shell
./bot.py
or
python3 ./bot.py
```

#### Sur Discord :

`?conf <prenom> <nom> <anniversaire jj/mm/aaaa> <lieu de naissance> <adresse> <code postal> <ville>` ⚠️ attention ⚠️ a bien mettre des `"` pour l'adresse et les villes si elles sont en plusieurs mots. Exemple : `?conf Jean dujardin 19/06/1972 "Marne la Vallée" "74 avenue du general leclerc" 75012 "Vitry sur Seine"`

`?gen <raison>` générer pour maintenant

`?gen <raison> <heure>` générer pour aujourd'hui à une autre heure

`?gen <raison> <date> <heure>` générer à une autre date et heure


### Installation

Faire bien attention aux locales et timezone pour générer date et heure de sortie ⚠️

Chrome/Chromium ainsi que le `chromedriver` ou `chromium-driver` ou `chromium-chromedriver` doit etre installé.

`$ apt-get install chromium chromium-driver chromium-l10n`

`$ apt-get install chromium-browser chromium-chromedriver chromium-browser-l10n`

Installer les dépendances python

`$ pip3 install -r requirements.txt`

Creer le fichier `config.py` avec les informations de configuration.

Cloner le generateur d'attestation de [@nirae](https://github.com/nirae) dans le dossier du bot ou a un autre endroit.

`$ git clone https://github.com/nirae/generateur_attestation_sortie.git`

Executer le bot

`$ ./bot.py`

## Configuration

Afin que le bot puisse ce connecter a discord il faut lui donner un **TOKEN** de connection que l'on récupère sur le [portail developpeur discord](https://discord.com/developers/applications)
Pour récupérer le **TOKEN** il faut créer une application puis un bot, [tutoriel ici](https://discordpy.readthedocs.io/en/latest/discord.html)

Créer un fichier config.py et y mettre :
```python
GEN_PATH = '<chemins vers le generateur>'
TOKEN = '<token du bot>'
```

## TODO

`?del` pour supprimer sa configuration
