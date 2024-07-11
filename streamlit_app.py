from datetime import datetime

import streamlit as st
import pandas as pd
import requests


API_URL = 'http://127.0.0.1:8000/tasks'


@st.cache(allow_output_mutation=True, show_spinner=False)
def get_tasks():
    response = requests.get(API_URL)
    return pd.DataFrame(response.json()) if response.ok else pd.DataFrame()

def create_task(task_data):
    response = requests.post(API_URL, json=task_data)
    return response.ok

def update_task(task_id, task_data):
    response = requests.put(f"{API_URL}/{task_id}", json=task_data)
    return response.ok

def delete_task(task_id):
    response = requests.delete(f"{API_URL}/{task_id}")
    return response.ok

def display_tasks():
    tasks = get_tasks()
    if not tasks.empty:
        st.write(tasks)
    else:
        st.write("タスクがありません。")

def task_form(task=None):
    # タスクがNoneでない場合、フォームキーをtaskのidから生成
    form_key = f"form_{task['id']}" if task is not None else "form_new"
    with st.form(key=form_key):
        # タスクがNoneではない場合、task Seriesから値を取得
        task_name_default = task["task_name"] if task is not None else ""
        deadline_default = datetime.strptime(task["deadline_date"], '%Y-%m-%d') if task is not None else datetime.now()
        status_default = ["未着手", "進行中", "完了"].index(task["status"]) if task is not None else 0

        task_name = st.text_input("タスク名", value=task_name_default)
        deadline_date = st.date_input("期限日", value=deadline_default)
        status = st.selectbox("ステータス", ["未着手", "進行中", "完了"], index=status_default)

        submitted = st.form_submit_button("更新" if task is not None else "登録")
        if submitted:
            if task is not None:
                task_data = {
                    "task_name": task_name,
                    "deadline_date": deadline_date.strftime('%Y-%m-%d'),
                    "status": status
                }
                if update_task(task['id'], task_data):
                    st.success("Task updated successfully!")
            else:
                task_data = {
                    "task_name": task_name,
                    "registration_date": datetime.now().strftime("%Y-%m-%d"),
                    "deadline_date": deadline_date.strftime('%Y-%m-%d'),
                    "status": status
                }
                if create_task(task_data):
                    st.success("Task created successfully!")

if __name__ == "__main__":
    st.title("TODOアプリ")
    if "reload" not in st.session_state:
        st.session_state.reload = True

    if st.session_state.reload:
        display_tasks()
        if st.button("Refresh"):
            st.rerun()

    with st.expander("新規タスクを登録"):
        task_form()

    if not get_tasks().empty:
        for idx, task in get_tasks().iterrows():
            with st.expander(f"タスクを編集する #{task['id']}"):
                task_form(task)
            with st.expander(f"タスクを削除する #{task['id']}"):
                if st.button("削除", key=f"delete_{task['id']}"):
                    if delete_task(task["id"]):
                        st.success("Task deleted successfully!")
                        st.rerun()