import os 
import random
from time import sleep

class Stats:
    def __init__(self, type:str, health:int, strength:int, magic:int, attacks:dict) -> None:
        self.type = type
        self.health = health
        self.strength = strength
        self.magic = magic
        self.attacks = attacks
        self.old_attacks = attacks.copy()
        self.old_health = health

    def reset_stats(self):
        self.health = self.old_health
        self.attacks = self.old_attacks

    def take_damage(self,damage):
        self.health -= damage

    def attack_choice(self):
        attack_list = list(self.attacks.items())
        return random.choice(attack_list)
        
    def is_alive(self):
        return self.health > 0
    
    def rewards(self):
        reward = (self.strength + self.magic) * len(self.attacks)
        return reward
    
    def attack_bonus(self):
        return max(self.strength, self.magic)
    
    def attack_increase(self):
        self.attacks = {key:value + self.attack_bonus() for key,value in self.attacks.items()}
        return self.attacks

    def attack_effect(self):
        pass


    
class Characters(Stats):
    def __init__(self, type, health: int, strength: int, magic: int, attacks: dict) -> None:
        super().__init__(type, health, strength, magic, attacks)
        self.experience_required = (self.strength + self.magic + self.health)
        self.level = 1
        self.money = 0

    def show_stats(self) -> str:
        return f"Type: {self.type}, Health: {self.health}, Strength: {self.strength}, Magic: {self.magic}, Attacks: {self.attacks}, Level: {self.level}"

    def increase_stats(self):
        self.old_health += 20
        self.strength += 3
        self.magic += 3
        self.level += 1

        self.attack_increase()
        self.reset_stats()

    def reward(self, enemy_xp):
        self.experience_required -= enemy_xp
        self.money += enemy_xp
        if self.experience_required <= 0:
            print(f"\nYou have leveled up! You are now level {self.level}")
            print("Stats Increased.")
            self.increase_stats()
            print(f"{self.show_stats()}")
            self.experience_required = (self.strength + self.magic + self.health)
        else:
            print(f"{self.experience_required} xp till level up!")


class Enemies(Stats):
    def __init__(self, type, health: int, strength: int, magic: int, attacks: dict) -> None:
        super().__init__(type, health, strength, magic, attacks)


class Battle():
    def __init__(self) -> None:
        enemy_dict = {
        "Spider":Enemies("Spider", 25, 4, 5, {"Web-Shot": 5, "Poison-Bite": 3}),
        "Goblin":Enemies("Goblin", 20, 6, 1, {"Gob Smash": 3, "Gob Punch": 2}),
        "Scarecrow":Enemies("Scarecrow", 30, 2, 4, {"Scare":1, "Crow": 5})     
        }

        self.enemy = random.choice(list(enemy_dict.values()))
        self.enemy_xp = (self.enemy.strength + self.enemy.magic) * len(self.enemy.attacks)
        self.character = self.character_selection(self.list_of_characters())

    def list_of_characters(self):
        characters = {
        "Warrior" : Characters("Warrior", 100, 10, 0, {"Slash": 5, "Stab":3}),
        "Mage" : Characters("Mage", 100, 0, 10, {"Fireball":5, "Zap":3}),
        "Archer": Characters("Archer", 10, 5, 5, {"Multi-Shot": 5, "Single-Shot":3}),
        }

        return characters

    def character_selection_code(self,character_list):
        for char in character_list:
            print(character_list[char].show_stats())

        user_char = input("Choose a character: ").capitalize()
        while user_char not in character_list.keys():
            user_char = input("Choose a valid character: ").capitalize()

        for char in character_list:
            if char == user_char:
                user_char = character_list[char]

        user_char.type = user_char.type + " " + input("What would you like to name your character?: ").title()
        return user_char

    def character_selection(self,character, show_stats: bool = False):
        character = self.character_selection_code(character)
        if show_stats:
            name = character.type.split(" ")
            return character[name[0]].show_stats()
        
        return character

    def game_end(self):
        end_game = ""
        while end_game != "end":
            end_game = input("Type 'end' to finish game. ").lower()
        sleep(1.1)
        os._exit(200)

    def is_battle_over(self):
        if not self.enemy.is_alive():
            print(f"\n{self.character.type} has killed {self.enemy.type}")
        elif not self.character.is_alive():
            print(f"\n{self.enemy.type} has killed {self.character.type}")
            print(f"Game Ending!")
            self.game_end()
        else:
            return False
        return True
    
    def battle_start_message(self):
        print(f"\n{self.character.type.capitalize()} encounters {self.enemy.type.capitalize()}")
        print("It attacks!\n")

    def player_turn(self):
        # Player Turn
        character_attack = self.character.attack_choice()
        character_attack_name = character_attack[0]
        character_attack_damage = character_attack[1]
        self.enemy.take_damage(character_attack_damage)
        print(f"{self.character.type} uses {character_attack_name} it does {character_attack_damage} damage!")
        print(f"{self.enemy.type} now has {self.enemy.health} health!\n")

    def enemy_turn(self):
        # Enemy Turn
        enemy_attack = self.enemy.attack_choice()
        enemy_attack_name = enemy_attack[0]
        enemy_attack_damage = enemy_attack[1]
        self.character.take_damage(enemy_attack_damage)
        print(f"{self.enemy.type} uses {enemy_attack_name} it does {enemy_attack_damage} damage!")
        print(f"{self.character.type} now has {self.character.health} health!\n")

    def battle_mechanic(self):
        self.battle_init()
        while not self.is_battle_over():

            self.player_turn()
            sleep(1)

            if self.is_battle_over():
                break

            self.enemy_turn()
            sleep(1)

        self.enemy.reset_stats()
        self.character.reset_stats()
        self.character.reward(self.enemy_xp)

    def battle_init(self):
        self.character.attack_increase()
        self.enemy.attack_increase()
        self.battle_start_message()


class Game(Battle):
    def __init__(self) -> None:
        super().__init__()
        self.chance = 10
        self.room_num = 1

    def choose_path(self):
        path = input(f"Enter 'w' to go west towards an enemy, or 'e' to go east towards an item shop. However be warned there is a 1 in {self.chance} chance of encountering a boss type enemy. ").lower()
        while path not in ["w", "e"]:
            path = input("Enter 'w' or 'e': ").lower()

        return path
    
    def shop_code(self):
        if random.randint(0,self.chance) == self.chance or self.chance == 0:
            self.battle_mechanic()
            self.chance = 10
        else:
            print("Shop is not open yet.")
            self.chance -= 2

    def path_code(self):
        if self.choose_path() == "w":
            self.battle_mechanic()
        else:
            self.shop_code()

    def game_loop(self):
        while True:
            print(f"\nRoom Number: {self.room_num}")
            self.path_code()
            self.room_num += 1

game = Game()
game.game_loop()
