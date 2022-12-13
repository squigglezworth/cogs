# ⚙️ Some things for Pycord
*Constructive suggestions are welcome*

<details>
  <summary><i><a href="cogs/roles.py"><b><code>roles</code></b></a> - Powerful role management system</i></summary>

  - Give users a simple role management UI
  - Define multiple commands/menus at runtime
  - Allow only a single role per menu (e.g. for letting the user choose a role icon role)
  - To use, see [`main.py#L4-L117`](main.py#L4-L117) for how to define menus, then import roles and call `roles.Roles()`
  - This will register at least 1 new command based on the settings provided
  <hr>
</details>
<details>
  <summary><i><a href="cogs/colors.py"><b><code>colors</code></b></a> - Easy color role management for both admins and users - <b>Inspired by <a href="https://fluxpoint.dev/reactify">Reactify</a></b></i></summary>

  - Admins can easily define new color roles by prefixing them with `[C]` (or change the prefix)
  - The cog will build a simple menu for users based on these rules
  - To use, simply add some color roles to your server, then import & add the cog
  - This will register `/colors`
<hr>
</details>
<details>
  <summary><i><a href="cogs/imdb.py"><b><code>imdb</code></b></a> - Simple IMDb lookup</i></summary>

  - Consider building a local sqlite database using [`imdb-dataset.sh`](imdb-dataset.sh), as this will speed things up considerably
  - Search by name or provide an ID
  - To use, just import and add the cog
  - This will register `/imdb`
  <hr>
</details>
<details>
  <summary><i><a href="cogs/publisher.py"><b><code>publisher</code></b></a> - Automagically publish messages from <a href="https://support.discord.com/hc/en-us/articles/360032008192-Announcement-Channels-">Announcement</a> channels</i></summary>

  - There are currently no permissions checks; disable access through your server's Integration settings
  - You may have to replace the emojis on [`cogs/publisher.py#L8-L22`](cogs/publisher.py#L8-L22)
  - To use, simply import and register the cog
  - This will register `/publisher`
  <hr>
</details>

## Usage
Check out [`example.py`](example.py) for basic usage of all these components.

See [`main.py`](main.py) for more practical examples:
- [Setting up logging](main.py#L123-L134)
- [Loading some things from `.env`](main.py#L136-L139)
- [`main.py#L156-L203`](main.py#L156-L203) combines views from `roles` & `colors` in one `/customize` command

## Screenshots
<details>
<summary><code>/customize</code></summary>
<img width=400 src="https://user-images.githubusercontent.com/20311086/205825222-a8a3e84a-2472-480c-9d46-eef7d5301285.gif" />
</details>
<details>
<summary><code>roles</code></summary>
  <img width=300 src="https://user-images.githubusercontent.com/20311086/204404664-07412de2-a306-42ec-b39c-5b7479b6c3d1.png" />
  <img width=300 src="https://user-images.githubusercontent.com/20311086/204404999-318706f3-36f2-434e-bf1d-f983e4ee345c.png" />
</details>
<details>
<summary><code>imdb</code></summary>
<img width=500 src="https://user-images.githubusercontent.com/20311086/204405345-07660af7-245b-4115-813e-db56570b51c1.png" />
<br>
<img width=300 src="https://user-images.githubusercontent.com/20311086/204405505-507a406d-8125-4fdc-b0cb-709a9b32d0fa.png" />
<img width=300 src="https://user-images.githubusercontent.com/20311086/204405847-f88bd9c7-fc9f-4a8d-9042-55a530b13d28.png" />
</details>
<details>
<summary><code>colors</code></summary>
<img width=400 src="https://user-images.githubusercontent.com/20311086/201162102-163788cd-9231-4cfe-81a9-661c24b7a22a.png" />
</details>
