import warnings
import requests
import pandas as pd
from cheminformatics.edu.base import BaseEDUInstance  # 从 base.py 导入

class EDUInstance(BaseEDUInstance):
    def __init__(self, apiKey, RESTURL="http://gressling.net/v2/"):
        super().__init__(apiKey, RESTURL)
        self.session = requests.Session()

    def connect(self):
        """Checks connection to the API by verifying if the status code is 200."""
        url = f"{self.RESTURL}api.php"
        query = {"apiKey": self.apiKey}
        try:
            response = self.session.get(url, params=query)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return False

    def testAccess(self):
        """Retrieves data from the API if connection is successful."""
        if self.connect():
            url = f"{self.RESTURL}api.php"
            query = {"apiKey": self.apiKey}
            response = self.session.get(url, params=query)
            return response.json()
        else:
            return "Connection failed"

    def getExperiments(self):
        """Retrieves data from the API if connection is successful."""
        if self.connect():
            url = f"{self.RESTURL}A1/A1.php"  # 修改为正确的端点
            query = {"apiKey": self.apiKey}
            try:
                response = self.session.get(url, params=query)
                response.raise_for_status()  # 确保请求成功
                json_data = response.json()
                print("API Response:", json_data)  # 打印响应内容
                if 'data' in json_data:
                    data = json_data['data']
                    print("Data Content:", data)  # 打印数据内容
                    if isinstance(data, list):
                        return pd.DataFrame(data)
                    else:
                        return "Data is not in a list format."
                else:
                    return "Response JSON does not contain 'data' key."
            except requests.RequestException as e:
                print(f"An error occurred: {e}")
                return "Request failed"
        else:
            return "Connection failed"



