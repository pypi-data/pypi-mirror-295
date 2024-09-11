from caplibproto.dqfxanalyticsservice_pb2 import FxNonDeliverableForwardPricingOutput, FxSwapPricingOutput, \
    FxForwardPricingOutput
from caplibproto.dqproto import dqCreateProtoFxRiskSettings, dqCreateProtoFxMktDataSet, \
    dqCreateProtoFxNonDeliverableForwardPricingInput, dqCreateProtoFxSwapPricingInput, \
    dqCreateProtoFxForwardPricingInput

from caplib.market import *
from caplib.datetime import *
from caplib.processrequest import process_request

def create_fx_risk_settings(ir_curve_settings,
                            price_settings,
                            vol_settings,
                            price_vol_settings,
                            theta_settings):
    """

    Parameters
    ----------
    ir_curve_settings: IrCurveRiskSettings
    price_settings: PriceRiskSettings
    vol_settings: VolRiskSettings
    price_vol_settings: PriceVolRiskSettings
    theta_settings: ThetaRiskSettings

    Returns
    -------
    FxRiskSettings

    """
    return dqCreateProtoFxRiskSettings(ir_curve_settings,
                                       price_settings,
                                       vol_settings,
                                       price_vol_settings,
                                       theta_settings)


def create_fx_mkt_data_set(as_of_date,
                           domestic_discount_curve,
                           foreign_discount_curve,
                           spot,
                           vol_surf):
    """

    Parameters
    ----------
    as_of_date: Date
    domestic_discount_curve: IrYieldCurve
    foreign_discount_curve: IrYieldCurve
    spot: FxSpotRate
    vol_surf: VolatilitySurface

    Returns
    -------
    FxMktDataSet

    """
    return dqCreateProtoFxMktDataSet(create_date(as_of_date),
                                     domestic_discount_curve,
                                     foreign_discount_curve,
                                     spot,
                                     vol_surf)


def fx_ndf_pricer(pricing_date,
                  instrument,
                  mkt_data,
                  pricing_settings,
                  risk_settings):
    """

    Parameters
    ----------
    pricing_date: Date
    instrument: FxNonDeliverableForwad
    mkt_data: FxMktDataSet
    pricing_settings: PricingSettings
    risk_settings: FxRiskSettings

    Returns
    -------
    PricingResults

    """
    pb_input = dqCreateProtoFxNonDeliverableForwardPricingInput(create_date(pricing_date),
                                                                instrument,
                                                                mkt_data,
                                                                pricing_settings,
                                                                risk_settings,
                                                                False, b'', b'', b'', b'')
    req_name = "FX_NONDELIVERABLE_FORWARD_PRICER"
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = FxNonDeliverableForwardPricingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.results


def fx_swap_pricer(pricing_date,
                   instrument,
                   mkt_data,
                   pricing_settings,
                   risk_settings):
    """

    Parameters
    ----------
    pricing_date: Date
    instrument: FxSwap
    mkt_data: FxMktDataSet
    pricing_settings: PricingSettings
    risk_settings: FxRiskSettings

    Returns
    -------
    PricingResults

    """
    pb_input = dqCreateProtoFxSwapPricingInput(create_date(pricing_date),
                                               instrument,
                                               mkt_data,
                                               pricing_settings,
                                               risk_settings,
                                               False, b'', b'', b'', b'')
    req_name = 'FX_SWAP_PRICER'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = FxSwapPricingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.results


def fx_forward_pricer(pricing_date,
                      instrument,
                      mkt_data,
                      pricing_settings,
                      risk_settings):
    """

    Parameters
    ----------
    pricing_date: Date
    instrument: FxForward
    mkt_data: FxMktDataSet
    pricing_settings: PricingSettings
    risk_settings: FxRiskSettings

    Returns
    -------
    PricingResults

    """
    pb_input = dqCreateProtoFxForwardPricingInput(create_date(pricing_date),
                                                  instrument,
                                                  mkt_data,
                                                  pricing_settings,
                                                  risk_settings,
                                                  False, b'', b'', b'', b'')
    req_name = 'FX_FORWARD_PRICER'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = FxForwardPricingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.results
