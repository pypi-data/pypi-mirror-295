from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Union, List, Literal
from urllib.parse import urlencode

import requests
import os
import sys
import pandas as pd

from .api_types import (
    DetailedMapLayerResponse,
    SimplifiedMapLayerResponse,
    Geography,
    MapJobProgress,
)
from .exceptions import ApiAuthenticationError, ApiTokenError, ApiGeneralError
from .helpers import json_response_to_df
from .parameter_mapping import update_legacy_parameter
from .urls import ApiUrls

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


@dataclass
class ScienceSdk:
    auth_token: str = field(default_factory=str, repr=False)
    environment: str = "production"
    api_urls: ApiUrls = None

    def __post_init__(self):
        self.api_urls = ApiUrls.create(self.environment)

    def _get_request(self, url, parameters: Optional[dict] = ""):
        if not self.auth_token:
            raise ApiTokenError

        response = requests.get(
            f"{url}{'?' if parameters else ''}{urlencode(parameters)}",
            headers={"Authorization": f"Bearer {self.auth_token}"},
        )
        response.raise_for_status()
        return response.json()

    def _post_request(self, url, data=None, parameters: Optional[dict] = ""):
        if not self.auth_token:
            raise ApiTokenError

        response = requests.post(
            f"{url}{'?' if parameters else ''}{urlencode(parameters)}",
            headers={"Authorization": f"Bearer {self.auth_token}"},
            json=data,
        )
        response.raise_for_status()
        return response.json()

    def _put_request(self, url, data=None, parameters: Optional[dict] = ""):
        if not self.auth_token:
            raise ApiTokenError

        response = requests.put(
            f"{url}{'?' if parameters else ''}{urlencode(parameters)}",
            headers={"Authorization": f"Bearer {self.auth_token}"},
            json=data,
        )
        response.raise_for_status()
        return response.json()

    # LIST OF ENDPOINTS

    # Authentication
    def login(self, username: str, password: str):
        r = requests.post(
            self.api_urls.AUTH_URL, data={"username": username, "password": password}
        )

        if r.status_code == 401:
            raise ApiAuthenticationError(r.text)

        elif not r.ok:
            raise ApiGeneralError(r.text)

        self.auth_token = r.json()["access"]

    # Planting Design

    def get_planting_design_detail(self, planting_design_id: int) -> dict:
        return self._get_request(
            f"{self.api_urls.GET_PLANTING_DESIGN_DETAIL}{str(planting_design_id)}"
        )

    def get_planting_design_list(self) -> dict:
        return self._get_request(self.api_urls.GET_PLANTING_DESIGN_LIST)

    # Map Layers
    def get_map_layers(
        self,
        planting_design_id: Optional[int] = None,
        categories: Optional[List[str]] = None,
        data_format: Optional[str] = None,
        external_map_layer_id: Optional[str] = None,
        geography: Optional[Geography] = None,
        detailed: bool = False,
    ) -> Union[List[DetailedMapLayerResponse], List[SimplifiedMapLayerResponse]]:
        """
        Fetches map layers from the API

        Parameters
        ----------
            planting_design_id: int
                Returns map layers for the given planting design.
            categories: List[str]
                Returns map layers that have the given categories. Expects the IDs of the categories.
            data_format: str
                Format in which you would like the underlying map layer data to be returned. Raster or web.
            external_map_layer_id: str
                Get a single map layer by external id. May return multiple sources (raster, web) unless filtered.
            geography: Geography
                Geography of the map layers. Global map layers are not tied to a specific planting design.
            detailed: bool
                Whether to return detailed information about the map layers or a simplified format.
        """

        parameters = {
            "planting_design_id": planting_design_id,
            "categories": categories,
            "data_format": data_format,
            "external_map_layer_id": external_map_layer_id,
            "geography": geography,
            "detailed": detailed,
        }
        parameters = {k: v for k, v in parameters.items() if v is not None}

        return self._get_request(self.api_urls.GET_MAP_LAYERS, parameters)

    def create_map_layer_from_job(self, map_layer_job_id: int):
        """
        Creates a map layer from a job

        Parameters
        ----------
            map_layer_job_id: int
                The id of the job to create the map layer from
        """
        parameters = {"map_layer_job_id": map_layer_job_id}
        return self._post_request(
            self.api_urls.CREATE_MAP_LAYER_FROM_JOB, parameters=parameters
        )

    def update_map_layer_job_progress(
        self,
        map_layer_job_id: int,
        step_id_to_update: int = None,
        percent_complete: float = None,
        started: bool = None,
        status: Literal["pending", "processing", "complete", "error"] = None,
    ):
        """
        Updates the progress of a map layer job

        Parameters
        ----------
            map_layer_job_id: int
                The id of the job to update
            status: Literal["pending", "processing", "complete", "error"]
                The status of the job
            step_id_to_update
                The id of the step to update
            percent_complete: float
                The percentage of the step that is complete
            started: bool
                Whether the step has started
        """
        data = {
            "map_layer_job_id": map_layer_job_id,
            **(
                {"step_id_to_update": step_id_to_update}
                if step_id_to_update is not None
                else {}
            ),
            **({"status": status} if status is not None else {}),
            **({"started": started} if started is not None else {}),
            **(
                {"percent_complete": percent_complete}
                if percent_complete is not None
                else {}
            ),
        }
        return self._put_request(self.api_urls.UPDATE_MAP_LAYER_JOB_PROGRESS, data=data)

    # Calibrate
    def get_calibrate_input(self, calibrate_scenario_id: int) -> dict:
        return self._get_request(
            f"{self.api_urls.GET_CALIBRATE_INPUT}{str(calibrate_scenario_id)}"
        )

    def update_calibrate_scenario_parameters(
        self, calibrate_scenario_id: int, parameters: list
    ) -> bool:
        """Updates parameters on a calibrate scenario"""

        url = self.api_urls.UPDATE_CALIBRATE_SCENARIO_PARAMETERS
        data = {"scenario_id": calibrate_scenario_id, "updated_parameters": parameters}
        return self._post_request(url, data)

    def complete_calibrate_scenario_calibration(
        self, calibrate_scenario_id: int, results: dict
    ) -> bool:
        """
        Signals a scenario calibration has finished with a calibrate output msg

        Parameters
        ----------
            calibrate_scenario_id: int | str
                The id of the calibrate scenario that was calibrated
            results: dict
                A dict with the keys
                    "success": bool
                    "msg": str Message when success is False

        """

        url = self.api_urls.COMPLETE_SCENARIO_CALIBRATION
        data = {"scenario_id": calibrate_scenario_id, **results}
        return self._post_request(url, data)

    def get_planting_design_scenarios(self, planting_design_id: int) -> [dict]:
        """
        Fetches all scenarios for a planting design.

        Parameters
        ----------
            planting_design_id:
                The id of the planting design to fetch the scenarios from

        Returns
        -------
            List of dicts with the keys:
                "scenario_id"
                "name": Calibrate Scenario Name
                "description"
                "status": Calibrate run status
                "species": Latin name of the associated spacies
                "use_for_fasttrack": Boolean flag indicating if it was selected for FastTrack
        """
        url = self.api_urls.GET_PLANTING_DESIGN_CALIBRATE_SCENARIOS
        data = self._get_request(f"{url}{str(planting_design_id)}")
        return data

    def get_siblings_for_calibrate_scenario(
        self, calibrate_scenario_id: int
    ) -> list[dict[int, str]]:
        """
        Returns a list of all the sibling scenarios (same Planting and Tree Species) of a given Scenario.

        Parameters
        ----------
            calibrate_scenario_id:
                The id of the calibrate scenario you want the siblings of

        Returns
        -------
            List of dicts with the keys:
                scenario_id: Scenario id
                status: calibrate run status
        """

        data = self._get_request(
            f"{self.api_urls.GET_CALIBRATE_SCENARIO_SIBLINGS}{str(calibrate_scenario_id)}"
        )
        return data

    # Density Analysis

    def get_da_input(self, da_run_id: int) -> dict:
        return self._get_request(f"{self.api_urls.GET_DA_INPUT}{str(da_run_id)}")

    def complete_da_run(self, da_run_id: int, results: dict) -> bool:
        """
        Signals a density analysis run has finished

        Parameters
        ----------
            da_run_id: int | str
                The id of the Density Analysis run that has finished
            results: dict
                A dict with the keys
                    "success": bool
                    "msg": str Error message when success is False
                    "version": str Fasttrack version used
        """
        url = self.api_urls.COMPLETE_DA_RUN
        data = {"da_run_id": da_run_id, **results}
        return self._post_request(url, data)

    # FastTrack
    def get_ft_input(self, ft_run_id: int):
        return self._get_request(f"{self.api_urls.GET_FT_INPUT}{str(ft_run_id)}")

    def complete_fasttrack_run(self, fasttrack_run_id: int, results: dict) -> bool:
        """
        Signals a fast track run has finished

        Parameters
        ----------
            fasttrack_run_id: int | str
                The id of the fasttrackRun that has finished
            results: dict
                A dict with the keys
                    "success": bool
                    "msg": str Error message when success is False
                    "version": str Fasttrack version used
        """
        url = self.api_urls.COMPLETE_FASTTRACK_RUN
        data = {"fasttrack_run_id": fasttrack_run_id, **results}
        return self._post_request(url, data)

    # Deprecated Endpoints
    def get_model_input_fast_track_json(
        self, site_design_configuration_id: int
    ) -> dict:
        return self._get_request(
            f"{self.api_urls.GET_MODEL_INPUT_FAST_TRACK}{str(site_design_configuration_id)}"
        )

    def get_model_input_fast_track(self, site_design_configuration_id: int) -> dict:
        data = self.get_model_input_fast_track_json(site_design_configuration_id)
        return json_response_to_df(data)

    def get_model_input_calibrate_fast_track_json(
        self, site_design_configuration_id: int
    ) -> dict:
        return self._get_request(
            f"{self.api_urls.GET_MODEL_INPUT_CALIBRATE_FAST_TRACK}{str(site_design_configuration_id)}"
        )

    def get_model_input_calibrate_fast_track(
        self, site_design_configuration_id: int
    ) -> dict:
        data = self.get_model_input_calibrate_fast_track_json(
            site_design_configuration_id
        )
        return json_response_to_df(data)

    def get_model_input_density_analyses_fast_track_json(
        self, site_design_configuration_id: int
    ) -> dict:
        return self._get_request(
            f"{self.api_urls.GET_MODEL_INPUT_DENSITY_ANALYSES_FAST_TRACK}{str(site_design_configuration_id)}"
        )

    def get_model_input_density_analyses_fast_track(
        self, site_design_configuration_id: int
    ) -> dict:
        data = self.get_model_input_density_analyses_fast_track_json(
            site_design_configuration_id
        )
        return json_response_to_df(data)

    # Methods for CMA / Calibrate Cloud

    def get_calibrate_scenario_state_vars(self, calibrate_scenario_id: int) -> dict:
        """
        Returns the init state variables for a calibrate scenario and a exclusion list

        Returns
        -------
            A dict with the keys:
                "state_variables": dict with the state variables as keys
                "excluded_state_variables": [str] List with names of the state variables to exclude from calibrate
        """

        data = self._get_request(
            f"{self.api_urls.GET_CALIBRATE_SCENARIO_STATE_VARS}{str(calibrate_scenario_id)}"
        )
        return data

    def get_calibrate_scenario_nfi_filter(self, calibrate_scenario_id: int):
        """Returns information about the NFI filter to be used to calibrate a scenario"""

        data = self._get_request(
            f"{self.api_urls.GET_CALIBRATE_SCENARIO_NFI_FILTER}{ str(calibrate_scenario_id)}"
        )
        return data

    def get_calibrate_scenario_settings(self, calibrate_scenario_id: int):
        """Returns the settings from a calibrate scenario"""

        data = self._get_request(
            f"{self.api_urls.GET_CALIBRATE_SCENARIO_SETTINGS}{str(calibrate_scenario_id)}"
        )
        return data

    def get_model_input_for_calibrate_scenario(
        self, calibrate_scenario_id: int
    ) -> dict:
        """Returns parameters for calibrate as a dict"""

        data = self._get_request(
            f"{self.api_urls.GET_MODEL_INPUT_FOR_SCENARIO_CALIBRATE}{str(calibrate_scenario_id)}"
        )
        return json_response_to_df(data)

    def get_updated_parameters_from_scenario(self, calibrate_scenario_id: int) -> dict:
        """
        Fetches all parameters from a scenario and returns a dict where the keys are the parameters names.
        If a parameter has not been calibrated, its calibrated_value will be None

        Parameters
        ----------
            calibrate_scenario_id:
                The id of the calibrate scenario

        Returns
        -------
            dict
                keys: Parameter name
                value: dict with the keys initial_value, lower, upper, calibrated_value
        """
        data = self._get_request(
            f"{self.api_urls.GET_CALIBRATE_SCENARIO_PARAMETERS}{str(calibrate_scenario_id)}"
        )
        wanted_k = ["initial_value", "lower", "upper", "calibrated_value"]
        params = {}
        for p in data:
            params[p.get("name", "_")] = dict((k, p.get(k)) for k in wanted_k)
        return params

    # FastTrak cloud
    def get_fasttrack_run_settings(self, fasttrack_run_id: int):
        """Returns data needed to configure and run FT"""
        data = self._get_request(
            f"{self.api_urls.GET_FASTTRACK_RUN_SETTINGS}{str(fasttrack_run_id)}"
        )
        return data

    # Density Analysis cloud
    def get_da_run_settings(self, da_run_id: int):
        """Returns data needed to configure and run DA"""
        data = self._get_request(f"{self.api_urls.GET_DA_RUN_SETTINGS}{str(da_run_id)}")
        return data

    #   NFI
    def save_nfi(self, data: dict):
        url = self.api_urls.SAVE_NFI
        return self._post_request(url, data)

    # Analyzer
    def llc_analyzer(self, data: dict):
        url = self.api_urls.LLC_ANALYZER
        return self._post_request(url, data)

    # START LEGACY METHODS --------------------
    # TODO: remove once all fast track instances use new SDK methods
    def get_model_inputs_as_df(self, config_option: int, legacy_parameters=False):
        data = self.get_model_input_as_json(config_option, legacy_parameters)

        site_info = data["site_info"]
        plot_types = data["plot_types"]
        parameter_data = data["parameter_data"]
        parameter_info = data["parameter_info"]
        species_info = data["species_info"]
        model_info = data["model_info"]

        df_sites_info = pd.json_normalize(site_info)
        df_plot_types = pd.json_normalize(plot_types)
        df_parameter_data = pd.json_normalize(parameter_data)
        df_parameter_info = pd.json_normalize(parameter_info)
        df_species_info = pd.json_normalize(species_info)
        df_model_info = pd.json_normalize(model_info)

        return (
            df_sites_info,
            df_plot_types,
            df_parameter_data,
            df_parameter_info,
            df_species_info,
            df_model_info,
        )

    def get_model_input_as_json(self, config_option, legacy_parameters):
        if not self.auth_token:
            raise ApiTokenError

        url = self.api_urls.GET_MODEL_INPUT_URL + str(config_option)

        if legacy_parameters:
            url = url + "?legacy_parameters"

        data = requests.get(
            url,
            headers={"Authorization": f"Bearer {self.auth_token}"},
        )

        return data.json()

    def get_old_model_inputs(self, model_runs: list, legacy_parameters=False):
        if not self.auth_token:
            raise ApiTokenError

        list_of_runs = ",".join(map(str, model_runs))
        data = requests.get(
            self.api_urls.GET_OLD_MODEL_INPUT_URL + f"={list_of_runs}",
            headers={"Authorization": f"Bearer {self.auth_token}"},
        )

        sites_info = data.json()["sites_info"]
        parameter_data = data.json()["parameter_data"]
        parameter_info = data.json()["parameter_info"]
        species_info = data.json()["species_info"]
        model_info = data.json()["model_info"]

        df_sites_info = pd.json_normalize(sites_info)
        df_parameter_data = pd.json_normalize(parameter_data)
        df_parameter_info = pd.json_normalize(parameter_info)
        df_species_info = pd.json_normalize(species_info)
        df_model_info = pd.json_normalize(model_info)

        if legacy_parameters:
            for i, row in df_parameter_data.iterrows():
                df_parameter_data.at[i, "ParameterName"] = update_legacy_parameter(
                    row["ParameterName"]
                )
            for i, row in df_parameter_info.iterrows():
                df_parameter_info.at[i, "ParameterName"] = update_legacy_parameter(
                    row["ParameterName"]
                )
        return (
            df_sites_info,
            df_parameter_data,
            df_parameter_info,
            df_species_info,
            df_model_info,
        )

    # END LEGACY METHODS --------------------
