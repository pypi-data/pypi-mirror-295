from .dqanalytics_pb2 import *
from .dqanalyticsservice_pb2 import *
from .dqcmanalytics_pb2 import *
from .dqcmanalyticsservice_pb2 import *
from .dqcmmarket_pb2 import *
from .dqcmmarketservice_pb2 import *
from .dqcranalytics_pb2 import *
from .dqcranalyticsservice_pb2 import *
from .dqcrmarket_pb2 import *
from .dqcrmarketservice_pb2 import *
from .dqdatetime_pb2 import *
from .dqdatetimeservice_pb2 import *
from .dqeqanalytics_pb2 import *
from .dqeqanalyticsservice_pb2 import *
from .dqeqmarketservice_pb2 import *
from .dqfianalytics_pb2 import *
from .dqfianalyticsservice_pb2 import *
from .dqfimarket_pb2 import *
from .dqfimarketservice_pb2 import *
from .dqfxanalytics_pb2 import *
from .dqfxanalyticsservice_pb2 import *
from .dqfxmarket_pb2 import *
from .dqfxmarketservice_pb2 import *
from .dqiranalytics_pb2 import *
from .dqiranalyticsservice_pb2 import *
from .dqirmarket_pb2 import *
from .dqirmarketservice_pb2 import *
from .dqlib_pb2 import *
from .dqmarket_pb2 import *
from .dqmarketrisk_pb2 import *
from .dqmarketriskservice_pb2 import *
from .dqmarketservice_pb2 import *
from .dqnumerics_pb2 import *
from .dqstaticdataservice_pb2 import *

import sys

import copy
#Curve
def dqCreateProtoCurve(p_interpolator, p_name):
    '''
    @args:
        1. p_interpolator: dqproto.Interpolator1D
        2. p_name: string
    @return:
        dqproto.Curve
    '''
    try:
        tmp_this= Curve()
        tmp_this.interpolator.CopyFrom(p_interpolator)
        tmp_this.name=p_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#TermStructureCurve
def dqCreateProtoTermStructureCurve(p_reference_date, p_day_count_convention, p_pillar_date, p_pillar_name, p_pillar_values, p_interp_method, p_extrap_method, p_name):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_day_count_convention: dqproto.DayCountConvention
        3. p_pillar_date: dqproto.Date
        4. p_pillar_name: string
        5. p_pillar_values: dqproto.Vector
        6. p_interp_method: dqproto.InterpMethod
        7. p_extrap_method: dqproto.ExtrapMethod
        8. p_name: string
    @return:
        dqproto.TermStructureCurve
    '''
    try:
        tmp_this= TermStructureCurve()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.day_count_convention=p_day_count_convention
        tmp_this.pillar_date.extend(p_pillar_date)
        tmp_this.pillar_name.extend(p_pillar_name)
        tmp_this.pillar_values.CopyFrom(p_pillar_values)
        tmp_this.interp_method=p_interp_method
        tmp_this.extrap_method=p_extrap_method
        tmp_this.name=p_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#AssetPriceCurve
def dqCreateProtoAssetPriceCurve(p_curve, p_currency):
    '''
    @args:
        1. p_curve: dqproto.TermStructureCurve
        2. p_currency: string
    @return:
        dqproto.AssetPriceCurve
    '''
    try:
        tmp_this= AssetPriceCurve()
        tmp_this.curve.CopyFrom(p_curve)
        tmp_this.currency=p_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#AssetYieldCurve
def dqCreateProtoAssetYieldCurve(p_curve, p_compounding_type):
    '''
    @args:
        1. p_curve: dqproto.TermStructureCurve
        2. p_compounding_type: dqproto.CompoundingType
    @return:
        dqproto.AssetYieldCurve
    '''
    try:
        tmp_this= AssetYieldCurve()
        tmp_this.curve.CopyFrom(p_curve)
        tmp_this.compounding_type=p_compounding_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrYieldCurve.Jacobian
def dqCreateProtoIrYieldCurve_Jacobian(p_name, p_matrix):
    '''
    @args:
        1. p_name: string
        2. p_matrix: dqproto.Matrix
    @return:
        dqproto.IrYieldCurve.Jacobian
    '''
    try:
        tmp_this= IrYieldCurve.Jacobian()
        tmp_this.name=p_name
        tmp_this.matrix.CopyFrom(p_matrix)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrYieldCurve
def dqCreateProtoIrYieldCurve(p_type, p_curve, p_currency, p_frequency, p_jacobians):
    '''
    @args:
        1. p_type: dqproto.IrYieldCurveType
        2. p_curve: dqproto.AssetYieldCurve
        3. p_currency: string
        4. p_frequency: dqproto.Frequency
        5. p_jacobians: dqproto.IrYieldCurve.Jacobian
    @return:
        dqproto.IrYieldCurve
    '''
    try:
        tmp_this= IrYieldCurve()
        tmp_this.type=p_type
        tmp_this.curve.CopyFrom(p_curve)
        tmp_this.currency=p_currency
        tmp_this.frequency=p_frequency
        tmp_this.jacobians.extend(p_jacobians)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditCurve
def dqCreateProtoCreditCurve(p_curve, p_credit_spreads):
    '''
    @args:
        1. p_curve: dqproto.TermStructureCurve
        2. p_credit_spreads: dqproto.Vector
    @return:
        dqproto.CreditCurve
    '''
    try:
        tmp_this= CreditCurve()
        tmp_this.curve.CopyFrom(p_curve)
        tmp_this.credit_spreads.CopyFrom(p_credit_spreads)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#DividendCurve
def dqCreateProtoDividendCurve(p_curve, p_yield_start_date, p_dividend_type):
    '''
    @args:
        1. p_curve: dqproto.AssetYieldCurve
        2. p_yield_start_date: dqproto.Date
        3. p_dividend_type: dqproto.DividendType
    @return:
        dqproto.DividendCurve
    '''
    try:
        tmp_this= DividendCurve()
        tmp_this.curve.CopyFrom(p_curve)
        tmp_this.yield_start_date.CopyFrom(p_yield_start_date)
        tmp_this.dividend_type=p_dividend_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#VolatilityCurve
def dqCreateProtoVolatilityCurve(p_reference_date, p_day_count_convention, p_pillar_date, p_pillar_name, p_volatilities, p_interp_method, p_extrap_method, p_underlying):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_day_count_convention: dqproto.DayCountConvention
        3. p_pillar_date: dqproto.Date
        4. p_pillar_name: string
        5. p_volatilities: dqproto.Vector
        6. p_interp_method: dqproto.InterpMethod
        7. p_extrap_method: dqproto.ExtrapMethod
        8. p_underlying: string
    @return:
        dqproto.VolatilityCurve
    '''
    try:
        tmp_this= VolatilityCurve()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.day_count_convention=p_day_count_convention
        tmp_this.pillar_date.extend(p_pillar_date)
        tmp_this.pillar_name.extend(p_pillar_name)
        tmp_this.volatilities.CopyFrom(p_volatilities)
        tmp_this.interp_method=p_interp_method
        tmp_this.extrap_method=p_extrap_method
        tmp_this.underlying=p_underlying
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#VolatilitySmile
def dqCreateProtoVolatilitySmile(p_vol_smile_type, p_reference_date, p_lower, p_upper, p_abscissas, p_vols, p_smile_method, p_term, p_model_params, p_auxiliary_params, p_extrap_method):
    '''
    @args:
        1. p_vol_smile_type: dqproto.VolSmileType
        2. p_reference_date: dqproto.Date
        3. p_lower: double
        4. p_upper: double
        5. p_abscissas: dqproto.Vector
        6. p_vols: dqproto.Vector
        7. p_smile_method: dqproto.VolSmileMethod
        8. p_term: double
        9. p_model_params: dqproto.Vector
        10. p_auxiliary_params: dqproto.Vector
        11. p_extrap_method: dqproto.ExtrapMethod
    @return:
        dqproto.VolatilitySmile
    '''
    try:
        tmp_this= VolatilitySmile()
        tmp_this.vol_smile_type=p_vol_smile_type
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.lower=p_lower
        tmp_this.upper=p_upper
        tmp_this.abscissas.CopyFrom(p_abscissas)
        tmp_this.vols.CopyFrom(p_vols)
        tmp_this.smile_method=p_smile_method
        tmp_this.term=p_term
        tmp_this.model_params.CopyFrom(p_model_params)
        tmp_this.auxiliary_params.CopyFrom(p_auxiliary_params)
        tmp_this.extrap_method=p_extrap_method
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#SabrVolSmile
def dqCreateProtoSabrVolSmile(p_vol_smile):
    '''
    @args:
        1. p_vol_smile: dqproto.VolatilitySmile
    @return:
        dqproto.SabrVolSmile
    '''
    try:
        tmp_this= SabrVolSmile()
        tmp_this.vol_smile.CopyFrom(p_vol_smile)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#SviVolSmile
def dqCreateProtoSviVolSmile(p_vol_smile):
    '''
    @args:
        1. p_vol_smile: dqproto.VolatilitySmile
    @return:
        dqproto.SviVolSmile
    '''
    try:
        tmp_this= SviVolSmile()
        tmp_this.vol_smile.CopyFrom(p_vol_smile)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ScalarVolSmile
def dqCreateProtoScalarVolSmile(p_vol_smile):
    '''
    @args:
        1. p_vol_smile: dqproto.VolatilitySmile
    @return:
        dqproto.ScalarVolSmile
    '''
    try:
        tmp_this= ScalarVolSmile()
        tmp_this.vol_smile.CopyFrom(p_vol_smile)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#VolatilitySurfaceDefinition
def dqCreateProtoVolatilitySurfaceDefinition(p_vol_smile_type, p_smile_method, p_smile_extrap_method, p_time_interp_method, p_time_extrap_method, p_day_count_convention, p_vol_type, p_wing_strike_type, p_lower, p_upper):
    '''
    @args:
        1. p_vol_smile_type: dqproto.VolSmileType
        2. p_smile_method: dqproto.VolSmileMethod
        3. p_smile_extrap_method: dqproto.ExtrapMethod
        4. p_time_interp_method: dqproto.VolTermInterpMethod
        5. p_time_extrap_method: dqproto.VolTermExtrapMethod
        6. p_day_count_convention: dqproto.DayCountConvention
        7. p_vol_type: dqproto.VolatilityType
        8. p_wing_strike_type: dqproto.WingStrikeType
        9. p_lower: double
        10. p_upper: double
    @return:
        dqproto.VolatilitySurfaceDefinition
    '''
    try:
        tmp_this= VolatilitySurfaceDefinition()
        tmp_this.vol_smile_type=p_vol_smile_type
        tmp_this.smile_method=p_smile_method
        tmp_this.smile_extrap_method=p_smile_extrap_method
        tmp_this.time_interp_method=p_time_interp_method
        tmp_this.time_extrap_method=p_time_extrap_method
        tmp_this.day_count_convention=p_day_count_convention
        tmp_this.vol_type=p_vol_type
        tmp_this.wing_strike_type=p_wing_strike_type
        tmp_this.lower=p_lower
        tmp_this.upper=p_upper
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#VolatilitySurfaceBuildSettings
def dqCreateProtoVolatilitySurfaceBuildSettings(p_ith_param_fixed, p_ith_param):
    '''
    @args:
        1. p_ith_param_fixed: int32
        2. p_ith_param: double
    @return:
        dqproto.VolatilitySurfaceBuildSettings
    '''
    try:
        tmp_this= VolatilitySurfaceBuildSettings()
        tmp_this.ith_param_fixed=p_ith_param_fixed
        tmp_this.ith_param=p_ith_param
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#OptionQuote
def dqCreateProtoOptionQuote(p_payoff_type, p_value, p_strike):
    '''
    @args:
        1. p_payoff_type: dqproto.PayoffType
        2. p_value: double
        3. p_strike: double
    @return:
        dqproto.OptionQuote
    '''
    try:
        tmp_this= OptionQuote()
        tmp_this.payoff_type=p_payoff_type
        tmp_this.value=p_value
        tmp_this.strike=p_strike
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#OptionQuoteVector
def dqCreateProtoOptionQuoteVector(p_term, p_term_date, p_quotes, p_tenor, p_tenor_date):
    '''
    @args:
        1. p_term: dqproto.Period
        2. p_term_date: dqproto.Date
        3. p_quotes: dqproto.OptionQuote
        4. p_tenor: dqproto.Period
        5. p_tenor_date: dqproto.Date
    @return:
        dqproto.OptionQuoteVector
    '''
    try:
        tmp_this= OptionQuoteVector()
        tmp_this.term.CopyFrom(p_term)
        tmp_this.term_date.CopyFrom(p_term_date)
        tmp_this.quotes.extend(p_quotes)
        tmp_this.tenor.CopyFrom(p_tenor)
        tmp_this.tenor_date.CopyFrom(p_tenor_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#OptionQuoteMatrix
def dqCreateProtoOptionQuoteMatrix(p_option_quote_value_type, p_option_quote_term_type, p_option_quote_strike_type, p_option_quote_exercise_type, p_option_quote_underlying_type, p_as_of_date, p_quote_smiles, p_asset_name):
    '''
    @args:
        1. p_option_quote_value_type: dqproto.OptionQuoteValueType
        2. p_option_quote_term_type: dqproto.OptionQuoteTermType
        3. p_option_quote_strike_type: dqproto.OptionQuoteStrikeType
        4. p_option_quote_exercise_type: dqproto.ExerciseType
        5. p_option_quote_underlying_type: dqproto.OptionUnderlyingType
        6. p_as_of_date: dqproto.Date
        7. p_quote_smiles: dqproto.OptionQuoteVector
        8. p_asset_name: string
    @return:
        dqproto.OptionQuoteMatrix
    '''
    try:
        tmp_this= OptionQuoteMatrix()
        tmp_this.option_quote_value_type=p_option_quote_value_type
        tmp_this.option_quote_term_type=p_option_quote_term_type
        tmp_this.option_quote_strike_type=p_option_quote_strike_type
        tmp_this.option_quote_exercise_type=p_option_quote_exercise_type
        tmp_this.option_quote_underlying_type=p_option_quote_underlying_type
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.quote_smiles.extend(p_quote_smiles)
        tmp_this.asset_name=p_asset_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#VolatilitySurface
def dqCreateProtoVolatilitySurface(p_definition, p_reference_date, p_vol_smiles, p_term_dates, p_underlying):
    '''
    @args:
        1. p_definition: dqproto.VolatilitySurfaceDefinition
        2. p_reference_date: dqproto.Date
        3. p_vol_smiles: dqproto.VolatilitySmile
        4. p_term_dates: dqproto.Date
        5. p_underlying: string
    @return:
        dqproto.VolatilitySurface
    '''
    try:
        tmp_this= VolatilitySurface()
        tmp_this.definition.CopyFrom(p_definition)
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.vol_smiles.extend(p_vol_smiles)
        tmp_this.term_dates.extend(p_term_dates)
        tmp_this.underlying=p_underlying
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PricingModelSettings
def dqCreateProtoPricingModelSettings(p_model_name, p_constant_params, p_model_params, p_asset, p_model_calibrated):
    '''
    @args:
        1. p_model_name: dqproto.PricingModelName
        2. p_constant_params: double
        3. p_model_params: dqproto.TermStructureCurve
        4. p_asset: string
        5. p_model_calibrated: bool
    @return:
        dqproto.PricingModelSettings
    '''
    try:
        tmp_this= PricingModelSettings()
        tmp_this.model_name=p_model_name
        tmp_this.constant_params.extend(p_constant_params)
        tmp_this.model_params.extend(p_model_params)
        tmp_this.asset=p_asset
        tmp_this.model_calibrated=p_model_calibrated
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#MonteCarloSettings
def dqCreateProtoMonteCarloSettings(p_num_simulations, p_uniform_number_type, p_seed, p_wiener_process_build_method, p_gaussian_number_method, p_use_antithetic, p_num_steps):
    '''
    @args:
        1. p_num_simulations: int32
        2. p_uniform_number_type: dqproto.UniformRandomNumberType
        3. p_seed: int32
        4. p_wiener_process_build_method: dqproto.WienerProcessBuildMethod
        5. p_gaussian_number_method: dqproto.GaussianNumberMethod
        6. p_use_antithetic: bool
        7. p_num_steps: int32
    @return:
        dqproto.MonteCarloSettings
    '''
    try:
        tmp_this= MonteCarloSettings()
        tmp_this.num_simulations=p_num_simulations
        tmp_this.uniform_number_type=p_uniform_number_type
        tmp_this.seed=p_seed
        tmp_this.wiener_process_build_method=p_wiener_process_build_method
        tmp_this.gaussian_number_method=p_gaussian_number_method
        tmp_this.use_antithetic=p_use_antithetic
        tmp_this.num_steps=p_num_steps
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PdeSettings
def dqCreateProtoPdeSettings(p_t_size, p_x_size, p_x_min, p_x_max, p_x_min_max_type, p_y_size, p_y_min, p_y_max, p_y_min_max_type, p_z_size, p_z_min, p_z_max, p_z_min_max_type, p_x_density, p_y_density, p_z_density, p_x_grid_type, p_y_grid_type, p_z_grid_type, p_x_interp_method, p_y_interp_method, p_z_interp_method):
    '''
    @args:
        1. p_t_size: int32
        2. p_x_size: int32
        3. p_x_min: double
        4. p_x_max: double
        5. p_x_min_max_type: dqproto.MinMaxType
        6. p_y_size: int32
        7. p_y_min: double
        8. p_y_max: double
        9. p_y_min_max_type: dqproto.MinMaxType
        10. p_z_size: int32
        11. p_z_min: double
        12. p_z_max: double
        13. p_z_min_max_type: dqproto.MinMaxType
        14. p_x_density: double
        15. p_y_density: double
        16. p_z_density: double
        17. p_x_grid_type: dqproto.GridType
        18. p_y_grid_type: dqproto.GridType
        19. p_z_grid_type: dqproto.GridType
        20. p_x_interp_method: dqproto.InterpMethod
        21. p_y_interp_method: dqproto.InterpMethod
        22. p_z_interp_method: dqproto.InterpMethod
    @return:
        dqproto.PdeSettings
    '''
    try:
        tmp_this= PdeSettings()
        tmp_this.t_size=p_t_size
        tmp_this.x_size=p_x_size
        tmp_this.x_min=p_x_min
        tmp_this.x_max=p_x_max
        tmp_this.x_min_max_type=p_x_min_max_type
        tmp_this.y_size=p_y_size
        tmp_this.y_min=p_y_min
        tmp_this.y_max=p_y_max
        tmp_this.y_min_max_type=p_y_min_max_type
        tmp_this.z_size=p_z_size
        tmp_this.z_min=p_z_min
        tmp_this.z_max=p_z_max
        tmp_this.z_min_max_type=p_z_min_max_type
        tmp_this.x_density=p_x_density
        tmp_this.y_density=p_y_density
        tmp_this.z_density=p_z_density
        tmp_this.x_grid_type=p_x_grid_type
        tmp_this.y_grid_type=p_y_grid_type
        tmp_this.z_grid_type=p_z_grid_type
        tmp_this.x_interp_method=p_x_interp_method
        tmp_this.y_interp_method=p_y_interp_method
        tmp_this.z_interp_method=p_z_interp_method
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PricingSettings
def dqCreateProtoPricingSettings(p_currency, p_inc_current, p_pde_settings, p_mc_settings, p_model_settings, p_pricing_method, p_specific_pricing_requests, p_cash_flows):
    '''
    @args:
        1. p_currency: string
        2. p_inc_current: bool
        3. p_pde_settings: dqproto.PdeSettings
        4. p_mc_settings: dqproto.MonteCarloSettings
        5. p_model_settings: dqproto.PricingModelSettings
        6. p_pricing_method: dqproto.PricingMethodName
        7. p_specific_pricing_requests: int32
        8. p_cash_flows: bool
    @return:
        dqproto.PricingSettings
    '''
    try:
        tmp_this= PricingSettings()
        tmp_this.currency=p_currency
        tmp_this.inc_current=p_inc_current
        tmp_this.pde_settings.CopyFrom(p_pde_settings)
        tmp_this.mc_settings.CopyFrom(p_mc_settings)
        tmp_this.model_settings.CopyFrom(p_model_settings)
        tmp_this.pricing_method=p_pricing_method
        tmp_this.specific_pricing_requests.extend(p_specific_pricing_requests)
        tmp_this.cash_flows=p_cash_flows
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ThetaRiskSettings
def dqCreateProtoThetaRiskSettings(p_theta, p_shift, p_scaling_factor):
    '''
    @args:
        1. p_theta: bool
        2. p_shift: int32
        3. p_scaling_factor: double
    @return:
        dqproto.ThetaRiskSettings
    '''
    try:
        tmp_this= ThetaRiskSettings()
        tmp_this.theta=p_theta
        tmp_this.shift=p_shift
        tmp_this.scaling_factor=p_scaling_factor
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCurveRiskSettings
def dqCreateProtoIrCurveRiskSettings(p_delta, p_gamma, p_curvature, p_shift, p_curvature_shift, p_method, p_granularity, p_scaling_factor, p_threading_mode):
    '''
    @args:
        1. p_delta: bool
        2. p_gamma: bool
        3. p_curvature: bool
        4. p_shift: double
        5. p_curvature_shift: double
        6. p_method: dqproto.FiniteDifferenceMethod
        7. p_granularity: dqproto.RiskGranularity
        8. p_scaling_factor: double
        9. p_threading_mode: dqproto.ThreadingMode
    @return:
        dqproto.IrCurveRiskSettings
    '''
    try:
        tmp_this= IrCurveRiskSettings()
        tmp_this.delta=p_delta
        tmp_this.gamma=p_gamma
        tmp_this.curvature=p_curvature
        tmp_this.shift=p_shift
        tmp_this.curvature_shift=p_curvature_shift
        tmp_this.method=p_method
        tmp_this.granularity=p_granularity
        tmp_this.scaling_factor=p_scaling_factor
        tmp_this.threading_mode=p_threading_mode
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditCurveRiskSettings
def dqCreateProtoCreditCurveRiskSettings(p_delta, p_gamma, p_shift, p_method, p_granularity, p_scaling_factor, p_threading_mode):
    '''
    @args:
        1. p_delta: bool
        2. p_gamma: bool
        3. p_shift: double
        4. p_method: dqproto.FiniteDifferenceMethod
        5. p_granularity: dqproto.RiskGranularity
        6. p_scaling_factor: double
        7. p_threading_mode: dqproto.ThreadingMode
    @return:
        dqproto.CreditCurveRiskSettings
    '''
    try:
        tmp_this= CreditCurveRiskSettings()
        tmp_this.delta=p_delta
        tmp_this.gamma=p_gamma
        tmp_this.shift=p_shift
        tmp_this.method=p_method
        tmp_this.granularity=p_granularity
        tmp_this.scaling_factor=p_scaling_factor
        tmp_this.threading_mode=p_threading_mode
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#DividendCurveRiskSettings
def dqCreateProtoDividendCurveRiskSettings(p_delta, p_gamma, p_shift, p_method, p_granularity, p_scaling_factor, p_threading_mode):
    '''
    @args:
        1. p_delta: bool
        2. p_gamma: bool
        3. p_shift: double
        4. p_method: dqproto.FiniteDifferenceMethod
        5. p_granularity: dqproto.RiskGranularity
        6. p_scaling_factor: double
        7. p_threading_mode: dqproto.ThreadingMode
    @return:
        dqproto.DividendCurveRiskSettings
    '''
    try:
        tmp_this= DividendCurveRiskSettings()
        tmp_this.delta=p_delta
        tmp_this.gamma=p_gamma
        tmp_this.shift=p_shift
        tmp_this.method=p_method
        tmp_this.granularity=p_granularity
        tmp_this.scaling_factor=p_scaling_factor
        tmp_this.threading_mode=p_threading_mode
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PriceRiskSettings
def dqCreateProtoPriceRiskSettings(p_delta, p_gamma, p_curvature, p_shift, p_curvature_shift, p_method, p_scaling_factor, p_threading_mode):
    '''
    @args:
        1. p_delta: bool
        2. p_gamma: bool
        3. p_curvature: bool
        4. p_shift: double
        5. p_curvature_shift: double
        6. p_method: dqproto.FiniteDifferenceMethod
        7. p_scaling_factor: double
        8. p_threading_mode: dqproto.ThreadingMode
    @return:
        dqproto.PriceRiskSettings
    '''
    try:
        tmp_this= PriceRiskSettings()
        tmp_this.delta=p_delta
        tmp_this.gamma=p_gamma
        tmp_this.curvature=p_curvature
        tmp_this.shift=p_shift
        tmp_this.curvature_shift=p_curvature_shift
        tmp_this.method=p_method
        tmp_this.scaling_factor=p_scaling_factor
        tmp_this.threading_mode=p_threading_mode
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#VolRiskSettings
def dqCreateProtoVolRiskSettings(p_vega, p_volga, p_shift, p_method, p_granularity, p_scaling_factor, p_threading_mode):
    '''
    @args:
        1. p_vega: bool
        2. p_volga: bool
        3. p_shift: double
        4. p_method: dqproto.FiniteDifferenceMethod
        5. p_granularity: dqproto.RiskGranularity
        6. p_scaling_factor: double
        7. p_threading_mode: dqproto.ThreadingMode
    @return:
        dqproto.VolRiskSettings
    '''
    try:
        tmp_this= VolRiskSettings()
        tmp_this.vega=p_vega
        tmp_this.volga=p_volga
        tmp_this.shift=p_shift
        tmp_this.method=p_method
        tmp_this.granularity=p_granularity
        tmp_this.scaling_factor=p_scaling_factor
        tmp_this.threading_mode=p_threading_mode
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PriceVolRiskSettings
def dqCreateProtoPriceVolRiskSettings(p_vanna, p_price_shift, p_vol_shift, p_method, p_granularity, p_price_scaling_factor, p_vol_scaling_factor, p_threading_mode):
    '''
    @args:
        1. p_vanna: bool
        2. p_price_shift: double
        3. p_vol_shift: double
        4. p_method: dqproto.FiniteDifferenceMethod
        5. p_granularity: dqproto.RiskGranularity
        6. p_price_scaling_factor: double
        7. p_vol_scaling_factor: double
        8. p_threading_mode: dqproto.ThreadingMode
    @return:
        dqproto.PriceVolRiskSettings
    '''
    try:
        tmp_this= PriceVolRiskSettings()
        tmp_this.vanna=p_vanna
        tmp_this.price_shift=p_price_shift
        tmp_this.vol_shift=p_vol_shift
        tmp_this.method=p_method
        tmp_this.granularity=p_granularity
        tmp_this.price_scaling_factor=p_price_scaling_factor
        tmp_this.vol_scaling_factor=p_vol_scaling_factor
        tmp_this.threading_mode=p_threading_mode
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#RiskSettings
def dqCreateProtoRiskSettings(p_risk, p_theta_settings):
    '''
    @args:
        1. p_risk: bool
        2. p_theta_settings: dqproto.ThetaRiskSettings
    @return:
        dqproto.RiskSettings
    '''
    try:
        tmp_this= RiskSettings()
        tmp_this.risk=p_risk
        tmp_this.theta_settings.CopyFrom(p_theta_settings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GeneralisedBlackScholesModel
def dqCreateProtoGeneralisedBlackScholesModel(p_num_assets, p_as_of_date, p_initial_values, p_ir_yield_curves, p_asset_yield_curves, p_volatility_curves, p_displacement, p_corr_matrix):
    '''
    @args:
        1. p_num_assets: int32
        2. p_as_of_date: dqproto.Date
        3. p_initial_values: dqproto.Vector
        4. p_ir_yield_curves: dqproto.IrYieldCurve
        5. p_asset_yield_curves: dqproto.AssetYieldCurve
        6. p_volatility_curves: dqproto.VolatilityCurve
        7. p_displacement: dqproto.Vector
        8. p_corr_matrix: dqproto.Matrix
    @return:
        dqproto.GeneralisedBlackScholesModel
    '''
    try:
        tmp_this= GeneralisedBlackScholesModel()
        tmp_this.num_assets=p_num_assets
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.initial_values.CopyFrom(p_initial_values)
        tmp_this.ir_yield_curves.extend(p_ir_yield_curves)
        tmp_this.asset_yield_curves.extend(p_asset_yield_curves)
        tmp_this.volatility_curves.extend(p_volatility_curves)
        tmp_this.displacement.CopyFrom(p_displacement)
        tmp_this.corr_matrix.CopyFrom(p_corr_matrix)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#DupireLocalVolModel
def dqCreateProtoDupireLocalVolModel(p_as_of_date, p_initial_value, p_ir_yield_curve, p_asset_yield_curve, p_volatility_surface, p_t_grid, p_x_grid, p_vol_spread):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_initial_value: double
        3. p_ir_yield_curve: dqproto.IrYieldCurve
        4. p_asset_yield_curve: dqproto.AssetYieldCurve
        5. p_volatility_surface: dqproto.VolatilitySurface
        6. p_t_grid: dqproto.Vector
        7. p_x_grid: dqproto.Vector
        8. p_vol_spread: double
    @return:
        dqproto.DupireLocalVolModel
    '''
    try:
        tmp_this= DupireLocalVolModel()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.initial_value=p_initial_value
        tmp_this.ir_yield_curve.CopyFrom(p_ir_yield_curve)
        tmp_this.asset_yield_curve.CopyFrom(p_asset_yield_curve)
        tmp_this.volatility_surface.CopyFrom(p_volatility_surface)
        tmp_this.t_grid.CopyFrom(p_t_grid)
        tmp_this.x_grid.CopyFrom(p_x_grid)
        tmp_this.vol_spread=p_vol_spread
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#HestonStochVolProcess
def dqCreateProtoHestonStochVolProcess(p_reference_date, p_initial_asset_price, p_initial_variance, p_kappa, p_theta, p_sigma, p_rho, p_ir_yield_curve, p_asset_yield_curve, p_volatility_curve):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_initial_asset_price: double
        3. p_initial_variance: double
        4. p_kappa: double
        5. p_theta: double
        6. p_sigma: double
        7. p_rho: double
        8. p_ir_yield_curve: dqproto.IrYieldCurve
        9. p_asset_yield_curve: dqproto.AssetYieldCurve
        10. p_volatility_curve: dqproto.VolatilityCurve
    @return:
        dqproto.HestonStochVolProcess
    '''
    try:
        tmp_this= HestonStochVolProcess()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.initial_asset_price=p_initial_asset_price
        tmp_this.initial_variance=p_initial_variance
        tmp_this.kappa=p_kappa
        tmp_this.theta=p_theta
        tmp_this.sigma=p_sigma
        tmp_this.rho=p_rho
        tmp_this.ir_yield_curve.CopyFrom(p_ir_yield_curve)
        tmp_this.asset_yield_curve.CopyFrom(p_asset_yield_curve)
        tmp_this.volatility_curve.CopyFrom(p_volatility_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#HestonStochVolModel
def dqCreateProtoHestonStochVolModel(p_num_assets, p_as_of_date, p_initial_asset_prices, p_initial_variances, p_kappas, p_thetas, p_sigmas, p_rhos, p_ir_yield_curves, p_asset_yield_curves, p_volatility_curves, p_corr_matrix):
    '''
    @args:
        1. p_num_assets: int32
        2. p_as_of_date: dqproto.Date
        3. p_initial_asset_prices: dqproto.Vector
        4. p_initial_variances: dqproto.Vector
        5. p_kappas: dqproto.Vector
        6. p_thetas: dqproto.Vector
        7. p_sigmas: dqproto.Vector
        8. p_rhos: dqproto.Vector
        9. p_ir_yield_curves: dqproto.IrYieldCurve
        10. p_asset_yield_curves: dqproto.AssetYieldCurve
        11. p_volatility_curves: dqproto.VolatilityCurve
        12. p_corr_matrix: dqproto.Matrix
    @return:
        dqproto.HestonStochVolModel
    '''
    try:
        tmp_this= HestonStochVolModel()
        tmp_this.num_assets=p_num_assets
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.initial_asset_prices.CopyFrom(p_initial_asset_prices)
        tmp_this.initial_variances.CopyFrom(p_initial_variances)
        tmp_this.kappas.CopyFrom(p_kappas)
        tmp_this.thetas.CopyFrom(p_thetas)
        tmp_this.sigmas.CopyFrom(p_sigmas)
        tmp_this.rhos.CopyFrom(p_rhos)
        tmp_this.ir_yield_curves.extend(p_ir_yield_curves)
        tmp_this.asset_yield_curves.extend(p_asset_yield_curves)
        tmp_this.volatility_curves.extend(p_volatility_curves)
        tmp_this.corr_matrix.CopyFrom(p_corr_matrix)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#HestonStochLocalVolModel
def dqCreateProtoHestonStochLocalVolModel(p_as_of_date, p_initial_asset_price, p_ir_yield_curve, p_asset_yield_curve, p_vol_surf, p_heston_process, p_mixing):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_initial_asset_price: double
        3. p_ir_yield_curve: dqproto.IrYieldCurve
        4. p_asset_yield_curve: dqproto.AssetYieldCurve
        5. p_vol_surf: dqproto.VolatilitySurface
        6. p_heston_process: dqproto.HestonStochVolProcess
        7. p_mixing: double
    @return:
        dqproto.HestonStochLocalVolModel
    '''
    try:
        tmp_this= HestonStochLocalVolModel()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.initial_asset_price=p_initial_asset_price
        tmp_this.ir_yield_curve.CopyFrom(p_ir_yield_curve)
        tmp_this.asset_yield_curve.CopyFrom(p_asset_yield_curve)
        tmp_this.vol_surf.CopyFrom(p_vol_surf)
        tmp_this.heston_process.CopyFrom(p_heston_process)
        tmp_this.mixing=p_mixing
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Sensitivity.Data
def dqCreateProtoSensitivity_Data(p_value, p_term_bucket_name, p_strike_bucket_name):
    '''
    @args:
        1. p_value: dqproto.Vector
        2. p_term_bucket_name: string
        3. p_strike_bucket_name: string
    @return:
        dqproto.Sensitivity.Data
    '''
    try:
        tmp_this= Sensitivity.Data()
        tmp_this.value.extend(p_value)
        tmp_this.term_bucket_name.extend(p_term_bucket_name)
        tmp_this.strike_bucket_name.extend(p_strike_bucket_name)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Sensitivity.RiskFactorData
def dqCreateProtoSensitivity_RiskFactorData(p_risk_factor, p_data):
    '''
    @args:
        1. p_risk_factor: string
        2. p_data: dqproto.Data
    @return:
        dqproto.Sensitivity.RiskFactorData
    '''
    try:
        tmp_this= Sensitivity.RiskFactorData()
        tmp_this.risk_factor=p_risk_factor
        tmp_this.data.CopyFrom(p_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Sensitivity.RiskClassData
def dqCreateProtoSensitivity_RiskClassData(p_risk_class, p_data):
    '''
    @args:
        1. p_risk_class: string
        2. p_data: dqproto.RiskFactorData
    @return:
        dqproto.Sensitivity.RiskClassData
    '''
    try:
        tmp_this= Sensitivity.RiskClassData()
        tmp_this.risk_class=p_risk_class
        tmp_this.data.extend(p_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Sensitivity.RiskData
def dqCreateProtoSensitivity_RiskData(p_risk, p_data):
    '''
    @args:
        1. p_risk: string
        2. p_data: dqproto.RiskClassData
    @return:
        dqproto.Sensitivity.RiskData
    '''
    try:
        tmp_this= Sensitivity.RiskData()
        tmp_this.risk=p_risk
        tmp_this.data.extend(p_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Sensitivity
def dqCreateProtoSensitivity(p_data):
    '''
    @args:
        1. p_data: dqproto.Sensitivity.RiskData
    @return:
        dqproto.Sensitivity
    '''
    try:
        tmp_this= Sensitivity()
        tmp_this.data.extend(p_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CouponFlowResult
def dqCreateProtoCouponFlowResult(p_start_dates, p_end_dates, p_fixing_dates, p_accruals, p_coupon_rate, p_discount_factor, p_cash_flow, p_discounted_cash_flow, p_payment_date, p_fixing_rates, p_nominal):
    '''
    @args:
        1. p_start_dates: dqproto.Date
        2. p_end_dates: dqproto.Date
        3. p_fixing_dates: dqproto.Date
        4. p_accruals: dqproto.Vector
        5. p_coupon_rate: double
        6. p_discount_factor: double
        7. p_cash_flow: double
        8. p_discounted_cash_flow: double
        9. p_payment_date: dqproto.Date
        10. p_fixing_rates: dqproto.Vector
        11. p_nominal: double
    @return:
        dqproto.CouponFlowResult
    '''
    try:
        tmp_this= CouponFlowResult()
        tmp_this.start_dates.extend(p_start_dates)
        tmp_this.end_dates.extend(p_end_dates)
        tmp_this.fixing_dates.extend(p_fixing_dates)
        tmp_this.accruals.CopyFrom(p_accruals)
        tmp_this.coupon_rate=p_coupon_rate
        tmp_this.discount_factor=p_discount_factor
        tmp_this.cash_flow=p_cash_flow
        tmp_this.discounted_cash_flow=p_discounted_cash_flow
        tmp_this.payment_date.CopyFrom(p_payment_date)
        tmp_this.fixing_rates.CopyFrom(p_fixing_rates)
        tmp_this.nominal=p_nominal
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PrincipleFlowResult
def dqCreateProtoPrincipleFlowResult(p_discount_factor, p_cash_flow, p_discounted_cash_flow, p_payment_date):
    '''
    @args:
        1. p_discount_factor: double
        2. p_cash_flow: double
        3. p_discounted_cash_flow: double
        4. p_payment_date: dqproto.Date
    @return:
        dqproto.PrincipleFlowResult
    '''
    try:
        tmp_this= PrincipleFlowResult()
        tmp_this.discount_factor=p_discount_factor
        tmp_this.cash_flow=p_cash_flow
        tmp_this.discounted_cash_flow=p_discounted_cash_flow
        tmp_this.payment_date.CopyFrom(p_payment_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CashFlowResults
def dqCreateProtoCashFlowResults(p_npv_pay_flows, p_npv_rec_flows, p_cpn_pay_flows, p_cpn_rec_flows, p_principle_pay_flows, p_principle_rec_flows, p_pay_currency, p_rec_currency):
    '''
    @args:
        1. p_npv_pay_flows: double
        2. p_npv_rec_flows: double
        3. p_cpn_pay_flows: dqproto.CouponFlowResult
        4. p_cpn_rec_flows: dqproto.CouponFlowResult
        5. p_principle_pay_flows: dqproto.PrincipleFlowResult
        6. p_principle_rec_flows: dqproto.PrincipleFlowResult
        7. p_pay_currency: string
        8. p_rec_currency: string
    @return:
        dqproto.CashFlowResults
    '''
    try:
        tmp_this= CashFlowResults()
        tmp_this.npv_pay_flows=p_npv_pay_flows
        tmp_this.npv_rec_flows=p_npv_rec_flows
        tmp_this.cpn_pay_flows.extend(p_cpn_pay_flows)
        tmp_this.cpn_rec_flows.extend(p_cpn_rec_flows)
        tmp_this.principle_pay_flows.extend(p_principle_pay_flows)
        tmp_this.principle_rec_flows.extend(p_principle_rec_flows)
        tmp_this.pay_currency=p_pay_currency
        tmp_this.rec_currency=p_rec_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PricingResults
def dqCreateProtoPricingResults(p_present_value, p_cash_value, p_sensitivity, p_cash_flow_results, p_currency, p_specific_pricing_results):
    '''
    @args:
        1. p_present_value: double
        2. p_cash_value: double
        3. p_sensitivity: dqproto.Sensitivity
        4. p_cash_flow_results: dqproto.CashFlowResults
        5. p_currency: string
        6. p_specific_pricing_results: dqproto.Vector
    @return:
        dqproto.PricingResults
    '''
    try:
        tmp_this= PricingResults()
        tmp_this.present_value=p_present_value
        tmp_this.cash_value=p_cash_value
        tmp_this.sensitivity.CopyFrom(p_sensitivity)
        tmp_this.cash_flow_results.CopyFrom(p_cash_flow_results)
        tmp_this.currency=p_currency
        tmp_this.specific_pricing_results.CopyFrom(p_specific_pricing_results)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Path
def dqCreateProtoPath(p_reference_date, p_time_grid, p_num_assets, p_num_scenarios, p_data):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_time_grid: dqproto.Vector
        3. p_num_assets: int32
        4. p_num_scenarios: int32
        5. p_data: dqproto.Matrix
    @return:
        dqproto.Path
    '''
    try:
        tmp_this= Path()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.time_grid.CopyFrom(p_time_grid)
        tmp_this.num_assets=p_num_assets
        tmp_this.num_scenarios=p_num_scenarios
        tmp_this.data.CopyFrom(p_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InstrumentStatisticsSeries
def dqCreateProtoInstrumentStatisticsSeries(p_ewma_decay_factor, p_time_series, p_period):
    '''
    @args:
        1. p_ewma_decay_factor: double
        2. p_time_series: dqproto.TimeSeries
        3. p_period: dqproto.Period
    @return:
        dqproto.InstrumentStatisticsSeries
    '''
    try:
        tmp_this= InstrumentStatisticsSeries()
        tmp_this.ewma_decay_factor.extend(p_ewma_decay_factor)
        tmp_this.time_series.CopyFrom(p_time_series)
        tmp_this.period.CopyFrom(p_period)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ScnSettings
def dqCreateProtoScnSettings(p_min, p_max, p_size, p_scn_gen_type):
    '''
    @args:
        1. p_min: double
        2. p_max: double
        3. p_size: int32
        4. p_scn_gen_type: int32
    @return:
        dqproto.ScnSettings
    '''
    try:
        tmp_this= ScnSettings()
        tmp_this.min=p_min
        tmp_this.max=p_max
        tmp_this.size=p_size
        tmp_this.scn_gen_type=p_scn_gen_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ScnAnalysisSettings
def dqCreateProtoScnAnalysisSettings(p_scn_analysis_type, p_price_scn_settings, p_vol_scn_settings, p_threading_mode):
    '''
    @args:
        1. p_scn_analysis_type: dqproto.ScnAnalysisType
        2. p_price_scn_settings: dqproto.ScnSettings
        3. p_vol_scn_settings: dqproto.ScnSettings
        4. p_threading_mode: dqproto.ThreadingMode
    @return:
        dqproto.ScnAnalysisSettings
    '''
    try:
        tmp_this= ScnAnalysisSettings()
        tmp_this.scn_analysis_type=p_scn_analysis_type
        tmp_this.price_scn_settings.CopyFrom(p_price_scn_settings)
        tmp_this.vol_scn_settings.CopyFrom(p_vol_scn_settings)
        tmp_this.threading_mode=p_threading_mode
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BlackScholesModelPathBuildingInput
def dqCreateProtoBlackScholesModelPathBuildingInput(p_settings, p_as_of_date, p_sim_sched, p_model, p_path_builder_handle):
    '''
    @args:
        1. p_settings: dqproto.MonteCarloSettings
        2. p_as_of_date: dqproto.Date
        3. p_sim_sched: dqproto.Schedule
        4. p_model: dqproto.GeneralisedBlackScholesModel
        5. p_path_builder_handle: string
    @return:
        dqproto.BlackScholesModelPathBuildingInput
    '''
    try:
        tmp_this= BlackScholesModelPathBuildingInput()
        tmp_this.settings.CopyFrom(p_settings)
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.sim_sched.CopyFrom(p_sim_sched)
        tmp_this.model.CopyFrom(p_model)
        tmp_this.path_builder_handle=p_path_builder_handle
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BlackScholesModelPathBuildingOutput
def dqCreateProtoBlackScholesModelPathBuildingOutput(p_path_builder_handle, p_success, p_err_msg):
    '''
    @args:
        1. p_path_builder_handle: string
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BlackScholesModelPathBuildingOutput
    '''
    try:
        tmp_this= BlackScholesModelPathBuildingOutput()
        tmp_this.path_builder_handle=p_path_builder_handle
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildAssetYieldCurveInput
def dqCreateProtoBuildAssetYieldCurveInput(p_spot, p_discount_curve, p_term_dates, p_future_prices, p_call_price_matrix, p_put_price_matrix, p_strike_matrix):
    '''
    @args:
        1. p_spot: double
        2. p_discount_curve: dqproto.IrYieldCurve
        3. p_term_dates: dqproto.Date
        4. p_future_prices: dqproto.Vector
        5. p_call_price_matrix: dqproto.Vector
        6. p_put_price_matrix: dqproto.Vector
        7. p_strike_matrix: dqproto.Vector
    @return:
        dqproto.BuildAssetYieldCurveInput
    '''
    try:
        tmp_this= BuildAssetYieldCurveInput()
        tmp_this.spot=p_spot
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.term_dates.extend(p_term_dates)
        tmp_this.future_prices.CopyFrom(p_future_prices)
        tmp_this.call_price_matrix.extend(p_call_price_matrix)
        tmp_this.put_price_matrix.extend(p_put_price_matrix)
        tmp_this.strike_matrix.extend(p_strike_matrix)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildAssetYieldCurveOutput
def dqCreateProtoBuildAssetYieldCurveOutput(p_asset_yield_curve, p_success, p_err_msg):
    '''
    @args:
        1. p_asset_yield_curve: dqproto.AssetYieldCurve
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildAssetYieldCurveOutput
    '''
    try:
        tmp_this= BuildAssetYieldCurveOutput()
        tmp_this.asset_yield_curve.CopyFrom(p_asset_yield_curve)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateOptionQuoteMatrixInput
def dqCreateProtoCreateOptionQuoteMatrixInput(p_underlying_name, p_as_of_date, p_exercise_type, p_quotes, p_underlying_price, p_factor):
    '''
    @args:
        1. p_underlying_name: string
        2. p_as_of_date: dqproto.Date
        3. p_exercise_type: dqproto.ExerciseType
        4. p_quotes: dqproto.CreateOptionQuoteMatrixInput.Row
        5. p_underlying_price: double
        6. p_factor: double
    @return:
        dqproto.CreateOptionQuoteMatrixInput
    '''
    try:
        tmp_this= CreateOptionQuoteMatrixInput()
        tmp_this.underlying_name=p_underlying_name
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.exercise_type=p_exercise_type
        tmp_this.quotes.extend(p_quotes)
        tmp_this.underlying_price=p_underlying_price
        tmp_this.factor=p_factor
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateOptionQuoteMatrixInput.Row
def dqCreateProtoCreateOptionQuoteMatrixInput_Row(p_expiry, p_strike, p_payoff_type, p_price):
    '''
    @args:
        1. p_expiry: dqproto.Date
        2. p_strike: double
        3. p_payoff_type: dqproto.PayoffType
        4. p_price: double
    @return:
        dqproto.CreateOptionQuoteMatrixInput.Row
    '''
    try:
        tmp_this= CreateOptionQuoteMatrixInput.Row()
        tmp_this.expiry.CopyFrom(p_expiry)
        tmp_this.strike=p_strike
        tmp_this.payoff_type=p_payoff_type
        tmp_this.price=p_price
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateOptionQuoteMatrixOutput
def dqCreateProtoCreateOptionQuoteMatrixOutput(p_option_quote_matrix, p_success, p_err_msg):
    '''
    @args:
        1. p_option_quote_matrix: dqproto.OptionQuoteMatrix
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateOptionQuoteMatrixOutput
    '''
    try:
        tmp_this= CreateOptionQuoteMatrixOutput()
        tmp_this.option_quote_matrix.CopyFrom(p_option_quote_matrix)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateProxyOptionQuoteMatrixInput
def dqCreateProtoCreateProxyOptionQuoteMatrixInput(p_underlying_name, p_ref_vol_surface, p_ref_underlying_price, p_underlying_price):
    '''
    @args:
        1. p_underlying_name: string
        2. p_ref_vol_surface: dqproto.VolatilitySurface
        3. p_ref_underlying_price: double
        4. p_underlying_price: double
    @return:
        dqproto.CreateProxyOptionQuoteMatrixInput
    '''
    try:
        tmp_this= CreateProxyOptionQuoteMatrixInput()
        tmp_this.underlying_name=p_underlying_name
        tmp_this.ref_vol_surface.CopyFrom(p_ref_vol_surface)
        tmp_this.ref_underlying_price=p_ref_underlying_price
        tmp_this.underlying_price=p_underlying_price
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateProxyOptionQuoteMatrixOutput
def dqCreateProtoCreateProxyOptionQuoteMatrixOutput(p_option_quote_matrix, p_success, p_err_msg):
    '''
    @args:
        1. p_option_quote_matrix: dqproto.OptionQuoteMatrix
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateProxyOptionQuoteMatrixOutput
    '''
    try:
        tmp_this= CreateProxyOptionQuoteMatrixOutput()
        tmp_this.option_quote_matrix.CopyFrom(p_option_quote_matrix)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetVolatilityInput
def dqCreateProtoGetVolatilityInput(p_volatility_surface, p_expiry, p_strike):
    '''
    @args:
        1. p_volatility_surface: dqproto.VolatilitySurface
        2. p_expiry: dqproto.Date
        3. p_strike: dqproto.Vector
    @return:
        dqproto.GetVolatilityInput
    '''
    try:
        tmp_this= GetVolatilityInput()
        tmp_this.volatility_surface.CopyFrom(p_volatility_surface)
        tmp_this.expiry.extend(p_expiry)
        tmp_this.strike.CopyFrom(p_strike)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetVolatilityOutput
def dqCreateProtoGetVolatilityOutput(p_volatility, p_success, p_err_msg):
    '''
    @args:
        1. p_volatility: dqproto.Matrix
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.GetVolatilityOutput
    '''
    try:
        tmp_this= GetVolatilityOutput()
        tmp_this.volatility.CopyFrom(p_volatility)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FlexPricingInput
def dqCreateProtoFlexPricingInput(p_pricing_date, p_spot, p_discount_curve, p_asset_curve, p_vol_surf, p_settings, p_fixing_schedules, p_payment_schedule, p_flex_pricer_handle):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_spot: double
        3. p_discount_curve: dqproto.IrYieldCurve
        4. p_asset_curve: dqproto.DividendCurve
        5. p_vol_surf: dqproto.VolatilitySurface
        6. p_settings: dqproto.PricingSettings
        7. p_fixing_schedules: dqproto.FixingSchedule
        8. p_payment_schedule: dqproto.Schedule
        9. p_flex_pricer_handle: string
    @return:
        dqproto.FlexPricingInput
    '''
    try:
        tmp_this= FlexPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.spot=p_spot
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.asset_curve.CopyFrom(p_asset_curve)
        tmp_this.vol_surf.CopyFrom(p_vol_surf)
        tmp_this.settings.CopyFrom(p_settings)
        tmp_this.fixing_schedules.extend(p_fixing_schedules)
        tmp_this.payment_schedule.CopyFrom(p_payment_schedule)
        tmp_this.flex_pricer_handle=p_flex_pricer_handle
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FlexPricingOutput
def dqCreateProtoFlexPricingOutput(p_flex_pricer_handle, p_success, p_err_msg):
    '''
    @args:
        1. p_flex_pricer_handle: string
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FlexPricingOutput
    '''
    try:
        tmp_this= FlexPricingOutput()
        tmp_this.flex_pricer_handle=p_flex_pricer_handle
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FlexGetFixingInput
def dqCreateProtoFlexGetFixingInput(p_flex_pricer_handle, p_ith_sim, p_fixing_date):
    '''
    @args:
        1. p_flex_pricer_handle: string
        2. p_ith_sim: int32
        3. p_fixing_date: dqproto.Date
    @return:
        dqproto.FlexGetFixingInput
    '''
    try:
        tmp_this= FlexGetFixingInput()
        tmp_this.flex_pricer_handle=p_flex_pricer_handle
        tmp_this.ith_sim=p_ith_sim
        tmp_this.fixing_date.CopyFrom(p_fixing_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FlexGetFixingOutput
def dqCreateProtoFlexGetFixingOutput(p_fixing, p_success, p_err_msg):
    '''
    @args:
        1. p_fixing: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FlexGetFixingOutput
    '''
    try:
        tmp_this= FlexGetFixingOutput()
        tmp_this.fixing=p_fixing
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FlexGetDiscountFactorInput
def dqCreateProtoFlexGetDiscountFactorInput(p_flex_pricer_handle, p_discount_date):
    '''
    @args:
        1. p_flex_pricer_handle: string
        2. p_discount_date: dqproto.Date
    @return:
        dqproto.FlexGetDiscountFactorInput
    '''
    try:
        tmp_this= FlexGetDiscountFactorInput()
        tmp_this.flex_pricer_handle=p_flex_pricer_handle
        tmp_this.discount_date.CopyFrom(p_discount_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FlexGetDiscountFactorOutput
def dqCreateProtoFlexGetDiscountFactorOutput(p_discount_factor, p_success, p_err_msg):
    '''
    @args:
        1. p_discount_factor: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FlexGetDiscountFactorOutput
    '''
    try:
        tmp_this= FlexGetDiscountFactorOutput()
        tmp_this.discount_factor=p_discount_factor
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetDiscountFactorInput
def dqCreateProtoGetDiscountFactorInput(p_term_dates, p_ir_yield_curve):
    '''
    @args:
        1. p_term_dates: dqproto.Date
        2. p_ir_yield_curve: dqproto.IrYieldCurve
    @return:
        dqproto.GetDiscountFactorInput
    '''
    try:
        tmp_this= GetDiscountFactorInput()
        tmp_this.term_dates.extend(p_term_dates)
        tmp_this.ir_yield_curve.CopyFrom(p_ir_yield_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetDiscountFactorOutput
def dqCreateProtoGetDiscountFactorOutput(p_discount_factors, p_success, p_err_msg):
    '''
    @args:
        1. p_discount_factors: dqproto.Vector
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.GetDiscountFactorOutput
    '''
    try:
        tmp_this= GetDiscountFactorOutput()
        tmp_this.discount_factors.CopyFrom(p_discount_factors)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetZeroRateInput
def dqCreateProtoGetZeroRateInput(p_term_dates, p_ir_yield_curve):
    '''
    @args:
        1. p_term_dates: dqproto.Date
        2. p_ir_yield_curve: dqproto.IrYieldCurve
    @return:
        dqproto.GetZeroRateInput
    '''
    try:
        tmp_this= GetZeroRateInput()
        tmp_this.term_dates.extend(p_term_dates)
        tmp_this.ir_yield_curve.CopyFrom(p_ir_yield_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetZeroRateOutput
def dqCreateProtoGetZeroRateOutput(p_zero_rate, p_success, p_err_msg):
    '''
    @args:
        1. p_zero_rate: dqproto.Vector
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.GetZeroRateOutput
    '''
    try:
        tmp_this= GetZeroRateOutput()
        tmp_this.zero_rate.CopyFrom(p_zero_rate)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetFwdRateInput
def dqCreateProtoGetFwdRateInput(p_term_dates, p_ir_yield_curve, p_tenor):
    '''
    @args:
        1. p_term_dates: dqproto.Date
        2. p_ir_yield_curve: dqproto.IrYieldCurve
        3. p_tenor: double
    @return:
        dqproto.GetFwdRateInput
    '''
    try:
        tmp_this= GetFwdRateInput()
        tmp_this.term_dates.extend(p_term_dates)
        tmp_this.ir_yield_curve.CopyFrom(p_ir_yield_curve)
        tmp_this.tenor=p_tenor
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetFwdRateOutput
def dqCreateProtoGetFwdRateOutput(p_fwd_rates, p_success, p_err_msg):
    '''
    @args:
        1. p_fwd_rates: dqproto.Vector
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.GetFwdRateOutput
    '''
    try:
        tmp_this= GetFwdRateOutput()
        tmp_this.fwd_rates.CopyFrom(p_fwd_rates)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetSurvivalProbabilityInput
def dqCreateProtoGetSurvivalProbabilityInput(p_term_dates, p_credit_curve):
    '''
    @args:
        1. p_term_dates: dqproto.Date
        2. p_credit_curve: dqproto.CreditCurve
    @return:
        dqproto.GetSurvivalProbabilityInput
    '''
    try:
        tmp_this= GetSurvivalProbabilityInput()
        tmp_this.term_dates.extend(p_term_dates)
        tmp_this.credit_curve.CopyFrom(p_credit_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetSurvivalProbabilityOutput
def dqCreateProtoGetSurvivalProbabilityOutput(p_survival_probabilities, p_success, p_err_msg):
    '''
    @args:
        1. p_survival_probabilities: dqproto.Vector
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.GetSurvivalProbabilityOutput
    '''
    try:
        tmp_this= GetSurvivalProbabilityOutput()
        tmp_this.survival_probabilities.CopyFrom(p_survival_probabilities)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetCreditSpreadInput
def dqCreateProtoGetCreditSpreadInput(p_term_dates, p_credit_curve):
    '''
    @args:
        1. p_term_dates: dqproto.Date
        2. p_credit_curve: dqproto.CreditCurve
    @return:
        dqproto.GetCreditSpreadInput
    '''
    try:
        tmp_this= GetCreditSpreadInput()
        tmp_this.term_dates.extend(p_term_dates)
        tmp_this.credit_curve.CopyFrom(p_credit_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetCreditSpreadOutput
def dqCreateProtoGetCreditSpreadOutput(p_credit_spreads, p_success, p_err_msg):
    '''
    @args:
        1. p_credit_spreads: dqproto.Vector
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.GetCreditSpreadOutput
    '''
    try:
        tmp_this= GetCreditSpreadOutput()
        tmp_this.credit_spreads.CopyFrom(p_credit_spreads)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetDividendInput
def dqCreateProtoGetDividendInput(p_term_dates, p_dividend_curve):
    '''
    @args:
        1. p_term_dates: dqproto.Date
        2. p_dividend_curve: dqproto.DividendCurve
    @return:
        dqproto.GetDividendInput
    '''
    try:
        tmp_this= GetDividendInput()
        tmp_this.term_dates.extend(p_term_dates)
        tmp_this.dividend_curve.CopyFrom(p_dividend_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetDividendOutput
def dqCreateProtoGetDividendOutput(p_dividends, p_success, p_err_msg):
    '''
    @args:
        1. p_dividends: dqproto.Vector
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.GetDividendOutput
    '''
    try:
        tmp_this= GetDividendOutput()
        tmp_this.dividends.CopyFrom(p_dividends)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ImpliedVolatilityCalculationInput
def dqCreateProtoImpliedVolatilityCalculationInput(p_calculation_date, p_underlying_price, p_discount_curve, p_asset_curve, p_settings, p_option_price, p_payoff_type, p_exercise_type, p_expiry_date, p_strike):
    '''
    @args:
        1. p_calculation_date: dqproto.Date
        2. p_underlying_price: double
        3. p_discount_curve: dqproto.IrYieldCurve
        4. p_asset_curve: dqproto.DividendCurve
        5. p_settings: dqproto.PricingSettings
        6. p_option_price: double
        7. p_payoff_type: dqproto.PayoffType
        8. p_exercise_type: dqproto.ExerciseType
        9. p_expiry_date: dqproto.Date
        10. p_strike: double
    @return:
        dqproto.ImpliedVolatilityCalculationInput
    '''
    try:
        tmp_this= ImpliedVolatilityCalculationInput()
        tmp_this.calculation_date.CopyFrom(p_calculation_date)
        tmp_this.underlying_price=p_underlying_price
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.asset_curve.CopyFrom(p_asset_curve)
        tmp_this.settings.CopyFrom(p_settings)
        tmp_this.option_price=p_option_price
        tmp_this.payoff_type=p_payoff_type
        tmp_this.exercise_type=p_exercise_type
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.strike=p_strike
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ImpliedVolatilityCalculationOutput
def dqCreateProtoImpliedVolatilityCalculationOutput(p_implied_volatility, p_success, p_err_msg):
    '''
    @args:
        1. p_implied_volatility: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.ImpliedVolatilityCalculationOutput
    '''
    try:
        tmp_this= ImpliedVolatilityCalculationOutput()
        tmp_this.implied_volatility=p_implied_volatility
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#AtmStrikeCalculationInput
def dqCreateProtoAtmStrikeCalculationInput(p_atm_type, p_expiry_date, p_underlying_price, p_discount_curve, p_fwd_curve, p_volatility_surface):
    '''
    @args:
        1. p_atm_type: dqproto.AtmType
        2. p_expiry_date: dqproto.Date
        3. p_underlying_price: double
        4. p_discount_curve: dqproto.IrYieldCurve
        5. p_fwd_curve: dqproto.DividendCurve
        6. p_volatility_surface: dqproto.VolatilitySurface
    @return:
        dqproto.AtmStrikeCalculationInput
    '''
    try:
        tmp_this= AtmStrikeCalculationInput()
        tmp_this.atm_type=p_atm_type
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.underlying_price=p_underlying_price
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.fwd_curve.CopyFrom(p_fwd_curve)
        tmp_this.volatility_surface.CopyFrom(p_volatility_surface)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#AtmStrikeCalculationOutput
def dqCreateProtoAtmStrikeCalculationOutput(p_strike, p_success, p_err_msg):
    '''
    @args:
        1. p_strike: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.AtmStrikeCalculationOutput
    '''
    try:
        tmp_this= AtmStrikeCalculationOutput()
        tmp_this.strike=p_strike
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#DeltaToStrikeCalculationInput
def dqCreateProtoDeltaToStrikeCalculationInput(p_delta_type, p_delta, p_option_type, p_expiry_date, p_underlying_price, p_discount_curve, p_fwd_curve, p_volatility_surface):
    '''
    @args:
        1. p_delta_type: dqproto.DeltaType
        2. p_delta: double
        3. p_option_type: dqproto.PayoffType
        4. p_expiry_date: dqproto.Date
        5. p_underlying_price: double
        6. p_discount_curve: dqproto.IrYieldCurve
        7. p_fwd_curve: dqproto.DividendCurve
        8. p_volatility_surface: dqproto.VolatilitySurface
    @return:
        dqproto.DeltaToStrikeCalculationInput
    '''
    try:
        tmp_this= DeltaToStrikeCalculationInput()
        tmp_this.delta_type=p_delta_type
        tmp_this.delta=p_delta
        tmp_this.option_type=p_option_type
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.underlying_price=p_underlying_price
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.fwd_curve.CopyFrom(p_fwd_curve)
        tmp_this.volatility_surface.CopyFrom(p_volatility_surface)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#DeltaToStrikeCalculationOutput
def dqCreateProtoDeltaToStrikeCalculationOutput(p_strike, p_success, p_err_msg):
    '''
    @args:
        1. p_strike: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.DeltaToStrikeCalculationOutput
    '''
    try:
        tmp_this= DeltaToStrikeCalculationOutput()
        tmp_this.strike=p_strike
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PmMarketConventions
def dqCreateProtoPmMarketConventions(p_atm_type, p_short_delta_type, p_long_delta_type, p_short_delta_cutoff, p_risk_reversal, p_smile_quote_type):
    '''
    @args:
        1. p_atm_type: dqproto.AtmType
        2. p_short_delta_type: dqproto.DeltaType
        3. p_long_delta_type: dqproto.DeltaType
        4. p_short_delta_cutoff: dqproto.Period
        5. p_risk_reversal: dqproto.RiskReversal
        6. p_smile_quote_type: dqproto.SmileQuoteType
    @return:
        dqproto.PmMarketConventions
    '''
    try:
        tmp_this= PmMarketConventions()
        tmp_this.atm_type=p_atm_type
        tmp_this.short_delta_type=p_short_delta_type
        tmp_this.long_delta_type=p_long_delta_type
        tmp_this.short_delta_cutoff.CopyFrom(p_short_delta_cutoff)
        tmp_this.risk_reversal=p_risk_reversal
        tmp_this.smile_quote_type=p_smile_quote_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PmParRateCurve.Pillar
def dqCreateProtoPmParRateCurve_Pillar(p_instrument_name, p_instrument_type, p_instrument_term, p_instrument_rate):
    '''
    @args:
        1. p_instrument_name: string
        2. p_instrument_type: dqproto.InstrumentType
        3. p_instrument_term: dqproto.Period
        4. p_instrument_rate: double
    @return:
        dqproto.PmParRateCurve.Pillar
    '''
    try:
        tmp_this= PmParRateCurve.Pillar()
        tmp_this.instrument_name=p_instrument_name
        tmp_this.instrument_type=p_instrument_type
        tmp_this.instrument_term.CopyFrom(p_instrument_term)
        tmp_this.instrument_rate=p_instrument_rate
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PmParRateCurve
def dqCreateProtoPmParRateCurve(p_reference_date, p_currency, p_name, p_pillars):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_currency: string
        3. p_name: string
        4. p_pillars: dqproto.PmParRateCurve.Pillar
    @return:
        dqproto.PmParRateCurve
    '''
    try:
        tmp_this= PmParRateCurve()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.currency=p_currency
        tmp_this.name=p_name
        tmp_this.pillars.extend(p_pillars)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmMktDataSet
def dqCreateProtoCmMktDataSet(p_as_of_date, p_discount_curve, p_dividend_curve, p_underlying_price, p_vol_surf, p_quanto_discount_curve, p_quanto_fx_vol_curve, p_quanto_correlation, p_underlying):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_discount_curve: dqproto.IrYieldCurve
        3. p_dividend_curve: dqproto.DividendCurve
        4. p_underlying_price: double
        5. p_vol_surf: dqproto.VolatilitySurface
        6. p_quanto_discount_curve: dqproto.IrYieldCurve
        7. p_quanto_fx_vol_curve: dqproto.VolatilityCurve
        8. p_quanto_correlation: double
        9. p_underlying: string
    @return:
        dqproto.CmMktDataSet
    '''
    try:
        tmp_this= CmMktDataSet()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.dividend_curve.CopyFrom(p_dividend_curve)
        tmp_this.underlying_price=p_underlying_price
        tmp_this.vol_surf.CopyFrom(p_vol_surf)
        tmp_this.quanto_discount_curve.CopyFrom(p_quanto_discount_curve)
        tmp_this.quanto_fx_vol_curve.CopyFrom(p_quanto_fx_vol_curve)
        tmp_this.quanto_correlation=p_quanto_correlation
        tmp_this.underlying=p_underlying
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmRiskSettings
def dqCreateProtoCmRiskSettings(p_ir_curve_settings, p_price_settings, p_vol_settings, p_price_vol_settings, p_theta_settings, p_dividend_curve_settings):
    '''
    @args:
        1. p_ir_curve_settings: dqproto.IrCurveRiskSettings
        2. p_price_settings: dqproto.PriceRiskSettings
        3. p_vol_settings: dqproto.VolRiskSettings
        4. p_price_vol_settings: dqproto.PriceVolRiskSettings
        5. p_theta_settings: dqproto.ThetaRiskSettings
        6. p_dividend_curve_settings: dqproto.DividendCurveRiskSettings
    @return:
        dqproto.CmRiskSettings
    '''
    try:
        tmp_this= CmRiskSettings()
        tmp_this.ir_curve_settings.CopyFrom(p_ir_curve_settings)
        tmp_this.price_settings.CopyFrom(p_price_settings)
        tmp_this.vol_settings.CopyFrom(p_vol_settings)
        tmp_this.price_vol_settings.CopyFrom(p_price_vol_settings)
        tmp_this.theta_settings.CopyFrom(p_theta_settings)
        tmp_this.dividend_curve_settings.CopyFrom(p_dividend_curve_settings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PmYieldCurveBuildingInput
def dqCreateProtoPmYieldCurveBuildingInput(p_reference_date, p_par_curve, p_discount_curve, p_spot_price, p_calc_jacobian, p_day_count, p_interp_method, p_extrap_method, p_curve_type, p_pm_tempalte, p_curve_name, p_shift, p_method, p_mode):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_par_curve: dqproto.PmParRateCurve
        3. p_discount_curve: dqproto.IrYieldCurve
        4. p_spot_price: double
        5. p_calc_jacobian: bool
        6. p_day_count: dqproto.DayCountConvention
        7. p_interp_method: dqproto.InterpMethod
        8. p_extrap_method: dqproto.ExtrapMethod
        9. p_curve_type: dqproto.IrYieldCurveType
        10. p_pm_tempalte: dqproto.PmCashTemplate
        11. p_curve_name: string
        12. p_shift: double
        13. p_method: dqproto.FiniteDifferenceMethod
        14. p_mode: dqproto.ThreadingMode
    @return:
        dqproto.PmYieldCurveBuildingInput
    '''
    try:
        tmp_this= PmYieldCurveBuildingInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.par_curve.CopyFrom(p_par_curve)
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.spot_price=p_spot_price
        tmp_this.calc_jacobian=p_calc_jacobian
        tmp_this.day_count=p_day_count
        tmp_this.interp_method=p_interp_method
        tmp_this.extrap_method=p_extrap_method
        tmp_this.curve_type=p_curve_type
        tmp_this.pm_tempalte.CopyFrom(p_pm_tempalte)
        tmp_this.curve_name=p_curve_name
        tmp_this.shift=p_shift
        tmp_this.method=p_method
        tmp_this.mode=p_mode
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PmYieldCurveBuildingOutput
def dqCreateProtoPmYieldCurveBuildingOutput(p_yield_curve, p_success, p_err_msg):
    '''
    @args:
        1. p_yield_curve: dqproto.DividendCurve
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.PmYieldCurveBuildingOutput
    '''
    try:
        tmp_this= PmYieldCurveBuildingOutput()
        tmp_this.yield_curve.CopyFrom(p_yield_curve)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmVolatilitySurfaceBuildingInput
def dqCreateProtoCmVolatilitySurfaceBuildingInput(p_reference_date, p_definition, p_quotes, p_underlying_prices, p_discount_curve, p_fwd_curve, p_build_settings, p_underlying):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_definition: dqproto.VolatilitySurfaceDefinition
        3. p_quotes: dqproto.OptionQuoteMatrix
        4. p_underlying_prices: dqproto.Vector
        5. p_discount_curve: dqproto.IrYieldCurve
        6. p_fwd_curve: dqproto.DividendCurve
        7. p_build_settings: dqproto.VolatilitySurfaceBuildSettings
        8. p_underlying: string
    @return:
        dqproto.CmVolatilitySurfaceBuildingInput
    '''
    try:
        tmp_this= CmVolatilitySurfaceBuildingInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.definition.CopyFrom(p_definition)
        tmp_this.quotes.CopyFrom(p_quotes)
        tmp_this.underlying_prices.CopyFrom(p_underlying_prices)
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.fwd_curve.CopyFrom(p_fwd_curve)
        tmp_this.build_settings.CopyFrom(p_build_settings)
        tmp_this.underlying=p_underlying
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmVolatilitySurfaceBuildingOutput
def dqCreateProtoCmVolatilitySurfaceBuildingOutput(p_vol_surf, p_success, p_err_msg):
    '''
    @args:
        1. p_vol_surf: dqproto.VolatilitySurface
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CmVolatilitySurfaceBuildingOutput
    '''
    try:
        tmp_this= CmVolatilitySurfaceBuildingOutput()
        tmp_this.vol_surf.CopyFrom(p_vol_surf)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PmVolatilitySurfaceBuildingInput
def dqCreateProtoPmVolatilitySurfaceBuildingInput(p_reference_date, p_definition, p_quotes, p_underlying_price, p_discount_curve, p_fwd_curve, p_build_settings, p_market_conventions, p_spot_template, p_underlying, p_vol_surf):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_definition: dqproto.VolatilitySurfaceDefinition
        3. p_quotes: dqproto.OptionQuoteMatrix
        4. p_underlying_price: double
        5. p_discount_curve: dqproto.IrYieldCurve
        6. p_fwd_curve: dqproto.DividendCurve
        7. p_build_settings: dqproto.VolatilitySurfaceBuildSettings
        8. p_market_conventions: dqproto.PmMarketConventions
        9. p_spot_template: dqproto.PmCashTemplate
        10. p_underlying: string
        11. p_vol_surf: string
    @return:
        dqproto.PmVolatilitySurfaceBuildingInput
    '''
    try:
        tmp_this= PmVolatilitySurfaceBuildingInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.definition.CopyFrom(p_definition)
        tmp_this.quotes.CopyFrom(p_quotes)
        tmp_this.underlying_price=p_underlying_price
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.fwd_curve.CopyFrom(p_fwd_curve)
        tmp_this.build_settings.CopyFrom(p_build_settings)
        tmp_this.market_conventions.CopyFrom(p_market_conventions)
        tmp_this.spot_template.CopyFrom(p_spot_template)
        tmp_this.underlying=p_underlying
        tmp_this.vol_surf=p_vol_surf
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PmVolatilitySurfaceBuildingOutput
def dqCreateProtoPmVolatilitySurfaceBuildingOutput(p_vol_surf, p_success, p_err_msg):
    '''
    @args:
        1. p_vol_surf: dqproto.VolatilitySurface
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.PmVolatilitySurfaceBuildingOutput
    '''
    try:
        tmp_this= PmVolatilitySurfaceBuildingOutput()
        tmp_this.vol_surf.CopyFrom(p_vol_surf)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmPricingInput
def dqCreateProtoCmPricingInput(p_pricing_date, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin, p_scn_settings):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_mkt_data: dqproto.CmMktDataSet
        3. p_pricing_settings: dqproto.PricingSettings
        4. p_risk_settings: dqproto.CmRiskSettings
        5. p_use_binary: bool
        6. p_instrument_bin: bytes
        7. p_mkt_data_bin: bytes
        8. p_pricing_settings_bin: bytes
        9. p_risk_settings_bin: bytes
        10. p_scn_settings: dqproto.ScnAnalysisSettings
    @return:
        dqproto.CmPricingInput
    '''
    try:
        tmp_this= CmPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        tmp_this.scn_settings.CopyFrom(p_scn_settings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmPricingOutput
def dqCreateProtoCmPricingOutput(p_results, p_success, p_err_msg, p_scn_results, p_scn_prices, p_scn_vols):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
        4. p_scn_results: dqproto.Matrix
        5. p_scn_prices: dqproto.Vector
        6. p_scn_vols: dqproto.Vector
    @return:
        dqproto.CmPricingOutput
    '''
    try:
        tmp_this= CmPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        tmp_this.scn_results.CopyFrom(p_scn_results)
        tmp_this.scn_prices.CopyFrom(p_scn_prices)
        tmp_this.scn_vols.CopyFrom(p_scn_vols)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmEuropeanOptionPricingInput
def dqCreateProtoCmEuropeanOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.EuropeanOption
    @return:
        dqproto.CmEuropeanOptionPricingInput
    '''
    try:
        tmp_this= CmEuropeanOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmAmericanOptionPricingInput
def dqCreateProtoCmAmericanOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.AmericanOption
    @return:
        dqproto.CmAmericanOptionPricingInput
    '''
    try:
        tmp_this= CmAmericanOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmAsianOptionPricingInput
def dqCreateProtoCmAsianOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.AsianOption
    @return:
        dqproto.CmAsianOptionPricingInput
    '''
    try:
        tmp_this= CmAsianOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmDigitalOptionPricingInput
def dqCreateProtoCmDigitalOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.DigitalOption
    @return:
        dqproto.CmDigitalOptionPricingInput
    '''
    try:
        tmp_this= CmDigitalOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmOneTouchOptionPricingInput
def dqCreateProtoCmOneTouchOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.OneTouchOption
    @return:
        dqproto.CmOneTouchOptionPricingInput
    '''
    try:
        tmp_this= CmOneTouchOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmDoubleTouchOptionPricingInput
def dqCreateProtoCmDoubleTouchOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.DoubleTouchOption
    @return:
        dqproto.CmDoubleTouchOptionPricingInput
    '''
    try:
        tmp_this= CmDoubleTouchOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmSingleBarrierOptionPricingInput
def dqCreateProtoCmSingleBarrierOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.SingleBarrierOption
    @return:
        dqproto.CmSingleBarrierOptionPricingInput
    '''
    try:
        tmp_this= CmSingleBarrierOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmDoubleBarrierOptionPricingInput
def dqCreateProtoCmDoubleBarrierOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.DoubleBarrierOption
    @return:
        dqproto.CmDoubleBarrierOptionPricingInput
    '''
    try:
        tmp_this= CmDoubleBarrierOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmSingleSharkFinOptionPricingInput
def dqCreateProtoCmSingleSharkFinOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.SingleSharkFinOption
    @return:
        dqproto.CmSingleSharkFinOptionPricingInput
    '''
    try:
        tmp_this= CmSingleSharkFinOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmDoubleSharkFinOptionPricingInput
def dqCreateProtoCmDoubleSharkFinOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.DoubleSharkFinOption
    @return:
        dqproto.CmDoubleSharkFinOptionPricingInput
    '''
    try:
        tmp_this= CmDoubleSharkFinOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmPingPongOptionPricingInput
def dqCreateProtoCmPingPongOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.PingPongOption
    @return:
        dqproto.CmPingPongOptionPricingInput
    '''
    try:
        tmp_this= CmPingPongOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmAirbagOptionPricingInput
def dqCreateProtoCmAirbagOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.AirbagOption
    @return:
        dqproto.CmAirbagOptionPricingInput
    '''
    try:
        tmp_this= CmAirbagOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmRangeAccrualOptionPricingInput
def dqCreateProtoCmRangeAccrualOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.RangeAccrualOption
    @return:
        dqproto.CmRangeAccrualOptionPricingInput
    '''
    try:
        tmp_this= CmRangeAccrualOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmPhoenixAutoCallableNotePricingInput
def dqCreateProtoCmPhoenixAutoCallableNotePricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.PhoenixAutoCallableNote
    @return:
        dqproto.CmPhoenixAutoCallableNotePricingInput
    '''
    try:
        tmp_this= CmPhoenixAutoCallableNotePricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CmSnowballAutoCallableNotePricingInput
def dqCreateProtoCmSnowballAutoCallableNotePricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.CmPricingInput
        2. p_instrument: dqproto.SnowballAutoCallableNote
    @return:
        dqproto.CmSnowballAutoCallableNotePricingInput
    '''
    try:
        tmp_this= CmSnowballAutoCallableNotePricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PmCashTemplate
def dqCreateProtoPmCashTemplate(p_name, p_start_delay, p_delivery_day_convention, p_calendar, p_day_count):
    '''
    @args:
        1. p_name: string
        2. p_start_delay: int32
        3. p_delivery_day_convention: dqproto.BusinessDayConvention
        4. p_calendar: string
        5. p_day_count: dqproto.DayCountConvention
    @return:
        dqproto.PmCashTemplate
    '''
    try:
        tmp_this= PmCashTemplate()
        tmp_this.name=p_name
        tmp_this.start_delay=p_start_delay
        tmp_this.delivery_day_convention=p_delivery_day_convention
        tmp_this.calendar.extend(p_calendar)
        tmp_this.day_count=p_day_count
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PmCashTemplateList
def dqCreateProtoPmCashTemplateList(p_pm_cash_template):
    '''
    @args:
        1. p_pm_cash_template: dqproto.PmCashTemplate
    @return:
        dqproto.PmCashTemplateList
    '''
    try:
        tmp_this= PmCashTemplateList()
        tmp_this.pm_cash_template.extend(p_pm_cash_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditParCurve.Pillar
def dqCreateProtoCreditParCurve_Pillar(p_instrument_name, p_instrument_type, p_maturity, p_quote, p_start_convention):
    '''
    @args:
        1. p_instrument_name: string
        2. p_instrument_type: dqproto.InstrumentType
        3. p_maturity: dqproto.Period
        4. p_quote: double
        5. p_start_convention: dqproto.InstrumentStartConvention
    @return:
        dqproto.CreditParCurve.Pillar
    '''
    try:
        tmp_this= CreditParCurve.Pillar()
        tmp_this.instrument_name=p_instrument_name
        tmp_this.instrument_type=p_instrument_type
        tmp_this.maturity.CopyFrom(p_maturity)
        tmp_this.quote=p_quote
        tmp_this.start_convention=p_start_convention
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditParCurve
def dqCreateProtoCreditParCurve(p_reference_date, p_currency, p_pillars, p_name):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_currency: string
        3. p_pillars: dqproto.CreditParCurve.Pillar
        4. p_name: string
    @return:
        dqproto.CreditParCurve
    '''
    try:
        tmp_this= CreditParCurve()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.currency=p_currency
        tmp_this.pillars.extend(p_pillars)
        tmp_this.name=p_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditCurveBuildSettings
def dqCreateProtoCreditCurveBuildSettings(p_curve_name, p_discount_curve, p_forward_curve):
    '''
    @args:
        1. p_curve_name: string
        2. p_discount_curve: dqproto.IrYieldCurve
        3. p_forward_curve: dqproto.IrYieldCurve
    @return:
        dqproto.CreditCurveBuildSettings
    '''
    try:
        tmp_this= CreditCurveBuildSettings()
        tmp_this.curve_name=p_curve_name
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.forward_curve.CopyFrom(p_forward_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CrRiskSettings
def dqCreateProtoCrRiskSettings(p_ir_curve_settings, p_credit_curve_settings, p_theta_settings):
    '''
    @args:
        1. p_ir_curve_settings: dqproto.IrCurveRiskSettings
        2. p_credit_curve_settings: dqproto.CreditCurveRiskSettings
        3. p_theta_settings: dqproto.ThetaRiskSettings
    @return:
        dqproto.CrRiskSettings
    '''
    try:
        tmp_this= CrRiskSettings()
        tmp_this.ir_curve_settings.CopyFrom(p_ir_curve_settings)
        tmp_this.credit_curve_settings.CopyFrom(p_credit_curve_settings)
        tmp_this.theta_settings.CopyFrom(p_theta_settings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CrMktDataSet
def dqCreateProtoCrMktDataSet(p_as_of_date, p_discount_curve, p_credit_curve):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_discount_curve: dqproto.IrYieldCurve
        3. p_credit_curve: dqproto.CreditCurve
    @return:
        dqproto.CrMktDataSet
    '''
    try:
        tmp_this= CrMktDataSet()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.credit_curve.CopyFrom(p_credit_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CdsPricingSettings
def dqCreateProtoCdsPricingSettings(p_recovery_rate, p_include_settlement_date_flows, p_numerical_fix, p_accrual_bias):
    '''
    @args:
        1. p_recovery_rate: double
        2. p_include_settlement_date_flows: bool
        3. p_numerical_fix: dqproto.NumericalFix
        4. p_accrual_bias: dqproto.AccrualBias
    @return:
        dqproto.CdsPricingSettings
    '''
    try:
        tmp_this= CdsPricingSettings()
        tmp_this.recovery_rate=p_recovery_rate
        tmp_this.include_settlement_date_flows=p_include_settlement_date_flows
        tmp_this.numerical_fix=p_numerical_fix
        tmp_this.accrual_bias=p_accrual_bias
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateCreditParCurveInput.Pillar
def dqCreateProtoCreateCreditParCurveInput_Pillar(p_instrument_name, p_instrument_type, p_maturity, p_quote, p_start_convention):
    '''
    @args:
        1. p_instrument_name: string
        2. p_instrument_type: dqproto.InstrumentType
        3. p_maturity: dqproto.Period
        4. p_quote: double
        5. p_start_convention: dqproto.InstrumentStartConvention
    @return:
        dqproto.CreateCreditParCurveInput.Pillar
    '''
    try:
        tmp_this= CreateCreditParCurveInput.Pillar()
        tmp_this.instrument_name=p_instrument_name
        tmp_this.instrument_type=p_instrument_type
        tmp_this.maturity.CopyFrom(p_maturity)
        tmp_this.quote=p_quote
        tmp_this.start_convention=p_start_convention
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateCreditParCurveInput
def dqCreateProtoCreateCreditParCurveInput(p_reference_date, p_currency, p_pillars, p_name):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_currency: string
        3. p_pillars: dqproto.CreateCreditParCurveInput.Pillar
        4. p_name: string
    @return:
        dqproto.CreateCreditParCurveInput
    '''
    try:
        tmp_this= CreateCreditParCurveInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.currency=p_currency
        tmp_this.pillars.extend(p_pillars)
        tmp_this.name=p_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateCreditParCurveOutput
def dqCreateProtoCreateCreditParCurveOutput(p_par_curve, p_success, p_err_msg):
    '''
    @args:
        1. p_par_curve: dqproto.CreditParCurve
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateCreditParCurveOutput
    '''
    try:
        tmp_this= CreateCreditParCurveOutput()
        tmp_this.par_curve.CopyFrom(p_par_curve)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditCurveBuildingInput
def dqCreateProtoCreditCurveBuildingInput(p_par_curve, p_curve_name, p_as_of_date, p_discount_curve, p_curve_building_method):
    '''
    @args:
        1. p_par_curve: dqproto.CreditParCurve
        2. p_curve_name: string
        3. p_as_of_date: dqproto.Date
        4. p_discount_curve: dqproto.IrYieldCurve
        5. p_curve_building_method: string
    @return:
        dqproto.CreditCurveBuildingInput
    '''
    try:
        tmp_this= CreditCurveBuildingInput()
        tmp_this.par_curve.CopyFrom(p_par_curve)
        tmp_this.curve_name=p_curve_name
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.curve_building_method=p_curve_building_method
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditCurveBuildingOutput
def dqCreateProtoCreditCurveBuildingOutput(p_credit_curve, p_success, p_err_msg):
    '''
    @args:
        1. p_credit_curve: dqproto.CreditCurve
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreditCurveBuildingOutput
    '''
    try:
        tmp_this= CreditCurveBuildingOutput()
        tmp_this.credit_curve.CopyFrom(p_credit_curve)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditDefaultSwapPricingInput
def dqCreateProtoCreditDefaultSwapPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.CreditDefaultSwap
        3. p_mkt_data: dqproto.CrMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.CrRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.CreditDefaultSwapPricingInput
    '''
    try:
        tmp_this= CreditDefaultSwapPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditDefaultSwapPricingOutput
def dqCreateProtoCreditDefaultSwapPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreditDefaultSwapPricingOutput
    '''
    try:
        tmp_this= CreditDefaultSwapPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditPremiumLeg
def dqCreateProtoCreditPremiumLeg(p_pay_receive, p_premium_rate, p_credit_premium_type, p_nominal, p_currency, p_cash_flow_schedule, p_day_count_convention, p_business_day_convention):
    '''
    @args:
        1. p_pay_receive: dqproto.PayReceiveFlag
        2. p_premium_rate: double
        3. p_credit_premium_type: dqproto.CreditPremiumType
        4. p_nominal: double
        5. p_currency: string
        6. p_cash_flow_schedule: dqproto.CreditPremiumLeg.CashFlowSchedule
        7. p_day_count_convention: dqproto.DayCountConvention
        8. p_business_day_convention: dqproto.BusinessDayConvention
    @return:
        dqproto.CreditPremiumLeg
    '''
    try:
        tmp_this= CreditPremiumLeg()
        tmp_this.pay_receive=p_pay_receive
        tmp_this.premium_rate=p_premium_rate
        tmp_this.credit_premium_type=p_credit_premium_type
        tmp_this.nominal=p_nominal
        tmp_this.currency=p_currency
        tmp_this.cash_flow_schedule.CopyFrom(p_cash_flow_schedule)
        tmp_this.day_count_convention=p_day_count_convention
        tmp_this.business_day_convention=p_business_day_convention
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditPremiumLeg.CashFlowSchedule.Row
def dqCreateProtoCreditPremiumLeg_CashFlowSchedule_Row(p_payment_date, p_start_date, p_end_date):
    '''
    @args:
        1. p_payment_date: dqproto.Date
        2. p_start_date: dqproto.Date
        3. p_end_date: dqproto.Date
    @return:
        dqproto.CreditPremiumLeg.CashFlowSchedule.Row
    '''
    try:
        tmp_this= CreditPremiumLeg.CashFlowSchedule.Row()
        tmp_this.payment_date.CopyFrom(p_payment_date)
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.end_date.CopyFrom(p_end_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditPremiumLeg.CashFlowSchedule
def dqCreateProtoCreditPremiumLeg_CashFlowSchedule(p_rows):
    '''
    @args:
        1. p_rows: dqproto.CreditPremiumLeg.CashFlowSchedule.Row
    @return:
        dqproto.CreditPremiumLeg.CashFlowSchedule
    '''
    try:
        tmp_this= CreditPremiumLeg.CashFlowSchedule()
        tmp_this.rows.extend(p_rows)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditProtectionLeg
def dqCreateProtoCreditProtectionLeg(p_pay_receive, p_settlement_type, p_reference_price, p_leverage, p_credit_protection_type, p_recovery_rate, p_start_date, p_end_date, p_nominal, p_currency):
    '''
    @args:
        1. p_pay_receive: dqproto.PayReceiveFlag
        2. p_settlement_type: dqproto.SettlementType
        3. p_reference_price: double
        4. p_leverage: double
        5. p_credit_protection_type: dqproto.CreditProtectionType
        6. p_recovery_rate: double
        7. p_start_date: dqproto.Date
        8. p_end_date: dqproto.Date
        9. p_nominal: double
        10. p_currency: string
    @return:
        dqproto.CreditProtectionLeg
    '''
    try:
        tmp_this= CreditProtectionLeg()
        tmp_this.pay_receive=p_pay_receive
        tmp_this.settlement_type=p_settlement_type
        tmp_this.reference_price=p_reference_price
        tmp_this.leverage=p_leverage
        tmp_this.credit_protection_type=p_credit_protection_type
        tmp_this.recovery_rate=p_recovery_rate
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.end_date.CopyFrom(p_end_date)
        tmp_this.nominal=p_nominal
        tmp_this.currency=p_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditDefaultSwap
def dqCreateProtoCreditDefaultSwap(p_premium_leg, p_protection_leg, p_effective_upfront_date, p_upfront_payment, p_accrual_rebate):
    '''
    @args:
        1. p_premium_leg: dqproto.CreditPremiumLeg
        2. p_protection_leg: dqproto.CreditProtectionLeg
        3. p_effective_upfront_date: dqproto.Date
        4. p_upfront_payment: double
        5. p_accrual_rebate: double
    @return:
        dqproto.CreditDefaultSwap
    '''
    try:
        tmp_this= CreditDefaultSwap()
        tmp_this.premium_leg.CopyFrom(p_premium_leg)
        tmp_this.protection_leg.CopyFrom(p_protection_leg)
        tmp_this.effective_upfront_date.CopyFrom(p_effective_upfront_date)
        tmp_this.upfront_payment=p_upfront_payment
        tmp_this.accrual_rebate=p_accrual_rebate
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditInstrumentTemplate
def dqCreateProtoCreditInstrumentTemplate(p_instrument_name, p_instrument_type, p_start_convention, p_start_delay, p_settlement_type, p_reference_price, p_leverage, p_credit_protection_type, p_recovery_rate, p_credit_premium_type, p_day_count_convention, p_frequency, p_business_day_convention, p_calendars, p_rebate_accrual):
    '''
    @args:
        1. p_instrument_name: string
        2. p_instrument_type: dqproto.InstrumentType
        3. p_start_convention: dqproto.InstrumentStartConvention
        4. p_start_delay: dqproto.Period
        5. p_settlement_type: dqproto.SettlementType
        6. p_reference_price: double
        7. p_leverage: double
        8. p_credit_protection_type: dqproto.CreditProtectionType
        9. p_recovery_rate: double
        10. p_credit_premium_type: dqproto.CreditPremiumType
        11. p_day_count_convention: dqproto.DayCountConvention
        12. p_frequency: dqproto.Frequency
        13. p_business_day_convention: dqproto.BusinessDayConvention
        14. p_calendars: string
        15. p_rebate_accrual: bool
    @return:
        dqproto.CreditInstrumentTemplate
    '''
    try:
        tmp_this= CreditInstrumentTemplate()
        tmp_this.instrument_name=p_instrument_name
        tmp_this.instrument_type=p_instrument_type
        tmp_this.start_convention=p_start_convention
        tmp_this.start_delay.CopyFrom(p_start_delay)
        tmp_this.settlement_type=p_settlement_type
        tmp_this.reference_price=p_reference_price
        tmp_this.leverage=p_leverage
        tmp_this.credit_protection_type=p_credit_protection_type
        tmp_this.recovery_rate=p_recovery_rate
        tmp_this.credit_premium_type=p_credit_premium_type
        tmp_this.day_count_convention=p_day_count_convention
        tmp_this.frequency=p_frequency
        tmp_this.business_day_convention=p_business_day_convention
        tmp_this.calendars.extend(p_calendars)
        tmp_this.rebate_accrual=p_rebate_accrual
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreditInstrumentTemplateList
def dqCreateProtoCreditInstrumentTemplateList(p_credit_instrument_template):
    '''
    @args:
        1. p_credit_instrument_template: dqproto.CreditInstrumentTemplate
    @return:
        dqproto.CreditInstrumentTemplateList
    '''
    try:
        tmp_this= CreditInstrumentTemplateList()
        tmp_this.credit_instrument_template.extend(p_credit_instrument_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildCreditDefaultSwapInput
def dqCreateProtoBuildCreditDefaultSwapInput(p_notional, p_issue_date, p_maturity_date, p_protection_pay_receive, p_protection_leg_settlement_type, p_protection_leg_reference_price, p_protection_leg_leverage, p_credit_protection_type, p_protection_leg_recovery_rate, p_coupon_rate, p_credit_premium_type, p_day_count_convention, p_frequency, p_business_day_convention, p_calendars, p_upfront_rate, p_rebate_accrual):
    '''
    @args:
        1. p_notional: dqproto.Notional
        2. p_issue_date: dqproto.Date
        3. p_maturity_date: dqproto.Date
        4. p_protection_pay_receive: dqproto.PayReceiveFlag
        5. p_protection_leg_settlement_type: dqproto.SettlementType
        6. p_protection_leg_reference_price: double
        7. p_protection_leg_leverage: double
        8. p_credit_protection_type: dqproto.CreditProtectionType
        9. p_protection_leg_recovery_rate: double
        10. p_coupon_rate: double
        11. p_credit_premium_type: dqproto.CreditPremiumType
        12. p_day_count_convention: dqproto.DayCountConvention
        13. p_frequency: dqproto.Frequency
        14. p_business_day_convention: dqproto.BusinessDayConvention
        15. p_calendars: string
        16. p_upfront_rate: double
        17. p_rebate_accrual: bool
    @return:
        dqproto.BuildCreditDefaultSwapInput
    '''
    try:
        tmp_this= BuildCreditDefaultSwapInput()
        tmp_this.notional.CopyFrom(p_notional)
        tmp_this.issue_date.CopyFrom(p_issue_date)
        tmp_this.maturity_date.CopyFrom(p_maturity_date)
        tmp_this.protection_pay_receive=p_protection_pay_receive
        tmp_this.protection_leg_settlement_type=p_protection_leg_settlement_type
        tmp_this.protection_leg_reference_price=p_protection_leg_reference_price
        tmp_this.protection_leg_leverage=p_protection_leg_leverage
        tmp_this.credit_protection_type=p_credit_protection_type
        tmp_this.protection_leg_recovery_rate=p_protection_leg_recovery_rate
        tmp_this.coupon_rate=p_coupon_rate
        tmp_this.credit_premium_type=p_credit_premium_type
        tmp_this.day_count_convention=p_day_count_convention
        tmp_this.frequency=p_frequency
        tmp_this.business_day_convention=p_business_day_convention
        tmp_this.calendars.extend(p_calendars)
        tmp_this.upfront_rate=p_upfront_rate
        tmp_this.rebate_accrual=p_rebate_accrual
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildCreditDefaultSwapOutput
def dqCreateProtoBuildCreditDefaultSwapOutput(p_credit_default_swap, p_success, p_err_msg):
    '''
    @args:
        1. p_credit_default_swap: dqproto.CreditDefaultSwap
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildCreditDefaultSwapOutput
    '''
    try:
        tmp_this= BuildCreditDefaultSwapOutput()
        tmp_this.credit_default_swap.CopyFrom(p_credit_default_swap)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Date
def dqCreateProtoDate(p_year, p_month, p_day):
    '''
    @args:
        1. p_year: int32
        2. p_month: int32
        3. p_day: int32
    @return:
        dqproto.Date
    '''
    try:
        tmp_this= Date()
        tmp_this.year=p_year
        tmp_this.month=p_month
        tmp_this.day=p_day
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Schedule
def dqCreateProtoSchedule(p_size, p_data, p_first_period_is_broken, p_last_period_is_broken):
    '''
    @args:
        1. p_size: int32
        2. p_data: dqproto.Date
        3. p_first_period_is_broken: bool
        4. p_last_period_is_broken: bool
    @return:
        dqproto.Schedule
    '''
    try:
        tmp_this= Schedule()
        tmp_this.size=p_size
        tmp_this.data.extend(p_data)
        tmp_this.first_period_is_broken=p_first_period_is_broken
        tmp_this.last_period_is_broken=p_last_period_is_broken
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Period
def dqCreateProtoPeriod(p_length, p_units, p_special_name):
    '''
    @args:
        1. p_length: int32
        2. p_units: dqproto.TimeUnit
        3. p_special_name: dqproto.SpecialPeriod
    @return:
        dqproto.Period
    '''
    try:
        tmp_this= Period()
        tmp_this.length=p_length
        tmp_this.units=p_units
        tmp_this.special_name=p_special_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Calendar
def dqCreateProtoCalendar(p_name, p_holiday, p_special_business_days):
    '''
    @args:
        1. p_name: string
        2. p_holiday: int32
        3. p_special_business_days: int32
    @return:
        dqproto.Calendar
    '''
    try:
        tmp_this= Calendar()
        tmp_this.name=p_name
        tmp_this.holiday.extend(p_holiday)
        tmp_this.special_business_days.extend(p_special_business_days)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalendarList
def dqCreateProtoCalendarList(p_calendar):
    '''
    @args:
        1. p_calendar: dqproto.Calendar
    @return:
        dqproto.CalendarList
    '''
    try:
        tmp_this= CalendarList()
        tmp_this.calendar.extend(p_calendar)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#JointCalendar
def dqCreateProtoJointCalendar(p_rule, p_calendars):
    '''
    @args:
        1. p_rule: dqproto.JointCalendarRule
        2. p_calendars: dqproto.Calendar
    @return:
        dqproto.JointCalendar
    '''
    try:
        tmp_this= JointCalendar()
        tmp_this.rule=p_rule
        tmp_this.calendars.extend(p_calendars)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GenerateDateInput
def dqCreateProtoGenerateDateInput(p_reference_date, p_period, p_calendar, p_business_day_convention, p_end_of_month, p_date_roll_convention):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_period: dqproto.Period
        3. p_calendar: string
        4. p_business_day_convention: dqproto.BusinessDayConvention
        5. p_end_of_month: bool
        6. p_date_roll_convention: dqproto.DateRollConvention
    @return:
        dqproto.GenerateDateInput
    '''
    try:
        tmp_this= GenerateDateInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.period.CopyFrom(p_period)
        tmp_this.calendar.extend(p_calendar)
        tmp_this.business_day_convention=p_business_day_convention
        tmp_this.end_of_month=p_end_of_month
        tmp_this.date_roll_convention=p_date_roll_convention
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GenerateDateOutput
def dqCreateProtoGenerateDateOutput(p_generated_date, p_success, p_err_msg):
    '''
    @args:
        1. p_generated_date: dqproto.Date
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.GenerateDateOutput
    '''
    try:
        tmp_this= GenerateDateOutput()
        tmp_this.generated_date.CopyFrom(p_generated_date)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GenerateScheduleInput
def dqCreateProtoGenerateScheduleInput(p_start_date, p_end_date, p_frequency, p_calendar, p_business_day_convention, p_stub_policy, p_date_roll_convention, p_broken_period_type):
    '''
    @args:
        1. p_start_date: dqproto.Date
        2. p_end_date: dqproto.Date
        3. p_frequency: dqproto.Frequency
        4. p_calendar: string
        5. p_business_day_convention: dqproto.BusinessDayConvention
        6. p_stub_policy: dqproto.StubPolicy
        7. p_date_roll_convention: dqproto.DateRollConvention
        8. p_broken_period_type: dqproto.BrokenPeriodType
    @return:
        dqproto.GenerateScheduleInput
    '''
    try:
        tmp_this= GenerateScheduleInput()
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.end_date.CopyFrom(p_end_date)
        tmp_this.frequency=p_frequency
        tmp_this.calendar.extend(p_calendar)
        tmp_this.business_day_convention=p_business_day_convention
        tmp_this.stub_policy=p_stub_policy
        tmp_this.date_roll_convention=p_date_roll_convention
        tmp_this.broken_period_type=p_broken_period_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GenerateScheduleOutput
def dqCreateProtoGenerateScheduleOutput(p_schedule, p_success, p_err_msg):
    '''
    @args:
        1. p_schedule: dqproto.Schedule
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.GenerateScheduleOutput
    '''
    try:
        tmp_this= GenerateScheduleOutput()
        tmp_this.schedule.CopyFrom(p_schedule)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#YearFractionCalculationInput
def dqCreateProtoYearFractionCalculationInput(p_day_count_convention, p_start_date, p_end_date, p_ref_start_date, p_ref_end_date, p_ref_period_end, p_frequency, p_is_end_of_month):
    '''
    @args:
        1. p_day_count_convention: dqproto.DayCountConvention
        2. p_start_date: dqproto.Date
        3. p_end_date: dqproto.Date
        4. p_ref_start_date: dqproto.Date
        5. p_ref_end_date: dqproto.Date
        6. p_ref_period_end: dqproto.Date
        7. p_frequency: dqproto.Frequency
        8. p_is_end_of_month: bool
    @return:
        dqproto.YearFractionCalculationInput
    '''
    try:
        tmp_this= YearFractionCalculationInput()
        tmp_this.day_count_convention=p_day_count_convention
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.end_date.CopyFrom(p_end_date)
        tmp_this.ref_start_date.CopyFrom(p_ref_start_date)
        tmp_this.ref_end_date.CopyFrom(p_ref_end_date)
        tmp_this.ref_period_end.CopyFrom(p_ref_period_end)
        tmp_this.frequency=p_frequency
        tmp_this.is_end_of_month=p_is_end_of_month
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#YearFractionCalculationOutput
def dqCreateProtoYearFractionCalculationOutput(p_year_fraction, p_success, p_err_msg):
    '''
    @args:
        1. p_year_fraction: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.YearFractionCalculationOutput
    '''
    try:
        tmp_this= YearFractionCalculationOutput()
        tmp_this.year_fraction=p_year_fraction
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqMktDataSet
def dqCreateProtoEqMktDataSet(p_as_of_date, p_discount_curve, p_dividend_curve, p_underlying_price, p_vol_surf, p_quanto_discount_curve, p_quanto_fx_vol_curve, p_quanto_correlation, p_underlying):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_discount_curve: dqproto.IrYieldCurve
        3. p_dividend_curve: dqproto.DividendCurve
        4. p_underlying_price: double
        5. p_vol_surf: dqproto.VolatilitySurface
        6. p_quanto_discount_curve: dqproto.IrYieldCurve
        7. p_quanto_fx_vol_curve: dqproto.VolatilityCurve
        8. p_quanto_correlation: double
        9. p_underlying: string
    @return:
        dqproto.EqMktDataSet
    '''
    try:
        tmp_this= EqMktDataSet()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.dividend_curve.CopyFrom(p_dividend_curve)
        tmp_this.underlying_price=p_underlying_price
        tmp_this.vol_surf.CopyFrom(p_vol_surf)
        tmp_this.quanto_discount_curve.CopyFrom(p_quanto_discount_curve)
        tmp_this.quanto_fx_vol_curve.CopyFrom(p_quanto_fx_vol_curve)
        tmp_this.quanto_correlation=p_quanto_correlation
        tmp_this.underlying=p_underlying
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqRiskSettings
def dqCreateProtoEqRiskSettings(p_ir_curve_settings, p_price_settings, p_vol_settings, p_price_vol_settings, p_theta_settings, p_dividend_curve_settings):
    '''
    @args:
        1. p_ir_curve_settings: dqproto.IrCurveRiskSettings
        2. p_price_settings: dqproto.PriceRiskSettings
        3. p_vol_settings: dqproto.VolRiskSettings
        4. p_price_vol_settings: dqproto.PriceVolRiskSettings
        5. p_theta_settings: dqproto.ThetaRiskSettings
        6. p_dividend_curve_settings: dqproto.DividendCurveRiskSettings
    @return:
        dqproto.EqRiskSettings
    '''
    try:
        tmp_this= EqRiskSettings()
        tmp_this.ir_curve_settings.CopyFrom(p_ir_curve_settings)
        tmp_this.price_settings.CopyFrom(p_price_settings)
        tmp_this.vol_settings.CopyFrom(p_vol_settings)
        tmp_this.price_vol_settings.CopyFrom(p_price_vol_settings)
        tmp_this.theta_settings.CopyFrom(p_theta_settings)
        tmp_this.dividend_curve_settings.CopyFrom(p_dividend_curve_settings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqIndexDividendCurveBuildingInput
def dqCreateProtoEqIndexDividendCurveBuildingInput(p_term_dates, p_call_price_matrix, p_put_price_matrix, p_strike_matrix, p_spot, p_discount_curve, p_future_prices):
    '''
    @args:
        1. p_term_dates: dqproto.Date
        2. p_call_price_matrix: dqproto.Vector
        3. p_put_price_matrix: dqproto.Vector
        4. p_strike_matrix: dqproto.Vector
        5. p_spot: double
        6. p_discount_curve: dqproto.IrYieldCurve
        7. p_future_prices: dqproto.Vector
    @return:
        dqproto.EqIndexDividendCurveBuildingInput
    '''
    try:
        tmp_this= EqIndexDividendCurveBuildingInput()
        tmp_this.term_dates.extend(p_term_dates)
        tmp_this.call_price_matrix.extend(p_call_price_matrix)
        tmp_this.put_price_matrix.extend(p_put_price_matrix)
        tmp_this.strike_matrix.extend(p_strike_matrix)
        tmp_this.spot=p_spot
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.future_prices.CopyFrom(p_future_prices)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqIndexDividendCurveBuildingOutput
def dqCreateProtoEqIndexDividendCurveBuildingOutput(p_dividend_curve, p_success, p_err_msg):
    '''
    @args:
        1. p_dividend_curve: dqproto.DividendCurve
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.EqIndexDividendCurveBuildingOutput
    '''
    try:
        tmp_this= EqIndexDividendCurveBuildingOutput()
        tmp_this.dividend_curve.CopyFrom(p_dividend_curve)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqVolatilitySurfaceBuildingInput
def dqCreateProtoEqVolatilitySurfaceBuildingInput(p_reference_date, p_definition, p_quotes, p_underlying_prices, p_discount_curve, p_dividend_curve, p_build_settings, p_pricing_settings, p_underlying):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_definition: dqproto.VolatilitySurfaceDefinition
        3. p_quotes: dqproto.OptionQuoteMatrix
        4. p_underlying_prices: dqproto.Vector
        5. p_discount_curve: dqproto.IrYieldCurve
        6. p_dividend_curve: dqproto.DividendCurve
        7. p_build_settings: dqproto.VolatilitySurfaceBuildSettings
        8. p_pricing_settings: dqproto.PricingSettings
        9. p_underlying: string
    @return:
        dqproto.EqVolatilitySurfaceBuildingInput
    '''
    try:
        tmp_this= EqVolatilitySurfaceBuildingInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.definition.CopyFrom(p_definition)
        tmp_this.quotes.CopyFrom(p_quotes)
        tmp_this.underlying_prices.CopyFrom(p_underlying_prices)
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.dividend_curve.CopyFrom(p_dividend_curve)
        tmp_this.build_settings.CopyFrom(p_build_settings)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.underlying=p_underlying
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqVolatilitySurfaceBuildingOutput
def dqCreateProtoEqVolatilitySurfaceBuildingOutput(p_volatility_surface, p_success, p_err_msg):
    '''
    @args:
        1. p_volatility_surface: dqproto.VolatilitySurface
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.EqVolatilitySurfaceBuildingOutput
    '''
    try:
        tmp_this= EqVolatilitySurfaceBuildingOutput()
        tmp_this.volatility_surface.CopyFrom(p_volatility_surface)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqPricingInput
def dqCreateProtoEqPricingInput(p_pricing_date, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin, p_scn_settings):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_mkt_data: dqproto.EqMktDataSet
        3. p_pricing_settings: dqproto.PricingSettings
        4. p_risk_settings: dqproto.EqRiskSettings
        5. p_use_binary: bool
        6. p_instrument_bin: bytes
        7. p_mkt_data_bin: bytes
        8. p_pricing_settings_bin: bytes
        9. p_risk_settings_bin: bytes
        10. p_scn_settings: dqproto.ScnAnalysisSettings
    @return:
        dqproto.EqPricingInput
    '''
    try:
        tmp_this= EqPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        tmp_this.scn_settings.CopyFrom(p_scn_settings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqPricingOutput
def dqCreateProtoEqPricingOutput(p_results, p_success, p_err_msg, p_scn_results, p_scn_prices, p_scn_vols):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
        4. p_scn_results: dqproto.Matrix
        5. p_scn_prices: dqproto.Vector
        6. p_scn_vols: dqproto.Vector
    @return:
        dqproto.EqPricingOutput
    '''
    try:
        tmp_this= EqPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        tmp_this.scn_results.CopyFrom(p_scn_results)
        tmp_this.scn_prices.CopyFrom(p_scn_prices)
        tmp_this.scn_vols.CopyFrom(p_scn_vols)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqEuropeanOptionPricingInput
def dqCreateProtoEqEuropeanOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.EuropeanOption
    @return:
        dqproto.EqEuropeanOptionPricingInput
    '''
    try:
        tmp_this= EqEuropeanOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqAmericanOptionPricingInput
def dqCreateProtoEqAmericanOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.AmericanOption
    @return:
        dqproto.EqAmericanOptionPricingInput
    '''
    try:
        tmp_this= EqAmericanOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqAsianOptionPricingInput
def dqCreateProtoEqAsianOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.AsianOption
    @return:
        dqproto.EqAsianOptionPricingInput
    '''
    try:
        tmp_this= EqAsianOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqDigitalOptionPricingInput
def dqCreateProtoEqDigitalOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.DigitalOption
    @return:
        dqproto.EqDigitalOptionPricingInput
    '''
    try:
        tmp_this= EqDigitalOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqOneTouchOptionPricingInput
def dqCreateProtoEqOneTouchOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.OneTouchOption
    @return:
        dqproto.EqOneTouchOptionPricingInput
    '''
    try:
        tmp_this= EqOneTouchOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqDoubleTouchOptionPricingInput
def dqCreateProtoEqDoubleTouchOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.DoubleTouchOption
    @return:
        dqproto.EqDoubleTouchOptionPricingInput
    '''
    try:
        tmp_this= EqDoubleTouchOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqSingleBarrierOptionPricingInput
def dqCreateProtoEqSingleBarrierOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.SingleBarrierOption
    @return:
        dqproto.EqSingleBarrierOptionPricingInput
    '''
    try:
        tmp_this= EqSingleBarrierOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqDoubleBarrierOptionPricingInput
def dqCreateProtoEqDoubleBarrierOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.DoubleBarrierOption
    @return:
        dqproto.EqDoubleBarrierOptionPricingInput
    '''
    try:
        tmp_this= EqDoubleBarrierOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqSingleSharkFinOptionPricingInput
def dqCreateProtoEqSingleSharkFinOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.SingleSharkFinOption
    @return:
        dqproto.EqSingleSharkFinOptionPricingInput
    '''
    try:
        tmp_this= EqSingleSharkFinOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqDoubleSharkFinOptionPricingInput
def dqCreateProtoEqDoubleSharkFinOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.DoubleSharkFinOption
    @return:
        dqproto.EqDoubleSharkFinOptionPricingInput
    '''
    try:
        tmp_this= EqDoubleSharkFinOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqPingPongOptionPricingInput
def dqCreateProtoEqPingPongOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.PingPongOption
    @return:
        dqproto.EqPingPongOptionPricingInput
    '''
    try:
        tmp_this= EqPingPongOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqAirbagOptionPricingInput
def dqCreateProtoEqAirbagOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.AirbagOption
    @return:
        dqproto.EqAirbagOptionPricingInput
    '''
    try:
        tmp_this= EqAirbagOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqRangeAccrualOptionPricingInput
def dqCreateProtoEqRangeAccrualOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.RangeAccrualOption
    @return:
        dqproto.EqRangeAccrualOptionPricingInput
    '''
    try:
        tmp_this= EqRangeAccrualOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqPhoenixAutoCallableNotePricingInput
def dqCreateProtoEqPhoenixAutoCallableNotePricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.PhoenixAutoCallableNote
    @return:
        dqproto.EqPhoenixAutoCallableNotePricingInput
    '''
    try:
        tmp_this= EqPhoenixAutoCallableNotePricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EqSnowballAutoCallableNotePricingInput
def dqCreateProtoEqSnowballAutoCallableNotePricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.EqPricingInput
        2. p_instrument: dqproto.SnowballAutoCallableNote
    @return:
        dqproto.EqSnowballAutoCallableNotePricingInput
    '''
    try:
        tmp_this= EqSnowballAutoCallableNotePricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondYieldCurveBuildSettings
def dqCreateProtoBondYieldCurveBuildSettings(p_curve_name, p_curve_type, p_interp_method, p_extrap_method):
    '''
    @args:
        1. p_curve_name: string
        2. p_curve_type: dqproto.IrYieldCurveType
        3. p_interp_method: dqproto.InterpMethod
        4. p_extrap_method: dqproto.ExtrapMethod
    @return:
        dqproto.BondYieldCurveBuildSettings
    '''
    try:
        tmp_this= BondYieldCurveBuildSettings()
        tmp_this.curve_name=p_curve_name
        tmp_this.curve_type=p_curve_type
        tmp_this.interp_method=p_interp_method
        tmp_this.extrap_method=p_extrap_method
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondParCurve.Pillar
def dqCreateProtoBondParCurve_Pillar(p_instrument_name, p_quote):
    '''
    @args:
        1. p_instrument_name: string
        2. p_quote: double
    @return:
        dqproto.BondParCurve.Pillar
    '''
    try:
        tmp_this= BondParCurve.Pillar()
        tmp_this.instrument_name=p_instrument_name
        tmp_this.quote=p_quote
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondParCurve
def dqCreateProtoBondParCurve(p_reference_date, p_currency, p_pillars, p_quote_type, p_name):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_currency: string
        3. p_pillars: dqproto.BondParCurve.Pillar
        4. p_quote_type: dqproto.BondQuoteType
        5. p_name: string
    @return:
        dqproto.BondParCurve
    '''
    try:
        tmp_this= BondParCurve()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.currency=p_currency
        tmp_this.pillars.extend(p_pillars)
        tmp_this.quote_type=p_quote_type
        tmp_this.name=p_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondYieldCurveBuildSettingsContainer
def dqCreateProtoBondYieldCurveBuildSettingsContainer(p_target_curve_name, p_bond_yield_curve_build_settings, p_par_curve, p_day_count_convention, p_compounding_type, p_frequency):
    '''
    @args:
        1. p_target_curve_name: string
        2. p_bond_yield_curve_build_settings: dqproto.BondYieldCurveBuildSettings
        3. p_par_curve: dqproto.BondParCurve
        4. p_day_count_convention: dqproto.DayCountConvention
        5. p_compounding_type: dqproto.CompoundingType
        6. p_frequency: dqproto.Frequency
    @return:
        dqproto.BondYieldCurveBuildSettingsContainer
    '''
    try:
        tmp_this= BondYieldCurveBuildSettingsContainer()
        tmp_this.target_curve_name=p_target_curve_name
        tmp_this.bond_yield_curve_build_settings.CopyFrom(p_bond_yield_curve_build_settings)
        tmp_this.par_curve.CopyFrom(p_par_curve)
        tmp_this.day_count_convention=p_day_count_convention
        tmp_this.compounding_type=p_compounding_type
        tmp_this.frequency=p_frequency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FiMktDataSet
def dqCreateProtoFiMktDataSet(p_as_of_date, p_discount_curve, p_spread_curve, p_forward_curve, p_underlying_discount_curve, p_underlying_income_curve):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_discount_curve: dqproto.IrYieldCurve
        3. p_spread_curve: dqproto.CreditCurve
        4. p_forward_curve: dqproto.IrYieldCurve
        5. p_underlying_discount_curve: dqproto.IrYieldCurve
        6. p_underlying_income_curve: dqproto.IrYieldCurve
    @return:
        dqproto.FiMktDataSet
    '''
    try:
        tmp_this= FiMktDataSet()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.spread_curve.CopyFrom(p_spread_curve)
        tmp_this.forward_curve.CopyFrom(p_forward_curve)
        tmp_this.underlying_discount_curve.CopyFrom(p_underlying_discount_curve)
        tmp_this.underlying_income_curve.CopyFrom(p_underlying_income_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FiRiskSettings
def dqCreateProtoFiRiskSettings(p_ir_curve_settings, p_cs_curve_settings, p_theta_settings):
    '''
    @args:
        1. p_ir_curve_settings: dqproto.IrCurveRiskSettings
        2. p_cs_curve_settings: dqproto.CreditCurveRiskSettings
        3. p_theta_settings: dqproto.ThetaRiskSettings
    @return:
        dqproto.FiRiskSettings
    '''
    try:
        tmp_this= FiRiskSettings()
        tmp_this.ir_curve_settings.CopyFrom(p_ir_curve_settings)
        tmp_this.cs_curve_settings.CopyFrom(p_cs_curve_settings)
        tmp_this.theta_settings.CopyFrom(p_theta_settings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateBondParCurveInput.Pillar
def dqCreateProtoCreateBondParCurveInput_Pillar(p_instrument_name, p_quote):
    '''
    @args:
        1. p_instrument_name: string
        2. p_quote: double
    @return:
        dqproto.CreateBondParCurveInput.Pillar
    '''
    try:
        tmp_this= CreateBondParCurveInput.Pillar()
        tmp_this.instrument_name=p_instrument_name
        tmp_this.quote=p_quote
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateBondParCurveInput
def dqCreateProtoCreateBondParCurveInput(p_reference_date, p_currency, p_pillars, p_quote_type, p_name):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_currency: string
        3. p_pillars: dqproto.CreateBondParCurveInput.Pillar
        4. p_quote_type: dqproto.BondQuoteType
        5. p_name: string
    @return:
        dqproto.CreateBondParCurveInput
    '''
    try:
        tmp_this= CreateBondParCurveInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.currency=p_currency
        tmp_this.pillars.extend(p_pillars)
        tmp_this.quote_type=p_quote_type
        tmp_this.name=p_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateBondParCurveOutput
def dqCreateProtoCreateBondParCurveOutput(p_bond_par_curve, p_success, p_err_msg):
    '''
    @args:
        1. p_bond_par_curve: dqproto.BondParCurve
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateBondParCurveOutput
    '''
    try:
        tmp_this= CreateBondParCurveOutput()
        tmp_this.bond_par_curve.CopyFrom(p_bond_par_curve)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondYieldCurveBuildingInput
def dqCreateProtoBondYieldCurveBuildingInput(p_reference_date, p_build_settings, p_fwd_curve, p_curve_building_method, p_calc_jacobian):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_build_settings: dqproto.BondYieldCurveBuildSettingsContainer
        3. p_fwd_curve: dqproto.IrYieldCurve
        4. p_curve_building_method: dqproto.IrYieldCurveBuildingMethod
        5. p_calc_jacobian: bool
    @return:
        dqproto.BondYieldCurveBuildingInput
    '''
    try:
        tmp_this= BondYieldCurveBuildingInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.build_settings.extend(p_build_settings)
        tmp_this.fwd_curve.CopyFrom(p_fwd_curve)
        tmp_this.curve_building_method=p_curve_building_method
        tmp_this.calc_jacobian=p_calc_jacobian
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondYieldCurveBuildingOutput
def dqCreateProtoBondYieldCurveBuildingOutput(p_ir_yield_curve, p_success, p_err_msg):
    '''
    @args:
        1. p_ir_yield_curve: dqproto.IrYieldCurve
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BondYieldCurveBuildingOutput
    '''
    try:
        tmp_this= BondYieldCurveBuildingOutput()
        tmp_this.ir_yield_curve.CopyFrom(p_ir_yield_curve)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondCreditSpreadCurveBuildingInput
def dqCreateProtoBondCreditSpreadCurveBuildingInput(p_reference_date, p_par_curve, p_discount_curve, p_fwd_curve, p_curve_name, p_curve_building_method, p_calc_jacobian):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_par_curve: dqproto.BondParCurve
        3. p_discount_curve: dqproto.IrYieldCurve
        4. p_fwd_curve: dqproto.IrYieldCurve
        5. p_curve_name: string
        6. p_curve_building_method: dqproto.IrYieldCurveBuildingMethod
        7. p_calc_jacobian: bool
    @return:
        dqproto.BondCreditSpreadCurveBuildingInput
    '''
    try:
        tmp_this= BondCreditSpreadCurveBuildingInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.par_curve.CopyFrom(p_par_curve)
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.fwd_curve.CopyFrom(p_fwd_curve)
        tmp_this.curve_name=p_curve_name
        tmp_this.curve_building_method=p_curve_building_method
        tmp_this.calc_jacobian=p_calc_jacobian
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondCreditSpreadCurveBuildingOutput
def dqCreateProtoBondCreditSpreadCurveBuildingOutput(p_credit_sprd_curve, p_success, p_err_msg, p_survival_probabilities):
    '''
    @args:
        1. p_credit_sprd_curve: dqproto.CreditCurve
        2. p_success: bool
        3. p_err_msg: string
        4. p_survival_probabilities: dqproto.Vector
    @return:
        dqproto.BondCreditSpreadCurveBuildingOutput
    '''
    try:
        tmp_this= BondCreditSpreadCurveBuildingOutput()
        tmp_this.credit_sprd_curve.CopyFrom(p_credit_sprd_curve)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        tmp_this.survival_probabilities.CopyFrom(p_survival_probabilities)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondFutConversionFactorCalculationInput
def dqCreateProtoBondFutConversionFactorCalculationInput(p_bond_cpn_rate, p_bond_cpn_freq, p_nominal_cpn_rate, p_bond_maturity, p_settlement_date, p_last_cpn_date):
    '''
    @args:
        1. p_bond_cpn_rate: double
        2. p_bond_cpn_freq: dqproto.Frequency
        3. p_nominal_cpn_rate: double
        4. p_bond_maturity: dqproto.Date
        5. p_settlement_date: dqproto.Date
        6. p_last_cpn_date: dqproto.Date
    @return:
        dqproto.BondFutConversionFactorCalculationInput
    '''
    try:
        tmp_this= BondFutConversionFactorCalculationInput()
        tmp_this.bond_cpn_rate=p_bond_cpn_rate
        tmp_this.bond_cpn_freq=p_bond_cpn_freq
        tmp_this.nominal_cpn_rate=p_nominal_cpn_rate
        tmp_this.bond_maturity.CopyFrom(p_bond_maturity)
        tmp_this.settlement_date.CopyFrom(p_settlement_date)
        tmp_this.last_cpn_date.CopyFrom(p_last_cpn_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondFutConversionFactorCalculationOutput
def dqCreateProtoBondFutConversionFactorCalculationOutput(p_conversion_factor, p_success, p_err_msg):
    '''
    @args:
        1. p_conversion_factor: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BondFutConversionFactorCalculationOutput
    '''
    try:
        tmp_this= BondFutConversionFactorCalculationOutput()
        tmp_this.conversion_factor=p_conversion_factor
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ImpliedRepoRateCalculationInput
def dqCreateProtoImpliedRepoRateCalculationInput(p_fut_price, p_conversion_factor, p_bond_clean_price, p_bond_cpn_rate, p_as_of_date, p_last_cpn_date, p_settlement_date, p_day_count, p_next_cpn_date, p_cpn_freq):
    '''
    @args:
        1. p_fut_price: double
        2. p_conversion_factor: double
        3. p_bond_clean_price: double
        4. p_bond_cpn_rate: double
        5. p_as_of_date: dqproto.Date
        6. p_last_cpn_date: dqproto.Date
        7. p_settlement_date: dqproto.Date
        8. p_day_count: dqproto.DayCountConvention
        9. p_next_cpn_date: dqproto.Date
        10. p_cpn_freq: dqproto.Frequency
    @return:
        dqproto.ImpliedRepoRateCalculationInput
    '''
    try:
        tmp_this= ImpliedRepoRateCalculationInput()
        tmp_this.fut_price=p_fut_price
        tmp_this.conversion_factor=p_conversion_factor
        tmp_this.bond_clean_price=p_bond_clean_price
        tmp_this.bond_cpn_rate=p_bond_cpn_rate
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.last_cpn_date.CopyFrom(p_last_cpn_date)
        tmp_this.settlement_date.CopyFrom(p_settlement_date)
        tmp_this.day_count=p_day_count
        tmp_this.next_cpn_date.CopyFrom(p_next_cpn_date)
        tmp_this.cpn_freq=p_cpn_freq
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ImpliedRepoRateCalculationOutput
def dqCreateProtoImpliedRepoRateCalculationOutput(p_implied_repo_rate, p_success, p_err_msg):
    '''
    @args:
        1. p_implied_repo_rate: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.ImpliedRepoRateCalculationOutput
    '''
    try:
        tmp_this= ImpliedRepoRateCalculationOutput()
        tmp_this.implied_repo_rate=p_implied_repo_rate
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#VanillaBondPricingInput
def dqCreateProtoVanillaBondPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.VanillaBond
        3. p_mkt_data: dqproto.FiMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FiRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.VanillaBondPricingInput
    '''
    try:
        tmp_this= VanillaBondPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#VanillaBondPricingOutput
def dqCreateProtoVanillaBondPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.VanillaBondPricingOutput
    '''
    try:
        tmp_this= VanillaBondPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#AssetBackedSecurityPricingInput
def dqCreateProtoAssetBackedSecurityPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.AssetBackedSecurity
        3. p_mkt_data: dqproto.FiMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FiRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.AssetBackedSecurityPricingInput
    '''
    try:
        tmp_this= AssetBackedSecurityPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#AssetBackedSecurityPricingOutput
def dqCreateProtoAssetBackedSecurityPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.AssetBackedSecurityPricingOutput
    '''
    try:
        tmp_this= AssetBackedSecurityPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#MortgageBackedSecurityPricingInput
def dqCreateProtoMortgageBackedSecurityPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.MortgageBackedSecurity
        3. p_mkt_data: dqproto.FiMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FiRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.MortgageBackedSecurityPricingInput
    '''
    try:
        tmp_this= MortgageBackedSecurityPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#MortgageBackedSecurityPricingOutput
def dqCreateProtoMortgageBackedSecurityPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.MortgageBackedSecurityPricingOutput
    '''
    try:
        tmp_this= MortgageBackedSecurityPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondForwardPricingInput
def dqCreateProtoBondForwardPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.BondForward
        3. p_mkt_data: dqproto.FiMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FiRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.BondForwardPricingInput
    '''
    try:
        tmp_this= BondForwardPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondForwardPricingOutput
def dqCreateProtoBondForwardPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BondForwardPricingOutput
    '''
    try:
        tmp_this= BondForwardPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondFuturePricingInput
def dqCreateProtoBondFuturePricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.BondFuture
        3. p_mkt_data: dqproto.FiMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FiRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.BondFuturePricingInput
    '''
    try:
        tmp_this= BondFuturePricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondFuturePricingOutput
def dqCreateProtoBondFuturePricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BondFuturePricingOutput
    '''
    try:
        tmp_this= BondFuturePricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondPledgedRepoPricingInput
def dqCreateProtoBondPledgedRepoPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.BondPledgedRepo
        3. p_mkt_data: dqproto.FiMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FiRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.BondPledgedRepoPricingInput
    '''
    try:
        tmp_this= BondPledgedRepoPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondPledgedRepoPricingOutput
def dqCreateProtoBondPledgedRepoPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BondPledgedRepoPricingOutput
    '''
    try:
        tmp_this= BondPledgedRepoPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondOutrightRepoPricingInput
def dqCreateProtoBondOutrightRepoPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.BondOutrightRepo
        3. p_mkt_data: dqproto.FiMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FiRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.BondOutrightRepoPricingInput
    '''
    try:
        tmp_this= BondOutrightRepoPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondOutrightRepoPricingOutput
def dqCreateProtoBondOutrightRepoPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BondOutrightRepoPricingOutput
    '''
    try:
        tmp_this= BondOutrightRepoPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondEuropeanOptionPricingInput
def dqCreateProtoBondEuropeanOptionPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.BondEuropeanOption
        3. p_mkt_data: dqproto.FiMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FiRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.BondEuropeanOptionPricingInput
    '''
    try:
        tmp_this= BondEuropeanOptionPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondEuropeanOptionPricingOutput
def dqCreateProtoBondEuropeanOptionPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BondEuropeanOptionPricingOutput
    '''
    try:
        tmp_this= BondEuropeanOptionPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondAmericanOptionPricingInput
def dqCreateProtoBondAmericanOptionPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.BondAmericanOption
        3. p_mkt_data: dqproto.FiMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FiRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.BondAmericanOptionPricingInput
    '''
    try:
        tmp_this= BondAmericanOptionPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondAmericanOptionPricingOutput
def dqCreateProtoBondAmericanOptionPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BondAmericanOptionPricingOutput
    '''
    try:
        tmp_this= BondAmericanOptionPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CallableBondPricingInput
def dqCreateProtoCallableBondPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.CallableBond
        3. p_mkt_data: dqproto.FiMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FiRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.CallableBondPricingInput
    '''
    try:
        tmp_this= CallableBondPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CallableBondPricingOutput
def dqCreateProtoCallableBondPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CallableBondPricingOutput
    '''
    try:
        tmp_this= CallableBondPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ConvertibleBondPricingInput
def dqCreateProtoConvertibleBondPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.ConvertibleBond
        3. p_mkt_data: dqproto.FiMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FiRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.ConvertibleBondPricingInput
    '''
    try:
        tmp_this= ConvertibleBondPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ConvertibleBondPricingOutput
def dqCreateProtoConvertibleBondPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.ConvertibleBondPricingOutput
    '''
    try:
        tmp_this= ConvertibleBondPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ExchangeableBondPricingInput
def dqCreateProtoExchangeableBondPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.ExchangeableBond
        3. p_mkt_data: dqproto.FiMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FiRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.ExchangeableBondPricingInput
    '''
    try:
        tmp_this= ExchangeableBondPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ExchangeableBondPricingOutput
def dqCreateProtoExchangeableBondPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.ExchangeableBondPricingOutput
    '''
    try:
        tmp_this= ExchangeableBondPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ExtendibleBondPricingInput
def dqCreateProtoExtendibleBondPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.ExtendibleBond
        3. p_mkt_data: dqproto.FiMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FiRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.ExtendibleBondPricingInput
    '''
    try:
        tmp_this= ExtendibleBondPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ExtendibleBondPricingOutput
def dqCreateProtoExtendibleBondPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.ExtendibleBondPricingOutput
    '''
    try:
        tmp_this= ExtendibleBondPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CallableStepUpBondPricingInput
def dqCreateProtoCallableStepUpBondPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.CallableStepUpBond
        3. p_mkt_data: dqproto.FiMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FiRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.CallableStepUpBondPricingInput
    '''
    try:
        tmp_this= CallableStepUpBondPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CallableStepUpBondPricingOutput
def dqCreateProtoCallableStepUpBondPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CallableStepUpBondPricingOutput
    '''
    try:
        tmp_this= CallableStepUpBondPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ZSpreadCalculationInput
def dqCreateProtoZSpreadCalculationInput(p_npv, p_calculation_date, p_bond, p_mkt_data):
    '''
    @args:
        1. p_npv: double
        2. p_calculation_date: dqproto.Date
        3. p_bond: dqproto.VanillaBond
        4. p_mkt_data: dqproto.FiMktDataSet
    @return:
        dqproto.ZSpreadCalculationInput
    '''
    try:
        tmp_this= ZSpreadCalculationInput()
        tmp_this.npv=p_npv
        tmp_this.calculation_date.CopyFrom(p_calculation_date)
        tmp_this.bond.CopyFrom(p_bond)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ZSpreadCalculationOutput
def dqCreateProtoZSpreadCalculationOutput(p_z_spread, p_success, p_err_msg):
    '''
    @args:
        1. p_z_spread: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.ZSpreadCalculationOutput
    '''
    try:
        tmp_this= ZSpreadCalculationOutput()
        tmp_this.z_spread=p_z_spread
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#YieldToMaturityCalculationInput
def dqCreateProtoYieldToMaturityCalculationInput(p_calculation_date, p_compounding_type, p_bond, p_forward_curve, p_price, p_price_type, p_frequency):
    '''
    @args:
        1. p_calculation_date: dqproto.Date
        2. p_compounding_type: dqproto.CompoundingType
        3. p_bond: dqproto.VanillaBond
        4. p_forward_curve: dqproto.IrYieldCurve
        5. p_price: double
        6. p_price_type: dqproto.BondQuoteType
        7. p_frequency: dqproto.Frequency
    @return:
        dqproto.YieldToMaturityCalculationInput
    '''
    try:
        tmp_this= YieldToMaturityCalculationInput()
        tmp_this.calculation_date.CopyFrom(p_calculation_date)
        tmp_this.compounding_type=p_compounding_type
        tmp_this.bond.CopyFrom(p_bond)
        tmp_this.forward_curve.CopyFrom(p_forward_curve)
        tmp_this.price=p_price
        tmp_this.price_type=p_price_type
        tmp_this.frequency=p_frequency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#YieldToMaturityCalculationOutput
def dqCreateProtoYieldToMaturityCalculationOutput(p_yield_to_maturity, p_success, p_err_msg):
    '''
    @args:
        1. p_yield_to_maturity: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.YieldToMaturityCalculationOutput
    '''
    try:
        tmp_this= YieldToMaturityCalculationOutput()
        tmp_this.yield_to_maturity=p_yield_to_maturity
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FixedCpnBondParRateCalculationInput
def dqCreateProtoFixedCpnBondParRateCalculationInput(p_calculation_date, p_bond, p_mkt_data):
    '''
    @args:
        1. p_calculation_date: dqproto.Date
        2. p_bond: dqproto.VanillaBond
        3. p_mkt_data: dqproto.FiMktDataSet
    @return:
        dqproto.FixedCpnBondParRateCalculationInput
    '''
    try:
        tmp_this= FixedCpnBondParRateCalculationInput()
        tmp_this.calculation_date.CopyFrom(p_calculation_date)
        tmp_this.bond.CopyFrom(p_bond)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FixedCpnBondParRateCalculationOutput
def dqCreateProtoFixedCpnBondParRateCalculationOutput(p_par_rate, p_success, p_err_msg):
    '''
    @args:
        1. p_par_rate: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FixedCpnBondParRateCalculationOutput
    '''
    try:
        tmp_this= FixedCpnBondParRateCalculationOutput()
        tmp_this.par_rate=p_par_rate
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Bond
def dqCreateProtoBond(p_issue_date, p_settlement_days, p_calendars, p_excoupon_period, p_excoupon_calendars, p_excoupon_day_convention, p_excoupon_end_of_month, p_issue_price, p_notional_type, p_recovery_rate):
    '''
    @args:
        1. p_issue_date: dqproto.Date
        2. p_settlement_days: int32
        3. p_calendars: string
        4. p_excoupon_period: dqproto.Period
        5. p_excoupon_calendars: string
        6. p_excoupon_day_convention: dqproto.BusinessDayConvention
        7. p_excoupon_end_of_month: bool
        8. p_issue_price: double
        9. p_notional_type: dqproto.NotionalType
        10. p_recovery_rate: double
    @return:
        dqproto.Bond
    '''
    try:
        tmp_this= Bond()
        tmp_this.issue_date.CopyFrom(p_issue_date)
        tmp_this.settlement_days=p_settlement_days
        tmp_this.calendars.extend(p_calendars)
        tmp_this.excoupon_period.CopyFrom(p_excoupon_period)
        tmp_this.excoupon_calendars.extend(p_excoupon_calendars)
        tmp_this.excoupon_day_convention=p_excoupon_day_convention
        tmp_this.excoupon_end_of_month=p_excoupon_end_of_month
        tmp_this.issue_price=p_issue_price
        tmp_this.notional_type=p_notional_type
        tmp_this.recovery_rate=p_recovery_rate
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#VanillaBond
def dqCreateProtoVanillaBond(p_bond, p_vanilla_bond_type, p_leg):
    '''
    @args:
        1. p_bond: dqproto.Bond
        2. p_vanilla_bond_type: dqproto.VanillaBondType
        3. p_leg: dqproto.IrVanillaLeg
    @return:
        dqproto.VanillaBond
    '''
    try:
        tmp_this= VanillaBond()
        tmp_this.bond.CopyFrom(p_bond)
        tmp_this.vanilla_bond_type=p_vanilla_bond_type
        tmp_this.leg.CopyFrom(p_leg)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#AssetBackedSecurity
def dqCreateProtoAssetBackedSecurity(p_bond):
    '''
    @args:
        1. p_bond: dqproto.VanillaBond
    @return:
        dqproto.AssetBackedSecurity
    '''
    try:
        tmp_this= AssetBackedSecurity()
        tmp_this.bond.CopyFrom(p_bond)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#MortgageBackedSecurity
def dqCreateProtoMortgageBackedSecurity(p_bond):
    '''
    @args:
        1. p_bond: dqproto.VanillaBond
    @return:
        dqproto.MortgageBackedSecurity
    '''
    try:
        tmp_this= MortgageBackedSecurity()
        tmp_this.bond.CopyFrom(p_bond)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#VanillaBondTemplate
def dqCreateProtoVanillaBondTemplate(p_instrument_name, p_vanilla_bond_type, p_settlement_days, p_leg_definition, p_excoupon_period, p_excoupon_calendar, p_excoupon_day_convention, p_excoupon_end_of_month, p_issue_date, p_rate, p_maturity, p_issue_price, p_start_date, p_notional_type, p_recovery_rate):
    '''
    @args:
        1. p_instrument_name: string
        2. p_vanilla_bond_type: dqproto.VanillaBondType
        3. p_settlement_days: int32
        4. p_leg_definition: dqproto.InterestRateLegDefinition
        5. p_excoupon_period: dqproto.Period
        6. p_excoupon_calendar: string
        7. p_excoupon_day_convention: dqproto.BusinessDayConvention
        8. p_excoupon_end_of_month: bool
        9. p_issue_date: dqproto.Date
        10. p_rate: double
        11. p_maturity: dqproto.Period
        12. p_issue_price: double
        13. p_start_date: dqproto.Date
        14. p_notional_type: dqproto.NotionalType
        15. p_recovery_rate: double
    @return:
        dqproto.VanillaBondTemplate
    '''
    try:
        tmp_this= VanillaBondTemplate()
        tmp_this.instrument_name=p_instrument_name
        tmp_this.vanilla_bond_type=p_vanilla_bond_type
        tmp_this.settlement_days=p_settlement_days
        tmp_this.leg_definition.CopyFrom(p_leg_definition)
        tmp_this.excoupon_period.CopyFrom(p_excoupon_period)
        tmp_this.excoupon_calendar=p_excoupon_calendar
        tmp_this.excoupon_day_convention=p_excoupon_day_convention
        tmp_this.excoupon_end_of_month=p_excoupon_end_of_month
        tmp_this.issue_date.CopyFrom(p_issue_date)
        tmp_this.rate=p_rate
        tmp_this.maturity.CopyFrom(p_maturity)
        tmp_this.issue_price=p_issue_price
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.notional_type=p_notional_type
        tmp_this.recovery_rate=p_recovery_rate
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#VanillaBondTemplateList
def dqCreateProtoVanillaBondTemplateList(p_vanilla_bond_template):
    '''
    @args:
        1. p_vanilla_bond_template: dqproto.VanillaBondTemplate
    @return:
        dqproto.VanillaBondTemplateList
    '''
    try:
        tmp_this= VanillaBondTemplateList()
        tmp_this.vanilla_bond_template.extend(p_vanilla_bond_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CallableBond
def dqCreateProtoCallableBond(p_vanilla_bond, p_payoff_type, p_strike_price, p_exercise_schedule, p_lower_adj_sprd, p_upper_adj_sprd):
    '''
    @args:
        1. p_vanilla_bond: dqproto.VanillaBond
        2. p_payoff_type: dqproto.PayoffType
        3. p_strike_price: double
        4. p_exercise_schedule: dqproto.ExerciseSchedule
        5. p_lower_adj_sprd: double
        6. p_upper_adj_sprd: double
    @return:
        dqproto.CallableBond
    '''
    try:
        tmp_this= CallableBond()
        tmp_this.vanilla_bond.CopyFrom(p_vanilla_bond)
        tmp_this.payoff_type=p_payoff_type
        tmp_this.strike_price=p_strike_price
        tmp_this.exercise_schedule.CopyFrom(p_exercise_schedule)
        tmp_this.lower_adj_sprd=p_lower_adj_sprd
        tmp_this.upper_adj_sprd=p_upper_adj_sprd
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CallableBondTemplate
def dqCreateProtoCallableBondTemplate(p_vanilla_bond_template, p_payoff_type, p_strike_price, p_early_redemption_start_date, p_notification_days, p_lower_adj_sprd, p_upper_adj_sprd):
    '''
    @args:
        1. p_vanilla_bond_template: dqproto.VanillaBondTemplate
        2. p_payoff_type: dqproto.PayoffType
        3. p_strike_price: double
        4. p_early_redemption_start_date: dqproto.Date
        5. p_notification_days: int32
        6. p_lower_adj_sprd: double
        7. p_upper_adj_sprd: double
    @return:
        dqproto.CallableBondTemplate
    '''
    try:
        tmp_this= CallableBondTemplate()
        tmp_this.vanilla_bond_template.CopyFrom(p_vanilla_bond_template)
        tmp_this.payoff_type=p_payoff_type
        tmp_this.strike_price=p_strike_price
        tmp_this.early_redemption_start_date.CopyFrom(p_early_redemption_start_date)
        tmp_this.notification_days=p_notification_days
        tmp_this.lower_adj_sprd=p_lower_adj_sprd
        tmp_this.upper_adj_sprd=p_upper_adj_sprd
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CallableBondTemplateList
def dqCreateProtoCallableBondTemplateList(p_callable_bond_template):
    '''
    @args:
        1. p_callable_bond_template: dqproto.CallableBondTemplate
    @return:
        dqproto.CallableBondTemplateList
    '''
    try:
        tmp_this= CallableBondTemplateList()
        tmp_this.callable_bond_template.extend(p_callable_bond_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondForward
def dqCreateProtoBondForward(p_underlying_bond):
    '''
    @args:
        1. p_underlying_bond: dqproto.VanillaBond
    @return:
        dqproto.BondForward
    '''
    try:
        tmp_this= BondForward()
        tmp_this.underlying_bond.CopyFrom(p_underlying_bond)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondFuture
def dqCreateProtoBondFuture(p_underlying_bond):
    '''
    @args:
        1. p_underlying_bond: dqproto.VanillaBond
    @return:
        dqproto.BondFuture
    '''
    try:
        tmp_this= BondFuture()
        tmp_this.underlying_bond.CopyFrom(p_underlying_bond)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondEuropeanOption
def dqCreateProtoBondEuropeanOption(p_underlying_bond):
    '''
    @args:
        1. p_underlying_bond: dqproto.VanillaBond
    @return:
        dqproto.BondEuropeanOption
    '''
    try:
        tmp_this= BondEuropeanOption()
        tmp_this.underlying_bond.CopyFrom(p_underlying_bond)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondAmericanOption
def dqCreateProtoBondAmericanOption(p_underlying_bond):
    '''
    @args:
        1. p_underlying_bond: dqproto.VanillaBond
    @return:
        dqproto.BondAmericanOption
    '''
    try:
        tmp_this= BondAmericanOption()
        tmp_this.underlying_bond.CopyFrom(p_underlying_bond)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ConvertibleBond
def dqCreateProtoConvertibleBond(p_underlying_bond):
    '''
    @args:
        1. p_underlying_bond: dqproto.VanillaBond
    @return:
        dqproto.ConvertibleBond
    '''
    try:
        tmp_this= ConvertibleBond()
        tmp_this.underlying_bond.CopyFrom(p_underlying_bond)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ExchangeableBond
def dqCreateProtoExchangeableBond(p_underlying_bond):
    '''
    @args:
        1. p_underlying_bond: dqproto.VanillaBond
    @return:
        dqproto.ExchangeableBond
    '''
    try:
        tmp_this= ExchangeableBond()
        tmp_this.underlying_bond.CopyFrom(p_underlying_bond)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ExtendibleBond
def dqCreateProtoExtendibleBond(p_underlying_bond):
    '''
    @args:
        1. p_underlying_bond: dqproto.VanillaBond
    @return:
        dqproto.ExtendibleBond
    '''
    try:
        tmp_this= ExtendibleBond()
        tmp_this.underlying_bond.CopyFrom(p_underlying_bond)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondPledgedRepo
def dqCreateProtoBondPledgedRepo(p_leg):
    '''
    @args:
        1. p_leg: dqproto.IrVanillaLeg
    @return:
        dqproto.BondPledgedRepo
    '''
    try:
        tmp_this= BondPledgedRepo()
        tmp_this.leg.CopyFrom(p_leg)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BondOutrightRepo
def dqCreateProtoBondOutrightRepo(p_underlying_bond):
    '''
    @args:
        1. p_underlying_bond: dqproto.VanillaBond
    @return:
        dqproto.BondOutrightRepo
    '''
    try:
        tmp_this= BondOutrightRepo()
        tmp_this.underlying_bond.CopyFrom(p_underlying_bond)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CallableStepUpBond
def dqCreateProtoCallableStepUpBond(p_underlying_bond):
    '''
    @args:
        1. p_underlying_bond: dqproto.VanillaBond
    @return:
        dqproto.CallableStepUpBond
    '''
    try:
        tmp_this= CallableStepUpBond()
        tmp_this.underlying_bond.CopyFrom(p_underlying_bond)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildVanillaBondInput
def dqCreateProtoBuildVanillaBondInput(p_nominal, p_vanilla_bond_template, p_fixings):
    '''
    @args:
        1. p_nominal: double
        2. p_vanilla_bond_template: dqproto.VanillaBondTemplate
        3. p_fixings: dqproto.TimeSeries
    @return:
        dqproto.BuildVanillaBondInput
    '''
    try:
        tmp_this= BuildVanillaBondInput()
        tmp_this.nominal=p_nominal
        tmp_this.vanilla_bond_template.CopyFrom(p_vanilla_bond_template)
        tmp_this.fixings.CopyFrom(p_fixings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildVanillaBondOutput
def dqCreateProtoBuildVanillaBondOutput(p_instrument, p_inst_name, p_success, p_err_msg):
    '''
    @args:
        1. p_instrument: dqproto.VanillaBond
        2. p_inst_name: string
        3. p_success: bool
        4. p_err_msg: string
    @return:
        dqproto.BuildVanillaBondOutput
    '''
    try:
        tmp_this= BuildVanillaBondOutput()
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.inst_name=p_inst_name
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildAssetBackedSecurityInput
def dqCreateProtoBuildAssetBackedSecurityInput(p_nominal, p_vanilla_bond_template, p_fixings):
    '''
    @args:
        1. p_nominal: double
        2. p_vanilla_bond_template: dqproto.VanillaBondTemplate
        3. p_fixings: dqproto.TimeSeries
    @return:
        dqproto.BuildAssetBackedSecurityInput
    '''
    try:
        tmp_this= BuildAssetBackedSecurityInput()
        tmp_this.nominal=p_nominal
        tmp_this.vanilla_bond_template.CopyFrom(p_vanilla_bond_template)
        tmp_this.fixings.CopyFrom(p_fixings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildAssetBackedSecurityOutput
def dqCreateProtoBuildAssetBackedSecurityOutput(p_instrument, p_success, p_err_msg):
    '''
    @args:
        1. p_instrument: dqproto.AssetBackedSecurity
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildAssetBackedSecurityOutput
    '''
    try:
        tmp_this= BuildAssetBackedSecurityOutput()
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildMortgageBackedSecurityInput
def dqCreateProtoBuildMortgageBackedSecurityInput(p_nominal, p_vanilla_bond_template, p_fixings):
    '''
    @args:
        1. p_nominal: double
        2. p_vanilla_bond_template: dqproto.VanillaBondTemplate
        3. p_fixings: dqproto.TimeSeries
    @return:
        dqproto.BuildMortgageBackedSecurityInput
    '''
    try:
        tmp_this= BuildMortgageBackedSecurityInput()
        tmp_this.nominal=p_nominal
        tmp_this.vanilla_bond_template.CopyFrom(p_vanilla_bond_template)
        tmp_this.fixings.CopyFrom(p_fixings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildMortgageBackedSecurityOutput
def dqCreateProtoBuildMortgageBackedSecurityOutput(p_instrument, p_success, p_err_msg):
    '''
    @args:
        1. p_instrument: dqproto.MortgageBackedSecurity
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildMortgageBackedSecurityOutput
    '''
    try:
        tmp_this= BuildMortgageBackedSecurityOutput()
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildCallableBondInput
def dqCreateProtoBuildCallableBondInput(p_nominal, p_callable_bond_template):
    '''
    @args:
        1. p_nominal: double
        2. p_callable_bond_template: dqproto.CallableBondTemplate
    @return:
        dqproto.BuildCallableBondInput
    '''
    try:
        tmp_this= BuildCallableBondInput()
        tmp_this.nominal=p_nominal
        tmp_this.callable_bond_template.CopyFrom(p_callable_bond_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildCallableBondOutput
def dqCreateProtoBuildCallableBondOutput(p_callable_bond, p_success, p_err_msg):
    '''
    @args:
        1. p_callable_bond: dqproto.CallableBond
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildCallableBondOutput
    '''
    try:
        tmp_this= BuildCallableBondOutput()
        tmp_this.callable_bond.CopyFrom(p_callable_bond)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildConvertibleBondInput
def dqCreateProtoBuildConvertibleBondInput(p_nominal, p_underlying_bond_template):
    '''
    @args:
        1. p_nominal: double
        2. p_underlying_bond_template: dqproto.VanillaBondTemplate
    @return:
        dqproto.BuildConvertibleBondInput
    '''
    try:
        tmp_this= BuildConvertibleBondInput()
        tmp_this.nominal=p_nominal
        tmp_this.underlying_bond_template.CopyFrom(p_underlying_bond_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildConvertibleBondOutput
def dqCreateProtoBuildConvertibleBondOutput(p_bond, p_success, p_err_msg):
    '''
    @args:
        1. p_bond: dqproto.ConvertibleBond
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildConvertibleBondOutput
    '''
    try:
        tmp_this= BuildConvertibleBondOutput()
        tmp_this.bond.CopyFrom(p_bond)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildExchangeableBondInput
def dqCreateProtoBuildExchangeableBondInput(p_nominal, p_underlying_bond_template):
    '''
    @args:
        1. p_nominal: double
        2. p_underlying_bond_template: dqproto.VanillaBondTemplate
    @return:
        dqproto.BuildExchangeableBondInput
    '''
    try:
        tmp_this= BuildExchangeableBondInput()
        tmp_this.nominal=p_nominal
        tmp_this.underlying_bond_template.CopyFrom(p_underlying_bond_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildExchangeableBondOutput
def dqCreateProtoBuildExchangeableBondOutput(p_bond, p_success, p_err_msg):
    '''
    @args:
        1. p_bond: dqproto.ExchangeableBond
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildExchangeableBondOutput
    '''
    try:
        tmp_this= BuildExchangeableBondOutput()
        tmp_this.bond.CopyFrom(p_bond)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildExtendibleBondInput
def dqCreateProtoBuildExtendibleBondInput(p_nominal, p_underlying_bond_template):
    '''
    @args:
        1. p_nominal: double
        2. p_underlying_bond_template: dqproto.VanillaBondTemplate
    @return:
        dqproto.BuildExtendibleBondInput
    '''
    try:
        tmp_this= BuildExtendibleBondInput()
        tmp_this.nominal=p_nominal
        tmp_this.underlying_bond_template.CopyFrom(p_underlying_bond_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildExtendibleBondOutput
def dqCreateProtoBuildExtendibleBondOutput(p_bond, p_success, p_err_msg):
    '''
    @args:
        1. p_bond: dqproto.ExtendibleBond
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildExtendibleBondOutput
    '''
    try:
        tmp_this= BuildExtendibleBondOutput()
        tmp_this.bond.CopyFrom(p_bond)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildBondForwardInput
def dqCreateProtoBuildBondForwardInput(p_nominal, p_underlying_bond_template):
    '''
    @args:
        1. p_nominal: double
        2. p_underlying_bond_template: dqproto.VanillaBondTemplate
    @return:
        dqproto.BuildBondForwardInput
    '''
    try:
        tmp_this= BuildBondForwardInput()
        tmp_this.nominal=p_nominal
        tmp_this.underlying_bond_template.CopyFrom(p_underlying_bond_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildBondForwardOutput
def dqCreateProtoBuildBondForwardOutput(p_instrument, p_success, p_err_msg):
    '''
    @args:
        1. p_instrument: dqproto.BondForward
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildBondForwardOutput
    '''
    try:
        tmp_this= BuildBondForwardOutput()
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildBondFutureInput
def dqCreateProtoBuildBondFutureInput(p_nominal, p_underlying_bond_template):
    '''
    @args:
        1. p_nominal: double
        2. p_underlying_bond_template: dqproto.VanillaBondTemplate
    @return:
        dqproto.BuildBondFutureInput
    '''
    try:
        tmp_this= BuildBondFutureInput()
        tmp_this.nominal=p_nominal
        tmp_this.underlying_bond_template.CopyFrom(p_underlying_bond_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildBondFutureOutput
def dqCreateProtoBuildBondFutureOutput(p_instrument, p_success, p_err_msg):
    '''
    @args:
        1. p_instrument: dqproto.BondFuture
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildBondFutureOutput
    '''
    try:
        tmp_this= BuildBondFutureOutput()
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildBondPledgedRepoInput
def dqCreateProtoBuildBondPledgedRepoInput(p_nominal, p_underlying_bond_template):
    '''
    @args:
        1. p_nominal: double
        2. p_underlying_bond_template: dqproto.VanillaBondTemplate
    @return:
        dqproto.BuildBondPledgedRepoInput
    '''
    try:
        tmp_this= BuildBondPledgedRepoInput()
        tmp_this.nominal=p_nominal
        tmp_this.underlying_bond_template.CopyFrom(p_underlying_bond_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildBondPledgedRepoOutput
def dqCreateProtoBuildBondPledgedRepoOutput(p_instrument, p_success, p_err_msg):
    '''
    @args:
        1. p_instrument: dqproto.BondPledgedRepo
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildBondPledgedRepoOutput
    '''
    try:
        tmp_this= BuildBondPledgedRepoOutput()
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildBondOutrightRepoInput
def dqCreateProtoBuildBondOutrightRepoInput(p_nominal, p_underlying_bond_template):
    '''
    @args:
        1. p_nominal: double
        2. p_underlying_bond_template: dqproto.VanillaBondTemplate
    @return:
        dqproto.BuildBondOutrightRepoInput
    '''
    try:
        tmp_this= BuildBondOutrightRepoInput()
        tmp_this.nominal=p_nominal
        tmp_this.underlying_bond_template.CopyFrom(p_underlying_bond_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildBondOutrightRepoOutput
def dqCreateProtoBuildBondOutrightRepoOutput(p_instrument, p_success, p_err_msg):
    '''
    @args:
        1. p_instrument: dqproto.BondOutrightRepo
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildBondOutrightRepoOutput
    '''
    try:
        tmp_this= BuildBondOutrightRepoOutput()
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildCallableStepUpBondInput
def dqCreateProtoBuildCallableStepUpBondInput(p_nominal, p_underlying_bond_template):
    '''
    @args:
        1. p_nominal: double
        2. p_underlying_bond_template: dqproto.VanillaBondTemplate
    @return:
        dqproto.BuildCallableStepUpBondInput
    '''
    try:
        tmp_this= BuildCallableStepUpBondInput()
        tmp_this.nominal=p_nominal
        tmp_this.underlying_bond_template.CopyFrom(p_underlying_bond_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildCallableStepUpBondOutput
def dqCreateProtoBuildCallableStepUpBondOutput(p_instrument, p_success, p_err_msg):
    '''
    @args:
        1. p_instrument: dqproto.CallableStepUpBond
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildCallableStepUpBondOutput
    '''
    try:
        tmp_this= BuildCallableStepUpBondOutput()
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildBondEuropeanOptionInput
def dqCreateProtoBuildBondEuropeanOptionInput(p_nominal, p_underlying_bond_template):
    '''
    @args:
        1. p_nominal: double
        2. p_underlying_bond_template: dqproto.VanillaBondTemplate
    @return:
        dqproto.BuildBondEuropeanOptionInput
    '''
    try:
        tmp_this= BuildBondEuropeanOptionInput()
        tmp_this.nominal=p_nominal
        tmp_this.underlying_bond_template.CopyFrom(p_underlying_bond_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildBondEuropeanOptionOutput
def dqCreateProtoBuildBondEuropeanOptionOutput(p_instrument, p_success, p_err_msg):
    '''
    @args:
        1. p_instrument: dqproto.BondEuropeanOption
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildBondEuropeanOptionOutput
    '''
    try:
        tmp_this= BuildBondEuropeanOptionOutput()
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildBondAmericanOptionInput
def dqCreateProtoBuildBondAmericanOptionInput(p_nominal, p_underlying_bond_template):
    '''
    @args:
        1. p_nominal: double
        2. p_underlying_bond_template: dqproto.VanillaBondTemplate
    @return:
        dqproto.BuildBondAmericanOptionInput
    '''
    try:
        tmp_this= BuildBondAmericanOptionInput()
        tmp_this.nominal=p_nominal
        tmp_this.underlying_bond_template.CopyFrom(p_underlying_bond_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildBondAmericanOptionOutput
def dqCreateProtoBuildBondAmericanOptionOutput(p_instrument, p_success, p_err_msg):
    '''
    @args:
        1. p_instrument: dqproto.BondAmericanOption
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildBondAmericanOptionOutput
    '''
    try:
        tmp_this= BuildBondAmericanOptionOutput()
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxMarketConventions
def dqCreateProtoFxMarketConventions(p_atm_type, p_short_delta_type, p_long_delta_type, p_short_delta_cutoff, p_risk_reversal, p_smile_quote_type, p_currency_pair):
    '''
    @args:
        1. p_atm_type: dqproto.AtmType
        2. p_short_delta_type: dqproto.DeltaType
        3. p_long_delta_type: dqproto.DeltaType
        4. p_short_delta_cutoff: dqproto.Period
        5. p_risk_reversal: dqproto.RiskReversal
        6. p_smile_quote_type: dqproto.SmileQuoteType
        7. p_currency_pair: dqproto.CurrencyPair
    @return:
        dqproto.FxMarketConventions
    '''
    try:
        tmp_this= FxMarketConventions()
        tmp_this.atm_type=p_atm_type
        tmp_this.short_delta_type=p_short_delta_type
        tmp_this.long_delta_type=p_long_delta_type
        tmp_this.short_delta_cutoff.CopyFrom(p_short_delta_cutoff)
        tmp_this.risk_reversal=p_risk_reversal
        tmp_this.smile_quote_type=p_smile_quote_type
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxOptionQuoteMatrix
def dqCreateProtoFxOptionQuoteMatrix(p_as_of_date, p_quote_smiles, p_asset_name):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_quote_smiles: dqproto.OptionQuoteVector
        3. p_asset_name: string
    @return:
        dqproto.FxOptionQuoteMatrix
    '''
    try:
        tmp_this= FxOptionQuoteMatrix()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.quote_smiles.extend(p_quote_smiles)
        tmp_this.asset_name=p_asset_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxVolatilitySurface
def dqCreateProtoFxVolatilitySurface(p_volatility_surface, p_currency_pair, p_market_conventions):
    '''
    @args:
        1. p_volatility_surface: dqproto.VolatilitySurface
        2. p_currency_pair: dqproto.CurrencyPair
        3. p_market_conventions: dqproto.FxMarketConventions
    @return:
        dqproto.FxVolatilitySurface
    '''
    try:
        tmp_this= FxVolatilitySurface()
        tmp_this.volatility_surface.CopyFrom(p_volatility_surface)
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.market_conventions.CopyFrom(p_market_conventions)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxMktDataSet
def dqCreateProtoFxMktDataSet(p_as_of_date, p_domestic_discount_curve, p_foreign_discount_curve, p_spot, p_vol_surf):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_domestic_discount_curve: dqproto.IrYieldCurve
        3. p_foreign_discount_curve: dqproto.IrYieldCurve
        4. p_spot: dqproto.FxSpotRate
        5. p_vol_surf: dqproto.VolatilitySurface
    @return:
        dqproto.FxMktDataSet
    '''
    try:
        tmp_this= FxMktDataSet()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.domestic_discount_curve.CopyFrom(p_domestic_discount_curve)
        tmp_this.foreign_discount_curve.CopyFrom(p_foreign_discount_curve)
        tmp_this.spot.CopyFrom(p_spot)
        tmp_this.vol_surf.CopyFrom(p_vol_surf)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxRiskSettings
def dqCreateProtoFxRiskSettings(p_ir_curve_settings, p_price_settings, p_vol_settings, p_price_vol_settings, p_theta_settings):
    '''
    @args:
        1. p_ir_curve_settings: dqproto.IrCurveRiskSettings
        2. p_price_settings: dqproto.PriceRiskSettings
        3. p_vol_settings: dqproto.VolRiskSettings
        4. p_price_vol_settings: dqproto.PriceVolRiskSettings
        5. p_theta_settings: dqproto.ThetaRiskSettings
    @return:
        dqproto.FxRiskSettings
    '''
    try:
        tmp_this= FxRiskSettings()
        tmp_this.ir_curve_settings.CopyFrom(p_ir_curve_settings)
        tmp_this.price_settings.CopyFrom(p_price_settings)
        tmp_this.vol_settings.CopyFrom(p_vol_settings)
        tmp_this.price_vol_settings.CopyFrom(p_price_vol_settings)
        tmp_this.theta_settings.CopyFrom(p_theta_settings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxForwardPricingInput
def dqCreateProtoFxForwardPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.FxForward
        3. p_mkt_data: dqproto.FxMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FxRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.FxForwardPricingInput
    '''
    try:
        tmp_this= FxForwardPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxForwardPricingOutput
def dqCreateProtoFxForwardPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FxForwardPricingOutput
    '''
    try:
        tmp_this= FxForwardPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxNonDeliverableForwardPricingInput
def dqCreateProtoFxNonDeliverableForwardPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.FxNonDeliverableForward
        3. p_mkt_data: dqproto.FxMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FxRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.FxNonDeliverableForwardPricingInput
    '''
    try:
        tmp_this= FxNonDeliverableForwardPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxNonDeliverableForwardPricingOutput
def dqCreateProtoFxNonDeliverableForwardPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FxNonDeliverableForwardPricingOutput
    '''
    try:
        tmp_this= FxNonDeliverableForwardPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSwapPricingInput
def dqCreateProtoFxSwapPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.FxSwap
        3. p_mkt_data: dqproto.FxMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FxRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.FxSwapPricingInput
    '''
    try:
        tmp_this= FxSwapPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSwapPricingOutput
def dqCreateProtoFxSwapPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FxSwapPricingOutput
    '''
    try:
        tmp_this= FxSwapPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxTimeOptionPricingInput
def dqCreateProtoFxTimeOptionPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.FxTimeOption
        3. p_mkt_data: dqproto.FxMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FxRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.FxTimeOptionPricingInput
    '''
    try:
        tmp_this= FxTimeOptionPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxTimeOptionPricingOutput
def dqCreateProtoFxTimeOptionPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FxTimeOptionPricingOutput
    '''
    try:
        tmp_this= FxTimeOptionPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateFxOptionQuoteMatrixInput
def dqCreateProtoCreateFxOptionQuoteMatrixInput(p_currency_pair, p_as_of_date, p_terms, p_quote_names, p_quotes):
    '''
    @args:
        1. p_currency_pair: dqproto.CurrencyPair
        2. p_as_of_date: dqproto.Date
        3. p_terms: string
        4. p_quote_names: string
        5. p_quotes: dqproto.Matrix
    @return:
        dqproto.CreateFxOptionQuoteMatrixInput
    '''
    try:
        tmp_this= CreateFxOptionQuoteMatrixInput()
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.terms.extend(p_terms)
        tmp_this.quote_names.extend(p_quote_names)
        tmp_this.quotes.CopyFrom(p_quotes)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateFxOptionQuoteMatrixOutput
def dqCreateProtoCreateFxOptionQuoteMatrixOutput(p_fx_option_quote_matrix, p_success, p_err_msg):
    '''
    @args:
        1. p_fx_option_quote_matrix: dqproto.FxOptionQuoteMatrix
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateFxOptionQuoteMatrixOutput
    '''
    try:
        tmp_this= CreateFxOptionQuoteMatrixOutput()
        tmp_this.fx_option_quote_matrix.CopyFrom(p_fx_option_quote_matrix)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxVolatilitySurfaceBuildingInput
def dqCreateProtoFxVolatilitySurfaceBuildingInput(p_reference_date, p_currency_pair, p_market_conventions, p_quotes, p_fx_spot_rate, p_domestic_discount_curve, p_foreign_discount_curve, p_definition, p_settings, p_name):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_currency_pair: dqproto.CurrencyPair
        3. p_market_conventions: dqproto.FxMarketConventions
        4. p_quotes: dqproto.FxOptionQuoteMatrix
        5. p_fx_spot_rate: dqproto.FxSpotRate
        6. p_domestic_discount_curve: dqproto.IrYieldCurve
        7. p_foreign_discount_curve: dqproto.IrYieldCurve
        8. p_definition: dqproto.VolatilitySurfaceDefinition
        9. p_settings: dqproto.VolatilitySurfaceBuildSettings
        10. p_name: string
    @return:
        dqproto.FxVolatilitySurfaceBuildingInput
    '''
    try:
        tmp_this= FxVolatilitySurfaceBuildingInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.market_conventions.CopyFrom(p_market_conventions)
        tmp_this.quotes.CopyFrom(p_quotes)
        tmp_this.fx_spot_rate.CopyFrom(p_fx_spot_rate)
        tmp_this.domestic_discount_curve.CopyFrom(p_domestic_discount_curve)
        tmp_this.foreign_discount_curve.CopyFrom(p_foreign_discount_curve)
        tmp_this.definition.CopyFrom(p_definition)
        tmp_this.settings.CopyFrom(p_settings)
        tmp_this.name=p_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxVolatilitySurfaceBuildingOutput
def dqCreateProtoFxVolatilitySurfaceBuildingOutput(p_fx_volatility_surface, p_atm_vol_curve, p_success, p_err_msg):
    '''
    @args:
        1. p_fx_volatility_surface: dqproto.FxVolatilitySurface
        2. p_atm_vol_curve: dqproto.VolatilityCurve
        3. p_success: bool
        4. p_err_msg: string
    @return:
        dqproto.FxVolatilitySurfaceBuildingOutput
    '''
    try:
        tmp_this= FxVolatilitySurfaceBuildingOutput()
        tmp_this.fx_volatility_surface.CopyFrom(p_fx_volatility_surface)
        tmp_this.atm_vol_curve.CopyFrom(p_atm_vol_curve)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateFxVolatilitySurfaceInput
def dqCreateProtoCreateFxVolatilitySurfaceInput(p_reference_date, p_currency_pair, p_term_dates, p_strikes, p_volatilities, p_definition, p_name, p_market_conventions):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_currency_pair: dqproto.CurrencyPair
        3. p_term_dates: dqproto.Date
        4. p_strikes: dqproto.Vector
        5. p_volatilities: dqproto.Vector
        6. p_definition: dqproto.VolatilitySurfaceDefinition
        7. p_name: string
        8. p_market_conventions: dqproto.FxMarketConventions
    @return:
        dqproto.CreateFxVolatilitySurfaceInput
    '''
    try:
        tmp_this= CreateFxVolatilitySurfaceInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.term_dates.extend(p_term_dates)
        tmp_this.strikes.extend(p_strikes)
        tmp_this.volatilities.extend(p_volatilities)
        tmp_this.definition.CopyFrom(p_definition)
        tmp_this.name=p_name
        tmp_this.market_conventions.CopyFrom(p_market_conventions)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateFxVolatilitySurfaceOutput
def dqCreateProtoCreateFxVolatilitySurfaceOutput(p_fx_volatility_surface, p_success, p_err_msg):
    '''
    @args:
        1. p_fx_volatility_surface: dqproto.FxVolatilitySurface
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateFxVolatilitySurfaceOutput
    '''
    try:
        tmp_this= CreateFxVolatilitySurfaceOutput()
        tmp_this.fx_volatility_surface.CopyFrom(p_fx_volatility_surface)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxPricingInput
def dqCreateProtoFxPricingInput(p_pricing_date, p_currency_pair, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_currency_pair_bin, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin, p_scn_settings):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_currency_pair: dqproto.CurrencyPair
        3. p_mkt_data: dqproto.FxMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.FxRiskSettings
        6. p_use_binary: bool
        7. p_currency_pair_bin: bytes
        8. p_instrument_bin: bytes
        9. p_mkt_data_bin: bytes
        10. p_pricing_settings_bin: bytes
        11. p_risk_settings_bin: bytes
        12. p_scn_settings: dqproto.ScnAnalysisSettings
    @return:
        dqproto.FxPricingInput
    '''
    try:
        tmp_this= FxPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.currency_pair_bin=p_currency_pair_bin
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        tmp_this.scn_settings.CopyFrom(p_scn_settings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxPricingOutput
def dqCreateProtoFxPricingOutput(p_results, p_success, p_err_msg, p_scn_results, p_scn_prices, p_scn_vols):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
        4. p_scn_results: dqproto.Matrix
        5. p_scn_prices: dqproto.Vector
        6. p_scn_vols: dqproto.Vector
    @return:
        dqproto.FxPricingOutput
    '''
    try:
        tmp_this= FxPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        tmp_this.scn_results.CopyFrom(p_scn_results)
        tmp_this.scn_prices.CopyFrom(p_scn_prices)
        tmp_this.scn_vols.CopyFrom(p_scn_vols)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxEuropeanOptionPricingInput
def dqCreateProtoFxEuropeanOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.EuropeanOption
    @return:
        dqproto.FxEuropeanOptionPricingInput
    '''
    try:
        tmp_this= FxEuropeanOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxAmericanOptionPricingInput
def dqCreateProtoFxAmericanOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.AmericanOption
    @return:
        dqproto.FxAmericanOptionPricingInput
    '''
    try:
        tmp_this= FxAmericanOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxAsianOptionPricingInput
def dqCreateProtoFxAsianOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.AsianOption
    @return:
        dqproto.FxAsianOptionPricingInput
    '''
    try:
        tmp_this= FxAsianOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxDigitalOptionPricingInput
def dqCreateProtoFxDigitalOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.DigitalOption
    @return:
        dqproto.FxDigitalOptionPricingInput
    '''
    try:
        tmp_this= FxDigitalOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxOneTouchOptionPricingInput
def dqCreateProtoFxOneTouchOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.OneTouchOption
    @return:
        dqproto.FxOneTouchOptionPricingInput
    '''
    try:
        tmp_this= FxOneTouchOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxDoubleTouchOptionPricingInput
def dqCreateProtoFxDoubleTouchOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.DoubleTouchOption
    @return:
        dqproto.FxDoubleTouchOptionPricingInput
    '''
    try:
        tmp_this= FxDoubleTouchOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSingleBarrierOptionPricingInput
def dqCreateProtoFxSingleBarrierOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.SingleBarrierOption
    @return:
        dqproto.FxSingleBarrierOptionPricingInput
    '''
    try:
        tmp_this= FxSingleBarrierOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxDoubleBarrierOptionPricingInput
def dqCreateProtoFxDoubleBarrierOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.DoubleBarrierOption
    @return:
        dqproto.FxDoubleBarrierOptionPricingInput
    '''
    try:
        tmp_this= FxDoubleBarrierOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSingleSharkFinOptionPricingInput
def dqCreateProtoFxSingleSharkFinOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.SingleSharkFinOption
    @return:
        dqproto.FxSingleSharkFinOptionPricingInput
    '''
    try:
        tmp_this= FxSingleSharkFinOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxDoubleSharkFinOptionPricingInput
def dqCreateProtoFxDoubleSharkFinOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.DoubleSharkFinOption
    @return:
        dqproto.FxDoubleSharkFinOptionPricingInput
    '''
    try:
        tmp_this= FxDoubleSharkFinOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxPingPongOptionPricingInput
def dqCreateProtoFxPingPongOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.PingPongOption
    @return:
        dqproto.FxPingPongOptionPricingInput
    '''
    try:
        tmp_this= FxPingPongOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxAirbagOptionPricingInput
def dqCreateProtoFxAirbagOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.AirbagOption
    @return:
        dqproto.FxAirbagOptionPricingInput
    '''
    try:
        tmp_this= FxAirbagOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxRangeAccrualOptionPricingInput
def dqCreateProtoFxRangeAccrualOptionPricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.RangeAccrualOption
    @return:
        dqproto.FxRangeAccrualOptionPricingInput
    '''
    try:
        tmp_this= FxRangeAccrualOptionPricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxPhoenixAutoCallableNotePricingInput
def dqCreateProtoFxPhoenixAutoCallableNotePricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.PhoenixAutoCallableNote
    @return:
        dqproto.FxPhoenixAutoCallableNotePricingInput
    '''
    try:
        tmp_this= FxPhoenixAutoCallableNotePricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSnowballAutoCallableNotePricingInput
def dqCreateProtoFxSnowballAutoCallableNotePricingInput(p_pricing_input, p_instrument):
    '''
    @args:
        1. p_pricing_input: dqproto.FxPricingInput
        2. p_instrument: dqproto.SnowballAutoCallableNote
    @return:
        dqproto.FxSnowballAutoCallableNotePricingInput
    '''
    try:
        tmp_this= FxSnowballAutoCallableNotePricingInput()
        tmp_this.pricing_input.CopyFrom(p_pricing_input)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxPriceCalculationInput
def dqCreateProtoFxPriceCalculationInput(p_price, p_dest_ccy, p_fx_rate):
    '''
    @args:
        1. p_price: dqproto.Price
        2. p_dest_ccy: string
        3. p_fx_rate: dqproto.ForeignExchangeRate
    @return:
        dqproto.FxPriceCalculationInput
    '''
    try:
        tmp_this= FxPriceCalculationInput()
        tmp_this.price.CopyFrom(p_price)
        tmp_this.dest_ccy=p_dest_ccy
        tmp_this.fx_rate.CopyFrom(p_fx_rate)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxPriceCalculationOutput
def dqCreateProtoFxPriceCalculationOutput(p_price, p_success, p_err_msg):
    '''
    @args:
        1. p_price: dqproto.Price
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FxPriceCalculationOutput
    '''
    try:
        tmp_this= FxPriceCalculationOutput()
        tmp_this.price.CopyFrom(p_price)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxForwardRateCalculationInput
def dqCreateProtoFxForwardRateCalculationInput(p_calculation_date, p_currency_pair, p_delivery_date, p_fx_spot_rate, p_domestic_discount_curve, p_foreign_discount_curve):
    '''
    @args:
        1. p_calculation_date: dqproto.Date
        2. p_currency_pair: dqproto.CurrencyPair
        3. p_delivery_date: dqproto.Date
        4. p_fx_spot_rate: dqproto.FxSpotRate
        5. p_domestic_discount_curve: dqproto.IrYieldCurve
        6. p_foreign_discount_curve: dqproto.IrYieldCurve
    @return:
        dqproto.FxForwardRateCalculationInput
    '''
    try:
        tmp_this= FxForwardRateCalculationInput()
        tmp_this.calculation_date.CopyFrom(p_calculation_date)
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.fx_spot_rate.CopyFrom(p_fx_spot_rate)
        tmp_this.domestic_discount_curve.CopyFrom(p_domestic_discount_curve)
        tmp_this.foreign_discount_curve.CopyFrom(p_foreign_discount_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxForwardRateCalculationOutput
def dqCreateProtoFxForwardRateCalculationOutput(p_forward_rate, p_success, p_err_msg):
    '''
    @args:
        1. p_forward_rate: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FxForwardRateCalculationOutput
    '''
    try:
        tmp_this= FxForwardRateCalculationOutput()
        tmp_this.forward_rate=p_forward_rate
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSwapPointCalculationInput
def dqCreateProtoFxSwapPointCalculationInput(p_calculation_date, p_currency_pair, p_delivery_date, p_fx_spot_rate, p_domestic_discount_curve, p_foreign_discount_curve):
    '''
    @args:
        1. p_calculation_date: dqproto.Date
        2. p_currency_pair: dqproto.CurrencyPair
        3. p_delivery_date: dqproto.Date
        4. p_fx_spot_rate: dqproto.FxSpotRate
        5. p_domestic_discount_curve: dqproto.IrYieldCurve
        6. p_foreign_discount_curve: dqproto.IrYieldCurve
    @return:
        dqproto.FxSwapPointCalculationInput
    '''
    try:
        tmp_this= FxSwapPointCalculationInput()
        tmp_this.calculation_date.CopyFrom(p_calculation_date)
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.fx_spot_rate.CopyFrom(p_fx_spot_rate)
        tmp_this.domestic_discount_curve.CopyFrom(p_domestic_discount_curve)
        tmp_this.foreign_discount_curve.CopyFrom(p_foreign_discount_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSwapPointCalculationOutput
def dqCreateProtoFxSwapPointCalculationOutput(p_swap_point, p_success, p_err_msg):
    '''
    @args:
        1. p_swap_point: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FxSwapPointCalculationOutput
    '''
    try:
        tmp_this= FxSwapPointCalculationOutput()
        tmp_this.swap_point=p_swap_point
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxAtmStrikeCalculationInput
def dqCreateProtoFxAtmStrikeCalculationInput(p_atm_type, p_expiry_date, p_fx_spot_rate, p_domestic_discount_curve, p_foreign_discount_curve, p_volatility_surface):
    '''
    @args:
        1. p_atm_type: dqproto.AtmType
        2. p_expiry_date: dqproto.Date
        3. p_fx_spot_rate: dqproto.FxSpotRate
        4. p_domestic_discount_curve: dqproto.IrYieldCurve
        5. p_foreign_discount_curve: dqproto.IrYieldCurve
        6. p_volatility_surface: dqproto.FxVolatilitySurface
    @return:
        dqproto.FxAtmStrikeCalculationInput
    '''
    try:
        tmp_this= FxAtmStrikeCalculationInput()
        tmp_this.atm_type=p_atm_type
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.fx_spot_rate.CopyFrom(p_fx_spot_rate)
        tmp_this.domestic_discount_curve.CopyFrom(p_domestic_discount_curve)
        tmp_this.foreign_discount_curve.CopyFrom(p_foreign_discount_curve)
        tmp_this.volatility_surface.CopyFrom(p_volatility_surface)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxAtmStrikeCalculationOutput
def dqCreateProtoFxAtmStrikeCalculationOutput(p_strike, p_success, p_err_msg):
    '''
    @args:
        1. p_strike: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FxAtmStrikeCalculationOutput
    '''
    try:
        tmp_this= FxAtmStrikeCalculationOutput()
        tmp_this.strike=p_strike
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxDeltaToStrikeCalculationInput
def dqCreateProtoFxDeltaToStrikeCalculationInput(p_delta_type, p_delta, p_option_type, p_expiry_date, p_fx_spot_rate, p_domestic_discount_curve, p_foreign_discount_curve, p_volatility_surface):
    '''
    @args:
        1. p_delta_type: dqproto.DeltaType
        2. p_delta: double
        3. p_option_type: dqproto.PayoffType
        4. p_expiry_date: dqproto.Date
        5. p_fx_spot_rate: dqproto.FxSpotRate
        6. p_domestic_discount_curve: dqproto.IrYieldCurve
        7. p_foreign_discount_curve: dqproto.IrYieldCurve
        8. p_volatility_surface: dqproto.FxVolatilitySurface
    @return:
        dqproto.FxDeltaToStrikeCalculationInput
    '''
    try:
        tmp_this= FxDeltaToStrikeCalculationInput()
        tmp_this.delta_type=p_delta_type
        tmp_this.delta=p_delta
        tmp_this.option_type=p_option_type
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.fx_spot_rate.CopyFrom(p_fx_spot_rate)
        tmp_this.domestic_discount_curve.CopyFrom(p_domestic_discount_curve)
        tmp_this.foreign_discount_curve.CopyFrom(p_foreign_discount_curve)
        tmp_this.volatility_surface.CopyFrom(p_volatility_surface)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxDeltaToStrikeCalculationOutput
def dqCreateProtoFxDeltaToStrikeCalculationOutput(p_strike, p_success, p_err_msg):
    '''
    @args:
        1. p_strike: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FxDeltaToStrikeCalculationOutput
    '''
    try:
        tmp_this= FxDeltaToStrikeCalculationOutput()
        tmp_this.strike=p_strike
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSpot
def dqCreateProtoFxSpot(p_buy_currency, p_buy_amount, p_sell_currency, p_sell_amount, p_delivery_date):
    '''
    @args:
        1. p_buy_currency: string
        2. p_buy_amount: double
        3. p_sell_currency: string
        4. p_sell_amount: double
        5. p_delivery_date: dqproto.Date
    @return:
        dqproto.FxSpot
    '''
    try:
        tmp_this= FxSpot()
        tmp_this.buy_currency=p_buy_currency
        tmp_this.buy_amount=p_buy_amount
        tmp_this.sell_currency=p_sell_currency
        tmp_this.sell_amount=p_sell_amount
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSpotTemplate
def dqCreateProtoFxSpotTemplate(p_type, p_name, p_currency_pair, p_spot_day_convention, p_calendar, p_spot_delay):
    '''
    @args:
        1. p_type: dqproto.InstrumentType
        2. p_name: string
        3. p_currency_pair: dqproto.CurrencyPair
        4. p_spot_day_convention: dqproto.BusinessDayConvention
        5. p_calendar: string
        6. p_spot_delay: dqproto.Period
    @return:
        dqproto.FxSpotTemplate
    '''
    try:
        tmp_this= FxSpotTemplate()
        tmp_this.type=p_type
        tmp_this.name=p_name
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.spot_day_convention=p_spot_day_convention
        tmp_this.calendar.extend(p_calendar)
        tmp_this.spot_delay.CopyFrom(p_spot_delay)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSpotTemplateList
def dqCreateProtoFxSpotTemplateList(p_fx_spot_template):
    '''
    @args:
        1. p_fx_spot_template: dqproto.FxSpotTemplate
    @return:
        dqproto.FxSpotTemplateList
    '''
    try:
        tmp_this= FxSpotTemplateList()
        tmp_this.fx_spot_template.extend(p_fx_spot_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxForward
def dqCreateProtoFxForward(p_buy_currency, p_buy_amount, p_sell_currency, p_sell_amount, p_delivery_date, p_expiry_date):
    '''
    @args:
        1. p_buy_currency: string
        2. p_buy_amount: double
        3. p_sell_currency: string
        4. p_sell_amount: double
        5. p_delivery_date: dqproto.Date
        6. p_expiry_date: dqproto.Date
    @return:
        dqproto.FxForward
    '''
    try:
        tmp_this= FxForward()
        tmp_this.buy_currency=p_buy_currency
        tmp_this.buy_amount=p_buy_amount
        tmp_this.sell_currency=p_sell_currency
        tmp_this.sell_amount=p_sell_amount
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxForwardTemplate
def dqCreateProtoFxForwardTemplate(p_type, p_name, p_fixing_offset, p_currency_pair, p_delivery_day_convention, p_fixing_day_convention, p_calendar):
    '''
    @args:
        1. p_type: dqproto.InstrumentType
        2. p_name: string
        3. p_fixing_offset: dqproto.Period
        4. p_currency_pair: dqproto.CurrencyPair
        5. p_delivery_day_convention: dqproto.BusinessDayConvention
        6. p_fixing_day_convention: dqproto.BusinessDayConvention
        7. p_calendar: string
    @return:
        dqproto.FxForwardTemplate
    '''
    try:
        tmp_this= FxForwardTemplate()
        tmp_this.type=p_type
        tmp_this.name=p_name
        tmp_this.fixing_offset.CopyFrom(p_fixing_offset)
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.delivery_day_convention=p_delivery_day_convention
        tmp_this.fixing_day_convention=p_fixing_day_convention
        tmp_this.calendar.extend(p_calendar)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxForwardTemplateList
def dqCreateProtoFxForwardTemplateList(p_fx_fwd_template):
    '''
    @args:
        1. p_fx_fwd_template: dqproto.FxForwardTemplate
    @return:
        dqproto.FxForwardTemplateList
    '''
    try:
        tmp_this= FxForwardTemplateList()
        tmp_this.fx_fwd_template.extend(p_fx_fwd_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxNonDeliverableForward
def dqCreateProtoFxNonDeliverableForward(p_buy_currency, p_buy_amount, p_sell_currency, p_sell_amount, p_delivery_date, p_expiry_date, p_settlement_currency):
    '''
    @args:
        1. p_buy_currency: string
        2. p_buy_amount: double
        3. p_sell_currency: string
        4. p_sell_amount: double
        5. p_delivery_date: dqproto.Date
        6. p_expiry_date: dqproto.Date
        7. p_settlement_currency: string
    @return:
        dqproto.FxNonDeliverableForward
    '''
    try:
        tmp_this= FxNonDeliverableForward()
        tmp_this.buy_currency=p_buy_currency
        tmp_this.buy_amount=p_buy_amount
        tmp_this.sell_currency=p_sell_currency
        tmp_this.sell_amount=p_sell_amount
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.settlement_currency=p_settlement_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxNdfTemplate
def dqCreateProtoFxNdfTemplate(p_type, p_name, p_fixing_offset, p_currency_pair, p_delivery_day_convention, p_fixing_day_convention, p_calendar, p_settlement_currency):
    '''
    @args:
        1. p_type: dqproto.InstrumentType
        2. p_name: string
        3. p_fixing_offset: dqproto.Period
        4. p_currency_pair: dqproto.CurrencyPair
        5. p_delivery_day_convention: dqproto.BusinessDayConvention
        6. p_fixing_day_convention: dqproto.BusinessDayConvention
        7. p_calendar: string
        8. p_settlement_currency: string
    @return:
        dqproto.FxNdfTemplate
    '''
    try:
        tmp_this= FxNdfTemplate()
        tmp_this.type=p_type
        tmp_this.name=p_name
        tmp_this.fixing_offset.CopyFrom(p_fixing_offset)
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.delivery_day_convention=p_delivery_day_convention
        tmp_this.fixing_day_convention=p_fixing_day_convention
        tmp_this.calendar.extend(p_calendar)
        tmp_this.settlement_currency=p_settlement_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxNdfTemplateList
def dqCreateProtoFxNdfTemplateList(p_fx_ndf_template):
    '''
    @args:
        1. p_fx_ndf_template: dqproto.FxNdfTemplate
    @return:
        dqproto.FxNdfTemplateList
    '''
    try:
        tmp_this= FxNdfTemplateList()
        tmp_this.fx_ndf_template.extend(p_fx_ndf_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSwap
def dqCreateProtoFxSwap(p_near_buy_currency, p_near_buy_amount, p_near_sell_currency, p_near_sell_amount, p_near_delivery_date, p_near_expiry_date, p_far_buy_currency, p_far_buy_amount, p_far_sell_currency, p_far_sell_amount, p_far_delivery_date, p_far_expiry_date):
    '''
    @args:
        1. p_near_buy_currency: string
        2. p_near_buy_amount: double
        3. p_near_sell_currency: string
        4. p_near_sell_amount: double
        5. p_near_delivery_date: dqproto.Date
        6. p_near_expiry_date: dqproto.Date
        7. p_far_buy_currency: string
        8. p_far_buy_amount: double
        9. p_far_sell_currency: string
        10. p_far_sell_amount: double
        11. p_far_delivery_date: dqproto.Date
        12. p_far_expiry_date: dqproto.Date
    @return:
        dqproto.FxSwap
    '''
    try:
        tmp_this= FxSwap()
        tmp_this.near_buy_currency=p_near_buy_currency
        tmp_this.near_buy_amount=p_near_buy_amount
        tmp_this.near_sell_currency=p_near_sell_currency
        tmp_this.near_sell_amount=p_near_sell_amount
        tmp_this.near_delivery_date.CopyFrom(p_near_delivery_date)
        tmp_this.near_expiry_date.CopyFrom(p_near_expiry_date)
        tmp_this.far_buy_currency=p_far_buy_currency
        tmp_this.far_buy_amount=p_far_buy_amount
        tmp_this.far_sell_currency=p_far_sell_currency
        tmp_this.far_sell_amount=p_far_sell_amount
        tmp_this.far_delivery_date.CopyFrom(p_far_delivery_date)
        tmp_this.far_expiry_date.CopyFrom(p_far_expiry_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSwapTemplate
def dqCreateProtoFxSwapTemplate(p_type, p_name, p_start_convention, p_currency_pair, p_calendar, p_start_day_convention, p_end_day_convention, p_fixing_offset, p_fixing_day_convetion):
    '''
    @args:
        1. p_type: dqproto.InstrumentType
        2. p_name: string
        3. p_start_convention: dqproto.InstrumentStartConvention
        4. p_currency_pair: dqproto.CurrencyPair
        5. p_calendar: string
        6. p_start_day_convention: dqproto.BusinessDayConvention
        7. p_end_day_convention: dqproto.BusinessDayConvention
        8. p_fixing_offset: dqproto.Period
        9. p_fixing_day_convetion: dqproto.BusinessDayConvention
    @return:
        dqproto.FxSwapTemplate
    '''
    try:
        tmp_this= FxSwapTemplate()
        tmp_this.type=p_type
        tmp_this.name=p_name
        tmp_this.start_convention=p_start_convention
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.calendar.extend(p_calendar)
        tmp_this.start_day_convention=p_start_day_convention
        tmp_this.end_day_convention=p_end_day_convention
        tmp_this.fixing_offset.CopyFrom(p_fixing_offset)
        tmp_this.fixing_day_convetion=p_fixing_day_convetion
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSwapTemplateList
def dqCreateProtoFxSwapTemplateList(p_fx_swap_template):
    '''
    @args:
        1. p_fx_swap_template: dqproto.FxSwapTemplate
    @return:
        dqproto.FxSwapTemplateList
    '''
    try:
        tmp_this= FxSwapTemplateList()
        tmp_this.fx_swap_template.extend(p_fx_swap_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxTimeOption
def dqCreateProtoFxTimeOption(p_buy_currency, p_buy_amount, p_sell_currency, p_sell_amount, p_delivery_date, p_exercise_start_date, p_exercise_end_date):
    '''
    @args:
        1. p_buy_currency: string
        2. p_buy_amount: double
        3. p_sell_currency: string
        4. p_sell_amount: double
        5. p_delivery_date: dqproto.Date
        6. p_exercise_start_date: dqproto.Date
        7. p_exercise_end_date: dqproto.Date
    @return:
        dqproto.FxTimeOption
    '''
    try:
        tmp_this= FxTimeOption()
        tmp_this.buy_currency=p_buy_currency
        tmp_this.buy_amount=p_buy_amount
        tmp_this.sell_currency=p_sell_currency
        tmp_this.sell_amount=p_sell_amount
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.exercise_start_date.CopyFrom(p_exercise_start_date)
        tmp_this.exercise_end_date.CopyFrom(p_exercise_end_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxTimeOptionTemplate
def dqCreateProtoFxTimeOptionTemplate(p_type, p_name, p_fixing_offset, p_currency_pair, p_delivery_day_convention, p_fixing_day_convention, p_calendar):
    '''
    @args:
        1. p_type: dqproto.InstrumentType
        2. p_name: string
        3. p_fixing_offset: dqproto.Period
        4. p_currency_pair: dqproto.CurrencyPair
        5. p_delivery_day_convention: dqproto.BusinessDayConvention
        6. p_fixing_day_convention: dqproto.BusinessDayConvention
        7. p_calendar: string
    @return:
        dqproto.FxTimeOptionTemplate
    '''
    try:
        tmp_this= FxTimeOptionTemplate()
        tmp_this.type=p_type
        tmp_this.name=p_name
        tmp_this.fixing_offset.CopyFrom(p_fixing_offset)
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.delivery_day_convention=p_delivery_day_convention
        tmp_this.fixing_day_convention=p_fixing_day_convention
        tmp_this.calendar.extend(p_calendar)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxTimeOptionTemplateList
def dqCreateProtoFxTimeOptionTemplateList(p_fx_time_option_template):
    '''
    @args:
        1. p_fx_time_option_template: dqproto.FxTimeOptionTemplate
    @return:
        dqproto.FxTimeOptionTemplateList
    '''
    try:
        tmp_this= FxTimeOptionTemplateList()
        tmp_this.fx_time_option_template.extend(p_fx_time_option_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxEuropeanOption
def dqCreateProtoFxEuropeanOption(p_currency_pair, p_call_currency, p_nominal, p_strike, p_delivery_date, p_expiry_date, p_payoff_currency):
    '''
    @args:
        1. p_currency_pair: dqproto.CurrencyPair
        2. p_call_currency: string
        3. p_nominal: double
        4. p_strike: double
        5. p_delivery_date: dqproto.Date
        6. p_expiry_date: dqproto.Date
        7. p_payoff_currency: string
    @return:
        dqproto.FxEuropeanOption
    '''
    try:
        tmp_this= FxEuropeanOption()
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.call_currency=p_call_currency
        tmp_this.nominal=p_nominal
        tmp_this.strike=p_strike
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.payoff_currency=p_payoff_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxAmericanOption
def dqCreateProtoFxAmericanOption(p_currency_pair, p_call_currency, p_strike, p_expiry_date, p_delivery_date, p_settlement_days, p_nominal, p_payoff_currency):
    '''
    @args:
        1. p_currency_pair: dqproto.CurrencyPair
        2. p_call_currency: string
        3. p_strike: double
        4. p_expiry_date: dqproto.Date
        5. p_delivery_date: dqproto.Date
        6. p_settlement_days: int32
        7. p_nominal: double
        8. p_payoff_currency: string
    @return:
        dqproto.FxAmericanOption
    '''
    try:
        tmp_this= FxAmericanOption()
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.call_currency=p_call_currency
        tmp_this.strike=p_strike
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.settlement_days=p_settlement_days
        tmp_this.nominal=p_nominal
        tmp_this.payoff_currency=p_payoff_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxAsianOption
def dqCreateProtoFxAsianOption(p_call_currency, p_avg_method, p_obs_type, p_expiry_date, p_delivery_date, p_fixing_schedule, p_strike_type, p_strike, p_nominal, p_currency_pair, p_payoff_currency):
    '''
    @args:
        1. p_call_currency: string
        2. p_avg_method: dqproto.AveragingMethod
        3. p_obs_type: dqproto.EventObservationType
        4. p_expiry_date: dqproto.Date
        5. p_delivery_date: dqproto.Date
        6. p_fixing_schedule: dqproto.FixingSchedule
        7. p_strike_type: dqproto.StrikeType
        8. p_strike: double
        9. p_nominal: double
        10. p_currency_pair: dqproto.CurrencyPair
        11. p_payoff_currency: string
    @return:
        dqproto.FxAsianOption
    '''
    try:
        tmp_this= FxAsianOption()
        tmp_this.call_currency=p_call_currency
        tmp_this.avg_method=p_avg_method
        tmp_this.obs_type=p_obs_type
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.strike_type=p_strike_type
        tmp_this.strike=p_strike
        tmp_this.nominal=p_nominal
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.payoff_currency=p_payoff_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxDigitalOption
def dqCreateProtoFxDigitalOption(p_currency_pair, p_call_currency, p_expiry_date, p_delivery_date, p_strike, p_asset, p_cash, p_payoff_currency):
    '''
    @args:
        1. p_currency_pair: dqproto.CurrencyPair
        2. p_call_currency: string
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_strike: double
        6. p_asset: double
        7. p_cash: double
        8. p_payoff_currency: string
    @return:
        dqproto.FxDigitalOption
    '''
    try:
        tmp_this= FxDigitalOption()
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.call_currency=p_call_currency
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.strike=p_strike
        tmp_this.asset=p_asset
        tmp_this.cash=p_cash
        tmp_this.payoff_currency=p_payoff_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSingleBarrierOption
def dqCreateProtoFxSingleBarrierOption(p_call_currency, p_strike, p_expiry_date, p_delivery_date, p_barrier_type, p_barrier_value, p_payment_type, p_cash_rebate, p_asset_rebate, p_nominal, p_currency_pair, p_settlement_days, p_payoff_currency, p_obs_type, p_fixing_schedule):
    '''
    @args:
        1. p_call_currency: string
        2. p_strike: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_barrier_type: dqproto.BarrierType
        6. p_barrier_value: double
        7. p_payment_type: dqproto.PaymentType
        8. p_cash_rebate: double
        9. p_asset_rebate: double
        10. p_nominal: double
        11. p_currency_pair: dqproto.CurrencyPair
        12. p_settlement_days: int32
        13. p_payoff_currency: string
        14. p_obs_type: dqproto.EventObservationType
        15. p_fixing_schedule: dqproto.FixingSchedule
    @return:
        dqproto.FxSingleBarrierOption
    '''
    try:
        tmp_this= FxSingleBarrierOption()
        tmp_this.call_currency=p_call_currency
        tmp_this.strike=p_strike
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.barrier_type=p_barrier_type
        tmp_this.barrier_value=p_barrier_value
        tmp_this.payment_type=p_payment_type
        tmp_this.cash_rebate=p_cash_rebate
        tmp_this.asset_rebate=p_asset_rebate
        tmp_this.nominal=p_nominal
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.settlement_days=p_settlement_days
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.obs_type=p_obs_type
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxDoubleBarrierOption
def dqCreateProtoFxDoubleBarrierOption(p_call_currency, p_strike, p_expiry_date, p_delivery_date, p_lower_barrier_type, p_lower_barrier_value, p_upper_barrier_type, p_upper_barrier_value, p_payment_type, p_lower_cash_rebate, p_lower_asset_rebate, p_upper_cash_rebate, p_upper_asset_rebate, p_nominal, p_currency_pair, p_settlement_days, p_payoff_currency, p_obs_type, p_fixing_schedule):
    '''
    @args:
        1. p_call_currency: string
        2. p_strike: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_lower_barrier_type: dqproto.BarrierType
        6. p_lower_barrier_value: double
        7. p_upper_barrier_type: dqproto.BarrierType
        8. p_upper_barrier_value: double
        9. p_payment_type: dqproto.PaymentType
        10. p_lower_cash_rebate: double
        11. p_lower_asset_rebate: double
        12. p_upper_cash_rebate: double
        13. p_upper_asset_rebate: double
        14. p_nominal: double
        15. p_currency_pair: dqproto.CurrencyPair
        16. p_settlement_days: int32
        17. p_payoff_currency: string
        18. p_obs_type: dqproto.EventObservationType
        19. p_fixing_schedule: dqproto.FixingSchedule
    @return:
        dqproto.FxDoubleBarrierOption
    '''
    try:
        tmp_this= FxDoubleBarrierOption()
        tmp_this.call_currency=p_call_currency
        tmp_this.strike=p_strike
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.lower_barrier_type=p_lower_barrier_type
        tmp_this.lower_barrier_value=p_lower_barrier_value
        tmp_this.upper_barrier_type=p_upper_barrier_type
        tmp_this.upper_barrier_value=p_upper_barrier_value
        tmp_this.payment_type=p_payment_type
        tmp_this.lower_cash_rebate=p_lower_cash_rebate
        tmp_this.lower_asset_rebate=p_lower_asset_rebate
        tmp_this.upper_cash_rebate=p_upper_cash_rebate
        tmp_this.upper_asset_rebate=p_upper_asset_rebate
        tmp_this.nominal=p_nominal
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.settlement_days=p_settlement_days
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.obs_type=p_obs_type
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxOneTouchOption
def dqCreateProtoFxOneTouchOption(p_asset, p_cash, p_expiry_date, p_delivery_date, p_barrier, p_payment_type, p_nominal, p_currency_pair, p_settlement_days, p_payoff_currency, p_obs_type, p_fixing_schedule):
    '''
    @args:
        1. p_asset: double
        2. p_cash: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_barrier: dqproto.Barrier
        6. p_payment_type: dqproto.PaymentType
        7. p_nominal: double
        8. p_currency_pair: dqproto.CurrencyPair
        9. p_settlement_days: int32
        10. p_payoff_currency: string
        11. p_obs_type: dqproto.EventObservationType
        12. p_fixing_schedule: dqproto.FixingSchedule
    @return:
        dqproto.FxOneTouchOption
    '''
    try:
        tmp_this= FxOneTouchOption()
        tmp_this.asset=p_asset
        tmp_this.cash=p_cash
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.barrier.CopyFrom(p_barrier)
        tmp_this.payment_type=p_payment_type
        tmp_this.nominal=p_nominal
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.settlement_days=p_settlement_days
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.obs_type=p_obs_type
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxDoubleTouchOption
def dqCreateProtoFxDoubleTouchOption(p_asset, p_cash, p_expiry_date, p_delivery_date, p_lower_barrier, p_upper_barrier, p_payment_type, p_nominal, p_currency_pair, p_settlement_days, p_payoff_currency, p_obs_type, p_fixing_schedule):
    '''
    @args:
        1. p_asset: double
        2. p_cash: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_lower_barrier: dqproto.Barrier
        6. p_upper_barrier: dqproto.Barrier
        7. p_payment_type: dqproto.PaymentType
        8. p_nominal: double
        9. p_currency_pair: dqproto.CurrencyPair
        10. p_settlement_days: int32
        11. p_payoff_currency: string
        12. p_obs_type: dqproto.EventObservationType
        13. p_fixing_schedule: dqproto.FixingSchedule
    @return:
        dqproto.FxDoubleTouchOption
    '''
    try:
        tmp_this= FxDoubleTouchOption()
        tmp_this.asset=p_asset
        tmp_this.cash=p_cash
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.lower_barrier.CopyFrom(p_lower_barrier)
        tmp_this.upper_barrier.CopyFrom(p_upper_barrier)
        tmp_this.payment_type=p_payment_type
        tmp_this.nominal=p_nominal
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.settlement_days=p_settlement_days
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.obs_type=p_obs_type
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSingleSharkFinOption
def dqCreateProtoFxSingleSharkFinOption(p_call_currency, p_strike, p_expiry_date, p_delivery_date, p_gearing, p_performance_type, p_barrier_obs_type, p_barrier_type, p_barrier_value, p_cash_rebate, p_asset_rebate, p_fixing_schedule, p_nominal, p_currency_pair, p_payoff_currency):
    '''
    @args:
        1. p_call_currency: string
        2. p_strike: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_gearing: double
        6. p_performance_type: dqproto.PerformanceType
        7. p_barrier_obs_type: dqproto.EventObservationType
        8. p_barrier_type: dqproto.BarrierType
        9. p_barrier_value: double
        10. p_cash_rebate: double
        11. p_asset_rebate: double
        12. p_fixing_schedule: dqproto.FixingSchedule
        13. p_nominal: double
        14. p_currency_pair: dqproto.CurrencyPair
        15. p_payoff_currency: string
    @return:
        dqproto.FxSingleSharkFinOption
    '''
    try:
        tmp_this= FxSingleSharkFinOption()
        tmp_this.call_currency=p_call_currency
        tmp_this.strike=p_strike
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.gearing=p_gearing
        tmp_this.performance_type=p_performance_type
        tmp_this.barrier_obs_type=p_barrier_obs_type
        tmp_this.barrier_type=p_barrier_type
        tmp_this.barrier_value=p_barrier_value
        tmp_this.cash_rebate=p_cash_rebate
        tmp_this.asset_rebate=p_asset_rebate
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.nominal=p_nominal
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.payoff_currency=p_payoff_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxDoubleSharkFinOption
def dqCreateProtoFxDoubleSharkFinOption(p_lower_strike, p_upper_strike, p_expiry_date, p_delivery_date, p_lower_participation, p_upper_participation, p_barrier_obs_type, p_lower_barrier, p_upper_barrier, p_lower_cash_rebate, p_lower_asset_rebate, p_upper_cash_rebate, p_upper_asset_rebate, p_fixing_schedule, p_nominal, p_currency_pair, p_payoff_currency):
    '''
    @args:
        1. p_lower_strike: double
        2. p_upper_strike: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_lower_participation: double
        6. p_upper_participation: double
        7. p_barrier_obs_type: dqproto.EventObservationType
        8. p_lower_barrier: double
        9. p_upper_barrier: double
        10. p_lower_cash_rebate: double
        11. p_lower_asset_rebate: double
        12. p_upper_cash_rebate: double
        13. p_upper_asset_rebate: double
        14. p_fixing_schedule: dqproto.FixingSchedule
        15. p_nominal: double
        16. p_currency_pair: dqproto.CurrencyPair
        17. p_payoff_currency: string
    @return:
        dqproto.FxDoubleSharkFinOption
    '''
    try:
        tmp_this= FxDoubleSharkFinOption()
        tmp_this.lower_strike=p_lower_strike
        tmp_this.upper_strike=p_upper_strike
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.lower_participation=p_lower_participation
        tmp_this.upper_participation=p_upper_participation
        tmp_this.barrier_obs_type=p_barrier_obs_type
        tmp_this.lower_barrier=p_lower_barrier
        tmp_this.upper_barrier=p_upper_barrier
        tmp_this.lower_cash_rebate=p_lower_cash_rebate
        tmp_this.lower_asset_rebate=p_lower_asset_rebate
        tmp_this.upper_cash_rebate=p_upper_cash_rebate
        tmp_this.upper_asset_rebate=p_upper_asset_rebate
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.nominal=p_nominal
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.payoff_currency=p_payoff_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxPingPongOption
def dqCreateProtoFxPingPongOption(p_asset, p_cash, p_expiry_date, p_delivery_date, p_lower_barrier, p_upper_barrier, p_obs_type, p_fixing_schedule, p_payment_type, p_settlement_days, p_nominal, p_currency_pair, p_payoff_currency):
    '''
    @args:
        1. p_asset: double
        2. p_cash: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_lower_barrier: dqproto.Barrier
        6. p_upper_barrier: dqproto.Barrier
        7. p_obs_type: dqproto.EventObservationType
        8. p_fixing_schedule: dqproto.FixingSchedule
        9. p_payment_type: dqproto.PaymentType
        10. p_settlement_days: int32
        11. p_nominal: double
        12. p_currency_pair: dqproto.CurrencyPair
        13. p_payoff_currency: string
    @return:
        dqproto.FxPingPongOption
    '''
    try:
        tmp_this= FxPingPongOption()
        tmp_this.asset=p_asset
        tmp_this.cash=p_cash
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.lower_barrier.CopyFrom(p_lower_barrier)
        tmp_this.upper_barrier.CopyFrom(p_upper_barrier)
        tmp_this.obs_type=p_obs_type
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.payment_type=p_payment_type
        tmp_this.settlement_days=p_settlement_days
        tmp_this.nominal=p_nominal
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.payoff_currency=p_payoff_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxRangeAccrualOption
def dqCreateProtoFxRangeAccrualOption(p_expiry_date, p_delivery_date, p_asset, p_cash, p_lower_barrier, p_upper_barrier, p_fixing_schedule, p_nominal, p_currency_pair, p_payoff_currency):
    '''
    @args:
        1. p_expiry_date: dqproto.Date
        2. p_delivery_date: dqproto.Date
        3. p_asset: double
        4. p_cash: double
        5. p_lower_barrier: double
        6. p_upper_barrier: double
        7. p_fixing_schedule: dqproto.FixingSchedule
        8. p_nominal: double
        9. p_currency_pair: dqproto.CurrencyPair
        10. p_payoff_currency: string
    @return:
        dqproto.FxRangeAccrualOption
    '''
    try:
        tmp_this= FxRangeAccrualOption()
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.asset=p_asset
        tmp_this.cash=p_cash
        tmp_this.lower_barrier=p_lower_barrier
        tmp_this.upper_barrier=p_upper_barrier
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.nominal=p_nominal
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.payoff_currency=p_payoff_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxPhoenixAutoCallableNote
def dqCreateProtoFxPhoenixAutoCallableNote(p_coupon_payoff_type, p_coupon_strike, p_coupon_rate, p_start_date, p_coupon_dates, p_knock_out_barrier_type, p_knock_out_barrier_value, p_knock_out_sched, p_knock_in_barrier_type, p_knock_in_barrier_value, p_knock_in_sched, p_long_short, p_knock_in_payoff_type, p_knock_in_payoff_strike, p_expiry, p_delivery, p_nominal, p_currency_pair, p_settlement_days, p_payoff_currency):
    '''
    @args:
        1. p_coupon_payoff_type: dqproto.PayoffType
        2. p_coupon_strike: double
        3. p_coupon_rate: double
        4. p_start_date: dqproto.Date
        5. p_coupon_dates: dqproto.Date
        6. p_knock_out_barrier_type: dqproto.BarrierType
        7. p_knock_out_barrier_value: double
        8. p_knock_out_sched: dqproto.FixingSchedule
        9. p_knock_in_barrier_type: dqproto.BarrierType
        10. p_knock_in_barrier_value: double
        11. p_knock_in_sched: dqproto.FixingSchedule
        12. p_long_short: dqproto.BuySellFlag
        13. p_knock_in_payoff_type: dqproto.PayoffType
        14. p_knock_in_payoff_strike: double
        15. p_expiry: dqproto.Date
        16. p_delivery: dqproto.Date
        17. p_nominal: double
        18. p_currency_pair: dqproto.CurrencyPair
        19. p_settlement_days: int32
        20. p_payoff_currency: string
    @return:
        dqproto.FxPhoenixAutoCallableNote
    '''
    try:
        tmp_this= FxPhoenixAutoCallableNote()
        tmp_this.coupon_payoff_type=p_coupon_payoff_type
        tmp_this.coupon_strike=p_coupon_strike
        tmp_this.coupon_rate=p_coupon_rate
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.coupon_dates.extend(p_coupon_dates)
        tmp_this.knock_out_barrier_type=p_knock_out_barrier_type
        tmp_this.knock_out_barrier_value=p_knock_out_barrier_value
        tmp_this.knock_out_sched.CopyFrom(p_knock_out_sched)
        tmp_this.knock_in_barrier_type=p_knock_in_barrier_type
        tmp_this.knock_in_barrier_value=p_knock_in_barrier_value
        tmp_this.knock_in_sched.CopyFrom(p_knock_in_sched)
        tmp_this.long_short=p_long_short
        tmp_this.knock_in_payoff_type=p_knock_in_payoff_type
        tmp_this.knock_in_payoff_strike=p_knock_in_payoff_strike
        tmp_this.expiry.CopyFrom(p_expiry)
        tmp_this.delivery.CopyFrom(p_delivery)
        tmp_this.nominal=p_nominal
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.settlement_days=p_settlement_days
        tmp_this.payoff_currency=p_payoff_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSnowballAutoCallableNote
def dqCreateProtoFxSnowballAutoCallableNote(p_coupon_rate, p_start_date, p_coupon_dates, p_knock_out_barrier_type, p_knock_out_barrier_value, p_knock_out_sched, p_knock_in_barrier_type, p_knock_in_barrier_value, p_knock_in_sched, p_long_short, p_knock_in_payoff_type, p_knock_in_payoff_strike, p_expiry, p_delivery, p_nominal, p_currency_pair, p_knock_in_payoff_gearing, p_reference_price, p_day_count, p_settlement_days, p_payoff_currency):
    '''
    @args:
        1. p_coupon_rate: double
        2. p_start_date: dqproto.Date
        3. p_coupon_dates: dqproto.Date
        4. p_knock_out_barrier_type: dqproto.BarrierType
        5. p_knock_out_barrier_value: double
        6. p_knock_out_sched: dqproto.FixingSchedule
        7. p_knock_in_barrier_type: dqproto.BarrierType
        8. p_knock_in_barrier_value: double
        9. p_knock_in_sched: dqproto.FixingSchedule
        10. p_long_short: dqproto.BuySellFlag
        11. p_knock_in_payoff_type: dqproto.PayoffType
        12. p_knock_in_payoff_strike: double
        13. p_expiry: dqproto.Date
        14. p_delivery: dqproto.Date
        15. p_nominal: double
        16. p_currency_pair: dqproto.CurrencyPair
        17. p_knock_in_payoff_gearing: double
        18. p_reference_price: double
        19. p_day_count: dqproto.DayCountConvention
        20. p_settlement_days: int32
        21. p_payoff_currency: string
    @return:
        dqproto.FxSnowballAutoCallableNote
    '''
    try:
        tmp_this= FxSnowballAutoCallableNote()
        tmp_this.coupon_rate=p_coupon_rate
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.coupon_dates.extend(p_coupon_dates)
        tmp_this.knock_out_barrier_type=p_knock_out_barrier_type
        tmp_this.knock_out_barrier_value=p_knock_out_barrier_value
        tmp_this.knock_out_sched.CopyFrom(p_knock_out_sched)
        tmp_this.knock_in_barrier_type=p_knock_in_barrier_type
        tmp_this.knock_in_barrier_value=p_knock_in_barrier_value
        tmp_this.knock_in_sched.CopyFrom(p_knock_in_sched)
        tmp_this.long_short=p_long_short
        tmp_this.knock_in_payoff_type=p_knock_in_payoff_type
        tmp_this.knock_in_payoff_strike=p_knock_in_payoff_strike
        tmp_this.expiry.CopyFrom(p_expiry)
        tmp_this.delivery.CopyFrom(p_delivery)
        tmp_this.nominal=p_nominal
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.knock_in_payoff_gearing=p_knock_in_payoff_gearing
        tmp_this.reference_price=p_reference_price
        tmp_this.day_count=p_day_count
        tmp_this.settlement_days=p_settlement_days
        tmp_this.payoff_currency=p_payoff_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateFxForwardInput
def dqCreateProtoCreateFxForwardInput(p_buy_currency, p_buy_amount, p_sell_currency, p_sell_amount, p_delivery, p_fx_fwd_template, p_expiry):
    '''
    @args:
        1. p_buy_currency: string
        2. p_buy_amount: double
        3. p_sell_currency: string
        4. p_sell_amount: double
        5. p_delivery: dqproto.Date
        6. p_fx_fwd_template: dqproto.FxForwardTemplate
        7. p_expiry: dqproto.Date
    @return:
        dqproto.CreateFxForwardInput
    '''
    try:
        tmp_this= CreateFxForwardInput()
        tmp_this.buy_currency=p_buy_currency
        tmp_this.buy_amount=p_buy_amount
        tmp_this.sell_currency=p_sell_currency
        tmp_this.sell_amount=p_sell_amount
        tmp_this.delivery.CopyFrom(p_delivery)
        tmp_this.fx_fwd_template.CopyFrom(p_fx_fwd_template)
        tmp_this.expiry.CopyFrom(p_expiry)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateFxForwardOutput
def dqCreateProtoCreateFxForwardOutput(p_fx_forward, p_success, p_err_msg):
    '''
    @args:
        1. p_fx_forward: dqproto.FxForward
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateFxForwardOutput
    '''
    try:
        tmp_this= CreateFxForwardOutput()
        tmp_this.fx_forward.CopyFrom(p_fx_forward)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateFxSwapInput
def dqCreateProtoCreateFxSwapInput(p_near_buy_currency, p_near_buy_amount, p_near_sell_currency, p_near_sell_amount, p_near_delivery_date, p_near_expiry_date, p_far_buy_currency, p_far_buy_amount, p_far_sell_currency, p_far_sell_amount, p_far_delivery_date, p_far_expiry_date, p_fx_swap_template):
    '''
    @args:
        1. p_near_buy_currency: string
        2. p_near_buy_amount: double
        3. p_near_sell_currency: string
        4. p_near_sell_amount: double
        5. p_near_delivery_date: dqproto.Date
        6. p_near_expiry_date: dqproto.Date
        7. p_far_buy_currency: string
        8. p_far_buy_amount: double
        9. p_far_sell_currency: string
        10. p_far_sell_amount: double
        11. p_far_delivery_date: dqproto.Date
        12. p_far_expiry_date: dqproto.Date
        13. p_fx_swap_template: dqproto.FxSwapTemplate
    @return:
        dqproto.CreateFxSwapInput
    '''
    try:
        tmp_this= CreateFxSwapInput()
        tmp_this.near_buy_currency=p_near_buy_currency
        tmp_this.near_buy_amount=p_near_buy_amount
        tmp_this.near_sell_currency=p_near_sell_currency
        tmp_this.near_sell_amount=p_near_sell_amount
        tmp_this.near_delivery_date.CopyFrom(p_near_delivery_date)
        tmp_this.near_expiry_date.CopyFrom(p_near_expiry_date)
        tmp_this.far_buy_currency=p_far_buy_currency
        tmp_this.far_buy_amount=p_far_buy_amount
        tmp_this.far_sell_currency=p_far_sell_currency
        tmp_this.far_sell_amount=p_far_sell_amount
        tmp_this.far_delivery_date.CopyFrom(p_far_delivery_date)
        tmp_this.far_expiry_date.CopyFrom(p_far_expiry_date)
        tmp_this.fx_swap_template.CopyFrom(p_fx_swap_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateFxSwapOutput
def dqCreateProtoCreateFxSwapOutput(p_fx_swap, p_success, p_err_msg):
    '''
    @args:
        1. p_fx_swap: dqproto.FxSwap
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateFxSwapOutput
    '''
    try:
        tmp_this= CreateFxSwapOutput()
        tmp_this.fx_swap.CopyFrom(p_fx_swap)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateFxNonDeliverableForwardInput
def dqCreateProtoCreateFxNonDeliverableForwardInput(p_buy_currency, p_buy_amount, p_sell_currency, p_sell_amount, p_delivery_date, p_expiry_date, p_settlement_currency, p_fx_ndf_template):
    '''
    @args:
        1. p_buy_currency: string
        2. p_buy_amount: double
        3. p_sell_currency: string
        4. p_sell_amount: double
        5. p_delivery_date: dqproto.Date
        6. p_expiry_date: dqproto.Date
        7. p_settlement_currency: string
        8. p_fx_ndf_template: dqproto.FxNdfTemplate
    @return:
        dqproto.CreateFxNonDeliverableForwardInput
    '''
    try:
        tmp_this= CreateFxNonDeliverableForwardInput()
        tmp_this.buy_currency=p_buy_currency
        tmp_this.buy_amount=p_buy_amount
        tmp_this.sell_currency=p_sell_currency
        tmp_this.sell_amount=p_sell_amount
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.settlement_currency=p_settlement_currency
        tmp_this.fx_ndf_template.CopyFrom(p_fx_ndf_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateFxNonDeliverableForwardOutput
def dqCreateProtoCreateFxNonDeliverableForwardOutput(p_fx_ndf, p_success, p_err_msg):
    '''
    @args:
        1. p_fx_ndf: dqproto.FxNonDeliverableForward
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateFxNonDeliverableForwardOutput
    '''
    try:
        tmp_this= CreateFxNonDeliverableForwardOutput()
        tmp_this.fx_ndf.CopyFrom(p_fx_ndf)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateFxTimeOptionInput
def dqCreateProtoCreateFxTimeOptionInput(p_buy_currency, p_buy_amount, p_sell_currency, p_sell_amount, p_delivery_date, p_exercise_start_date, p_exercise_end_date, p_fx_time_option_template):
    '''
    @args:
        1. p_buy_currency: string
        2. p_buy_amount: double
        3. p_sell_currency: string
        4. p_sell_amount: double
        5. p_delivery_date: dqproto.Date
        6. p_exercise_start_date: dqproto.Date
        7. p_exercise_end_date: dqproto.Date
        8. p_fx_time_option_template: dqproto.FxTimeOptionTemplate
    @return:
        dqproto.CreateFxTimeOptionInput
    '''
    try:
        tmp_this= CreateFxTimeOptionInput()
        tmp_this.buy_currency=p_buy_currency
        tmp_this.buy_amount=p_buy_amount
        tmp_this.sell_currency=p_sell_currency
        tmp_this.sell_amount=p_sell_amount
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.exercise_start_date.CopyFrom(p_exercise_start_date)
        tmp_this.exercise_end_date.CopyFrom(p_exercise_end_date)
        tmp_this.fx_time_option_template.CopyFrom(p_fx_time_option_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateFxTimeOptionOutput
def dqCreateProtoCreateFxTimeOptionOutput(p_fx_time_option, p_success, p_err_msg):
    '''
    @args:
        1. p_fx_time_option: dqproto.FxTimeOption
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateFxTimeOptionOutput
    '''
    try:
        tmp_this= CreateFxTimeOptionOutput()
        tmp_this.fx_time_option.CopyFrom(p_fx_time_option)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSpotDateCalculationInput
def dqCreateProtoFxSpotDateCalculationInput(p_calculation_date, p_currency_pair, p_fx_spot_template):
    '''
    @args:
        1. p_calculation_date: dqproto.Date
        2. p_currency_pair: dqproto.CurrencyPair
        3. p_fx_spot_template: dqproto.FxSpotTemplate
    @return:
        dqproto.FxSpotDateCalculationInput
    '''
    try:
        tmp_this= FxSpotDateCalculationInput()
        tmp_this.calculation_date.CopyFrom(p_calculation_date)
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.fx_spot_template.CopyFrom(p_fx_spot_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSpotDateCalculationOutput
def dqCreateProtoFxSpotDateCalculationOutput(p_spot_date, p_success, p_err_msg):
    '''
    @args:
        1. p_spot_date: dqproto.Date
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FxSpotDateCalculationOutput
    '''
    try:
        tmp_this= FxSpotDateCalculationOutput()
        tmp_this.spot_date.CopyFrom(p_spot_date)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxForwardDateCalculationInput
def dqCreateProtoFxForwardDateCalculationInput(p_calculation_date, p_currency_pair, p_term, p_spot_date, p_fx_fwd_template):
    '''
    @args:
        1. p_calculation_date: dqproto.Date
        2. p_currency_pair: dqproto.CurrencyPair
        3. p_term: dqproto.Period
        4. p_spot_date: dqproto.Date
        5. p_fx_fwd_template: dqproto.FxSpotTemplate
    @return:
        dqproto.FxForwardDateCalculationInput
    '''
    try:
        tmp_this= FxForwardDateCalculationInput()
        tmp_this.calculation_date.CopyFrom(p_calculation_date)
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.term.CopyFrom(p_term)
        tmp_this.spot_date.CopyFrom(p_spot_date)
        tmp_this.fx_fwd_template.CopyFrom(p_fx_fwd_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxForwardDateCalculationOutput
def dqCreateProtoFxForwardDateCalculationOutput(p_expiry_date, p_delivery_date, p_success, p_err_msg):
    '''
    @args:
        1. p_expiry_date: dqproto.Date
        2. p_delivery_date: dqproto.Date
        3. p_success: bool
        4. p_err_msg: string
    @return:
        dqproto.FxForwardDateCalculationOutput
    '''
    try:
        tmp_this= FxForwardDateCalculationOutput()
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxOptionDateCalculationInput
def dqCreateProtoFxOptionDateCalculationInput(p_calculation_date, p_currency_pair, p_term, p_business_day_convention, p_fx_spot_template):
    '''
    @args:
        1. p_calculation_date: dqproto.Date
        2. p_currency_pair: dqproto.CurrencyPair
        3. p_term: dqproto.Period
        4. p_business_day_convention: dqproto.BusinessDayConvention
        5. p_fx_spot_template: dqproto.FxSpotTemplate
    @return:
        dqproto.FxOptionDateCalculationInput
    '''
    try:
        tmp_this= FxOptionDateCalculationInput()
        tmp_this.calculation_date.CopyFrom(p_calculation_date)
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        tmp_this.term.CopyFrom(p_term)
        tmp_this.business_day_convention=p_business_day_convention
        tmp_this.fx_spot_template.CopyFrom(p_fx_spot_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxOptionDateCalculationOutput
def dqCreateProtoFxOptionDateCalculationOutput(p_expiry_date, p_delivery_date, p_success, p_err_msg):
    '''
    @args:
        1. p_expiry_date: dqproto.Date
        2. p_delivery_date: dqproto.Date
        3. p_success: bool
        4. p_err_msg: string
    @return:
        dqproto.FxOptionDateCalculationOutput
    '''
    try:
        tmp_this= FxOptionDateCalculationOutput()
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxFixingDateCalculationInput
def dqCreateProtoFxFixingDateCalculationInput(p_delivery_date, p_spot_template):
    '''
    @args:
        1. p_delivery_date: dqproto.Date
        2. p_spot_template: dqproto.FxSpotTemplate
    @return:
        dqproto.FxFixingDateCalculationInput
    '''
    try:
        tmp_this= FxFixingDateCalculationInput()
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.spot_template.CopyFrom(p_spot_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxFixingDateCalculationOutput
def dqCreateProtoFxFixingDateCalculationOutput(p_fixing_date, p_success, p_err_msg):
    '''
    @args:
        1. p_fixing_date: dqproto.Date
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.FxFixingDateCalculationOutput
    '''
    try:
        tmp_this= FxFixingDateCalculationOutput()
        tmp_this.fixing_date.CopyFrom(p_fixing_date)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrMktDataSet
def dqCreateProtoIrMktDataSet(p_as_of_date, p_discount_curve, p_underlying_interest_rate, p_forward_curve):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_discount_curve: dqproto.IrYieldCurve
        3. p_underlying_interest_rate: string
        4. p_forward_curve: dqproto.IrYieldCurve
    @return:
        dqproto.IrMktDataSet
    '''
    try:
        tmp_this= IrMktDataSet()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.underlying_interest_rate.extend(p_underlying_interest_rate)
        tmp_this.forward_curve.extend(p_forward_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCrossCcyMktDataSet
def dqCreateProtoIrCrossCcyMktDataSet(p_as_of_date, p_base_discount_curve, p_underlying_interest_rate, p_forward_curve, p_cross_ccy_discount_curve, p_fx_spot):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_base_discount_curve: dqproto.IrYieldCurve
        3. p_underlying_interest_rate: string
        4. p_forward_curve: dqproto.IrYieldCurve
        5. p_cross_ccy_discount_curve: dqproto.IrYieldCurve
        6. p_fx_spot: dqproto.FxSpotRate
    @return:
        dqproto.IrCrossCcyMktDataSet
    '''
    try:
        tmp_this= IrCrossCcyMktDataSet()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.base_discount_curve.CopyFrom(p_base_discount_curve)
        tmp_this.underlying_interest_rate.extend(p_underlying_interest_rate)
        tmp_this.forward_curve.extend(p_forward_curve)
        tmp_this.cross_ccy_discount_curve.CopyFrom(p_cross_ccy_discount_curve)
        tmp_this.fx_spot.CopyFrom(p_fx_spot)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrRiskSettings
def dqCreateProtoIrRiskSettings(p_ir_curve_settings, p_theta_settings):
    '''
    @args:
        1. p_ir_curve_settings: dqproto.IrCurveRiskSettings
        2. p_theta_settings: dqproto.ThetaRiskSettings
    @return:
        dqproto.IrRiskSettings
    '''
    try:
        tmp_this= IrRiskSettings()
        tmp_this.ir_curve_settings.CopyFrom(p_ir_curve_settings)
        tmp_this.theta_settings.CopyFrom(p_theta_settings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#XccyIrRiskSettings
def dqCreateProtoXccyIrRiskSettings(p_ir_curve_settings, p_theta_settings, p_fx_settings):
    '''
    @args:
        1. p_ir_curve_settings: dqproto.IrCurveRiskSettings
        2. p_theta_settings: dqproto.ThetaRiskSettings
        3. p_fx_settings: dqproto.PriceRiskSettings
    @return:
        dqproto.XccyIrRiskSettings
    '''
    try:
        tmp_this= XccyIrRiskSettings()
        tmp_this.ir_curve_settings.CopyFrom(p_ir_curve_settings)
        tmp_this.theta_settings.CopyFrom(p_theta_settings)
        tmp_this.fx_settings.CopyFrom(p_fx_settings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrParRateCurve.Pillar
def dqCreateProtoIrParRateCurve_Pillar(p_instrument_name, p_instrument_type, p_instrument_term, p_instrument_rate, p_start_convention):
    '''
    @args:
        1. p_instrument_name: string
        2. p_instrument_type: dqproto.InstrumentType
        3. p_instrument_term: dqproto.Period
        4. p_instrument_rate: double
        5. p_start_convention: dqproto.InstrumentStartConvention
    @return:
        dqproto.IrParRateCurve.Pillar
    '''
    try:
        tmp_this= IrParRateCurve.Pillar()
        tmp_this.instrument_name=p_instrument_name
        tmp_this.instrument_type=p_instrument_type
        tmp_this.instrument_term.CopyFrom(p_instrument_term)
        tmp_this.instrument_rate=p_instrument_rate
        tmp_this.start_convention=p_start_convention
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrParRateCurve
def dqCreateProtoIrParRateCurve(p_reference_date, p_currency, p_name, p_pillars):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_currency: string
        3. p_name: string
        4. p_pillars: dqproto.IrParRateCurve.Pillar
    @return:
        dqproto.IrParRateCurve
    '''
    try:
        tmp_this= IrParRateCurve()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.currency=p_currency
        tmp_this.name=p_name
        tmp_this.pillars.extend(p_pillars)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrYieldCurveBuildSettings.DiscountCurveManager.Curve
def dqCreateProtoIrYieldCurveBuildSettings_DiscountCurveManager_Curve(p_currency_name, p_curve_name):
    '''
    @args:
        1. p_currency_name: string
        2. p_curve_name: string
    @return:
        dqproto.IrYieldCurveBuildSettings.DiscountCurveManager.Curve
    '''
    try:
        tmp_this= IrYieldCurveBuildSettings.DiscountCurveManager.Curve()
        tmp_this.currency_name=p_currency_name
        tmp_this.curve_name=p_curve_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrYieldCurveBuildSettings.DiscountCurveManager
def dqCreateProtoIrYieldCurveBuildSettings_DiscountCurveManager(p_curves):
    '''
    @args:
        1. p_curves: dqproto.IrYieldCurveBuildSettings.DiscountCurveManager.Curve
    @return:
        dqproto.IrYieldCurveBuildSettings.DiscountCurveManager
    '''
    try:
        tmp_this= IrYieldCurveBuildSettings.DiscountCurveManager()
        tmp_this.curves.extend(p_curves)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrYieldCurveBuildSettings.ForwardCurveManager.Curve
def dqCreateProtoIrYieldCurveBuildSettings_ForwardCurveManager_Curve(p_index_name, p_curve_name):
    '''
    @args:
        1. p_index_name: string
        2. p_curve_name: string
    @return:
        dqproto.IrYieldCurveBuildSettings.ForwardCurveManager.Curve
    '''
    try:
        tmp_this= IrYieldCurveBuildSettings.ForwardCurveManager.Curve()
        tmp_this.index_name=p_index_name
        tmp_this.curve_name=p_curve_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrYieldCurveBuildSettings.ForwardCurveManager
def dqCreateProtoIrYieldCurveBuildSettings_ForwardCurveManager(p_curves):
    '''
    @args:
        1. p_curves: dqproto.IrYieldCurveBuildSettings.ForwardCurveManager.Curve
    @return:
        dqproto.IrYieldCurveBuildSettings.ForwardCurveManager
    '''
    try:
        tmp_this= IrYieldCurveBuildSettings.ForwardCurveManager()
        tmp_this.curves.extend(p_curves)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrYieldCurveBuildSettings
def dqCreateProtoIrYieldCurveBuildSettings(p_curve_name, p_use_on_tn_fx_swap, p_discount_curve_manager, p_forward_curve_manager):
    '''
    @args:
        1. p_curve_name: string
        2. p_use_on_tn_fx_swap: bool
        3. p_discount_curve_manager: dqproto.IrYieldCurveBuildSettings.DiscountCurveManager
        4. p_forward_curve_manager: dqproto.IrYieldCurveBuildSettings.ForwardCurveManager
    @return:
        dqproto.IrYieldCurveBuildSettings
    '''
    try:
        tmp_this= IrYieldCurveBuildSettings()
        tmp_this.curve_name=p_curve_name
        tmp_this.use_on_tn_fx_swap=p_use_on_tn_fx_swap
        tmp_this.discount_curve_manager.CopyFrom(p_discount_curve_manager)
        tmp_this.forward_curve_manager.CopyFrom(p_forward_curve_manager)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCapFloorVolatilitySurface
def dqCreateProtoIrCapFloorVolatilitySurface(p_volatility_surface, p_ibor_index, p_currency):
    '''
    @args:
        1. p_volatility_surface: dqproto.VolatilitySurface
        2. p_ibor_index: string
        3. p_currency: string
    @return:
        dqproto.IrCapFloorVolatilitySurface
    '''
    try:
        tmp_this= IrCapFloorVolatilitySurface()
        tmp_this.volatility_surface.CopyFrom(p_volatility_surface)
        tmp_this.ibor_index=p_ibor_index
        tmp_this.currency=p_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrSwaptionAtmQuoteMatrix
def dqCreateProtoIrSwaptionAtmQuoteMatrix(p_as_of_date, p_terms, p_tenors, p_vols):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_terms: dqproto.Period
        3. p_tenors: dqproto.Period
        4. p_vols: dqproto.Matrix
    @return:
        dqproto.IrSwaptionAtmQuoteMatrix
    '''
    try:
        tmp_this= IrSwaptionAtmQuoteMatrix()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.terms.extend(p_terms)
        tmp_this.tenors.extend(p_tenors)
        tmp_this.vols.CopyFrom(p_vols)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrSwaptionQuoteCube
def dqCreateProtoIrSwaptionQuoteCube(p_atm_vol_matrix, p_otm_vol_matrices):
    '''
    @args:
        1. p_atm_vol_matrix: dqproto.IrSwaptionAtmQuoteMatrix
        2. p_otm_vol_matrices: dqproto.IrSwaptionQuoteCube.IrSwaptionOtmQuoteMatrix
    @return:
        dqproto.IrSwaptionQuoteCube
    '''
    try:
        tmp_this= IrSwaptionQuoteCube()
        tmp_this.atm_vol_matrix.CopyFrom(p_atm_vol_matrix)
        tmp_this.otm_vol_matrices.extend(p_otm_vol_matrices)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrSwaptionQuoteCube.IrSwaptionOtmQuoteMatrix
def dqCreateProtoIrSwaptionQuoteCube_IrSwaptionOtmQuoteMatrix(p_tenor, p_otm_vol_matrix):
    '''
    @args:
        1. p_tenor: dqproto.Period
        2. p_otm_vol_matrix: dqproto.OptionQuoteMatrix
    @return:
        dqproto.IrSwaptionQuoteCube.IrSwaptionOtmQuoteMatrix
    '''
    try:
        tmp_this= IrSwaptionQuoteCube.IrSwaptionOtmQuoteMatrix()
        tmp_this.tenor.CopyFrom(p_tenor)
        tmp_this.otm_vol_matrix.CopyFrom(p_otm_vol_matrix)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrSwaptionVolatilitySurface
def dqCreateProtoIrSwaptionVolatilitySurface(p_reference_date, p_name, p_currency, p_ibor_index, p_definition, p_atm_vol_interpolator, p_param_interpolators, p_tenors):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_name: string
        3. p_currency: string
        4. p_ibor_index: string
        5. p_definition: dqproto.VolatilitySurfaceDefinition
        6. p_atm_vol_interpolator: dqproto.BiLinearInterpolator
        7. p_param_interpolators: dqproto.BiLinearInterpolator
        8. p_tenors: dqproto.Vector
    @return:
        dqproto.IrSwaptionVolatilitySurface
    '''
    try:
        tmp_this= IrSwaptionVolatilitySurface()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.name=p_name
        tmp_this.currency=p_currency
        tmp_this.ibor_index=p_ibor_index
        tmp_this.definition.CopyFrom(p_definition)
        tmp_this.atm_vol_interpolator.CopyFrom(p_atm_vol_interpolator)
        tmp_this.param_interpolators.extend(p_param_interpolators)
        tmp_this.tenors.CopyFrom(p_tenors)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrParRateCurveInput
def dqCreateProtoCreateIrParRateCurveInput(p_as_of_date, p_currency, p_curve_name, p_inst_names, p_inst_types, p_inst_terms, p_factors, p_quotes):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_currency: string
        3. p_curve_name: string
        4. p_inst_names: string
        5. p_inst_types: string
        6. p_inst_terms: string
        7. p_factors: double
        8. p_quotes: double
    @return:
        dqproto.CreateIrParRateCurveInput
    '''
    try:
        tmp_this= CreateIrParRateCurveInput()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.currency=p_currency
        tmp_this.curve_name=p_curve_name
        tmp_this.inst_names.extend(p_inst_names)
        tmp_this.inst_types.extend(p_inst_types)
        tmp_this.inst_terms.extend(p_inst_terms)
        tmp_this.factors.extend(p_factors)
        tmp_this.quotes.extend(p_quotes)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrParRateCurveOutput
def dqCreateProtoCreateIrParRateCurveOutput(p_ir_par_rate_curve, p_success, p_err_msg):
    '''
    @args:
        1. p_ir_par_rate_curve: dqproto.IrParRateCurve
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateIrParRateCurveOutput
    '''
    try:
        tmp_this= CreateIrParRateCurveOutput()
        tmp_this.ir_par_rate_curve.CopyFrom(p_ir_par_rate_curve)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrYieldCurveBuildSettingsInput.DiscountCurveSettings
def dqCreateProtoCreateIrYieldCurveBuildSettingsInput_DiscountCurveSettings(p_currency_name, p_curve_name):
    '''
    @args:
        1. p_currency_name: string
        2. p_curve_name: string
    @return:
        dqproto.CreateIrYieldCurveBuildSettingsInput.DiscountCurveSettings
    '''
    try:
        tmp_this= CreateIrYieldCurveBuildSettingsInput.DiscountCurveSettings()
        tmp_this.currency_name=p_currency_name
        tmp_this.curve_name=p_curve_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrYieldCurveBuildSettingsInput.ForwardCurveSettings
def dqCreateProtoCreateIrYieldCurveBuildSettingsInput_ForwardCurveSettings(p_index_name, p_curve_name):
    '''
    @args:
        1. p_index_name: string
        2. p_curve_name: string
    @return:
        dqproto.CreateIrYieldCurveBuildSettingsInput.ForwardCurveSettings
    '''
    try:
        tmp_this= CreateIrYieldCurveBuildSettingsInput.ForwardCurveSettings()
        tmp_this.index_name=p_index_name
        tmp_this.curve_name=p_curve_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrYieldCurveBuildSettingsInput
def dqCreateProtoCreateIrYieldCurveBuildSettingsInput(p_curve_name, p_use_on_tn_fx_swap, p_discount_curve_settings, p_forward_curve_settings):
    '''
    @args:
        1. p_curve_name: string
        2. p_use_on_tn_fx_swap: bool
        3. p_discount_curve_settings: dqproto.CreateIrYieldCurveBuildSettingsInput.DiscountCurveSettings
        4. p_forward_curve_settings: dqproto.CreateIrYieldCurveBuildSettingsInput.ForwardCurveSettings
    @return:
        dqproto.CreateIrYieldCurveBuildSettingsInput
    '''
    try:
        tmp_this= CreateIrYieldCurveBuildSettingsInput()
        tmp_this.curve_name=p_curve_name
        tmp_this.use_on_tn_fx_swap=p_use_on_tn_fx_swap
        tmp_this.discount_curve_settings.extend(p_discount_curve_settings)
        tmp_this.forward_curve_settings.extend(p_forward_curve_settings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrYieldCurveBuildSettingsOutput
def dqCreateProtoCreateIrYieldCurveBuildSettingsOutput(p_ir_yield_curve_build_settings, p_success, p_err_msg):
    '''
    @args:
        1. p_ir_yield_curve_build_settings: dqproto.IrYieldCurveBuildSettings
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateIrYieldCurveBuildSettingsOutput
    '''
    try:
        tmp_this= CreateIrYieldCurveBuildSettingsOutput()
        tmp_this.ir_yield_curve_build_settings.CopyFrom(p_ir_yield_curve_build_settings)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrSingleCurrencyCurveBuildingInput.IrYieldCurveBuildSettingsContainer
def dqCreateProtoIrSingleCurrencyCurveBuildingInput_IrYieldCurveBuildSettingsContainer(p_target_curve_name, p_ir_yield_curve_build_settings, p_par_curve, p_day_count_convention, p_compounding_type, p_frequency):
    '''
    @args:
        1. p_target_curve_name: string
        2. p_ir_yield_curve_build_settings: dqproto.IrYieldCurveBuildSettings
        3. p_par_curve: dqproto.IrParRateCurve
        4. p_day_count_convention: dqproto.DayCountConvention
        5. p_compounding_type: dqproto.CompoundingType
        6. p_frequency: dqproto.Frequency
    @return:
        dqproto.IrSingleCurrencyCurveBuildingInput.IrYieldCurveBuildSettingsContainer
    '''
    try:
        tmp_this= IrSingleCurrencyCurveBuildingInput.IrYieldCurveBuildSettingsContainer()
        tmp_this.target_curve_name=p_target_curve_name
        tmp_this.ir_yield_curve_build_settings.CopyFrom(p_ir_yield_curve_build_settings)
        tmp_this.par_curve.CopyFrom(p_par_curve)
        tmp_this.day_count_convention=p_day_count_convention
        tmp_this.compounding_type=p_compounding_type
        tmp_this.frequency=p_frequency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrSingleCurrencyCurveBuildingInput
def dqCreateProtoIrSingleCurrencyCurveBuildingInput(p_reference_date, p_build_settings, p_other_curves, p_building_method, p_calc_jacobian, p_shift, p_finite_difference_method, p_threading_mode):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_build_settings: dqproto.IrSingleCurrencyCurveBuildingInput.IrYieldCurveBuildSettingsContainer
        3. p_other_curves: dqproto.IrYieldCurve
        4. p_building_method: dqproto.IrYieldCurveBuildingMethod
        5. p_calc_jacobian: int32
        6. p_shift: double
        7. p_finite_difference_method: dqproto.FiniteDifferenceMethod
        8. p_threading_mode: dqproto.ThreadingMode
    @return:
        dqproto.IrSingleCurrencyCurveBuildingInput
    '''
    try:
        tmp_this= IrSingleCurrencyCurveBuildingInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.build_settings.extend(p_build_settings)
        tmp_this.other_curves.extend(p_other_curves)
        tmp_this.building_method=p_building_method
        tmp_this.calc_jacobian=p_calc_jacobian
        tmp_this.shift=p_shift
        tmp_this.finite_difference_method=p_finite_difference_method
        tmp_this.threading_mode=p_threading_mode
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrSingleCurrencyCurveBuildingOutput
def dqCreateProtoIrSingleCurrencyCurveBuildingOutput(p_target_curves, p_success, p_err_msg):
    '''
    @args:
        1. p_target_curves: dqproto.IrYieldCurve
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.IrSingleCurrencyCurveBuildingOutput
    '''
    try:
        tmp_this= IrSingleCurrencyCurveBuildingOutput()
        tmp_this.target_curves.extend(p_target_curves)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrVanillaInstrumentPricingInput
def dqCreateProtoIrVanillaInstrumentPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.IrVanillaInstrument
        3. p_mkt_data: dqproto.IrMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.IrRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.IrVanillaInstrumentPricingInput
    '''
    try:
        tmp_this= IrVanillaInstrumentPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrVanillaInstrumentPricingOutput
def dqCreateProtoIrVanillaInstrumentPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.IrVanillaInstrumentPricingOutput
    '''
    try:
        tmp_this= IrVanillaInstrumentPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCrossCurrencyCurveBuildingInput.IrYieldCurveBuildSettingsContainer
def dqCreateProtoIrCrossCurrencyCurveBuildingInput_IrYieldCurveBuildSettingsContainer(p_target_curve_name, p_ir_yield_curve_build_settings, p_par_curve, p_day_count_convention, p_compounding_type, p_frequency):
    '''
    @args:
        1. p_target_curve_name: string
        2. p_ir_yield_curve_build_settings: dqproto.IrYieldCurveBuildSettings
        3. p_par_curve: dqproto.IrParRateCurve
        4. p_day_count_convention: dqproto.DayCountConvention
        5. p_compounding_type: dqproto.CompoundingType
        6. p_frequency: dqproto.Frequency
    @return:
        dqproto.IrCrossCurrencyCurveBuildingInput.IrYieldCurveBuildSettingsContainer
    '''
    try:
        tmp_this= IrCrossCurrencyCurveBuildingInput.IrYieldCurveBuildSettingsContainer()
        tmp_this.target_curve_name=p_target_curve_name
        tmp_this.ir_yield_curve_build_settings.CopyFrom(p_ir_yield_curve_build_settings)
        tmp_this.par_curve.CopyFrom(p_par_curve)
        tmp_this.day_count_convention=p_day_count_convention
        tmp_this.compounding_type=p_compounding_type
        tmp_this.frequency=p_frequency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCrossCurrencyCurveBuildingInput
def dqCreateProtoIrCrossCurrencyCurveBuildingInput(p_reference_date, p_build_settings, p_other_curves, p_fx_spot, p_building_method, p_calc_jacobian, p_shift, p_finite_difference_method, p_threading_mode):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_build_settings: dqproto.IrCrossCurrencyCurveBuildingInput.IrYieldCurveBuildSettingsContainer
        3. p_other_curves: dqproto.IrYieldCurve
        4. p_fx_spot: dqproto.FxSpotRate
        5. p_building_method: dqproto.IrYieldCurveBuildingMethod
        6. p_calc_jacobian: int32
        7. p_shift: double
        8. p_finite_difference_method: dqproto.FiniteDifferenceMethod
        9. p_threading_mode: dqproto.ThreadingMode
    @return:
        dqproto.IrCrossCurrencyCurveBuildingInput
    '''
    try:
        tmp_this= IrCrossCurrencyCurveBuildingInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.build_settings.extend(p_build_settings)
        tmp_this.other_curves.extend(p_other_curves)
        tmp_this.fx_spot.CopyFrom(p_fx_spot)
        tmp_this.building_method=p_building_method
        tmp_this.calc_jacobian=p_calc_jacobian
        tmp_this.shift=p_shift
        tmp_this.finite_difference_method=p_finite_difference_method
        tmp_this.threading_mode=p_threading_mode
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCrossCurrencyCurveBuildingOutput
def dqCreateProtoIrCrossCurrencyCurveBuildingOutput(p_target_curves, p_success, p_err_msg):
    '''
    @args:
        1. p_target_curves: dqproto.IrYieldCurve
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.IrCrossCurrencyCurveBuildingOutput
    '''
    try:
        tmp_this= IrCrossCurrencyCurveBuildingOutput()
        tmp_this.target_curves.extend(p_target_curves)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CrossCurrencySwapPricingInput
def dqCreateProtoCrossCurrencySwapPricingInput(p_pricing_date, p_instrument, p_pricing_settings, p_mkt_data, p_risk_settings, p_use_binary, p_instrument_bin, p_pricing_settings_bin, p_mkt_data_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.IrVanillaInstrument
        3. p_pricing_settings: dqproto.PricingSettings
        4. p_mkt_data: dqproto.IrCrossCcyMktDataSet
        5. p_risk_settings: dqproto.XccyIrRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_pricing_settings_bin: bytes
        9. p_mkt_data_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.CrossCurrencySwapPricingInput
    '''
    try:
        tmp_this= CrossCurrencySwapPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CrossCurrencySwapPricingOutput
def dqCreateProtoCrossCurrencySwapPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CrossCurrencySwapPricingOutput
    '''
    try:
        tmp_this= CrossCurrencySwapPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrCapFloorQuoteMatrixInput
def dqCreateProtoCreateIrCapFloorQuoteMatrixInput(p_as_of_date, p_terms, p_strikes, p_vols, p_inst_name, p_factor):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_terms: dqproto.Period
        3. p_strikes: dqproto.Vector
        4. p_vols: dqproto.Matrix
        5. p_inst_name: string
        6. p_factor: double
    @return:
        dqproto.CreateIrCapFloorQuoteMatrixInput
    '''
    try:
        tmp_this= CreateIrCapFloorQuoteMatrixInput()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.terms.extend(p_terms)
        tmp_this.strikes.CopyFrom(p_strikes)
        tmp_this.vols.CopyFrom(p_vols)
        tmp_this.inst_name=p_inst_name
        tmp_this.factor=p_factor
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrCapFloorQuoteMatrixOutput
def dqCreateProtoCreateIrCapFloorQuoteMatrixOutput(p_quote_matrix, p_success, p_err_msg):
    '''
    @args:
        1. p_quote_matrix: dqproto.OptionQuoteMatrix
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateIrCapFloorQuoteMatrixOutput
    '''
    try:
        tmp_this= CreateIrCapFloorQuoteMatrixOutput()
        tmp_this.quote_matrix.CopyFrom(p_quote_matrix)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrCapFloorVolatilitySurfaceInput
def dqCreateProtoCreateIrCapFloorVolatilitySurfaceInput(p_reference_date, p_term_dates, p_strikes, p_volatilities, p_definition, p_name, p_ibor_index):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_term_dates: dqproto.Date
        3. p_strikes: dqproto.Vector
        4. p_volatilities: dqproto.Vector
        5. p_definition: dqproto.VolatilitySurfaceDefinition
        6. p_name: string
        7. p_ibor_index: string
    @return:
        dqproto.CreateIrCapFloorVolatilitySurfaceInput
    '''
    try:
        tmp_this= CreateIrCapFloorVolatilitySurfaceInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.term_dates.extend(p_term_dates)
        tmp_this.strikes.extend(p_strikes)
        tmp_this.volatilities.extend(p_volatilities)
        tmp_this.definition.CopyFrom(p_definition)
        tmp_this.name=p_name
        tmp_this.ibor_index=p_ibor_index
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrCapFloorVolatilitySurfaceOutput
def dqCreateProtoCreateIrCapFloorVolatilitySurfaceOutput(p_ir_cap_floor_vol_surf, p_success, p_err_msg):
    '''
    @args:
        1. p_ir_cap_floor_vol_surf: dqproto.IrCapFloorVolatilitySurface
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateIrCapFloorVolatilitySurfaceOutput
    '''
    try:
        tmp_this= CreateIrCapFloorVolatilitySurfaceOutput()
        tmp_this.ir_cap_floor_vol_surf.CopyFrom(p_ir_cap_floor_vol_surf)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrSwaptionQuoteCubeInput.Pillar
def dqCreateProtoCreateIrSwaptionQuoteCubeInput_Pillar(p_terms):
    '''
    @args:
        1. p_terms: dqproto.Period
    @return:
        dqproto.CreateIrSwaptionQuoteCubeInput.Pillar
    '''
    try:
        tmp_this= CreateIrSwaptionQuoteCubeInput.Pillar()
        tmp_this.terms.extend(p_terms)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrSwaptionQuoteCubeInput
def dqCreateProtoCreateIrSwaptionQuoteCubeInput(p_as_of_date, p_atm_terms, p_atm_tenors, p_atm_vols, p_otm_tenors, p_otm_strikes, p_otm_terms, p_otm_vols):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_atm_terms: dqproto.Period
        3. p_atm_tenors: dqproto.Period
        4. p_atm_vols: dqproto.Matrix
        5. p_otm_tenors: dqproto.Period
        6. p_otm_strikes: dqproto.Vector
        7. p_otm_terms: dqproto.CreateIrSwaptionQuoteCubeInput.Pillar
        8. p_otm_vols: dqproto.Matrix
    @return:
        dqproto.CreateIrSwaptionQuoteCubeInput
    '''
    try:
        tmp_this= CreateIrSwaptionQuoteCubeInput()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.atm_terms.extend(p_atm_terms)
        tmp_this.atm_tenors.extend(p_atm_tenors)
        tmp_this.atm_vols.CopyFrom(p_atm_vols)
        tmp_this.otm_tenors.extend(p_otm_tenors)
        tmp_this.otm_strikes.CopyFrom(p_otm_strikes)
        tmp_this.otm_terms.extend(p_otm_terms)
        tmp_this.otm_vols.extend(p_otm_vols)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrSwaptionQuoteCubeOutput
def dqCreateProtoCreateIrSwaptionQuoteCubeOutput(p_quote_cube, p_success, p_err_msg):
    '''
    @args:
        1. p_quote_cube: dqproto.IrSwaptionQuoteCube
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateIrSwaptionQuoteCubeOutput
    '''
    try:
        tmp_this= CreateIrSwaptionQuoteCubeOutput()
        tmp_this.quote_cube.CopyFrom(p_quote_cube)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrSwaptionVolatilitySurfaceInput
def dqCreateProtoCreateIrSwaptionVolatilitySurfaceInput(p_reference_date, p_vol_type, p_terms, p_tenors, p_strikes, p_volatilities, p_name):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_vol_type: dqproto.VolatilityType
        3. p_terms: dqproto.Vector
        4. p_tenors: dqproto.Vector
        5. p_strikes: dqproto.Vector
        6. p_volatilities: dqproto.Matrix
        7. p_name: string
    @return:
        dqproto.CreateIrSwaptionVolatilitySurfaceInput
    '''
    try:
        tmp_this= CreateIrSwaptionVolatilitySurfaceInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.vol_type=p_vol_type
        tmp_this.terms.extend(p_terms)
        tmp_this.tenors.CopyFrom(p_tenors)
        tmp_this.strikes.CopyFrom(p_strikes)
        tmp_this.volatilities.extend(p_volatilities)
        tmp_this.name=p_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateIrSwaptionVolatilitySurfaceOutput
def dqCreateProtoCreateIrSwaptionVolatilitySurfaceOutput(p_ir_swaption_vol_surf, p_success, p_err_msg):
    '''
    @args:
        1. p_ir_swaption_vol_surf: dqproto.IrSwaptionVolatilitySurface
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateIrSwaptionVolatilitySurfaceOutput
    '''
    try:
        tmp_this= CreateIrSwaptionVolatilitySurfaceOutput()
        tmp_this.ir_swaption_vol_surf.CopyFrom(p_ir_swaption_vol_surf)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCapFloorPricingInput
def dqCreateProtoIrCapFloorPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.IrCapFloor
        3. p_mkt_data: dqproto.IrMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.IrRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.IrCapFloorPricingInput
    '''
    try:
        tmp_this= IrCapFloorPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCapFloorPricingOutput
def dqCreateProtoIrCapFloorPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.IrCapFloorPricingOutput
    '''
    try:
        tmp_this= IrCapFloorPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCapFloorVolatilitySurfaceBuildingInput
def dqCreateProtoIrCapFloorVolatilitySurfaceBuildingInput(p_ibor_index, p_reference_date, p_quotes_matrix, p_discount_curve, p_forward_curve, p_displacement, p_definition, p_name):
    '''
    @args:
        1. p_ibor_index: string
        2. p_reference_date: dqproto.Date
        3. p_quotes_matrix: dqproto.OptionQuoteMatrix
        4. p_discount_curve: dqproto.IrYieldCurve
        5. p_forward_curve: dqproto.IrYieldCurve
        6. p_displacement: double
        7. p_definition: dqproto.VolatilitySurfaceDefinition
        8. p_name: string
    @return:
        dqproto.IrCapFloorVolatilitySurfaceBuildingInput
    '''
    try:
        tmp_this= IrCapFloorVolatilitySurfaceBuildingInput()
        tmp_this.ibor_index=p_ibor_index
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.quotes_matrix.CopyFrom(p_quotes_matrix)
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.forward_curve.CopyFrom(p_forward_curve)
        tmp_this.displacement=p_displacement
        tmp_this.definition.CopyFrom(p_definition)
        tmp_this.name=p_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCapFloorVolatilitySurfaceBuildingOutput
def dqCreateProtoIrCapFloorVolatilitySurfaceBuildingOutput(p_vol_surf, p_success, p_err_msg):
    '''
    @args:
        1. p_vol_surf: dqproto.IrCapFloorVolatilitySurface
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.IrCapFloorVolatilitySurfaceBuildingOutput
    '''
    try:
        tmp_this= IrCapFloorVolatilitySurfaceBuildingOutput()
        tmp_this.vol_surf.CopyFrom(p_vol_surf)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrEuropeanSwaptionPricingInput
def dqCreateProtoIrEuropeanSwaptionPricingInput(p_pricing_date, p_instrument, p_mkt_data, p_pricing_settings, p_risk_settings, p_use_binary, p_instrument_bin, p_mkt_data_bin, p_pricing_settings_bin, p_risk_settings_bin):
    '''
    @args:
        1. p_pricing_date: dqproto.Date
        2. p_instrument: dqproto.IrEuropeanSwaption
        3. p_mkt_data: dqproto.IrMktDataSet
        4. p_pricing_settings: dqproto.PricingSettings
        5. p_risk_settings: dqproto.IrRiskSettings
        6. p_use_binary: bool
        7. p_instrument_bin: bytes
        8. p_mkt_data_bin: bytes
        9. p_pricing_settings_bin: bytes
        10. p_risk_settings_bin: bytes
    @return:
        dqproto.IrEuropeanSwaptionPricingInput
    '''
    try:
        tmp_this= IrEuropeanSwaptionPricingInput()
        tmp_this.pricing_date.CopyFrom(p_pricing_date)
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.mkt_data.CopyFrom(p_mkt_data)
        tmp_this.pricing_settings.CopyFrom(p_pricing_settings)
        tmp_this.risk_settings.CopyFrom(p_risk_settings)
        tmp_this.use_binary=p_use_binary
        tmp_this.instrument_bin=p_instrument_bin
        tmp_this.mkt_data_bin=p_mkt_data_bin
        tmp_this.pricing_settings_bin=p_pricing_settings_bin
        tmp_this.risk_settings_bin=p_risk_settings_bin
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrEuropeanSwaptionPricingOutput
def dqCreateProtoIrEuropeanSwaptionPricingOutput(p_results, p_success, p_err_msg):
    '''
    @args:
        1. p_results: dqproto.PricingResults
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.IrEuropeanSwaptionPricingOutput
    '''
    try:
        tmp_this= IrEuropeanSwaptionPricingOutput()
        tmp_this.results.CopyFrom(p_results)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetIrSwaptionVolatilityInput
def dqCreateProtoGetIrSwaptionVolatilityInput(p_volatility_surface, p_forward, p_term, p_tenor, p_strikes):
    '''
    @args:
        1. p_volatility_surface: dqproto.IrSwaptionVolatilitySurface
        2. p_forward: double
        3. p_term: double
        4. p_tenor: double
        5. p_strikes: dqproto.Vector
    @return:
        dqproto.GetIrSwaptionVolatilityInput
    '''
    try:
        tmp_this= GetIrSwaptionVolatilityInput()
        tmp_this.volatility_surface.CopyFrom(p_volatility_surface)
        tmp_this.forward=p_forward
        tmp_this.term=p_term
        tmp_this.tenor=p_tenor
        tmp_this.strikes.CopyFrom(p_strikes)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetIrSwaptionVolatilityOutput
def dqCreateProtoGetIrSwaptionVolatilityOutput(p_volatilities, p_success, p_err_msg):
    '''
    @args:
        1. p_volatilities: dqproto.Vector
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.GetIrSwaptionVolatilityOutput
    '''
    try:
        tmp_this= GetIrSwaptionVolatilityOutput()
        tmp_this.volatilities.CopyFrom(p_volatilities)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrSwaptionVolatilitySurfaceBuildingInput
def dqCreateProtoIrSwaptionVolatilitySurfaceBuildingInput(p_reference_date, p_quote_cube, p_discount_curve, p_forward_curve, p_vol_surf_definition, p_build_settings, p_inst_name, p_underlying_swap_tempalte):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_quote_cube: dqproto.IrSwaptionQuoteCube
        3. p_discount_curve: dqproto.IrYieldCurve
        4. p_forward_curve: dqproto.IrYieldCurve
        5. p_vol_surf_definition: dqproto.VolatilitySurfaceDefinition
        6. p_build_settings: dqproto.VolatilitySurfaceBuildSettings
        7. p_inst_name: string
        8. p_underlying_swap_tempalte: dqproto.InterestRateInstrumentTemplate
    @return:
        dqproto.IrSwaptionVolatilitySurfaceBuildingInput
    '''
    try:
        tmp_this= IrSwaptionVolatilitySurfaceBuildingInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.quote_cube.CopyFrom(p_quote_cube)
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.forward_curve.CopyFrom(p_forward_curve)
        tmp_this.vol_surf_definition.CopyFrom(p_vol_surf_definition)
        tmp_this.build_settings.CopyFrom(p_build_settings)
        tmp_this.inst_name=p_inst_name
        tmp_this.underlying_swap_tempalte.CopyFrom(p_underlying_swap_tempalte)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrSwaptionVolatilitySurfaceBuildingOutput
def dqCreateProtoIrSwaptionVolatilitySurfaceBuildingOutput(p_vol_surf, p_success, p_err_msg):
    '''
    @args:
        1. p_vol_surf: dqproto.IrSwaptionVolatilitySurface
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.IrSwaptionVolatilitySurfaceBuildingOutput
    '''
    try:
        tmp_this= IrSwaptionVolatilitySurfaceBuildingOutput()
        tmp_this.vol_surf.CopyFrom(p_vol_surf)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IborIndexRateCalculationInput
def dqCreateProtoIborIndexRateCalculationInput(p_fixing_date, p_ibor_index, p_ir_yield_curve):
    '''
    @args:
        1. p_fixing_date: dqproto.Date
        2. p_ibor_index: dqproto.IborIndex
        3. p_ir_yield_curve: dqproto.IrYieldCurve
    @return:
        dqproto.IborIndexRateCalculationInput
    '''
    try:
        tmp_this= IborIndexRateCalculationInput()
        tmp_this.fixing_date.extend(p_fixing_date)
        tmp_this.ibor_index.CopyFrom(p_ibor_index)
        tmp_this.ir_yield_curve.CopyFrom(p_ir_yield_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IborIndexRateCalculationOutput
def dqCreateProtoIborIndexRateCalculationOutput(p_ibor_index_rate, p_success, p_err_msg):
    '''
    @args:
        1. p_ibor_index_rate: dqproto.Vector
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.IborIndexRateCalculationOutput
    '''
    try:
        tmp_this= IborIndexRateCalculationOutput()
        tmp_this.ibor_index_rate.CopyFrom(p_ibor_index_rate)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrVanillaSwapRateCalculationInput
def dqCreateProtoIrVanillaSwapRateCalculationInput(p_calculation_date, p_swap_tempalte, p_tenor, p_discount_curve, p_forward_curve):
    '''
    @args:
        1. p_calculation_date: dqproto.Date
        2. p_swap_tempalte: dqproto.InterestRateInstrumentTemplate
        3. p_tenor: dqproto.Period
        4. p_discount_curve: dqproto.IrYieldCurve
        5. p_forward_curve: dqproto.IrYieldCurve
    @return:
        dqproto.IrVanillaSwapRateCalculationInput
    '''
    try:
        tmp_this= IrVanillaSwapRateCalculationInput()
        tmp_this.calculation_date.CopyFrom(p_calculation_date)
        tmp_this.swap_tempalte.CopyFrom(p_swap_tempalte)
        tmp_this.tenor.CopyFrom(p_tenor)
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.forward_curve.CopyFrom(p_forward_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrVanillaSwapRateCalculationOutput
def dqCreateProtoIrVanillaSwapRateCalculationOutput(p_swap_rate, p_success, p_err_msg):
    '''
    @args:
        1. p_swap_rate: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.IrVanillaSwapRateCalculationOutput
    '''
    try:
        tmp_this= IrVanillaSwapRateCalculationOutput()
        tmp_this.swap_rate=p_swap_rate
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#TenorBasisSwapSpreadCalculationInput
def dqCreateProtoTenorBasisSwapSpreadCalculationInput(p_calculation_date, p_swap_tempalte, p_tenor, p_discount_curve, p_short_tenor_forward_curve, p_long_tenor_forward_curve):
    '''
    @args:
        1. p_calculation_date: dqproto.Date
        2. p_swap_tempalte: dqproto.InterestRateInstrumentTemplate
        3. p_tenor: dqproto.Period
        4. p_discount_curve: dqproto.IrYieldCurve
        5. p_short_tenor_forward_curve: dqproto.IrYieldCurve
        6. p_long_tenor_forward_curve: dqproto.IrYieldCurve
    @return:
        dqproto.TenorBasisSwapSpreadCalculationInput
    '''
    try:
        tmp_this= TenorBasisSwapSpreadCalculationInput()
        tmp_this.calculation_date.CopyFrom(p_calculation_date)
        tmp_this.swap_tempalte.CopyFrom(p_swap_tempalte)
        tmp_this.tenor.CopyFrom(p_tenor)
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.short_tenor_forward_curve.CopyFrom(p_short_tenor_forward_curve)
        tmp_this.long_tenor_forward_curve.CopyFrom(p_long_tenor_forward_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#TenorBasisSwapSpreadCalculationOutput
def dqCreateProtoTenorBasisSwapSpreadCalculationOutput(p_basis_spread, p_success, p_err_msg):
    '''
    @args:
        1. p_basis_spread: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.TenorBasisSwapSpreadCalculationOutput
    '''
    try:
        tmp_this= TenorBasisSwapSpreadCalculationOutput()
        tmp_this.basis_spread=p_basis_spread
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CrossCurrencyBasisSwapSpreadCalculationInput
def dqCreateProtoCrossCurrencyBasisSwapSpreadCalculationInput(p_calculation_date, p_swap_tempalte, p_tenor, p_fx_spot_rate, p_target_discount_curve, p_target_forward_curve, p_base_discount_curve, p_base_forward_curve):
    '''
    @args:
        1. p_calculation_date: dqproto.Date
        2. p_swap_tempalte: dqproto.InterestRateInstrumentTemplate
        3. p_tenor: dqproto.Period
        4. p_fx_spot_rate: dqproto.FxSpotRate
        5. p_target_discount_curve: dqproto.IrYieldCurve
        6. p_target_forward_curve: dqproto.IrYieldCurve
        7. p_base_discount_curve: dqproto.IrYieldCurve
        8. p_base_forward_curve: dqproto.IrYieldCurve
    @return:
        dqproto.CrossCurrencyBasisSwapSpreadCalculationInput
    '''
    try:
        tmp_this= CrossCurrencyBasisSwapSpreadCalculationInput()
        tmp_this.calculation_date.CopyFrom(p_calculation_date)
        tmp_this.swap_tempalte.CopyFrom(p_swap_tempalte)
        tmp_this.tenor.CopyFrom(p_tenor)
        tmp_this.fx_spot_rate.CopyFrom(p_fx_spot_rate)
        tmp_this.target_discount_curve.CopyFrom(p_target_discount_curve)
        tmp_this.target_forward_curve.CopyFrom(p_target_forward_curve)
        tmp_this.base_discount_curve.CopyFrom(p_base_discount_curve)
        tmp_this.base_forward_curve.CopyFrom(p_base_forward_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CrossCurrencyBasisSwapSpreadCalculationOutput
def dqCreateProtoCrossCurrencyBasisSwapSpreadCalculationOutput(p_basis_spread, p_success, p_err_msg):
    '''
    @args:
        1. p_basis_spread: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CrossCurrencyBasisSwapSpreadCalculationOutput
    '''
    try:
        tmp_this= CrossCurrencyBasisSwapSpreadCalculationOutput()
        tmp_this.basis_spread=p_basis_spread
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CrossCurrencySwapRateCalculationInput
def dqCreateProtoCrossCurrencySwapRateCalculationInput(p_calculation_date, p_swap_tempalte, p_tenor, p_fx_spot_rate, p_target_discount_curve, p_base_discount_curve, p_base_forward_curve):
    '''
    @args:
        1. p_calculation_date: dqproto.Date
        2. p_swap_tempalte: dqproto.InterestRateInstrumentTemplate
        3. p_tenor: dqproto.Period
        4. p_fx_spot_rate: dqproto.FxSpotRate
        5. p_target_discount_curve: dqproto.IrYieldCurve
        6. p_base_discount_curve: dqproto.IrYieldCurve
        7. p_base_forward_curve: dqproto.IrYieldCurve
    @return:
        dqproto.CrossCurrencySwapRateCalculationInput
    '''
    try:
        tmp_this= CrossCurrencySwapRateCalculationInput()
        tmp_this.calculation_date.CopyFrom(p_calculation_date)
        tmp_this.swap_tempalte.CopyFrom(p_swap_tempalte)
        tmp_this.tenor.CopyFrom(p_tenor)
        tmp_this.fx_spot_rate.CopyFrom(p_fx_spot_rate)
        tmp_this.target_discount_curve.CopyFrom(p_target_discount_curve)
        tmp_this.base_discount_curve.CopyFrom(p_base_discount_curve)
        tmp_this.base_forward_curve.CopyFrom(p_base_forward_curve)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CrossCurrencySwapRateCalculationOutput
def dqCreateProtoCrossCurrencySwapRateCalculationOutput(p_swap_rate, p_success, p_err_msg):
    '''
    @args:
        1. p_swap_rate: double
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CrossCurrencySwapRateCalculationOutput
    '''
    try:
        tmp_this= CrossCurrencySwapRateCalculationOutput()
        tmp_this.swap_rate=p_swap_rate
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IborIndex
def dqCreateProtoIborIndex(p_type, p_name, p_tenor, p_currency, p_start_delay, p_calendar, p_day_count_convention, p_interest_day_convention, p_date_roll_convention, p_ibor_index_type):
    '''
    @args:
        1. p_type: dqproto.InterestRateIndexType
        2. p_name: string
        3. p_tenor: dqproto.Period
        4. p_currency: string
        5. p_start_delay: dqproto.Period
        6. p_calendar: string
        7. p_day_count_convention: dqproto.DayCountConvention
        8. p_interest_day_convention: dqproto.BusinessDayConvention
        9. p_date_roll_convention: dqproto.DateRollConvention
        10. p_ibor_index_type: dqproto.IborIndexType
    @return:
        dqproto.IborIndex
    '''
    try:
        tmp_this= IborIndex()
        tmp_this.type=p_type
        tmp_this.name=p_name
        tmp_this.tenor.CopyFrom(p_tenor)
        tmp_this.currency=p_currency
        tmp_this.start_delay.CopyFrom(p_start_delay)
        tmp_this.calendar.extend(p_calendar)
        tmp_this.day_count_convention=p_day_count_convention
        tmp_this.interest_day_convention=p_interest_day_convention
        tmp_this.date_roll_convention=p_date_roll_convention
        tmp_this.ibor_index_type=p_ibor_index_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IborIndexList
def dqCreateProtoIborIndexList(p_ibor_index):
    '''
    @args:
        1. p_ibor_index: dqproto.IborIndex
    @return:
        dqproto.IborIndexList
    '''
    try:
        tmp_this= IborIndexList()
        tmp_this.ibor_index.extend(p_ibor_index)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#TimeSeriesMap
def dqCreateProtoTimeSeriesMap(p_name, p_time_series):
    '''
    @args:
        1. p_name: string
        2. p_time_series: dqproto.TimeSeries
    @return:
        dqproto.TimeSeriesMap
    '''
    try:
        tmp_this= TimeSeriesMap()
        tmp_this.name=p_name
        tmp_this.time_series.CopyFrom(p_time_series)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#LegFixings
def dqCreateProtoLegFixings(p_leg_fixings):
    '''
    @args:
        1. p_leg_fixings: dqproto.TimeSeriesMap
    @return:
        dqproto.LegFixings
    '''
    try:
        tmp_this= LegFixings()
        tmp_this.leg_fixings.extend(p_leg_fixings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InterestRateLegScheduleDefinition.InterestCaculationScheduleDefinition
def dqCreateProtoInterestRateLegScheduleDefinition_InterestCaculationScheduleDefinition(p_schedule_generation_method, p_reference_schedule, p_calendar_list, p_frequency, p_business_day_convention, p_stub_policy, p_broken_period_type, p_date_roll_convention, p_relative_schedule_generation_mode):
    '''
    @args:
        1. p_schedule_generation_method: dqproto.ScheduleGenerationMethod
        2. p_reference_schedule: dqproto.InterestScheduleType
        3. p_calendar_list: string
        4. p_frequency: dqproto.Frequency
        5. p_business_day_convention: dqproto.BusinessDayConvention
        6. p_stub_policy: dqproto.StubPolicy
        7. p_broken_period_type: dqproto.BrokenPeriodType
        8. p_date_roll_convention: dqproto.DateRollConvention
        9. p_relative_schedule_generation_mode: dqproto.RelativeScheduleGenerationMode
    @return:
        dqproto.InterestRateLegScheduleDefinition.InterestCaculationScheduleDefinition
    '''
    try:
        tmp_this= InterestRateLegScheduleDefinition.InterestCaculationScheduleDefinition()
        tmp_this.schedule_generation_method=p_schedule_generation_method
        tmp_this.reference_schedule=p_reference_schedule
        tmp_this.calendar_list.extend(p_calendar_list)
        tmp_this.frequency=p_frequency
        tmp_this.business_day_convention=p_business_day_convention
        tmp_this.stub_policy=p_stub_policy
        tmp_this.broken_period_type=p_broken_period_type
        tmp_this.date_roll_convention=p_date_roll_convention
        tmp_this.relative_schedule_generation_mode=p_relative_schedule_generation_mode
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InterestRateLegScheduleDefinition.InterestPaymentScheduleDefinition
def dqCreateProtoInterestRateLegScheduleDefinition_InterestPaymentScheduleDefinition(p_schedule_generation_method, p_reference_schedule, p_calendar_list, p_frequency, p_business_day_convention, p_payment_date_mode, p_frequency_ratio, p_payment_date_offset, p_relative_schedule_generation_mode):
    '''
    @args:
        1. p_schedule_generation_method: dqproto.ScheduleGenerationMethod
        2. p_reference_schedule: dqproto.InterestScheduleType
        3. p_calendar_list: string
        4. p_frequency: dqproto.Frequency
        5. p_business_day_convention: dqproto.BusinessDayConvention
        6. p_payment_date_mode: dqproto.DateGenerationMode
        7. p_frequency_ratio: int32
        8. p_payment_date_offset: dqproto.Period
        9. p_relative_schedule_generation_mode: dqproto.RelativeScheduleGenerationMode
    @return:
        dqproto.InterestRateLegScheduleDefinition.InterestPaymentScheduleDefinition
    '''
    try:
        tmp_this= InterestRateLegScheduleDefinition.InterestPaymentScheduleDefinition()
        tmp_this.schedule_generation_method=p_schedule_generation_method
        tmp_this.reference_schedule=p_reference_schedule
        tmp_this.calendar_list.extend(p_calendar_list)
        tmp_this.frequency=p_frequency
        tmp_this.business_day_convention=p_business_day_convention
        tmp_this.payment_date_mode=p_payment_date_mode
        tmp_this.frequency_ratio=p_frequency_ratio
        tmp_this.payment_date_offset.CopyFrom(p_payment_date_offset)
        tmp_this.relative_schedule_generation_mode=p_relative_schedule_generation_mode
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InterestRateLegScheduleDefinition.InterestRateFixingScheduleDefinition
def dqCreateProtoInterestRateLegScheduleDefinition_InterestRateFixingScheduleDefinition(p_schedule_generation_method, p_reference_schedule, p_calendar_list, p_frequency, p_business_day_convention, p_fixing_date_mode, p_frequency_ratio, p_fixing_date_offset, p_relative_schedule_generation_mode):
    '''
    @args:
        1. p_schedule_generation_method: dqproto.ScheduleGenerationMethod
        2. p_reference_schedule: dqproto.InterestScheduleType
        3. p_calendar_list: string
        4. p_frequency: dqproto.Frequency
        5. p_business_day_convention: dqproto.BusinessDayConvention
        6. p_fixing_date_mode: dqproto.DateGenerationMode
        7. p_frequency_ratio: int32
        8. p_fixing_date_offset: dqproto.Period
        9. p_relative_schedule_generation_mode: dqproto.RelativeScheduleGenerationMode
    @return:
        dqproto.InterestRateLegScheduleDefinition.InterestRateFixingScheduleDefinition
    '''
    try:
        tmp_this= InterestRateLegScheduleDefinition.InterestRateFixingScheduleDefinition()
        tmp_this.schedule_generation_method=p_schedule_generation_method
        tmp_this.reference_schedule=p_reference_schedule
        tmp_this.calendar_list.extend(p_calendar_list)
        tmp_this.frequency=p_frequency
        tmp_this.business_day_convention=p_business_day_convention
        tmp_this.fixing_date_mode=p_fixing_date_mode
        tmp_this.frequency_ratio=p_frequency_ratio
        tmp_this.fixing_date_offset.CopyFrom(p_fixing_date_offset)
        tmp_this.relative_schedule_generation_mode=p_relative_schedule_generation_mode
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InterestRateLegScheduleDefinition
def dqCreateProtoInterestRateLegScheduleDefinition(p_interest_calculation_schedule_definition, p_interest_payment_schedule_definition, p_interest_rate_fixing_schedule_definition):
    '''
    @args:
        1. p_interest_calculation_schedule_definition: dqproto.InterestRateLegScheduleDefinition.InterestCaculationScheduleDefinition
        2. p_interest_payment_schedule_definition: dqproto.InterestRateLegScheduleDefinition.InterestPaymentScheduleDefinition
        3. p_interest_rate_fixing_schedule_definition: dqproto.InterestRateLegScheduleDefinition.InterestRateFixingScheduleDefinition
    @return:
        dqproto.InterestRateLegScheduleDefinition
    '''
    try:
        tmp_this= InterestRateLegScheduleDefinition()
        tmp_this.interest_calculation_schedule_definition.CopyFrom(p_interest_calculation_schedule_definition)
        tmp_this.interest_payment_schedule_definition.CopyFrom(p_interest_payment_schedule_definition)
        tmp_this.interest_rate_fixing_schedule_definition.CopyFrom(p_interest_rate_fixing_schedule_definition)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InterestRateLegDefinition
def dqCreateProtoInterestRateLegDefinition(p_leg_type, p_currency, p_day_count_convention, p_ibor_index, p_payment_discount_method, p_interest_calculation_method, p_interest_rate_calculation_method, p_broken_rate_calculation_method, p_notional_exchange, p_spread, p_fx_convert, p_fx_reset, p_schedule_definition):
    '''
    @args:
        1. p_leg_type: dqproto.InterestRateLegType
        2. p_currency: string
        3. p_day_count_convention: dqproto.DayCountConvention
        4. p_ibor_index: string
        5. p_payment_discount_method: dqproto.PaymentDiscountMethod
        6. p_interest_calculation_method: dqproto.InterestCalculationMethod
        7. p_interest_rate_calculation_method: dqproto.InterestRateCalculationMethod
        8. p_broken_rate_calculation_method: dqproto.BrokenRateCalculationMethod
        9. p_notional_exchange: dqproto.NotionalExchange
        10. p_spread: bool
        11. p_fx_convert: bool
        12. p_fx_reset: bool
        13. p_schedule_definition: dqproto.InterestRateLegScheduleDefinition
    @return:
        dqproto.InterestRateLegDefinition
    '''
    try:
        tmp_this= InterestRateLegDefinition()
        tmp_this.leg_type=p_leg_type
        tmp_this.currency=p_currency
        tmp_this.day_count_convention=p_day_count_convention
        tmp_this.ibor_index=p_ibor_index
        tmp_this.payment_discount_method=p_payment_discount_method
        tmp_this.interest_calculation_method=p_interest_calculation_method
        tmp_this.interest_rate_calculation_method=p_interest_rate_calculation_method
        tmp_this.broken_rate_calculation_method=p_broken_rate_calculation_method
        tmp_this.notional_exchange=p_notional_exchange
        tmp_this.spread=p_spread
        tmp_this.fx_convert=p_fx_convert
        tmp_this.fx_reset=p_fx_reset
        tmp_this.schedule_definition.CopyFrom(p_schedule_definition)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InterestSchedule.Row
def dqCreateProtoInterestSchedule_Row(p_fixing_date, p_start_date, p_end_date, p_fixing_value, p_fixing_weight):
    '''
    @args:
        1. p_fixing_date: dqproto.Date
        2. p_start_date: dqproto.Date
        3. p_end_date: dqproto.Date
        4. p_fixing_value: double
        5. p_fixing_weight: double
    @return:
        dqproto.InterestSchedule.Row
    '''
    try:
        tmp_this= InterestSchedule.Row()
        tmp_this.fixing_date.CopyFrom(p_fixing_date)
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.end_date.CopyFrom(p_end_date)
        tmp_this.fixing_value=p_fixing_value
        tmp_this.fixing_weight=p_fixing_weight
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InterestSchedule
def dqCreateProtoInterestSchedule(p_data):
    '''
    @args:
        1. p_data: dqproto.InterestSchedule.Row
    @return:
        dqproto.InterestSchedule
    '''
    try:
        tmp_this= InterestSchedule()
        tmp_this.data.extend(p_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCashFlowSchedule.Row
def dqCreateProtoIrCashFlowSchedule_Row(p_payment_date, p_interest_schedule, p_notional):
    '''
    @args:
        1. p_payment_date: dqproto.Date
        2. p_interest_schedule: dqproto.InterestSchedule
        3. p_notional: double
    @return:
        dqproto.IrCashFlowSchedule.Row
    '''
    try:
        tmp_this= IrCashFlowSchedule.Row()
        tmp_this.payment_date.CopyFrom(p_payment_date)
        tmp_this.interest_schedule.CopyFrom(p_interest_schedule)
        tmp_this.notional=p_notional
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCashFlowSchedule
def dqCreateProtoIrCashFlowSchedule(p_data):
    '''
    @args:
        1. p_data: dqproto.IrCashFlowSchedule.Row
    @return:
        dqproto.IrCashFlowSchedule
    '''
    try:
        tmp_this= IrCashFlowSchedule()
        tmp_this.data.extend(p_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InterestRateLeg
def dqCreateProtoInterestRateLeg(p_pay_receive, p_leg_definition, p_cash_flow_schedule):
    '''
    @args:
        1. p_pay_receive: dqproto.PayReceiveFlag
        2. p_leg_definition: dqproto.InterestRateLegDefinition
        3. p_cash_flow_schedule: dqproto.IrCashFlowSchedule
    @return:
        dqproto.InterestRateLeg
    '''
    try:
        tmp_this= InterestRateLeg()
        tmp_this.pay_receive=p_pay_receive
        tmp_this.leg_definition.CopyFrom(p_leg_definition)
        tmp_this.cash_flow_schedule.CopyFrom(p_cash_flow_schedule)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrVanillaLeg
def dqCreateProtoIrVanillaLeg(p_interest_rate_leg, p_rate, p_notional):
    '''
    @args:
        1. p_interest_rate_leg: dqproto.InterestRateLeg
        2. p_rate: double
        3. p_notional: dqproto.Notional
    @return:
        dqproto.IrVanillaLeg
    '''
    try:
        tmp_this= IrVanillaLeg()
        tmp_this.interest_rate_leg.CopyFrom(p_interest_rate_leg)
        tmp_this.rate=p_rate
        tmp_this.notional.CopyFrom(p_notional)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InterestRateInstrument
def dqCreateProtoInterestRateInstrument(p_instrument, p_num_legs, p_type):
    '''
    @args:
        1. p_instrument: dqproto.FinancialInstrument
        2. p_num_legs: int32
        3. p_type: dqproto.InstrumentType
    @return:
        dqproto.InterestRateInstrument
    '''
    try:
        tmp_this= InterestRateInstrument()
        tmp_this.instrument.CopyFrom(p_instrument)
        tmp_this.num_legs=p_num_legs
        tmp_this.type=p_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCrossCurrencyBasisSwap
def dqCreateProtoIrCrossCurrencyBasisSwap(p_ir_vanilla_instrument, p_spread_leg_index, p_base_leg_index):
    '''
    @args:
        1. p_ir_vanilla_instrument: dqproto.IrVanillaInstrument
        2. p_spread_leg_index: int32
        3. p_base_leg_index: int32
    @return:
        dqproto.IrCrossCurrencyBasisSwap
    '''
    try:
        tmp_this= IrCrossCurrencyBasisSwap()
        tmp_this.ir_vanilla_instrument.CopyFrom(p_ir_vanilla_instrument)
        tmp_this.spread_leg_index=p_spread_leg_index
        tmp_this.base_leg_index=p_base_leg_index
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCrossCurrencyFixedFloatingSwap
def dqCreateProtoIrCrossCurrencyFixedFloatingSwap(p_ir_vanilla_instrument, p_fixed_leg_index, p_floating_leg_index):
    '''
    @args:
        1. p_ir_vanilla_instrument: dqproto.IrVanillaInstrument
        2. p_fixed_leg_index: int32
        3. p_floating_leg_index: int32
    @return:
        dqproto.IrCrossCurrencyFixedFloatingSwap
    '''
    try:
        tmp_this= IrCrossCurrencyFixedFloatingSwap()
        tmp_this.ir_vanilla_instrument.CopyFrom(p_ir_vanilla_instrument)
        tmp_this.fixed_leg_index=p_fixed_leg_index
        tmp_this.floating_leg_index=p_floating_leg_index
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCrossCurrencySwap
def dqCreateProtoIrCrossCurrencySwap(p_legs, p_instrument):
    '''
    @args:
        1. p_legs: dqproto.IrVanillaLeg
        2. p_instrument: dqproto.IrVanillaInstrument
    @return:
        dqproto.IrCrossCurrencySwap
    '''
    try:
        tmp_this= IrCrossCurrencySwap()
        tmp_this.legs.extend(p_legs)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrDeposit
def dqCreateProtoIrDeposit(p_reference_date, p_inst_name, p_tenor, p_rate, p_pay_receive, p_notional, p_instrument):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_inst_name: string
        3. p_tenor: dqproto.Period
        4. p_rate: double
        5. p_pay_receive: dqproto.PayReceiveFlag
        6. p_notional: double
        7. p_instrument: dqproto.IrVanillaInstrument
    @return:
        dqproto.IrDeposit
    '''
    try:
        tmp_this= IrDeposit()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.inst_name=p_inst_name
        tmp_this.tenor.CopyFrom(p_tenor)
        tmp_this.rate=p_rate
        tmp_this.pay_receive=p_pay_receive
        tmp_this.notional=p_notional
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrFixedFloatingSwap
def dqCreateProtoIrFixedFloatingSwap(p_ir_vanilla_instrument, p_fixed_leg_index, p_floating_leg_index):
    '''
    @args:
        1. p_ir_vanilla_instrument: dqproto.IrVanillaInstrument
        2. p_fixed_leg_index: int32
        3. p_floating_leg_index: int32
    @return:
        dqproto.IrFixedFloatingSwap
    '''
    try:
        tmp_this= IrFixedFloatingSwap()
        tmp_this.ir_vanilla_instrument.CopyFrom(p_ir_vanilla_instrument)
        tmp_this.fixed_leg_index=p_fixed_leg_index
        tmp_this.floating_leg_index=p_floating_leg_index
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrForwardRateAgreement
def dqCreateProtoIrForwardRateAgreement(p_reference_date, p_inst_name, p_start, p_rate, p_pay_receive, p_notional, p_instrument):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_inst_name: string
        3. p_start: dqproto.Period
        4. p_rate: double
        5. p_pay_receive: dqproto.PayReceiveFlag
        6. p_notional: double
        7. p_instrument: dqproto.IrVanillaInstrument
    @return:
        dqproto.IrForwardRateAgreement
    '''
    try:
        tmp_this= IrForwardRateAgreement()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.inst_name=p_inst_name
        tmp_this.start.CopyFrom(p_start)
        tmp_this.rate=p_rate
        tmp_this.pay_receive=p_pay_receive
        tmp_this.notional=p_notional
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrTenorBasisSwap
def dqCreateProtoIrTenorBasisSwap(p_ir_vanilla_instrument, p_spread_leg_index, p_base_leg_index):
    '''
    @args:
        1. p_ir_vanilla_instrument: dqproto.IrVanillaInstrument
        2. p_spread_leg_index: int32
        3. p_base_leg_index: int32
    @return:
        dqproto.IrTenorBasisSwap
    '''
    try:
        tmp_this= IrTenorBasisSwap()
        tmp_this.ir_vanilla_instrument.CopyFrom(p_ir_vanilla_instrument)
        tmp_this.spread_leg_index=p_spread_leg_index
        tmp_this.base_leg_index=p_base_leg_index
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrVanillaInstrument
def dqCreateProtoIrVanillaInstrument(p_interest_rate_instrument, p_legs):
    '''
    @args:
        1. p_interest_rate_instrument: dqproto.InterestRateInstrument
        2. p_legs: dqproto.IrVanillaLeg
    @return:
        dqproto.IrVanillaInstrument
    '''
    try:
        tmp_this= IrVanillaInstrument()
        tmp_this.interest_rate_instrument.CopyFrom(p_interest_rate_instrument)
        tmp_this.legs.extend(p_legs)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrVanillaSwap
def dqCreateProtoIrVanillaSwap(p_reference_date, p_inst_name, p_tenor, p_pay_receive, p_fixed_rate, p_spread, p_notional, p_leg_fixings, p_instrument):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_inst_name: string
        3. p_tenor: dqproto.Period
        4. p_pay_receive: dqproto.PayReceiveFlag
        5. p_fixed_rate: double
        6. p_spread: double
        7. p_notional: double
        8. p_leg_fixings: dqproto.Vector
        9. p_instrument: dqproto.IrVanillaInstrument
    @return:
        dqproto.IrVanillaSwap
    '''
    try:
        tmp_this= IrVanillaSwap()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.inst_name=p_inst_name
        tmp_this.tenor.CopyFrom(p_tenor)
        tmp_this.pay_receive=p_pay_receive
        tmp_this.fixed_rate=p_fixed_rate
        tmp_this.spread=p_spread
        tmp_this.notional=p_notional
        tmp_this.leg_fixings.CopyFrom(p_leg_fixings)
        tmp_this.instrument.CopyFrom(p_instrument)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InterestRateInstrumentTemplate
def dqCreateProtoInterestRateInstrumentTemplate(p_instrument_type, p_instrument_name, p_start_delay, p_leg_definition, p_start_convention):
    '''
    @args:
        1. p_instrument_type: dqproto.InstrumentType
        2. p_instrument_name: string
        3. p_start_delay: dqproto.Period
        4. p_leg_definition: dqproto.InterestRateLegDefinition
        5. p_start_convention: dqproto.InstrumentStartConvention
    @return:
        dqproto.InterestRateInstrumentTemplate
    '''
    try:
        tmp_this= InterestRateInstrumentTemplate()
        tmp_this.instrument_type=p_instrument_type
        tmp_this.instrument_name=p_instrument_name
        tmp_this.start_delay.CopyFrom(p_start_delay)
        tmp_this.leg_definition.extend(p_leg_definition)
        tmp_this.start_convention=p_start_convention
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InterestRateInstrumentTemplateList
def dqCreateProtoInterestRateInstrumentTemplateList(p_interest_rate_instrument_template):
    '''
    @args:
        1. p_interest_rate_instrument_template: dqproto.InterestRateInstrumentTemplate
    @return:
        dqproto.InterestRateInstrumentTemplateList
    '''
    try:
        tmp_this= InterestRateInstrumentTemplateList()
        tmp_this.interest_rate_instrument_template.extend(p_interest_rate_instrument_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrFutureTemplate
def dqCreateProtoIrFutureTemplate(p_ir_instrument_template, p_settle_day_rule, p_mkt_convention):
    '''
    @args:
        1. p_ir_instrument_template: dqproto.InterestRateInstrumentTemplate
        2. p_settle_day_rule: dqproto.IrFutureTemplate.SettleDayRule
        3. p_mkt_convention: dqproto.IrFutureMktConvention
    @return:
        dqproto.IrFutureTemplate
    '''
    try:
        tmp_this= IrFutureTemplate()
        tmp_this.ir_instrument_template.CopyFrom(p_ir_instrument_template)
        tmp_this.settle_day_rule.extend(p_settle_day_rule)
        tmp_this.mkt_convention=p_mkt_convention
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrFutureTemplate.SettleDayRule
def dqCreateProtoIrFutureTemplate_SettleDayRule(p_name, p_month, p_ith_week, p_week_day, p_is_active):
    '''
    @args:
        1. p_name: string
        2. p_month: int32
        3. p_ith_week: int32
        4. p_week_day: dqproto.Weekday
        5. p_is_active: bool
    @return:
        dqproto.IrFutureTemplate.SettleDayRule
    '''
    try:
        tmp_this= IrFutureTemplate.SettleDayRule()
        tmp_this.name=p_name
        tmp_this.month=p_month
        tmp_this.ith_week=p_ith_week
        tmp_this.week_day=p_week_day
        tmp_this.is_active=p_is_active
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrFutureTemplateList
def dqCreateProtoIrFutureTemplateList(p_ir_future_template):
    '''
    @args:
        1. p_ir_future_template: dqproto.IrFutureTemplate
    @return:
        dqproto.IrFutureTemplateList
    '''
    try:
        tmp_this= IrFutureTemplateList()
        tmp_this.ir_future_template.extend(p_ir_future_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrOptionlet
def dqCreateProtoIrOptionlet(p_ibor_index, p_start_date, p_end_date, p_payment_date, p_fixing_date, p_ir_instrument, p_european_option, p_notional):
    '''
    @args:
        1. p_ibor_index: dqproto.IborIndex
        2. p_start_date: dqproto.Date
        3. p_end_date: dqproto.Date
        4. p_payment_date: dqproto.Date
        5. p_fixing_date: dqproto.Date
        6. p_ir_instrument: dqproto.InterestRateInstrument
        7. p_european_option: dqproto.EuropeanOption
        8. p_notional: dqproto.Notional
    @return:
        dqproto.IrOptionlet
    '''
    try:
        tmp_this= IrOptionlet()
        tmp_this.ibor_index.CopyFrom(p_ibor_index)
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.end_date.CopyFrom(p_end_date)
        tmp_this.payment_date.CopyFrom(p_payment_date)
        tmp_this.fixing_date.CopyFrom(p_fixing_date)
        tmp_this.ir_instrument.CopyFrom(p_ir_instrument)
        tmp_this.european_option.CopyFrom(p_european_option)
        tmp_this.notional.CopyFrom(p_notional)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrCapFloor
def dqCreateProtoIrCapFloor(p_type, p_start_date, p_end_date, p_notional, p_strike, p_ir_optionlets, p_leg_definition):
    '''
    @args:
        1. p_type: dqproto.Type
        2. p_start_date: dqproto.Date
        3. p_end_date: dqproto.Date
        4. p_notional: dqproto.Notional
        5. p_strike: double
        6. p_ir_optionlets: dqproto.IrOptionlet
        7. p_leg_definition: dqproto.InterestRateLegDefinition
    @return:
        dqproto.IrCapFloor
    '''
    try:
        tmp_this= IrCapFloor()
        tmp_this.type=p_type
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.end_date.CopyFrom(p_end_date)
        tmp_this.notional.CopyFrom(p_notional)
        tmp_this.strike=p_strike
        tmp_this.ir_optionlets.extend(p_ir_optionlets)
        tmp_this.leg_definition.CopyFrom(p_leg_definition)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrEuropeanSwaption
def dqCreateProtoIrEuropeanSwaption(p_exercise_date, p_settlement_date, p_settlement_type, p_underlying_swap, p_ir_instrument, p_vanilla_payoff):
    '''
    @args:
        1. p_exercise_date: dqproto.Date
        2. p_settlement_date: dqproto.Date
        3. p_settlement_type: dqproto.SettlementType
        4. p_underlying_swap: dqproto.IrFixedFloatingSwap
        5. p_ir_instrument: dqproto.InterestRateInstrument
        6. p_vanilla_payoff: dqproto.VanillaPayoff
    @return:
        dqproto.IrEuropeanSwaption
    '''
    try:
        tmp_this= IrEuropeanSwaption()
        tmp_this.exercise_date.CopyFrom(p_exercise_date)
        tmp_this.settlement_date.CopyFrom(p_settlement_date)
        tmp_this.settlement_type=p_settlement_type
        tmp_this.underlying_swap.CopyFrom(p_underlying_swap)
        tmp_this.ir_instrument.CopyFrom(p_ir_instrument)
        tmp_this.vanilla_payoff.CopyFrom(p_vanilla_payoff)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildIrForwardRateAgreementInput
def dqCreateProtoBuildIrForwardRateAgreementInput(p_reference_date, p_inst_name, p_start, p_rate, p_pay_receive, p_notional, p_leg_fixings):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_inst_name: string
        3. p_start: dqproto.Period
        4. p_rate: double
        5. p_pay_receive: dqproto.PayReceiveFlag
        6. p_notional: double
        7. p_leg_fixings: dqproto.LegFixings
    @return:
        dqproto.BuildIrForwardRateAgreementInput
    '''
    try:
        tmp_this= BuildIrForwardRateAgreementInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.inst_name=p_inst_name
        tmp_this.start.CopyFrom(p_start)
        tmp_this.rate=p_rate
        tmp_this.pay_receive=p_pay_receive
        tmp_this.notional=p_notional
        tmp_this.leg_fixings.CopyFrom(p_leg_fixings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildIrForwardRateAgreementOutput
def dqCreateProtoBuildIrForwardRateAgreementOutput(p_inst, p_success, p_err_msg):
    '''
    @args:
        1. p_inst: dqproto.IrVanillaInstrument
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildIrForwardRateAgreementOutput
    '''
    try:
        tmp_this= BuildIrForwardRateAgreementOutput()
        tmp_this.inst.CopyFrom(p_inst)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildIrFutureInput
def dqCreateProtoBuildIrFutureInput(p_reference_date, p_inst_name, p_inst_tenor, p_quote):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_inst_name: string
        3. p_inst_tenor: dqproto.Period
        4. p_quote: double
    @return:
        dqproto.BuildIrFutureInput
    '''
    try:
        tmp_this= BuildIrFutureInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.inst_name=p_inst_name
        tmp_this.inst_tenor.CopyFrom(p_inst_tenor)
        tmp_this.quote=p_quote
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildIrFutureOutput
def dqCreateProtoBuildIrFutureOutput(p_inst, p_success, p_err_msg):
    '''
    @args:
        1. p_inst: dqproto.IrVanillaInstrument
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildIrFutureOutput
    '''
    try:
        tmp_this= BuildIrFutureOutput()
        tmp_this.inst.CopyFrom(p_inst)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildIrVanillaInstrumentInput
def dqCreateProtoBuildIrVanillaInstrumentInput(p_start_date, p_maturity_date, p_pay_receive, p_fixed_rate, p_spread, p_notional, p_capital_conversion_rate, p_inst_tempalte, p_leg_fixings):
    '''
    @args:
        1. p_start_date: dqproto.Date
        2. p_maturity_date: dqproto.Date
        3. p_pay_receive: dqproto.PayReceiveFlag
        4. p_fixed_rate: double
        5. p_spread: double
        6. p_notional: double
        7. p_capital_conversion_rate: double
        8. p_inst_tempalte: dqproto.InterestRateInstrumentTemplate
        9. p_leg_fixings: dqproto.LegFixings
    @return:
        dqproto.BuildIrVanillaInstrumentInput
    '''
    try:
        tmp_this= BuildIrVanillaInstrumentInput()
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.maturity_date.CopyFrom(p_maturity_date)
        tmp_this.pay_receive=p_pay_receive
        tmp_this.fixed_rate=p_fixed_rate
        tmp_this.spread=p_spread
        tmp_this.notional=p_notional
        tmp_this.capital_conversion_rate=p_capital_conversion_rate
        tmp_this.inst_tempalte.CopyFrom(p_inst_tempalte)
        tmp_this.leg_fixings.CopyFrom(p_leg_fixings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildIrVanillaInstrumentOutput
def dqCreateProtoBuildIrVanillaInstrumentOutput(p_inst, p_success, p_err_msg):
    '''
    @args:
        1. p_inst: dqproto.IrVanillaInstrument
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildIrVanillaInstrumentOutput
    '''
    try:
        tmp_this= BuildIrVanillaInstrumentOutput()
        tmp_this.inst.CopyFrom(p_inst)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrFutureDateCalculationInput
def dqCreateProtoIrFutureDateCalculationInput(p_instrument_name, p_term, p_as_of_date):
    '''
    @args:
        1. p_instrument_name: string
        2. p_term: string
        3. p_as_of_date: dqproto.Date
    @return:
        dqproto.IrFutureDateCalculationInput
    '''
    try:
        tmp_this= IrFutureDateCalculationInput()
        tmp_this.instrument_name=p_instrument_name
        tmp_this.term=p_term
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IrFutureDateCalculationOutput
def dqCreateProtoIrFutureDateCalculationOutput(p_ir_future_date, p_success, p_err_msg):
    '''
    @args:
        1. p_ir_future_date: dqproto.Date
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.IrFutureDateCalculationOutput
    '''
    try:
        tmp_this= IrFutureDateCalculationOutput()
        tmp_this.ir_future_date.CopyFrom(p_ir_future_date)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildCrossCurrencySwapInput
def dqCreateProtoBuildCrossCurrencySwapInput(p_reference_date, p_tenor, p_rate, p_pay_receive, p_notional, p_capital_conversion_rate, p_leg_fixings, p_inst_tempalte):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_tenor: dqproto.Period
        3. p_rate: double
        4. p_pay_receive: dqproto.PayReceiveFlag
        5. p_notional: double
        6. p_capital_conversion_rate: double
        7. p_leg_fixings: dqproto.LegFixings
        8. p_inst_tempalte: dqproto.InterestRateInstrumentTemplate
    @return:
        dqproto.BuildCrossCurrencySwapInput
    '''
    try:
        tmp_this= BuildCrossCurrencySwapInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.tenor.CopyFrom(p_tenor)
        tmp_this.rate=p_rate
        tmp_this.pay_receive=p_pay_receive
        tmp_this.notional=p_notional
        tmp_this.capital_conversion_rate=p_capital_conversion_rate
        tmp_this.leg_fixings.CopyFrom(p_leg_fixings)
        tmp_this.inst_tempalte.CopyFrom(p_inst_tempalte)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildCrossCurrencySwapOutput
def dqCreateProtoBuildCrossCurrencySwapOutput(p_inst, p_success, p_err_msg):
    '''
    @args:
        1. p_inst: dqproto.IrVanillaInstrument
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildCrossCurrencySwapOutput
    '''
    try:
        tmp_this= BuildCrossCurrencySwapOutput()
        tmp_this.inst.CopyFrom(p_inst)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildIrEuropeanSwaptionInput
def dqCreateProtoBuildIrEuropeanSwaptionInput(p_exercise_date, p_settlement_date, p_settlement_type, p_swap_maturity, p_fixed_rate, p_pay_receive, p_notional, p_inst_tempalte):
    '''
    @args:
        1. p_exercise_date: dqproto.Date
        2. p_settlement_date: dqproto.Date
        3. p_settlement_type: dqproto.SettlementType
        4. p_swap_maturity: dqproto.Date
        5. p_fixed_rate: double
        6. p_pay_receive: dqproto.PayReceiveFlag
        7. p_notional: dqproto.Notional
        8. p_inst_tempalte: dqproto.InterestRateInstrumentTemplate
    @return:
        dqproto.BuildIrEuropeanSwaptionInput
    '''
    try:
        tmp_this= BuildIrEuropeanSwaptionInput()
        tmp_this.exercise_date.CopyFrom(p_exercise_date)
        tmp_this.settlement_date.CopyFrom(p_settlement_date)
        tmp_this.settlement_type=p_settlement_type
        tmp_this.swap_maturity.CopyFrom(p_swap_maturity)
        tmp_this.fixed_rate=p_fixed_rate
        tmp_this.pay_receive=p_pay_receive
        tmp_this.notional.CopyFrom(p_notional)
        tmp_this.inst_tempalte.CopyFrom(p_inst_tempalte)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildIrEuropeanSwaptionOutput
def dqCreateProtoBuildIrEuropeanSwaptionOutput(p_european_swaption, p_success, p_err_msg):
    '''
    @args:
        1. p_european_swaption: dqproto.IrEuropeanSwaption
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildIrEuropeanSwaptionOutput
    '''
    try:
        tmp_this= BuildIrEuropeanSwaptionOutput()
        tmp_this.european_swaption.CopyFrom(p_european_swaption)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildIrCapFloorInput
def dqCreateProtoBuildIrCapFloorInput(p_type, p_strike, p_start_date, p_end_date, p_notional, p_inst_tempalte):
    '''
    @args:
        1. p_type: dqproto.Type
        2. p_strike: double
        3. p_start_date: dqproto.Date
        4. p_end_date: dqproto.Date
        5. p_notional: dqproto.Notional
        6. p_inst_tempalte: dqproto.InterestRateInstrumentTemplate
    @return:
        dqproto.BuildIrCapFloorInput
    '''
    try:
        tmp_this= BuildIrCapFloorInput()
        tmp_this.type=p_type
        tmp_this.strike=p_strike
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.end_date.CopyFrom(p_end_date)
        tmp_this.notional.CopyFrom(p_notional)
        tmp_this.inst_tempalte.CopyFrom(p_inst_tempalte)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildIrCapFloorOutput
def dqCreateProtoBuildIrCapFloorOutput(p_ir_cap_floor):
    '''
    @args:
        1. p_ir_cap_floor: dqproto.IrCapFloor
    @return:
        dqproto.BuildIrCapFloorOutput
    '''
    try:
        tmp_this= BuildIrCapFloorOutput()
        tmp_this.ir_cap_floor.CopyFrom(p_ir_cap_floor)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#DqlibRequest
def dqCreateProtoDqlibRequest(p_name, p_serialized_request):
    '''
    @args:
        1. p_name: string
        2. p_serialized_request: bytes
    @return:
        dqproto.DqlibRequest
    '''
    try:
        tmp_this= DqlibRequest()
        tmp_this.name=p_name
        tmp_this.serialized_request=p_serialized_request
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#DqlibResponse
def dqCreateProtoDqlibResponse(p_serialized_response):
    '''
    @args:
        1. p_serialized_response: bytes
    @return:
        dqproto.DqlibResponse
    '''
    try:
        tmp_this= DqlibResponse()
        tmp_this.serialized_response=p_serialized_response
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Notional
def dqCreateProtoNotional(p_currency, p_amount):
    '''
    @args:
        1. p_currency: string
        2. p_amount: double
    @return:
        dqproto.Notional
    '''
    try:
        tmp_this= Notional()
        tmp_this.currency=p_currency
        tmp_this.amount=p_amount
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Barrier
def dqCreateProtoBarrier(p_barrier_type, p_value):
    '''
    @args:
        1. p_barrier_type: dqproto.BarrierType
        2. p_value: double
    @return:
        dqproto.Barrier
    '''
    try:
        tmp_this= Barrier()
        tmp_this.barrier_type=p_barrier_type
        tmp_this.value=p_value
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Price
def dqCreateProtoPrice(p_amount, p_currency):
    '''
    @args:
        1. p_amount: double
        2. p_currency: string
    @return:
        dqproto.Price
    '''
    try:
        tmp_this= Price()
        tmp_this.amount=p_amount
        tmp_this.currency=p_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Currency
def dqCreateProtoCurrency(p_name):
    '''
    @args:
        1. p_name: string
    @return:
        dqproto.Currency
    '''
    try:
        tmp_this= Currency()
        tmp_this.name=p_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CurrencyList
def dqCreateProtoCurrencyList(p_currency):
    '''
    @args:
        1. p_currency: dqproto.Currency
    @return:
        dqproto.CurrencyList
    '''
    try:
        tmp_this= CurrencyList()
        tmp_this.currency.extend(p_currency)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CurrencyPair
def dqCreateProtoCurrencyPair(p_left_currency, p_right_currency):
    '''
    @args:
        1. p_left_currency: dqproto.Currency
        2. p_right_currency: dqproto.Currency
    @return:
        dqproto.CurrencyPair
    '''
    try:
        tmp_this= CurrencyPair()
        tmp_this.left_currency.CopyFrom(p_left_currency)
        tmp_this.right_currency.CopyFrom(p_right_currency)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ForeignExchangeRate
def dqCreateProtoForeignExchangeRate(p_value, p_base_currency, p_target_currency):
    '''
    @args:
        1. p_value: double
        2. p_base_currency: string
        3. p_target_currency: string
    @return:
        dqproto.ForeignExchangeRate
    '''
    try:
        tmp_this= ForeignExchangeRate()
        tmp_this.value=p_value
        tmp_this.base_currency=p_base_currency
        tmp_this.target_currency=p_target_currency
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FxSpotRate
def dqCreateProtoFxSpotRate(p_fx_rate, p_ref_date, p_spot_date):
    '''
    @args:
        1. p_fx_rate: dqproto.ForeignExchangeRate
        2. p_ref_date: dqproto.Date
        3. p_spot_date: dqproto.Date
    @return:
        dqproto.FxSpotRate
    '''
    try:
        tmp_this= FxSpotRate()
        tmp_this.fx_rate.CopyFrom(p_fx_rate)
        tmp_this.ref_date.CopyFrom(p_ref_date)
        tmp_this.spot_date.CopyFrom(p_spot_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FixingSchedule.Row
def dqCreateProtoFixingSchedule_Row(p_fixing_date, p_fixing_value, p_fixing_weight):
    '''
    @args:
        1. p_fixing_date: dqproto.Date
        2. p_fixing_value: double
        3. p_fixing_weight: double
    @return:
        dqproto.FixingSchedule.Row
    '''
    try:
        tmp_this= FixingSchedule.Row()
        tmp_this.fixing_date.CopyFrom(p_fixing_date)
        tmp_this.fixing_value=p_fixing_value
        tmp_this.fixing_weight=p_fixing_weight
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FixingSchedule
def dqCreateProtoFixingSchedule(p_data):
    '''
    @args:
        1. p_data: dqproto.FixingSchedule.Row
    @return:
        dqproto.FixingSchedule
    '''
    try:
        tmp_this= FixingSchedule()
        tmp_this.data.extend(p_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculationSchedule.Row
def dqCreateProtoCalculationSchedule_Row(p_calc_date, p_fixing_schdules):
    '''
    @args:
        1. p_calc_date: dqproto.Date
        2. p_fixing_schdules: dqproto.FixingSchedule
    @return:
        dqproto.CalculationSchedule.Row
    '''
    try:
        tmp_this= CalculationSchedule.Row()
        tmp_this.calc_date.CopyFrom(p_calc_date)
        tmp_this.fixing_schdules.extend(p_fixing_schdules)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculationSchedule
def dqCreateProtoCalculationSchedule(p_obs_type, p_data):
    '''
    @args:
        1. p_obs_type: dqproto.EventObservationType
        2. p_data: dqproto.CalculationSchedule.Row
    @return:
        dqproto.CalculationSchedule
    '''
    try:
        tmp_this= CalculationSchedule()
        tmp_this.obs_type=p_obs_type
        tmp_this.data.extend(p_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#AutoExerciseSchedule.Row
def dqCreateProtoAutoExerciseSchedule_Row(p_lower_barrier, p_upper_barrier, p_fixing_schedule):
    '''
    @args:
        1. p_lower_barrier: dqproto.Barrier
        2. p_upper_barrier: dqproto.Barrier
        3. p_fixing_schedule: dqproto.FixingSchedule
    @return:
        dqproto.AutoExerciseSchedule.Row
    '''
    try:
        tmp_this= AutoExerciseSchedule.Row()
        tmp_this.lower_barrier.CopyFrom(p_lower_barrier)
        tmp_this.upper_barrier.CopyFrom(p_upper_barrier)
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#AutoExerciseSchedule
def dqCreateProtoAutoExerciseSchedule(p_obs_type, p_data):
    '''
    @args:
        1. p_obs_type: dqproto.EventObservationType
        2. p_data: dqproto.AutoExerciseSchedule.Row
    @return:
        dqproto.AutoExerciseSchedule
    '''
    try:
        tmp_this= AutoExerciseSchedule()
        tmp_this.obs_type=p_obs_type
        tmp_this.data.extend(p_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ExerciseSchedule.Row
def dqCreateProtoExerciseSchedule_Row(p_exercise_date, p_settlement_date, p_fee, p_fee_type):
    '''
    @args:
        1. p_exercise_date: dqproto.Date
        2. p_settlement_date: dqproto.Date
        3. p_fee: double
        4. p_fee_type: dqproto.ExerciseFeeType
    @return:
        dqproto.ExerciseSchedule.Row
    '''
    try:
        tmp_this= ExerciseSchedule.Row()
        tmp_this.exercise_date.CopyFrom(p_exercise_date)
        tmp_this.settlement_date.CopyFrom(p_settlement_date)
        tmp_this.fee=p_fee
        tmp_this.fee_type=p_fee_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ExerciseSchedule
def dqCreateProtoExerciseSchedule(p_data):
    '''
    @args:
        1. p_data: dqproto.ExerciseSchedule.Row
    @return:
        dqproto.ExerciseSchedule
    '''
    try:
        tmp_this= ExerciseSchedule()
        tmp_this.data.extend(p_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#TimeSeries
def dqCreateProtoTimeSeries(p_keys, p_values, p_mode, p_name):
    '''
    @args:
        1. p_keys: dqproto.Date
        2. p_values: dqproto.Matrix
        3. p_mode: dqproto.Mode
        4. p_name: string
    @return:
        dqproto.TimeSeries
    '''
    try:
        tmp_this= TimeSeries()
        tmp_this.keys.extend(p_keys)
        tmp_this.values.CopyFrom(p_values)
        tmp_this.mode=p_mode
        tmp_this.name=p_name
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Payoff
def dqCreateProtoPayoff(p_calculation_schedule, p_payment_type):
    '''
    @args:
        1. p_calculation_schedule: dqproto.CalculationSchedule
        2. p_payment_type: dqproto.PaymentType
    @return:
        dqproto.Payoff
    '''
    try:
        tmp_this= Payoff()
        tmp_this.calculation_schedule.CopyFrom(p_calculation_schedule)
        tmp_this.payment_type=p_payment_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#VanillaPayoff
def dqCreateProtoVanillaPayoff(p_payoff_type, p_strike, p_fixing_date, p_gearing, p_performance_type):
    '''
    @args:
        1. p_payoff_type: dqproto.PayoffType
        2. p_strike: double
        3. p_fixing_date: dqproto.Date
        4. p_gearing: double
        5. p_performance_type: dqproto.PerformanceType
    @return:
        dqproto.VanillaPayoff
    '''
    try:
        tmp_this= VanillaPayoff()
        tmp_this.payoff_type=p_payoff_type
        tmp_this.strike=p_strike
        tmp_this.fixing_date.CopyFrom(p_fixing_date)
        tmp_this.gearing=p_gearing
        tmp_this.performance_type=p_performance_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#FinancialInstrument
def dqCreateProtoFinancialInstrument(p_instrument_type, p_assets, p_nominal, p_exercise_type, p_exercise_schedule):
    '''
    @args:
        1. p_instrument_type: string
        2. p_assets: string
        3. p_nominal: double
        4. p_exercise_type: dqproto.ExerciseType
        5. p_exercise_schedule: dqproto.ExerciseSchedule
    @return:
        dqproto.FinancialInstrument
    '''
    try:
        tmp_this= FinancialInstrument()
        tmp_this.instrument_type=p_instrument_type
        tmp_this.assets.extend(p_assets)
        tmp_this.nominal=p_nominal
        tmp_this.exercise_type=p_exercise_type
        tmp_this.exercise_schedule.CopyFrom(p_exercise_schedule)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#EuropeanOption
def dqCreateProtoEuropeanOption(p_payoff_type, p_strike, p_delivery, p_expiry, p_nominal, p_underlying, p_underlying_currency, p_payoff_currency, p_underlying_type):
    '''
    @args:
        1. p_payoff_type: dqproto.PayoffType
        2. p_strike: double
        3. p_delivery: dqproto.Date
        4. p_expiry: dqproto.Date
        5. p_nominal: double
        6. p_underlying: string
        7. p_underlying_currency: string
        8. p_payoff_currency: string
        9. p_underlying_type: dqproto.InstrumentType
    @return:
        dqproto.EuropeanOption
    '''
    try:
        tmp_this= EuropeanOption()
        tmp_this.payoff_type=p_payoff_type
        tmp_this.strike=p_strike
        tmp_this.delivery.CopyFrom(p_delivery)
        tmp_this.expiry.CopyFrom(p_expiry)
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#AmericanOption
def dqCreateProtoAmericanOption(p_payoff_type, p_strike, p_expiry_date, p_delivery_date, p_settlement_days, p_nominal, p_underlying, p_underlying_currency, p_payoff_currency, p_underlying_type):
    '''
    @args:
        1. p_payoff_type: dqproto.PayoffType
        2. p_strike: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_settlement_days: int32
        6. p_nominal: double
        7. p_underlying: string
        8. p_underlying_currency: string
        9. p_payoff_currency: string
        10. p_underlying_type: dqproto.InstrumentType
    @return:
        dqproto.AmericanOption
    '''
    try:
        tmp_this= AmericanOption()
        tmp_this.payoff_type=p_payoff_type
        tmp_this.strike=p_strike
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.settlement_days=p_settlement_days
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#DigitalOption
def dqCreateProtoDigitalOption(p_payoff_type, p_expiry_date, p_delivery_date, p_strike, p_asset, p_cash, p_nominal, p_underlying, p_underlying_currency, p_payoff_currency, p_underlying_type):
    '''
    @args:
        1. p_payoff_type: dqproto.PayoffType
        2. p_expiry_date: dqproto.Date
        3. p_delivery_date: dqproto.Date
        4. p_strike: double
        5. p_asset: double
        6. p_cash: double
        7. p_nominal: double
        8. p_underlying: string
        9. p_underlying_currency: string
        10. p_payoff_currency: string
        11. p_underlying_type: dqproto.InstrumentType
    @return:
        dqproto.DigitalOption
    '''
    try:
        tmp_this= DigitalOption()
        tmp_this.payoff_type=p_payoff_type
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.strike=p_strike
        tmp_this.asset=p_asset
        tmp_this.cash=p_cash
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#AsianOption
def dqCreateProtoAsianOption(p_payoff_type, p_avg_method, p_obs_type, p_expiry_date, p_delivery_date, p_fixing_schedule, p_strike_type, p_strike, p_nominal, p_underlying, p_underlying_currency, p_payoff_currency, p_underlying_type):
    '''
    @args:
        1. p_payoff_type: dqproto.PayoffType
        2. p_avg_method: dqproto.AveragingMethod
        3. p_obs_type: dqproto.EventObservationType
        4. p_expiry_date: dqproto.Date
        5. p_delivery_date: dqproto.Date
        6. p_fixing_schedule: dqproto.FixingSchedule
        7. p_strike_type: dqproto.StrikeType
        8. p_strike: double
        9. p_nominal: double
        10. p_underlying: string
        11. p_underlying_currency: string
        12. p_payoff_currency: string
        13. p_underlying_type: dqproto.InstrumentType
    @return:
        dqproto.AsianOption
    '''
    try:
        tmp_this= AsianOption()
        tmp_this.payoff_type=p_payoff_type
        tmp_this.avg_method=p_avg_method
        tmp_this.obs_type=p_obs_type
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.strike_type=p_strike_type
        tmp_this.strike=p_strike
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#OneTouchOption
def dqCreateProtoOneTouchOption(p_asset, p_cash, p_expiry_date, p_delivery_date, p_barrier, p_payment_type, p_nominal, p_underlying, p_settlement_days, p_obs_type, p_fixing_schedule, p_underlying_currency, p_payoff_currency, p_underlying_type):
    '''
    @args:
        1. p_asset: double
        2. p_cash: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_barrier: dqproto.Barrier
        6. p_payment_type: dqproto.PaymentType
        7. p_nominal: double
        8. p_underlying: string
        9. p_settlement_days: int32
        10. p_obs_type: dqproto.EventObservationType
        11. p_fixing_schedule: dqproto.FixingSchedule
        12. p_underlying_currency: string
        13. p_payoff_currency: string
        14. p_underlying_type: dqproto.InstrumentType
    @return:
        dqproto.OneTouchOption
    '''
    try:
        tmp_this= OneTouchOption()
        tmp_this.asset=p_asset
        tmp_this.cash=p_cash
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.barrier.CopyFrom(p_barrier)
        tmp_this.payment_type=p_payment_type
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.settlement_days=p_settlement_days
        tmp_this.obs_type=p_obs_type
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#DoubleTouchOption
def dqCreateProtoDoubleTouchOption(p_asset, p_cash, p_expiry_date, p_delivery_date, p_lower_barrier, p_upper_barrier, p_payment_type, p_nominal, p_underlying, p_settlement_days, p_obs_type, p_fixing_schedule, p_underlying_currency, p_payoff_currency, p_underlying_type):
    '''
    @args:
        1. p_asset: double
        2. p_cash: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_lower_barrier: dqproto.Barrier
        6. p_upper_barrier: dqproto.Barrier
        7. p_payment_type: dqproto.PaymentType
        8. p_nominal: double
        9. p_underlying: string
        10. p_settlement_days: int32
        11. p_obs_type: dqproto.EventObservationType
        12. p_fixing_schedule: dqproto.FixingSchedule
        13. p_underlying_currency: string
        14. p_payoff_currency: string
        15. p_underlying_type: dqproto.InstrumentType
    @return:
        dqproto.DoubleTouchOption
    '''
    try:
        tmp_this= DoubleTouchOption()
        tmp_this.asset=p_asset
        tmp_this.cash=p_cash
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.lower_barrier.CopyFrom(p_lower_barrier)
        tmp_this.upper_barrier.CopyFrom(p_upper_barrier)
        tmp_this.payment_type=p_payment_type
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.settlement_days=p_settlement_days
        tmp_this.obs_type=p_obs_type
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#SingleBarrierOption
def dqCreateProtoSingleBarrierOption(p_payoff_type, p_strike, p_expiry_date, p_delivery_date, p_barrier, p_payment_type, p_cash_rebate, p_asset_rebate, p_nominal, p_underlying, p_settlement_days, p_obs_type, p_fixing_schedule, p_underlying_currency, p_payoff_currency, p_underlying_type):
    '''
    @args:
        1. p_payoff_type: dqproto.PayoffType
        2. p_strike: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_barrier: dqproto.Barrier
        6. p_payment_type: dqproto.PaymentType
        7. p_cash_rebate: double
        8. p_asset_rebate: double
        9. p_nominal: double
        10. p_underlying: string
        11. p_settlement_days: int32
        12. p_obs_type: dqproto.EventObservationType
        13. p_fixing_schedule: dqproto.FixingSchedule
        14. p_underlying_currency: string
        15. p_payoff_currency: string
        16. p_underlying_type: dqproto.InstrumentType
    @return:
        dqproto.SingleBarrierOption
    '''
    try:
        tmp_this= SingleBarrierOption()
        tmp_this.payoff_type=p_payoff_type
        tmp_this.strike=p_strike
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.barrier.CopyFrom(p_barrier)
        tmp_this.payment_type=p_payment_type
        tmp_this.cash_rebate=p_cash_rebate
        tmp_this.asset_rebate=p_asset_rebate
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.settlement_days=p_settlement_days
        tmp_this.obs_type=p_obs_type
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#DoubleBarrierOption
def dqCreateProtoDoubleBarrierOption(p_payoff_type, p_strike, p_expiry_date, p_delivery_date, p_lower_barrier, p_upper_barrier, p_payment_type, p_lower_cash_rebate, p_lower_asset_rebate, p_upper_cash_rebate, p_upper_asset_rebate, p_nominal, p_underlying, p_settlement_days, p_obs_type, p_fixing_schedule, p_underlying_currency, p_payoff_currency, p_underlying_type):
    '''
    @args:
        1. p_payoff_type: dqproto.PayoffType
        2. p_strike: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_lower_barrier: dqproto.Barrier
        6. p_upper_barrier: dqproto.Barrier
        7. p_payment_type: dqproto.PaymentType
        8. p_lower_cash_rebate: double
        9. p_lower_asset_rebate: double
        10. p_upper_cash_rebate: double
        11. p_upper_asset_rebate: double
        12. p_nominal: double
        13. p_underlying: string
        14. p_settlement_days: int32
        15. p_obs_type: dqproto.EventObservationType
        16. p_fixing_schedule: dqproto.FixingSchedule
        17. p_underlying_currency: string
        18. p_payoff_currency: string
        19. p_underlying_type: dqproto.InstrumentType
    @return:
        dqproto.DoubleBarrierOption
    '''
    try:
        tmp_this= DoubleBarrierOption()
        tmp_this.payoff_type=p_payoff_type
        tmp_this.strike=p_strike
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.lower_barrier.CopyFrom(p_lower_barrier)
        tmp_this.upper_barrier.CopyFrom(p_upper_barrier)
        tmp_this.payment_type=p_payment_type
        tmp_this.lower_cash_rebate=p_lower_cash_rebate
        tmp_this.lower_asset_rebate=p_lower_asset_rebate
        tmp_this.upper_cash_rebate=p_upper_cash_rebate
        tmp_this.upper_asset_rebate=p_upper_asset_rebate
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.settlement_days=p_settlement_days
        tmp_this.obs_type=p_obs_type
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#AirbagOption
def dqCreateProtoAirbagOption(p_payoff_type, p_knock_in_strike, p_barrier_obs_type, p_barrier, p_lower_gearing, p_upper_gearing, p_lower_strike, p_upper_strike, p_fixing_schedule, p_expiry_date, p_delivery_date, p_nominal, p_underlying, p_underlying_currency, p_payoff_currency, p_underlying_type):
    '''
    @args:
        1. p_payoff_type: dqproto.PayoffType
        2. p_knock_in_strike: double
        3. p_barrier_obs_type: dqproto.EventObservationType
        4. p_barrier: dqproto.Barrier
        5. p_lower_gearing: double
        6. p_upper_gearing: double
        7. p_lower_strike: double
        8. p_upper_strike: double
        9. p_fixing_schedule: dqproto.FixingSchedule
        10. p_expiry_date: dqproto.Date
        11. p_delivery_date: dqproto.Date
        12. p_nominal: double
        13. p_underlying: string
        14. p_underlying_currency: string
        15. p_payoff_currency: string
        16. p_underlying_type: dqproto.InstrumentType
    @return:
        dqproto.AirbagOption
    '''
    try:
        tmp_this= AirbagOption()
        tmp_this.payoff_type=p_payoff_type
        tmp_this.knock_in_strike=p_knock_in_strike
        tmp_this.barrier_obs_type=p_barrier_obs_type
        tmp_this.barrier.CopyFrom(p_barrier)
        tmp_this.lower_gearing=p_lower_gearing
        tmp_this.upper_gearing=p_upper_gearing
        tmp_this.lower_strike=p_lower_strike
        tmp_this.upper_strike=p_upper_strike
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CollarOption
def dqCreateProtoCollarOption(p_payoff_type, p_lower_gearing, p_upper_gearing, p_lower_strike, p_upper_strike, p_expiry_date, p_delivery_date, p_nominal, p_underlying, p_underlying_currency, p_payoff_currency, p_underlying_type):
    '''
    @args:
        1. p_payoff_type: dqproto.PayoffType
        2. p_lower_gearing: double
        3. p_upper_gearing: double
        4. p_lower_strike: double
        5. p_upper_strike: double
        6. p_expiry_date: dqproto.Date
        7. p_delivery_date: dqproto.Date
        8. p_nominal: double
        9. p_underlying: string
        10. p_underlying_currency: string
        11. p_payoff_currency: string
        12. p_underlying_type: dqproto.InstrumentType
    @return:
        dqproto.CollarOption
    '''
    try:
        tmp_this= CollarOption()
        tmp_this.payoff_type=p_payoff_type
        tmp_this.lower_gearing=p_lower_gearing
        tmp_this.upper_gearing=p_upper_gearing
        tmp_this.lower_strike=p_lower_strike
        tmp_this.upper_strike=p_upper_strike
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#SingleSharkFinOption
def dqCreateProtoSingleSharkFinOption(p_payoff_type, p_strike, p_expiry_date, p_delivery_date, p_gearing, p_performance_type, p_barrier_obs_type, p_barrier, p_cash_rebate, p_asset_rebate, p_fixing_schedule, p_nominal, p_underlying, p_underlying_currency, p_payoff_currency, p_underlying_type, p_settlement_days, p_payment_type):
    '''
    @args:
        1. p_payoff_type: dqproto.PayoffType
        2. p_strike: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_gearing: double
        6. p_performance_type: dqproto.PerformanceType
        7. p_barrier_obs_type: dqproto.EventObservationType
        8. p_barrier: dqproto.Barrier
        9. p_cash_rebate: double
        10. p_asset_rebate: double
        11. p_fixing_schedule: dqproto.FixingSchedule
        12. p_nominal: double
        13. p_underlying: string
        14. p_underlying_currency: string
        15. p_payoff_currency: string
        16. p_underlying_type: dqproto.InstrumentType
        17. p_settlement_days: int32
        18. p_payment_type: dqproto.PaymentType
    @return:
        dqproto.SingleSharkFinOption
    '''
    try:
        tmp_this= SingleSharkFinOption()
        tmp_this.payoff_type=p_payoff_type
        tmp_this.strike=p_strike
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.gearing=p_gearing
        tmp_this.performance_type=p_performance_type
        tmp_this.barrier_obs_type=p_barrier_obs_type
        tmp_this.barrier.CopyFrom(p_barrier)
        tmp_this.cash_rebate=p_cash_rebate
        tmp_this.asset_rebate=p_asset_rebate
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        tmp_this.settlement_days=p_settlement_days
        tmp_this.payment_type=p_payment_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#DoubleSharkFinOption
def dqCreateProtoDoubleSharkFinOption(p_lower_strike, p_upper_strike, p_expiry_date, p_delivery_date, p_lower_participation, p_upper_participation, p_barrier_obs_type, p_lower_barrier, p_upper_barrier, p_lower_cash_rebate, p_lower_asset_rebate, p_upper_cash_rebate, p_upper_asset_rebate, p_fixing_schedule, p_nominal, p_underlying, p_underlying_currency, p_payoff_currency, p_underlying_type, p_settlement_days, p_payment_type, p_performance_type):
    '''
    @args:
        1. p_lower_strike: double
        2. p_upper_strike: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_lower_participation: double
        6. p_upper_participation: double
        7. p_barrier_obs_type: dqproto.EventObservationType
        8. p_lower_barrier: double
        9. p_upper_barrier: double
        10. p_lower_cash_rebate: double
        11. p_lower_asset_rebate: double
        12. p_upper_cash_rebate: double
        13. p_upper_asset_rebate: double
        14. p_fixing_schedule: dqproto.FixingSchedule
        15. p_nominal: double
        16. p_underlying: string
        17. p_underlying_currency: string
        18. p_payoff_currency: string
        19. p_underlying_type: dqproto.InstrumentType
        20. p_settlement_days: int32
        21. p_payment_type: dqproto.PaymentType
        22. p_performance_type: dqproto.PerformanceType
    @return:
        dqproto.DoubleSharkFinOption
    '''
    try:
        tmp_this= DoubleSharkFinOption()
        tmp_this.lower_strike=p_lower_strike
        tmp_this.upper_strike=p_upper_strike
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.lower_participation=p_lower_participation
        tmp_this.upper_participation=p_upper_participation
        tmp_this.barrier_obs_type=p_barrier_obs_type
        tmp_this.lower_barrier=p_lower_barrier
        tmp_this.upper_barrier=p_upper_barrier
        tmp_this.lower_cash_rebate=p_lower_cash_rebate
        tmp_this.lower_asset_rebate=p_lower_asset_rebate
        tmp_this.upper_cash_rebate=p_upper_cash_rebate
        tmp_this.upper_asset_rebate=p_upper_asset_rebate
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        tmp_this.settlement_days=p_settlement_days
        tmp_this.payment_type=p_payment_type
        tmp_this.performance_type=p_performance_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PingPongOption
def dqCreateProtoPingPongOption(p_asset, p_cash, p_expiry_date, p_delivery_date, p_lower_barrier, p_upper_barrier, p_obs_type, p_fixing_schedule, p_payment_type, p_settlement_days, p_nominal, p_underlying, p_underlying_currency, p_payoff_currency, p_underlying_type):
    '''
    @args:
        1. p_asset: double
        2. p_cash: double
        3. p_expiry_date: dqproto.Date
        4. p_delivery_date: dqproto.Date
        5. p_lower_barrier: dqproto.Barrier
        6. p_upper_barrier: dqproto.Barrier
        7. p_obs_type: dqproto.EventObservationType
        8. p_fixing_schedule: dqproto.FixingSchedule
        9. p_payment_type: dqproto.PaymentType
        10. p_settlement_days: int32
        11. p_nominal: double
        12. p_underlying: string
        13. p_underlying_currency: string
        14. p_payoff_currency: string
        15. p_underlying_type: dqproto.InstrumentType
    @return:
        dqproto.PingPongOption
    '''
    try:
        tmp_this= PingPongOption()
        tmp_this.asset=p_asset
        tmp_this.cash=p_cash
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.lower_barrier.CopyFrom(p_lower_barrier)
        tmp_this.upper_barrier.CopyFrom(p_upper_barrier)
        tmp_this.obs_type=p_obs_type
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.payment_type=p_payment_type
        tmp_this.settlement_days=p_settlement_days
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#RangeAccrualOption
def dqCreateProtoRangeAccrualOption(p_expiry_date, p_delivery_date, p_asset, p_cash, p_lower_barrier, p_upper_barrier, p_fixing_schedule, p_nominal, p_underlying, p_underlying_currency, p_payoff_currency, p_underlying_type):
    '''
    @args:
        1. p_expiry_date: dqproto.Date
        2. p_delivery_date: dqproto.Date
        3. p_asset: double
        4. p_cash: double
        5. p_lower_barrier: double
        6. p_upper_barrier: double
        7. p_fixing_schedule: dqproto.FixingSchedule
        8. p_nominal: double
        9. p_underlying: string
        10. p_underlying_currency: string
        11. p_payoff_currency: string
        12. p_underlying_type: dqproto.InstrumentType
    @return:
        dqproto.RangeAccrualOption
    '''
    try:
        tmp_this= RangeAccrualOption()
        tmp_this.expiry_date.CopyFrom(p_expiry_date)
        tmp_this.delivery_date.CopyFrom(p_delivery_date)
        tmp_this.asset=p_asset
        tmp_this.cash=p_cash
        tmp_this.lower_barrier=p_lower_barrier
        tmp_this.upper_barrier=p_upper_barrier
        tmp_this.fixing_schedule.CopyFrom(p_fixing_schedule)
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#PhoenixAutoCallableNote
def dqCreateProtoPhoenixAutoCallableNote(p_coupon_payoff_type, p_coupon_strike, p_coupon_rate, p_start_date, p_coupon_dates, p_knock_out_barrier, p_knock_out_sched, p_knock_in_barrier, p_knock_in_sched, p_long_short, p_knock_in_payoff_type, p_knock_in_payoff_strike, p_expiry, p_delivery, p_nominal, p_underlying, p_settlement_days, p_underlying_currency, p_payoff_currency, p_underlying_type, p_day_count):
    '''
    @args:
        1. p_coupon_payoff_type: dqproto.PayoffType
        2. p_coupon_strike: double
        3. p_coupon_rate: double
        4. p_start_date: dqproto.Date
        5. p_coupon_dates: dqproto.Date
        6. p_knock_out_barrier: dqproto.Barrier
        7. p_knock_out_sched: dqproto.FixingSchedule
        8. p_knock_in_barrier: dqproto.Barrier
        9. p_knock_in_sched: dqproto.FixingSchedule
        10. p_long_short: dqproto.BuySellFlag
        11. p_knock_in_payoff_type: dqproto.PayoffType
        12. p_knock_in_payoff_strike: double
        13. p_expiry: dqproto.Date
        14. p_delivery: dqproto.Date
        15. p_nominal: double
        16. p_underlying: string
        17. p_settlement_days: int32
        18. p_underlying_currency: string
        19. p_payoff_currency: string
        20. p_underlying_type: dqproto.InstrumentType
        21. p_day_count: dqproto.DayCountConvention
    @return:
        dqproto.PhoenixAutoCallableNote
    '''
    try:
        tmp_this= PhoenixAutoCallableNote()
        tmp_this.coupon_payoff_type=p_coupon_payoff_type
        tmp_this.coupon_strike=p_coupon_strike
        tmp_this.coupon_rate=p_coupon_rate
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.coupon_dates.extend(p_coupon_dates)
        tmp_this.knock_out_barrier.CopyFrom(p_knock_out_barrier)
        tmp_this.knock_out_sched.CopyFrom(p_knock_out_sched)
        tmp_this.knock_in_barrier.CopyFrom(p_knock_in_barrier)
        tmp_this.knock_in_sched.CopyFrom(p_knock_in_sched)
        tmp_this.long_short=p_long_short
        tmp_this.knock_in_payoff_type=p_knock_in_payoff_type
        tmp_this.knock_in_payoff_strike=p_knock_in_payoff_strike
        tmp_this.expiry.CopyFrom(p_expiry)
        tmp_this.delivery.CopyFrom(p_delivery)
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.settlement_days=p_settlement_days
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        tmp_this.day_count=p_day_count
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#SnowballAutoCallableNote
def dqCreateProtoSnowballAutoCallableNote(p_coupon_rate, p_start_date, p_coupon_dates, p_knock_out_barrier, p_knock_out_sched, p_knock_in_barrier, p_knock_in_sched, p_long_short, p_knock_in_payoff_type, p_knock_in_payoff_strike, p_expiry, p_delivery, p_nominal, p_underlying, p_knock_in_payoff_gearing, p_reference_price, p_day_count, p_settlement_days, p_underlying_currency, p_payoff_currency, p_underlying_type):
    '''
    @args:
        1. p_coupon_rate: double
        2. p_start_date: dqproto.Date
        3. p_coupon_dates: dqproto.Date
        4. p_knock_out_barrier: dqproto.Barrier
        5. p_knock_out_sched: dqproto.FixingSchedule
        6. p_knock_in_barrier: dqproto.Barrier
        7. p_knock_in_sched: dqproto.FixingSchedule
        8. p_long_short: dqproto.BuySellFlag
        9. p_knock_in_payoff_type: dqproto.PayoffType
        10. p_knock_in_payoff_strike: double
        11. p_expiry: dqproto.Date
        12. p_delivery: dqproto.Date
        13. p_nominal: double
        14. p_underlying: string
        15. p_knock_in_payoff_gearing: double
        16. p_reference_price: double
        17. p_day_count: dqproto.DayCountConvention
        18. p_settlement_days: int32
        19. p_underlying_currency: string
        20. p_payoff_currency: string
        21. p_underlying_type: dqproto.InstrumentType
    @return:
        dqproto.SnowballAutoCallableNote
    '''
    try:
        tmp_this= SnowballAutoCallableNote()
        tmp_this.coupon_rate=p_coupon_rate
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.coupon_dates.extend(p_coupon_dates)
        tmp_this.knock_out_barrier.CopyFrom(p_knock_out_barrier)
        tmp_this.knock_out_sched.CopyFrom(p_knock_out_sched)
        tmp_this.knock_in_barrier.CopyFrom(p_knock_in_barrier)
        tmp_this.knock_in_sched.CopyFrom(p_knock_in_sched)
        tmp_this.long_short=p_long_short
        tmp_this.knock_in_payoff_type=p_knock_in_payoff_type
        tmp_this.knock_in_payoff_strike=p_knock_in_payoff_strike
        tmp_this.expiry.CopyFrom(p_expiry)
        tmp_this.delivery.CopyFrom(p_delivery)
        tmp_this.nominal=p_nominal
        tmp_this.underlying=p_underlying
        tmp_this.knock_in_payoff_gearing=p_knock_in_payoff_gearing
        tmp_this.reference_price=p_reference_price
        tmp_this.day_count=p_day_count
        tmp_this.settlement_days=p_settlement_days
        tmp_this.underlying_currency=p_underlying_currency
        tmp_this.payoff_currency=p_payoff_currency
        tmp_this.underlying_type=p_underlying_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#HsScnGenSettings
def dqCreateProtoHsScnGenSettings(p_risk_factor_change_type, p_change_period, p_num_scenarios, p_ewma_decay_factor, p_smoothing_weight, p_zero_return_handling, p_vol_floor, p_vol_cap):
    '''
    @args:
        1. p_risk_factor_change_type: dqproto.RiskFactorChangeType
        2. p_change_period: dqproto.Period
        3. p_num_scenarios: int32
        4. p_ewma_decay_factor: double
        5. p_smoothing_weight: double
        6. p_zero_return_handling: dqproto.ZeroReturnHandlingMethod
        7. p_vol_floor: double
        8. p_vol_cap: double
    @return:
        dqproto.HsScnGenSettings
    '''
    try:
        tmp_this= HsScnGenSettings()
        tmp_this.risk_factor_change_type=p_risk_factor_change_type
        tmp_this.change_period.CopyFrom(p_change_period)
        tmp_this.num_scenarios=p_num_scenarios
        tmp_this.ewma_decay_factor=p_ewma_decay_factor
        tmp_this.smoothing_weight=p_smoothing_weight
        tmp_this.zero_return_handling=p_zero_return_handling
        tmp_this.vol_floor=p_vol_floor
        tmp_this.vol_cap=p_vol_cap
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InitialMarginCalculationSettings
def dqCreateProtoInitialMarginCalculationSettings(p_im_type, p_fhs_probability, p_stressed_probability, p_stressed_risk_contribution, p_margin_floor_rate, p_fhs_risk_measure_type, p_stress_risk_measure_type, p_calc_mirrored_im, p_num_days_for_return, p_volatility_multiplier, p_margin_floor, p_liquidity_risk_buffer, p_benchmark_indices, p_round_up_value):
    '''
    @args:
        1. p_im_type: dqproto.InitialMarginType
        2. p_fhs_probability: double
        3. p_stressed_probability: double
        4. p_stressed_risk_contribution: double
        5. p_margin_floor_rate: double
        6. p_fhs_risk_measure_type: dqproto.MarketRiskMeasure
        7. p_stress_risk_measure_type: dqproto.MarketRiskMeasure
        8. p_calc_mirrored_im: bool
        9. p_num_days_for_return: int32
        10. p_volatility_multiplier: double
        11. p_margin_floor: double
        12. p_liquidity_risk_buffer: double
        13. p_benchmark_indices: string
        14. p_round_up_value: int32
    @return:
        dqproto.InitialMarginCalculationSettings
    '''
    try:
        tmp_this= InitialMarginCalculationSettings()
        tmp_this.im_type=p_im_type
        tmp_this.fhs_probability=p_fhs_probability
        tmp_this.stressed_probability=p_stressed_probability
        tmp_this.stressed_risk_contribution=p_stressed_risk_contribution
        tmp_this.margin_floor_rate=p_margin_floor_rate
        tmp_this.fhs_risk_measure_type=p_fhs_risk_measure_type
        tmp_this.stress_risk_measure_type=p_stress_risk_measure_type
        tmp_this.calc_mirrored_im=p_calc_mirrored_im
        tmp_this.num_days_for_return=p_num_days_for_return
        tmp_this.volatility_multiplier=p_volatility_multiplier
        tmp_this.margin_floor=p_margin_floor
        tmp_this.liquidity_risk_buffer=p_liquidity_risk_buffer
        tmp_this.benchmark_indices.extend(p_benchmark_indices)
        tmp_this.round_up_value=p_round_up_value
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InitialMarginSettings
def dqCreateProtoInitialMarginSettings(p_tier_p_im_settings, p_tier_n_im_settings, p_round_up_value, p_save_pnl_data):
    '''
    @args:
        1. p_tier_p_im_settings: dqproto.TierPInitialMarginSettings
        2. p_tier_n_im_settings: dqproto.TierNInitialMarginSettings
        3. p_round_up_value: int32
        4. p_save_pnl_data: bool
    @return:
        dqproto.InitialMarginSettings
    '''
    try:
        tmp_this= InitialMarginSettings()
        tmp_this.tier_p_im_settings.CopyFrom(p_tier_p_im_settings)
        tmp_this.tier_n_im_settings.CopyFrom(p_tier_n_im_settings)
        tmp_this.round_up_value=p_round_up_value
        tmp_this.save_pnl_data=p_save_pnl_data
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InstrumentCleansedReturnSettings
def dqCreateProtoInstrumentCleansedReturnSettings(p_return_type, p_period, p_start_date, p_end_date, p_seed_mode, p_num_seed_days, p_seed_date, p_ewma_decay_factor, p_zero_return_method, p_use_fallback, p_fallback_indicator, p_vol_multiplier):
    '''
    @args:
        1. p_return_type: dqproto.RiskFactorChangeType
        2. p_period: dqproto.Period
        3. p_start_date: dqproto.Date
        4. p_end_date: dqproto.Date
        5. p_seed_mode: dqproto.EwmaSeedMode
        6. p_num_seed_days: int32
        7. p_seed_date: dqproto.Date
        8. p_ewma_decay_factor: double
        9. p_zero_return_method: dqproto.ZeroReturnHandlingMethod
        10. p_use_fallback: bool
        11. p_fallback_indicator: int32
        12. p_vol_multiplier: double
    @return:
        dqproto.InstrumentCleansedReturnSettings
    '''
    try:
        tmp_this= InstrumentCleansedReturnSettings()
        tmp_this.return_type=p_return_type
        tmp_this.period.CopyFrom(p_period)
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.end_date.CopyFrom(p_end_date)
        tmp_this.seed_mode=p_seed_mode
        tmp_this.num_seed_days=p_num_seed_days
        tmp_this.seed_date.CopyFrom(p_seed_date)
        tmp_this.ewma_decay_factor=p_ewma_decay_factor
        tmp_this.zero_return_method=p_zero_return_method
        tmp_this.use_fallback=p_use_fallback
        tmp_this.fallback_indicator=p_fallback_indicator
        tmp_this.vol_multiplier=p_vol_multiplier
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InstrumentReturnSettings
def dqCreateProtoInstrumentReturnSettings(p_return_type, p_period, p_start_date, p_end_date, p_seed_mode, p_num_seed_days, p_seed_date, p_ewma_decay_factors, p_zero_return_method):
    '''
    @args:
        1. p_return_type: dqproto.RiskFactorChangeType
        2. p_period: dqproto.Period
        3. p_start_date: dqproto.Date
        4. p_end_date: dqproto.Date
        5. p_seed_mode: dqproto.EwmaSeedMode
        6. p_num_seed_days: int32
        7. p_seed_date: dqproto.Date
        8. p_ewma_decay_factors: double
        9. p_zero_return_method: dqproto.ZeroReturnHandlingMethod
    @return:
        dqproto.InstrumentReturnSettings
    '''
    try:
        tmp_this= InstrumentReturnSettings()
        tmp_this.return_type=p_return_type
        tmp_this.period.CopyFrom(p_period)
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.end_date.CopyFrom(p_end_date)
        tmp_this.seed_mode=p_seed_mode
        tmp_this.num_seed_days=p_num_seed_days
        tmp_this.seed_date.CopyFrom(p_seed_date)
        tmp_this.ewma_decay_factors.extend(p_ewma_decay_factors)
        tmp_this.zero_return_method=p_zero_return_method
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#MarketRiskMeasureSettings
def dqCreateProtoMarketRiskMeasureSettings(p_risk_measure_type, p_probability, p_antithetic):
    '''
    @args:
        1. p_risk_measure_type: dqproto.MarketRiskMeasure
        2. p_probability: double
        3. p_antithetic: bool
    @return:
        dqproto.MarketRiskMeasureSettings
    '''
    try:
        tmp_this= MarketRiskMeasureSettings()
        tmp_this.risk_measure_type=p_risk_measure_type
        tmp_this.probability=p_probability
        tmp_this.antithetic=p_antithetic
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#MarketRiskReport.PnlVector
def dqCreateProtoMarketRiskReport_PnlVector(p_position_name, p_data):
    '''
    @args:
        1. p_position_name: string
        2. p_data: dqproto.Vector
    @return:
        dqproto.MarketRiskReport.PnlVector
    '''
    try:
        tmp_this= MarketRiskReport.PnlVector()
        tmp_this.position_name=p_position_name
        tmp_this.data.CopyFrom(p_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#MarketRiskReport.PnlMatrix
def dqCreateProtoMarketRiskReport_PnlMatrix(p_type, p_positions_pnl_vectors, p_portfolio_pnl_vector, p_schedule):
    '''
    @args:
        1. p_type: dqproto.InitialMarginType
        2. p_positions_pnl_vectors: dqproto.PnlVector
        3. p_portfolio_pnl_vector: dqproto.PnlVector
        4. p_schedule: dqproto.Vector
    @return:
        dqproto.MarketRiskReport.PnlMatrix
    '''
    try:
        tmp_this= MarketRiskReport.PnlMatrix()
        tmp_this.type=p_type
        tmp_this.positions_pnl_vectors.extend(p_positions_pnl_vectors)
        tmp_this.portfolio_pnl_vector.CopyFrom(p_portfolio_pnl_vector)
        tmp_this.schedule.CopyFrom(p_schedule)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#MarketRiskReport.RiskMeasures
def dqCreateProtoMarketRiskReport_RiskMeasures(p_name, p_initial_margin, p_initial_margin_mirrored, p_fhs_risk, p_fhs_risk_mirrored, p_stressed_risk, p_stressed_risk_mirrored):
    '''
    @args:
        1. p_name: string
        2. p_initial_margin: double
        3. p_initial_margin_mirrored: double
        4. p_fhs_risk: double
        5. p_fhs_risk_mirrored: double
        6. p_stressed_risk: double
        7. p_stressed_risk_mirrored: double
    @return:
        dqproto.MarketRiskReport.RiskMeasures
    '''
    try:
        tmp_this= MarketRiskReport.RiskMeasures()
        tmp_this.name=p_name
        tmp_this.initial_margin=p_initial_margin
        tmp_this.initial_margin_mirrored=p_initial_margin_mirrored
        tmp_this.fhs_risk=p_fhs_risk
        tmp_this.fhs_risk_mirrored=p_fhs_risk_mirrored
        tmp_this.stressed_risk=p_stressed_risk
        tmp_this.stressed_risk_mirrored=p_stressed_risk_mirrored
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#MarketRiskReport
def dqCreateProtoMarketRiskReport(p_type, p_batch_id, p_aod, p_portfolio_risk, p_position_risks, p_realized_pnl, p_pnl_matrices, p_portfolio_id):
    '''
    @args:
        1. p_type: dqproto.MarketRiskAnalysisType
        2. p_batch_id: string
        3. p_aod: int32
        4. p_portfolio_risk: dqproto.MarketRiskReport.RiskMeasures
        5. p_position_risks: dqproto.MarketRiskReport.RiskMeasures
        6. p_realized_pnl: double
        7. p_pnl_matrices: dqproto.MarketRiskReport.PnlMatrix
        8. p_portfolio_id: string
    @return:
        dqproto.MarketRiskReport
    '''
    try:
        tmp_this= MarketRiskReport()
        tmp_this.type=p_type
        tmp_this.batch_id=p_batch_id
        tmp_this.aod=p_aod
        tmp_this.portfolio_risk.CopyFrom(p_portfolio_risk)
        tmp_this.position_risks.extend(p_position_risks)
        tmp_this.realized_pnl=p_realized_pnl
        tmp_this.pnl_matrices.extend(p_pnl_matrices)
        tmp_this.portfolio_id=p_portfolio_id
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#RiskFactorDataCleansingSettings
def dqCreateProtoRiskFactorDataCleansingSettings(p_benchmark_return_settings, p_index_return_settings, p_instrument_cleansed_return_settings, p_benchmark_index):
    '''
    @args:
        1. p_benchmark_return_settings: dqproto.InstrumentReturnSettings
        2. p_index_return_settings: dqproto.InstrumentReturnSettings
        3. p_instrument_cleansed_return_settings: dqproto.InstrumentCleansedReturnSettings
        4. p_benchmark_index: string
    @return:
        dqproto.RiskFactorDataCleansingSettings
    '''
    try:
        tmp_this= RiskFactorDataCleansingSettings()
        tmp_this.benchmark_return_settings.CopyFrom(p_benchmark_return_settings)
        tmp_this.index_return_settings.CopyFrom(p_index_return_settings)
        tmp_this.instrument_cleansed_return_settings.CopyFrom(p_instrument_cleansed_return_settings)
        tmp_this.benchmark_index=p_benchmark_index
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Scenario
def dqCreateProtoScenario(p_risk_factor_name, p_type, p_period, p_values, p_dates, p_as_of_date):
    '''
    @args:
        1. p_risk_factor_name: string
        2. p_type: dqproto.RiskFactorChangeType
        3. p_period: dqproto.Period
        4. p_values: dqproto.Vector
        5. p_dates: dqproto.Date
        6. p_as_of_date: dqproto.Date
    @return:
        dqproto.Scenario
    '''
    try:
        tmp_this= Scenario()
        tmp_this.risk_factor_name=p_risk_factor_name
        tmp_this.type=p_type
        tmp_this.period.CopyFrom(p_period)
        tmp_this.values.CopyFrom(p_values)
        tmp_this.dates.extend(p_dates)
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ScenarioGenSettings
def dqCreateProtoScenarioGenSettings(p_risk_factor_change_type, p_change_period, p_num_scenarios, p_ewma_decay_factor, p_smoothing_weight, p_zero_return_handling, p_vol_floor, p_vol_cap, p_stressed_start_date, p_stress_day_lag):
    '''
    @args:
        1. p_risk_factor_change_type: dqproto.RiskFactorChangeType
        2. p_change_period: dqproto.Period
        3. p_num_scenarios: int32
        4. p_ewma_decay_factor: double
        5. p_smoothing_weight: double
        6. p_zero_return_handling: dqproto.ZeroReturnHandlingMethod
        7. p_vol_floor: double
        8. p_vol_cap: double
        9. p_stressed_start_date: dqproto.Date
        10. p_stress_day_lag: int32
    @return:
        dqproto.ScenarioGenSettings
    '''
    try:
        tmp_this= ScenarioGenSettings()
        tmp_this.risk_factor_change_type=p_risk_factor_change_type
        tmp_this.change_period.CopyFrom(p_change_period)
        tmp_this.num_scenarios=p_num_scenarios
        tmp_this.ewma_decay_factor=p_ewma_decay_factor
        tmp_this.smoothing_weight=p_smoothing_weight
        tmp_this.zero_return_handling=p_zero_return_handling
        tmp_this.vol_floor=p_vol_floor
        tmp_this.vol_cap=p_vol_cap
        tmp_this.stressed_start_date.CopyFrom(p_stressed_start_date)
        tmp_this.stress_day_lag=p_stress_day_lag
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ScenarioManagerItem
def dqCreateProtoScenarioManagerItem(p_name, p_scenario):
    '''
    @args:
        1. p_name: string
        2. p_scenario: dqproto.Scenario
    @return:
        dqproto.ScenarioManagerItem
    '''
    try:
        tmp_this= ScenarioManagerItem()
        tmp_this.name=p_name
        tmp_this.scenario.CopyFrom(p_scenario)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#ScenarioManager
def dqCreateProtoScenarioManager(p_items):
    '''
    @args:
        1. p_items: dqproto.ScenarioManagerItem
    @return:
        dqproto.ScenarioManager
    '''
    try:
        tmp_this= ScenarioManager()
        tmp_this.items.extend(p_items)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#StressedScnGenSettings
def dqCreateProtoStressedScnGenSettings(p_risk_factor_change_type, p_change_period, p_benchmark_index, p_stressed_start_date, p_stress_day_lag):
    '''
    @args:
        1. p_risk_factor_change_type: dqproto.RiskFactorChangeType
        2. p_change_period: dqproto.Period
        3. p_benchmark_index: string
        4. p_stressed_start_date: dqproto.Date
        5. p_stress_day_lag: int32
    @return:
        dqproto.StressedScnGenSettings
    '''
    try:
        tmp_this= StressedScnGenSettings()
        tmp_this.risk_factor_change_type=p_risk_factor_change_type
        tmp_this.change_period.CopyFrom(p_change_period)
        tmp_this.benchmark_index=p_benchmark_index
        tmp_this.stressed_start_date.CopyFrom(p_stressed_start_date)
        tmp_this.stress_day_lag=p_stress_day_lag
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#TierNInitialMarginSettings
def dqCreateProtoTierNInitialMarginSettings(p_num_days_for_return, p_volatility_mulitplier, p_margin_floor, p_liquidity_risk_buffer, p_benchmark_indices):
    '''
    @args:
        1. p_num_days_for_return: int32
        2. p_volatility_mulitplier: double
        3. p_margin_floor: double
        4. p_liquidity_risk_buffer: double
        5. p_benchmark_indices: string
    @return:
        dqproto.TierNInitialMarginSettings
    '''
    try:
        tmp_this= TierNInitialMarginSettings()
        tmp_this.num_days_for_return=p_num_days_for_return
        tmp_this.volatility_mulitplier=p_volatility_mulitplier
        tmp_this.margin_floor=p_margin_floor
        tmp_this.liquidity_risk_buffer=p_liquidity_risk_buffer
        tmp_this.benchmark_indices.extend(p_benchmark_indices)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#TierPInitialMarginSettings
def dqCreateProtoTierPInitialMarginSettings(p_im_type, p_margin_floor_rate, p_stress_risk_contribution, p_hs_settings, p_stressed_settings):
    '''
    @args:
        1. p_im_type: dqproto.InitialMarginType
        2. p_margin_floor_rate: double
        3. p_stress_risk_contribution: double
        4. p_hs_settings: dqproto.MarketRiskMeasureSettings
        5. p_stressed_settings: dqproto.MarketRiskMeasureSettings
    @return:
        dqproto.TierPInitialMarginSettings
    '''
    try:
        tmp_this= TierPInitialMarginSettings()
        tmp_this.im_type=p_im_type
        tmp_this.margin_floor_rate=p_margin_floor_rate
        tmp_this.stress_risk_contribution=p_stress_risk_contribution
        tmp_this.hs_settings.CopyFrom(p_hs_settings)
        tmp_this.stressed_settings.CopyFrom(p_stressed_settings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#TradingPosition
def dqCreateProtoTradingPosition(p_buy_sell, p_norminal, p_inst_name, p_tier):
    '''
    @args:
        1. p_buy_sell: dqproto.BuySellFlag
        2. p_norminal: double
        3. p_inst_name: string
        4. p_tier: dqproto.InstrumentTier
    @return:
        dqproto.TradingPosition
    '''
    try:
        tmp_this= TradingPosition()
        tmp_this.buy_sell=p_buy_sell
        tmp_this.norminal=p_norminal
        tmp_this.inst_name=p_inst_name
        tmp_this.tier=p_tier
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Portfolio
def dqCreateProtoPortfolio(p_id, p_position):
    '''
    @args:
        1. p_id: string
        2. p_position: dqproto.TradingPosition
    @return:
        dqproto.Portfolio
    '''
    try:
        tmp_this= Portfolio()
        tmp_this.id=p_id
        tmp_this.position.extend(p_position)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateExpectedShortfallInput
def dqCreateProtoCalculateExpectedShortfallInput(p_profit_loss_samples, p_probability, p_calc_es_mirrored):
    '''
    @args:
        1. p_profit_loss_samples: dqproto.Vector
        2. p_probability: double
        3. p_calc_es_mirrored: bool
    @return:
        dqproto.CalculateExpectedShortfallInput
    '''
    try:
        tmp_this= CalculateExpectedShortfallInput()
        tmp_this.profit_loss_samples.CopyFrom(p_profit_loss_samples)
        tmp_this.probability=p_probability
        tmp_this.calc_es_mirrored=p_calc_es_mirrored
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateExpectedShortfallOutput
def dqCreateProtoCalculateExpectedShortfallOutput(p_expected_shortfall, p_expected_shortfall_mirrored, p_success, p_err_msg):
    '''
    @args:
        1. p_expected_shortfall: double
        2. p_expected_shortfall_mirrored: double
        3. p_success: bool
        4. p_err_msg: string
    @return:
        dqproto.CalculateExpectedShortfallOutput
    '''
    try:
        tmp_this= CalculateExpectedShortfallOutput()
        tmp_this.expected_shortfall=p_expected_shortfall
        tmp_this.expected_shortfall_mirrored=p_expected_shortfall_mirrored
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateValueAtRiskInput
def dqCreateProtoCalculateValueAtRiskInput(p_profit_loss_samples, p_probability, p_calc_var_mirrored):
    '''
    @args:
        1. p_profit_loss_samples: dqproto.Vector
        2. p_probability: double
        3. p_calc_var_mirrored: bool
    @return:
        dqproto.CalculateValueAtRiskInput
    '''
    try:
        tmp_this= CalculateValueAtRiskInput()
        tmp_this.profit_loss_samples.CopyFrom(p_profit_loss_samples)
        tmp_this.probability=p_probability
        tmp_this.calc_var_mirrored=p_calc_var_mirrored
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateValueAtRiskOutput
def dqCreateProtoCalculateValueAtRiskOutput(p_value_at_risk, p_value_at_risk_mirrored, p_success, p_err_msg):
    '''
    @args:
        1. p_value_at_risk: double
        2. p_value_at_risk_mirrored: double
        3. p_success: bool
        4. p_err_msg: string
    @return:
        dqproto.CalculateValueAtRiskOutput
    '''
    try:
        tmp_this= CalculateValueAtRiskOutput()
        tmp_this.value_at_risk=p_value_at_risk
        tmp_this.value_at_risk_mirrored=p_value_at_risk_mirrored
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildHistSimIrYieldCurveInput
def dqCreateProtoBuildHistSimIrYieldCurveInput(p_sim_date, p_reference_curve, p_hist_curve_start, p_hist_curve_end, p_curve_dates):
    '''
    @args:
        1. p_sim_date: dqproto.Date
        2. p_reference_curve: dqproto.IrYieldCurve
        3. p_hist_curve_start: dqproto.IrYieldCurve
        4. p_hist_curve_end: dqproto.IrYieldCurve
        5. p_curve_dates: dqproto.Date
    @return:
        dqproto.BuildHistSimIrYieldCurveInput
    '''
    try:
        tmp_this= BuildHistSimIrYieldCurveInput()
        tmp_this.sim_date.CopyFrom(p_sim_date)
        tmp_this.reference_curve.CopyFrom(p_reference_curve)
        tmp_this.hist_curve_start.CopyFrom(p_hist_curve_start)
        tmp_this.hist_curve_end.CopyFrom(p_hist_curve_end)
        tmp_this.curve_dates.extend(p_curve_dates)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildHistSimIrYieldCurveOutput
def dqCreateProtoBuildHistSimIrYieldCurveOutput(p_ir_yield_curve, p_success, p_err_msg):
    '''
    @args:
        1. p_ir_yield_curve: dqproto.IrYieldCurve
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildHistSimIrYieldCurveOutput
    '''
    try:
        tmp_this= BuildHistSimIrYieldCurveOutput()
        tmp_this.ir_yield_curve.CopyFrom(p_ir_yield_curve)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildHistSimCreditCurveInput
def dqCreateProtoBuildHistSimCreditCurveInput(p_sim_date, p_reference_curve, p_hist_curve_start, p_hist_curve_end, p_curve_dates):
    '''
    @args:
        1. p_sim_date: dqproto.Date
        2. p_reference_curve: dqproto.CreditCurve
        3. p_hist_curve_start: dqproto.CreditCurve
        4. p_hist_curve_end: dqproto.CreditCurve
        5. p_curve_dates: dqproto.Date
    @return:
        dqproto.BuildHistSimCreditCurveInput
    '''
    try:
        tmp_this= BuildHistSimCreditCurveInput()
        tmp_this.sim_date.CopyFrom(p_sim_date)
        tmp_this.reference_curve.CopyFrom(p_reference_curve)
        tmp_this.hist_curve_start.CopyFrom(p_hist_curve_start)
        tmp_this.hist_curve_end.CopyFrom(p_hist_curve_end)
        tmp_this.curve_dates.extend(p_curve_dates)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildHistSimCreditCurveOutput
def dqCreateProtoBuildHistSimCreditCurveOutput(p_sim_curve, p_success, p_err_msg):
    '''
    @args:
        1. p_sim_curve: dqproto.CreditCurve
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildHistSimCreditCurveOutput
    '''
    try:
        tmp_this= BuildHistSimCreditCurveOutput()
        tmp_this.sim_curve.CopyFrom(p_sim_curve)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildHistSimFxSpotRateInput
def dqCreateProtoBuildHistSimFxSpotRateInput(p_sim_date, p_reference_spot, p_hist_spot_start, p_hist_spot_end, p_use_template, p_fx_spot_template):
    '''
    @args:
        1. p_sim_date: dqproto.Date
        2. p_reference_spot: dqproto.FxSpotRate
        3. p_hist_spot_start: dqproto.FxSpotRate
        4. p_hist_spot_end: dqproto.FxSpotRate
        5. p_use_template: bool
        6. p_fx_spot_template: dqproto.FxSpotTemplate
    @return:
        dqproto.BuildHistSimFxSpotRateInput
    '''
    try:
        tmp_this= BuildHistSimFxSpotRateInput()
        tmp_this.sim_date.CopyFrom(p_sim_date)
        tmp_this.reference_spot.CopyFrom(p_reference_spot)
        tmp_this.hist_spot_start.CopyFrom(p_hist_spot_start)
        tmp_this.hist_spot_end.CopyFrom(p_hist_spot_end)
        tmp_this.use_template=p_use_template
        tmp_this.fx_spot_template.CopyFrom(p_fx_spot_template)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildHistSimFxSpotRateOutput
def dqCreateProtoBuildHistSimFxSpotRateOutput(p_fx_spot_rate, p_success, p_err_msg):
    '''
    @args:
        1. p_fx_spot_rate: dqproto.FxSpotRate
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildHistSimFxSpotRateOutput
    '''
    try:
        tmp_this= BuildHistSimFxSpotRateOutput()
        tmp_this.fx_spot_rate.CopyFrom(p_fx_spot_rate)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildHistSimFxVolSurfaceInput
def dqCreateProtoBuildHistSimFxVolSurfaceInput(p_sim_date, p_reference_vol_surf, p_hist_vol_surf_start, p_hist_vol_surf_end, p_vol_surf_dates, p_vol_surf_strikes, p_spot, p_dom_discount_curve, p_for_discount_curve, p_settings):
    '''
    @args:
        1. p_sim_date: dqproto.Date
        2. p_reference_vol_surf: dqproto.FxVolatilitySurface
        3. p_hist_vol_surf_start: dqproto.FxVolatilitySurface
        4. p_hist_vol_surf_end: dqproto.FxVolatilitySurface
        5. p_vol_surf_dates: dqproto.Date
        6. p_vol_surf_strikes: dqproto.Vector
        7. p_spot: dqproto.FxSpotRate
        8. p_dom_discount_curve: dqproto.IrYieldCurve
        9. p_for_discount_curve: dqproto.IrYieldCurve
        10. p_settings: dqproto.VolatilitySurfaceBuildSettings
    @return:
        dqproto.BuildHistSimFxVolSurfaceInput
    '''
    try:
        tmp_this= BuildHistSimFxVolSurfaceInput()
        tmp_this.sim_date.CopyFrom(p_sim_date)
        tmp_this.reference_vol_surf.CopyFrom(p_reference_vol_surf)
        tmp_this.hist_vol_surf_start.CopyFrom(p_hist_vol_surf_start)
        tmp_this.hist_vol_surf_end.CopyFrom(p_hist_vol_surf_end)
        tmp_this.vol_surf_dates.extend(p_vol_surf_dates)
        tmp_this.vol_surf_strikes.extend(p_vol_surf_strikes)
        tmp_this.spot.CopyFrom(p_spot)
        tmp_this.dom_discount_curve.CopyFrom(p_dom_discount_curve)
        tmp_this.for_discount_curve.CopyFrom(p_for_discount_curve)
        tmp_this.settings.CopyFrom(p_settings)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BuildHistSimFxVolSurfaceOutput
def dqCreateProtoBuildHistSimFxVolSurfaceOutput(p_fx_volatility_surface, p_success, p_err_msg):
    '''
    @args:
        1. p_fx_volatility_surface: dqproto.FxVolatilitySurface
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.BuildHistSimFxVolSurfaceOutput
    '''
    try:
        tmp_this= BuildHistSimFxVolSurfaceOutput()
        tmp_this.fx_volatility_surface.CopyFrom(p_fx_volatility_surface)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CurveSensiTransformerInput
def dqCreateProtoCurveSensiTransformerInput(p_dest_terms, p_src_terms, p_src_sensi):
    '''
    @args:
        1. p_dest_terms: dqproto.Vector
        2. p_src_terms: dqproto.Vector
        3. p_src_sensi: dqproto.Vector
    @return:
        dqproto.CurveSensiTransformerInput
    '''
    try:
        tmp_this= CurveSensiTransformerInput()
        tmp_this.dest_terms.CopyFrom(p_dest_terms)
        tmp_this.src_terms.CopyFrom(p_src_terms)
        tmp_this.src_sensi.CopyFrom(p_src_sensi)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CurveSensiTransformerOutput
def dqCreateProtoCurveSensiTransformerOutput(p_new_sensi, p_success, p_err_msg):
    '''
    @args:
        1. p_new_sensi: dqproto.Vector
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CurveSensiTransformerOutput
    '''
    try:
        tmp_this= CurveSensiTransformerOutput()
        tmp_this.new_sensi.CopyFrom(p_new_sensi)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateInitialMarginInput
def dqCreateProtoCalculateInitialMarginInput(p_type, p_positions, p_fhs_return_scenarios, p_stress_return_scenarios, p_probability, p_stress_risk_contribution, p_floor_rate, p_fhs_risk_measure_type, p_stress_risk_measure_type, p_analysis_type):
    '''
    @args:
        1. p_type: dqproto.InitialMarginType
        2. p_positions: dqproto.TradingPosition
        3. p_fhs_return_scenarios: dqproto.Matrix
        4. p_stress_return_scenarios: dqproto.Matrix
        5. p_probability: double
        6. p_stress_risk_contribution: double
        7. p_floor_rate: double
        8. p_fhs_risk_measure_type: dqproto.MarketRiskMeasure
        9. p_stress_risk_measure_type: dqproto.MarketRiskMeasure
        10. p_analysis_type: dqproto.MarketRiskAnalysisType
    @return:
        dqproto.CalculateInitialMarginInput
    '''
    try:
        tmp_this= CalculateInitialMarginInput()
        tmp_this.type=p_type
        tmp_this.positions.extend(p_positions)
        tmp_this.fhs_return_scenarios.CopyFrom(p_fhs_return_scenarios)
        tmp_this.stress_return_scenarios.CopyFrom(p_stress_return_scenarios)
        tmp_this.probability=p_probability
        tmp_this.stress_risk_contribution=p_stress_risk_contribution
        tmp_this.floor_rate=p_floor_rate
        tmp_this.fhs_risk_measure_type=p_fhs_risk_measure_type
        tmp_this.stress_risk_measure_type=p_stress_risk_measure_type
        tmp_this.analysis_type=p_analysis_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateInitialMarginOutput
def dqCreateProtoCalculateInitialMarginOutput(p_initial_margin_first, p_initial_margin_second):
    '''
    @args:
        1. p_initial_margin_first: double
        2. p_initial_margin_second: double
    @return:
        dqproto.CalculateInitialMarginOutput
    '''
    try:
        tmp_this= CalculateInitialMarginOutput()
        tmp_this.initial_margin_first=p_initial_margin_first
        tmp_this.initial_margin_second=p_initial_margin_second
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateInstrumentCleansedReturnsInput
def dqCreateProtoCalculateInstrumentCleansedReturnsInput(p_settings, p_inst_price_series, p_inst_listed_date, p_proxy_return_series):
    '''
    @args:
        1. p_settings: dqproto.InstrumentCleansedReturnSettings
        2. p_inst_price_series: dqproto.TimeSeries
        3. p_inst_listed_date: dqproto.Date
        4. p_proxy_return_series: dqproto.InstrumentStatisticsSeries
    @return:
        dqproto.CalculateInstrumentCleansedReturnsInput
    '''
    try:
        tmp_this= CalculateInstrumentCleansedReturnsInput()
        tmp_this.settings.CopyFrom(p_settings)
        tmp_this.inst_price_series.CopyFrom(p_inst_price_series)
        tmp_this.inst_listed_date.CopyFrom(p_inst_listed_date)
        tmp_this.proxy_return_series.CopyFrom(p_proxy_return_series)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateInstrumentCleansedReturnsOutput
def dqCreateProtoCalculateInstrumentCleansedReturnsOutput(p_cleansed_returns_series):
    '''
    @args:
        1. p_cleansed_returns_series: dqproto.InstrumentStatisticsSeries
    @return:
        dqproto.CalculateInstrumentCleansedReturnsOutput
    '''
    try:
        tmp_this= CalculateInstrumentCleansedReturnsOutput()
        tmp_this.cleansed_returns_series.CopyFrom(p_cleansed_returns_series)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateInstrumentRawReturnsInput
def dqCreateProtoCalculateInstrumentRawReturnsInput(p_settings, p_inst_price_series):
    '''
    @args:
        1. p_settings: dqproto.InstrumentReturnSettings
        2. p_inst_price_series: dqproto.TimeSeries
    @return:
        dqproto.CalculateInstrumentRawReturnsInput
    '''
    try:
        tmp_this= CalculateInstrumentRawReturnsInput()
        tmp_this.settings.CopyFrom(p_settings)
        tmp_this.inst_price_series.CopyFrom(p_inst_price_series)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateInstrumentRawReturnsOutput
def dqCreateProtoCalculateInstrumentRawReturnsOutput(p_raw_returns_series):
    '''
    @args:
        1. p_raw_returns_series: dqproto.InstrumentStatisticsSeries
    @return:
        dqproto.CalculateInstrumentRawReturnsOutput
    '''
    try:
        tmp_this= CalculateInstrumentRawReturnsOutput()
        tmp_this.raw_returns_series.CopyFrom(p_raw_returns_series)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateInstrumentStatisticsInput
def dqCreateProtoCalculateInstrumentStatisticsInput(p_inst_price_series, p_seed_date, p_num_seed_days, p_ewma_decay_factors, p_seed_mode, p_use_fallback, p_fallback_indicator, p_vol_multiplier, p_inst_listed_date, p_proxy_inst_stat_series, p_zero_return_handling, p_return_type, p_period, p_start_date, p_end_date):
    '''
    @args:
        1. p_inst_price_series: dqproto.TimeSeries
        2. p_seed_date: dqproto.Date
        3. p_num_seed_days: int32
        4. p_ewma_decay_factors: double
        5. p_seed_mode: dqproto.EwmaSeedMode
        6. p_use_fallback: bool
        7. p_fallback_indicator: int32
        8. p_vol_multiplier: double
        9. p_inst_listed_date: dqproto.Date
        10. p_proxy_inst_stat_series: dqproto.InstrumentStatisticsSeries
        11. p_zero_return_handling: dqproto.ZeroReturnHandlingMethod
        12. p_return_type: dqproto.RiskFactorChangeType
        13. p_period: dqproto.Period
        14. p_start_date: dqproto.Date
        15. p_end_date: dqproto.Date
    @return:
        dqproto.CalculateInstrumentStatisticsInput
    '''
    try:
        tmp_this= CalculateInstrumentStatisticsInput()
        tmp_this.inst_price_series.CopyFrom(p_inst_price_series)
        tmp_this.seed_date.CopyFrom(p_seed_date)
        tmp_this.num_seed_days=p_num_seed_days
        tmp_this.ewma_decay_factors.extend(p_ewma_decay_factors)
        tmp_this.seed_mode=p_seed_mode
        tmp_this.use_fallback=p_use_fallback
        tmp_this.fallback_indicator=p_fallback_indicator
        tmp_this.vol_multiplier=p_vol_multiplier
        tmp_this.inst_listed_date.CopyFrom(p_inst_listed_date)
        tmp_this.proxy_inst_stat_series.CopyFrom(p_proxy_inst_stat_series)
        tmp_this.zero_return_handling=p_zero_return_handling
        tmp_this.return_type=p_return_type
        tmp_this.period.CopyFrom(p_period)
        tmp_this.start_date.CopyFrom(p_start_date)
        tmp_this.end_date.CopyFrom(p_end_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateInstrumentStatisticsOutput
def dqCreateProtoCalculateInstrumentStatisticsOutput(p_inst_stat_series):
    '''
    @args:
        1. p_inst_stat_series: dqproto.InstrumentStatisticsSeries
    @return:
        dqproto.CalculateInstrumentStatisticsOutput
    '''
    try:
        tmp_this= CalculateInstrumentStatisticsOutput()
        tmp_this.inst_stat_series.CopyFrom(p_inst_stat_series)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateMarginFloorInput
def dqCreateProtoCalculateMarginFloorInput(p_positions, p_floor_rate):
    '''
    @args:
        1. p_positions: dqproto.TradingPosition
        2. p_floor_rate: double
    @return:
        dqproto.CalculateMarginFloorInput
    '''
    try:
        tmp_this= CalculateMarginFloorInput()
        tmp_this.positions.extend(p_positions)
        tmp_this.floor_rate=p_floor_rate
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateMarginFloorOutput
def dqCreateProtoCalculateMarginFloorOutput(p_margin_floor):
    '''
    @args:
        1. p_margin_floor: double
    @return:
        dqproto.CalculateMarginFloorOutput
    '''
    try:
        tmp_this= CalculateMarginFloorOutput()
        tmp_this.margin_floor=p_margin_floor
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateProfitLossInput
def dqCreateProtoCalculateProfitLossInput(p_portfolio, p_scenarios):
    '''
    @args:
        1. p_portfolio: dqproto.Portfolio
        2. p_scenarios: dqproto.Scenario
    @return:
        dqproto.CalculateProfitLossInput
    '''
    try:
        tmp_this= CalculateProfitLossInput()
        tmp_this.portfolio.CopyFrom(p_portfolio)
        tmp_this.scenarios.extend(p_scenarios)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateProfitLossOutput.Row
def dqCreateProtoCalculateProfitLossOutput_Row(p_name, p_profit_loss_samples):
    '''
    @args:
        1. p_name: string
        2. p_profit_loss_samples: dqproto.Vector
    @return:
        dqproto.CalculateProfitLossOutput.Row
    '''
    try:
        tmp_this= CalculateProfitLossOutput.Row()
        tmp_this.name=p_name
        tmp_this.profit_loss_samples.CopyFrom(p_profit_loss_samples)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateProfitLossOutput
def dqCreateProtoCalculateProfitLossOutput(p_profit_losses):
    '''
    @args:
        1. p_profit_losses: dqproto.CalculateProfitLossOutput.Row
    @return:
        dqproto.CalculateProfitLossOutput
    '''
    try:
        tmp_this= CalculateProfitLossOutput()
        tmp_this.profit_losses.extend(p_profit_losses)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateRiskFactorReturnInput
def dqCreateProtoCalculateRiskFactorReturnInput(p_placeholder):
    '''
    @args:
        1. p_placeholder: double
    @return:
        dqproto.CalculateRiskFactorReturnInput
    '''
    try:
        tmp_this= CalculateRiskFactorReturnInput()
        tmp_this.placeholder=p_placeholder
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CalculateRiskFactorReturnOutput
def dqCreateProtoCalculateRiskFactorReturnOutput(p_placeholder):
    '''
    @args:
        1. p_placeholder: double
    @return:
        dqproto.CalculateRiskFactorReturnOutput
    '''
    try:
        tmp_this= CalculateRiskFactorReturnOutput()
        tmp_this.placeholder=p_placeholder
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GenerateFhsScenariosInput
def dqCreateProtoGenerateFhsScenariosInput(p_inst_stat_series, p_risk_factor_name, p_settings, p_as_of_date):
    '''
    @args:
        1. p_inst_stat_series: dqproto.InstrumentStatisticsSeries
        2. p_risk_factor_name: string
        3. p_settings: dqproto.HsScnGenSettings
        4. p_as_of_date: dqproto.Date
    @return:
        dqproto.GenerateFhsScenariosInput
    '''
    try:
        tmp_this= GenerateFhsScenariosInput()
        tmp_this.inst_stat_series.CopyFrom(p_inst_stat_series)
        tmp_this.risk_factor_name=p_risk_factor_name
        tmp_this.settings.CopyFrom(p_settings)
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GenerateFhsScenariosOutput
def dqCreateProtoGenerateFhsScenariosOutput(p_scenarios):
    '''
    @args:
        1. p_scenarios: dqproto.Scenario
    @return:
        dqproto.GenerateFhsScenariosOutput
    '''
    try:
        tmp_this= GenerateFhsScenariosOutput()
        tmp_this.scenarios.CopyFrom(p_scenarios)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GenerateStressScenariosInput
def dqCreateProtoGenerateStressScenariosInput(p_inst_stat_series, p_risk_factor_name, p_settings, p_stress_dates, p_as_of_date):
    '''
    @args:
        1. p_inst_stat_series: dqproto.InstrumentStatisticsSeries
        2. p_risk_factor_name: string
        3. p_settings: dqproto.StressedScnGenSettings
        4. p_stress_dates: dqproto.Date
        5. p_as_of_date: dqproto.Date
    @return:
        dqproto.GenerateStressScenariosInput
    '''
    try:
        tmp_this= GenerateStressScenariosInput()
        tmp_this.inst_stat_series.CopyFrom(p_inst_stat_series)
        tmp_this.risk_factor_name=p_risk_factor_name
        tmp_this.settings.CopyFrom(p_settings)
        tmp_this.stress_dates.extend(p_stress_dates)
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GenerateStressScenariosOutput
def dqCreateProtoGenerateStressScenariosOutput(p_scenarios):
    '''
    @args:
        1. p_scenarios: dqproto.Scenario
    @return:
        dqproto.GenerateStressScenariosOutput
    '''
    try:
        tmp_this= GenerateStressScenariosOutput()
        tmp_this.scenarios.CopyFrom(p_scenarios)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IdentifyStressDatesInput
def dqCreateProtoIdentifyStressDatesInput(p_benchmark_stat_series, p_settings, p_as_of_date):
    '''
    @args:
        1. p_benchmark_stat_series: dqproto.InstrumentStatisticsSeries
        2. p_settings: dqproto.StressedScnGenSettings
        3. p_as_of_date: dqproto.Date
    @return:
        dqproto.IdentifyStressDatesInput
    '''
    try:
        tmp_this= IdentifyStressDatesInput()
        tmp_this.benchmark_stat_series.extend(p_benchmark_stat_series)
        tmp_this.settings.CopyFrom(p_settings)
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#IdentifyStressDatesOutput
def dqCreateProtoIdentifyStressDatesOutput(p_stress_dates):
    '''
    @args:
        1. p_stress_dates: dqproto.Date
    @return:
        dqproto.IdentifyStressDatesOutput
    '''
    try:
        tmp_this= IdentifyStressDatesOutput()
        tmp_this.stress_dates.extend(p_stress_dates)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#RunInitialMarginBacktestingEngineInput
def dqCreateProtoRunInitialMarginBacktestingEngineInput(p_schedule, p_portfolio, p_inst_raw_return_series_handle, p_all_cleansed_return_series_handle, p_im_settings, p_hs_scn_gen_settings, p_stressed_scn_gen_settings, p_type):
    '''
    @args:
        1. p_schedule: dqproto.Schedule
        2. p_portfolio: dqproto.Portfolio
        3. p_inst_raw_return_series_handle: string
        4. p_all_cleansed_return_series_handle: string
        5. p_im_settings: dqproto.InitialMarginSettings
        6. p_hs_scn_gen_settings: dqproto.HsScnGenSettings
        7. p_stressed_scn_gen_settings: dqproto.StressedScnGenSettings
        8. p_type: dqproto.MarketRiskAnalysisType
    @return:
        dqproto.RunInitialMarginBacktestingEngineInput
    '''
    try:
        tmp_this= RunInitialMarginBacktestingEngineInput()
        tmp_this.schedule.CopyFrom(p_schedule)
        tmp_this.portfolio.extend(p_portfolio)
        tmp_this.inst_raw_return_series_handle=p_inst_raw_return_series_handle
        tmp_this.all_cleansed_return_series_handle=p_all_cleansed_return_series_handle
        tmp_this.im_settings.CopyFrom(p_im_settings)
        tmp_this.hs_scn_gen_settings.CopyFrom(p_hs_scn_gen_settings)
        tmp_this.stressed_scn_gen_settings.CopyFrom(p_stressed_scn_gen_settings)
        tmp_this.type=p_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#RunInitialMarginBacktestingEngineOutput.ReportBin
def dqCreateProtoRunInitialMarginBacktestingEngineOutput_ReportBin(p_aod, p_portfolio_id, p_data):
    '''
    @args:
        1. p_aod: int32
        2. p_portfolio_id: string
        3. p_data: bytes
    @return:
        dqproto.RunInitialMarginBacktestingEngineOutput.ReportBin
    '''
    try:
        tmp_this= RunInitialMarginBacktestingEngineOutput.ReportBin()
        tmp_this.aod=p_aod
        tmp_this.portfolio_id=p_portfolio_id
        tmp_this.data=p_data
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#RunInitialMarginBacktestingEngineOutput.BacktestingResult
def dqCreateProtoRunInitialMarginBacktestingEngineOutput_BacktestingResult(p_portfolio_id, p_initial_margin, p_initial_margin_hs, p_initial_margin_stressed, p_mirrored_initial_margin, p_mirrored_initial_margin_hs, p_mirrored_initial_margin_stressed, p_realized_pnl):
    '''
    @args:
        1. p_portfolio_id: string
        2. p_initial_margin: dqproto.Vector
        3. p_initial_margin_hs: dqproto.Vector
        4. p_initial_margin_stressed: dqproto.Vector
        5. p_mirrored_initial_margin: dqproto.Vector
        6. p_mirrored_initial_margin_hs: dqproto.Vector
        7. p_mirrored_initial_margin_stressed: dqproto.Vector
        8. p_realized_pnl: dqproto.Vector
    @return:
        dqproto.RunInitialMarginBacktestingEngineOutput.BacktestingResult
    '''
    try:
        tmp_this= RunInitialMarginBacktestingEngineOutput.BacktestingResult()
        tmp_this.portfolio_id=p_portfolio_id
        tmp_this.initial_margin.CopyFrom(p_initial_margin)
        tmp_this.initial_margin_hs.CopyFrom(p_initial_margin_hs)
        tmp_this.initial_margin_stressed.CopyFrom(p_initial_margin_stressed)
        tmp_this.mirrored_initial_margin.CopyFrom(p_mirrored_initial_margin)
        tmp_this.mirrored_initial_margin_hs.CopyFrom(p_mirrored_initial_margin_hs)
        tmp_this.mirrored_initial_margin_stressed.CopyFrom(p_mirrored_initial_margin_stressed)
        tmp_this.realized_pnl.CopyFrom(p_realized_pnl)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#RunInitialMarginBacktestingEngineOutput
def dqCreateProtoRunInitialMarginBacktestingEngineOutput(p_schedule, p_result, p_report_bin, p_type):
    '''
    @args:
        1. p_schedule: dqproto.Schedule
        2. p_result: dqproto.RunInitialMarginBacktestingEngineOutput.BacktestingResult
        3. p_report_bin: dqproto.RunInitialMarginBacktestingEngineOutput.ReportBin
        4. p_type: dqproto.MarketRiskAnalysisType
    @return:
        dqproto.RunInitialMarginBacktestingEngineOutput
    '''
    try:
        tmp_this= RunInitialMarginBacktestingEngineOutput()
        tmp_this.schedule.CopyFrom(p_schedule)
        tmp_this.result.extend(p_result)
        tmp_this.report_bin.extend(p_report_bin)
        tmp_this.type=p_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#RunInitialMarginBacktestingInput
def dqCreateProtoRunInitialMarginBacktestingInput(p_schedule, p_portfolio, p_raw_return_series, p_cleansed_return_series, p_im_settings, p_hs_scn_gen_settings, p_stressed_scn_gen_settings, p_name, p_tag):
    '''
    @args:
        1. p_schedule: dqproto.Schedule
        2. p_portfolio: dqproto.Portfolio
        3. p_raw_return_series: dqproto.InstrumentStatisticsSeries
        4. p_cleansed_return_series: dqproto.InstrumentStatisticsSeries
        5. p_im_settings: dqproto.InitialMarginSettings
        6. p_hs_scn_gen_settings: dqproto.HsScnGenSettings
        7. p_stressed_scn_gen_settings: dqproto.StressedScnGenSettings
        8. p_name: string
        9. p_tag: string
    @return:
        dqproto.RunInitialMarginBacktestingInput
    '''
    try:
        tmp_this= RunInitialMarginBacktestingInput()
        tmp_this.schedule.CopyFrom(p_schedule)
        tmp_this.portfolio.extend(p_portfolio)
        tmp_this.raw_return_series.extend(p_raw_return_series)
        tmp_this.cleansed_return_series.extend(p_cleansed_return_series)
        tmp_this.im_settings.CopyFrom(p_im_settings)
        tmp_this.hs_scn_gen_settings.CopyFrom(p_hs_scn_gen_settings)
        tmp_this.stressed_scn_gen_settings.CopyFrom(p_stressed_scn_gen_settings)
        tmp_this.name=p_name
        tmp_this.tag=p_tag
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#RunInitialMarginBacktestingOutput
def dqCreateProtoRunInitialMarginBacktestingOutput(p_initial_margin_backtesting_engine):
    '''
    @args:
        1. p_initial_margin_backtesting_engine: string
    @return:
        dqproto.RunInitialMarginBacktestingOutput
    '''
    try:
        tmp_this= RunInitialMarginBacktestingOutput()
        tmp_this.initial_margin_backtesting_engine=p_initial_margin_backtesting_engine
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetInitialMarginBacktestingResultInput
def dqCreateProtoGetInitialMarginBacktestingResultInput(p_initial_margin_backtesting_engine, p_portfolio, p_instrument, p_backtesting_date, p_option):
    '''
    @args:
        1. p_initial_margin_backtesting_engine: string
        2. p_portfolio: string
        3. p_instrument: string
        4. p_backtesting_date: dqproto.Date
        5. p_option: string
    @return:
        dqproto.GetInitialMarginBacktestingResultInput
    '''
    try:
        tmp_this= GetInitialMarginBacktestingResultInput()
        tmp_this.initial_margin_backtesting_engine=p_initial_margin_backtesting_engine
        tmp_this.portfolio=p_portfolio
        tmp_this.instrument=p_instrument
        tmp_this.backtesting_date.CopyFrom(p_backtesting_date)
        tmp_this.option=p_option
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#GetInitialMarginBacktestingResultOutput
def dqCreateProtoGetInitialMarginBacktestingResultOutput(p_portfolio_margins, p_portfolio_margins_hs, p_portfolio_margins_stressed, p_antithetic_portfolio_margins, p_antithetic_portfolio_margins_hs, p_antithetic_portfolio_margins_stressed, p_position_margin, p_position_margin_hs, p_position_margin_stressed, p_antithetic_position_margin, p_antithetic_position_margin_hs, p_antithetic_position_margin_stressed, p_profit_losses):
    '''
    @args:
        1. p_portfolio_margins: dqproto.Vector
        2. p_portfolio_margins_hs: dqproto.Vector
        3. p_portfolio_margins_stressed: dqproto.Vector
        4. p_antithetic_portfolio_margins: dqproto.Vector
        5. p_antithetic_portfolio_margins_hs: dqproto.Vector
        6. p_antithetic_portfolio_margins_stressed: dqproto.Vector
        7. p_position_margin: double
        8. p_position_margin_hs: double
        9. p_position_margin_stressed: double
        10. p_antithetic_position_margin: double
        11. p_antithetic_position_margin_hs: double
        12. p_antithetic_position_margin_stressed: double
        13. p_profit_losses: dqproto.Vector
    @return:
        dqproto.GetInitialMarginBacktestingResultOutput
    '''
    try:
        tmp_this= GetInitialMarginBacktestingResultOutput()
        tmp_this.portfolio_margins.CopyFrom(p_portfolio_margins)
        tmp_this.portfolio_margins_hs.CopyFrom(p_portfolio_margins_hs)
        tmp_this.portfolio_margins_stressed.CopyFrom(p_portfolio_margins_stressed)
        tmp_this.antithetic_portfolio_margins.CopyFrom(p_antithetic_portfolio_margins)
        tmp_this.antithetic_portfolio_margins_hs.CopyFrom(p_antithetic_portfolio_margins_hs)
        tmp_this.antithetic_portfolio_margins_stressed.CopyFrom(p_antithetic_portfolio_margins_stressed)
        tmp_this.position_margin=p_position_margin
        tmp_this.position_margin_hs=p_position_margin_hs
        tmp_this.position_margin_stressed=p_position_margin_stressed
        tmp_this.antithetic_position_margin=p_antithetic_position_margin
        tmp_this.antithetic_position_margin_hs=p_antithetic_position_margin_hs
        tmp_this.antithetic_position_margin_stressed=p_antithetic_position_margin_stressed
        tmp_this.profit_losses.CopyFrom(p_profit_losses)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#MktDataBuildingInput
def dqCreateProtoMktDataBuildingInput(p_as_of_date, p_spot, p_discount_curve, p_asset_curve, p_quote_matrix, p_spot_greeks, p_vol_greeks, p_spot_vol_greeks, p_theta, p_dSpot, p_dVol, p_object_handle, p_vol_surf_definition):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_spot: double
        3. p_discount_curve: dqproto.IrYieldCurve
        4. p_asset_curve: dqproto.AssetYieldCurve
        5. p_quote_matrix: dqproto.OptionQuoteMatrix
        6. p_spot_greeks: bool
        7. p_vol_greeks: bool
        8. p_spot_vol_greeks: bool
        9. p_theta: bool
        10. p_dSpot: double
        11. p_dVol: double
        12. p_object_handle: string
        13. p_vol_surf_definition: dqproto.VolatilitySurfaceDefinition
    @return:
        dqproto.MktDataBuildingInput
    '''
    try:
        tmp_this= MktDataBuildingInput()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.spot=p_spot
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.asset_curve.CopyFrom(p_asset_curve)
        tmp_this.quote_matrix.CopyFrom(p_quote_matrix)
        tmp_this.spot_greeks=p_spot_greeks
        tmp_this.vol_greeks=p_vol_greeks
        tmp_this.spot_vol_greeks=p_spot_vol_greeks
        tmp_this.theta=p_theta
        tmp_this.dSpot=p_dSpot
        tmp_this.dVol=p_dVol
        tmp_this.object_handle=p_object_handle
        tmp_this.vol_surf_definition.CopyFrom(p_vol_surf_definition)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#MktDataBuildingOutput
def dqCreateProtoMktDataBuildingOutput(p_object_handle):
    '''
    @args:
        1. p_object_handle: string
    @return:
        dqproto.MktDataBuildingOutput
    '''
    try:
        tmp_this= MktDataBuildingOutput()
        tmp_this.object_handle=p_object_handle
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#StressedMktDataBuildingInput
def dqCreateProtoStressedMktDataBuildingInput(p_spot, p_discount_curve, p_asset_curve, p_vol_surf, p_spot_shift, p_vol_shift, p_interest_rate_shift, p_asset_yield_shift, p_object_handle):
    '''
    @args:
        1. p_spot: double
        2. p_discount_curve: dqproto.IrYieldCurve
        3. p_asset_curve: dqproto.AssetYieldCurve
        4. p_vol_surf: dqproto.VolatilitySurface
        5. p_spot_shift: double
        6. p_vol_shift: double
        7. p_interest_rate_shift: double
        8. p_asset_yield_shift: double
        9. p_object_handle: string
    @return:
        dqproto.StressedMktDataBuildingInput
    '''
    try:
        tmp_this= StressedMktDataBuildingInput()
        tmp_this.spot=p_spot
        tmp_this.discount_curve.CopyFrom(p_discount_curve)
        tmp_this.asset_curve.CopyFrom(p_asset_curve)
        tmp_this.vol_surf.CopyFrom(p_vol_surf)
        tmp_this.spot_shift=p_spot_shift
        tmp_this.vol_shift=p_vol_shift
        tmp_this.interest_rate_shift=p_interest_rate_shift
        tmp_this.asset_yield_shift=p_asset_yield_shift
        tmp_this.object_handle=p_object_handle
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#StressedMktDataBuildingOutput
def dqCreateProtoStressedMktDataBuildingOutput(p_object_handle):
    '''
    @args:
        1. p_object_handle: string
    @return:
        dqproto.StressedMktDataBuildingOutput
    '''
    try:
        tmp_this= StressedMktDataBuildingOutput()
        tmp_this.object_handle=p_object_handle
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#RiskFactorChangeCalculationInput
def dqCreateProtoRiskFactorChangeCalculationInput(p_type, p_samples):
    '''
    @args:
        1. p_type: dqproto.RiskFactorChangeType
        2. p_samples: dqproto.Vector
    @return:
        dqproto.RiskFactorChangeCalculationInput
    '''
    try:
        tmp_this= RiskFactorChangeCalculationInput()
        tmp_this.type=p_type
        tmp_this.samples.CopyFrom(p_samples)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#InstrumentQuoteSeries
def dqCreateProtoInstrumentQuoteSeries(p_quote_series, p_listed_date, p_proxy_index):
    '''
    @args:
        1. p_quote_series: dqproto.TimeSeries
        2. p_listed_date: dqproto.Date
        3. p_proxy_index: string
    @return:
        dqproto.InstrumentQuoteSeries
    '''
    try:
        tmp_this= InstrumentQuoteSeries()
        tmp_this.quote_series.CopyFrom(p_quote_series)
        tmp_this.listed_date.CopyFrom(p_listed_date)
        tmp_this.proxy_index=p_proxy_index
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#RunRiskFactorDataCleansingEngineInput
def dqCreateProtoRunRiskFactorDataCleansingEngineInput(p_settings, p_index_series, p_inst_quote_series, p_index_cleansed_return_manager_handle, p_inst_raw_return_manager_handle, p_inst_raw_return_series_handle, p_all_cleansed_return_series_handle):
    '''
    @args:
        1. p_settings: dqproto.RiskFactorDataCleansingSettings
        2. p_index_series: dqproto.TimeSeries
        3. p_inst_quote_series: dqproto.InstrumentQuoteSeries
        4. p_index_cleansed_return_manager_handle: string
        5. p_inst_raw_return_manager_handle: string
        6. p_inst_raw_return_series_handle: string
        7. p_all_cleansed_return_series_handle: string
    @return:
        dqproto.RunRiskFactorDataCleansingEngineInput
    '''
    try:
        tmp_this= RunRiskFactorDataCleansingEngineInput()
        tmp_this.settings.CopyFrom(p_settings)
        tmp_this.index_series.extend(p_index_series)
        tmp_this.inst_quote_series.extend(p_inst_quote_series)
        tmp_this.index_cleansed_return_manager_handle=p_index_cleansed_return_manager_handle
        tmp_this.inst_raw_return_manager_handle=p_inst_raw_return_manager_handle
        tmp_this.inst_raw_return_series_handle=p_inst_raw_return_series_handle
        tmp_this.all_cleansed_return_series_handle=p_all_cleansed_return_series_handle
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#RunRiskFactorDataCleansingEngineOutput
def dqCreateProtoRunRiskFactorDataCleansingEngineOutput(p_success):
    '''
    @args:
        1. p_success: bool
    @return:
        dqproto.RunRiskFactorDataCleansingEngineOutput
    '''
    try:
        tmp_this= RunRiskFactorDataCleansingEngineOutput()
        tmp_this.success=p_success
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#RunVarEngineInput
def dqCreateProtoRunVarEngineInput(p_settings, p_as_of_date, p_first_scn, p_last_scn, p_trade_file_name, p_trade_file_location):
    '''
    @args:
        1. p_settings: dqproto.MarketRiskMeasureSettings
        2. p_as_of_date: dqproto.Date
        3. p_first_scn: int32
        4. p_last_scn: int32
        5. p_trade_file_name: string
        6. p_trade_file_location: string
    @return:
        dqproto.RunVarEngineInput
    '''
    try:
        tmp_this= RunVarEngineInput()
        tmp_this.settings.CopyFrom(p_settings)
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.first_scn=p_first_scn
        tmp_this.last_scn=p_last_scn
        tmp_this.trade_file_name=p_trade_file_name
        tmp_this.trade_file_location=p_trade_file_location
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#RunVarEngineOutput
def dqCreateProtoRunVarEngineOutput(p_finished):
    '''
    @args:
        1. p_finished: bool
    @return:
        dqproto.RunVarEngineOutput
    '''
    try:
        tmp_this= RunVarEngineOutput()
        tmp_this.finished=p_finished
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#UpdateFhsScenariosInput
def dqCreateProtoUpdateFhsScenariosInput(p_scenarios, p_inst_stat_series, p_ewma_decay_factor, p_smoothing_weight, p_vol_floor, p_vol_cap, p_zero_return_handling, p_aod):
    '''
    @args:
        1. p_scenarios: dqproto.Scenario
        2. p_inst_stat_series: dqproto.InstrumentStatisticsSeries
        3. p_ewma_decay_factor: double
        4. p_smoothing_weight: double
        5. p_vol_floor: double
        6. p_vol_cap: double
        7. p_zero_return_handling: dqproto.ZeroReturnHandlingMethod
        8. p_aod: int32
    @return:
        dqproto.UpdateFhsScenariosInput
    '''
    try:
        tmp_this= UpdateFhsScenariosInput()
        tmp_this.scenarios.CopyFrom(p_scenarios)
        tmp_this.inst_stat_series.CopyFrom(p_inst_stat_series)
        tmp_this.ewma_decay_factor=p_ewma_decay_factor
        tmp_this.smoothing_weight=p_smoothing_weight
        tmp_this.vol_floor=p_vol_floor
        tmp_this.vol_cap=p_vol_cap
        tmp_this.zero_return_handling=p_zero_return_handling
        tmp_this.aod=p_aod
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#UpdateFhsScenariosOutput
def dqCreateProtoUpdateFhsScenariosOutput(p_scenarios):
    '''
    @args:
        1. p_scenarios: dqproto.Scenario
    @return:
        dqproto.UpdateFhsScenariosOutput
    '''
    try:
        tmp_this= UpdateFhsScenariosOutput()
        tmp_this.scenarios.CopyFrom(p_scenarios)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#UpdateInstrumentStatisticsInput
def dqCreateProtoUpdateInstrumentStatisticsInput(p_inst_price_series, p_as_of_date, p_use_fallback, p_fallback_indicator, p_vol_multiplier, p_inst_listed_date, p_proxy_inst_stat_series, p_zero_return_handling, p_return_type):
    '''
    @args:
        1. p_inst_price_series: dqproto.TimeSeries
        2. p_as_of_date: dqproto.Date
        3. p_use_fallback: bool
        4. p_fallback_indicator: int32
        5. p_vol_multiplier: double
        6. p_inst_listed_date: dqproto.Date
        7. p_proxy_inst_stat_series: dqproto.InstrumentStatisticsSeries
        8. p_zero_return_handling: dqproto.ZeroReturnHandlingMethod
        9. p_return_type: dqproto.RiskFactorChangeType
    @return:
        dqproto.UpdateInstrumentStatisticsInput
    '''
    try:
        tmp_this= UpdateInstrumentStatisticsInput()
        tmp_this.inst_price_series.CopyFrom(p_inst_price_series)
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.use_fallback=p_use_fallback
        tmp_this.fallback_indicator=p_fallback_indicator
        tmp_this.vol_multiplier=p_vol_multiplier
        tmp_this.inst_listed_date.CopyFrom(p_inst_listed_date)
        tmp_this.proxy_inst_stat_series.CopyFrom(p_proxy_inst_stat_series)
        tmp_this.zero_return_handling=p_zero_return_handling
        tmp_this.return_type=p_return_type
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#UpdateInstrumentStatisticsOutput
def dqCreateProtoUpdateInstrumentStatisticsOutput(p_inst_stat_series):
    '''
    @args:
        1. p_inst_stat_series: dqproto.InstrumentStatisticsSeries
    @return:
        dqproto.UpdateInstrumentStatisticsOutput
    '''
    try:
        tmp_this= UpdateInstrumentStatisticsOutput()
        tmp_this.inst_stat_series.CopyFrom(p_inst_stat_series)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#UpdateStressScenariosInput
def dqCreateProtoUpdateStressScenariosInput(p_scenarios, p_inst_stat_series, p_benchmark_stat_series, p_current_stress_dates, p_stress_day_lag, p_aod):
    '''
    @args:
        1. p_scenarios: dqproto.Scenario
        2. p_inst_stat_series: dqproto.InstrumentStatisticsSeries
        3. p_benchmark_stat_series: dqproto.InstrumentStatisticsSeries
        4. p_current_stress_dates: dqproto.Date
        5. p_stress_day_lag: int32
        6. p_aod: int32
    @return:
        dqproto.UpdateStressScenariosInput
    '''
    try:
        tmp_this= UpdateStressScenariosInput()
        tmp_this.scenarios.CopyFrom(p_scenarios)
        tmp_this.inst_stat_series.CopyFrom(p_inst_stat_series)
        tmp_this.benchmark_stat_series.extend(p_benchmark_stat_series)
        tmp_this.current_stress_dates.extend(p_current_stress_dates)
        tmp_this.stress_day_lag=p_stress_day_lag
        tmp_this.aod=p_aod
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#UpdateStressScenariosOutput
def dqCreateProtoUpdateStressScenariosOutput(p_scenarios):
    '''
    @args:
        1. p_scenarios: dqproto.Scenario
    @return:
        dqproto.UpdateStressScenariosOutput
    '''
    try:
        tmp_this= UpdateStressScenariosOutput()
        tmp_this.scenarios.CopyFrom(p_scenarios)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#VarEngineInput
def dqCreateProtoVarEngineInput(p_as_of_date, p_start_scenario, p_end_scenario, p_risk_factor_file_name, p_risk_factor_location, p_trade_location):
    '''
    @args:
        1. p_as_of_date: dqproto.Date
        2. p_start_scenario: int32
        3. p_end_scenario: int32
        4. p_risk_factor_file_name: string
        5. p_risk_factor_location: string
        6. p_trade_location: string
    @return:
        dqproto.VarEngineInput
    '''
    try:
        tmp_this= VarEngineInput()
        tmp_this.as_of_date.CopyFrom(p_as_of_date)
        tmp_this.start_scenario=p_start_scenario
        tmp_this.end_scenario=p_end_scenario
        tmp_this.risk_factor_file_name=p_risk_factor_file_name
        tmp_this.risk_factor_location=p_risk_factor_location
        tmp_this.trade_location=p_trade_location
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#VarEngineOutput
def dqCreateProtoVarEngineOutput(p_status):
    '''
    @args:
        1. p_status: string
    @return:
        dqproto.VarEngineOutput
    '''
    try:
        tmp_this= VarEngineOutput()
        tmp_this.status=p_status
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateFxSpotRateInput
def dqCreateProtoCreateFxSpotRateInput(p_reference_date, p_spot_date, p_value, p_currency_pair):
    '''
    @args:
        1. p_reference_date: dqproto.Date
        2. p_spot_date: dqproto.Date
        3. p_value: double
        4. p_currency_pair: dqproto.CurrencyPair
    @return:
        dqproto.CreateFxSpotRateInput
    '''
    try:
        tmp_this= CreateFxSpotRateInput()
        tmp_this.reference_date.CopyFrom(p_reference_date)
        tmp_this.spot_date.CopyFrom(p_spot_date)
        tmp_this.value=p_value
        tmp_this.currency_pair.CopyFrom(p_currency_pair)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateFxSpotRateOutput
def dqCreateProtoCreateFxSpotRateOutput(p_fx_spot_rate, p_success, p_err_msg):
    '''
    @args:
        1. p_fx_spot_rate: dqproto.FxSpotRate
        2. p_success: bool
        3. p_err_msg: string
    @return:
        dqproto.CreateFxSpotRateOutput
    '''
    try:
        tmp_this= CreateFxSpotRateOutput()
        tmp_this.fx_spot_rate.CopyFrom(p_fx_spot_rate)
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Vector
def dqCreateProtoVector(p_data):
    '''
    @args:
        1. p_data: double
    @return:
        dqproto.Vector
    '''
    try:
        tmp_this= Vector()
        tmp_this.data.extend(p_data)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Matrix
def dqCreateProtoMatrix(p_rows, p_cols, p_data, p_storage_order):
    '''
    @args:
        1. p_rows: int32
        2. p_cols: int32
        3. p_data: double
        4. p_storage_order: dqproto.StorageOrder
    @return:
        dqproto.Matrix
    '''
    try:
        tmp_this= Matrix()
        tmp_this.rows=p_rows
        tmp_this.cols=p_cols
        tmp_this.data.extend(p_data)
        tmp_this.storage_order=p_storage_order
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Interpolator1D
def dqCreateProtoInterpolator1D(p_interp_method, p_extrap_method, p_size, p_abscissas, p_ordinates, p_model_params, p_auxiliary_params):
    '''
    @args:
        1. p_interp_method: dqproto.InterpMethod
        2. p_extrap_method: dqproto.ExtrapMethod
        3. p_size: int32
        4. p_abscissas: dqproto.Vector
        5. p_ordinates: dqproto.Vector
        6. p_model_params: dqproto.Vector
        7. p_auxiliary_params: dqproto.Vector
    @return:
        dqproto.Interpolator1D
    '''
    try:
        tmp_this= Interpolator1D()
        tmp_this.interp_method=p_interp_method
        tmp_this.extrap_method=p_extrap_method
        tmp_this.size=p_size
        tmp_this.abscissas.CopyFrom(p_abscissas)
        tmp_this.ordinates.CopyFrom(p_ordinates)
        tmp_this.model_params.CopyFrom(p_model_params)
        tmp_this.auxiliary_params.CopyFrom(p_auxiliary_params)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#Interpolator2D
def dqCreateProtoInterpolator2D(p_x_interp_method, p_y_interp_method, p_x_extrap_method, p_y_extrap_method, p_y_abscissas, p_x_interpolators):
    '''
    @args:
        1. p_x_interp_method: dqproto.InterpMethod
        2. p_y_interp_method: dqproto.InterpMethod
        3. p_x_extrap_method: dqproto.ExtrapMethod
        4. p_y_extrap_method: dqproto.ExtrapMethod
        5. p_y_abscissas: dqproto.Vector
        6. p_x_interpolators: dqproto.Interpolator1D
    @return:
        dqproto.Interpolator2D
    '''
    try:
        tmp_this= Interpolator2D()
        tmp_this.x_interp_method=p_x_interp_method
        tmp_this.y_interp_method=p_y_interp_method
        tmp_this.x_extrap_method=p_x_extrap_method
        tmp_this.y_extrap_method=p_y_extrap_method
        tmp_this.y_abscissas.CopyFrom(p_y_abscissas)
        tmp_this.x_interpolators.extend(p_x_interpolators)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#BiLinearInterpolator
def dqCreateProtoBiLinearInterpolator(p_interpolator):
    '''
    @args:
        1. p_interpolator: dqproto.Interpolator2D
    @return:
        dqproto.BiLinearInterpolator
    '''
    try:
        tmp_this= BiLinearInterpolator()
        tmp_this.interpolator.CopyFrom(p_interpolator)
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateStaticDataInput
def dqCreateProtoCreateStaticDataInput(p_static_data_type, p_static_data):
    '''
    @args:
        1. p_static_data_type: dqproto.StaticDataType
        2. p_static_data: bytes
    @return:
        dqproto.CreateStaticDataInput
    '''
    try:
        tmp_this= CreateStaticDataInput()
        tmp_this.static_data_type=p_static_data_type
        tmp_this.static_data=p_static_data
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

#CreateStaticDataOutput
def dqCreateProtoCreateStaticDataOutput(p_success, p_err_msg):
    '''
    @args:
        1. p_success: bool
        2. p_err_msg: string
    @return:
        dqproto.CreateStaticDataOutput
    '''
    try:
        tmp_this= CreateStaticDataOutput()
        tmp_this.success=p_success
        tmp_this.err_msg=p_err_msg
        return tmp_this
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

