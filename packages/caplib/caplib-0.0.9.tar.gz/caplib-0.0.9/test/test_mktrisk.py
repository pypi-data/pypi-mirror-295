# -*- coding: utf-8 -*-
import unittest

from datetime import datetime

from caplib.mktrisk import *

class TestMktRisk(unittest.TestCase):
    def setUp(self):
        cal_cfets = 'CAL_CFETS'
        
        hol_serial_numbers =[44654, 44954]
        sbd_serial_numbers = [44655]
        # Convert list of serial numbers to datetime objects
        holidays = [datetime.fromordinal(sn) for sn in hol_serial_numbers]
        specials = [datetime.fromordinal(sn) for sn in sbd_serial_numbers]
        create_calendar(cal_cfets, holidays, specials)
        
        create_ibor_index('shibor_3m', '3m', 'CNY', ['CAL_CFETS'], 1,
                          'ACT_360', 'MODIFIED_FOLLOWING', 'INVALID_DATE_ROLL_CONVENTION', 'STANDARD_IBOR_INDEX')

        fixed_leg = create_fixed_leg_definition('cny', 'cal_cfets', 'QUARTERLY')
        floating_leg = create_floating_leg_definition('cny', 'shibor_3m', 'cal_cfets', ['cal_cfets'], 'QUARTERLY',
                                                      'QUARTERLY', day_count='ACT_360',
                                                      payment_discount_method='NO_DISCOUNT', rate_calc_method='STANDARD',
                                                      spread=False,
                                                      interest_day_convention='MODIFIED_FOLLOWING', stub_policy='INITIAL',
                                                      broken_period_type='LONG',
                                                      pay_day_offset=0, pay_day_convention='MODIFIED_FOLLOWING',
                                                      fixing_day_convention='MODIFIED_PRECEDING', fixing_mode='IN_ADVANCE',
                                                      fixing_day_offset=-1,
                                                      notional_exchange='INVALID_NOTIONAL_EXCHANGE')
        create_fx_swap_template(inst_name="TestFxSwap",
                                start_convention="INVALID_INSTRUMENT_START_CONVENTION",
                                currency_pair="USDCNY",
                                calendars=["CAL_CFETS"],
                                start_day_convention="MODIFIED_PRECEDING",
                                end_day_convention="MODIFIED_PRECEDING",
                                fixing_offset="180d",
                                fixing_day_convention="MODIFIED_PRECEDING")

        create_fx_spot_template(inst_name="TestFxSpot",
                                currency_pair="USDCNY",
                                spot_day_convention="FOLLOWING",
                                calendars=["CAL_CFETS"],
                                spot_delay="1d")

        self.cny_shibor_3m_swap_template = create_ir_vanilla_swap_template('cny_shibor_3m', 1, fixed_leg, floating_leg,
                                                                           'SPOTSTART')

        self.as_of_date = datetime(2022, 3, 9)
        self.cny_shibor_3m_curve = create_ir_yield_curve(self.as_of_date, 'CNY',
                                                         [datetime(2022, 3, 10), datetime(2025, 3, 10)],
                                                         [0.02, 0.025],
                                                         day_count='ACT_365_FIXED',
                                                         interp_method='LINEAR_INTERP',
                                                         extrap_method='FLAT_EXTRAP',
                                                         compounding_type='CONTINUOUS_COMPOUNDING',
                                                         frequency='ANNUAL',
                                                         jacobian=[0.0],
                                                         curve_name='CNY_SHIBOR_3M',
                                                         pillar_names=['1D', '3Y'])

    def test_simulate_risk_factor(self):
        expected = b'\n\rCNY_SHIBOR_3M\x1a\x16\n\x14\n\x03CNY\x12\rCNY_SHIBOR_3M"\x1c\n\x1a\n\tSHIBOR_3M\x12\rCNY_SHIBOR_3M'
        risk_factor_changes = {'CNY': 'CNY_SHIBOR_3M'}
        change_type = {'SHIBOR_3M': 'CNY_SHIBOR_3M'}
        base = 0.3
        test = simulate_risk_factor(risk_factor_changes, change_type, base)
        self.assertEqual(test.SerializeToString(), expected)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIrAnalytics)
    unittest.TextTestRunner(verbosity=2).run(suite)
