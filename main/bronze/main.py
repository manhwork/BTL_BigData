import argparse

from main.bronze.bronze_service import BronzeIngestionRequest, BronzeService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Bronze operations via legacy Spark pipeline.")
    parser.add_argument("action", choices=["ingest", "read"])
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

    service = BronzeService()
    if args.action == "ingest":
        result = service.ingest(request)
        print(
            f"Bronze ingestion completed: dataset_type={result.dataset_type}, "
            f"category={result.category}, output={result.bronze_output_path}"
        )
        return

    result = service.read(request)
    print(f"Bronze read completed: path={result.bronze_path}")
    result.dataframe.show(5, truncate=False)


if __name__ == "__main__":
    main()

