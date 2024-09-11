import logging
import re
from typing import Dict

from .uniqueid import unique_id_patterns

logger = logging.getLogger(__name__)


def check_missing_data_keys(dataKeys: list, uniqueIdFormat: str):
    uniqueIdKeys = re.findall(r"{(.*?)}", uniqueIdFormat)
    dataKeys.extend(["location", "projectid", "get_role_id(name,projectid)"])
    missingKeys = []
    for key in uniqueIdKeys:
        if key.lower() not in dataKeys:
            missingKeys.append(key)
    return missingKeys


def get_role_id(roleName: str, projectId: str) -> str:
    if roleName and projectId:
        if roleName.startswith("organizations/"):
            return roleName

        elif roleName.startswith("projects/"):
            return roleName

        elif roleName.startswith("roles/"):
            return f"projects/{projectId}/{roleName}"

        logger.error("Invalid role name provided, GCP role name and projectId required")
        raise ValueError(
            "Invalid role name provided, GCP role name and projectId required",
        )

    else:
        logger.error("GCP roleName and projectId required")
        raise ValueError(
            "Invalid parameters provided, GCP role name and projectId required",
        )


class GCPUniqueId:
    def get_unique_id(
        self,
        service: str,
        resourceType: str,
        data: Dict,
        projectId: str | None = None,
        location: str | None = None,
    ) -> str:
        uniqueIds: Dict = unique_id_patterns
        data = {k.lower().replace("_", ""): v for k, v in data.items()}
        dataKeys = list(data.keys())

        if not uniqueIds.get(service, None):
            logger.error(f"GCP service {service} unknown")
            raise ValueError(f"GCP service {service} unknown")

        elif not uniqueIds.get(service, {}).get(resourceType, None):
            logger.error(
                f"GCP service {service} resource type {resourceType} not supported",
            )
            raise ValueError(
                f"GCP service {service} resource type {resourceType} not supported",
            )

        elif "projectId" in uniqueIds[service][resourceType] and not projectId:
            uniqueIdFormat = (
                uniqueIds[service][resourceType]
                .replace(" ", "")
                .replace('data["', "")
                .replace('".lower()]', "")
            )
            logger.error("GCP projectId required")
            raise ValueError(f"Invalid parameters provided, GCP projectId required,\
                uniqueId format for resource {service} {resourceType} is {uniqueIdFormat}")

        elif "location" in uniqueIds[service][resourceType] and not location:
            uniqueIdFormat = (
                uniqueIds[service][resourceType]
                .replace(" ", "")
                .replace('data["', "")
                .replace('".lower()]', "")
            )
            logger.error("GCP location required")
            raise ValueError(
                f"Invalid parameters provided, GCP location required, ,\
                    uniqueId format for resource {service} {resourceType} is {uniqueIdFormat}",
            )

        else:
            uniqueIdFormat = (
                uniqueIds[service][resourceType]
                .replace(" ", "")
                .replace('data["', "")
                .replace('".lower()]', "")
            )
            missingKeys = check_missing_data_keys(dataKeys, uniqueIdFormat)
            if len(missingKeys) > 0:
                errorMsg = ""
                for key in missingKeys:
                    errorMsg += f" {key},"

                errorMsg = errorMsg[:-1]

                logger.error(f"GCP{errorMsg} keys required in data parameter")
                raise ValueError(
                    f"Invalid parameters provided, GCP{errorMsg} keys required in data parameter,\
                         uniqueId format for resource {service} {resourceType} is {uniqueIdFormat}",
                )

            else:
                return eval(f"f'{uniqueIds[service][resourceType]}'").replace(" ", "")

    def get_unique_id_format(self, service: str, resourceType: str) -> str:
        uniqueIds: Dict = unique_id_patterns

        if not uniqueIds.get(service, None):
            logger.error(f"GCP service {service} unknown")
            raise ValueError(f"GCP service {service} unknown")

        elif not uniqueIds.get(service, {}).get(resourceType, None):
            logger.error(
                f"GCP service {service} resource type {resourceType} not supported",
            )
            raise ValueError(
                f"GCP service {service} resource type {resourceType} not supported",
            )

        else:
            return (
                uniqueIds[service][resourceType]
                .replace(" ", "")
                .replace('data["', "")
                .replace('".lower()]', "")
            )
