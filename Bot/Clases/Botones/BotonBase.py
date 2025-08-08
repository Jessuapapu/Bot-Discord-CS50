from discord import ButtonStyle, Interaction, ui

class botonBase():
    def __init__(self, label: str, style: ButtonStyle):
        self.boton = ui.Button(label=label, style=style)
        self.boton.callback = self.callBack

    async def callBack(self, interaction_button: Interaction):
        pass

