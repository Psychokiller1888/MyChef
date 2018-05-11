# MyChef

## Snips - Assistant de cuisine (for english, check below)

Ce project est ma petite contribution en remerciement pour le starter Kit que j'ai reçu de Snips.

Une fois installé cet assistant vous permettra d'avoir votre propre livre de recette intéractif à la cuisine!

Une série de vidéo est dédié à ce project: [Youtube playlist](https://www.youtube.com/watch?v=fCKCjN41n70&t=3s&list=PLO6q51Ysp78kkZyly_RQ5Bu_91IXSXprc&index=1)

La vidéo concernant la programmation est ici: [Youtube partie 4](https://www.youtube.com/watch?v=V6pvFjn0Vt0)

Comme tout project qui se respecte, une TODO list est prévue:

- Ajout des ingrédients à une liste accessible
- Support pour les équipements de cuisine intelligent (ex. pré chauffer le four)

Pour les personnes qui auraient déjà un assistant configuré, j'ai publié le bundle, sur la console Snips, en Français pour que vous puissiez l'ajouter à votre assistant existant.


## Snips - Kitchen assistant

This project is my little payback to thank Snips for the Starter kit they sent me as a preview.

Once installed, this assistant will offer you the power of an interactive recipe book directly in your kitchen!

A serie of (french, EN subtitles to come) video dedicated to the project can be found here: [Youtube playlist](https://www.youtube.com/watch?v=fCKCjN41n70&t=3s&list=PLO6q51Ysp78kkZyly_RQ5Bu_91IXSXprc&index=1)

The video treating about this program is to be found here: [Youtube part 4](https://www.youtube.com/watch?v=V6pvFjn0Vt0)

As every respectable project, a TODO:

- Adding ingredients directly to an accessible list
- Support intelligent kitchen devices (ex. pre heating oven)


### Installation

Dependencies
```
sudo pip install spidev
sudo pip install paho-mqtt
```

Installation
```
git clone https://github.com/Psychokiller1888/MyChef.git
sudo rm -rf /usr/share/snips/assistant
sudo mv MyChef/mychef.service /etc/systemd/system

FRENCH
 * sudo mv MyChef/assistants/assistant_fr /usr/share/snips/assistant
ENGLISH
 * sudo mv MyChef/assistants/assistant_en /usr/share/snips/assistant
 * cd MyChef
 * sudo nano settings.py => change 'LANG' = 'en'

sudo systemctl restart "snips-*"
sudo systemctl start mychef
sudo systemctl enable mychef
```
