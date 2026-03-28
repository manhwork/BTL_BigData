import unittest

from main.bronze.bronze_service import BronzeIngestionRequest, BronzeService


class FakeDataFrame:
    pass


class FakeReader:
    def __init__(self) -> None:
        self.paths = []
        self.dataframe = FakeDataFrame()

    def parquet(self, path):
        self.paths.append(path)
        return self.dataframe


class FakeSparkSession:
    def __init__(self) -> None:
        self.read = FakeReader()


class FakeSparkSessionFactory:
    def __init__(self) -> None:
        self.calls = []
        self.spark = FakeSparkSession()

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self.spark, "spark-context"


class FakeBronzeUploader:
    def __init__(self) -> None:
        self.calls = []

    def upload(self, *, request, spark) -> None:
        self.calls.append((request, spark))


class BronzeServiceTest(unittest.TestCase):
    def test_ingest_uses_shared_session_factory_and_uploader(self) -> None:
        session_factory = FakeSparkSessionFactory()
        uploader = FakeBronzeUploader()
        service = BronzeService(session_factory=session_factory, bronze_uploader=uploader)
        request = BronzeIngestionRequest(dataset_type="meta", category="Books")

        result = service.ingest(request)

        self.assertEqual(
            session_factory.calls,
            [{"driver_memory_gb": 10, "executor_memory_gb": 10, "reserve_cores": 1}],
        )
        self.assertEqual(uploader.calls, [(request, session_factory.spark)])
        self.assertTrue(result.succeeded)
        self.assertEqual(result.bronze_output_path, request.bronze_output_path)

    def test_read_uses_shared_session_factory_and_parquet_reader(self) -> None:
        session_factory = FakeSparkSessionFactory()
        service = BronzeService(session_factory=session_factory, bronze_uploader=FakeBronzeUploader())
        request = BronzeIngestionRequest(dataset_type="review", category="Appliances")

        result = service.read(request)

        self.assertEqual(
            session_factory.spark.read.paths,
            ["gs://amazon-reviews-lakehouse-data/bronze-zone/review-data/Appliances"],
        )
        self.assertIs(result.dataframe, session_factory.spark.read.dataframe)
        self.assertEqual(result.bronze_path, request.bronze_output_path)


if __name__ == "__main__":
    unittest.main()
