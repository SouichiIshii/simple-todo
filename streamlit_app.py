from datetime import datetime

import streamlit as st
import pandas as pd
import requests


API_URL = 'http://127.0.0.1:8000/tasks'


def list_tasks():
    response = requests.get(url=API_URL)
    data = response.json()
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)

def create_task(task_data):
    response = requests.post(
        url=API_URL,
        json=task_data
    )
    st.rerun()

def update_task(id, task_data):
    response = requests.put(
        url=f'{API_URL}/{id}',
        json=task_data
    )
    st.rerun()

def delete_task(id):
    response = requests.delete(url=f'{API_URL}/{id}')
    st.rerun()

def task_form(task=None):
    form_key = f"task_form_{task['id']}" if task is not None else "new_task_form"
    with st.form(key=form_key):
        task_name = st.text_input("タスク名", value='' if task is None else task["task_name"])
        registration_date = datetime.today().strftime("%Y-%m-%d")
        deadline_date = st.date_input("期限日", value=datetime.now() if task is None else datetime.strptime(task["deadline_date"], '%Y-%m-%d'))
        status = st.selectbox("タスクの状況を入力してください。", options=["未着手", "進行中", "完了"], index=0 if task is None else ["未着手", "進行中", "完了"].index(task["status"]))

        submit_button = st.form_submit_button("登録" if task is None else "更新")
        if submit_button:
            task_data = {
                "task_name": task_name,
                "registration_date": registration_date,
                "deadline_date": deadline_date.strftime('%Y-%m-%d'),
                "status": status
            }
            if task is None:
                create_task(task_data=task_data)
            else:
                update_task(id=task["id"], task_data=task_data)


if __name__ == "__main__":
    tasks = list_tasks()
    if not tasks.empty:
        st.subheader("タスク一覧")
        st.write(tasks)
    else:
        st.write("タスク一覧", "現在登録されているタスクはありません。")

    st.subheader("新規タスク登録")
    task_form()

    if not tasks.empty:
        for index, task in tasks.iterrows():
            col1, col2, col3 = st.columns([1, 1, 8])
            if col1.button("編集", key=f'edit-{index}'):
                task_form(task=task)
            if col2.button("削除", key=f'delete-{index}'):
                delete_task(task["id"])
