from typing import Any

from earthscale.datasets.visualization import (
    BaseVisualizationParams,
    CategoricalVisualization,
    RGBVisualization,
    SingleBandVisualization,
    VectorVisualization,
    Visualization,
    VisualizationType,
)
from supabase import Client

_VIZ_TABLE = "viz_params"


class VizNotFoundError(Exception):
    pass


def _unpack_viz_params(
    viz_type: VisualizationType, viz_params: dict[str, Any]
) -> BaseVisualizationParams:
    if viz_type == VisualizationType.VECTOR:
        return VectorVisualization(**viz_params)
    elif viz_type == VisualizationType.RGB:
        return RGBVisualization(**viz_params)
    elif viz_type == VisualizationType.SINGLE_BAND:
        return SingleBandVisualization(**viz_params)
    elif viz_type == VisualizationType.CATEGORICAL:
        # TODO: this is a hack to remove extra fields from the viz params
        viz_params_dict = {
            "valueMap": viz_params["valueMap"],
            "colorMap": viz_params["colorMap"],
        }
        return CategoricalVisualization(**viz_params_dict)
    else:
        raise ValueError(f"Unknown visualization type {viz_type}")


class VizRepository:
    def __init__(
        self,
        client: Client,
    ):
        self.client = client

    def get(
        self,
        id_: str,
    ) -> Visualization:
        query = (
            self.client.table(_VIZ_TABLE)
            .select("*")
            .eq("id", id_)
            .order("created_at", desc=True)
        )
        results = query.limit(1).execute()

        if results.data is None or len(results.data) == 0:
            raise VizNotFoundError(f"No item found with id {id_}")

        data = results.data[0]
        viz_type = VisualizationType(data["type"])
        viz_params = data["params"]
        viz_params = _unpack_viz_params(viz_type, viz_params)
        viz = Visualization(viz_type, viz_params)
        return viz
