from dataclasses import dataclass, fields

from enum import Enum


class APIEnvironment(Enum):
    """
    At the moment the same Hyphen API is used for all environments. But leaving this here ready in case we ever
    need different API urls for different environments with Hyper API.
    """

    PRODUCTION = "https://internal-landlifecompany.appspot.com"
    STAGING = "https://staging-dot-internal-landlifecompany.ue.r.appspot.com"
    LOCAL = "http://127.0.0.1:8000"


@dataclass
class ApiUrls:
    # Authentication
    AUTH_URL: str = "/api/v1/token/"

    # Planting Design
    GET_PLANTING_DESIGN_DETAIL: str = "/plantingdesign/api/detail/"
    GET_PLANTING_DESIGN_LIST: str = "/plantingdesign/api/list"

    # Map Layers
    GET_MAP_LAYERS: str = "/rs_dashboard/map_layers"
    CREATE_MAP_LAYER_FROM_JOB: str = "/rs_dashboard/create_map_layer_from_map_job"
    UPDATE_MAP_LAYER_JOB_PROGRESS: str = "/rs_dashboard/update_map_layer_job_progress"

    # Calibrate
    GET_CALIBRATE_INPUT: str = "/sciencemodel/calibrateinput/"
    UPDATE_CALIBRATE_SCENARIO_PARAMETERS: str = (
        "/sciencemodel/fasttrackinput/calibrate_scenario_update_parameters"
    )

    COMPLETE_SCENARIO_CALIBRATION: str = (
        "/sciencemodel/fasttrackinput/complete_scenario_calibration"
    )
    GET_PLANTING_DESIGN_CALIBRATE_SCENARIOS: str = (
        "/sciencemodel/fasttrackinput/list_planting_design_calibrate_scenarios/"
    )
    GET_CALIBRATE_SCENARIO_SIBLINGS: str = (
        "/sciencemodel/fasttrackinput/list_siblings_calibrate_scenarios/"
    )

    # Density Analysis
    GET_DA_INPUT: str = "/sciencemodel/densityanalysisinput/"
    COMPLETE_DA_RUN: str = "/sciencemodel/fasttrackinput/complete_density_run"

    # FastTrack
    GET_FT_INPUT: str = "/sciencemodel/fasttrackinput/"
    COMPLETE_FASTTRACK_RUN: str = "/sciencemodel/fasttrackinput/complete_fasttrack_run"

    # Deprecated
    GET_MODEL_INPUT_FAST_TRACK: str = (
        "/sciencemodel/fasttrackinput/model_input_fast_track/"
    )
    GET_MODEL_INPUT_CALIBRATE_FAST_TRACK: str = (
        "/sciencemodel/fasttrackinput/model_input_calibrate_fast_track/"
    )
    GET_MODEL_INPUT_DENSITY_ANALYSES_FAST_TRACK: str = (
        "/sciencemodel/fasttrackinput/model_input_density_analyses_fast_track/"
    )

    # Cloud Calibrate
    GET_MODEL_INPUT_FOR_SCENARIO_CALIBRATE: str = (
        "/sciencemodel/fasttrackinput/model_input_for_scenario_calibrate/"
    )
    GET_CALIBRATE_SCENARIO_SETTINGS: str = (
        "/sciencemodel/fasttrackinput/calibrate_scenario_settings/"
    )
    GET_CALIBRATE_SCENARIO_NFI_FILTER: str = (
        "/sciencemodel/fasttrackinput/nfi_filter_for_calibrate_scenario/"
    )
    GET_CALIBRATE_SCENARIO_STATE_VARS: str = (
        "/sciencemodel/fasttrackinput/calibrate_scenario_state_vars/"
    )
    GET_CALIBRATE_SCENARIO_PARAMETERS: str = (
        "/sciencemodel/fasttrackinput/calibrate_scenario_get_parameters/"
    )

    # Cloud FT
    GET_FASTTRACK_RUN_SETTINGS: str = (
        "/sciencemodel/fasttrackinput/fasttrack_run_settings/"
    )

    # Cloud DA
    GET_DA_RUN_SETTINGS: str = "/sciencemodel/fasttrackinput/density_run_settings/"

    # LEGACY ENDPOINTS -----------
    GET_MODEL_INPUT_URL: str = "/sciencemodel/fasttrackinput/planting_design_config/"
    GET_OLD_MODEL_INPUT_URL: str = "/api/v1/llcmodel/model_input?model_run_ids"

    # NFI
    SAVE_NFI: str = "/sciencemodel/nfiinput/save_nfi"

    # Analyzer
    LLC_ANALYZER: str = "/rs_dashboard/llc_analyzer"

    @classmethod
    def create(cls, environment: str = "production"):
        """
        This method creates an instance of HyphenApiUrls and sets the base url. Right now it is set to always use
        production, but this can be changed here.
        environment: str: The environment to set the base url for. Should be lowercase string.
        """
        base_url = None

        if environment == "production":
            base_url = APIEnvironment.PRODUCTION.value
        elif environment == "staging":
            base_url = APIEnvironment.STAGING.value
        elif environment == "local":
            base_url = APIEnvironment.LOCAL.value
        else:
            base_url = environment

        instance = cls()

        for field in fields(instance):
            new_val = base_url + getattr(instance, field.name)
            setattr(instance, field.name, new_val)

        return instance
