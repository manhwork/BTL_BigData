from dataclasses import dataclass


@dataclass(frozen=True)
class SilverJobRequest:
    category: str
    source_path: str | None = None


@dataclass(frozen=True)
class SilverJobResult:
    category: str
    stage: str
    target_path: str
    succeeded: bool


class SilverService:
    def clean(self, request: SilverJobRequest) -> SilverJobResult:
        return SilverJobResult(
            category=request.category,
            stage="clean",
            target_path=f"gs://amazon-reviews-lakehouse-data/silver-zone/clean-data/{request.category}",
            succeeded=True,
        )

    def enrich(self, request: SilverJobRequest) -> SilverJobResult:
        return SilverJobResult(
            category=request.category,
            stage="enrich",
            target_path=f"gs://amazon-reviews-lakehouse-data/silver-zone/enriched-data/{request.category}",
            succeeded=True,
        )

    def publish(self, request: SilverJobRequest) -> SilverJobResult:
        return SilverJobResult(
            category=request.category,
            stage="publish",
            target_path=f"gs://amazon-reviews-lakehouse-data/silver-zone/final-data/{request.category}",
            succeeded=True,
        )

