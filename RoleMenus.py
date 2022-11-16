import discord, re, random
from random import shuffle
from discord.ext import commands

class BuildDropdown(discord.ui.Select):
    def __init__(self, dropdown, settings, ctx, LastUpdates = None):
        options = []
        self.dropdown = dropdown
        self.settings = settings
        self.ctx = ctx

        if dropdown["randomize"]:
            shuffle(dropdown["roles"])

        # Start building the dropdown menu for a given list of 'roles'
        for r in dropdown["roles"]:
            role = ctx.guild.get_role(r[0])

            update = None
            if LastUpdates and role in [u[1] for u in LastUpdates]:
                update = list(filter(lambda u: u[1] == role, LastUpdates))[0][0]

            description = r[1]
            # When a user already has this role - or when the user added it last time - change the description accordingly
            # if role in ctx.user.roles or (LastUpdate and LastUpdate[0] == 1 and role is LastUpdate[1]):
            if role in ctx.user.roles or update == 1:
                description="You already have this role. Click to remove it"
            # If the user removed the role last time - and it is thus available again - reset the description
            # if LastUpdate and LastUpdate[0] == 0 and role is LastUpdate[1]:
            if update == 0:
                description=r[1]
            # The above checks are necessary due to an outdated user instance - unsure how to retrieve an updated one

            # Add each role to the list of options
            option = discord.SelectOption(
                label=role.name,
                description=description,
                value=str(role.id)
            )
            # Add the emoji provided during setup
            if r[2]:
                option.emoji = r[2]
            options += [option]

        # Assemble & return the dropdown menu
        super().__init__(
                placeholder=dropdown["placeholder"],
                options=options,
                min_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        """
        Respond to a user selecting a role from a menu
        """
        UserRoles = interaction.user.roles
        LastUpdates = []
        for r in self.values:
            # Get the role the user has selected
            role = interaction.guild.get_role(int(r))
            # Remove it if they already have it
            if role in interaction.user.roles:
                print(f"[roles - {self.ctx.command}] Removing roles from {interaction.user}")

                # Prepare info for updating the message
                # deleted, role
                LastUpdates.append([0, role])
                # Remove it from a list of user's current roles, which will be displayed when the message is updated
                UserRoles.remove(role)

                await interaction.user.remove_roles(role)
            else:
                # If specified, only allow 1 role from this menu
                if self.settings["max_one"]:
                    print(f"[roles - {self.ctx.command}] max_one specified; removing all roles")

                    MenuRoles = []
                    # Assemble a list of all roles for this menu
                    for m in self.settings["dropdowns"]:
                        for r in m["roles"]:
                            MenuRoles += [r[0]]

                    # Add all the roles we're about to remove to the LastUpdates array
                    for f in filter(lambda r: r.id in [r for r in MenuRoles], interaction.user.roles):
                        LastUpdates.append([0,f])

                    # Filter out the roles in this menu from the user's roles
                    UserRoles = list(filter(lambda r: r.id not in [r for r in MenuRoles], interaction.user.roles))

                    # Update the user's roles
                    await interaction.user.edit(roles=UserRoles)

                print(f"[roles - {self.ctx.command}] Adding roles to {interaction.user}")

                # Prepare info for updating the message
                # added, role
                LastUpdates.append([1, role])
                # Add it to a list of user's current roles, which will be displayed when the message is updated
                UserRoles.insert(0, role)

                # Finally add the role to the user
                await interaction.user.add_roles(role)

        # Retrieve the message embed & view
        # The embed contains some message, usually a list of the user's roles
        # The view contains the dropdown menus
        embed, view = BuildMessage(self.ctx, UserRoles, self.settings, LastUpdates)

        # Update the existing message with the embed & view
        await interaction.response.edit_message(embed=embed, view=view)

class BuildClearButton(discord.ui.Button):
    def __init__(self, settings, ctx, LastUpdates = None):
        self.ctx = ctx
        self.settings = settings
        self.LastUpdates = LastUpdates

        super().__init__(label="Clear all roles",
                         style=discord.ButtonStyle.danger)

    async def callback(self, interaction):
        print(f"[roles - {self.ctx.command}] {interaction.user} selected 'Clear all'")

        # Build a list of all roles in this menu
        MenuRoles = []
        for m in self.settings["dropdowns"]:
            for r in m["roles"]:
                MenuRoles += [r[0]]

        # Add all the roles we're about to remove to the LastUpdates array
        LastUpdates = []
        for f in filter(lambda r: r.id in [r for r in MenuRoles], interaction.user.roles):
            LastUpdates.append([0,f])

        # Remove them from the user's roles and update the user
        UserRoles = list(filter(lambda r: r.id not in [r for r in MenuRoles], interaction.user.roles))
        await interaction.user.edit(roles=UserRoles)

        # Update the message
        embed, view = BuildMessage(self.ctx, UserRoles, self.settings, LastUpdates)
        await interaction.response.edit_message(embed=embed, view=view)

class BuildView(discord.ui.View):
    """
    Assemble the dropdowns for a given menu into a View
    """
    def __init__(self, menu, ctx, LastUpdates = None):
        super().__init__()

        for dropdown in menu["dropdowns"]:
            self.add_item(BuildDropdown(dropdown, menu, ctx, LastUpdates))
        self.add_item(BuildClearButton(menu, ctx, LastUpdates))

def BuildMessage(ctx, UserRoles, menu, LastUpdates = None):
    """
    Builds & returns the message (embed & view) to /commands and interactions
    """
    MenuRoles = []
    RolesList = ""
    ShortRolesList = ""

    # Assemble a list of all roles for this menu
    for m in menu["dropdowns"]:
        for r in m["roles"]:
            MenuRoles += [r[0]]

    # Here we build the list of the user's current roles
    for r in reversed(UserRoles):
        if r.id not in menu["exclude"] + [484805623209525258]:
            RolesList += f"<@&{r.id}> "
        if r.id in MenuRoles:
            ShortRolesList += f"<@&{r.id}> "
    if not ShortRolesList:
        ShortRolesList = "empty!"

    # Prepare the View
    # If the user has selected a role, pass it along (LastUpdate)
    view = BuildView(menu, ctx, LastUpdates)

    # Prepare the embed
    data = {
        "ctx": ctx,
        "RolesList": RolesList,
        "ShortRolesList": ShortRolesList
    }
    embed = discord.Embed(color=0x299aff, description=menu["embed"].format(**data))

    return embed, view

async def CommandCallback(ctx):
    print(f"[roles - {ctx.command}] Responding to {ctx.user}")

    global SETTINGS

    # Prepare the embed & view for the initial response, passing the user's roles at the time of calling
    UserRoles = ctx.user.roles
    embed, view = BuildMessage(ctx, UserRoles, SETTINGS[str(ctx.command)])

    await ctx.respond(ephemeral=True, embed=embed, view=view)

SETTINGS = None
def register(bot, settings, guilds = None):
    """
    Register commands based on the passed menus - see main.py for example
    """
    global SETTINGS
    SETTINGS = settings

    for c in settings:
        print(f"[roles] Registering /{c}" + (f" on {len(guilds)} guilds" if guilds else " globally"))

        command = discord.SlashCommand(
                            CommandCallback,
                            callback=CommandCallback,
                            name=c,
                            description=settings[c]["description"])

        bot.add_application_command(command)
