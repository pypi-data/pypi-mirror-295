from __future__ import annotations
import typing as t
import pandas as pd
from pydantic import ConfigDict, BaseModel
from .utils import reform_for_multiindex_df


class SolarTimeSeries(BaseModel):
    r"""-"""

    ideal_tracker_rotation: t.Optional[list] = None

    front_total_poa: t.Optional[list] = None

    rear_total_poa: t.Optional[list] = None

    effective_total_poa: t.Optional[list] = None

    array_dc_snow_loss: t.Optional[list] = None

    array_gross_dc_power: t.Optional[list] = None

    array_dc_power: t.Optional[list] = None

    array_dc_voltage: t.Optional[list] = None

    inverter_mppt_dc_voltage: t.Optional[list] = None

    inverter_mppt_loss: t.Optional[list] = None

    inverter_clipping_loss: t.Optional[list] = None

    inverter_night_tare_loss: t.Optional[list] = None

    inverter_power_consumption_loss: t.Optional[list] = None

    inverter_efficiency: t.Optional[list] = None

    ambient_temp: t.Optional[list] = None

    gross_ac_power: list

    mv_transformer_loss: t.Optional[list] = None

    mv_transformer_load_loss: t.Optional[list] = None

    mv_transformer_no_load_loss: t.Optional[list] = None

    mv_ac_power: list

    ac_wiring_loss: list

    hv_transformer_loss: t.Optional[list] = None

    hv_transformer_load_loss: t.Optional[list] = None

    hv_transformer_no_load_loss: t.Optional[list] = None

    transformer_load_loss: list

    transformer_no_load_loss: list

    hv_ac_power: list

    ac_transmission_loss: list

    gen: list

    poi_unadjusted: list

    system_power: list

    positive_system_power: list

    negative_system_power: list

    sam_design_parameters: dict


class SolarWaterfall(BaseModel):
    r"""-"""

    gh_ann: t.Optional[float] = None

    nominal_poa_ann: t.Optional[float] = None

    shading_lp: t.Optional[float] = None

    soiling_lp: t.Optional[float] = None

    reflection_lp: t.Optional[float] = None

    bifacial_lp: t.Optional[float] = None

    dc_nominal_ann: t.Optional[float] = None

    snow_lp: t.Optional[float] = None

    module_temp_lp: t.Optional[float] = None

    mppt_lp: t.Optional[float] = None

    mismatch_lp: t.Optional[float] = None

    diodes_lp: t.Optional[float] = None

    dc_wiring_lp: t.Optional[float] = None

    tracking_error_lp: t.Optional[float] = None

    mppt_error_lp: t.Optional[float] = None

    nameplate_lp: t.Optional[float] = None

    dc_optimizer_lp: t.Optional[float] = None

    dc_avail_lp: t.Optional[float] = None

    dc_net_ann: t.Optional[float] = None

    inverter_clipping_lp: t.Optional[float] = None

    inverter_consumption_lp: t.Optional[float] = None

    inverter_nightcons_lp: t.Optional[float] = None

    inverter_efficiency_lp: t.Optional[float] = None

    ac_gross_ann: t.Optional[float] = None

    mv_transformer_lp: t.Optional[float] = None

    ac_wiring_lp: t.Optional[float] = None

    hv_transformer_lp: t.Optional[float] = None

    transformer_lp: float

    transmission_lp: float

    poi_clipping_lp: float

    ac_availcurtail_lp: float

    annual_energy: float


class SolarStorageTimeSeries(BaseModel):
    r"""-"""

    battery_internal_energy: list

    battery_internal_energy_max: list

    battery_limit: t.Union[float, list]

    battery_output: list

    excess_power_at_coupling: list

    captured_excess_at_coupling: list

    solar_storage_dc_voltage: t.Optional[list] = None

    solar_storage_dc_power: t.Optional[list] = None

    solar_storage_power_at_coupling: t.Optional[list] = None

    inverter_clipping_loss: t.Optional[list] = None

    inverter_tare_loss: t.Optional[list] = None

    inverter_parasitic_loss: t.Optional[list] = None

    inverter_consumption_loss: t.Optional[list] = None

    inverter_efficiency: t.Optional[list] = None

    solar_storage_gross_ac_power: t.Optional[list] = None

    mv_xfmr_loss: t.Optional[list] = None

    mv_xfmr_load_loss: t.Optional[list] = None

    mv_xfmr_no_load_loss: t.Optional[list] = None

    solar_storage_ac_power: list

    solar_storage_mv_ac_power: t.Optional[list] = None

    hvac_loss: t.Optional[list] = None

    ac_wiring_loss: t.Optional[list] = None

    hv_xfmr_loss: t.Optional[list] = None

    hv_xfmr_load_loss: t.Optional[list] = None

    hv_xfmr_no_load_loss: t.Optional[list] = None

    transformer_loss: t.Optional[list] = None

    solar_storage_hv_ac_power: list

    transmission_loss: list

    solar_storage_gen: list

    solar_storage_poi_unadjusted: list

    solar_storage_poi: list

    positive_solar_storage_poi: list

    negative_solar_storage_poi: list


class SolarStorageWaterfall(SolarWaterfall):
    r"""-"""

    battery_operation_lp: float

    excess_power_at_coupling_lp: float

    captured_excess_at_coupling_lp: float

    bess_hvac_lp: t.Optional[float] = None


class OptimizerTimeSeries(BaseModel):
    r"""-"""
    model_config = ConfigDict(extra="allow")

    # note this might not be present because there were no hvac inputs, but also because for standalone+downstream and
    #  hybrid this signal is moved into system/solar_storage
    hvac_loss: t.Optional[list] = None

    import_limit_at_coupling: t.Optional[list] = None

    export_limit_at_coupling: t.Optional[list] = None

    target_load: t.Optional[list] = None

    charge_actual: list

    discharge_actual: list

    charge: list

    discharge: list

    charge_hi: list

    discharge_hi: list

    charge_lo: list

    discharge_lo: list

    battery_output: list

    output: list

    total_output: list

    internal_energy: list

    soe_actual: list

    soe_lo: list

    soe_hi: list

    soe_hb_actual: list

    soe_hb_lo: list

    soe_hb_hi: list

    soe_mean_actual: list

    soe_mean_lo: list

    soe_mean_hi: list

    dam_charge: t.Optional[list] = None

    dam_discharge: t.Optional[list] = None

    dam_base_point: t.Optional[list] = None

    negative_dam_base_point: t.Optional[list] = None

    dam_solar: t.Optional[list] = None

    rtm_charge: t.Optional[list] = None

    rtm_discharge: t.Optional[list] = None

    rtm_base_point: t.Optional[list] = None

    negative_rtm_base_point: t.Optional[list] = None

    rtm_solar: t.Optional[list] = None

    rtm_price: t.Optional[list] = None

    dam_price: t.Optional[list] = None

    imbalance: t.Optional[list] = None

    theoretical_dam_soe: t.Optional[list] = None

    solar_actual: t.Optional[list] = None

    solar_hi: t.Optional[list] = None

    solar_lo: t.Optional[list] = None

    net_load: t.Optional[list] = None


class MarketAwardsTimeSeries(BaseModel):
    r"""-"""
    model_config = ConfigDict(extra="allow")

    charge: list

    discharge: list

    total_output: list

    rt_tare: list

    dam_charge: list

    dam_discharge: list

    dam_base_point: list

    negative_dam_base_point: list

    rtm_charge: list

    rtm_discharge: list

    rtm_base_point: list

    solar_actual: t.Optional[list] = None

    dam_solar: t.Optional[list] = None

    rtm_solar: t.Optional[list] = None


class StandaloneStorageSystemTimeSeries(BaseModel):
    r"""-"""

    dc_power: t.Optional[list] = None

    dc_voltage: t.Optional[list] = None

    inverter_clipping_loss: t.Optional[list] = None

    inverter_tare_loss: t.Optional[list] = None

    inverter_parasitic_loss: t.Optional[list] = None

    inverter_consumption_loss: t.Optional[list] = None

    inverter_efficiency: t.Optional[list] = None

    gross_ac_power: t.Optional[list] = None

    hvac_loss: t.Optional[list] = None

    ac_power: list

    mv_xfmr_loss: t.Optional[list] = None

    mv_xfmr_load_loss: t.Optional[list] = None

    mv_xfmr_no_load_loss: t.Optional[list] = None

    ac_wiring_loss: t.Optional[list] = None

    hv_xfmr_loss: t.Optional[list] = None

    hv_xfmr_load_loss: t.Optional[list] = None

    hv_xfmr_no_load_loss: t.Optional[list] = None

    transformer_loss: t.Optional[list] = None

    hv_ac_power: list

    transmission_loss: list

    gen: list

    poi_unadjusted: list

    poi: list

    positive_poi: list

    negative_poi: list


class GenerationModelResults(SolarTimeSeries):
    r"""Results schema returned when a
    :class:`~generation_models.generation_models.generation_models.PVGenerationModel`,
    :class:`~generation_models.generation_models.generation_models.ACExternalGenerationModel` or
    :class:`~generation_models.generation_models.generation_models.DCExternalGenerationModel` simulation is run"""

    tyba_api_loss_waterfall: SolarWaterfall

    warnings: t.List[str]

    coupling: None

    def time_series_df(self):
        return pd.DataFrame(
            self.model_dump(
                exclude={
                    "tyba_api_loss_waterfall",
                    "warnings",
                    "coupling",
                    "sam_design_parameters",
                },
                exclude_none=True,
            )
        )


class PVStorageModelResults(BaseModel):
    r"""Results schema returned when a :class:`~generation_models.generation_models.generation_models.PVStorageModel`
    simulation is run
    """

    solar_only: SolarTimeSeries

    solar_storage: SolarStorageTimeSeries

    waterfall: SolarStorageWaterfall

    optimizer: OptimizerTimeSeries

    market_awards: t.Optional[MarketAwardsTimeSeries] = None

    warnings: t.List[str]

    coupling: str

    def time_series_df(self):
        model_dict = self.model_dump(
            exclude={
                "solar_only": {"sam_design_parameters"},
                "waterfall": True,
                "warnings": True,
                "coupling": True,
            },
            exclude_none=True,
        )
        if isinstance(model_dict["solar_storage"]["battery_limit"], float):
            model_dict["solar_storage"]["battery_limit"] = [model_dict["solar_storage"]["battery_limit"]] * len(
                model_dict["solar_storage"]["battery_internal_energy_max"]
            )
        return pd.DataFrame(reform_for_multiindex_df(model_dict))


class StandaloneStorageModelWithDownstreamResults(BaseModel):
    r"""Results schema returned when a
    :class:`~generation_models.generation_models.generation_models.StandaloneStorageModel` simulation is run with a
    :attr:`~generation_models.generation_models.generation_models.StandaloneStorageModel.downstream_system` specified"""

    system: StandaloneStorageSystemTimeSeries

    optimizer_outputs: OptimizerTimeSeries

    market_awards: t.Optional[MarketAwardsTimeSeries] = None

    def time_series_df(self):
        model_dict = self.model_dump(exclude_none=True)
        return pd.DataFrame(reform_for_multiindex_df(model_dict))


class StandaloneStorageModelSimpleResults(OptimizerTimeSeries):
    r"""Results schema returned when a
    :class:`~generation_models.generation_models.generation_models.StandaloneStorageModel` simulation is run without a
    :attr:`~generation_models.generation_models.generation_models.StandaloneStorageModel.downstream_system` specified"""
    model_config = ConfigDict(extra="allow")

    def time_series_df(self):
        return pd.DataFrame(self.model_dump(exclude_none=True))
