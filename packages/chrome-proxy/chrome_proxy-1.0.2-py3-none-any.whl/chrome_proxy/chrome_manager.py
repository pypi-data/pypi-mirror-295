import argparse
import os
import shutil
import subprocess
import winreg

from .proxy_app import start_proxy


def get_chrome_path():
    """尝试获取 Google Chrome 安装路径"""
    try:
        reg_key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe",
        )
        chrome_path, _ = winreg.QueryValueEx(reg_key, None)
        winreg.CloseKey(reg_key)
        return chrome_path
    except Exception as e:
        print(f"从注册表获取 Chrome 路径失败: {e}")

    chrome_path = shutil.which("chrome") or shutil.which("google-chrome")
    if chrome_path:
        return chrome_path

    print("未能找到 Chrome 安装路径")
    return None


def start_chrome_with_debugging(
    chrome_path, headless=False, port=9222, profile_dir="C:\\selenium\\ChromeProfile"
):
    """启动 Chrome 并开启远程调试功能"""
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
    cmd = f'"{chrome_path}" --remote-debugging-port={port} --user-data-dir="{profile_dir}"'
    if headless:
        cmd += " --headless"
    try:
        subprocess.Popen(cmd)
        print(f"Chrome 已成功启动，远程调试端口: {port}，用户数据目录: {profile_dir}")
    except Exception as e:
        print(f"启动 Chrome 失败: {e}")


def main():
    parser = argparse.ArgumentParser(description="Chrome Proxy")
    parser.add_argument(
        "--headless", action="store_true", help="Run Chrome in headless mode"
    )
    args = parser.parse_args()
    if args.headless:
        print("Running in headless mode")
    chrome_path = get_chrome_path()
    if chrome_path:
        start_chrome_with_debugging(chrome_path, headless=args.headless)
        start_proxy()
    else:
        print("无法启动 Chrome，因为未能找到 Chrome 安装路径。")
