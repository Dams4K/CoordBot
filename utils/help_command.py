import discord
from discord.commands import SlashCommand, SlashCommandGroup
from discord.ext import commands
from discord.ext import bridge
from discord.ext.pages import Paginator, Page, PaginatorButton
from utils.bot_embeds import InformativeEmbed, NormalEmbed

class CommandCompatibility:
    SLASH_COMPATIBILITY = "s"
    MAPPED_SLASH_COMPATIBILITY = "m"
    PREFIX_COMPATIBILITY = "p"

class BotHelpCommand(commands.HelpCommand):
    def get_ext_command(self, ext_command: commands.Command):
        qualified_name = None
        mention = None
        compatibility = ""
        subcommands = [] #TODO

        if ext_command.enabled and not ext_command.hidden:
            if isinstance(ext_command, commands.Group):
                for command in ext_command.all_commands.values():
                    subcommands.append(self.get_ext_command(command))

            qualified_name = ext_command.qualified_name
            mention = self.context.guild_config.prefix + qualified_name
            compatibility = CommandCompatibility.PREFIX_COMPATIBILITY
        
        return qualified_name, mention, compatibility, subcommands

    def get_slash_command(self, slash_command: SlashCommand):
        qualified_name = None
        mention = None
        compatibility = ""
        subcommands = []

        if isinstance(slash_command, SlashCommand):
            qualified_name = slash_command.qualified_name
            mention = slash_command.mention
            compatibility = CommandCompatibility.SLASH_COMPATIBILITY
        elif isinstance(slash_command, SlashCommandGroup):
            if isinstance(slash_command, bridge.BridgeCommandGroup):
                if slash_command.mapped:
                    qualified_name = slash_command.mapped.qualified_name
                    mention = slash_command.mapped.mention
                    compatibility = CommandCompatibility.MAPPED_SLASH_COMPATIBILITY
            
            for subcommand in slash_command.subcommands:
                subcommands.append(self.get_slash_command(subcommand))
        
        return qualified_name, mention, compatibility, subcommands

    def get_bridge_command(self, bridge_command: bridge.BridgeCommand):
        qualified_name = None
        mention = None
        compatibility = ""
        subcommands = []

        slash_qualified_name, slash_mention, slash_compatibility, slash_subcommands = self.get_slash_command(bridge_command.slash_variant)
        ext_qualified_name, ext_mention, ext_compatibility, ext_subcommands = self.get_ext_command(bridge_command.ext_variant)

        if CommandCompatibility.MAPPED_SLASH_COMPATIBILITY == slash_compatibility:
            mention = f"{slash_mention} | {ext_mention}"
        else:
            mention = slash_mention or ext_mention
        
        qualified_name = slash_qualified_name or ext_qualified_name
        compatibility = slash_compatibility + ext_compatibility
        subcommands = slash_subcommands or ext_subcommands

        return qualified_name, mention, compatibility, subcommands

    def format_command(self, command: bridge.BridgeCommand):
        slash_variant = command.slash_variant
        ext_variant = command.ext_variant

        mentions = []
        compatibilitys = []
        subcommands = []

        if isinstance(slash_variant, SlashCommand):
            compatibilitys.append(CommandCompatibility.SLASH_COMPATIBILITY)
            mentions.append(slash_variant.mention)
        elif isinstance(slash_variant, SlashCommandGroup):
            if command.mapped:
                compatibilitys.append(CommandCompatibility.MAPPED_SLASH_COMPATIBILITY)
                mentions.append(command.mapped.mention)
            
            subcommands = self.format_bridge_commands(command.subcommands)
        
        if ext_variant.enabled:
            compatibilitys.append(CommandCompatibility.PREFIX_COMPATIBILITY)

            ext_only = not CommandCompatibility.SLASH_COMPATIBILITY in compatibilitys
            is_same_name = slash_variant.qualified_name == ext_variant.qualified_name
            if ext_only or not is_same_name:
                mentions.append(self.context.guild_config.prefix + ext_variant.qualified_name)
        
        
        formatted_mentions = " | ".join(mentions)
        formatted_compatibilitys = "".join(compatibilitys)
        formatted_subcommands = "\n> ".join(subcommands)
        if formatted_subcommands:
            formatted_subcommands = "\n> " + formatted_subcommands

        return f"{formatted_mentions} `{formatted_compatibilitys}`{formatted_subcommands}"

    def format_bridge_commands(self, bridge_commands):
        sendable_commands = []

        for command in bridge_commands:
            sendable_commands.append(self.format_command(command))
        
        return sendable_commands

    async def send_bot_help(self, mapping):
        ctx = self.context

        guild_config = ctx.guild_config

        presentation_embed = NormalEmbed(guild_config, title="‎ ‎ ‎ ‎ Page d'aide ‎ ‎ ‎ ‎")

        pages = [presentation_embed]

        for cog, raw_commands in mapping.items():
            if cog is None or raw_commands == []:
                continue
            
            bridge_commands = [command for command in raw_commands if isinstance(command, bridge.BridgeCommand)]
            ext_commands = [command for command in raw_commands if isinstance(command, commands.Command)]
            slash_commands = [command for command in raw_commands if isinstance(command, SlashCommand)]

            bot_commands = {}

            for command in bridge_commands:
                command_info = self.get_bridge_command(command)
                bot_commands.setdefault(command_info[0], command_info[1:])

            for command in ext_commands:
                command_info = self.get_ext_command(command)
                bot_commands.setdefault(command_info[0], command_info[1:])
                
            for command in slash_commands:
                command_info = self.get_slash_command(command)
                bot_commands.setdefault(command_info[0], command_info[1:])
            
            description = "\n".join(self.format_bridge_commands(bridge_commands))

            page_embed = InformativeEmbed(guild_config, title=f"Aide {cog.qualified_name.replace('Cog', '')}", description=description)
            pages.append(page_embed)

        paginator = Paginator(pages)
        await paginator.send(ctx)