import unittest

from main.gold.gold_service import GoldJobRequest, GoldService


class GoldServiceTest(unittest.TestCase):
    def test_build_user_behavior_returns_gold_path(self) -> None:
        service = GoldService()
        request = GoldJobRequest(category="Appliances")

        result = service.build_user_behavior(request)

        self.assertTrue(result.succeeded)
        self.assertEqual(result.job_name, "user_behavior")
        self.assertEqual(
            result.target_path,
            "gs://amazon-reviews-lakehouse-data/gold-zone/user-behavior/Appliances",
        )

    def test_build_fake_review_returns_gold_path(self) -> None:
        service = GoldService()
        request = GoldJobRequest(category="Books")

        result = service.build_fake_review(request)

        self.assertTrue(result.succeeded)
        self.assertEqual(result.job_name, "fake_review")
        self.assertEqual(
            result.target_path,
            "gs://amazon-reviews-lakehouse-data/gold-zone/fake-review/Books",
        )


if __name__ == "__main__":
    unittest.main()
