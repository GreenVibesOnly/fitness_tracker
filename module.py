from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        '''Выводит информацию о тренировке на экран.'''
        return self.message.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    M_IN_KM = 1000
    MIN_IN_HR = 60
    LEN_STEP = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Переопределите get_spent_calories '
            f'в классе {self.__class__.__name__}.'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    LEN_STEP: float = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий при беге."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HR))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float

    LEN_STEP: float = 0.65
    CALORIES_WEIGHT_MULTIPLIER_1: float = 0.035
    CALORIES_WEIGHT_MULTIPLIER_2: float = 0.029
    KM_H_IN_M_C: float = 0.278
    M_IN_CM: int = 100

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий при ходьбе."""
        return ((self.CALORIES_WEIGHT_MULTIPLIER_1
                * self.weight
                + ((self.get_mean_speed() * self.KM_H_IN_M_C)**2
                   / (self.height / self.M_IN_CM))
                * self.CALORIES_WEIGHT_MULTIPLIER_2
                * self.weight) * (self.duration * self.MIN_IN_HR))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float  # M
    count_pool: int

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_MULTIPLIER: int = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий при плавании."""
        return ((self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.CALORIES_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    class_code = {'SWM': Swimming,
                  'RUN': Running,
                  'WLK': SportsWalking}
    if workout_type not in class_code:
        raise ValueError('Такой тренировки нет.')
    return class_code[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),  # количество гребков, время в часах,
                                        # вес пользователя, длина бассейна,
                                        # сколько раз переплыл бассейн.
        ('RUN', [15000, 1, 75]),  # количество шагов, время тренировки в часах,
                                  # вес пользователя.
        ('WLK', [9000, 1, 75, 180]),  # количество шагов, время трен. в часах,
                                      # вес пользователя, рост пользователя.
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
