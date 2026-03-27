import argparse

from main.bronze.ingest import BronzeIngestionService
from main.bronze.models import BronzeIngestionRequest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Bronze ingestion via legacy Spark pipeline.")
    parser.add_argument("--dataset-type", choices=["meta", "review"], required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--driver-memory-gb", type=int, default=10)
    parser.add_argument("--executor-memory-gb", type=int, default=10)
    parser.add_argument("--reserve-cores", type=int, default=1)
    parser.add_argument("--compression-codec", default="gzip")
    parser.add_argument("--clear-hf-cache", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    request = BronzeIngestionRequest(
        dataset_type=args.dataset_type,
        category=args.category,
        driver_memory_gb=args.driver_memory_gb,
        executor_memory_gb=args.executor_memory_gb,
        reserve_cores=args.reserve_cores,
        compression_codec=args.compression_codec,
        clear_hf_cache=args.clear_hf_cache,
    )
    result = BronzeIngestionService().ingest(request)
    print(
        f"Bronze ingestion completed: dataset_type={result.dataset_type}, "
        f"category={result.category}, output={result.bronze_output_path}"
    )


if __name__ == "__main__":
    main()

