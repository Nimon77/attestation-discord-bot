# Bot discord generateur d'attestaion
Ce bot discord utilise le [générateur d'attestation de sortie](https://github.com/nirae/generateur_attestation_sortie) de [@nirae](https://github.com/nirae) qui utilise le site officiel du gouvernement `media.interieur.gouv.fr/deplacement-covid-19/` pour générer des attestations

## Utilisation
### Usage

```shell
./bot.py
or
python3 ./bot.py
```

### Installation

Faire bien attention aux locales et timezone pour générer date et heure de sortie /!\

Chrome/Chromium ainsi que le `chromedriver` ou `chromium-driver` doit etre installé.
`$ apt-get install chromium chromium-driver chromium-l10n`

Installer les dépendances python
`$ pip3 install -r requirements.txt`

Creer le fichier `config.py` avec les informations de configuration.

Cloner le generateur d'attestation de [@nirae](https://github.com/nirae) dans le dossier du bot ou a un autre endroit.
`$ git clone https://github.com/nirae/generateur_attestation_sortie.git`

Lancer le bot
`./bot.py`

## Configuration

Afin que le bot puisse ce connecter a discord il faut lui donner un **TOKEN** de connection que l'on récupère sur le [portail developpeur discord](https://discord.com/developers/applications)
Pour récupérer le **TOKEN** il faut créer une application puis un bot, [tutoriel ici](https://discordpy.readthedocs.io/en/latest/discord.html)

Créer un fichier config.py et y mettre :
```python
GEN_PATH = '<chemins vers le generateur>'
TOKEN = '<token du bot>'
```
