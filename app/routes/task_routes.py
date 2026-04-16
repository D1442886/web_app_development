from flask import Blueprint, render_template, request, redirect, url_for, flash
# from app.models.task import TaskModel  # 之後連同實作一起開啟

# 我們使用 Blueprint 來整理路由，這讓專案結構更乾淨。
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    """
    任務列表頁面 (GET)
    - 讀取 URL query 參數 filter
    - 呼叫 TaskModel 取出相關任務
    - 將任務清單渲染至 index.html
    """
    pass

@tasks_bp.route('/tasks', methods=['POST'])
def add_task():
    """
    新增任務 (POST)
    - 取得表單內的 title 欄位
    - 檢查是否為空，若是則 flash 錯誤訊息
    - 呼叫 TaskModel 進行儲存
    - 重導向回首頁
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    切換任務完成狀態 (POST)
    - 根據傳入的 task_id，呼叫 TaskModel 更新資料
    - 重導向回首頁
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    刪除任務 (POST)
    - 根據傳入的 task_id，呼叫 TaskModel 刪除資料庫中的紀錄
    - 重導向回首頁
    """
    pass
