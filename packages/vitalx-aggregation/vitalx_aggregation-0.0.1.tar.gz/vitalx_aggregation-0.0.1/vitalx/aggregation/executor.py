import io
import tarfile
import warnings
from typing import Sequence, overload
from uuid import UUID

import polars
import requests

from vitalx.aggregation.auth_utils import ExecutorAuth, infer_executor_auth
from vitalx.aggregation.dsl import QueryInstructionPartial
from vitalx.aggregation.types import (
    Query,
    QueryConfig,
    QueryInstruction,
    RelativeTimeframe,
)
from vitalx.types.environments import VitalEnvironmentT, VitalRegionT, api_base_url


class Executor:
    environment: VitalEnvironmentT
    region: VitalRegionT
    team_id: UUID
    auth: ExecutorAuth

    def __init__(
        self,
        *,
        environment: VitalEnvironmentT,
        region: VitalRegionT,
        team_id: UUID,
        api_key: str | None = None,
    ) -> None:
        self.auth = infer_executor_auth(team_id=team_id, explicit_api_key=api_key)
        self.team_id = team_id
        self.region = region
        self.environment = environment

        warnings.filterwarnings("ignore", message="Polars found a filename")

    @overload
    def query(
        self,
        timeframe: RelativeTimeframe,
        instruction: QueryInstruction | QueryInstructionPartial,
        /,
        *,
        user_id: UUID,
        config: QueryConfig = QueryConfig(),
    ) -> tuple[polars.DataFrame]:
        pass

    @overload
    def query(
        self,
        timeframe: RelativeTimeframe,
        instruction_1: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_2: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        /,
        *,
        user_id: UUID,
        config: QueryConfig = QueryConfig(),
    ) -> tuple[polars.DataFrame, polars.DataFrame]:
        pass

    @overload
    def query(
        self,
        timeframe: RelativeTimeframe,
        instruction_1: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_2: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_3: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        /,
        *,
        user_id: UUID,
        config: QueryConfig = QueryConfig(),
    ) -> tuple[polars.DataFrame, polars.DataFrame, polars.DataFrame]:
        pass

    @overload
    def query(
        self,
        timeframe: RelativeTimeframe,
        instruction_1: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_2: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_3: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_4: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        /,
        *,
        user_id: UUID,
        config: QueryConfig = QueryConfig(),
    ) -> tuple[polars.DataFrame, polars.DataFrame, polars.DataFrame, polars.DataFrame]:
        pass

    @overload
    def query(
        self,
        timeframe: RelativeTimeframe,
        instruction_1: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_2: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_3: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_4: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_5: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        /,
        *,
        user_id: UUID,
        config: QueryConfig = QueryConfig(),
    ) -> tuple[
        polars.DataFrame,
        polars.DataFrame,
        polars.DataFrame,
        polars.DataFrame,
        polars.DataFrame,
    ]:
        pass

    @overload
    def query(
        self,
        timeframe: RelativeTimeframe,
        instruction_1: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_2: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_3: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_4: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_5: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        instruction_6: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        /,
        *,
        user_id: UUID,
        config: QueryConfig = QueryConfig(),
    ) -> tuple[
        polars.DataFrame,
        polars.DataFrame,
        polars.DataFrame,
        polars.DataFrame,
        polars.DataFrame,
        polars.DataFrame,
    ]:
        pass

    @overload
    def query(
        self,
        timeframe: RelativeTimeframe,
        /,
        *instructions: QueryInstruction | QueryInstructionPartial,  # noqa: F841
        user_id: UUID,
        config: QueryConfig = QueryConfig(),
    ) -> tuple[polars.DataFrame, ...]:
        pass

    def query(
        self,
        timeframe: RelativeTimeframe,
        /,
        *instructions: QueryInstruction | QueryInstructionPartial,
        user_id: UUID,
        config: QueryConfig = QueryConfig(),
    ) -> Sequence[polars.DataFrame]:
        query = Query(
            timeframe=timeframe,
            instructions=list(
                inst if isinstance(inst, QueryInstruction) else inst.finalize()
                for inst in instructions
            ),
            config=config,
        )

        resp = requests.post(
            "{}{}/{}".format(
                api_base_url(self.environment, self.region),
                "aggregate/v1/query_one",
                str(user_id),
            ),
            headers={
                **(self.auth.headers()),
                "Accept": "application/vnd.vital.tar+gzip+parquet",
            },
            json=query.model_dump(mode="json"),
        )

        resp.raise_for_status()

        df = list[polars.DataFrame]()

        with tarfile.open(fileobj=io.BytesIO(resp.content), mode="r:gz") as tar:
            members = sorted(
                tar.getmembers(), key=lambda m: int(m.name.removesuffix(".parquet"))
            )

            for member in members:
                file = tar.extractfile(member)
                assert file is not None
                df.append(polars.read_parquet(file))

        return df
