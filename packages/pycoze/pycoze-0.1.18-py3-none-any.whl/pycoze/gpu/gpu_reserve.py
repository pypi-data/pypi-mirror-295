import subprocess
import sqlite3
import atexit
import time
import os
import psutil

try:
    from pycoze.utils import utils

    # 定义数据库连接和初始化
    params = utils.arg.read_params()
    if params:
        DATABASE_PATH = params["appPath"] + "/gpu_usage.db"
    else:
        raise Exception("No params")
except:
    DATABASE_DIR = os.path.expanduser("~/pycoze")
    os.makedirs(DATABASE_DIR, exist_ok=True)
    DATABASE_PATH = os.path.join(DATABASE_DIR, "gpu_usage.db")
TABLE_NAME = "gpu_usage"


def initialize_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            process_id TEXT NOT NULL,
            reserved_gb REAL NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


# 检测GPU资源
def get_gpu_resources():
    try:
        # 使用nvidia-smi命令获取GPU信息
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
            stdout=subprocess.PIPE,
            text=True,
        )
        free_memory = result.stdout.strip().split("\n")
        total_free_memory = sum(float(mem) for mem in free_memory)

        # 获取正在使用GPU的进程信息
        process_result = subprocess.run(
            [
                "nvidia-smi",
                "--query-compute-apps=pid,process_name,used_memory",
                "--format=csv,noheader,nounits",
            ],
            stdout=subprocess.PIPE,
            text=True,
        )
        process_info = process_result.stdout.strip().split("\n")

        # 过滤掉进程名中包含"python"的进程
        python_memory_usage = 0.0
        for process in process_info:
            pid, process_name, used_memory = process.split(", ")
            if "python" in process_name.lower():
                python_memory_usage += float(used_memory)

        # 计算排除python进程后的总空闲内存
        total_free_memory -= python_memory_usage
        return round(total_free_memory / 1024, 2)
    except Exception as e:
        print(f"Error getting GPU resources: {e}")
        return 0.0


# 预留GPU资源
def reserve_gpu(gb):
    process_id = str(os.getpid())
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT SUM(reserved_gb) FROM {TABLE_NAME}")
        total_reserved = cursor.fetchone()[0]
        if total_reserved is None:
            total_reserved = 0.0
        available_gb = get_gpu_resources() - total_reserved
        if available_gb >= gb:
            cursor.execute(
                f"INSERT INTO {TABLE_NAME} (process_id, reserved_gb) VALUES (?, ?)",
                (process_id, gb),
            )
            conn.commit()
            print(f"预留成功，剩余GPU大小: {available_gb - gb} GB")
            return True
        else:
            print(f"预留失败，剩余GPU大小: {available_gb} GB")
            return False


def reserve_gpu_retry(gb, retry=10000):
    for i in range(retry):
        time.sleep(1)
        if reserve_gpu(gb):
            if i % 10 == 0 or i < 10:
                print(f"重试第{i}次")
            return True
    return False


# 释放GPU资源
def release_gpu():
    process_id = str(os.getpid())
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE process_id = ?", (process_id,))
        conn.commit()
        # 计算释放后的剩余GPU大小
        cursor.execute(f"SELECT SUM(reserved_gb) FROM {TABLE_NAME}")
        total_reserved = cursor.fetchone()[0]
        if total_reserved is None:
            total_reserved = 0.0
        available_gb = get_gpu_resources() - total_reserved
        print(f"释放成功，剩余GPU大小: {available_gb} GB")


# 注册退出时的清理函数
def cleanup():
    release_gpu()
    print("程序退出，GPU资源已释放")


def initialize_and_check():
    initialize_db()
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT process_id, reserved_gb FROM {TABLE_NAME}")
        rows = cursor.fetchall()
        for row in rows:
            process_id, reserved_gb = row
            try:
                # 检查进程是否存在
                psutil.Process(int(process_id))
            except psutil.NoSuchProcess:
                # 进程不存在，删除对应的记录
                cursor.execute(
                    f"DELETE FROM {TABLE_NAME} WHERE process_id = ?", (process_id,)
                )
                print(f"进程 {process_id} 不存在，已删除对应的预留记录")
        conn.commit()


# 在模块加载时执行初始化检查
initialize_and_check()

# 注册清理函数
atexit.register(cleanup)

if __name__ == "__main__":
    if reserve_gpu_retry(10):
        print("GPU资源预留成功")
        time.sleep(100)
        release_gpu()
        print("GPU资源释放成功")
    else:
        print("GPU资源不足，无法预留")
