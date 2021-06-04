class Advancement:
    def __init__(self, p, name: str, parent: str):
        self.p = p
        self.name = name
        self.p.advancements[name] = {}
    
    def set_icon(self, itemName: str, nbt: dict=None):
        if not 'display' in self.p.advancements[self.name].keys():
            self.p.advancements[self.name]['display'] = {}
        self.p.advancements[self.name]['display']['item'] = itemName
        if nbt is not None:
            self.p.advancements[self.name]['display']['nbt'] = nbt