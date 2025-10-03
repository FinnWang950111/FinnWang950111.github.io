import os
import re
import json
from datetime import datetime

# 指定torrent文件夹路径
torrent_dir = 'torrent'

# 初始化结果列表
torrent_files = []

# 定义版本发布日期（用于显示）
version_dates = {
    '5.8.0': '2017-05',
    '5.9.0': '2017-05',
    '5.9.1': '2017-07',
    '5.9.2': '2017-09',
    '5.9.3': '2017-12',
    '5.9.4': '2018-02',
    '5.9.5': '2018-05',
    '5.9.6': '2018-08',
    '5.9.7': '2018-11',
    '5.9.8': '2019-01',
    '5.9.9': '2019-04',
    '5.10.0': '2018-06',
    '5.10.1': '2018-07',
    '5.11.0': '2018-09',
    '5.11.1': '2018-10',
    '5.11.2': '2018-12',
    '5.11.3': '2019-01',
    '5.12.0': '2019-01',
    '5.12.1': '2019-02',
    '5.12.2': '2019-04',
    '5.12.3': '2019-05',
    '5.12.4': '2019-07',
    '5.12.5': '2019-09',
    '5.12.6': '2019-11',
    '5.12.7': '2020-01',
    '5.12.8': '2020-03',
    '5.12.9': '2020-05',
    '5.12.10': '2020-07',
    '5.12.11': '2020-09',
    '5.12.12': '2021-01',
    '5.13.0': '2019-06',
    '5.13.1': '2019-09',
    '5.13.2': '2019-12',
    '5.14.0': '2020-04',
    '5.14.1': '2020-07',
    '5.14.2': '2020-11'
}

# 扫描torrent文件夹
for filename in os.listdir(torrent_dir):
    if filename.endswith('.torrent'):
        # 改进的正则表达式，支持额外标识符
        match = re.match(r'qt-opensource-(windows|mac|linux)-(x86|x64)((?:-[^-]+)+)-(\d+\.\d+\.\d+)\.(exe|dmg|run)\.torrent', filename)
        
        # 尝试标准格式
        if not match:
            match = re.match(r'qt-opensource-(windows|mac|linux)-(x86|x64)-(\d+\.\d+\.\d+)\.(exe|dmg|run)\.torrent', filename)
            if match:
                os_type = match.group(1)
                architecture = match.group(2)
                version = match.group(3)
                extension = match.group(4)
                extra_info = ''
        else:
            os_type = match.group(1)
            architecture = match.group(2)
            extra_info = match.group(3).replace('-', ' ').strip()
            version = match.group(4)
            extension = match.group(5)
            
        # 尝试online installer格式
        if not match:
            match = re.match(r'qt-online-installer-(windows|linux|macOS)-(x64|arm64)-(\d+\.\d+\.\d+)\.(exe|run|dmg)\.torrent', filename)
            if match:
                os_type = match.group(1)
                architecture = match.group(2)
                version = match.group(3)
                extension = match.group(4)
                extra_info = 'Online Installer'
        
        if match:
            # 确定操作系统显示名称
            os_display = {
                'windows': 'Windows',
                'mac': 'macOS',
                'macOS': 'macOS',
                'linux': 'Linux'
            }.get(os_type, os_type)
            
            # 确定架构显示名称
            arch_display = '32-bit' if architecture == 'x86' else '64-bit' if architecture == 'x64' else architecture
            
            # 组合显示名称，包含额外信息
            display_name = f"{os_display} ({arch_display})"
            if extra_info:
                display_name += f" - {extra_info}"
            
            # 获取文件大小
            file_path = os.path.join(torrent_dir, filename)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # 转换为MB
            file_size_str = f"{file_size:.2f} MB" if file_size < 1024 else f"{file_size/1024:.2f} GB"
            
            # 获取版本号前缀（用于过滤）
            version_prefix = '.'.join(version.split('.')[:2])
            
            # 获取发布日期
            release_date = version_dates.get(version, '未知')
            
            # 添加到结果列表
            torrent_files.append({
                'filename': filename,
                'os': os_type,
                'os_display': display_name,
                'version': version,
                'version_prefix': version_prefix,
                'extension': extension.upper(),
                'file_size': file_size_str,
                'release_date': release_date
            })

# 按版本号排序（从新到旧）
torrent_files.sort(key=lambda x: [int(part) for part in x['version'].split('.')], reverse=True)

# 生成JavaScript数据文件
with open('torrent_data.js', 'w', encoding='utf-8') as f:
    f.write('// 自动生成的torrent文件数据\n')
    f.write('// 生成时间: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n\n')
    f.write('const torrentFiles = ' + json.dumps(torrent_files, ensure_ascii=False, indent=2) + ';\n')

print(f'成功生成torrent_data.js，包含 {len(torrent_files)} 个torrent文件信息')