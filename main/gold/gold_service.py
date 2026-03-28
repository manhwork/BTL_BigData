from dataclasses import dataclass


@dataclass(frozen=True)
class GoldJobRequest:
    category: str
    source_path: str | None = None


@dataclass(frozen=True)
class GoldJobResult:
    category: str
    job_name: str
    target_path: str
    succeeded: bool


class GoldService:
    def build_user_behavior(self, request: GoldJobRequest) -> GoldJobResult:
        return GoldJobResult(
            category=request.category,
            job_name="user_behavior",
            target_path=f"gs://amazon-reviews-lakehouse-data/gold-zone/user-behavior/{request.category}",
            succeeded=True,
        )

    def build_trust_score(self, request: GoldJobRequest) -> GoldJobResult:
        return GoldJobResult(
            category=request.category,
            job_name="trust_score",
            target_path=f"gs://amazon-reviews-lakehouse-data/gold-zone/trust-score/{request.category}",
            succeeded=True,
        )

    def build_fake_review(self, request: GoldJobRequest) -> GoldJobResult:
        return GoldJobResult(
            category=request.category,
            job_name="fake_review",
            target_path=f"gs://amazon-reviews-lakehouse-data/gold-zone/fake-review/{request.category}",
            succeeded=True,
        )

