# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 13:00:34 2022

@author: dingq
"""

from caplibproto.dqproto import *

from caplib.staticdata import create_static_data
from caplib.datetime import *

def to_time_series_mode(src):
    '''
    Convert a string to TimeSeries.Mode.
    
    Parameters
    ----------
    src : str
        a string of frequency, i.e. 'TS_FORWARD_MODE'.
    
    Returns
    -------
    None.

    '''
    if src is None:
        return TS_FORWARD_MODE
    if src in ['', 'nan']:
        return TS_FORWARD_MODE
    else:
        return TimeSeries.Mode.DESCRIPTOR.values_by_name[src.upper()].number


def to_exercise_type(src):
    '''
    将字符串转换为 ExerciseType.

    Parameters
    ----------
    src : str

    Returns
    -------
    ExerciseType

    '''
    if src is None:
        return EUROPEAN
    if src in ['', 'nan']:
        return EUROPEAN
    else:
        return ExerciseType.DESCRIPTOR.values_by_name[src.upper()].number


def to_payoff_type(src):
    '''
    将字符串转换为 PayoffType.

    Parameters
    ----------
    src : str

    Returns
    -------
    PayoffType

    '''
    if src is None:
        return CALL
    if src in ['', 'nan']:
        return CALL
    else:
        return PayoffType.DESCRIPTOR.values_by_name[src.upper()].number



# Time Series
def create_time_series(dates,
                       values,
                       mode='TS_FORWARD_MODE',
                       name=''):
    '''
    Create a time series.
    
    Parameters
    ----------
    dates : list
        A list of datetime.The dates are type of Date.
    values : list
        A list of floating numbers.
    mode : TimeSeries.Mode, optional
        Mode indicates the time series is in the date ascending (forward) or descending (backward) order. The default is 'TS_FORWARD_MODE'.
    name : str, optional
        Name of time series given by user. The default is ''.
    
    Returns
    -------
    TimeSeries
        A time series object.
    
    '''
    p_dates = [create_date(d) for d in dates]
    p_values = dqCreateProtoMatrix(len(values), 1, values, Matrix.StorageOrder.ColMajor)
    return dqCreateProtoTimeSeries(p_dates, p_values, to_time_series_mode(mode), name.upper())


# Currency Pair
def to_ccy_pair(src):
    '''
    Create a currency pair. 
    
    Parameters
    ----------
    src : str
        a string of 6 chars, i.e. 'USDCNY', 'usdcny'.
    
    Returns
    -------
    CurrencyPair
        Object of CurrencyPair.
    
    '''
    left = src[0:3]
    right = src[3:6]
    return dqCreateProtoCurrencyPair(dqCreateProtoCurrency(left.upper()),
                                     dqCreateProtoCurrency(right.upper()))


#NotionalExchange
def to_notional_exchange(src):
    if src is None:
        return INVALID_NOTIONAL_EXCHANGE
    
    if src in ['', 'nan']:
        return INVALID_NOTIONAL_EXCHANGE
    else:
        return NotionalExchange.DESCRIPTOR.values_by_name[src.upper()].number
    
#InstrumentStartConvention
def to_instrument_start_convention(src):
    if src is None:
        return SPOTSTART
    
    if src in ['', 'nan']:
        return SPOTSTART
    else:
        return InstrumentStartConvention.DESCRIPTOR.values_by_name[src.upper()].number

#PayReceiveFlag
def to_pay_receive_flag(src):
    if src is None:
        return PAY
    
    if src in ['', 'nan']:
        return PAY
    else:
        return PayReceiveFlag.DESCRIPTOR.values_by_name[src.upper()].number

#NotionalType
def to_notional_type(src):
    if src is None:
        return CONST_NOTIONAL
    
    if src in ['', 'nan']:
        return CONST_NOTIONAL
    else:
        return NotionalType.DESCRIPTOR.values_by_name[src.upper()].number

#StrikeType
def to_strike_type(src):
    if src is None:
        return FIXED_STRIKE
    
    if src in ['', 'nan']:
        return FIXED_STRIKE
    else:
        return StrikeType.DESCRIPTOR.values_by_name[src.upper()].number

#AveragingMethod
def to_averaging_method(src):
    if src is None:
        return ARITHMETIC_AVERAGE_METHOD
    
    if src in ['', 'nan']:
        return ARITHMETIC_AVERAGE_METHOD
    else:
        return AveragingMethod.DESCRIPTOR.values_by_name[src.upper()].number

#EventObservationType
def to_event_observation_type(src):
    if src is None:
        return CONTINUOUS_OBSERVATION_TYPE
    
    if src in ['', 'nan']:
        return CONTINUOUS_OBSERVATION_TYPE
    else:
        return EventObservationType.DESCRIPTOR.values_by_name[src.upper()].number

def create_fixing_schedule(fixing_dates: list, 
                           fixing_values: list,
                           fixing_weights: list):
    if len(fixing_dates) != len(fixing_values) or len(fixing_dates) != len(fixing_weights):
        raise ValueError("fixing_dates, fixing_values, and fixing_weights must have the same size.")
    
    rows = []
    for i in range(len(fixing_dates)):
        rows.append(dqCreateProtoFixingSchedule_Row(create_date(fixing_dates[i]), fixing_values[i], fixing_weights[i]))    
    return dqCreateProtoFixingSchedule(rows)

def create_foreign_exchange_rate(value,
                                 base_currency,
                                 target_currency):
    """
    创建一个外汇利率对象.

    Parameters
    ----------
    value: float
    base_currency: str
    target_currency: str

    Returns
    -------
    ForeignExchangeRate

    """
    return dqCreateProtoForeignExchangeRate(value,
                                            base_currency,
                                            target_currency)

def create_fx_spot_rate(fx_rate,
                        ref_date,
                        spot_date):
    """
    创建一个外汇即期利率对象.

    Parameters
    ----------
    fx_rate: ForeignExchangeRate
    ref_date: Date
    spot_date: Date

    Returns
    -------
    FxSpotRate

    """
    return dqCreateProtoFxSpotRate(fx_rate,
                                   create_date(ref_date),
                                   create_date(spot_date))

def create_fx_spot_template(inst_name,
                            currency_pair,
                            spot_day_convention,
                            calendars,
                            spot_delay):
    """
    Create a fx spot template object.

    :param inst_name: str
    :param currency_pair: str
    :param spot_day_convention: str
    :param calendars: list
    :param spot_delay: str
    :return: FxSpotTemplate
    """
    p_type = FX_SPOT
    p_currency_pair = to_ccy_pair(currency_pair)
    p_spot_day_convention = to_business_day_convention(spot_day_convention)
    p_spot_delay = to_period(spot_delay)
    pb_data = dqCreateProtoFxSpotTemplate(p_type,
                                          inst_name,
                                          p_currency_pair,
                                          p_spot_day_convention,
                                          calendars,
                                          p_spot_delay)
    pb_data_list = dqCreateProtoFxSpotTemplateList([pb_data])
    create_static_data('SDT_FX_SPOT', pb_data_list.SerializeToString())
    return pb_data


#CreateDigitalOption
def create_digital_option(payoff_type,
                              expiry,
                              delivery,
                              strike,
                              cash,
                              asset,
                              nominal,
                              payoff_ccy,
                              underlying_type,
                              underlying_ccy,
                              underlying):
   return dqCreateProtoDigitalOption(to_payoff_type(payoff_type),
                                                create_date(expiry),
                                                create_date(delivery),
                                                strike,
                                                cash,
                                                asset,
                                                nominal,
                                                underlying,
                                                underlying_ccy,
                                                payoff_ccy,
                                                underlying_type)

#CreateEuropeanOption
def create_european_option(payoff_type,
                          expiry,
                          delivery,
                          strike,
                          nominal,
                          payoff_ccy,
                          underlying_type,
                          underlying_ccy,
                          underlying):
    return dqCreateProtoEuropeanOption(to_payoff_type(payoff_type),
                                       strike,
                                                create_date(delivery),
                                                create_date(expiry),
                                                nominal,
                                                underlying,
                                                underlying_ccy,
                                                payoff_ccy,
                                                underlying_type)

#CreateAmericanOption
def create_american_option(payoff_type,
                          expiry,
                          strike,
                          settlement_days,
                          nominal,
                          payoff_ccy,
                          underlying_type,
                          underlying_ccy,
                          underlying):
    return dqCreateProtoAmericanOption(to_payoff_type(payoff_type),
                                       strike,
                                       create_date(expiry),
                                       create_date(expiry),
                                       settlement_days,
                                                nominal,
                                                underlying,
                                                underlying_ccy,
                                                payoff_ccy,
                                                underlying_type)
        
#CreateAsianOption
def create_asian_option(payoff_type,
                        expiry,
                        delivery,
                        strike_type,
                        strike,
                        avg_method,
                        obs_type,
                        fixing_schedule,
                        nominal,
                        payoff_ccy,
                        underlying_type,
                        underlying_ccy,
                        underlying):
    return dqCreateProtoAsianOption(to_payoff_type(payoff_type),
                                    to_averaging_method(avg_method),
                                    to_event_observation_type(obs_type),
                                    create_date(expiry),
                                    create_date(delivery),
                                    create_fixing_schedule(fixing_schedule),
                                    to_strike_type(strike_type),
                                    strike,
                                                nominal,
                                                underlying,
                                                underlying_ccy,
                                                payoff_ccy,
                                                underlying_type)

#CreateOneTouchOption
def create_one_touch_option(expiry,
                            delivery,
                            barrier_type,
                            barrier_value,
                            barrier_obs_type,
                            obs_schedule,
                            payment_type,
                            cash,
                            asset,
                            settlement_days,
                            nominal,
                            payoff_ccy,
                            underlying_type,
                            underlying_ccy,
                            underlying,
                            tag,
                            save,
                            location):
    try:
        one_touch_option = OneTouchOption()
        one_touch_option.expiry_date = create_date(expiry)
        one_touch_option.delivery_date = create_date(delivery)
        one_touch_option.asset = asset
        one_touch_option.cash = cash
        one_touch_option.barrier = Barrier()
        one_touch_option.barrier.barrier_type = to_barrier_type(barrier_type)
        one_touch_option.barrier.value = barrier_value
        one_touch_option.payment_type = to_payment_type(payment_type)
        one_touch_option.nominal = nominal
        one_touch_option.underlying = underlying
        one_touch_option.payoff_currency = payoff_ccy
        one_touch_option.underlying_currency = underlying_ccy
        one_touch_option.underlying_type = to_underlying_type(underlying_type)
        one_touch_option.obs_type = to_event_observation_type(barrier_obs_type)
        if one_touch_option.obs_type != EventObservationType.CONTINUOUS_OBSERVATION_TYPE:
            one_touch_option.fixing_schedule = create_fixing_schedule(obs_schedule)
        one_touch_option.settlement_days = settlement_days
        return one_touch_option
    except Exception as e:
        log_write_log_file(e.toString())
        return e.toString()

#CreateDoubleTouchOption
def create_double_touch_option(expiry,
                              delivery,
                              lower_barrier_type,
                              lower_barrier_value,
                              upper_barrier_type,
                              upper_barrier_value,
                              barrier_obs_type,
                              obs_schedule,
                              payment_type,
                              cash,
                              asset,
                              settlement_days,
                              nominal,
                              payoff_ccy,
                              underlying_type,
                              underlying_ccy,
                              underlying,
                              tag,
                              save,
                              location):
    try:
        double_touch_option = DoubleTouchOption()
        double_touch_option.expiry_date = create_date(expiry)
        double_touch_option.delivery_date = create_date(delivery)
        double_touch_option.asset = asset
        double_touch_option.cash = cash
        double_touch_option.lower_barrier = Barrier()
        double_touch_option.upper_barrier = Barrier()
        double_touch_option.lower_barrier.barrier_type = to_barrier_type(lower_barrier_type)
        double_touch_option.lower_barrier.value = lower_barrier_value
        double_touch_option.upper_barrier.barrier_type = to_barrier_type(upper_barrier_type)
        double_touch_option.upper_barrier.value = upper_barrier_value
        double_touch_option.payment_type = to_payment_type(payment_type)
        double_touch_option.nominal = nominal
        double_touch_option.underlying = underlying
        double_touch_option.payoff_currency = payoff_ccy
        double_touch_option.underlying_currency = underlying_ccy
        double_touch_option.underlying_type = to_underlying_type(underlying_type)
        double_touch_option.obs_type = to_event_observation_type(barrier_obs_type)
        if double_touch_option.obs_type != EventObservationType.CONTINUOUS_OBSERVATION_TYPE:
            double_touch_option.fixing_schedule = create_fixing_schedule(obs_schedule)
        double_touch_option.settlement_days = settlement_days
        
        return store_object_to_cache("", tag, "DoubleTouchOption", double_touch_option)
    except Exception as e:
        log_write_log_file(e.toString())
        return e.toString()
    
#region DqCreateSingleBarrierOption
def create_single_barrier_option(payoff_type,
                                strike,
                                expiry,
                                delivery,
                                barrier_type,
                                barrier_value,
                                barrier_obs_type,
                                obs_schedule,
                                payment_type,
                                cash_rebate,
                                asset_rebate,
                                settlement_days,
                                nominal,
                                payoff_ccy,
                                underlying_type,
                                underlying_ccy,
                                underlying,
                                tag,
                                save,
                                location):
    try:
        single_barrier_option = SingleBarrierOption()
        single_barrier_option.payoff_type = to_payoff_type(payoff_type)
        single_barrier_option.strike = strike
        single_barrier_option.expiry_date = create_date(expiry)
        single_barrier_option.delivery_date = create_date(delivery)
        single_barrier_option.barrier = Barrier()
        single_barrier_option.barrier.barrier_type = to_barrier_type(barrier_type)
        single_barrier_option.barrier.value = barrier_value
        single_barrier_option.payment_type = to_payment_type(payment_type)
        single_barrier_option.cash_rebate = cash_rebate
        single_barrier_option.asset_rebate = asset_rebate
        single_barrier_option.nominal = nominal
        single_barrier_option.underlying = underlying
        single_barrier_option.payoff_currency = payoff_ccy
        single_barrier_option.underlying_currency = underlying_ccy
        single_barrier_option.underlying_type = to_underlying_type(underlying_type)
        single_barrier_option.obs_type = to_event_observation_type(barrier_obs_type)
        if single_barrier_option.obs_type != EventObservationType.CONTINUOUS_OBSERVATION_TYPE:
            single_barrier_option.fixing_schedule = create_fixing_schedule(obs_schedule)
        single_barrier_option.settlement_days = settlement_days
        
        return store_object_to_cache("", tag, "SingleBarrierOption", single_barrier_option)
    except Exception as e:
        log_write_log_file(e.toString())
        return e.toString()
#region DqCreateDoubleBarrierOption
def create_double_barrier_option(payoff_type,
                                strike,
                                expiry,
                                delivery,
                                lower_barrier,
                                upper_barrier,
                                barrier_obs_type,
                                obs_schedule,
                                payment_type,
                                lower_rebate,
                                upper_rebate,
                                settlement_days,
                                nominal,
                                payoff_ccy,
                                underlying_type,
                                underlying_ccy,
                                underlying,
                                tag,
                                save,
                                location):
    try:
        double_barrier_option = DoubleBarrierOption()
        double_barrier_option.payoff_type = to_payoff_type(payoff_type)
        double_barrier_option.strike = strike
        double_barrier_option.expiry_date = create_date(expiry)
        double_barrier_option.delivery_date = create_date(delivery)
        double_barrier_option.lower_barrier = Barrier()
        double_barrier_option.upper_barrier = Barrier()
        double_barrier_option.lower_barrier.barrier_type = to_barrier_type(lower_barrier[0])
        double_barrier_option.lower_barrier.value = lower_barrier[1]
        double_barrier_option.upper_barrier.barrier_type = to_barrier_type(upper_barrier[0])
        double_barrier_option.upper_barrier.value = upper_barrier[1]
        double_barrier_option.payment_type = to_payment_type(payment_type) if payment_type != "" else PaymentType.PAY_AT_HIT
        double_barrier_option.lower_cash_rebate = lower_rebate[0]
        double_barrier_option.lower_asset_rebate = lower_rebate[1]
        double_barrier_option.upper_cash_rebate = upper_rebate[0]
        double_barrier_option.upper_asset_rebate = upper_rebate[1]
        double_barrier_option.nominal = nominal
        double_barrier_option.underlying = underlying
        double_barrier_option.payoff_currency = payoff_ccy
        double_barrier_option.underlying_currency = underlying_ccy
        double_barrier_option.underlying_type = to_underlying_type(underlying_type) if underlying_type != "" else InstrumentType.SPOT
        double_barrier_option.obs_type = to_event_observation_type(barrier_obs_type) if barrier_obs_type != "" else EventObservationType.CONTINUOUS_OBSERVATION_TYPE
        if double_barrier_option.obs_type != EventObservationType.CONTINUOUS_OBSERVATION_TYPE:
            double_barrier_option.fixing_schedule = create_fixing_schedule(obs_schedule)
        double_barrier_option.settlement_days = settlement_days
        if save:
            file_name = "DoubleBarrierOption_".lower() + "_" + tag
            save_as_bin_file(double_barrier_option.SerializeToString(), file_name, location)
            save_as_txt_file(json_format.MessageToJson(double_barrier_option), file_name, location)
        return store_object_to_cache("", tag, "DoubleBarrierOption", double_barrier_option)
    except Exception as e:
        log_write_log_file(e.toString())
        return e.toString()
#region DqCreateSingleSharkFinOption
def create_single_shark_fin_option(
        payoff_type,
        strike,
        expiry,
        delivery,
        gearing,
        performance_type,
        barrier_type,
        barrier_value,
        barrier_obs_type,
        obs_schedule,
        payment_type,
        cash_rebate,
        asset_rebate,
        settlement_days,
        nominal,
        payoff_ccy,
        underlying_type,
        underlying_ccy,
        underlying,
        tag,
        save,
        location):
    try:
        single_shark_fin_option = SingleSharkFinOption()
        single_shark_fin_option.payoff_type = to_payoff_type(payoff_type)
        single_shark_fin_option.strike = strike
        single_shark_fin_option.expiry_date = create_date(expiry)
        single_shark_fin_option.delivery_date = create_date(delivery)
        single_shark_fin_option.gearing = gearing
        
        single_shark_fin_option.performance_type = to_performance_type(performance_type) if performance_type != "" else PerformanceType.RelativePerformType
        single_shark_fin_option.barrier = Barrier()
        single_shark_fin_option.barrier.barrier_type = to_barrier_type(barrier_type)
        single_shark_fin_option.barrier.value = barrier_value
        single_shark_fin_option.cash_rebate = cash_rebate
        single_shark_fin_option.asset_rebate = asset_rebate
        single_shark_fin_option.payment_type = to_payment_type(payment_type) if payment_type != "" else PaymentType.PayAtHit
        single_shark_fin_option.nominal = nominal
        single_shark_fin_option.underlying = underlying
        single_shark_fin_option.payoff_currency = payoff_ccy
        single_shark_fin_option.underlying_currency = underlying_ccy
        single_shark_fin_option.underlying_type = to_underlying_type(underlying_type) if underlying_type != "" else InstrumentType.Spot
        single_shark_fin_option.barrier_obs_type = to_event_observation_type(barrier_obs_type) if barrier_obs_type != "" else EventObservationType.ContinuousObservationType
        if single_shark_fin_option.barrier_obs_type != EventObservationType.ContinuousObservationType:
            single_shark_fin_option.fixing_schedule = create_fixing_schedule(obs_schedule)
        single_shark_fin_option.settlement_days = settlement_days
        if save:
            file_name = "SingleSharkFinOption_" + tag
            save_as_bin_file(single_shark_fin_option.SerializeToString(), file_name, location)
            save_as_txt_file(json_format.MessageToJson(single_shark_fin_option), file_name, location)
        return store_object_to_cache("", tag, "SingleSharkFinOption", single_shark_fin_option)
    except Exception as e:
        log_write_log_file(e.toString())
        return e.toString()
    
#region DqCreateDoubleSharkFinOption
def create_double_shark_fin_option(
        strikes,
        expiry,
        delivery,
        participations,
        performance_type,
        barriers,
        barrier_obs_type,
        obs_schedule,
        payment_type,
        lower_rebate,
        upper_rebate,
        settlement_days,
        nominal,
        payoff_ccy,
        underlying_type,
        underlying_ccy,
        underlying,
        tag,
        save,
        location):
    try:
        double_shark_fin_option = DoubleSharkFinOption()
        double_shark_fin_option.lower_strike = strikes[0]
        double_shark_fin_option.upper_strike = strikes[1]
        double_shark_fin_option.expiry_date = create_date(expiry)
        double_shark_fin_option.delivery_date = create_date(delivery)
        double_shark_fin_option.lower_participation = participations[0]
        double_shark_fin_option.upper_participation = participations[1]
        double_shark_fin_option.performance_type = to_performance_type(performance_type) if performance_type != "" else PerformanceType.RelativePerformType
        double_shark_fin_option.lower_barrier = barriers[0]
        double_shark_fin_option.upper_barrier = barriers[1]
        double_shark_fin_option.lower_cash_rebate = lower_rebate[0]
        double_shark_fin_option.lower_asset_rebate = lower_rebate[1]
        double_shark_fin_option.upper_cash_rebate = upper_rebate[0]
        double_shark_fin_option.upper_asset_rebate = upper_rebate[1]
        double_shark_fin_option.payment_type = to_payment_type(payment_type) if payment_type != "" else PaymentType.PayAtHit
        double_shark_fin_option.nominal = nominal
        double_shark_fin_option.underlying = underlying
        double_shark_fin_option.payoff_currency = payoff_ccy
        double_shark_fin_option.underlying_currency = underlying_ccy
        double_shark_fin_option.underlying_type = to_underlying_type(underlying_type) if underlying_type != "" else InstrumentType.Spot
        double_shark_fin_option.barrier_obs_type = to_event_observation_type(barrier_obs_type) if barrier_obs_type != "" else EventObservationType.ContinuousObservationType
        if double_shark_fin_option.barrier_obs_type != EventObservationType.ContinuousObservationType:
            double_shark_fin_option.fixing_schedule = create_fixing_schedule(obs_schedule)
        double_shark_fin_option.settlement_days = settlement_days
        if save:
            file_name = "DoubleSharkFinOption_" + tag
            save_as_bin_file(double_shark_fin_option.SerializeToString(), file_name, location)
            save_as_txt_file(json_format.MessageToJson(double_shark_fin_option), file_name, location)
        return store_object_to_cache("", tag, "DoubleSharkFinOption", double_shark_fin_option)
    except Exception as e:
        log_write_log_file(e.toString())
        return e.toString()
#region DqCreateRangeAccrualOption
def create_range_accrual_option(expiry_date: int,
                                  delivery_date: int,
                                  asset: float,
                                  cash: float,
                                  lower_barrier: float,
                                  upper_barrier: float,
                                  obs_schedule: list,
                                  nominal: float,
                                  payoff_ccy: str,
                                  underlying_type: str,
                                  underlying_ccy: str,
                                  underlying: str,
                                  tag: str,
                                  save: bool,
                                  location: str):
    try:
        instrument = RangeAccrualOption()
        instrument.expiry_date = create_date(expiry_date)
        instrument.delivery_date = create_date(delivery_date)
        instrument.asset = asset
        instrument.cash = cash
        instrument.lower_barrier = lower_barrier
        instrument.upper_barrier = upper_barrier
        instrument.nominal = nominal
        instrument.underlying = underlying
        instrument.payoff_currency = payoff_ccy
        instrument.underlying_currency = underlying_ccy
        instrument.underlying_type = to_underlying_type(underlying_type) if underlying_type != "" else InstrumentType.Spot
        instrument.fixing_schedule = create_fixing_schedule(obs_schedule)
        if save:
            file_name = "RangeAccrualOption_" + tag
            save_as_bin_file(instrument.SerializeToString(), file_name, location)
            save_as_txt_file(json_format.MessageToJson(instrument), file_name, location)
        return store_object_to_cache("", tag, "RangeAccrualOption", instrument)
    except Exception as e:
        log_write_log_file(e.toString())
        return e.toString()
#region DqCreateAirBagOption
def create_air_bag_option(payoff_type: str, 
                             expiry: int,
                             delivery: int,
                             lower_strike: float,
                             upper_strike: float,
                             lower_participation: float,
                             upper_participation: float,
                             knock_in_strike: float,
                             barrier_type: str,
                             barrier_value: float,
                             barrier_obs_type: str,
                             obs_schedule: list,                    
                             nominal: float,
                             payoff_ccy: str,
                             underlying_type: str,
                             underlying_ccy: str,
                             underlying: str,
                             tag: str,
                             save: bool,
                             location: str):
    try:
        instrument = AirbagOption()
        instrument.payoff_type = to_payoff_type(payoff_type)
        instrument.knock_in_strike = knock_in_strike
        instrument.barrier_obs_type = to_event_observation_type(barrier_obs_type) if barrier_obs_type != "" else EventObservationType.DiscreteObservationType
        instrument.barrier = Barrier()
        instrument.barrier.barrier_type = to_barrier_type(barrier_type)
        instrument.barrier.value = barrier_value
        instrument.lower_gearing = lower_participation
        instrument.upper_gearing = upper_participation
        instrument.lower_strike = lower_strike
        instrument.upper_strike = upper_strike
        instrument.expiry_date = create_date(expiry)
        instrument.delivery_date = create_date(delivery)
        instrument.nominal = nominal
        instrument.underlying = underlying
        instrument.payoff_currency = payoff_ccy
        instrument.underlying_currency = underlying_ccy
        instrument.underlying_type = to_underlying_type(underlying_type) if underlying_type != "" else InstrumentType.Spot
        if instrument.barrier_obs_type != EventObservationType.ContinuousObservationType:
            instrument.fixing_schedule = create_fixing_schedule(obs_schedule)
        
        if save:
            file_name = "AirBagOption_" + tag
            save_as_bin_file(instrument.SerializeToString(), file_name, location)
            save_as_txt_file(json_format.MessageToJson(instrument), file_name, location)
        return store_object_to_cache("", tag, "AirBagOption", instrument)
    except Exception as e:
        log_write_log_file(e.toString())
        return e.toString()
#region DqCreatePingPongOption
def create_ping_pong_option(expiry: int,
                               delivery: int,
                               lower_barrier: list,
                               upper_barrier: list,
                               barrier_obs_type: str,
                               obs_schedule: list,
                               payment_type: str,
                               cash: float,
                               asset: float,
                               settlement_days: int,
                               nominal: float,
                               payoff_ccy: str,
                               underlying_type: str,
                               underlying_ccy: str,
                               underlying: str,
                               tag: str,
                               save: bool,
                               location: str):
    try:
        ping_pong_option = PingPongOption()
        ping_pong_option.expiry_date = create_date(expiry)
        ping_pong_option.delivery_date = create_date(delivery)
        ping_pong_option.lower_barrier = Barrier()
        ping_pong_option.lower_barrier.barrier_type = to_barrier_type(lower_barrier[0])
        ping_pong_option.lower_barrier.value = lower_barrier[1]
        ping_pong_option.upper_barrier = Barrier()
        ping_pong_option.upper_barrier.barrier_type = to_barrier_type(upper_barrier[0])
        ping_pong_option.upper_barrier.value = upper_barrier[1]
        ping_pong_option.payment_type = to_payment_type(payment_type) if payment_type != "" else PaymentType.PayAtHit
        ping_pong_option.cash = cash
        ping_pong_option.asset = asset
        ping_pong_option.nominal = nominal
        ping_pong_option.underlying = underlying
        ping_pong_option.payoff_currency = payoff_ccy
        ping_pong_option.underlying_currency = underlying_ccy
        ping_pong_option.underlying_type = to_underlying_type(underlying_type) if underlying_type != "" else InstrumentType.Spot
        ping_pong_option.obs_type = to_event_observation_type(barrier_obs_type) if barrier_obs_type != "" else EventObservationType.ContinuousObservationType
        if ping_pong_option.obs_type != EventObservationType.ContinuousObservationType:
            ping_pong_option.fixing_schedule = create_fixing_schedule(obs_schedule)
        ping_pong_option.settlement_days = settlement_days
        if save:
            file_name = f"ping_pong_option_{tag.lower()}"
            save_as_bin_file(ping_pong_option.SerializeToString(), file_name, location)
            save_as_txt_file(json_format.MessageToJson(ping_pong_option), file_name, location)
        return store_object_to_cache("", tag, "PingPongOption", ping_pong_option)
    except Exception as e:
        log_write_log_file(e.toString())
        return e.toString()
#region DqCreateCollarOption
def create_collar_option(payoff_type: str,
                            lower_gearing: float,
                            upper_gearing: float,
                            lower_strike: float,
                            upper_strike: float,
                            expiry: int,
                            delivery: int,
                            nominal: float,
                            payoff_ccy: str,
                            underlying_type: str,
                            underlying_ccy: str,
                            underlying: str,
                            tag: str,
                            save: bool,
                            location: str):
    try:
        collar_option = CollarOption()
        collar_option.payoff_type = to_payoff_type(payoff_type)
        collar_option.lower_gearing = lower_gearing
        collar_option.upper_gearing = upper_gearing
        collar_option.lower_strike = lower_strike
        collar_option.upper_strike = upper_strike
        collar_option.expiry_date = create_date(expiry)
        collar_option.delivery_date = create_date(delivery)
        collar_option.nominal = nominal
        collar_option.underlying = underlying
        collar_option.payoff_currency = payoff_ccy
        collar_option.underlying_currency = underlying_ccy
        collar_option.underlying_type = to_underlying_type(underlying_type) if underlying_type != "" else InstrumentType.Spot
        if save:
            file_name = f"collar_option_{tag.lower()}"
            save_as_bin_file(collar_option.SerializeToString(), file_name, location)
            save_as_txt_file(json_format.MessageToJson(collar_option), file_name, location)
        return store_object_to_cache("", tag, "CollarOption", collar_option)
    except Exception as e:
        log_write_log_file(e.toString())
        return e.toString()
#region DqCreatePhoenixAutoCallableNote
def create_phoenix_auto_callable_note(
    coupon_payoff: list,
    start_date: int,
    coupon_dates: list,
    day_count: str,
    knock_out_barrier: list,
    knock_out_sched: list,
    knock_in_barrier: list,
    knock_in_sched: list,
    long_short: str,
    knock_in_payoff: list,
    expiry: int,
    delivery: int,
    settlement_days: int,
    nominal: float,
    payoff_ccy: str,
    underlying_type: str,
    underlying_ccy: str,
    underlying: str,
    tag: str,
    save: bool,
    location: str
):
    try:
        phoenix_auto_callable_note = PhoenixAutoCallableNote()
        if len(coupon_payoff) < 3:
            raise ValueError("coupon payoff should have at least 3 elements!")
        phoenix_auto_callable_note.coupon_payoff_type = to_payoff_type(coupon_payoff[0])
        phoenix_auto_callable_note.coupon_strike = float(coupon_payoff[1])
        phoenix_auto_callable_note.coupon_rate = float(coupon_payoff[2])
        phoenix_auto_callable_note.day_count = to_day_count(day_count) if day_count != "" else DayCountConvention.Act365Fixed
        phoenix_auto_callable_note.start_date = create_date(start_date)
        phoenix_auto_callable_note.knock_out_barrier = Barrier()
        phoenix_auto_callable_note.knock_out_barrier.barrier_type = to_barrier_type(knock_out_barrier[0])
        phoenix_auto_callable_note.knock_out_barrier.value = float(knock_out_barrier[1])
        phoenix_auto_callable_note.knock_in_barrier = Barrier()
        phoenix_auto_callable_note.knock_in_barrier.barrier_type = to_barrier_type(knock_in_barrier[0])
        phoenix_auto_callable_note.knock_in_barrier.value = float(knock_in_barrier[1])
        
        phoenix_auto_callable_note.long_short = to_buy_sell_flag(long_short) if long_short != "" else BuySellFlag.Sell
        if len(knock_in_payoff) < 2:
            raise ValueError("knock in payoff should have at least 2 elements!")
        phoenix_auto_callable_note.knock_in_payoff_type = to_payoff_type(knock_in_payoff[0]) if knock_in_payoff[0] != "" else PayoffType.Put
        phoenix_auto_callable_note.knock_in_payoff_strike = float(knock_in_payoff[1])
        phoenix_auto_callable_note.expiry = create_date(expiry)
        phoenix_auto_callable_note.delivery = create_date(delivery)
        phoenix_auto_callable_note.nominal = nominal
        phoenix_auto_callable_note.underlying = underlying
        phoenix_auto_callable_note.payoff_currency = payoff_ccy
        phoenix_auto_callable_note.underlying_currency = underlying_ccy
        phoenix_auto_callable_note.underlying_type = to_underlying_type(underlying_type) if underlying_type != "" else InstrumentType.Spot
        phoenix_auto_callable_note.settlement_days = settlement_days
        for coupon_date in coupon_dates:
            phoenix_auto_callable_note.coupon_dates.append(create_date(int(coupon_date)))
        phoenix_auto_callable_note.knock_out_sched = create_fixing_schedule(knock_out_sched)
        phoenix_auto_callable_note.knock_in_sched = create_fixing_schedule(knock_in_sched)
        if save:
            file_name = f"PhoenixAutoCallableNote_{tag.lower()}"
            save_as_bin_file(phoenix_auto_callable_note.SerializeToString(), file_name, location)
            save_as_txt_file(json_format.MessageToJson(phoenix_auto_callable_note), file_name, location)
        return store_object_to_cache("", tag, "PhoenixAutoCallableNote", phoenix_auto_callable_note)
    except Exception as e:
        log_write_log_file(e.toString())
        return e.toString()
#region DqCreateSnowballAutoCallableNote
def create_snowball_auto_callable_note(
    coupon_rate: float,
    start_date: int,
    coupon_dates: list,
    day_count: str,
    knock_out_barrier: list,
    knock_out_sched: list,
    knock_in_barrier: list,
    knock_in_sched: list,
    long_short: str,
    knock_in_payoff: list,
    reference_price: float,
    expiry: int,
    delivery: list,
    nominal: float,
    payoff_ccy: str,
    underlying_type: str,
    underlying_ccy: str,
    underlying: str,
    tag: str,
    save: bool,
    location: str
):
    try:
        snowball_auto_callable_note = SnowballAutoCallableNote()
        snowball_auto_callable_note.coupon_rate = coupon_rate
        snowball_auto_callable_note.day_count = to_day_count(day_count) if day_count != "" else DayCountConvention.Act365Fixed
        snowball_auto_callable_note.start_date = create_date(start_date)
        snowball_auto_callable_note.knock_out_barrier = Barrier()
        snowball_auto_callable_note.knock_out_barrier.barrier_type = to_barrier_type(knock_out_barrier[0])
        snowball_auto_callable_note.knock_out_barrier.value = float(knock_out_barrier[1])
        snowball_auto_callable_note.knock_in_barrier = Barrier()
        snowball_auto_callable_note.knock_in_barrier.barrier_type = to_barrier_type(knock_in_barrier[0])
        snowball_auto_callable_note.knock_in_barrier.value = float(knock_in_barrier[1])
        snowball_auto_callable_note.long_short = to_buy_sell_flag(long_short) if long_short != "" else BuySellFlag.Sell
        if len(knock_in_payoff) < 3:
            raise ValueError("knock in payoff should have at least 3 elements!")
        snowball_auto_callable_note.knock_in_payoff_type = to_payoff_type(knock_in_payoff[0]) if knock_in_payoff[0] != "" else PayoffType.Put
        snowball_auto_callable_note.knock_in_payoff_strike = float(knock_in_payoff[1])
        snowball_auto_callable_note.knock_in_payoff_gearing = float(knock_in_payoff[2])
        snowball_auto_callable_note.reference_price = reference_price
        snowball_auto_callable_note.expiry = create_date(expiry)
        snowball_auto_callable_note.delivery = create_date(delivery[0])
        snowball_auto_callable_note.nominal = nominal
        snowball_auto_callable_note.settlement_days = int(delivery[1]) if len(delivery) > 1 else 1
        snowball_auto_callable_note.underlying = underlying
        snowball_auto_callable_note.payoff_currency = payoff_ccy
        snowball_auto_callable_note.underlying_currency = underlying_ccy
        snowball_auto_callable_note.underlying_type = to_underlying_type(underlying_type) if underlying_type != "" else InstrumentType.Spot
        for coupon_date in coupon_dates:
            snowball_auto_callable_note.coupon_dates.append(create_date(coupon_date))
        snowball_auto_callable_note.knock_out_sched = create_fixing_schedule(knock_out_sched)
        snowball_auto_callable_note.knock_in_sched = create_fixing_schedule(knock_in_sched)
        if save:
            file_name = f"SnowballAutoCallableNote_{tag.lower()}"
            save_as_bin_file(snowball_auto_callable_note.SerializeToString(), file_name, location)
            save_as_txt_file(json_format.MessageToJson(snowball_auto_callable_note), file_name, location)
        return store_object_to_cache("", tag, "SnowballAutoCallableNote", snowball_auto_callable_note)
    except Exception as e:
        log_write_log_file(e.toString())
        return e.toString()