from discord import *

from lang import CommandLocalization


class BotSlashCommand(SlashCommand, CommandLocalization):
    def __init__(self, func: callable, *args, **kwargs) -> None:
        name: str = kwargs.get("name", func.__name__)
        parent = kwargs.get("parent", None)

        filename = name
        if isinstance(parent, CommandLocalization):
            filename = f"{parent} {name}"
        
        CommandLocalization.__init__(self, filename)
           
        kwargs.setdefault("description", self.loc_description)
        kwargs.setdefault("name_localizations", self.loc_name_localizations)
        kwargs.setdefault("description_localizations", self.loc_description_localizations)

        return SlashCommand.__init__(self, func, *args, **kwargs)
    
    def _validate_parameters(self):
        super()._validate_parameters()
        for option in self.options:
            option_localization = self.get_option_localization(option.name)
            option_localization.add_localization(option)

class BotSlashCommandGroup(SlashCommandGroup, CommandLocalization):
    def __init__(self, name: str, description: str = None, guild_ids: list[int] = None, parent = None, **kwargs) -> None:

        filename = name
        if isinstance(parent, CommandLocalization):
            filename = f"{parent} {name}"
        CommandLocalization.__init__(self, filename)
        
        description = description or self.loc_description

        kwargs.setdefault("name_localizations", self.loc_name_localizations)
        kwargs.setdefault("description_localizations", self.loc_description_localizations)

        return SlashCommandGroup.__init__(self, name, description, guild_ids, parent, **kwargs)


    def command(self, cls = BotSlashCommand, **kwargs):
        return super().command(cls, **kwargs)
    
    def create_subgroup(
        self,
        name: str,
        description: str | None = None,
        guild_ids: list[int] | None = None,
        **kwargs,
    ):
        """
        Creates a new subgroup for this BotSlashCommandGroup.

        Parameters
        ----------
        name: :class:`str`
            The name of the group to create.
        description: Optional[:class:`str`]
            The description of the group to create.
        guild_ids: Optional[List[:class:`int`]]
            A list of the IDs of each guild this group should be added to, making it a guild command.
            This will be a global command if ``None`` is passed.
        guild_only: :class:`bool`
            Whether the command should only be usable inside a guild.
        nsfw: :class:`bool`
            Whether the command should be restricted to 18+ channels and users.
            Apps intending to be listed in the App Directory cannot have NSFW commands.
        default_member_permissions: :class:`~discord.Permissions`
            The default permissions a member needs to be able to run the command.
        checks: List[callable[[:class:`.ApplicationContext`], :class:`bool`]]
            A list of predicates that verifies if the command could be executed
            with the given :class:`.ApplicationContext` as the sole parameter. If an exception
            is necessary to be thrown to signal failure, then one inherited from
            :exc:`.ApplicationCommandError` should be used. Note that if the checks fail then
            :exc:`.CheckFailure` exception is raised to the :func:`.on_application_command_error`
            event.
        name_localizations: Optional[Dict[:class:`str`, :class:`str`]]
            The name localizations for this command. The values of this should be ``"locale": "name"``. See
            `here <https://discord.com/developers/docs/reference#locales>`_ for a list of valid locales.
        description_localizations: Optional[Dict[:class:`str`, :class:`str`]]
            The description localizations for this command. The values of this should be ``"locale": "description"``.
            See `here <https://discord.com/developers/docs/reference#locales>`_ for a list of valid locales.

        Returns
        -------
        BotSlashCommandGroup
            The slash command group that was created.
        """

        if self.parent is not None:
            # TODO: Improve this error message
            raise Exception("a subgroup cannot have a subgroup")

        sub_command_group = BotSlashCommandGroup(
            name, description, guild_ids, parent=self, **kwargs
        )
        self.subcommands.append(sub_command_group)
        return sub_command_group


class BotUserCommand(UserCommand, CommandLocalization):
    def __init__(self, func: callable, *args, **kwargs):
        filename = kwargs.get("name", func.__name__.capitalize())

        CommandLocalization.__init__(self, filename)

        capitalized_loc_name_localizations = None
        if self.loc_name_localizations:
            capitalized_loc_name_localizations = {key: value.capitalize() for key, value in self.loc_name_localizations.items()}

        kwargs.setdefault("name_localizations", capitalized_loc_name_localizations)

        return UserCommand.__init__(self, func, *args, **kwargs)

class BotMessageCommand(MessageCommand, CommandLocalization):
    def __init__(self, func: callable, *args, **kwargs):
        filename = kwargs.get("name", func.__name__.capitalize())

        CommandLocalization.__init__(self, filename)
        
        capitalized_loc_name_localizations = None
        if self.loc_name_localizations:
            capitalized_loc_name_localizations = {key: value.capitalize() for key, value in self.loc_name_localizations.items()}

        kwargs.setdefault("name_localizations", capitalized_loc_name_localizations)

        return MessageCommand.__init__(self, func, *args, **kwargs)
    

def bot_user_command(**kwargs):
    """Decorator for user commands that invokes :func:`application_command`.

    .. versionadded:: 2.0

    Returns
    -------
    Callable[..., :class:`.UserCommand`]
        A decorator that converts the provided method into a :class:`.UserCommand`.
    """
    return application_command(cls=BotUserCommand, **kwargs)

def bot_message_command(**kwargs):
    """Decorator for message commands that invokes :func:`application_command`.

    .. versionadded:: 2.0

    Returns
    -------
    Callable[..., :class:`.MessageCommand`]
        A decorator that converts the provided method into a :class:`.MessageCommand`.
    """
    return application_command(cls=BotMessageCommand, **kwargs)

def bot_slash_command(**kwargs):
    """Decorator for slash commands that invokes :func:`application_command`.

    .. versionadded:: 2.0

    Returns
    -------
    Callable[..., :class:`.SlashCommand`]
        A decorator that converts the provided method into a :class:`.SlashCommand`.
    """
    return application_command(cls=BotSlashCommand, **kwargs)