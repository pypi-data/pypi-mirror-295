from clouduniqueid.clouds.aws import AWSUniqueId

aws = AWSUniqueId()
region = 'us-east-1'
accountId = '12345'


def test_aws_ec2_instance():
    data = {'InstanceId': 'i-12345'}
    service = 'ec2'
    resourceType = 'instance'
    expected_id = "arn:aws:ec2:us-east-1:12345:instance/i-12345"

    out_id = aws.get_unique_id(
        data=data, service=service, region=region,
        accountId=accountId, resourceType=resourceType,
    )

    assert out_id == expected_id.replace(" ", "")


def test_aws_s3_bucket():
    data = {'bucketName': 'b12345'}
    service = 's3'
    resourceType = 'bucket'
    expected_id = "arn:aws:s3:::b12345"

    out_id = aws.get_unique_id(
        data=data, service=service, resourceType=resourceType,
    )

    assert out_id == expected_id.replace(" ", "")


def test_aws_lambda_function():
    data = {'FunctionName': 'f12345'}
    service = 'lambda'
    resourceType = 'function'
    expected_id = "arn:aws:lambda:us-east-1:12345:function:f12345"

    out_id = aws.get_unique_id(
        data=data, service=service, region=region,
        accountId=accountId, resourceType=resourceType,
    )

    assert out_id == expected_id.replace(" ", "")


def test_aws_lambda_function_alias():
    data = {'FunctionName': 'f12345', 'name': 'a12345'}
    service = 'lambda'
    resourceType = 'alias'
    expected_id = "arn:aws:lambda:us-east-1:12345:function:f12345:a12345"

    out_id = aws.get_unique_id(
        data=data, service=service, region=region,
        accountId=accountId, resourceType=resourceType,
    )

    assert out_id == expected_id.replace(" ", "")


def test_aws_lambda_function_alias_format():
    service = 'lambda'
    resourceType = 'alias'
    expected_id = "arn:{partition}:lambda:{region}:{accountId}:function:{FunctionName}:{Name}"

    out_id = aws.get_unique_id_format(
        service=service, resourceType=resourceType,
    )

    assert out_id == expected_id.replace(" ", "")
