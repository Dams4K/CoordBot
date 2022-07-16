def is_admin(ctx):
    return ctx.author.guild_permissions.administrator