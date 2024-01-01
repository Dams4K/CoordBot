def command(
        self,
        name: str = MISSING,
        cls: type[CommandT] = MISSING,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[[Callable[Concatenate[ContextT, P], Coro[Any]]], CommandT]:
        """A shortcut decorator that invokes :func:`.command` and adds it to
        the internal command list via :meth:`~.GroupMixin.add_command`.

        Returns
        -------
        Callable[..., :class:`Command`]
            A decorator that converts the provided method into a Command, adds it to the bot, then returns it.
        """

        def decorator(func: Callable[Concatenate[ContextT, P], Coro[Any]]) -> CommandT:
            kwargs.setdefault("parent", self)
            result = command2(name=name, cls=cls, *args, **kwargs)(func)
            self.add_command(result)
            return result

        return decorator


def command2(
    name: str = MISSING, cls: type[CommandT] = MISSING, **attrs: Any
) -> Callable[
    [
        (
            Callable[Concatenate[ContextT, P], Coro[Any]]
            | Callable[Concatenate[CogT, ContextT, P], Coro[T]]
        )
    ],
    Command[CogT, P, T] | CommandT,
]:
    """A decorator that transforms a function into a :class:`.Command`
    or if called with :func:`.group`, :class:`.Group`.

    By default the ``help`` attribute is received automatically from the
    docstring of the function and is cleaned up with the use of
    ``inspect.cleandoc``. If the docstring is ``bytes``, then it is decoded
    into :class:`str` using utf-8 encoding.

    All checks added using the :func:`.check` & co. decorators are added into
    the function. There is no way to supply your own checks through this
    decorator.

    Parameters
    ----------
    name: :class:`str`
        The name to create the command with. By default, this uses the
        function name unchanged.
    cls
        The class to construct with. By default, this is :class:`.Command`.
        You usually do not change this.
    attrs
        Keyword arguments to pass into the construction of the class denoted
        by ``cls``.

    Raises
    ------
    TypeError
        If the function is not a coroutine or is already a command.
    """
    if cls is MISSING:
        cls = Command  # type: ignore

    def decorator(func):
        if isinstance(func, Command):
            raise TypeError("Callback is already a command.")
        return cls(func, name=name, **attrs)

    return decorator

def add_command(self, command: Command[CogT, Any, Any]) -> None:
        """Adds a :class:`.Command` into the internal list of commands.

        This is usually not called, instead the :meth:`~.GroupMixin.command` or
        :meth:`~.GroupMixin.group` shortcut decorators are used instead.

        .. versionchanged:: 1.4
             Raise :exc:`.CommandRegistrationError` instead of generic :exc:`.ClientException`

        Parameters
        ----------
        command: :class:`Command`
            The command to add.

        Raises
        ------
        :exc:`.CommandRegistrationError`
            If the command or its alias is already registered by different command.
        TypeError
            If the command passed is not a subclass of :class:`.Command`.
        """

        if not isinstance(command, Command):
            raise TypeError("The command passed must be a subclass of Command")

        if isinstance(self, Command):
            command.parent = self

        if command.name in self.prefixed_commands:
            raise CommandRegistrationError(command.name)

        self.prefixed_commands[command.name] = command
        for alias in command.aliases:
            if alias in self.prefixed_commands:
                self.remove_command(command.name)
                raise CommandRegistrationError(alias, alias_conflict=True)
            self.prefixed_commands[alias] = command

# OPTIONAL

def group(
        self,
        name: str = MISSING,
        cls: type[GroupT] = MISSING,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[[Callable[Concatenate[ContextT, P], Coro[Any]]], GroupT]:
        """A shortcut decorator that invokes :func:`.group` and adds it to
        the internal command list via :meth:`~.GroupMixin.add_command`.

        Returns
        -------
        Callable[..., :class:`Group`]
            A decorator that converts the provided method into a Group, adds it to the bot, then returns it.
        """

        def decorator(func: Callable[Concatenate[ContextT, P], Coro[Any]]) -> GroupT:
            kwargs.setdefault("parent", self)
            result = group(name=name, cls=cls, *args, **kwargs)(func)
            self.add_command(result)
            return result

        return decorator