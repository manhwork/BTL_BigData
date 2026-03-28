from dataclasses import dataclass
from importlib import import_module

from main.common.spark import LegacySparkSessionFactory


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


@dataclass(frozen=True)
class BronzeReadResult:
    spark: object
    spark_context: object
    dataframe: object
    bronze_path: str


class _LegacyBronzeUploader:
    def upload(self, *, request: BronzeIngestionRequest, spark) -> None:
        legacy_module = import_module("load_rawData.load")

        if request.dataset_type == "meta":
            legacy_module.upload_meta_data(
                spark,
                request.category,
                compression_codec=request.compression_codec,
                clear_hf_cache=request.clear_hf_cache,
            )
            return

        legacy_module.upload_review_data(
            spark,
            request.category,
            compression_codec=request.compression_codec,
            clear_hf_cache=request.clear_hf_cache,
        )


class BronzeService:
    def __init__(self, session_factory=None, bronze_uploader=None) -> None:
        self.session_factory = session_factory or LegacySparkSessionFactory()
        self.bronze_uploader = bronze_uploader or _LegacyBronzeUploader()

    def _create_session(self, request: BronzeIngestionRequest):
        return self.session_factory.create(
            driver_memory_gb=request.driver_memory_gb,
            executor_memory_gb=request.executor_memory_gb,
            reserve_cores=request.reserve_cores,
        )

    def ingest(self, request: BronzeIngestionRequest) -> BronzeIngestionResult:
        spark, _ = self._create_session(request)
        self.bronze_uploader.upload(request=request, spark=spark)
        return BronzeIngestionResult(
            dataset_type=request.dataset_type,
            category=request.category,
            bronze_output_path=request.bronze_output_path,
            succeeded=True,
        )

    def read(self, request: BronzeIngestionRequest) -> BronzeReadResult:
        spark, spark_context = self._create_session(request)
        dataframe = spark.read.parquet(request.bronze_output_path)
        return BronzeReadResult(
            spark=spark,
            spark_context=spark_context,
            dataframe=dataframe,
            bronze_path=request.bronze_output_path,
        )

