import discord
from discord.commands import SlashCommand
from discord.ext import commands
from discord.ext import bridge
from discord.ext.pages import Paginator, Page, PaginatorButton
from utils.bot_embeds import InformativeEmbed, NormalEmbed

class CommandCompatibility:
    SLASH_COMPATIBILITY = "s"
    MAPPED_SLASH_COMPATIBILITY = "m"
    PREFIX_COMPATIBILITY = "p"

class BotHelpCommand(commands.HelpCommand):
    def prettify_bridge_commands(self, bridge_commands, guild_prefix):
        sendable_commands = []

        for command in bridge_commands:
            slash_variant = command.slash_variant
            ext_variant = command.ext_variant

            command_compatibility = ""
            sendable_subcommands = []
            if not slash_variant.id is None or (not slash_variant.parent is None and not slash_variant.qualified_id is None):
                command_compatibility += CommandCompatibility.SLASH_COMPATIBILITY
            elif isinstance(command, bridge.BridgeCommandGroup):
                if command.mapped:
                    command_compatibility += CommandCompatibility.MAPPED_SLASH_COMPATIBILITY
                sendable_subcommands = [f"\n> {subcommand}" for subcommand in self.prettify_bridge_commands(command.subcommands, guild_prefix)]
                sendable_subcommands.append("\n")
            
            if ext_variant.enabled:
                command_compatibility += CommandCompatibility.PREFIX_COMPATIBILITY
            
            command_mention = "no_mention_found"
            if CommandCompatibility.SLASH_COMPATIBILITY in command_compatibility:
                command_mention = f"</{slash_variant.qualified_name}:{slash_variant.qualified_id}>"
            elif CommandCompatibility.PREFIX_COMPATIBILITY in command_compatibility:
                command_mention = guild_prefix + ext_variant.name
            
            if CommandCompatibility.MAPPED_SLASH_COMPATIBILITY in command_compatibility:
                command_mention += f" | </{command.mapped.qualified_name}:{command.mapped.qualified_id}>"

            sendable_commands.append(f"{command_mention} `{command_compatibility}`" + "".join(sendable_subcommands))
        
        return sendable_commands

    async def send_bot_help(self, mapping):
        ctx = self.context

        guild_config = ctx.guild_config

        presentation_embed = NormalEmbed(guild_config, title="Page d'aide")

        pages = [presentation_embed]

        for cog, raw_commands in mapping.items():
            if cog is None or raw_commands == []:
                continue
            
            bridge_commands = [command for command in raw_commands if isinstance(command, bridge.BridgeCommand)]
            ext_commands = [command for command in raw_commands if isinstance(command, commands.Command)]
            slash_commands = [command for command in raw_commands if isinstance(command, SlashCommand)]

            description = "\n".join(self.prettify_bridge_commands(bridge_commands, guild_config.prefix))

            page_embed = InformativeEmbed(guild_config, title=f"Aide {cog.qualified_name.replace('Cog', '')}", description=description)
            pages.append(page_embed)

        paginator = Paginator(pages)
        await paginator.send(ctx)