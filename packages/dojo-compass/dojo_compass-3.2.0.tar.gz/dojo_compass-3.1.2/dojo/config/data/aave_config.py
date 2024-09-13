"""Aave configuration data."""
from dataclasses import dataclass

aave_supported_tokens = ["USDC", "WBTC", "USDT", "DAI", "WETH", "UNI", "BAL"]


@dataclass
class _RateStrategy:
    name: str
    optimalUsageRatio: int
    baseVariableBorrowRate: int
    variableRateSlope1: int
    variableRateSlope2: int
    stableRateSlope1: int
    stableRateSlope2: int
    baseStableRateOffset: int
    stableRateExcessOffset: int
    optimalStableToTotalDebtRatio: int


@dataclass
class _Strategy:
    rateStrategy: _RateStrategy
    baseLTVAsCollateral: int
    liquidationThreshold: int
    liquidationBonus: int
    liquidationProtocolFee: int
    borrowingEnabled: bool
    stableBorrowRateEnabled: bool
    flashLoanEnabled: bool
    reserveDecimals: int
    aTokenImpl: str
    reserveFactor: int
    supplyCap: int
    borrowCap: int
    debtCeiling: int
    borrowableIsolation: bool


@dataclass
class _Reserve:
    DAI: _Strategy
    USDC: _Strategy
    WBTC: _Strategy
    WETH: _Strategy
    USDT: _Strategy
    UNI: _Strategy
    BAL: _Strategy


rateStrategyVolatileOne: _RateStrategy = _RateStrategy(
    name="rateStrategyVolatileOne",
    optimalUsageRatio=int(float(0.45) * (10**27)),
    baseVariableBorrowRate=0,
    variableRateSlope1=int(float(0.07) * (10**27)),
    variableRateSlope2=int(float(3) * (10**27)),
    stableRateSlope1=int(float(0.07) * (10**27)),
    stableRateSlope2=int(float(3) * (10**27)),
    baseStableRateOffset=int(float(0.02) * (10**27)),
    stableRateExcessOffset=int(float(0.05) * (10**27)),
    optimalStableToTotalDebtRatio=int(float(0.2) * (10**27)),
)

rateStrategyStableOne: _RateStrategy = _RateStrategy(
    name="rateStrategyStableOne",
    optimalUsageRatio=int(float(0.9) * (10**27)),
    baseVariableBorrowRate=0,
    variableRateSlope1=int(float(0.04) * (10**27)),
    variableRateSlope2=int(float(0.6) * (10**27)),
    stableRateSlope1=int(float(0.005) * (10**27)),
    stableRateSlope2=int(float(0.6) * (10**27)),
    baseStableRateOffset=int(float(0.01) * (10**27)),
    stableRateExcessOffset=int(float(0.08) * (10**27)),
    optimalStableToTotalDebtRatio=int(float(0.2) * (10**27)),
)

rateStrategyStableTwo: _RateStrategy = _RateStrategy(
    name="rateStrategyStableTwo",
    optimalUsageRatio=int(float(0.8) * (10**27)),
    baseVariableBorrowRate=0,
    variableRateSlope1=int(float(0.04) * (10**27)),
    variableRateSlope2=int(float(0.75) * (10**27)),
    stableRateSlope1=int(float(0.005) * (10**27)),
    stableRateSlope2=int(float(0.75) * (10**27)),
    baseStableRateOffset=int(float(0.01) * (10**27)),
    stableRateExcessOffset=int(float(0.08) * (10**27)),
    optimalStableToTotalDebtRatio=int(float(0.2) * (10**27)),
)

strategyDAI: _Strategy = _Strategy(
    rateStrategy=rateStrategyStableTwo,
    baseLTVAsCollateral=7500,
    liquidationThreshold=8000,
    liquidationBonus=10500,
    liquidationProtocolFee=1000,
    borrowingEnabled=True,
    stableBorrowRateEnabled=True,
    flashLoanEnabled=True,
    reserveDecimals=18,
    aTokenImpl="AToken",
    reserveFactor=1000,
    supplyCap=2000000000,
    borrowCap=0,
    debtCeiling=0,
    borrowableIsolation=True,
)

strategyUSDC: _Strategy = _Strategy(
    rateStrategy=rateStrategyStableOne,
    baseLTVAsCollateral=8000,
    liquidationThreshold=8500,
    liquidationBonus=10500,
    liquidationProtocolFee=1000,
    borrowingEnabled=True,
    stableBorrowRateEnabled=True,
    flashLoanEnabled=True,
    reserveDecimals=6,
    aTokenImpl="AToken",
    reserveFactor=1000,
    supplyCap=2000000000,
    borrowCap=0,
    debtCeiling=0,
    borrowableIsolation=True,
)

strategyWETH: _Strategy = _Strategy(
    rateStrategy=rateStrategyVolatileOne,
    baseLTVAsCollateral=8000,
    liquidationThreshold=8250,
    liquidationBonus=10500,
    liquidationProtocolFee=1000,
    borrowingEnabled=True,
    stableBorrowRateEnabled=False,
    flashLoanEnabled=True,
    reserveDecimals=18,
    aTokenImpl="AToken",
    reserveFactor=1000,
    supplyCap=0,
    borrowCap=0,
    debtCeiling=0,
    borrowableIsolation=False,
)

strategyWBTC: _Strategy = _Strategy(
    rateStrategy=rateStrategyVolatileOne,
    baseLTVAsCollateral=7000,
    liquidationThreshold=7500,
    liquidationBonus=11000,
    liquidationProtocolFee=1000,
    borrowingEnabled=True,
    stableBorrowRateEnabled=False,
    flashLoanEnabled=True,
    reserveDecimals=8,
    aTokenImpl="AToken",
    reserveFactor=2000,
    supplyCap=0,
    borrowCap=0,
    debtCeiling=0,
    borrowableIsolation=False,
)

strategyUSDT: _Strategy = _Strategy(
    rateStrategy=rateStrategyStableOne,
    baseLTVAsCollateral=7500,
    liquidationThreshold=8000,
    liquidationBonus=10500,
    liquidationProtocolFee=1000,
    borrowingEnabled=True,
    stableBorrowRateEnabled=True,
    flashLoanEnabled=True,
    reserveDecimals=6,
    aTokenImpl="AToken",
    reserveFactor=1000,
    supplyCap=2000000000,
    borrowCap=0,
    debtCeiling=500000000,
    borrowableIsolation=True,
)

ReservesConfig: _Reserve = _Reserve(
    DAI=strategyDAI,
    USDC=strategyUSDC,
    WBTC=strategyWBTC,
    WETH=strategyWETH,
    USDT=strategyUSDT,
    UNI=strategyDAI,
    BAL=strategyDAI,
)
"""AAVEv3 error codes.

CALLER_NOT_POOL_ADMIN = '1'; // 'The caller of the function is not a pool admin'
CALLER_NOT_EMERGENCY_ADMIN = '2'; // 'The caller of the function is not an emergencyadmin'
CALLER_NOT_POOL_OR_EMERGENCY_ADMIN = '3'; // 'The caller of the function is not a pool oremergency admin'
CALLER_NOT_RISK_OR_POOL_ADMIN = '4'; // 'The caller of the function is not a risk or pooladmin'
CALLER_NOT_ASSET_LISTING_OR_POOL_ADMIN = '5'; // 'The caller of the function is not anasset listing or pool admin'
CALLER_NOT_BRIDGE = '6'; // 'The caller of the function is not a bridge'
ADDRESSES_PROVIDER_NOT_REGISTERED = '7'; // 'Pool addresses provider is not registered'
INVALID_ADDRESSES_PROVIDER_ID = '8'; // 'Invalid id for the pool addresses provider'
NOT_CONTRACT = '9'; // 'Address is not a contract'
CALLER_NOT_POOL_CONFIGURATOR = '10'; // 'The caller of the function is not the poolconfigurator'
CALLER_NOT_ATOKEN = '11'; // 'The caller of the function is not an AToken'
INVALID_ADDRESSES_PROVIDER = '12'; // 'The address of the pool addresses provider isinvalid'
INVALID_FLASHLOAN_EXECUTOR_RETURN = '13'; // 'Invalid return value of the flashloanexecutor function'
RESERVE_ALREADY_ADDED = '14'; // 'Reserve has already been added to reserve list'
NO_MORE_RESERVES_ALLOWED = '15'; // 'Maximum amount of reserves in the pool reached'
EMODE_CATEGORY_RESERVED = '16'; // 'Zero eMode category is reserved for volatileheterogeneous assets'
INVALID_EMODE_CATEGORY_ASSIGNMENT = '17'; // 'Invalid eMode category assignment to asset'
RESERVE_LIQUIDITY_NOT_ZERO = '18'; // 'The liquidity of the reserve needs to be 0'
FLASHLOAN_PREMIUM_INVALID = '19'; // 'Invalid flashloan premium'
INVALID_RESERVE_PARAMS = '20'; // 'Invalid risk parameters for the reserve'
INVALID_EMODE_CATEGORY_PARAMS = '21'; // 'Invalid risk parameters for the eMode category'
BRIDGE_PROTOCOL_FEE_INVALID = '22'; // 'Invalid bridge protocol fee'
CALLER_MUST_BE_POOL = '23'; // 'The caller of this function must be a pool'
INVALID_MINT_AMOUNT = '24'; // 'Invalid amount to mint'
INVALID_BURN_AMOUNT = '25'; // 'Invalid amount to burn'
INVALID_AMOUNT = '26'; // 'Amount must be greater than 0'
RESERVE_INACTIVE = '27'; // 'Action requires an active reserve'
RESERVE_FROZEN = '28'; // 'Action cannot be performed because the reserve is frozen'
RESERVE_PAUSED = '29'; // 'Action cannot be performed because the reserve is paused'
BORROWING_NOT_ENABLED = '30'; // 'Borrowing is not enabled'
STABLE_BORROWING_NOT_ENABLED = '31'; // 'Stable borrowing is not enabled'
NOT_ENOUGH_AVAILABLE_USER_BALANCE = '32'; // 'User cannot withdraw more than theavailable balance'
INVALID_INTEREST_RATE_MODE_SELECTED = '33'; // 'Invalid interest rate mode selected'
COLLATERAL_BALANCE_IS_ZERO = '34'; // 'The collateral balance is 0'
HEALTH_FACTOR_LOWER_THAN_LIQUIDATION_THRESHOLD = '35'; // 'Health factor is lesser thanthe liquidation threshold'
COLLATERAL_CANNOT_COVER_NEW_BORROW = '36'; // 'There is not enough collateral to cover anew borrow'
COLLATERAL_SAME_AS_BORROWING_CURRENCY = '37'; // 'Collateral is (mostly) the samecurrency that is being borrowed'
AMOUNT_BIGGER_THAN_MAX_LOAN_SIZE_STABLE = '38'; // 'Requested amount greater than max loan size in stable rate mode'
NO_DEBT_OF_SELECTED_TYPE = '39'; // 'For repayment of a specific type of debt, the userneeds to have debt that type'
NO_EXPLICIT_AMOUNT_TO_REPAY_ON_BEHALF = '40'; // 'To repay on behalf of a user anexplicit amount to repay is needed'
NO_OUTSTANDING_STABLE_DEBT = '41'; // 'User does not have outstanding stable rate debt onthis reserve'
NO_OUTSTANDING_VARIABLE_DEBT = '42'; // 'User does not have outstanding variable ratedebt on this reserve'
UNDERLYING_BALANCE_ZERO = '43'; // 'The underlying balance needs to be greater than 0'
INTEREST_RATE_REBALANCE_CONDITIONS_NOT_MET = '44'; // 'Interest rate rebalance conditionswere not met'
HEALTH_FACTOR_NOT_BELOW_THRESHOLD = '45'; // 'Health factor is not below the threshold'
COLLATERAL_CANNOT_BE_LIQUIDATED = '46'; // 'The collateral chosen cannot be liquidated'
SPECIFIED_CURRENCY_NOT_BORROWED_BY_USER = '47'; // 'User did not borrow the specifiedcurrency'
SAME_BLOCK_BORROW_REPAY = '48'; // 'Borrow and repay in same block is not allowed'
INCONSISTENT_FLASHLOAN_PARAMS = '49'; // 'Inconsistent flashloan parameters'
BORROW_CAP_EXCEEDED = '50'; // 'Borrow cap is exceeded'
SUPPLY_CAP_EXCEEDED = '51'; // 'Supply cap is exceeded'
UNBACKED_MINT_CAP_EXCEEDED = '52'; // 'Unbacked mint cap is exceeded'
DEBT_CEILING_EXCEEDED = '53'; // 'Debt ceiling is exceeded'
ATOKEN_SUPPLY_NOT_ZERO = '54'; // 'AToken supply is not zero'
STABLE_DEBT_NOT_ZERO = '55'; // 'Stable debt supply is not zero'
VARIABLE_DEBT_SUPPLY_NOT_ZERO = '56'; // 'Variable debt supply is not zero'
LTV_VALIDATION_FAILED = '57'; // 'Ltv validation failed'
INCONSISTENT_EMODE_CATEGORY = '58'; // 'Inconsistent eMode category'
PRICE_ORACLE_SENTINEL_CHECK_FAILED = '59'; // 'Price oracle sentinel validation failed'
ASSET_NOT_BORROWABLE_IN_ISOLATION = '60'; // 'Asset is not borrowable in isolation mode'
RESERVE_ALREADY_INITIALIZED = '61'; // 'Reserve has already been initialized'
USER_IN_ISOLATION_MODE = '62'; // 'User is in isolation mode'
INVALID_LTV = '63'; // 'Invalid ltv parameter for the reserve'
INVALID_LIQ_THRESHOLD = '64'; // 'Invalid liquidity threshold parameter for the reserve'
INVALID_LIQ_BONUS = '65'; // 'Invalid liquidity bonus parameter for the reserve'
INVALID_DECIMALS = '66'; // 'Invalid decimals parameter of the underlying asset of thereserve'
INVALID_RESERVE_FACTOR = '67'; // 'Invalid reserve factor parameter for the reserve'
INVALID_BORROW_CAP = '68'; // 'Invalid borrow cap for the reserve'
INVALID_SUPPLY_CAP = '69'; // 'Invalid supply cap for the reserve'
INVALID_LIQUIDATION_PROTOCOL_FEE = '70'; // 'Invalid liquidation protocol fee for thereserve'
INVALID_EMODE_CATEGORY = '71'; // 'Invalid eMode category for the reserve'
INVALID_UNBACKED_MINT_CAP = '72'; // 'Invalid unbacked mint cap for the reserve'
INVALID_DEBT_CEILING = '73'; // 'Invalid debt ceiling for the reserve
INVALID_RESERVE_INDEX = '74'; // 'Invalid reserve index'
ACL_ADMIN_CANNOT_BE_ZERO = '75'; // 'ACL admin cannot be set to the zero address'
INCONSISTENT_PARAMS_LENGTH = '76'; // 'Array parameters that should be equal length arenot'
ZERO_ADDRESS_NOT_VALID = '77'; // 'Zero address not valid'
INVALID_EXPIRATION = '78'; // 'Invalid expiration'
INVALID_SIGNATURE = '79'; // 'Invalid signature'
OPERATION_NOT_SUPPORTED = '80'; // 'Operation not supported'
DEBT_CEILING_NOT_ZERO = '81'; // 'Debt ceiling is not zero'
ASSET_NOT_LISTED = '82'; // 'Asset is not listed'
INVALID_OPTIMAL_USAGE_RATIO = '83'; // 'Invalid optimal usage ratio'
INVALID_OPTIMAL_STABLE_TO_TOTAL_DEBT_RATIO = '84'; // 'Invalid optimal stable to totaldebt ratio'
UNDERLYING_CANNOT_BE_RESCUED = '85'; // 'The underlying asset cannot be rescued'
ADDRESSES_PROVIDER_ALREADY_ADDED = '86'; // 'Reserve has already been added to reservelist'
POOL_ADDRESSES_DO_NOT_MATCH = '87'; // 'The token implementation pool address and thepool do not match'
STABLE_BORROWING_ENABLED = '88'; // 'Stable borrowing is enabled'
SILOED_BORROWING_VIOLATION = '89'; // 'User is trying to borrow multiple assets includinga siloed one'
RESERVE_DEBT_NOT_ZERO = '90'; // the total debt of the reserve needs to be 0
"""
