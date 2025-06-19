# Абстрактная Стратегия (Интерфейс)
class DiscountStrategy:
    def calculate_discount(self, order_total: float) -> float:
        """Рассчитать сумму скидки на основе общей суммы заказа.
        Args:
            order_total (float): Общая сумма заказа до скидки.
        Returns:
            float: Сумма скидки.
        """
        raise NotImplementedError("Метод calculate_discount должен быть переопределен в подклассе")

# Конкретные Стратегии
class NoDiscount(DiscountStrategy):
    """Стратегия 'Без скидки'."""
    def calculate_discount(self, order_total: float) -> float:
        return 0.0

class FixedDiscount(DiscountStrategy):
    """Стратегия 'Фиксированная скидка'."""
    def __init__(self, discount_amount: float):
        self.discount_amount = discount_amount

    def calculate_discount(self, order_total: float) -> float:
        return self.discount_amount

class PercentageDiscount(DiscountStrategy):
    """Стратегия 'Процентная скидка'."""
    def __init__(self, discount_percent: float):
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Процент скидки должен быть между 0 и 100")
        self.discount_percent = discount_percent

    def calculate_discount(self, order_total: float) -> float:
        return order_total * (self.discount_percent / 100)

class BonusPointsDiscount(DiscountStrategy):
    """Стратегия 'Скидка бонусными баллами' (1 балл = 1 рубль)."""
    def __init__(self, bonus_points: int):
        if bonus_points < 0:
            raise ValueError("Количество бонусных баллов не может быть отрицательным")
        self.bonus_points = bonus_points

    def calculate_discount(self, order_total: float) -> float:
        # Скидка не может превышать сумму заказа
        return min(order_total, float(self.bonus_points))

# Контекст (Клиент, использующий Стратегию)
class Order:
    def __init__(self, order_total: float, discount_strategy: DiscountStrategy = None):
        self.order_total = order_total
        # По умолчанию - без скидки
        self.discount_strategy = discount_strategy or NoDiscount()

    def set_discount_strategy(self, discount_strategy: DiscountStrategy):
        """Установить стратегию расчета скидки."""
        self.discount_strategy = discount_strategy

    def calculate_final_price(self) -> float:
        """Рассчитать итоговую цену с учетом скидки."""
        discount = self.discount_strategy.calculate_discount(self.order_total)
        final_price = self.order_total - discount
        return max(0.0, final_price)  # Итоговая цена не может быть отрицательной