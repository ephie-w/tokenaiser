'''
Author: Yifei Wang
Github: ephiewangyf@gmail.com
Date: 2025-11-14 10:07:29
LastEditors: ephie && ephiewangyf@gmail.com
LastEditTime: 2025-11-14 10:21:03
FilePath: /tokenaiser/tools/apihub.py
Description: 
'''

from google.adk.tools.apihub_tool.apihub_toolset import APIHubToolset

class ApihubToolset(APIHubToolset):
    def __init__(self):
        super().__init__(
            name="apihub",
            description="APIHub toolset with ADC auth",
            apihub_resource_name="apihub-resource-name",
        )

    
    @classmethod
    def from_config(cls, config, base_path):
        # YAML 加载必须实现 from_config
        return cls()