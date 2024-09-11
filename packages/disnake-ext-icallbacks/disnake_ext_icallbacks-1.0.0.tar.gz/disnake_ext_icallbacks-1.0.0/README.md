# disnake-ext-icallbacks

disnake-ext-icallbacks (**i**nteraction **callbacks**) is an extension that allows you to create callback listeners with custom IDs. You will find this useful if you hate `View` classes like me (and too lazy to stack `on_interaction` events, or simply love the callback decorators from [interactions.py](https://github.com/interactions-py/interactions.py).

---

## Installation

**Python 3.8 or higher is required.**

To install the extension, simply run the following command:

```py
pip install disnake-ext-icallbacks
```

It will be installed with your disnake installation and can be imported with:

```py
from disnake.ext import icallbacks
# or
from disnake.ext.icallbacks import *
```

## Usage & Examples

To use this extension, you must first hook it to your bot instance:

```py
import disnake
from disnake.ext import commands, icallbacks

bot = commands.Bot(...)
icallbacks.setup(bot)
```

This will inject the `@component_callback` and `@modal_callback` decorators to your bot instance and set up the necessary event listeners.

---

Then, you can use the decorators to create a component/modal listener with the custom ID:

```py
@bot.slash_command()
async def button(self, inter: disnake.ApplicationCommandInteraction):
    await inter.send(
        components=[
            disnake.ui.Button(label="Click Me", custom_id="button_custom_id"),
        ],
    )

@bot.component_callback("button_custom_id")
async def on_button_click(inter: disnake.MessageInteraction):
    await inter.send("Button clicked!")
```

or in a cog class:

```py
class MyCog(commands.Cog):
    @icallbacks.component_callback("button_custom_id")
    async def on_button_click(self, inter: disnake.MessageInteraction):
        await inter.send("Button clicked!")
```

---

You can also use the `@modal_callback` decorator to create a modal listener with the custom ID:

```py
@bot.slash_command()
async def modal(self, inter: disnake.ApplicationCommandInteraction):
    await inter.response.send_modal(
        title="test",
        custom_id="modal_custom_id",
        components=[disnake.ui.TextInput(label="Input", custom_id="input1")]
    )

@bot.modal_callback("modal_custom_id")
async def on_modal_submit(inter: disnake.MessageInteraction):
    await inter.send(f"Input: {inter.text_values["input1"]}")
```

or again, in a cog class:

```py
class MyCog(commands.Cog):
    @icallbacks.modal_callback("modal_custom_id")
    async def on_modal_submit(self, inter: disnake.MessageInteraction):
        await inter.send(f"Input: {inter.text_values["input1"]}")
```

---

Additionally, you can match the custom ID with a regex pattern:

```py
import re

re_pattern = re.compile(r"button_custom_id:(\d+)")

@bot.slash_command()
async def buttons(self, inter: disnake.ApplicationCommandInteraction):
    await inter.send(
        components=[
            disnake.ui.Button(label="B1", custom_id="button_custom_id:1"),
            disnake.ui.Button(label="B2", custom_id="button_custom_id:2"),
        ],
    )

@bot.component_callback(re_pattern)
async def on_button_click(inter: disnake.MessageInteraction):
    match = re_pattern.match(inter.data.custom_id)
    await inter.send(f"Button {match.group(1)} clicked!")
```

## Credits

This extension is inspired by the [interactions.py](https://github.com/interactions-py/interactions.py) library.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) for details.
