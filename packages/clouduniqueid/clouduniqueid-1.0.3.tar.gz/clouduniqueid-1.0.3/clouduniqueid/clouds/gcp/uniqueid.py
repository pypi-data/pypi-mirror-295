from typing import Dict


unique_id_patterns: Dict = {
    "iam": {
        "user": '{data["email".lower()]}',
        "service-account": '{data["email".lower()]}',
        "group": '{data["email".lower()]}',
        "domain": '{data["email".lower()]}',
        "role": '{get_role_id(data["name".lower()],projectId)}',
    },
    "apigateway": {
        "location": '{data["locationId".lower()]}',
        "api": 'projects/{projectId}/locations/{location}/apis/{data["ApiName".lower()]}',
        "config": 'projects/{projectId}/locations/{location}/apis/{data["ApiName".lower()]}/configs/{data["ApiConfigName".lower()}',
        "gateway": 'projects/{projectId}/locations/{location}/gateways/{data["GatewayName".lower()]}',
    },
    "bigtable": {
        "instance": 'projects/{projectId}/instances/{data["InstanceName".lower()]}',
        "cluster": 'projects/{projectId}/instances/{data["InstanceName".lower()]}/clusters/{data["ClusterName".lower()]}',
        "cluster-backup": 'projects/{projectId}/instances/{data["InstanceName".lower()]}/clusters/{data["ClusterName".lower()]}/backups/{data["BackupName".lower()]}',
        "table": 'projects/{projectId}/instances/{data["InstanceName".lower()]}/tables/{data["TableName".lower()]}',
    },
    "logging": {
        "metric": 'projects/{projectId}/metrics/{data["MetricName".lower()]}',
        "sink": 'projects/{projectId}/sinks/{data["Name".lower()]}',
    },
    "function": {
        "location": '{data["name".lower()]}',
        "function": 'projects/{projectId}/locations/{location}/functions/{data["FunctionName".lower()]}',
    },
}
