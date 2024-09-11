from clouduniqueid.clouds.gcp import GCPUniqueId


gcp = GCPUniqueId()
projectId = 'proj-123'
location = 'us-east-a1'


def test_gcp_iam_user():
    data = {'email': 'saccount@demo.com'}
    service = 'iam'
    resourceType = 'user'
    expected_id = "saccount@demo.com"

    out_id = gcp.get_unique_id(
        data=data, service=service, resourceType=resourceType,
    )

    assert out_id == expected_id.replace(" ", "")
