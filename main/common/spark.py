from importlib import import_module


class LegacySparkSessionFactory:
    def create(
        self,
        *,
        driver_memory_gb: int,
        executor_memory_gb: int,
        reserve_cores: int,
    ):
        legacy_module = import_module("load_rawData.load")
        return legacy_module.create_spark_session(
            driver_memory_gb=driver_memory_gb,
            executor_memory_gb=executor_memory_gb,
            reserve_cores=reserve_cores,
        )
