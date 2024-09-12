import unittest
from datetime import datetime

from caplib.analytics import *
from caplib.fxmarket import *
from caplib.fxanalytics import *
from caplib.market import *


class TestFxAnalytics(unittest.TestCase):

    def setUp(self):
        cal_cfets = 'CAL_CFETS'
        
        hol_serial_numbers =[44654, 44954]
        sbd_serial_numbers = [44655]
        # Convert list of serial numbers to datetime objects
        holidays = [datetime.fromordinal(sn) for sn in hol_serial_numbers]
        specials = [datetime.fromordinal(sn) for sn in sbd_serial_numbers]
        create_calendar(cal_cfets, holidays, specials)
        
        self.as_of_date = datetime(2022, 3, 9)

        vol_surf_definition = create_volatility_surface_definition(vol_smile_type='STRIKE_VOL_SMILE',
                                                                   smile_method='LINEAR_SMILE_METHOD',
                                                                   smile_extrap_method='FLAT_EXTRAP',
                                                                   time_interp_method='LINEAR_IN_VARIANCE',
                                                                   time_extrap_method='FLAT_IN_VOLATILITY',
                                                                   day_count_convention='ACT_365_FIXED',
                                                                   vol_type='LOG_NORMAL_VOL_TYPE',
                                                                   wing_strike_type='DELTA',
                                                                   lower=0.05,
                                                                   upper=0.4)

        #curve = create_yield_curve(as_of_date=self.as_of_date,
        #                           term_dates=[datetime(2022, 3, 10), datetime(2025, 3, 10)],
        #                           zero_rates=[0.02, 0.025])


        vol_smile1 = create_volatility_smile(vol_smile_type='STRIKE_VOL_SMILE',
                                             reference_date=datetime(2022, 3, 9),
                                             strikes=[1.0, 2.0],
                                             vols = [0.1, 0.1],
                                             smile_method='LINEAR_SMILE_METHOD',
                                             extrap_method='FLAT_EXTRAP',
                                             time_interp_method='LINEAR_IN_VARIANCE',
                                             time_extrap_method='FLAT_IN_VOLATILITY',
                                             term=0.02,
                                             model_params=[],
                                             auxilary_params=[],
                                             lower=0.05,
                                             upper=0.4)
        vol_smile2 = create_volatility_smile(vol_smile_type='STRIKE_VOL_SMILE',
                                             reference_date=datetime(2022, 3, 9),
                                             strikes=[1.0, 2.0],
                                             vols = [0.1, 0.1],
                                             smile_method='LINEAR_SMILE_METHOD',
                                             extrap_method='FLAT_EXTRAP',
                                             time_interp_method='LINEAR_IN_VARIANCE',
                                             time_extrap_method='FLAT_IN_VOLATILITY',
                                             term=0.04,
                                             model_params=[],
                                             auxilary_params=[],
                                             lower=0.05,
                                             upper=0.4)
        self.vol_surf = create_volatility_surface(definition=vol_surf_definition,
                                                  reference_date=datetime(2022, 3, 9),
                                                  vol_smiles=[vol_smile1, vol_smile2],
                                                  term_dates=[datetime(2022, 3, 10), datetime(2025, 3, 10)])

        self.domestic_discount_curve_cnh = create_ir_yield_curve(self.as_of_date,
                                                                 'CNH',
                                                                 [datetime(2022, 3, 10), datetime(2025, 3, 10)],
                                                                 [0.02, 0.025])
        self.domestic_discount_curve_cny = create_ir_yield_curve(self.as_of_date,
                                                                 'CNY',
                                                                 [datetime(2022, 3, 10), datetime(2025, 3, 10)],
                                                                 [0.02, 0.025])
        self.foreign_discount_curve_usd = create_ir_yield_curve(self.as_of_date,
                                                                'USD',
                                                                [datetime(2022, 3, 10), datetime(2025, 3, 10)],
                                                                [0.02, 0.025])

        foreign_exchange_rate1 = create_foreign_exchange_rate(6.6916, "CNH", "USD")
        self.fx_spot_rate1 = create_fx_spot_rate(foreign_exchange_rate1, datetime(2022, 3, 9),
                                                 datetime(2022, 3, 9))

        foreign_exchange_rate2 = create_foreign_exchange_rate(6.7, "CNY", "USD")
        self.fx_spot_rate2 = create_fx_spot_rate(foreign_exchange_rate2, datetime(2022, 3, 9),
                                                 datetime(2022, 3, 9))

        # USD/CNH
        self.fx_mkt_data_set1 = create_fx_mkt_data_set(self.as_of_date,
                                                       self.domestic_discount_curve_cnh,
                                                       self.foreign_discount_curve_usd,
                                                       self.fx_spot_rate1,
                                                       self.vol_surf)

        # USD/CNY
        self.fx_mkt_data_set2 = create_fx_mkt_data_set(self.as_of_date,
                                                       self.domestic_discount_curve_cny,
                                                       self.foreign_discount_curve_usd,
                                                       self.fx_spot_rate2,
                                                       self.vol_surf)

        self.pricing_settings1 = create_pricing_settings('CNH',
                                                         False,
                                                         create_model_settings('BLACK_SCHOLES_MERTON'),
                                                         'ANALYTICAL',
                                                         create_pde_settings(),
                                                         create_monte_carlo_settings())
        self.pricing_settings2 = create_pricing_settings('CNY',
                                                         False,
                                                         create_model_settings('BLACK_SCHOLES_MERTON'),
                                                         'ANALYTICAL',
                                                         create_pde_settings(),
                                                         create_monte_carlo_settings())

        ir_curve_settings = create_ir_curve_risk_settings()
        price_settings = create_price_risk_settings()
        vol_settings = create_vol_risk_settings()
        price_vol_settings = create_price_vol_risk_settings()
        theta_settings = create_theta_risk_settings()
        self.risk_settings = create_fx_risk_settings(ir_curve_settings,
                                                     price_settings,
                                                     vol_settings,
                                                     price_vol_settings,
                                                     theta_settings)

    def test_create_fx_risk_settings(self):
        expected = b'\n!\x08\x01\x18\x01!-C\x1c\xeb\xe26\x1a?){\x14\xaeG\xe1zt?8\x01A-C\x1c\xeb\xe26\x1a?\x12\x1d\x08\x01!-C\x1c\xeb\xe26\x1a?){\x14\xaeG\xe1zt?A-C\x1c\xeb\xe26\x1a?\x1a\x12!-C\x1c\xeb\xe26\x1a?A-C\x1c\xeb\xe26\x1a?"$\x11-C\x1c\xeb\xe26\x1a?\x19-C\x1c\xeb\xe26\x1a?!-C\x1c\xeb\xe26\x1a?A-C\x1c\xeb\xe26\x1a?*\r\x08\x01\x10\x01\x19\x1ag\x016\x9fqf?'
        ir_curve_settings = create_ir_curve_risk_settings(delta=True, curvature=True, granularity='TERM_BUCKET_RISK')
        price_settings = create_price_risk_settings(delta=True)
        vol_settings = create_vol_risk_settings()
        price_vol_settings = create_price_vol_risk_settings()
        theta_settings = create_theta_risk_settings(theta=True)
        test = create_fx_risk_settings(ir_curve_settings,
                                       price_settings,
                                       vol_settings,
                                       price_vol_settings,
                                       theta_settings)
        self.assertEqual(test.SerializeToString(), expected)

    def test_create_fx_mkt_data_set(self):
        expected = b'\n\x07\x08\xe6\x0f\x10\x03\x18\t\x12X\x12;\n7\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x00*\x12\n\x10{\x14\xaeG\xe1z\x94?\x9a\x99\x99\x99\x99\x99\x99?0\x018\x01\x10\x01\x1a\x03CNY \x01:\x12\x12\x10\x08\x01\x10\x01\x1a\x08\x00\x00\x00\x00\x00\x00\x00\x00 \x01\x1aX\x12;\n7\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x00*\x12\n\x10{\x14\xaeG\xe1z\x94?\x9a\x99\x99\x99\x99\x99\x99?0\x018\x01\x10\x01\x1a\x03USD \x01:\x12\x12\x10\x08\x01\x10\x01\x1a\x08\x00\x00\x00\x00\x00\x00\x00\x00 \x01"\'\n\x13\t\xcd\xcc\xcc\xcc\xcc\xcc\x1a@\x12\x03CNY\x1a\x03USD\x12\x07\x08\xe6\x0f\x10\x03\x18\t\x1a\x07\x08\xe6\x0f\x10\x03\x18\t*\xed\x01\n \x08\x01\x10\x01\x18\x01 \x01(\x010\x028\x01I\x9a\x99\x99\x99\x99\x99\xa9?Q\x9a\x99\x99\x99\x99\x99\xd9?\x12\x07\x08\xe6\x0f\x10\x03\x18\t\x1aV\x08\x01\x12\x07\x08\xe6\x0f\x10\x03\x18\t\x19\x9a\x99\x99\x99\x99\x99\xa9?!\x9a\x99\x99\x99\x99\x99\xd9?*\x12\n\x10\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x00@0\x019{\x14\xaeG\xe1z\x94?B\x12\n\x10\x9a\x99\x99\x99\x99\x99\xb9?\x9a\x99\x99\x99\x99\x99\xb9?J\x00R\x00X\x01\x1aV\x08\x01\x12\x07\x08\xe6\x0f\x10\x03\x18\t\x19\x9a\x99\x99\x99\x99\x99\xa9?!\x9a\x99\x99\x99\x99\x99\xd9?*\x12\n\x10\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x00@0\x019{\x14\xaeG\xe1z\xa4?B\x12\n\x10\x9a\x99\x99\x99\x99\x99\xb9?\x9a\x99\x99\x99\x99\x99\xb9?J\x00R\x00X\x01"\x07\x08\xe6\x0f\x10\x03\x18\n"\x07\x08\xe9\x0f\x10\x03\x18\n'
        
        test = create_fx_mkt_data_set(self.as_of_date,
                                      self.domestic_discount_curve_cny,
                                      self.foreign_discount_curve_usd,
                                      self.fx_spot_rate2,
                                      self.vol_surf)
        #print('test_create_fx_mkt_data_set', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)

    def test_fx_ndf_pricer(self):
        expected = b'\x1a\x00"\x00*\x03CNH2\x00'
        fx_ndf_template = create_fx_ndf_template(inst_name="TestFxNdf",
                                                 fixing_offset="180d",
                                                 currency_pair="USDCNH",
                                                 delivery_day_convention="MODIFIED_PRECEDING",
                                                 fixing_day_convention="MODIFIED_PRECEDING",
                                                 calendars=["CAL_CFETS"],
                                                 settlement_currency="USD")

        fx_ndf = create_fx_non_deliverable_forwad(buy_currency="USD",
                                                  buy_amount=10000,
                                                  sell_currency="CNH",
                                                  sell_amount=66916,
                                                  delivery_date=datetime(2022, 12, 21),
                                                  expiry_date=datetime(2022, 12, 21),
                                                  settlement_currency="USD",
                                                  fx_ndf_template=fx_ndf_template)

        test = fx_ndf_pricer(pricing_date=datetime(2022, 3, 9),
                             instrument=fx_ndf,
                             mkt_data=self.fx_mkt_data_set1,
                             pricing_settings=self.pricing_settings1,
                             risk_settings=self.risk_settings)
        self.assertEqual(test.SerializeToString(), expected)

    def test_fx_swap_pricer(self):
        expected = b'\t\x00\x00\x00\x00\x00\x00\xb0=\x1a\x00"\x00*\x03CNY2\x00'
        fx_swap_template = create_fx_swap_template(inst_name="TestFxSwap",
                                                   start_convention="INVALID_INSTRUMENT_START_CONVENTION",
                                                   currency_pair="USDCNY",
                                                   calendars=["CAL_CFETS"],
                                                   start_day_convention="MODIFIED_PRECEDING",
                                                   end_day_convention="MODIFIED_PRECEDING",
                                                   fixing_offset="180d",
                                                   fixing_day_convention="MODIFIED_PRECEDING")

        fx_swap = create_fx_swap(near_buy_currency="USD",
                                 near_buy_amount=10000,
                                 near_sell_currency="CNY",
                                 near_sell_amount=67000,
                                 near_delivery_date=datetime(2022, 12, 21),
                                 near_expiry_date=None,
                                 far_buy_currency="USD",
                                 far_buy_amount=10000,
                                 far_sell_currency="CNY",
                                 far_sell_amount=67000,
                                 far_delivery_date=datetime(2023, 12, 21),
                                 far_expiry_date=None,
                                 fx_swap_template=fx_swap_template)

        test = fx_swap_pricer(pricing_date=datetime(2022, 3, 9),
                              instrument=fx_swap,
                              mkt_data=self.fx_mkt_data_set2,
                              pricing_settings=self.pricing_settings2,
                              risk_settings=self.risk_settings)
        self.assertEqual(test.SerializeToString(), expected)

    def test_fx_forward_pricer(self):
        expected = b'\x1a\x00"\x00*\x03CNY2\x00'
        fx_fwd_template = create_fx_forward_template(inst_name="TestFxForward",
                                                     fixing_offset="180d",
                                                     currency_pair="USDCNY",
                                                     delivery_day_convention="MODIFIED_PRECEDING",
                                                     fixing_day_convention="MODIFIED_PRECEDING",
                                                     calendars=["CAL_CFETS"])

        fx_forward = create_fx_forward(buy_currency="USD",
                                       buy_amount=10000,
                                       sell_currency="CNY",
                                       sell_amount=67000,
                                       delivery=datetime(2022, 12, 21),
                                       fx_fwd_template=fx_fwd_template,
                                       expiry=None)

        test = fx_forward_pricer(pricing_date=datetime(2022, 3, 9),
                                 instrument=fx_forward,
                                 mkt_data=self.fx_mkt_data_set2,
                                 pricing_settings=self.pricing_settings2,
                                 risk_settings=self.risk_settings)
        self.assertEqual(test.SerializeToString(), expected)


if __name__ == "__main__":
    unittest.main()
