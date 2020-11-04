# Work with Python 3.7
import os
import discord
from discord.ext import commands
import asyncio
import subprocess
import json
import yaml
import ruamel.yaml
from pprint import pprint
from datetime import datetime
from CREDENTIAL import token

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
async def gen(ctx, *args):
	if not (os.path.isfile(f'{ctx.author.id}.yaml')):
		await ctx.send('Erreur : aucune configuration trouver, utiliser ?conf <prenom> <nom> <anniversaire jj/MM/AAAA> <lieu de naissance> <adresse> <code postal> <ville>\n`mettre des "" autour de l\'adresse : "74 avenue du general leclerc" 75012 Paris`')
	else:
		now = datetime.now()
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
		size = len(args)
		if args[0] not in available_reasons:
			await ctx.send('Erreur : raison non valable\n```Raisons disponible :\nachats\nsante\nfamille\ntravail\nhandicap\nsports_animaux\nconvocation\nmissions\nenfants```')
			return
		if (size > 1):
			try:
				date = datetime.strptime(args[1], '%d/%m/%Y')
			except ValueError:
				ctx.send("Erreur : date non valide. Format JJ/MM/AAAA")
				return
			try:
				time = datetime.strptime(args[2], '%H:%M')
			except ValueError:
				ctx.send("Erreur : heure non valide. Format HH:MM")
				return
			date = date.strftime("%d/%m/%Y")
			time = time.strftime("%H:%M")
		else:
			date = now.strftime("%d/%m/%Y")
			time = now.strftime("%H:%M")

		config = open(f'{ctx.author.id}.yaml')
		data = yaml.load(config, Loader=yaml.FullLoader)
		data[f'{ctx.author.id}']['reason'] = args[0]
		data[f'{ctx.author.id}']['date'] = date
		data[f'{ctx.author.id}']['time'] = time
		with open(f'{ctx.author.id}.yaml', 'w') as fp:
			yaml.dump(data, fp)
		print(3)
		subprocess.call(['./app.py', '-c', f'{ctx.author.id}.yaml'])
		log = open("bot.log", "a")
		log.write(f'?gen demander par {ctx.author}\n')
		log.close()
		await ctx.send(f"Attestation pour le {date} a {time}", file=discord.File(f'./{ctx.author.id}_attestation.pdf'))
		os.remove(f'{ctx.author.id}_attestation.pdf')
@gen.error
async def gen_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Erreur : `?gen <raison>` ou `?gen <raison> <date>` ou `?gen <raison> <heure>` ou `?gen <raison> <date> <heure>`\n```Raisons disponible :\nachats\nsante\nfamille\ntravail\nhandicap\nsports_animaux\nconvocation\nmissions\nenfants```')

@client.command()
async def conf(ctx, fname, lname, birthday, POBirth, address, zip, city):
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
@conf.error
async def conf_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Erreur : ?conf <prenom> <nom> <anniversaire dd/mm/yyyy> <lieu de naissance> <adresse> <code postal> <ville>\n`mettre des "" autour de l\'adresse : "74 avenue du general leclerc" 75012 Paris`')

@client.command()
@commands.is_owner()
async def stop(ctx):
    await client.logout()
@stop.error
async def stop_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        log = open("bot.log", "a")
        log.write(f'\n*stop demander par {ctx.author}\n\n')
        log.close()
        await ctx.send('Cette commande est réserver au propriétaire du bot')

try:
    client.run(TOKEN)
finally:
    exit()
