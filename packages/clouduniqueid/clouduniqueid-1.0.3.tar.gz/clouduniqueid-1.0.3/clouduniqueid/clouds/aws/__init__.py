import logging
import re
from typing import Dict

from .uniqueid import unique_id_patterns

logger = logging.getLogger(__name__)


def check_missing_data_keys(dataKeys: list, uniqueIdFormat: str):
    uniqueIdKeys = re.findall(r"{(.*?)}", uniqueIdFormat)
    dataKeys.extend(["region", "accountid", "partition"])
    missingKeys = []
    for key in uniqueIdKeys:
        if key.lower() not in dataKeys:
            missingKeys.append(key)

    return missingKeys


class AWSUniqueId:
    def get_unique_id(
        self,
        service: str,
        resourceType: str,
        data: Dict,
        accountId: str | None = None,
        region: str | None = None,
        partition: str = "aws",
    ) -> str:
        uniqueIds: Dict = unique_id_patterns
        data = {k.lower().replace("_", ""): v for k, v in data.items()}
        dataKeys = list(data.keys())

        if not uniqueIds.get(service, None):
            logger.error(f"AWS service {service} unknown")
            return ""
            # raise ValueError(f"AWS service {service} unknown")

        elif not uniqueIds.get(service, {}).get(resourceType, None):
            logger.error(
                f"AWS service {service} resource type {resourceType} not supported",
            )
            # raise ValueError(
            #     f"AWS service {service} resource type {resourceType} not supported",
            # )
            return ""

        elif "accountId" in uniqueIds[service][resourceType] and not accountId:
            uniqueIdFormat = (
                uniqueIds[service][resourceType]
                .replace(" ", "")
                .replace('data["', "")
                .replace('".lower()]', "")
            )
            logger.error("AWS accountId required")
            # raise ValueError(f"Invalid parameters provided, AWS accountId required,\
            #     uniqueId format for resource {service} {resourceType} is {uniqueIdFormat}")
            return ""

        elif "region" in uniqueIds[service][resourceType] and not region:
            uniqueIdFormat = (
                uniqueIds[service][resourceType]
                .replace(" ", "")
                .replace('data["', "")
                .replace('".lower()]', "")
            )
            logger.error("AWS region required")
            # raise ValueError(
            #     f"Invalid parameters provided, AWS region required, ,\
            #         uniqueId format for resource {service} {resourceType} is {uniqueIdFormat}",
            # )
            return ""

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

                logger.error(f"AWS{errorMsg} keys required in data parameter")
                # raise ValueError(
                #     f"Invalid parameters provided, AWS{errorMsg} keys required in data parameter,\
                #         uniqueId format for resource {service} {resourceType} is {uniqueIdFormat}",
                # )
                return ""

            else:
                if uniqueIds[service][resourceType].startswith("hashlib"):
                    if resourceType == "acl":
                        return "{}:{}:{}:{}:{}:{}:{}:{}".format(
                            accountId,
                            data.get("owner"),
                            data.get("ownerid"),
                            data.get("type"),
                            data.get("displayname"),
                            data.get("granteeid"),
                            data.get("uri"),
                            data.get("permission"),
                        )

                    return eval(
                        eval(f"f'{uniqueIds[service][resourceType]}'").replace(" ", ""),
                    )

                return eval(f"f'{uniqueIds[service][resourceType]}'").replace(" ", "")

    def get_unique_id_format(self, service: str, resourceType: str) -> str:
        uniqueIds: Dict = unique_id_patterns

        if not uniqueIds.get(service, None):
            logger.error(f"AWS service {service} unknown")
            # raise ValueError(f"AWS service {service} unknown")
            return ""

        elif not uniqueIds.get(service, {}).get(resourceType, None):
            logger.error(
                f"AWS service {service} resource type {resourceType} not supported",
            )
            # raise ValueError(
            #     f"AWS service {service} resource type {resourceType} not supported",
            # )
            return ""

        else:
            return (
                uniqueIds[service][resourceType]
                .replace(" ", "")
                .replace('data["', "")
                .replace('".lower()]', "")
            )
