import os
import subprocess
import json

class MobileCollector:
    def __init__(self):
        self.data = {}

    def collect_metrics(self):
        self.data['device_model'] = self.get_device_model()
        self.data['battery'] = self.get_battery_info()
        self.data['memory'] = self.get_memory_info()
        self.data['storage'] = self.get_storage_info()

    def get_device_model(self):
        model = subprocess.check_output(['adb', 'shell', 'getprop', 'ro.product.model']).strip()
        return model.decode('utf-8')

    def get_battery_info(self):
        battery_info = subprocess.check_output(['adb', 'shell', 'dumpsys', 'battery']).decode('utf-8')
        return battery_info

    def get_memory_info(self):
        memory_info = subprocess.check_output(['adb', 'shell', 'dumpsys', 'meminfo']).decode('utf-8')
        return memory_info

    def get_storage_info(self):
        storage_info = subprocess.check_output(['adb', 'shell', 'df']).decode('utf-8')
        return storage_info

    def save_to_file(self, filepath='phone_metrics.json'):
        with open(filepath, 'w') as f:
            json.dump(self.data, f, indent=4)

if __name__ == '__main__':
    collector = MobileCollector()
    collector.collect_metrics()
    collector.save_to_file()