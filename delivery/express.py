from datetime import datetime, timedelta
from decimal import Decimal


class ExpressDelivery:
    """Système de livraison express"""

    EXPRESS_FEE = Decimal('1500')  # 1500 FCFA
    STANDARD_FEE = Decimal('500')  # 500 FCFA
    EXPRESS_TIME_HOURS = 2
    STANDARD_TIME_HOURS = 48

    @staticmethod
    def calculate_delivery_fee(distance_km):
        """Calculer les frais de livraison selon la distance"""
        if distance_km <= 5:
            return Decimal('500')
        elif distance_km <= 10:
            return Decimal('1000')
        elif distance_km <= 20:
            return Decimal('1500')
        else:
            return Decimal('2000') + Decimal(str((distance_km - 20) * 50))

    @staticmethod
    def get_estimated_time(distance_km, is_express=False):
        """Temps estimé de livraison"""
        base_time = distance_km / 30  # 30 km/h en moyenne
        if is_express:
            return max(1, int(base_time))  # Minimum 1 heure
        else:
            return max(24, int(base_time * 12))  # Minimum 24 heures

    @staticmethod
    def is_available_in_city(city):
        """Vérifier si la livraison express est disponible dans la ville"""
        express_cities = ['Abidjan', 'Bouaké', 'Yamoussoukro']
        return city in express_cities