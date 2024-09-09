# -*- coding: utf-8 -*-
import logging
import sys
from enum import Enum
from typing import Any, Dict, Optional

import pydantic
from pydantic import BaseModel, Field, validator


class OmitEnum(Enum):
    """TODO: Insert docstring for this OmitEnum class."""

    FALSE = "false"
    TRUE = "true"


class TargetNameEnum(Enum):
    """TODO: Insert docstring for this TargetNameEnum class."""

    FBN1 = "FBN1"


class TaskEnum(Enum):
    """TODO: Insert docstring for this TaskEnum class."""

    UNKNOWN = "UNKNOWN"
    STANDARD = "STANDARD"


class ReporterEnum(Enum):
    """TODO: Insert docstring for this ReporterEnum class."""

    FAM = "FAM"


class QuencherEnum(Enum):
    """TODO: Insert docstring for this QuencherEnum class."""

    NFQMGB = "NFQ-MGB"


class QuantityMeanEnum(Enum):
    """TODO: Insert docstring for this QuantityMeanEnum class."""

    QUANTITYMEAN_0_000 = "0.000"
    QUANTITYMEAN_0_128 = "0.128"
    QUANTITYMEAN_0_179 = "0.179"
    QUANTITYMEAN_0_002 = "0.002"
    QUANTITYMEAN_0_141 = "0.141"
    QUANTITYMEAN_0_159 = "0.159"
    QUANTITYMEAN_0_005 = "0.005"
    QUANTITYMEAN_0_123 = "0.123"
    QUANTITYMEAN_0_166 = "0.166"
    QUANTITYMEAN_0_003 = "0.003"
    QUANTITYMEAN_0_001 = "0.001"
    QUANTITYMEAN_0_244 = "0.244"
    QUANTITYMEAN_0_418 = "0.418"


class QuantitySdEnum(Enum):
    """TODO: Insert docstring for this QuantitySdEnum class."""

    QUANTITYSD_0_005 = "0.005"
    QUANTITYSD_0_004 = "0.004"
    QUANTITYSD_0_000 = "0.000"
    QUANTITYSD_0_006 = "0.006"
    QUANTITYSD_0_001 = "0.001"
    QUANTITYSD_0_017 = "0.017"


class YinterceptEnum(Enum):
    """TODO: Insert docstring for this Y-interceptEnum class."""

    Y_INTERCEPT_24_508 = "24.508"


class RSuperscript2Enum(Enum):
    """TODO: Insert docstring for this RSuperscript2Enum class."""

    RSUPERSCRIPT2_0_978 = "0.978"


class SlopeEnum(Enum):
    """TODO: Insert docstring for this SlopeEnum class."""

    SLOPE3612 = "-3.612"


class EfficiencyEnum(Enum):
    """TODO: Insert docstring for this EfficiencyEnum class."""

    EFFICIENCY_89_154 = "89.154"


class AutomaticCtThresholdEnum(Enum):
    """TODO: Insert docstring for this AutomaticCtThresholdEnum class."""

    FALSE = "false"


class CtThresholdEnum(Enum):
    """TODO: Insert docstring for this CtThresholdEnum class."""

    CTTHRESHOLD_0_100 = "0.100"


class AutomaticBaselineEnum(Enum):
    """TODO: Insert docstring for this AutomaticBaselineEnum class."""

    TRUE = "true"


class BaselineStartEnum(Enum):
    """TODO: Insert docstring for this BaselineStartEnum class."""

    BASELINESTART_3 = "3"


class BaselineEndEnum(Enum):
    """TODO: Insert docstring for this BaselineEndEnum class."""

    BASELINEEND_40 = "40"
    BASELINEEND_33 = "33"
    BASELINEEND_24 = "24"
    BASELINEEND_23 = "23"
    BASELINEEND_31 = "31"
    BASELINEEND_20 = "20"
    BASELINEEND_34 = "34"
    BASELINEEND_30 = "30"
    BASELINEEND_29 = "29"
    BASELINEEND_25 = "25"
    BASELINEEND_26 = "26"
    BASELINEEND_27 = "27"
    BASELINEEND_28 = "28"
    BASELINEEND_35 = "35"
    BASELINEEND_32 = "32"
    BASELINEEND_36 = "36"
    BASELINEEND_22 = "22"


class AmpStatusEnum(Enum):
    """TODO: Insert docstring for this AmpStatusEnum class."""

    NOAMP = "No Amp"
    AMP = "Amp"
    INCONCLUSIVE = "Inconclusive"


class CommentsEnum(Enum):
    """TODO: Insert docstring for this CommentsEnum class."""


class HighsdEnum(Enum):
    """TODO: Insert docstring for this HighsdEnum class."""

    HIGHSD_N = "N"
    HIGHSD_Y = "Y"


class NoampEnum(Enum):
    """TODO: Insert docstring for this NoampEnum class."""

    NOAMP_Y = "Y"
    NOAMP_N = "N"


class CqConfEnum(Enum):
    """TODO: Insert docstring for this CqConfEnum class."""

    CQCONF_Y = "Y"
    CQCONF_N = "N"


class ExpfailEnum(Enum):
    """TODO: Insert docstring for this ExpfailEnum class."""

    EXPFAIL_Y = "Y"
    EXPFAIL_N = "N"


class InvalidWellError(Exception):
    """TODO: insert docstring for this InvalidWellError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidWellError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidWellPositionError(Exception):
    """TODO: insert docstring for this InvalidWellPositionError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidWellPositionError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidOmitError(Exception):
    """TODO: insert docstring for this InvalidOmitError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidOmitError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidSampleNameError(Exception):
    """TODO: insert docstring for this InvalidSampleNameError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidSampleNameError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidTargetNameError(Exception):
    """TODO: insert docstring for this InvalidTargetNameError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidTargetNameError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidTaskError(Exception):
    """TODO: insert docstring for this InvalidTaskError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidTaskError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidReporterError(Exception):
    """TODO: insert docstring for this InvalidReporterError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidReporterError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidQuencherError(Exception):
    """TODO: insert docstring for this InvalidQuencherError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidQuencherError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidCtError(Exception):
    """TODO: insert docstring for this InvalidCtError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidCtError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidCtMeanError(Exception):
    """TODO: insert docstring for this InvalidCtMeanError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidCtMeanError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidCtSdError(Exception):
    """TODO: insert docstring for this InvalidCtSdError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidCtSdError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidQuantityError(Exception):
    """TODO: insert docstring for this InvalidQuantityError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidQuantityError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidQuantityMeanError(Exception):
    """TODO: insert docstring for this InvalidQuantityMeanError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidQuantityMeanError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidQuantitySdError(Exception):
    """TODO: insert docstring for this InvalidQuantitySdError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidQuantitySdError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidYinterceptError(Exception):
    """TODO: insert docstring for this InvalidYinterceptError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidYinterceptError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidRSuperscript2Error(Exception):
    """TODO: insert docstring for this InvalidRSuperscript2Error class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidRSuperscript2Error class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidSlopeError(Exception):
    """TODO: insert docstring for this InvalidSlopeError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidSlopeError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidEfficiencyError(Exception):
    """TODO: insert docstring for this InvalidEfficiencyError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidEfficiencyError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidAutomaticCtThresholdError(Exception):
    """TODO: insert docstring for this InvalidAutomaticCtThresholdError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidAutomaticCtThresholdError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidCtThresholdError(Exception):
    """TODO: insert docstring for this InvalidCtThresholdError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidCtThresholdError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidAutomaticBaselineError(Exception):
    """TODO: insert docstring for this InvalidAutomaticBaselineError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidAutomaticBaselineError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidBaselineStartError(Exception):
    """TODO: insert docstring for this InvalidBaselineStartError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidBaselineStartError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidBaselineEndError(Exception):
    """TODO: insert docstring for this InvalidBaselineEndError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidBaselineEndError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidAmpStatusError(Exception):
    """TODO: insert docstring for this InvalidAmpStatusError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidAmpStatusError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidCommentsError(Exception):
    """TODO: insert docstring for this InvalidCommentsError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidCommentsError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidCqConfError(Exception):
    """TODO: insert docstring for this InvalidCqConfError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidCqConfError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidHighsdError(Exception):
    """TODO: insert docstring for this InvalidHighsdError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidHighsdError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidNoampError(Exception):
    """TODO: insert docstring for this InvalidNoampError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidNoampError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class InvalidExpfailError(Exception):
    """TODO: insert docstring for this InvalidExpfailError class."""

    def __init__(self, value: str, message: str) -> None:
        """Class constructor for InvalidExpfailError class."""
        self.value = value
        self.message = message
        super().__init__(message)


class Record(BaseModel):
    """Class for encapsulating the rows in SampleRun files."""

    well: int = Field(
        ...,  # Indicates this is a required field
        example=["1", "2", "3", "4"],
        description="TBD",
        frozen=True,
        ge=1,
        le=96,
        alias="Well",
    )

    wellposition: str = Field(
        ...,  # Indicates this is a required field
        example=["A1", "A2", "A3", "A4"],
        description="TBD",
        frozen=True,
        # min_length=2,
        # max_length=2,
        alias="Well Position",
    )

    samplename: Optional[str] = Field(
        # ...,  # Indicates this is a required field
        example=["624", "FLO1 3/14 - REP 1", "POS - REP 1", "3% - REP 3"],
        description="TBD",
        frozen=True,
        min_length=3,
        max_length=20,
        alias="Sample Name",
    )

    targetname: Optional[str] = Field(
        None,  # Indicates this is a required field
        example=["FBN1"],
        description="This is the target name.",
        frozen=True,
        min_length=3,
        max_length=5,
        alias="Target Name",
    )

    quantity: Optional[float] = Field(
        default=0.0,  # Sets default value
        example=["0.000", "0.133", "0.127", "0.123"],
        description="The quantity.",
        alias="Quantity",
    )

    # TODO: A value is required when the Task is UNKNOWN
    quantitymean: Optional[float] = Field(
        # ...,  # Indicates this is a required field
        None,
        example=["0.000", "0.128", "0.179", "0.002"],
        description="TBD",
        frozen=True,
        alias="Quantity Mean",
    )

    # TODO: A value is required when the Task is UNKNOWN
    quantitysd: Optional[float] = Field(
        # ...,  # Indicates this is a required field
        None,
        example=["0.005", "0.004", "0.000", "0.006"],
        description="TBD",
        frozen=True,
        alias="Quantity SD",
    )

    yintercept: float = Field(
        ...,  # Indicates this is a required field
        example=["24.508"],
        description="TBD",
        frozen=True,
        alias="Y-Intercept",
    )

    rsuperscript2: float = Field(
        ...,  # Indicates this is a required field
        example=["0.978"],
        description="TBD",
        frozen=True,
        # ge=0.978,
        # le=0.978,
        alias="R(superscript 2)",
    )

    slope: float = Field(
        ...,  # Indicates this is a required field
        example=["-3.612"],
        description="TBD",
        frozen=True,
        alias="Slope",
    )

    efficiency: Optional[float] = Field(
        None,  # Indicates this is a required field
        example=["89.154"],
        description="TBD",
        frozen=True,
        alias="Efficiency",
    )

    ampstatus: str = Field(
        # ampstatus: AmpStatusEnum = Field(
        # ...,  # Indicates this is a required field
        example=["No Amp", "Amp", "Inconclusive"],
        description="The amplification status.",
        frozen=True,
        alias="Amp Status",
    )

    nmv: Optional[float] = Field(
        None,
        description="The normalized methylation value.",
        frozen=True,
    )

    @pydantic.root_validator(pre=True)
    def is_record_valid(cls, values) -> None:
        # #logging.info(f"In root validator with values '{values}'")
        # TODO: need to implement the root validator
        # raise InvalidRecordError(message="")
        return values

    @pydantic.validator("well")
    # @classmethod
    def is_well_valid(cls, value):
        """Validate value for Well column (column number 1)."""
        # #logging.info(f"In well validator with value '{value}'")
        if value:
            # TODO: implement validation here
            return value
        else:
            raise InvalidWellError(
                value=value, message="Well (in column number 1) should ...  TODO"
            )

    @pydantic.validator("wellposition")
    # @classmethod
    def is_wellposition_valid(cls, value):
        """Validate value for Well Position column (column number 2)."""
        # #logging.info(f"In wellposition validator with value '{value}'")
        if value:
            # TODO: implement validation here
            return value
        else:
            raise InvalidWellPositionError(
                value=value,
                message="Well Position (in column number 2) should ...  TODO",
            )

    @pydantic.validator(
        "samplename",
        always=True,
    )
    # @classmethod
    def is_samplename_valid(cls, value: Optional[str], values: Dict[str, Any]):
        """Validate value for Sample Name column (column number 4)."""
        # #logging.info(f"In samplename validator with value '{value}' and values '{values}'")
        if value is None or value == "":
            if "ct" not in values:
                logging.warning("ct not in values")
                return None

            if values["ct"] == "Undetermined":
                return value
            else:
                raise InvalidSampleNameError(
                    value=value,
                    message="Sample Name (in column number 4) should defined",
                )

        return value

    @pydantic.validator("quantity")
    # @classmethod
    def is_quantity_valid(cls, value: float, values):
        """Validate value for Quantity column (column number 12)."""
        # logging.info(f"In quantity validator with value '{value}'")
        if value is None or value == "":
            return None
        if value == 0 or value == 0.0 or value:
            # TODO: implement validation here
            return value
        else:
            print(f"{value=}")
            sys.exit(1)
            raise InvalidQuantityError(
                value=value,
                message=f"JS1 Encountered invalid quantity (in column number 12) with sample name '{values['samplename']}'",
            )

    # @classmethod
    @pydantic.validator("quantitymean", always=True, check_fields=True)
    def is_quantitymean_valid(cls, value, values):
        """Validate value for Quantity Mean column (column number 13)."""
        # logging.info(f"In quantitymean validator with value '{value}'")
        # logging.info(f"samplename: {values['samplename']}")
        # logging.info(f"values: {values}")

        if value is None or value == "":
            return None
            # if "samplename" not in values:
        #         logging.warning(f"samplename is not defined while checking Quantity Mean (in column number 13)")
        #         return None
        #         # raise Exception("samplename is not defined")
        #     if values["samplename"] in ("STD 1", "STD 2", "STD 3", "STD 4", "STD 5"):
        #         logging.info(f"samplename is '{values['samplename']}' while checking Quantity Mean (in column number 13)")
        #         return None
        #     else:
        #         raise InvalidQuantityMeanError(value=value, message=f"Quantity Mean (in column number 13) should defined")
        return value

    @pydantic.validator("yintercept")
    # @classmethod
    def is_yintercept_valid(cls, value):
        """Validate value for Y-Intercept column (column number 15)."""
        # logging.info(f"In yintercept validator with value '{value}'")
        if value:
            # TODO: implement validation here
            return value
        elif value == 24.508:
            return value
        else:
            raise InvalidYinterceptError(
                value=value,
                message="Y-Intercept (in column number 15) should ...  TODO",
            )

    @pydantic.validator("rsuperscript2")
    # @classmethod
    def is_rsuperscript2_valid(cls, value):
        """Validate value for R(superscript 2) column (column number 16)."""
        # logging.info(f"In rsuperscript2 validator with value '{value}'")
        if value:
            # TODO: implement validation here
            return value
        elif value == 0.978:
            return value
        else:
            raise InvalidRSuperscript2Error(
                value=value,
                message="R(superscript 2) (in column number 16) should ...  TODO",
            )

    @pydantic.validator("slope")
    # @classmethod
    def is_slope_valid(cls, value):
        """Validate value for Slope column (column number 17)."""
        # logging.info(f"In slope validator with value '{value}'")
        if value:
            # TODO: implement validation here
            return value
        elif value == -3.612:
            return value
        else:
            raise InvalidSlopeError(
                value=value, message="Slope (in column number 17) should ...  TODO"
            )

    @pydantic.validator("efficiency")
    # @classmethod
    def is_efficiency_valid(cls, value):
        """Validate value for Efficiency column (column number 18)."""
        # logging.info(f"In efficiency validator with value '{value}'")
        if value:
            # TODO: implement validation here
            return value
        elif value == 89.154:
            return value
        else:
            raise InvalidEfficiencyError(
                value=value,
                message="Efficiency (in column number 18) should ...  TODO",
            )

    @pydantic.validator("ampstatus")
    # @classmethod
    def is_ampstatus_valid(cls, value):
        """Validate value for Amp Status column (column number 24)."""
        # logging.info(f"In ampstatus validator with value '{value}'")
        if value:
            # TODO: implement validation here
            return value
        elif value == "No Amp":
            return value
        elif value == "Amp":
            return value
        elif value == "Inconclusive":
            return value
        else:
            raise InvalidAmpStatusError(
                value=value,
                message="Amp Status (in column number 24) should ...  TODO",
            )

    @validator("quantity", pre=True, always=True)
    def convert_quantity_empty_str_to_none(cls, v):
        return None if v == "" else v

    @validator("quantitymean", pre=True, always=True)
    def convert_quantitymean_empty_str_to_none(cls, v):
        return None if v == "" else v

    @validator("quantitysd", pre=True, always=True)
    def convert_quantitysd_empty_str_to_none(cls, v):
        return None if v == "" else v
