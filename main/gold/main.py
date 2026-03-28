import argparse

from main.gold.gold_service import GoldJobRequest, GoldService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Gold jobs.")
    parser.add_argument(
        "action",
        choices=["build-user-behavior", "build-trust-score", "build-fake-review"],
    )
    parser.add_argument("--category", required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    request = GoldJobRequest(category=args.category)
    service = GoldService()

    if args.action == "build-user-behavior":
        result = service.build_user_behavior(request)
    elif args.action == "build-trust-score":
        result = service.build_trust_score(request)
    else:
        result = service.build_fake_review(request)

    print(
        f"Gold job completed: job={result.job_name}, "
        f"category={result.category}, output={result.target_path}"
    )


if __name__ == "__main__":
    main()

