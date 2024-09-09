from enum import Enum


class Asset(Enum):
    ACTIVE = 'A'
    ACTIVE_HIGH = 'AH'
    ACTIVE_LOW = 'AL'
    FROZEN = 'F'
    FROZEN_LOW = 'FL'
    FROZEN_HIGH = 'FH'
    DELETED = 'D'


class Risk(Enum):
    EXPOSURE = 'E'

    TRIAGE = 'T'
    TRIAGE_INFO = 'TI'
    TRIAGE_LOW = 'TL'
    TRIAGE_MEDIUM = 'TM'
    TRIAGE_HIGH = 'TH'
    TRIAGE_CRITICAL = 'TC'

    OPEN = 'O'
    OPEN_INFO = 'OI'
    OPEN_LOW = 'OL'
    OPEN_MEDIUM = 'OM'
    OPEN_HIGH = 'OH'
    OPEN_CRITICAL = 'OC'

    REMEDIATED = 'R'
    REMEDIATED_INFO = 'RI'
    REMEDIATED_LOW = 'RL'
    REMEDIATED_MEDIUM = 'RM'
    REMEDIATED_HIGH = 'RH'
    REMEDIATED_CRITICAL = 'RC'

    MACHINE_OPEN = 'MO'
    MACHINE_OPEN_INFO = 'MOI'
    MACHINE_OPEN_LOW = 'MOL'
    MACHINE_OPEN_MEDIUM = 'MOM'
    MACHINE_OPEN_HIGH = 'MOH'
    MACHINE_OPEN_CRITICAL = 'MOC'

    DELETED = 'D'
    MACHINE_DELETED = 'MD'
    MACHINE_DELETED_INFO = 'MDI'
    MACHINE_DELETED_LOW = 'MDL'
    MACHINE_DELETED_MEDIUM = 'MDM'
    MACHINE_DELETED_HIGH = 'MDH'
    MACHINE_DELETED_CRITICAL = 'MDC'


class AddRisk(Enum):
    """ AddRisk is a subset of Risk. These are the only valid statuses when creating manual risks """
    TRIAGE_INFO = 'TI'
    TRIAGE_LOW = 'TL'
    TRIAGE_MEDIUM = 'TM'
    TRIAGE_HIGH = 'TH'
    TRIAGE_CRITICAL = 'TC'
