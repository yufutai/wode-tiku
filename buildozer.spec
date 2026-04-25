[app]
# 应用名称
title = 题库悬浮搜

# 包名 (反向域名)
package.name = floatingsearch

# 包域名
package.domain = org.example

# 主入口文件
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

# 版本号
version = 1.0

# 最低要求的 Python 版本
requirements = python3,kivy==2.3.0

# --- 安卓权限 (关键) ---
# READ/WRITE: 读取题目.txt
# SYSTEM_ALERT_WINDOW: 悬浮窗权限
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, SYSTEM_ALERT_WINDOW

# --- 图标 (可选) ---
# icon.filename = %(source.dir)s/data/icon.png

[buildozer]
# 打包目录
bin_dir = 
build_dir = 
base_dir = 

# 虚拟机配置
vm_arch = arm64-v8a