

import unittest
from clouduniqueid.clouds.bitbucket import BitbucketUniqueId


class TestBitbucketUniqueId(unittest.TestCase):

    def setUp(self):
        self.bitbucket_unique_id = BitbucketUniqueId()

    def test_get_unique_id_workspace(self):
        data = {
            "workspace": "my_workspace"
        }
        expected = "bitbucket:my_workspace"
        result = self.bitbucket_unique_id.get_unique_id(service="bitbucket", resourceType="workspace", data=data)
        self.assertEqual(result, expected)

    def test_get_unique_id_member(self):
        data = {
            "workspace": "my_workspace",
            "member": "my_member"
        }
        expected = "bitbucket:my_workspace:my_member"
        result = self.bitbucket_unique_id.get_unique_id(service="bitbucket", resourceType="member", data=data)
        self.assertEqual(result, expected)

    def test_unique_id_project(self):
        data = {
            "workspace": "my_workspace",
            "project": "my_project"
        }
        expected = "bitbucket:my_workspace:my_project"
        result = self.bitbucket_unique_id.get_unique_id(service="bitbucket", resourceType="project", data=data)
        self.assertEqual(result, expected)

    def test_unique_id_repository(self):
        data = {
            "workspace": "my_workspace",
            "project": "my_project",
            "repository": "my_repository"
        }
        expected = "bitbucket:my_workspace:my_project:my_repository"
        result = self.bitbucket_unique_id.get_unique_id(service="bitbucket", resourceType="repository", data=data)
        self.assertEqual(result, expected)

    def test_unique_id_invalid_service(self):
        data = {
            "workspace": "my_workspace"
        }
        result = self.bitbucket_unique_id.get_unique_id(service="invalid_service", resourceType="workspace", data=data)
        self.assertEqual(result, "")

    def test_unique_id_invalid_resource_type(self):
        data = {
            "workspace": "my_workspace"
        }
        result = self.bitbucket_unique_id.get_unique_id(service="bitbucket", resourceType="invalid_resource", data=data)
        self.assertEqual(result, "")

    def test_unique_id_missing_keys(self):
        data = {
            "workspace": "my_workspace"
        }
        result = self.bitbucket_unique_id.get_unique_id(service="bitbucket", resourceType="member", data=data)
        self.assertEqual(result, "")

    def test_unique_id_format_1(self):

        resource_type = "workspace"
        expected = "bitbucket:{workspace}"
        result = self.bitbucket_unique_id.get_unique_id_format(resourceType=resource_type)
        self.assertEqual(result, expected)

    def test_unique_id_format_2(self):
        resource_type = "project"
        expected = "bitbucket:{workspace}:{project}"
        result = self.bitbucket_unique_id.get_unique_id_format(resourceType=resource_type)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
