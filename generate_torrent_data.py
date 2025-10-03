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
        # 使用正则表达式解析文件名
        match = re.match(r'qt-opensource-(windows|mac|linux)-(x86|x64)-(\d+\.\d+\.\d+)\.(exe|dmg|run)\.torrent', filename)
        if match:
            os_type = match.group(1)
            architecture = match.group(2)
            version = match.group(3)
            extension = match.group(4)
            
            # 确定操作系统显示名称
            os_display = {
                'windows': 'Windows',
                'mac': 'macOS',
                'linux': 'Linux'
            }.get(os_type, os_type)
            
            # 确定架构显示名称
            arch_display = '32-bit' if architecture == 'x86' else '64-bit'
            
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
                'os_display': f"{os_display} ({arch_display})",
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