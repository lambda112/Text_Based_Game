class Characters:
    
    def __init__(self, name:str, health:int, strength:int, magic:int, attacks:dict):
        self.type = name
        self.health = health
        self.strength = strength
        self.magic = magic
        self.attacks = attacks
        
    def calculate_level(self):
        power = self.strength + self.magic
        self.level = ((self.health * power) // 1000) * len(self.attacks)
        return self.level
    
    def calculate_damage(self):
        for i in self.attacks:
            self.attacks[i] += self.strength

    def show_stats(self):
        return f"Type: {self.type}, Health: {self.health}, Strength: {self.strength}, Magic: {self.magic}, Attacks: {self.attacks}, Level: {self.calculate_level()}"

warrior = Characters("Warrior", 100, 10, 0, {"Slash": 5, "Stab":3})
mage = Characters("Mage", 100, 0, 10, {"Fireball":5, "Zap":3})
archer = Characters("Archer", 100, 5, 5, {"Multi-Shot": 5, "Single-Shot":3})

print(warrior.show_stats())
print(mage.show_stats())
print(archer.show_stats())