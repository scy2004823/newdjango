# Trae-2025.10.13 基础环境

本仓库用于在 Windows + Python 虚拟环境下搭建并测试基础 Django 环境。

## 准备环境
- 激活虚拟环境：`./venv/Scripts/Activate.ps1`
- 验证 Python：`python --version`
- 验证 pip：`python -m pip --version`

## 安装 Django（若网络/SSL受限的建议）
1. 常规方式：`python -m pip install django`
2. 指定镜像源（示例：清华）：
   - 临时：`python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django`
   - 或在用户目录创建 `pip\pip.ini`（Windows）：
     ```ini
     [global]
     index-url = https://pypi.tuna.tsinghua.edu.cn/simple
     trusted-host = pypi.tuna.tsinghua.edu.cn
     ```
3. 若仍遇到 `check_hostname requires server_hostname`，可尝试：
   - 关闭系统代理/VPN后重试
   - 切换网络（热点/其他网络）
   - 用 `--trusted-host pypi.org --trusted-host files.pythonhosted.org`（仅在受限网络中临时使用）

## 创建 Django 项目（安装成功后）
```powershell
python -m django startproject mysite
cd mysite
python manage.py startapp main
python manage.py runserver
```

## 目录说明
- `venv/` 虚拟环境目录（已在 `.gitignore` 中忽略）
- 后续将生成 `mysite/` 项目与 `main/` 应用目录

## 提交与推送
```powershell
git add .
git commit -m "chore: bootstrap repo docs and config"
git remote add origin https://github.com/<your-username>/Trae-2025.10.13.git
git push -u origin main
```

> 提示：首次推送可能需要 GitHub 登录或使用 PAT（`repo` 权限）。