import json

from is3_python_sdk.domain.data_dto import DataEntity
from is3_python_sdk.utils.config_util import get_header
from is3_python_sdk.utils.config_util import get_server_name


def create_data_entity(filePath, jsonData):
    serverName = get_server_name(filePath, 'server')
    headers = get_header(filePath, 'key')
    dataDto = DataEntity(
        preData=jsonData.get('data', {}),
        pluginDataConfig=jsonData.get('pluginDataConfig', {}),
        taskInstanceId=1111,
        taskId=1,
        nodeId=1,
        logId=1,
        serverName=serverName,
        headers=headers,
        prjId=int(json.dumps(jsonData.get('prjId', 1))),
        tenantId=1,
        bootstrapServers='1',
    )
    return dataDto
