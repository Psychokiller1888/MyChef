#!/usr/bin/python
# -*- coding: utf-8 -*-

## Made by Psycho - 2018 ##

import codecs
import json
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as mqttPublish
import pixels
from threading import Timer
import time

OUVRIR_RECETTE 				= 'hermes/intent/Psychokiller1888:ouvrirRecette'
ETAPE_SUIVANTE 				= 'hermes/intent/Psychokiller1888:etapeSuivante'
INGREDIENTS 				= 'hermes/intent/Psychokiller1888:ingredients'
ETAPE_PRECEDENTE 			= 'hermes/intent/Psychokiller1888:etapePrecedente'
REPETER_ETAPE 				= 'hermes/intent/Psychokiller1888:repeterEtape'
ACTIVER_MINUTEUR 			= 'hermes/intent/Psychokiller1888:activerMinuteur'

HERMES_ON_HOTWORD 			= 'hermes/hotword/default/detected'
HERMES_START_LISTENING 		= 'hermes/asr/startListening'
HERMES_SAY 					= 'hermes/tts/say'
HERMES_CAPTURED 			= 'hermes/asr/textCaptured'
HERMES_HOTWORD_TOGGLE_ON 	= 'hermes/hotword/toggleOn'

def onConnect(client, userData, flags, rc):
	mqttClient.subscribe(OUVRIR_RECETTE)
	mqttClient.subscribe(ETAPE_SUIVANTE)
	mqttClient.subscribe(INGREDIENTS)
	mqttClient.subscribe(ETAPE_PRECEDENTE)
	mqttClient.subscribe(REPETER_ETAPE)
	mqttClient.subscribe(ACTIVER_MINUTEUR)

	mqttClient.subscribe(HERMES_ON_HOTWORD)
	mqttClient.subscribe(HERMES_START_LISTENING)
	mqttClient.subscribe(HERMES_SAY)
	mqttClient.subscribe(HERMES_CAPTURED)
	mqttClient.subscribe(HERMES_HOTWORD_TOGGLE_ON)
	mqttPublish.single('hermes/feedback/sound/toggleOn', payload=json.dumps({'siteId': 'default'}), hostname='127.0.0.1', port=1883)

def onMessage(client, userData, message):
	intent = message.topic

	if intent == HERMES_ON_HOTWORD:
		leds.wakeup()
		return

	elif intent == HERMES_SAY:
		leds.speak()
		return

	elif intent == HERMES_CAPTURED:
		leds.think()
		return

	elif intent == HERMES_START_LISTENING:
		leds.listen()
		return

	elif intent == HERMES_HOTWORD_TOGGLE_ON:
		leds.off()
		return

	global recipe, currentStep, timers, confirm

	payload = json.loads(message.payload)
	sessionId = payload['sessionId']

	if intent == OUVRIR_RECETTE:
		if 'slots' not in payload:
			error(sessionId)
			return

		slotRecipeName = payload['slots'][0]['value']['value'].encode('utf-8')

		if recipe is not None and currentStep > 0:
			if confirm <= 0:
				confirm = 1
				endTalk(sessionId, text="Nous avons déjà commencé une recette! Si j'en ouvre une autre, on ne pourra plus continuer sur celle-ci et tous les minuteurs seront annulés! Confirme ton intention en me demandant à nouveau d'ouvrir la recette!")
				return
			else:
				for timer in timers:
					timer.cancel()

				timers = {}
				confirm = 0
				currentStep = 0

		if os.path.isfile('./recettes/{}.json'.format(slotRecipeName.lower())):
			endTalk(sessionId, text="Ok, j'ouvre la recette {}, un instant".format(payload['slots'][0]['rawValue']))
			currentStep = 0

			file = codecs.open('./recettes/{}.json'.format(slotRecipeName.lower()), 'r', encoding='utf-8')
			string = file.read()
			file.close()
			recipe = json.loads(string)

			time.sleep(2)

			recipeName = recipe['name'] if 'phonetic' not in recipe else recipe['phonetic']
			timeType = 'cuisson' if 'cookingTime' in recipe else 'repos'
			cookOrWaitTime = recipe['cookingTime'] if timeType == 'cuisson' else recipe['waitTime']

			say(text=u"La recette {} est une préparation {}, pour {} personnes, qui nécessite environ {} dont {} de préparation et {} de {}".format(
				recipeName,
				recipe['difficulty'],
				recipe['person'],
				recipe['totalTime'],
				recipe['preparationTime'],
				cookOrWaitTime,
				timeType
			))
		else:
			endTalk(sessionId, text=u"Je suis désolé mais je ne trouve pas cette recette")

	elif intent == ETAPE_SUIVANTE:
		if recipe is None:
			endTalk(sessionId, text=u"Pardon, mais tu ne m'as pas demandé d'ouvrir une recette!")
		else:
			if str(currentStep + 1) not in recipe['steps']:
				endTalk(sessionId, text="Nous sommes arrivé à la fin de la recette, il n'y a pas d'étape supplémentaire, si ce n'est déguster la préparation! Bon appetit!")
			else:
				currentStep += 1
				step = recipe['steps'][str(currentStep)]

				ask = False
				if type(step) is dict and currentStep not in timers:
					ask = True
					step = step['text']

				endTalk(sessionId, text=u"Voici la prochaine étape: {}".format(step))
				if ask:
					say(text="Cette étape comporte un minuteur. Tu peux me demander de minuter dès que tu seras prêt")

	elif intent == INGREDIENTS:
		if recipe is None:
			endTalk(sessionId, text=u"Pardon, mais tu ne m'as pas demandé d'ouvrir une recette!")
		else:
			ingredients = ''
			for ingredient in recipe['ingredients']:
				ingredients += u"{}. ".format(ingredient)

			endTalk(sessionId, text=u"Pour préparer la recette {} il faudra les ingrédients suivant: {}".format(recipe['name'], ingredients))

	elif intent == ETAPE_PRECEDENTE:
		if recipe is None:
			endTalk(sessionId, text=u"Pardon, mais tu ne m'as pas demandé d'ouvrir une recette!")
		else:
			if currentStep <= 1:
				endTalk(sessionId, text="Il n'y a pas d'étape précédante")
			else:
				currentStep -= 1
				step = recipe['steps'][str(currentStep)]

				ask = False
				timer = 0
				if type(step) is dict and currentStep not in timers:
					ask = True
					timer = step['timer']
					step = step['text']

				endTalk(sessionId, text=u"L'étape précédente était: {}".format(step))
				if ask:
					say(text=u"Cette étape comportait un minuteur de {} secondes. Tu peux me demander de minuter si tu es prêt".format(timer))

	elif intent == REPETER_ETAPE:
		if recipe is None:
			endTalk(sessionId, text=u"Pardon, mais tu ne m'as pas demandé d'ouvrir une recette!")
		else:
			if currentStep <= 1:
				endTalk(sessionId, text="Je n'ai rien a répéter, on a même pas commencé!")
			else:
				step = recipe['steps'][str(currentStep)]
				endTalk(sessionId, text=u"L'étape était: {}".format(step))

	elif intent == ACTIVER_MINUTEUR:
		if recipe is None:
			endTalk(sessionId, text=u"Minuteur? On a pas encore de recette!")
		else:
			step = recipe['steps'][str(currentStep)]

			if type(step) is not dict:
				endTalk(sessionId, text=u"Il n'y a pas de minuteur pour cette étape")
			elif currentStep in timers:
				endTalk(sessionId, text=u"Un minuteur est déjà démarré pour cette étape")
			else:
				timer = Timer(int(step['timer']), onTimeUp, args=[currentStep, step])
				timer.start()
				timers[currentStep] = timer
				endTalk(sessionId, text=u"Ok! Minuteur pour cette étape démarré!")


def error(sessionId):
	endTalk(sessionId, "Désolé, mais il y a eu une erreur")

def endTalk(sessionId, text):
	mqttClient.publish('hermes/dialogueManager/endSession', json.dumps({
		'sessionId': sessionId,
		'text': text
	}))

def say(text):
	mqttClient.publish('hermes/dialogueManager/startSession', json.dumps({
		'init': {
			'type': 'notification',
			'text': text
		}
	}))

def onTimeUp(*args, **kwargs):
	global timers
	wasStep = args[0]
	step = args[1]
	del timers[wasStep]
	say(text=u'Un minuteur est arrivé à terme: {}'.format(step['textAfterTimer']))


mqttClient = None
leds = None
running = True
recipe = None
currentStep = 0
timers = {}
confirm = 0

if __name__ == '__main__':
	print('Chargement...')
	leds = pixels.Pixels()
	leds.off()
	mqttClient = mqtt.Client()
	mqttClient.on_connect = onConnect
	mqttClient.on_message = onMessage
	mqttClient.connect('localhost', 1883)
	print('Assistant de cuisine fonctionnel, chef!')
	mqttClient.loop_start()
	try:
		while running:
			time.sleep(0.1)
	except KeyboardInterrupt:
		mqttClient.loop_stop()
		mqttClient.disconnect()
		running = False
	finally:
		print('Arret')
