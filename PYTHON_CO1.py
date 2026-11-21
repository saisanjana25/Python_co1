from decimal import Decimal, ROUND_HALF_UP
from typing import List, Tuple

class MilkCalculator:
    SEASON_RATES = {
        "REGULAR": {"BASE_RATE": Decimal('30.00'), "FAT_STEP": Decimal('0.40'), "SNF_STEP": Decimal('0.30')},
        "SUMMER":  {"BASE_RATE": Decimal('32.00'), "FAT_STEP": Decimal('0.45'), "SNF_STEP": Decimal('0.30')}
    }
    BASE_FAT = Decimal('3.50')
    BASE_SNF = Decimal('8.50')
    STEP_SIZE = Decimal('0.10')
    BONUS_THRESHOLD = Decimal('500.00')
    BONUS_RATE_PER_LITRE = Decimal('0.50')

    @classmethod
    def rate_per_litre(cls, fat: float, snf: float, season: str = "REGULAR") -> Decimal:
        season_cfg = cls.SEASON_RATES.get(season.upper(), cls.SEASON_RATES["REGULAR"])
        d_fat = Decimal(str(fat))
        d_snf = Decimal(str(snf))
        
        fat_steps = (d_fat - cls.BASE_FAT) / cls.STEP_SIZE
        snf_steps = (d_snf - cls.BASE_SNF) / cls.STEP_SIZE
        
        rate = season_cfg["BASE_RATE"] + (fat_steps * season_cfg["FAT_STEP"]) + (snf_steps * season_cfg["SNF_STEP"])
        return rate.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @classmethod
    def calculate_ten_day_payout(cls, deliveries: List[Tuple[float, float, float]], season: str = "REGULAR") -> dict:
        total_litres = Decimal('0.00')
        base_payout = Decimal('0.00')
        
        for litres, fat, snf in deliveries:
            d_litres = Decimal(str(litres))
            rate = cls.rate_per_litre(fat, snf, season)
            shift_pay = (d_litres * rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            total_litres += d_litres
            base_payout += shift_pay
            
        bonus = Decimal('0.00')
        if total_litres > cls.BONUS_THRESHOLD:
            bonus = (total_litres * cls.BONUS_RATE_PER_LITRE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
        return {
            "total_litres": total_litres,
            "base_payout": base_payout,
            "bonus": bonus,
            "final_payout": base_payout + bonus
        }

if __name__ == "__main__":
    r_summer = MilkCalculator.rate_per_litre(4.25, 8.75, season="SUMMER")
    print(f"Summer Rate (Fat 4.25%, SNF 8.75%): Rs {r_summer}")
    assert r_summer == Decimal('36.13')
    
    sample_deliveries = [(26.0, 3.50, 8.50) for _ in range(20)]
    res = MilkCalculator.calculate_ten_day_payout(sample_deliveries, season="REGULAR")
    print(f"Total: {res['total_litres']} L | Base: Rs {res['base_payout']} | Bonus: Rs {res['bonus']} | Final: Rs {res['final_payout']}")
    assert res['bonus'] == Decimal('260.00')
    print("Task 12 Verification Passed Successfully!")
