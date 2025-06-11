import pygame

class Car:
    def __init__(self, path, game_resulution, direction = "up"):
        self.__divisor = 5
        
        self.direction = direction
        self.resolution = self.__get_car_resolution(game_resulution)
        self.sprite = self.__import_car_image(path, direction)
        car_len = self.get_colisor()
        self.width = car_len[0]
        self.height = car_len[1]

        
    def __import_car_image(self, path, direction):
        rotation = {
            "up": 90,
            "down": 270,
            "left": 180,
            "right": 0
        }
            
        return pygame.transform.scale(pygame.transform.rotate(pygame.image.load(path), rotation[direction]), self.resolution)
    
    
    def __get_car_resolution(self, game_resolution):
        if (self.direction == "left" or self.direction == "right"):
            return (game_resolution[0] / self.__divisor, game_resolution[1] / self.__divisor)
        else:
            return (game_resolution[1] / self.__divisor, game_resolution[0] / self.__divisor)
        
    
    def get_colisor(self):
        x_tolerance = 250
        y_tolerance = 70
        
        if (self.direction == "up" or self.direction == "down"):
            return (int(self.resolution[0] - (x_tolerance / self.__divisor)), int(self.resolution[1] - (y_tolerance /self.__divisor)))
        else:
            return (int(self.resolution[1] - (x_tolerance / self.__divisor)), int(self.resolution[0] - (y_tolerance /self.__divisor)))
