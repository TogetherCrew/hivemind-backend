from unittest import TestCase
from bson import ObjectId
from datetime import datetime

from tc_hivemind_backend.db.modules_base import ModulesBase
from tc_hivemind_backend.db.mongo import MongoSingleton


class TestModulesBaseQuery(TestCase):
    def setUp(self) -> None:
        self.client = MongoSingleton.get_instance().get_client()
        self.client["Core"].drop_collection("modules")

        # Create sample modules for testing
        self.community_id1 = ObjectId("6579c364f1120850414e0dc5")
        self.community_id2 = ObjectId("6579c364f1120850414e0dc6")

        # Module with platform "discord"
        self.client["Core"]["modules"].insert_one(
            {
                "_id": ObjectId("6579c364f1120850414e0dc7"),
                "name": "hivemind",
                "community": self.community_id1,
                "activated": True,
                "options": {"platforms": [{"name": "discord", "id": "platform1"}]},
                "metadata": {"key1": "value1"},
                "createdAt": datetime.now(),
                "updatedAt": datetime.now(),
            }
        )

        # Module with platform "github"
        self.client["Core"]["modules"].insert_one(
            {
                "_id": ObjectId("6579c364f1120850414e0dc8"),
                "name": "hivemind",
                "community": self.community_id1,
                "activated": True,
                "options": {"platforms": [{"name": "github", "id": "platform2"}]},
                "metadata": {"key2": "value2"},
                "createdAt": datetime.now(),
                "updatedAt": datetime.now(),
            }
        )

        # Module with platform "discord" but not activated
        self.client["Core"]["modules"].insert_one(
            {
                "_id": ObjectId("6579c364f1120850414e0dc9"),
                "name": "hivemind",
                "community": self.community_id2,
                "activated": False,
                "options": {"platforms": [{"name": "discord", "id": "platform3"}]},
                "metadata": {"key3": "value3"},
                "createdAt": datetime.now(),
                "updatedAt": datetime.now(),
            }
        )

        # Module with different name but platform "discord"
        self.client["Core"]["modules"].insert_one(
            {
                "_id": ObjectId("6579c364f1120850414e0dca"),
                "name": "other-module",
                "community": self.community_id2,
                "activated": True,
                "options": {"platforms": [{"name": "discourse", "id": "platform4"}]},
                "metadata": {"key4": "value4"},
                "createdAt": datetime.now(),
                "updatedAt": datetime.now(),
            }
        )

        # Module with multiple platforms
        self.client["Core"]["modules"].insert_one(
            {
                "_id": ObjectId("6579c364f1120850414e0dcb"),
                "name": "hivemind",
                "community": self.community_id2,
                "activated": True,
                "options": {
                    "platforms": [
                        {"name": "discord", "id": "platform5"},
                        {"name": "github", "id": "platform6"},
                    ]
                },
                "metadata": {"key5": "value5"},
                "createdAt": datetime.now(),
                "updatedAt": datetime.now(),
            }
        )

    def test_query_with_platform(self):
        """Test querying modules with a specific platform"""
        modules_base = ModulesBase()
        result = modules_base.query(platform="discord")

        # Should return 2 modules (both activated hivemind modules with discord platform)
        self.assertEqual(len(result), 2)

        # Check that the results have the correct platform
        for module in result:
            self.assertEqual(module["name"], "hivemind")
            self.assertTrue(module["activated"])

            platform_names = [p["name"] for p in module["options"]["platforms"]]
            self.assertIn("discord", platform_names)

    def test_query_with_projection(self):
        """Test querying modules with a projection"""
        modules_base = ModulesBase()
        result = modules_base.query(
            platform="github", projection={"metadata": 1, "_id": 0}
        )

        # Should return 2 modules (both activated hivemind modules with github platform)
        self.assertEqual(len(result), 2)

        # Check that only the projected fields are returned
        for module in result:
            self.assertIn("metadata", module)
            self.assertNotIn("_id", module)
            self.assertNotIn("name", module)
            self.assertNotIn("community", module)
            self.assertNotIn("activated", module)
            self.assertNotIn("options", module)

    def test_query_no_matching_modules(self):
        """Test query when no modules match the criteria"""
        modules_base = ModulesBase()
        result = modules_base.query(platform="slack")

        # Should return an empty list
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    def test_query_multiple_platforms(self):
        """Test query results for a module with multiple platforms"""
        modules_base = ModulesBase()

        # Query for discord and check if the multi-platform module is included
        discord_results = modules_base.query(platform="discord")
        multi_platform_module = next(
            (m for m in discord_results if str(m["_id"]) == "6579c364f1120850414e0dcb"),
            None,
        )
        self.assertIsNotNone(multi_platform_module)

        # Query for github and check if the same multi-platform module is included
        github_results = modules_base.query(platform="github")
        multi_platform_module = next(
            (m for m in github_results if str(m["_id"]) == "6579c364f1120850414e0dcb"),
            None,
        )
        self.assertIsNotNone(multi_platform_module)

    def test_query_empty_platform_name(self):
        """Test query with empty platform name"""
        modules_base = ModulesBase()
        result = modules_base.query(platform="")

        # Should return an empty list since no module has an empty platform name
        self.assertEqual(len(result), 0)
