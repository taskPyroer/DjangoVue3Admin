"""
Time:     2024/1/4 11:10
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     init.py
Describe:
"""
import json
import os

from django.core.management.base import BaseCommand
from django.core.management import call_command

from application.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Initializes the project data.'

    def handle(self, *args, **options):
        path_file = os.path.join(BASE_DIR, "app_init", "management", "commands")
        files = os.listdir(path_file)
        for file in files:
            # 判断文件是否为 JSON 文件
            if file.endswith(".json"):
                json_file = os.path.join(path_file, file)

                # py manage.py dumpdata app_dict -o app_dict.json #导出数据的会出现编码问题，需要转化一下
                # with open(json_file, 'rb') as f:
                #     contents = f.read().decode('gbk')
                # json_obj = json.loads(contents)
                # with open(json_file, 'w', encoding='utf-8') as f:
                #     json.dump(json_obj, f, ensure_ascii=False, indent=4)
                call_command('loaddata', json_file)
                self.stdout.write(self.style.SUCCESS(f'{file.replace(".json", "")} initialized successfully.'))
        self.stdout.write(self.style.SUCCESS('Data initialized successfully.'))
