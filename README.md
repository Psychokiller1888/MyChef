# MyChef

## Snips - Assistant de cuisine (for english, check below)

Ce project est ma petite contribution en remerciement pour le starter Kit que j'ai reçu de Snips.

Une fois installé cet assistant vous permettra d'avoir votre propre livre de recette intéractif à la cuisine!

Une série de vidéo est dédié à ce project: (url playlist)

La vidéo concernant la programmation est ici: [Youtube partie 4](https://www.youtube.com/watch?v=V6pvFjn0Vt0)

Comme tout project qui se respecte, une TODO list est prévue:

- Support mulilangue
- Ajout des ingrédients à une liste accessible
- Support pour les équipements de cuisine intelligent (ex. pré chauffer le four)


## Snips - Kitchen assistant

This project is my little payback to thank Snips for the Starter kit they sent me as a preview.

Once installed, this assistant will offer you the power of an interactive recipe book directly in your kitchen!

A serie of (french, EN subtitles to come) video dedicated to the project can be found here: (url playlist)

The video treating about this program is to be found here: [Youtube part 4](https://www.youtube.com/watch?v=V6pvFjn0Vt0)

As every respectable project, a TODO:

- Multilang support
- Adding ingredients directly to an accessible list
- Support intelligent kitch devices (ex. pre heating oven)


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
sudo mv mychef/assistant /usr/share/snips/assistant
sudo mv mychef/mychef.service /etc/systemd/system
sudo systemctl start mychef
sudo systemctl enable mychef
```
