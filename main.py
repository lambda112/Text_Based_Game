class Characters:   
    def __init__(self, name:str, health:int, strength:int, magic:int, attacks:dict) -> None:
        self.name = name
        self.health = health
        self.strength = strength
        self.magic = magic
        self.attacks = attacks
        power = self.strength + self.magic
        self.level = ((self.health * power) // 1000) * len(self.attacks)
    
    def calculate_damage(self):
        for i in self.attacks:
            if self.strength > self.magic:
                self.attacks[i] += self.strength
            else:
                self.attacks[i] += self.magic


    def is_dead(self):
        if self.health > 0:
            print(f"{self.name} has died.")
            return True
        else:
            return False 


    def show_stats(self):
        return f"Type: {self.name}, Health: {self.health}, Strength: {self.strength}, Magic: {self.magic}, Attacks: {self.attacks}, Level: {self.level}"
    

class Enemy(Characters):
    def __init__(self, name: str, health: int, strength: int, magic: int, attacks: dict) -> None:
        super().__init__(name, health, strength, magic, attacks)



warrior_char = Characters("Warrior", 100, 10, 0, {"Slash": 5, "Stab":3})
mage_char = Characters("Mage", 100, 0, 10, {"Fireball":5, "Zap":3})
archer_char = Characters("Archer", 100, 5, 5, {"Multi-Shot": 5, "Single-Shot":3})
spider_enemy = Enemy("Spider", 100, 5, 5, {"Web-Shot": 5, "Poison-Bite": 3})


def display_stats():
    print(warrior_char.show_stats())
    print(mage_char.show_stats())
    print(archer_char.show_stats())


def choose_char(show_stats: bool = False, name: str = "Warrior",):
    character = {"Warrior": warrior_char, "Mage": mage_char, "Archer": archer_char}
    
    if show_stats:
        return character[name].show_stats()
    
    user_char = input("Choose a character: ").capitalize()
    while user_char not in character.keys():
        user_char = input("Choose a valid character: ").capitalize()

    for char in character:
        if char == user_char:
            user_char = character[char]

    return user_char


char = choose_char()
char.calculate_damage()
spider_enemy.calculate_damage()

print(choose_char(True, char.name))