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

client = commands.Bot(command_prefix='?',owner_id=194422040227348480)

def check_auth(ctx):
    return ctx.message.author.id == 194422040227348480 or ctx.message.author.id == 219193195978817536

@client.event
async def on_ready():
    global nimon, andy
    log = open("bot.log", "w")
    log.write('Logged in as\n')
    log.write(f'{client.user.name}\n')
    log.write(f'{client.user.id}\n')
    log.write('------\n')
    log.close()
    game = discord.Game("?help")
    await client.change_presence(status=discord.Status('online'),
                                    activity=game,
                                    afk=False)
    nimon = await client.fetch_user(194422040227348480)
    andy = await client.fetch_user(219193195978817536)

@client.command()
async def gen(ctx, reason, *args):
	if not (os.path.isfile(f'{ctx.author.id}.yaml')):
		await ctx.send('Erreur : aucune configuration trouver, utiliser ?conf <prenom> <nom> <anniversaire jj/MM/AAAA> <lieu de naissance> <adresse> <code postal> <ville>\n`mettre des "" autour de l\'adresse : "74 avenue du general leclerc" 75012 Paris`')
	else:
		now = datetime.now()
		year = now.strftime("%Y")
		available_reasons = [
			'achats',
			'sante',
			'famille',
			'travail',
			'handicap',
			'sports_animaux',
			'convocation',
			'missions',
			'enfants'
		]
		if reason not in available_reasons:
			await ctx.send('Erreur : raison non valable\n```Raisons disponible :\nachats\nsante\nfamille\ntravail\nhandicap\nsports_animaux\nconvocation\nmissions\nenfants```')
			return
		size = len(args)
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
		config = open(f'{ctx.author.id}.yaml')
		data = yaml.load(config, Loader=yaml.FullLoader)
		data[f'{ctx.author.id}']['reason'] = reason
		data[f'{ctx.author.id}']['date'] = date
		data[f'{ctx.author.id}']['time'] = time
		with open(f'{ctx.author.id}.yaml', 'w') as fp:
			yaml.dump(data, fp)
		subprocess.call([f'{GEN_PASS}/app.py', '-c', f'{ctx.author.id}.yaml'])
		log = open("bot.log", "a")
		log.write(f'?gen demander par {ctx.author}\n')
		log.close()
		await ctx.author.send(f"Attestation pour le {date} a {time}", file=discord.File(f'{ctx.author.id}_attestation.pdf'))
		os.remove(f'{ctx.author.id}_attestation.pdf')
@gen.error
async def gen_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('- `?gen <raison>` générer pour maintenant\n- `?gen <raison> <heure>` générer pour aujourd\'hui à une autre heure\n- `?gen <raison> <date> <heure>` générer à une autre date et heure\n```Raisons disponible :\nachats\nsante\nfamille\ntravail\nhandicap\nsports_animaux\nconvocation\nmissions\nenfants```')

@client.command()
@commands.dm_only()
async def conf(ctx, fname, lname, birthday, POBirth, address, zip, city, *args):
	if (len(args) > 0):
		await ctx.send('Trop d\'arguments, avez-vous bien mis des "" autour de l\'adresse ?\nExemple : `?conf Jean dujardin 19/06/1972 "Marne la Vallée" "74 avenue du general leclerc" 94400 "Vitry sur Seine"`')
		return
	try:
		birthday = datetime.strptime(birthday, '%d/%m/%Y').strftime(f"%d/%m/%Y")
	except ValueError:
		await ctx.send("Anniversaire non valide. Format JJ/MM/AAAA")
		return
	if not zip.isnumeric():
		await ctx.send("Code postal non valide")
		return
	data = {
		f"{ctx.author.id}": {
			"first_name": fname,
			"last_name": lname,
			"birthday": birthday,
			"placeofbirth": POBirth,
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
	await ctx.send("Configuration sauvegarder")
@conf.error
async def conf_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('`?conf <prenom> <nom> <anniversaire jj/mm/aaaa> <lieu de naissance> <adresse> <code postal> <ville>`\nmettre des "" autour de l\'adresse et des villes si le nom est en plusieurs mots.\nExemple : `?conf Jean dujardin 19/06/1972 "Marne la Vallée" "74 avenue du general leclerc" 75012 "Vitry sur Seine"`')
	if isinstance(error, commands.PrivateMessageOnly):
		await ctx.send('Pour respecter votre vie priver merci d\'utiliser cette commande en message prive avec le bot')

try:
    client.run(TOKEN)
finally:
    exit()
