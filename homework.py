from typing import Dict, Tuple, Type
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        dist = self.get_distance()
        return dist / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__, self.duration,
                              self.get_distance(), self.get_mean_speed(),
                              self.get_spent_calories()
                              )
        return message


class Running(Training):
    """Тренировка: бег."""
    RUN_CAL_1: int = 18
    RUN_CAL_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mid_speed: float = self.get_mean_speed()
        return (
            (self.RUN_CAL_1 * mid_speed - self.RUN_CAL_2) * self.weight
            / self.M_IN_KM * self.duration * self.HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_CAL_1: float = 0.035
    WALK_CAL_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mid_speed: float = self.get_mean_speed()
        return (
            (self.WALK_CAL_1 * self.weight + (mid_speed**2 // self.height)
             * self.WALK_CAL_2 * self.weight) * self.duration * self.HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    SWIM_CAL_1: float = 1.1
    SWIM_CAL_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mid_speed: float = self.get_mean_speed()
        return (mid_speed + self.SWIM_CAL_1) * self.SWIM_CAL_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    sport: Dict[str, Type[Training]] = {'SWM': Swimming,
                                        'RUN': Running,
                                        'WLK': SportsWalking
                                        }
    training = sport[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info: Type[InfoMessage] = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: Tuple[str, float] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
