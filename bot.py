#! /usr/bin/env python3

import os
import discord
from discord.ext import commands
import asyncio
import subprocess
import json
import yaml
import ruamel.yaml
import re
from conf import *
from datetime import datetime

available_reasons = [
    'sante',
    'famille',
    'travail',
    'handicap',
    'animaux',
    'convocation',
    'missions',
    'achats',
    'sport',
    'demarche',
    'demenagement',
    'culte-culturel',
    'enfants'
]


available_curfew_reasons = {
    'sante': 'checkbox-curfew-sante',
    'famille': 'checkbox-curfew-famille',
    'travail': 'checkbox-curfew-travail',
    'handicap': 'checkbox-curfew-famille',
    'animaux': 'checkbox-curfew-animaux',
    'convocation': 'checkbox-curfew-convocation_demarches',
    'missions': 'checkbox-curfew-travail'
}

available_quarantine_reasons = {
    'sante': 'checkbox-quarantine-sante',
    'famille': 'checkbox-quarantine-famille',
    'travail': 'checkbox-quarantine-travail',
    'handicap': 'checkbox-quarantine-famille',
    'convocation': 'checkbox-quarantine-convocation_demarches',
    'sport': 'checkbox-quarantine-sport',
    'achats': 'checkbox-quarantine-achats_culte_culturel',
    'enfants': 'checkbox-quarantine-famille',
    'culte-culturel': 'checkbox-quarantine-achats_culte_culturel',
    'demarche': 'checkbox-quarantine-convocation_demarches',
    'demenagement': 'checkbox-quarantine-demenagement',
    'animaux': 'checkbox-quarantine-sport',
    'missions': 'checkbox-quarantine-travail'
}


available_context = {
    'couvre-feu': 'curfew-button',
    'confinement': 'quarantine-button'
}

client = commands.Bot(command_prefix='?')

@client.event
async def on_ready():
	log = open("bot.log", "a")
	log.write('Logged in as\n')
	log.write(f'{client.user.name}\n')
	log.write(f'{client.user.id}\n')
	log.write('------\n')
	log.close()
	game = discord.Game("?help")
	await client.change_presence(status=discord.Status('online'),
									activity=game,
									afk=False)

@client.command()
async def gen(ctx, reason, *args):
	if not (os.path.isfile(f'{ctx.author.id}.yaml')):
		await ctx.send('Erreur : aucune configuration trouver, utiliser ?conf en message privé avec le bot')
		await ctx.author.send('utiliser `?conf` ici\n\n`?conf <prenom> <nom> <anniversaire jj/mm/aaaa> <adresse> <code postal> <ville>`\nmettre des "" autour de l\'adresse et des villes si le nom est en plusieurs mots.\nExemple : `?conf Jean dujardin 19/06/1972 "74 avenue du general leclerc" 75012 "Vitry sur Seine"`')
		return
	else:
		now = datetime.now()
		year = now.strftime("%Y")
		if reason not in available_reasons:
			await ctx.send('Erreur : raison non valable\n```Raisons disponible :\n' + '\n'.join(available_reasons) + '```')
			return
		size = len(args)

		msg = await ctx.send('1️⃣: couvre-feu\t2️⃣: confinement');
		await msg.add_reaction("1️⃣")
		await msg.add_reaction("2️⃣")
		def check(reaction):
			return reaction.user_id == ctx.author.id and reaction.message_id == msg.id and reaction.emoji.name in ['1️⃣', '2️⃣']
		try:
			reaction = await client.wait_for('raw_reaction_add', timeout=60.0, check=check)
		except asyncio.TimeoutError:
			return
		else:
			config = open(f'{ctx.author.id}.yaml')
			data = yaml.load(config, Loader=yaml.FullLoader)
			if reaction.emoji.name == '1️⃣':
				data[f'{ctx.author.id}']['context'] = "couvre-feu"
			else:
				data[f'{ctx.author.id}']['context'] = "confinement"
		if data[f'{ctx.author.id}']['context'] == 'couvre-feu':
			if not reason in available_curfew_reasons:
				await ctx.send("La raison '%s' n'est pas valable pendant le %s" % (reason, data[f'{ctx.author.id}']['context']))
				return
		elif data[f'{ctx.author.id}']['context'] == 'confinement':
			if not reason in available_quarantine_reasons:
				await ctx.send("La raison '%s' n'est pas valable pendant le %s" % (reason, data[f'{ctx.author.id}']['context']))
				return
		if (size == 1):
			try:
				time = datetime.strptime(args[0], '%H:%M').strftime("%H:%M")
			except ValueError:
				await ctx.send("Erreur : heure non valide. Format HH:MM")
				return
			date = now.strftime("%d/%m/%Y")
		elif (size > 1):
			try:
				date = datetime.strptime(args[0], '%d/%m').strftime(f"%d/%m/{year}")
			except ValueError:
				await ctx.send("Erreur : date non valide. Format JJ/MM")
				return
			try:
				time = datetime.strptime(args[1], '%H:%M').strftime("%H:%M")
			except ValueError:
				await ctx.send("Erreur : heure non valide. Format HH:MM")
				return
		else:
			date = now.strftime("%d/%m/%Y")
			time = now.strftime("%H:%M")
		data[f'{ctx.author.id}']['reason'] = reason
		data[f'{ctx.author.id}']['date'] = date
		data[f'{ctx.author.id}']['time'] = time
		with open(f'{ctx.author.id}.yaml', 'w') as fp:
			yaml.dump(data, fp)
		codeproc = subprocess.call(['python3', f'{GEN_PATH}/app.py', '-c', f'{ctx.author.id}.yaml'])
		log = open("bot.log", "a")
		log.write(f'?gen demander par {ctx.author}\n')
		log.close()
		await ctx.author.send(f"Attestation pour le {date} a {time}", file=discord.File(f'{ctx.author.id}_attestation.pdf'))
		os.remove(f'{ctx.author.id}_attestation.pdf')
@gen.error
async def gen_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('- `?gen <raison>` générer pour maintenant\n- `?gen <raison> <heure>` générer pour aujourd\'hui à une autre heure\n- `?gen <raison> <date> <heure>` générer à une autre date et heure\n```Raisons disponible :\n' + '\n'.join(available_reasons) + '```')

@client.command()
@commands.dm_only()
async def conf(ctx, fname, lname, birthday, address, zip, city, *args):
	
	try:
		birthday = datetime.strptime(birthday, '%d/%m/%Y').strftime('%d/%m/%Y')
	except ValueError:
		await ctx.send("Anniversaire non valide. Format JJ/MM/AAAA")
		return
	if (datetime.strptime(birthday, '%d/%m/%Y').strftime('%Y') < '1900'):
		await ctx.send("Merci de mettre votre VRAIE date de naissance")
		return
	if not zip.isnumeric():
		await ctx.send("Code postal non valide")
		return
	data = {
		f"{ctx.author.id}": {
			"first_name": fname,
			"last_name": lname,
			"birthday": birthday,
			"address": address,
			"zipcode": zip,
			"city": city,
			"reason": "",
			"date": "",
			"time": ""
		}
	}
	with open(f'{ctx.author.id}.yaml', "w") as file:
		yaml.dump(data, file)
	log = open("bot.log", "a")
	log.write(f'?conf executer par {ctx.author}\n')
	log.close()
	await ctx.send("Configuration sauvegarder")
@conf.error
async def conf_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('`?conf <prenom> <nom> <anniversaire jj/mm/aaaa> <adresse> <code postal> <ville>`\nmettre des "" autour de l\'adresse et des villes si le nom est en plusieurs mots.\nExemple : `?conf Jean dujardin 19/06/1972 "74 avenue du general leclerc" 75012 "Vitry sur Seine"`')
	if isinstance(error, commands.PrivateMessageOnly):
		await ctx.send('Pour respecter votre vie priver merci d\'utiliser cette commande en message prive avec le bot')
		await ctx.author.send('ici pour le ?conf :)')

@client.command()
async def delete(ctx):
	if os.path.exists(f'{ctx.author.id}.yaml'):
		try:
			os.remove(f'{ctx.author.id}.yaml')
		except:
			await ctx.send("Erreur lors de la suppression de la configuration contacter developpeur")
			return
		await ctx.send("Votre configuration a été supprimer")
	else:
		await ctx.send('Votre configuration n\'existe pas')

try:
	client.run(TOKEN)
finally:
	exit()
