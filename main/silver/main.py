import argparse

from main.silver.silver_service import SilverJobRequest, SilverService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Silver jobs.")
    parser.add_argument("action", choices=["clean", "enrich", "publish"])
    parser.add_argument("--category", required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    request = SilverJobRequest(category=args.category)
    service = SilverService()

    if args.action == "clean":
        result = service.clean(request)
    elif args.action == "enrich":
        result = service.enrich(request)
    else:
        result = service.publish(request)

    print(
        f"Silver job completed: stage={result.stage}, "
        f"category={result.category}, output={result.target_path}"
    )


if __name__ == "__main__":
    main()

