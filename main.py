import random
import os
from time import sleep


class Characters:   
    def __init__(self, name:str, health:int, strength:int, magic:int, attacks:dict) -> None:
        self.name = name
        self.health = health
        self.strength = strength
        self.magic = magic
        self.attacks = attacks
        power = self.strength + self.magic
        self.level = ((self.health * power) // 1000) * len(self.attacks)


    def show_stats(self) -> str:
        return f"Type: {self.name}, Health: {self.health}, Strength: {self.strength}, Magic: {self.magic}, Attacks: {self.attacks}, Level: {self.level}"
    

    def calculate_damage(self) -> None:
        for i in self.attacks:
            if self.strength > self.magic:
                self.attacks[i] += self.strength
            else:
                self.attacks[i] += (self.magic + random.randint(1, self.magic))


    def is_alive(self) -> bool:
        if self.health < 0:
            print(f"{self.name} has died.")
            return False
        else:
            return True 
        

    def attack(self) -> int:
        if self.is_alive():
            attack_list = list(self.attacks.keys())
            attack_name = random.choice(attack_list)
            attack_damage = self.attacks[attack_name]
            print(f"{self.name} uses {attack_name} it does {attack_damage} damage!")
            sleep(2)
            return attack_damage
        else:
            return 0
    

    def damage(self, damage) -> None:
        self.health -= damage
        print(f"{self.name} now has {self.health} health!\n")
        sleep(2)


    def game_end(self):
        end_game = ""
        while end_game != "end":
            end_game = input("Type 'end' to finish game. ").lower()

        sleep(1.1)
        os._exit(200)

    

class Enemy(Characters):
    def __init__(self, name: str, health: int, strength: int, magic: int, attacks: dict) -> None:
        super().__init__(name, health, strength, magic, attacks)


# Player Stats
warrior_char = Characters("Warrior", 100, 10, 0, {"Slash": 5, "Stab":3})
mage_char = Characters("Mage", 100, 0, 10, {"Fireball":5, "Zap":3})
archer_char = Characters("Archer", 100, 5, 5, {"Multi-Shot": 5, "Single-Shot":3})

# Enemy Stats
spider_enemy = Enemy("Spider", 10, 1, 5, {"Web-Shot": 5, "Poison-Bite": 3})


def display_stats():
    print(warrior_char.show_stats())
    print(mage_char.show_stats())
    print(archer_char.show_stats())


def choose_char(show_stats: bool = False, name: str = "Warrior",):
    character = {"Warrior": warrior_char, "Mage": mage_char, "Archer": archer_char}
    
    if show_stats:
        name = name.split(" ")
        return character[name[0]].show_stats()
    
    user_char = input("Choose a character: ").capitalize()
    while user_char not in character.keys():
        user_char = input("Choose a valid character: ").capitalize()

    for char in character:
        if char == user_char:
            user_char = character[char]

    user_char.name = user_char.name + " " + input("What would you like to name your character?: ").title()
    return user_char


def battle(character, enemy):
    character.calculate_damage()
    enemy.calculate_damage()
    print(f"You come across a {enemy.name}.\nIt attacks!\n")
    sleep(1.2)

    while True:
        # Player Turn
        if character.is_alive():
            char_damage = character.attack()
            enemy.damage(char_damage)
        else:
            print(f"{character.name} has lost to {enemy.name}!\nEnding Game!")
            character.game_end()
            
        # Enemy Turn
        if enemy.is_alive():
            enemy_damage = enemy.attack()
            character.damage(enemy_damage)
        else:
            print(f"{character.name} has beat {enemy.name}!\nCongratulations!")
            return None


char = choose_char()
print(choose_char(True, char.name))
sleep(2)
print("")
battle(char, spider_enemy)
