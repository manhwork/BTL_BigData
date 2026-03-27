from main.bronze.models import BronzeIngestionRequest, BronzeIngestionResult
from main.bronze.upload import LegacyBronzeUploader
from main.common.spark import LegacySparkSessionFactory


class BronzeIngestionService:
    def __init__(self, session_factory=None, bronze_uploader=None) -> None:
        self.session_factory = session_factory or LegacySparkSessionFactory()
        self.bronze_uploader = bronze_uploader or LegacyBronzeUploader()

    def ingest(self, request: BronzeIngestionRequest) -> BronzeIngestionResult:
        spark, _ = self.session_factory.create(
            driver_memory_gb=request.driver_memory_gb,
            executor_memory_gb=request.executor_memory_gb,
            reserve_cores=request.reserve_cores,
        )
        self.bronze_uploader.upload(request=request, spark=spark)
        return BronzeIngestionResult(
            dataset_type=request.dataset_type,
            category=request.category,
            bronze_output_path=request.bronze_output_path,
            succeeded=True,
        )
