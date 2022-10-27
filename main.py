import discord
from colorama import Fore
import consts
import os
from bashrc import *
from hastebin import *

class BasteRC_v2(discord.Client):
    async def on_ready(self):
        try:
            print(f"{Fore.GREEN}Connecté à {self.user.name}#{self.user.discriminator} ({self.user.id}){Fore.RESET}")
        except:
            print(f"{Fore.RED}Impossible de se connecter")
            return

    async def on_message(self, message):
        author = message.author
        author_id = str(author.id)
        args = message.content.split(" ")
        command = args[0]
        args = args[1:]
        prefix = consts.PREFIX

        # Anti redondance
        if(author == self.user):
            return

        print(f"{Fore.GREEN}{author.name}#{author.discriminator} ({author_id}){Fore.RESET} : {message.content}")

        # Commandes
        ## Commande help
        if(command == f"{prefix}help"):
            embed = discord.Embed(title="BasteRC", description="Liste des commandes", color=0x00ff00)
            ## Toutes les commandes
            embed.add_field(name=f"{prefix}help", value="Affiche cette page", inline=False)
            embed.add_field(name=f"{prefix}init_bashrc", value="Initialisation votre bashrc", inline=False)
            embed.add_field(name=f"{prefix}del_bashrc", value="Supprime votre bashrc", inline=False)
            embed.add_field(name=f"{prefix}get_bashrc", value="Envoie votre bashrc custom", inline=False)
            embed.add_field(name=f"{prefix}change_name_color", value="Change la couleur du nom", inline=False)
            embed.add_field(name=f"{prefix}change_machine_color", value="Change la couleur de la machine", inline=False)
            embed.add_field(name=f"{prefix}change_dir_color", value="Change la couleur du dossier", inline=False)
            embed.add_field(name=f"{prefix}change_prompt_color", value="Change la couleur du prompt", inline=False)
            embed.add_field(name=f"{prefix}change_title", value="Change le titre de la fenêtre", inline=False)
            embed.add_field(name=f"{prefix}change_use_bashrc_val", value="Change l'utilisation de VT", inline=False)

            embed.set_footer(text="BasteRC v2.0.0")
            await message.channel.send(embed=embed)

        ## Commande init_bashrc
        elif(command == f"{prefix}init_bashrc"):
            if(have_bashrc(author_id)):
                await message.channel.send(f"{author.mention} Vous avez déjà un bashrc")
            else:
                init_bashrc(author_id)
                await message.channel.send(f"{author.mention} Votre bashrc a été initialisé")

        ## Commande del_bashrc
        elif(command == f"{prefix}del_bashrc"):
            if(have_bashrc(author_id)):
                del_bashrc(author_id)
                await message.channel.send(f"{author.mention} Votre bashrc a été supprimé")
            else:
                await message.channel.send(f"{author.mention} Vous n'avez pas de bashrc")

        ## Commande get_bashrc
        elif(command == f"{prefix}get_bashrc"):
            if(have_bashrc(author_id)):
                await author.send(f"""To install this bashrc, you need to do this :
                1. curl -L {get_url_to_code(genere_bashrc(author_id))} -o .bashrc
                2. Enjoy !""")
            else:
                await message.channel.send(f"{author.mention} Vous n'avez pas de bashrc")

        ## Commande colors
        elif(command == f"{prefix}colors"):
            embed = discord.Embed(title="BasteRC", description="Liste des couleurs", color=0x00ff00)
            for color in consts.COLOR.keys():
                embed.add_field(name=color, value="-", inline=True)
            embed.set_footer(text="Les couleurs sont en anglais")
            await message.channel.send(embed=embed)

        ## Commande change_name_color
        elif(command == f"{prefix}change_name_color"):
            if(len(args) == 1):
                if(verif_color(args[0])):
                    change_name_color(author_id, args[0])
                    await message.channel.send(f"{author.mention} La couleur de votre nom a été changé")
                else:
                    await message.channel.send(f"{author.mention} La couleur {args[0]} n'existe pas, pour voir la liste des couleurs, faites {prefix}colors")
            else:
                await message.channel.send(f"{author.mention} Il manque un argument")

        ## Commande change_machine_color
        elif(command == f"{prefix}change_machine_color"):
            if(len(args) == 1):
                if(verif_color(args[0])):
                    change_machine_color(author_id, args[0])
                    await message.channel.send(f"{author.mention} La couleur de votre machine a été changé")
                else:
                    await message.channel.send(f"{author.mention} La couleur {args[0]} n'existe pas, pour voir la liste des couleurs, faites {prefix}colors")
            else:
                await message.channel.send(f"{author.mention} Il manque un argument")

        ## Commande change_dir_color
        elif(command == f"{prefix}change_dir_color"):
            if(len(args) == 1):
                if(verif_color(args[0])):
                    change_dir_color(author_id, args[0])
                    await message.channel.send(f"{author.mention} La couleur de votre dossier a été changé")
                else:
                    await message.channel.send(f"{author.mention} La couleur {args[0]} n'existe pas, pour voir la liste des couleurs, faites {prefix}colors")
            else:
                await message.channel.send(f"{author.mention} Il manque un argument")

        ## Commande change_prompt_color
        elif(command == f"{prefix}change_prompt_color"):
            if(len(args) == 1):
                if(verif_color(args[0])):
                    change_prompt_color(author_id, args[0])
                    await message.channel.send(f"{author.mention} La couleur de votre prompt a été changé")
                else:
                    await message.channel.send(f"{author.mention} La couleur {args[0]} n'existe pas, pour voir la liste des couleurs, faites {prefix}colors")
            else:
                await message.channel.send(f"{author.mention} Il manque un argument")

        ## Commande change_title
        elif(command == f"{prefix}change_title"):
            if(len(args) == 1):
                change_title(author_id, args[0])
                await message.channel.send(f"{author.mention} Le titre de votre bashrc a été changé")
            else:
                await message.channel.send(f"{author.mention} Il manque un argument")

        ## Commande change_use_vt
        elif(command == f"{prefix}change_use_bashrc_val"):
            if(len(args) == 1):
                if(args[0] == "True" or args[0] == "False"):
                    change_use_vt(author_id, args[0])
                    await message.channel.send(f"{author.mention} La valeur de use_bashrc a été changé")
                else:
                    await message.channel.send(f"{author.mention} La valeur doit être True ou False")
            else:
                await message.channel.send(f"{author.mention} Il manque un argument")

        
if __name__ == "__main__":
    init_bd()
    os.system("clear" if os.name == "posix" else "cls")
    intents = discord.Intents.default()
    intents.message_content = True
    client = BasteRC_v2(intents=intents)
    client.run(consts.TOKEN)