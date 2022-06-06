from django.db import models 
from django.contrib.auth.models import User
from copy import copy
from .constants import * 

class Core(models.Model): 
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE) 
    coins = models.IntegerField(default=0) 
    click_power = models.IntegerField(default=1) 
    level = models.IntegerField(default=1)
    auto_click_power = models.IntegerField(default=0)

    # def click(self): 
    #     self.coins += self.click_power

    #     if self.coins >= self.calculate_next_level_price(): 
    #         self.level += 1                       
    
    #         return True 
    #     return False 

    def set_coins(self, coins, commit=True): 
        self.coins = coins
        boost_type = self.get_boost_type()
        is_level_updated = self.is_levelup() 

        if is_level_updated:
            self.level += 1
        if commit:
            self.save()

        return is_level_updated, boost_type
    
    def get_boost_type(self):
        if self.level % 3 == 0:
            return BOOST_TYPE_NAME_TO_NUMBER['auto']
        return BOOST_TYPE_NAME_TO_NUMBER['casual']
    
    def is_levelup(self):
        return self.coins >= self.calculate_next_level_price()
     
    def calculate_next_level_price(self): 
        return (self.level**2)*10*(self.level) 

class Boost(models.Model): 
    core = models.ForeignKey(Core, null=False, on_delete=models.CASCADE) 
    level = models.IntegerField(default=0) 
    price = models.IntegerField(default=10) 
    power = models.IntegerField(default=1)

    type = models.PositiveSmallIntegerField(default=0, choices=BOOST_TYPE_CHOICES) # Поле с типом буста. PositiveSmallInteger не позволяет значению быть меньше нуля.
                                                                                   # Атрибут choices позволяют в админке смотреть в поле тип буста и вместо цифр видеть буквы.
    def levelup(self, current_coins): 
        if self.price > current_coins: # Если монет недостаточно, ничего не делаем. 
            return False

        old_boost_stats = copy(self)

        self.core.coins = current_coins - self.price 
        self.core.click_power += self.power * BOOST_TYPE_VALUES[self.type]['click_power_scale'] # Умножаем силу клика на константу.
        self.core.auto_click_power += self.power * BOOST_TYPE_VALUES[self.type]['auto_click_power_scale'] # Умножаем силу автоклика на константу.
        self.core.save() 

        self.level += 1 
        self.power *= 2
        self.price *= self.price * BOOST_TYPE_VALUES[self.type]['price_scale'] # Умножаем ценник на константу.
        self.save() 

        return old_boost_stats, self