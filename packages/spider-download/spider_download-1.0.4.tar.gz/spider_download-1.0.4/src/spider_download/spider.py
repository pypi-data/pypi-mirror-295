import os.path
import random
import time
import traceback
from queue import Queue
from threading import Thread

import requests
from tqdm import tqdm


class Spider:
    def __init__(self, task_list, thread_num=2):
        """
        多线程下载
        :param task_list: [(url,file_name),(url,file_name),...]
        :param thread_num: 线程数
        """
        self.task_list = task_list
        self.thread_num = thread_num
        self.save_path = os.path.join(
            os.path.expanduser("~"), "Desktop", "SpiderDownload"
        )
        self._tasks = Queue()  # 待爬取的链接队列
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        self.proxies = None

    def _urls_in(self):
        """url入队列"""
        for task in self.task_list:
            self._tasks.put(task)

    def _download(self, url, file_path):
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print(f"{url} 已下载，跳过\n")
            return
        print(f"下载链接: {url} \n")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        resp = requests.get(
            url, headers=self.headers, stream=True, timeout=20, proxies=self.proxies
        )
        # 获取文件总大小
        total_size = int(resp.headers.get("content-length", 0))
        if total_size < 5 * 1024 * 1024:  # 小于5MB的文件，不显示进度条
            with open(file_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            with open(file_path, "wb") as f, tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                desc=file_path,
                initial=0,
                ascii=True,
            ) as pbar:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        time.sleep(random.uniform(1, 2))

    def _write_failed_txt(self, task):
        with open(
            "failed.txt",
            "a",
            encoding="utf-8",
        ) as f:
            f.write(str(task))
            f.write(",")
            f.write("\n")

    # 爬取页面并处理结果
    def _crawl(self):
        while not self._tasks.empty():
            task = self._tasks.get()
            try:
                self._download(
                    url=task[0], file_path=os.path.join(self.save_path, task[1])
                )
            except Exception:
                # 下载失败，将失败任务写入文件
                self._write_failed_txt(task)
                print(traceback.format_exc())
            finally:
                self._tasks.task_done()

    # 启动多线程爬虫
    def run(self):
        print(f"文件下载目录：{self.save_path}")
        self._urls_in()
        for i in range(self.thread_num):
            t = Thread(target=self._crawl)
            t.start()
        self._tasks.join()


if __name__ == "__main__":
    spider = Spider(
        task_list=[
            (
                "https://assets.mixkit.co/active_storage/sfx/833/833-preview.mp3",
                "Metal hammer hit.mp3",
            ),
        ],
        thread_num=4,
    )
    spider.run()
