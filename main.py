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
        self.level = 0
        self.experience = (self.strength + self.magic + self.health)


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

    
class Room():

    def __init__(self, items:dict) -> None:
        self.exp = 0
        self.money = 0
        self.items = items
        self.enemy_chance = 20
        self.room_num = 1


    def choose_path(self):
        path = input(f"Enter 'w' to go west towards an enemy, or 'e' to go east towards an item shop. However be warned there is a 1 in {self.enemy_chance} chance of encountering a boss type enemy. ")
        while path not in ["w", "e"]:
            path = input("Enter 'w' or 'e': ")

        return path
    

    def calculate_xp(enemy):
        xp = (enemy.strength + enemy.magic + enemy.health)
        return xp
    

    def calculate_money(enemy):
        money = enemy.strength + enemy.magic
        return money
    

    def calculate_enemy(self):
        num = 0
        if self.room_num >= 5:
            num = 5
        elif self.room_num >= 10:
            num = 10

        print(num)
        return num
    

    def enter_room(self, path, char):
        print(enemy)
        while True:
            print(f"Room: {self.room_num}")
            if path == "w":
                print(self.calculate_enemy())
                enemy = enemy[self.calculate_enemy()]
                battle(char, enemy)
                char.experience -= self.calculate_xp(enemy)
                char.money += self.calculate_money(enemy)
            else:
                if random.randint(0,self.enemy_chance) == self.enemy_chance or self.enemy_chance == 0:
                    enemy = enemy["e"]
                    battle(char, enemy)
                else:
                    print("Shop is not open yet")
                    self.enemy_chance -= 2

            if char.experience < 0:
                char.level += 1
                char.strength += 3
                char.magic += 2
                char.health += 20
                char.experience = (char.strength + char.magic + char.health)
            else:
                print(f"{char.name} is level {char.level} and requires {char.experience} xp.")

            self.room_num += 1
            self.choose_path()


# Player Stats
warrior_char = Characters("Warrior", 100, 10, 0, {"Slash": 5, "Stab":3})
mage_char = Characters("Mage", 100, 0, 10, {"Fireball":5, "Zap":3})
archer_char = Characters("Archer", 100, 5, 5, {"Multi-Shot": 5, "Single-Shot":3})


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
room = Room(0, 0, 0)
print(choose_char(True, char.name))
room.enter_room(room.choose_path(), char)


room_five_enemies = {
    "Spider":Enemy("Spider", 25, 4, 5, {"Web-Shot": 5, "Poison-Bite": 3}),
    "Goblin":Enemy("Goblin", 20, 6, 1, {"Gob Smash": 3, "Gob Punch": 2}),
    "Scarecrow":Enemy("Scarecrow", 30, 2, 4, {"Scare":1, "Crow": 5})     
    }