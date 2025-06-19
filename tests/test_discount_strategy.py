
import pytest
from src.discount_strategy import (Order, NoDiscount, FixedDiscount,
                                  PercentageDiscount, BonusPointsDiscount)

# Тесты для конкретных стратегий
def test_no_discount():
    strategy = NoDiscount()
    assert strategy.calculate_discount(1000) == 0.0

def test_fixed_discount():
    strategy = FixedDiscount(150.0)
    assert strategy.calculate_discount(1000) == 150.0
    assert strategy.calculate_discount(50) == 150.0  # Скидка больше суммы заказа

def test_percentage_discount_valid():
    strategy = PercentageDiscount(10.0)  # 10%
    assert strategy.calculate_discount(1000) == 100.0
    assert strategy.calculate_discount(500) == 50.0

def test_percentage_discount_invalid():
    with pytest.raises(ValueError):  # Ожидаем ошибку
        PercentageDiscount(110.0)
    with pytest.raises(ValueError):
        PercentageDiscount(-10.0)

def test_bonus_points_discount():
    strategy = BonusPointsDiscount(200)  # 200 баллов = 200 руб
    assert strategy.calculate_discount(1000) == 200.0
    assert strategy.calculate_discount(150) == 150.0  # Скидка ограничена суммой заказа
    assert strategy.calculate_discount(0) == 0.0

def test_bonus_points_discount_invalid():
    with pytest.raises(ValueError):
        BonusPointsDiscount(-50)

# Тесты для класса Order (Контекста)
def test_order_no_strategy():
    order = Order(1000.0)  # По умолчанию NoDiscount
    assert order.calculate_final_price() == 1000.0

def test_order_set_strategy():
    order = Order(1000.0)
    fixed_discount = FixedDiscount(150.0)
    order.set_discount_strategy(fixed_discount)
    assert order.calculate_final_price() == 850.0

def test_order_final_price_non_negative():
    order = Order(50.0, FixedDiscount(150.0))  # Скидка больше суммы заказа
    assert order.calculate_final_price() == 0.0  # Цена не может быть < 0

# Тест, который ПАДАЕТ (намеренно для демонстрации Actions)
def test_order_percentage_discount():
    order = Order(1000.0, PercentageDiscount(20.0))  # 20%
    assert order.calculate_final_price() == 800.0  # Ожидаем 800.0, тест упадет!