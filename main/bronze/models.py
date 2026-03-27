from dataclasses import dataclass


@dataclass(frozen=True)
class BronzeIngestionRequest:
    dataset_type: str
    category: str
    driver_memory_gb: int = 10
    executor_memory_gb: int = 10
    reserve_cores: int = 1
    compression_codec: str = "gzip"
    clear_hf_cache: bool = True

    @property
    def bronze_output_path(self) -> str:
        dataset_folder = "meta-data" if self.dataset_type == "meta" else "review-data"
        return f"gs://amazon-reviews-lakehouse-data/bronze-zone/{dataset_folder}/{self.category}"


@dataclass(frozen=True)
class BronzeIngestionResult:
    dataset_type: str
    category: str
    bronze_output_path: str
    succeeded: bool
