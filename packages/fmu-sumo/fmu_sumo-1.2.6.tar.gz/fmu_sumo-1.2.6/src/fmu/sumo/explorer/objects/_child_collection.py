"""Module containing class for collection of children"""

from typing import List, Dict, Union
from sumo.wrapper import SumoClient
from fmu.sumo.explorer.objects._document_collection import DocumentCollection
from fmu.sumo.explorer.timefilter import TimeFilter
from fmu.sumo.explorer.pit import Pit

_CHILD_FIELDS = {
    "include": [],
    "exclude": ["data.spec.columns", "fmu.realization.parameters"],
}


class ChildCollection(DocumentCollection):
    """Class for representing a collection of child objects in Sumo"""

    def __init__(
        self,
        doc_type: str,
        sumo: SumoClient,
        case_uuid: str,
        query: Dict = None,
        pit: Pit = None,
    ):
        self._case_uuid = case_uuid
        super().__init__(doc_type, sumo, query, _CHILD_FIELDS, pit)

    @property
    def names(self) -> List[str]:
        """List of unique object names"""
        return self._get_field_values("data.name.keyword")

    @property
    async def names_async(self) -> List[str]:
        """List of unique object names"""
        return await self._get_field_values_async("data.name.keyword")

    @property
    def tagnames(self) -> List[str]:
        """List of unqiue object tagnames"""
        return self._get_field_values("data.tagname.keyword")

    @property
    async def tagnames_async(self) -> List[str]:
        """List of unqiue object tagnames"""
        return await self._get_field_values_async("data.tagname.keyword")

    @property
    def dataformats(self) -> List[str]:
        """List of unique data.format values"""
        return self._get_field_values("data.format.keyword")

    @property
    async def dataformats_async(self) -> List[str]:
        """List of unique data.format values"""
        return await self._get_field_values_async("data.format.keyword")

    @property
    def iterations(self) -> List[int]:
        """List of unique object iteration names"""
        return self._get_field_values("fmu.iteration.name.keyword")

    @property
    async def iterations_async(self) -> List[int]:
        """List of unique object iteration names"""
        return await self._get_field_values_async("fmu.iteration.name.keyword")

    @property
    def realizations(self) -> List[int]:
        """List of unique object realization ids"""
        return self._get_field_values("fmu.realization.id")

    @property
    async def realizations_async(self) -> List[int]:
        """List of unique object realization ids"""
        return await self._get_field_values_async("fmu.realization.id")

    @property
    def aggregations(self) -> List[str]:
        """List of unique object aggregation operations"""
        return self._get_field_values("fmu.aggregation.operation.keyword")

    @property
    async def aggregations_async(self) -> List[str]:
        """List of unique object aggregation operations"""
        return await self._get_field_values_async(
            "fmu.aggregation.operation.keyword"
        )

    @property
    def stages(self) -> List[str]:
        """List of unique stages"""
        return self._get_field_values("fmu.context.stage.keyword")

    @property
    async def stages_async(self) -> List[str]:
        """List of unique stages"""
        return await self._get_field_values_async("fmu.context.stage.keyword")

    @property
    def stratigraphic(self) -> List[str]:
        """List of unqiue object stratigraphic"""
        return self._get_field_values("data.stratigraphic")

    @property
    async def stratigraphic_async(self) -> List[str]:
        """List of unqiue object stratigraphic"""
        return await self._get_field_values_async("data.stratigraphic")

    @property
    def vertical_domain(self) -> List[str]:
        """List of unqiue object vertical domain"""
        return self._get_field_values("data.vertical_domain")

    @property
    async def vertical_domain_async(self) -> List[str]:
        """List of unqiue object vertical domain"""
        return await self._get_field_values_async("data.vertical_domain")

    @property
    def contents(self) -> List[str]:
        """List of unique contents"""
        return self._get_field_values("data.content.keyword")

    @property
    async def contents_async(self) -> List[str]:
        """List of unique contents"""
        return self._get_field_values_async("data.content.keyword")

    def _init_query(self, doc_type: str, query: Dict = None) -> Dict:
        new_query = super()._init_query(doc_type, query)
        case_filter = {
            "bool": {
                "must": [
                    {"term": {"_sumo.parent_object.keyword": self._case_uuid}}
                ]
            }
        }

        return self._utils.extend_query_object(new_query, case_filter)

    def _add_filter(
        self,
        name: Union[str, List[str], bool] = None,
        tagname: Union[str, List[str], bool] = None,
        dataformat: Union[str, List[str], bool] = None,
        iteration: Union[str, List[str], bool] = None,
        realization: Union[int, List[int], bool] = None,
        aggregation: Union[str, List[str], bool] = None,
        stage: Union[str, List[str], bool] = None,
        column: Union[str, List[str], bool] = None,
        time: TimeFilter = None,
        uuid: Union[str, List[str], bool] = None,
        stratigraphic: Union[str, List[str], bool] = None,
        vertical_domain: Union[str, List[str], bool] = None,
        content: Union[str, List[str], bool] = None,
        is_observation: bool = None,
        is_prediction: bool = None,
    ):
        must = []
        must_not = []

        prop_map = {
            "data.name.keyword": name,
            "data.tagname.keyword": tagname,
            "data.format": dataformat,
            "fmu.iteration.name.keyword": iteration,
            "fmu.realization.id": realization,
            "fmu.aggregation.operation.keyword": aggregation,
            "fmu.context.stage.keyword": stage,
            "data.spec.columns.keyword": column,
            "_id": uuid,
            "data.vertical_domain.keyword": vertical_domain,
            "data.content.keyword": content,
        }

        for prop, value in prop_map.items():
            if value is not None:
                if isinstance(value, bool):
                    if value:
                        must.append({"exists": {"field": prop}})
                    else:
                        must_not.append({"exists": {"field": prop}})
                else:
                    term = "terms" if isinstance(value, list) else "term"
                    must.append({term: {prop: value}})

        bool_prop_map = {
            "data.stratigraphic": stratigraphic,
            "data.is_observation": is_observation,
            "data.is_prediction": is_prediction,
        }
        for prop, value in bool_prop_map.items():
            if value is not None:
                must.append({"term": {prop: value}})

        query = {"bool": {}}

        if len(must) > 0:
            query["bool"]["must"] = must

        if len(must_not) > 0:
            query["bool"]["must_not"] = must_not

        if time:
            query = self._utils.extend_query_object(query, time._get_query())

        return super()._add_filter(query)
