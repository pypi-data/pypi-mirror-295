from typing import Dict

unique_id_patterns: Dict = {
    "a4b": {  # Alexa for Business
        "address-book": None,
        "conference-provider": None,
        "contact": None,
        "device": None,
        "network-profile": None,
        "profile": None,
        "room": None,
        "schedule": None,
        "skill-group": None,
        "user": None,
    },
    "access-analyzer": {  # IAM Access Analyzer
        "analyzer": None,
    },
    "acm": {  # AWS Certificate Manager
        "certificate": None,
    },
    "acm-pca": {  # AWS Certificate Manager Private Certificate Authority
        "certificate-authority": None,
    },
    "amplify": {  # AWS Amplify
        "apps": None,
    },
    "apigateway": {  # Manage Amazon API Gateway
        "rest-api": 'arn:{partition}:apigateway:{region}::/restapis/{data["id".lower()]}',
        "resource": 'arn:{partition}:apigateway:{region}::/restapis/{data["RestApiId".lower()]}/\
            resource/{data["id".lower()]}',
        "stage": 'arn:{partition}:apigateway:{region}::/restapis/{data["RestApiId".lower()]}/\
            stages/{data["StageName".lower()]}',
        "clientcertificates": 'arn:{partition}:apigateway:{region}::/clientcertificates/{data["ClientCertificateId".lower()]}',
    },
    "appconfig": {  # AWS AppConfig
        "application": None,
        "deploymentstrategy": None,
    },
    "appflow": {  # Amazon AppFlow
        "connectorprofile": None,
        "flow": None,
    },
    "appmesh": {  # AWS App Mesh
        "mesh": None,
    },
    "appmesh-preview": {  # AWS App Mesh Preview
        "mesh": None,
    },
    "appstream": {  # Amazon AppStream 2.0
        "fleet": None,
        "image": None,
        "image-builder": None,
        "stack": None,
    },
    "appsync": {  # AWS AppSync
        "apis": None,
    },
    "artifact": {  # AWS Artifact
        "agreement": None,
        "customer-agreement": None,
        "report-package": None,
    },
    "athena": {  # Amazon Athena
        "datacatalog": None,
        "workgroup": None,
    },
    "autoscaling": {  # Amazon EC2 Auto Scaling
        "autoScalingGroup": 'arn:{partition}:autoscaling:{region}:{accountId}:autoScalingGroup:\
            {data["groupId".lower()]}:autoScalingGroupName/{data["autoScalingGroupName".lower()]}',
        "launchConfiguration": 'arn:{partition}:autoscaling:{region}:{accountId}:launchConfiguration:\
            {data["launchConfigurationId".lower()]}:launchConfigurationName/{data["launchConfigurationName".lower()]}',
    },
    "aws-marketplace": {  # AWS Marketplace Catalog
    },
    "backup": {  # AWS Backup
        "backup-plan": None,
        "backup-vault": None,
    },
    "batch": {  # AWS Batch
        "job-definition": None,
        "job-queue": None,
    },
    "budgets": {  # AWS Budget Service
        "budget": None,
    },
    "cassandra": {  # Amazon Keyspaces (for Apache Cassandra)
        "": None,
    },
    "catalog": {  # AWS Service Catalog
        "portfolio": None,
        "product": None,
    },
    "chatbot": {  # AWS Chatbot
    },
    "chime": {  # Amazon Chime
        "meeting": None,
    },
    "cloud9": {  # AWS Cloud9
        "environment": None,
    },
    "clouddirectory": {  # Amazon Cloud Directory
        "directory": None,
        "schema": None,
    },
    "cloudformation": {  # AWS CloudFormation
        "changeSet": 'arn:{partition}:cloudformation:{region}:{accountId}:changeSet/{data["ChangeSetName".lower()]}/{data["Id".lower()]}',
        "stack": 'arn:{partition}:cloudformation:{region}:{accountId}:stack/{data["StackName".lower()]}/{data["Id".lower()]}',
        "stackset": 'arn:{partition}:cloudformation:{region}:{accountId}:stackset/{data["StackSetName".lower()]}:{data["Id".lower()]}',
    },
    "cloudfront": {  # Amazon CloudFront
        "distribution": 'arn:{partition}:cloudfront::{accountId}:distribution/{data["DistributionId".lower()]}',
        "origin-access-identity": 'arn:{partition}:cloudfront::{accountId}:origin-access-identity/{data["Id".lower()]}',
        "streaming-distribution": 'arn:{partition}:cloudfront::{accountId}:streaming-distribution/{data["DistributionId".lower()]}',
    },
    "cloudhsm": {  # AWS CloudHSM
        "backup": None,
        "cluster": None,
    },
    "cloudsearch": {  # Amazon CloudSearch
        "domain": None,
    },
    "cloudtrail": {  # AWS CloudTrail
        "trail": 'arn:{partition}:cloudtrail:{region}:{accountId}:trail/{data["Name".lower()]}',
    },
    "cloudwatch": {  # Amazon CloudWatch
        "alarm": 'arn:{partition}:cloudwatch:{region}:{accountId}:alarm:{data["AlarmName".lower()]}',
        "dashboard": 'arn:{partition}:cloudwatch::{region}:dashboard/{data["DashboardName".lower()]}',
        "insight-rule": 'arn:{partition}:cloudwatch:{region}:{accountId}:insight-rule/{data["InsightRuleName".lower()]}',
        "metric": 'arn:{partition}:cloudwatch::{region}:{accountId}:metric/{data["MetricName".lower()]}',
    },
    "codeartifact": {  # AWS CodeArtifact
        "domain": None,
        "package": None,
        "repository": None,
    },
    "codebuild": {  # AWS CodeBuild
        "build": None,
        "project": None,
        "report": None,
        "report-group": None,
    },
    "codecommit": {  # Amazon CodeGuru Reviewer
    },
    "codedeploy": {  # AWS CodeDeploy
        "application": None,
        "deploymentconfig": None,
        "deploymentgroup": None,
        "instance": None,
    },
    "codeguru-profiler": {  # Amazon CodeGuru Profiler
        "profilingGroup": None,
    },
    "codeguru-reviewer": {  # Amazon CodeGuru Reviewer
        ".+": None,
        "association": None,
    },
    "codepipeline": {  # AWS CodePipeline
        "actiontype": None,
        "webhook": None,
    },
    "codestar": {  # AWS CodeStar
        "project": None,
    },
    "codestar-connections": {  # AWS CodeStar Connections
        "connection": None,
    },
    "codestar-notifications": {  # AWS CodeStar Notifications
        "notificationrule": None,
    },
    "cognito-identity": {  # Amazon Cognito Identity
        "identitypool": None,
    },
    "cognito-idp": {  # Amazon Cognito User Pools
        "userpool": None,
    },
    "cognito-sync": {  # Amazon Cognito Sync
        "identitypool": None,
    },
    "comprehend": {  # Amazon Comprehend
        "document-classifier": None,
        "document-classifier-endpoint": None,
        "entity-recognizer": None,
    },
    "config": {  # AWS Config
        "aggregation-authorization": None,
        "config-aggregator": None,
        "config-rule": None,
        "conformance-pack": None,
        "organization-config-rule": None,
        "organization-conformance-pack": None,
        "remediation-configuration": None,
    },
    "connect": {  # Amazon Connect
        "instance": None,
    },
    "cur": {  # AWS Cost and Usage Report
        "definition": None,
    },
    "dataexchange": {  # AWS Data Exchange
        "data-sets": None,
        "jobs": None,
    },
    "datasync": {  # DataSync
        "agent": None,
        "location": None,
        "task": None,
    },
    "dax": {  # Amazon DynamoDB Accelerator (DAX)
        "cache": None,
    },
    "deepcomposer": {  # AWS DeepComposer
        "audio": None,
        "composition": None,
        "model": None,
    },
    "deeplens": {  # AWS DeepLens
        "device": None,
        "model": None,
        "project": None,
    },
    "deepracer": {  # AWS DeepRacer
        " evaluation_job": None,
        "leaderboard": None,
        "leaderboard_evaluation_job": None,
        "model": None,
        "track": None,
        "training_job": None,
    },
    "detective": {  # Amazon Detective
        "graph": None,
    },
    "devicefarm": {  # AWS Device Farm
        "artifact": None,
        "device": None,
        "deviceinstance": None,
        "devicepool": None,
        "instanceprofile": None,
        "job": None,
        "networkprofile": None,
        "project": None,
        "run": None,
        "sample": None,
        "session": None,
        "suite": None,
        "test": None,
        "testgrid-project": None,
        "testgrid-session": None,
        "upload": None,
        "vpceconfiguration": None,
    },
    "directconnect": {  # AWS Direct Connect
        "dx-gateway": None,
        "dxcon": None,
        "dxlag": None,
        "dxvif": None,
    },
    "dlm": {  # Amazon Data Lifecycle Manager
        "policy": None,
    },
    "dms": {  # AWS Database Migration Service
        "cert": None,
        "endpoint": None,
        "es": None,
        "rep": None,
        "subgrp": None,
        "task": None,
    },
    "ds": {  # AWS Directory Service
        "directory": None,
    },
    "dynamodb": {  # Amazon DynamoDB
        "global-table": 'arn:{partition}:dynamodb::{accountId}:global-table/{data["GlobalTableName".lower()]}',
        "table": 'arn:{partition}:dynamodb:{region}:{accountId}:table/{data["TableName".lower()]}',
        "index": 'arn:{partition}:dynamodb:{region}:{accountId}:table/{data["TableName".lower()]}/\
            index/{data["IndexName".lower()]}',
    },
    "ec2": {  # AWS Systems Manager
        "capacity-reservation": 'arn:{partition}:ec2:{region}:{accountId}:capacity-reservation/\
            {data["CapacityReservationId".lower()]}',
        "client-vpn-endpoint": 'arn:{partition}:ec2:{region}:{accountId}:client-vpn-endpoint/\
            {data["ClientVpnEndpointId".lower()]}',
        "customer-gateway": 'arn:{partition}:ec2:{region}:{accountId}:customer-gateway/\
            {data["CustomerGatewayId".lower()]}',
        "dedicated-host": 'arn:{partition}:ec2:{region}:{accountId}:dedicated-host/{data["DedicatedHostId".lower()]}',
        "dhcp-options": 'arn:{partition}:ec2:{region}:{accountId}:dhcp-options/{data["DhcpOptionsId".lower()]}',
        "elastic-gpu": 'arn:{partition}:ec2:{region}:{accountId}:elastic-gpu/{data["ElasticGpuId".lower()]}',
        "fpga-image": 'arn:{partition}:ec2:{region}::fpga-image/{data["FpgaImageId".lower()]}',
        "image": 'arn:{partition}:ec2:{region}::image/{data["ImageId".lower()]}',
        "instance": 'arn:{partition}:ec2:{region}:{accountId}:instance/{data["InstanceId".lower()]}',
        "internet-gateway": 'arn:{partition}:ec2:{region}:{accountId}:internet-gateway/\
            {data["InternetGatewayId".lower()]}',
        "key-pair": 'arn:{partition}:ec2:{region}:{accountId}:key-pair/{data["KeyName".lower()]}',
        "launch-template": 'arn:{partition}:ec2:{region}:{accountId}:launch-template/\
            {data["LaunchTemplateId".lower()]}',
        "local-gateway": 'arn:{partition}:ec2:{region}:{accountId}:local-gateway/{data["LocalGatewayId".lower()]}',
        "local-gateway-route-table": 'arn:{partition}:ec2:{region}:{accountId}:local-gateway-route-table/\
            {data["LocalGatewayRoutetableId".lower()]}',
        "local-gateway-route-table-virtual-interface-group-association": 'arn:{partition}:ec2:{region}:{accountId}:\
            local-gateway-route-table-virtual-interface-group-association/\
                {data["LocalGatewayRouteTableVirtualInterfaceGroupAssociationId".lower()]}',
        "local-gateway-route-table-vpc-association": 'arn:{partition}:ec2:{region}:{accountId}:\
            local-gateway-route-table-vpc-association/{data["LocalGatewayRouteTableVpcAssociationId".lower()]}',
        "local-gateway-virtual-interface": 'arn:{partition}:ec2:{region}:{accountId}:\
            local-gateway-virtual-interface/{data["LocalGatewayVirtualInterfaceId".lower()]}',
        "local-gateway-virtual-interface-group": 'arn:{partition}:ec2:{region}:{accountId}:\
            local-gateway-virtual-interface-group/{data["LocalGatewayVirtualInterfaceGroupId".lower()]}',
        "network-acl": 'arn:{partition}:ec2:{region}:{accountId}:network-acl/{data["NaclId".lower()]}',
        "network-interface": 'arn:{partition}:ec2:{region}:{accountId}:network-interface/\
            {data["NetworkInterfaceId".lower()]}',
        "placement-group": 'arn:{partition}:ec2:{region}:{accountId}:placement-group/\
            {data["PlacementGroupName".lower()]}',
        "reserved-instances": 'arn:{partition}:ec2:{region}:{accountId}:reserved-instances/\
            {data["ReservationId".lower()]}',
        "route-table": 'arn:{partition}:ec2:{region}:{accountId}:route-table/{data["RouteTableId".lower()]}',
        "security-group": 'arn:{partition}:ec2:{region}:{accountId}:security-group/{data["SecurityGroupId".lower()]}',
        "snapshot": 'arn:{partition}:ec2:{region}::snapshot/{data["SnapshotId".lower()]}',
        "spot-instances-request": 'arn:{partition}:ec2:{region}:{accountId}:spot-instances-request/\
            {data["SpotInstanceRequestId".lower()]}',
        "subnet": 'arn:{partition}:ec2:{region}:{accountId}:subnet/{data["SubnetId".lower()]}',
        "traffic-mirror-filter": 'arn:{partition}:ec2:{region}:{accountId}:traffic-mirror-filter/\
            {data["TrafficMirrorFilterId".lower()]}',
        "traffic-mirror-filter-rule": 'arn:{partition}:ec2:{region}:{accountId}:traffic-mirror-filter-rule/\
            {data["TrafficMirrorFilterRuleId".lower()]}',
        "traffic-mirror-session": 'arn:{partition}:ec2:{region}:{accountId}:traffic-mirror-session/\
            {data["TrafficMirrorSessionId".lower()]}',
        "traffic-mirror-target": 'arn:{partition}:ec2:{region}:{accountId}:traffic-mirror-target/\
            {data["TrafficMirrorTargetId".lower()]}',
        "transit-gateway": 'arn:{partition}:ec2:{region}:{accountId}:transit-gateway/\
            {data["TransitGatewayId".lower()]}',
        "transit-gateway-attachment": 'arn:{partition}:ec2:{region}:{accountId}:transit-gateway-attachment/\
            {data["TransitGatewayAttachmentId".lower()]}',
        "transit-gateway-multicast-domain": 'arn:{partition}:ec2:{region}:{accountId}:\
            transit-gateway-multicast-domain/{data["TransitGatewayMulticastDomainId".lower()]}',
        "transit-gateway-route-table": 'arn:{partition}:ec2:{region}:{accountId}:\
            transit-gateway-route-table/{data["TransitGatewayRouteTableId".lower()]}',
        "volume": 'arn:{partition}:ec2:{region}:{accountId}:volume/{data["VolumeId".lower()]}',
        "vpc": 'arn:{partition}:ec2:{region}:{accountId}:vpc/{data["VpcId".lower()]}',
        "vpc-endpoint": 'arn:{partition}:ec2:{region}:{accountId}:vpc-endpoint/{data["VpcEndpointId".lower()]}',
        "vpc-endpoint-service": 'arn:{partition}:ec2:{region}:{accountId}:vpc-endpoint-service/\
            {data["VpcEndpointServiceId".lower()]}',
        "vpc-flow-log": 'arn:{partition}:ec2:{region}:{accountId}:vpc-flow-log/{data["VpcFlowLogId".lower()]}',
        "vpc-peering-connection": 'arn:{partition}:ec2:{region}:{accountId}:vpc-peering-connection/\
            {data["VpcPeeringConnectionId".lower()]}',
        "vpn-connection": 'arn:{partition}:ec2:{region}:{accountId}:vpn-connection/{data["VpnConnectionId".lower()]}',
        "vpn-gateway": 'arn:{partition}:ec2:{region}:{accountId}:vpn-gateway/{data["VpnGatewayId".lower()]}',
        "elastic-ip": 'arn:{partition}:ec2:{region}:{accountId}:elastic-ip/{data["AllocationId".lower()]}',
    },
    "ecr": {  # Amazon Elastic Container Registry
        "repository": 'arn:{partition}:ecr:{region}:{accountId}:repository/{data["RepositoryName".lower()]}',
        "image": '{data["repoUri".lower()]}:{data["imageTag".lower()]}',
    },
    "ecs": {  # Amazon Elastic Container Service
        "cluster": 'arn:{partition}:ecs:{region}:{accountId}:cluster/{data["ClusterName".lower()]}',
        "container-instance": 'arn:{partition}:ecs:{region}:{accountId}:container-instance/\
            {data["ClusterName".lower()]}/{data["ContainerInstanceId".lower()]}',
        "service": 'arn:{partition}:ecs:{region}:{accountId}:service/{data["ClusterName".lower()]}/\
            {data["ServiceName".lower()]}',
        "task": 'arn:{partition}:ecs:{region}:{accountId}:task/{data["ClusterName".lower()]}/{data["TaskId".lower()]}',
        "task-definition": 'arn:{partition}:ecs:{region}:{accountId}:task-definition/\
            {data["TaskDefinitionFamilyName".lower()]}:{data["TaskDefinitionRevisionNumber".lower()]}',
    },
    "eks": {  # Amazon Elastic Container Service for Kubernetes
        "cluster": 'arn:{partition}:eks:{region}:{accountId}:cluster/{data["ClusterName".lower()]}',
        "fargateprofile": 'arn:{partition}:eks:{region}:{accountId}:fargateprofile/{data["ClusterName".lower()]}/\
            {data["FargateProfileName".lower()]}/{data["UUID.lower()]}',
        "nodegroup": 'arn:{partition}:eks:{region}:{accountId}:nodegroup/{data["ClusterName".lower()]}/\
            {data["NodegroupName".lower()]}/{data["UUID.lower()]}',
    },
    "elastic-inference": {  # Amazon Elastic Inference
        "elastic-inference-accelerator": None,
    },
    "elasticbeanstalk": {  # AWS Elastic Beanstalk
        "application": None,
        "applicationversion": None,
        "configurationtemplate": None,
        "environment": None,
        "platform": None,
        "solutionstack": None,
    },
    "elasticfilesystem": {  # Amazon Elastic File System
        "access-point": None,
        "file-system": None,
    },
    "elasticloadbalancing": {  # AWS WAF V2
        "listener": 'arn:{partition}:elasticloadbalancing:{region}:{accountId}:\
            listener/app/{data["LoadBalancerName".lower()]}/{data["LoadBalancerId".lower()]}/\
                {data["ListenerId".lower()]}',
        "listener-rule": 'arn:{partition}:elasticloadbalancing:{region}:{accountId}:\
            listener-rule/net/{data["LoadBalancerName".lower()]}/{data["LoadBalancerId".lower()]}/\
                {data["ListenerId".lower()]}/{data["ListenerRuleId".lower()]}',
        "loadbalancer": 'arn:{partition}:elasticloadbalancing:{region}:{accountId}:loadbalancer/\
            {data["LoadBalancerName".lower()]}',
        "targetgroup": 'arn:{partition}:elasticloadbalancing:{region}:{accountId}:targetgroup/\
            {data["TargetGroupName".lower()]}/{data["TargetGroupId".lower()]}',
    },
    "elasticmapreduce": {  # Amazon Elastic MapReduce
        "cluster": None,
        "editor": None,
    },
    "elastictranscoder": {  # Amazon Elastic Transcoder
        "job": None,
        "pipeline": None,
        "preset": None,
    },
    "es": {  # Amazon Elasticsearch Service
        "domain": 'arn:{partition}:es:{region}:{accountId}:domain/{data["Name".lower()]}',
    },
    "elasticache": {  # Amazon Elasticache Service
        "cluster": 'arn:{partition}:elasticache:{region}:{accountId}:cluster:{data["CacheClusterId".lower()]}',
        "reserved-instance": 'arn:{partition}:elasticache:{region}:{accountId}:reserved-instance:{data["ReservedCacheNodeId".lower()]}',
    },
    "events": {  # Amazon EventBridge
        "event-bus": 'arn:{partition}:events:{region}:{accountId}:event-bus/{data["EventBusName".lower()]}',
        "event-source": None,
        "rule": 'arn:{partition}:events:{region}:{accountId}:rule/{data["RuleName".lower()]}',
    },
    "execute-api": {  # Amazon API Gateway
    },
    "firehose": {  # Amazon Kinesis Firehose
        "deliverystream": None,
    },
    "fms": {  # AWS Firewall Manager
        "policy": None,
    },
    "forecast": {  # Amazon Forecast
        "algorithm": None,
        "dataset": None,
        "dataset-group": None,
        "dataset-import-job": None,
        "forecast": None,
        "forecast-export-job": None,
        "predictor": None,
    },
    "freertos": {  # Amazon FreeRTOS
        "configuration": None,
    },
    "fsx": {  # Amazon FSx
        "backup": None,
        "file-system": None,
        "task": None,
    },
    "gamelift": {  # Amazon GameLift
        "alias": None,
        "build": None,
        "fleet": None,
        "gamesessionqueue": None,
        "matchmakingconfiguration": None,
        "matchmakingruleset": None,
        "script": None,
    },
    "glacier": {  # Amazon Glacier
        "vaults": None,
    },
    "globalaccelerator": {  # AWS Global Accelerator
        "accelerator": None,
    },
    "glue": {  # AWS Glue
        "catalog": None,
        "connection": None,
        "crawler": None,
        "database": None,
        "devendpoint": None,
        "job": None,
        "mlTransform": None,
        "table": None,
        "tableVersion": None,
        "trigger": None,
        "userDefinedFunction": None,
        "workflow": None,
    },
    "greengrass": {  # AWS IoT Greengrass
        "": None,
    },
    "groundstation": {  # AWS Ground Station
        "config": None,
        "contact": None,
        "dataflow-endpoint-group": None,
        "groundstation": None,
        "mission-profile": None,
        "satellite": None,
    },
    "guardduty": {  # Amazon GuardDuty
        "detector": None,
    },
    "health": {  # AWS Health APIs and Notifications
        "event": None,
    },
    "honeycode": {  # Amazon Honeycode
        "screen": None,
        "screen-automation": None,
    },
    "iam": {  # AWS Security Token Service
        "access-report": 'arn:{partition}:iam::{accountId}:access-report/{data["EntityPath".lower()]}',
        "assumed-role": 'arn:{partition}:iam::{accountId}:assumed-role/{data["RoleName".lower()]}/\
            {data["RoleSessionName".lower()]}',
        "federated-user": 'arn:{partition}:iam::{accountId}:federated-user/{data["UserName".lower()]}',
        "group": 'arn:{partition}:iam::{accountId}:group/{data["GroupName".lower()]}',
        "instance-profile": 'arn:{partition}:iam::{accountId}:instance-profile/{data["InstanceProfileName".lower()]}',
        "mfa": 'arn:{partition}:iam::{accountId}:mfa/{data["MfaTokenId".lower()]}',
        "oidc-provider": 'arn:{partition}:iam::{accountId}:oidc-provider/{data["OidcProviderName".lower()]}',
        "policy": 'arn:{partition}:iam::{accountId}:policy/{data["PolicyName".lower()]}',
        "role": 'arn:{partition}:iam::{accountId}:role/{data["RoleName".lower()]}',
        "saml-provider": 'arn:{partition}:iam::{accountId}:saml-provider/{data["SamlProviderName".lower()]}',
        "server-certificate": 'arn:{partition}:iam::{accountId}:server-certificate/{data["CertificateName".lower()]}',
        "sms-mfa": 'arn:{partition}:iam::{accountId}:sms-mfa/{data["MfaTokenId".lower()]}',
        "user": 'arn:{partition}:iam::{accountId}:user/{data["UserName".lower()]}',
        "user-access-key": '{data["AccessKeyId".lower()]}',
        "policy-statement": '{data["PolicyId".lower()]}/statement/{data["StatementId".lower()]}',
        "service-access": 'hashlib.md5((data["PrincipalARN".lower()] + data["ServiceName".lower()]).encode("UTF-8")).hexdigest()',
    },
    "imagebuilder": {  # Amazon EC2 Image Builder
        "component": None,
        "distribution-configuration": None,
        "image": None,
        "image-pipeline": None,
        "image-recipe": None,
        "infrastructure-configuration": None,
    },
    "iot": {  # AWS IoT
        "authorizer": None,
        "billinggroup": None,
        "cacert": None,
        "cert": None,
        "client": None,
        "dimension": None,
        "index": None,
        "job": None,
        "mitigationaction": None,
        "otaupdate": None,
        "policy": None,
        "provisioningtemplate": None,
        "rolealias": None,
        "rule": None,
        "scheduledaudit": None,
        "securityprofile": None,
        "stream": None,
        "thing": None,
        "thinggroup": None,
        "thingtype": None,
        "topic": None,
        "topicfilter": None,
        "tunnel": None,
    },
    "iot1click": {  # AWS IoT 1-Click
        "devices": None,
        "projects": None,
    },
    "iotanalytics": {  # AWS IoT Analytics
        "channel": None,
        "dataset": None,
        "datastore": None,
        "pipeline": None,
    },
    "iotevents": {  # AWS IoT Events
        "detectorModel": None,
        "input": None,
    },
    "iotsitewise": {  # AWS IoT SiteWise
        "access-policy": None,
        "asset": None,
        "asset-model": None,
        "dashboard": None,
        "gateway": None,
        "portal": None,
        "project": None,
    },
    "iotthingsgraph": {  # AWS IoT Things Graph
        "Deployment": None,
        "System": None,
        "Workflow": None,
    },
    "kafka": {  # Amazon Managed Streaming for Kafka
        "cluster": None,
    },
    "kendra": {  # Amazon Kendra
        "index": None,
    },
    "kinesis": {  # Amazon Kinesis
        "stream": None,
    },
    "kinesisanalytics": {  # Amazon Kinesis Analytics V2
        "application": None,
    },
    "kinesisvideo": {  # Amazon Kinesis Video Streams
        "channel": None,
        "stream": None,
    },
    "kms": {  # AWS Key Management Service
        "alias": 'arn:{partition}:kms:{region}:{accountId}:{data["AliasName".lower()]}',
        "key": 'arn:{partition}:kms:{region}:{accountId}:key/{data["KeyId".lower()]}',
    },
    "lambda": {  # AWS Lambda
        "event-source-mapping": 'arn:{partition}:lambda:{region}:{accountId}:event-source-mapping:\
            {data["UUID".lower()]}',
        "function": 'arn:{partition}:lambda:{region}:{accountId}:function:{data["FunctionName".lower()]}',
        "code-signing-config": 'arn:{partition}:lambda:{region}:{accountId}:code-signing-config:\
            {data["CodeSigningConfigId".lower()]}',
        "alias": 'arn:{partition}:lambda:{region}:{accountId}:function:{data["FunctionName".lower()]}:\
            {data["Name".lower()]}',
        "version": 'arn:{partition}:lambda:{region}:{accountId}:function:{data["FunctionName".lower()]}:\
            {data["Version".lower()]}',
        "layer": 'arn:{partition}:lambda:{region}:{accountId}:layer:{data["LayerName".lower()]}',
        "layer-version": 'arn:{partition}:lambda:{region}:{accountId}:layer:{data["LayerName".lower()]}:\
            {data["Version".lower()]}',
    },
    "lex": {  # Amazon Lex
        "bot": None,
        "bot-channel": None,
        "intent": None,
        "slottype": None,
    },
    "license-manager": {  # AWS License Manager
        "license-configuration": None,
    },
    "lightsail": {  # Amazon Lightsail
        "CloudFormationStackRecord": None,
        "Disk": None,
        "DiskSnapshot": None,
        "Domain": None,
        "ExportSnapshotRecord": None,
        "Instance": None,
        "InstanceSnapshot": None,
        "KeyPair": None,
        "LoadBalancer": None,
        "LoadBalancerTlsCertificate": None,
        "PeeredVpc": None,
        "RelationalDatabase": None,
        "RelationalDatabaseSnapshot": None,
        "StaticIp": None,
    },
    "logs": {  # Amazon CloudWatch Logs
        "log-group": 'arn:{partition}:logs:{region}:{accountId}:log-group:{data["LogGroupName".lower()]}',
    },
    "machinelearning": {  # Amazon Machine Learning
        "batchprediction": None,
        "datasource": None,
        "evaluation": None,
        "mlmodel": None,
    },
    "macie2": {  # Amazon Macie
        "classification-job": None,
        "custom-data-identifier": None,
        "findings-filter": None,
        "member": None,
    },
    "managedblockchain": {  # Amazon Managed Blockchain
        "invitations": None,
        "members": None,
        "networks": None,
        "nodes": None,
        "proposals": None,
    },
    "mediaconnect": {  # AWS Elemental MediaConnect
        "entitlement": None,
        "flow": None,
        "output": None,
        "source": None,
    },
    "mediaconvert": {  # AWS Elemental MediaConvert
        "certificates": None,
        "jobTemplates": None,
        "jobs": None,
        "presets": None,
        "queues": None,
    },
    "medialive": {  # AWS Elemental MediaLive
        "channel": None,
        "input": None,
        "inputDevice": None,
        "inputSecurityGroup": None,
        "multiplex": None,
        "offering": None,
        "reservation": None,
    },
    "mediapackage": {  # AWS Elemental MediaPackage
        "channels": None,
        "origin_endpoints": None,
    },
    "mediapackage-vod": {  # AWS Elemental MediaPackage VOD
        "assets": None,
        "packaging-configurations": None,
        "packaging-groups": None,
    },
    "mediastore": {  # AWS Elemental MediaStore
        "container": None,
    },
    "mediatailor": {  # AWS Elemental MediaTailor
        "playbackConfiguration": None,
    },
    "mgh": {  # AWS Migration Hub
        "progressUpdateStream": None,
    },
    "mobilehub": {  # AWS Mobile Hub
        "project": None,
    },
    "mobiletargeting": {  # Amazon Pinpoint
        "apps": None,
        "recommenders": None,
        "templates": None,
    },
    "mq": {  # Amazon MQ
        "broker": None,
        "configuration": None,
    },
    "neptune-db": {  # Amazon Neptune
    },
    "networkmanager": {  # Network Manager
        "device": None,
        "global-network": None,
        "link": None,
        "site": None,
    },
    "opsworks": {  # AWS OpsWorks
        "stack": None,
    },
    "organizations": {  # AWS Organizations
        "account": None,
        "handshake": None,
        "organization": None,
        "ou": None,
        "policy": None,
        "root": None,
    },
    "outposts": {  # AWS Outposts
        "order": None,
        "outpost": None,
        "site": None,
    },
    "personalize": {  # Amazon Personalize
        "algorithm": None,
        "campaign": None,
        "dataset": None,
        "dataset-group": None,
        "dataset-import-job": None,
        "event-tracker": None,
        "feature-transformation": None,
        "recipe": None,
        "schema": None,
        "solution": None,
    },
    "pi": {  # AWS Performance Insights
        "metrics": None,
    },
    "polly": {  # Amazon Polly
        "lexicon": None,
    },
    "qldb": {  # Amazon QLDB
        "ledger": None,
        "stream": None,
    },
    "quicksight": {  # Amazon QuickSight
        "assignment": None,
        "dashboard": None,
        "group": None,
        "template": None,
        "user": None,
    },
    "ram": {  # AWS Resource Access Manager
        "permission": None,
        "resource-share": None,
        "resource-share-invitation": None,
    },
    "rds": {  # Amazon RDS
        "cluster": 'arn:{partition}:rds:{region}:{accountId}:cluster:{data["DbClusterInstanceName".lower()]}',
        "cluster-endpoint": 'arn:{partition}:rds:{region}:{accountId}:cluster-endpoint:\
            {data["DbClusterEndpoint".lower()]}',
        "cluster-pg": 'arn:{partition}:rds:{region}:{accountId}:cluster-pg:\
            {data["ClusterParameterGroupName".lower()]}',
        "cluster-snapshot": 'arn:{partition}:rds:{region}:{accountId}:\
            cluster-snapshot:{data["ClusterSnapshotName".lower()]}',
        "db": 'arn:{partition}:rds:{region}:{accountId}:db:{data["DbInstanceName".lower()]}',
        "db-proxy": 'arn:{partition}:rds:{region}:{accountId}:db-proxy:{data["DbProxyId".lower()]}',
        "es": 'arn:{partition}:rds:{region}:{accountId}:es:{data["SubscriptionName".lower()]}',
        "og": 'arn:{partition}:rds:{region}:{accountId}:og:{data["OptionGroupName".lower()]}',
        "pg": 'arn:{partition}:rds:{region}:{accountId}:pg:{data["ParameterGroupName".lower()]}',
        "ri": 'arn:{partition}:rds:{region}:{accountId}:ri:{data["ReservedDbInstanceName".lower()]}',
        "secgrp": 'arn:{partition}:rds:{region}:{accountId}:secgrp:{data["SecurityGroupName".lower()]}',
        "snapshot": 'arn:{partition}:rds:{region}:{accountId}:snapshot:{data["SnapshotName".lower()]}',
        "subgrp": 'arn:{partition}:rds:{region}:{accountId}:subgrp:{data["SubnetGroupName".lower()]}',
        "target": 'arn:{partition}:rds:{region}:{accountId}:target:{data["TargetId".lower()]}',
        "target-group": 'arn:{partition}:rds:{region}:{accountId}:target-group:{data["TargetGroupId".lower()]}',
    },
    "rds-db": {  # Amazon RDS IAM Authentication
        "dbuser": None,
    },
    "redshift": {  # Amazon Redshift
        "cluster": 'arn:{partition}:redshift:{region}:{accountId}:cluster:{data["ClusterName".lower()]}',
        "dbgroup": 'arn:{partition}:redshift:{region}:{accountId}:dbgroup:{data["ClusterName".lower()]}/\
            {data["DbGroup".lower()]}',
        "dbname": 'arn:{partition}:redshift:{region}:{accountId}:dbname:{data["ClusterName".lower()]}/\
            {data["DbName".lower()]}',
        "dbuser": 'arn:{partition}:redshift:{region}:{accountId}:dbuser:{data["ClusterName".lower()]}/\
            {data["DbUser".lower()]}',
        "eventsubscription": 'arn:{partition}:redshift:{region}:{accountId}:eventsubscription:\
            {data["EventSubscriptionName".lower()]}',
        "hsmclientcertificate": 'arn:{partition}:redshift:{region}:{accountId}:hsmclientcertificate:\
            {data["HSMClientCertificateId".lower()]}',
        "hsmconfiguration": 'arn:{partition}:redshift:{region}:{accountId}:hsmconfiguration:\
            {data["HSMConfigurationId".lower()]}',
        "parametergroup": 'arn:{partition}:redshift:{region}:{accountId}:parametergroup:\
            {data["ParameterGroupName".lower()]}',
        "securitygroup": 'arn:{partition}:redshift:{region}:{accountId}:securitygroup:\
            {data["SecurityGroupName".lower()]}/ec2securitygroup/{data["Owner".lower()]}/\
                {data["Ec2SecurityGroupId".lower()]}',
        "securitygroupingress": 'arn:{partition}:redshift:{region}:{accountId}:\
            securitygroupingress:{data["SecurityGroupName".lower()]}',
        "snapshot": 'arn:{partition}:redshift:{region}:{accountId}:snapshot:{data["ClusterName".lower()]}/\
            {data["SnapshotName".lower()]}',
        "snapshotcopygrant": 'arn:{partition}:redshift:{region}:{accountId}:snapshotcopygrant:\
            {data["SnapshotCopyGrantName".lower()]}',
        "snapshotschedule": 'arn:{partition}:redshift:{region}:{accountId}:snapshotschedule:\
            {data["ParameterGroupName".lower()]}',
        "subnetgroup": 'arn:{partition}:redshift:{region}:{accountId}:subnetgroup:{data["SubnetGroupName".lower()]}',
        "reserved-node": 'arn:{partition}:redshift:{region}:{accountId}:reserved-node/{data["ReservedNodeId".lower()]}',
    },
    "rekognition": {  # Amazon Rekognition
        "collection": None,
        "project": None,
        "streamprocessor": None,
    },
    "resource-groups": {  # AWS Resource Groups
        "group": None,
    },
    "robomaker": {  # AWS RoboMaker
        "deployment-fleet": None,
        "deployment-job": None,
        "robot": None,
        "robot-application": None,
        "simulation-application": None,
        "simulation-job": None,
        "simulation-job-batch": None,
    },
    "route53": {  # Amazon Route 53
        "change": 'arn:{partition}:route53:::change/{data["Id".lower()]}',
        "delegationset": 'arn:{partition}:route53:::delegationset/{data["Id".lower()]}',
        "healthcheck": 'arn:{partition}:route53:::healthcheck/{data["Id".lower()]}',
        "hostedzone": 'arn:{partition}:route53:::hostedzone/{data["Id".lower()]}',
        "queryloggingconfig": 'arn:{partition}:route53:::queryloggingconfig/{data["Id".lower()]}',
        "trafficpolicy": 'arn:{partition}:route53:::trafficpolicy/{data["Id".lower()]}',
        "trafficpolicyinstance": 'arn:{partition}:route53:::trafficpolicyinstance/{data["Id".lower()]}',
        "dns-record": 'arn:{partition}:route53:::recordset/{data["Id".lower()]}',
        "domain": '{data["DomainName".lower()]}',
    },
    "route53resolver": {  # Amazon Route 53 Resolver
        "resolver-endpoint": None,
        "resolver-rule": None,
    },
    "s3": {  # Amazon S3
        "bucket": 'arn:{partition}:s3:::{data["bucketName".lower()]}',
        "acl": 'hashlib.sha256(data.encode("utf8")).hexdigest()',
        "accesspoint": None,
        "job": None,
    },
    "sagemaker": {  # Amazon SageMaker
        "algorithm": None,
        "app": None,
        "automl-job": None,
        "code-repository": None,
        "compilation-job": None,
        "domain": None,
        "endpoint": None,
        "endpoint-config": None,
        "experiment": None,
        "experiment-trial": None,
        "experiment-trial-component": None,
        "flow-definition": None,
        "human-loop": None,
        "human-task-ui": None,
        "hyper-parameter-tuning-job": None,
        "labeling-job": None,
        "model": None,
        "model-package": None,
        "monitoring-schedule": None,
        "notebook-instance": None,
        "notebook-instance-lifecycle-config": None,
        "processing-job": None,
        "training-job": None,
        "transform-job": None,
        "user-profile": None,
        "workforce": None,
        "workteam": None,
    },
    "savingsplans": {  # AWS Savings Plans
        "savingsplan": None,
    },
    "schemas": {  # Amazon EventBridge Schemas
        "discoverer": None,
        "registry": None,
        "schema": None,
    },
    "sdb": {  # Amazon SimpleDB
        "domain": None,
    },
    "secretsmanager": {  # AWS Secrets Manager
        "secret": None,
    },
    "securityhub": {  # AWS Security Hub
        "hub": None,
        "product": None,
    },
    "serverlessrepo": {  # AWS Serverless Application Repository
        "applications": None,
    },
    "servicediscovery": {  # AWS Cloud Map
        "namespace": None,
        "service": None,
    },
    "servicequotas": {  # Service Quotas
    },
    "ses": {  # Amazon SES
        "configuration-set": 'arn:{partition}:ses:{region}:{accountId}:configuration-set/{data["ConfigurationSetName".lower()]}',
        "custom-verification-email-template": 'arn:{partition}:ses:{region}:{accountId}:custom-verification-email-template/{data["TemplateName".lower()]}',
        "dedicated-ip-pool": None,
        "deliverability-test-report": None,
        "identity": 'arn:{partition}:ses:{region}:{accountId}:identity/{data["IdentityName".lower()]}',
        "receipt-filter": None,
        "receipt-rule-set": None,
        "template": 'arn:{partition}:ses:{region}:{accountId}:template/{data["TemplateName".lower()]}',
    },
    "shield": {  # AWS Shield
        "attack": None,
        "protection": None,
    },
    "signer": {  # AWS Code Signing for Amazon FreeRTOS
        "": None,
    },
    "sns": {  # Amazon SNS
        "topic": 'arn:{partition}:sns:{region}:{accountId}:{data["TopicName".lower()]}',
    },
    "sqs": {  # Amazon SQS
        "queue": 'arn:{partition}:sqs:{region}:{accountId}:{data["QueueName".lower()]}',
    },
    "ssm": {  # AWS Systems Manager
        "association": None,
        "automation-definition": None,
        "automation-execution": None,
        "document": None,
        "maintenancewindow": None,
        "managed-instance": None,
        "managed-instance-inventory": None,
        "opsitem": None,
        "parameter": None,
        "patchbaseline": None,
        "resource-data-sync": None,
        "servicesetting": None,
        "session": None,
        "windowtarget": None,
        "windowtask": None,
    },
    "states": {  # AWS Step Functions
        "activity": None,
        "execution": None,
        "stateMachine": None,
    },
    "storagegateway": {  # Amazon Storage Gateway
        "gateway": None,
        "share": None,
        "tape": None,
    },
    "sumerian": {  # Amazon Sumerian
        "project": None,
    },
    "swf": {  # Amazon Simple Workflow Service
        "domain": None,
    },
    "synthetics": {  # Amazon CloudWatch Synthetics
        "canary": None,
    },
    "transfer": {  # AWS Transfer for SFTP
        "server": None,
        "user": None,
    },
    "trustedadvisor": {  # AWS Trusted Advisor
        "checks": None,
    },
    "waf": {  # AWS WAF
        "bytematchset": None,
        "geomatchset": None,
        "ipset": None,
        "ratebasedrule": None,
        "regexmatch": None,
        "regexpatternset": None,
        "rule": None,
        "rulegroup": None,
        "sizeconstraintset": None,
        "sqlinjectionset": None,
        "webacl": None,
        "xssmatchset": None,
    },
    "waf-regional": {  # AWS WAF Regional
        "bytematchset": None,
        "geomatchset": None,
        "ipset": None,
        "ratebasedrule": None,
        "regexmatch": None,
        "regexpatternset": None,
        "rule": None,
        "rulegroup": None,
        "sizeconstraintset": None,
        "sqlinjectionset": None,
        "webacl": None,
        "xssmatchset": None,
    },
    "wafv2": {  # AWS WAF V2
    },
    "wellarchitected": {  # AWS Well-Architected Tool
        "workload": None,
    },
    "worklink": {  # Amazon WorkLink
        "fleet": None,
    },
    "workmail": {  # Amazon WorkMail
        "organization": None,
    },
    "workmailmessageflow": {  # Amazon WorkMail Message Flow
        "message": None,
    },
    "workspaces": {  # Amazon WorkSpaces
        "directory": None,
        "workspace": None,
        "workspacebundle": None,
        "workspaceipgroup": None,
    },
    "xray": {  # AWS X-Ray
        "group": None,
        "sampling-rule": None,
    },
}
