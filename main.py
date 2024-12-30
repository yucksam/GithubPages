import tkinter as tk
from tkinter import ttk
import random

# 定义进程控制块
class PCB:
    def __init__(self, name, priority, run_time):
        self.name = name          # 进程名
        self.priority = priority  # 优先数
        self.run_time = run_time  # 要求运行时间
        self.status = 'R'         # 状态 ('R' 就绪, 'E' 结束)
        self.next = None          # 指向下一个进程


# 定义进程调度器
class ProcessScheduler:
    def __init__(self):
        self.queue = None
        self.completed = []  # 用于存储已完成的进程

    def insert_process(self, process):
        """按优先数从大到小插入进程"""
        if not self.queue or process.priority > self.queue.priority:
            process.next = self.queue
            self.queue = process
        else:
            current = self.queue
            while current.next and current.next.priority >= process.priority:
                current = current.next
            process.next = current.next
            current.next = process

    def schedule(self):
        """调度并更新队列"""
        if not self.queue:
            return None
        # 选择队首进程
        process = self.queue
        self.queue = self.queue.next  # 移除队首
        # 模拟进程运行
        process.priority -= 1
        process.run_time -= 1
        if process.run_time == 0:
            process.status = 'E'
            self.completed.append(process)  # 加入已完成队列
        else:
            process.status = 'R'
            self.insert_process(process)  # 重新插入队列
        return process

    def auto_schedule(self, update_callback):
        """自动调度所有进程，直到队列为空"""
        if self.queue:
            process = self.schedule()
            update_callback(process)
            self.queue_display_after = self.queue  # 保存当前队列状态
            self.update_ui_after(process)


# 创建 Tkinter 界面
class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("操作系统实验四")

        self.scheduler = ProcessScheduler()
        self.init_processes()
        self.current_process = None

        # GUI 元素
        self.left_frame = tk.Frame(root)
        self.right_frame = tk.Frame(root)
        self.left_frame.grid(row=0, column=0, padx=20, pady=20)
        self.right_frame.grid(row=0, column=1, padx=20, pady=20)

        # 左边：未完成队列
        self.queue_label = tk.Label(self.left_frame, text="未完成进程队列", font=("Arial", 16, "bold"))
        self.queue_label.pack()
        self.queue_display = tk.Text(self.left_frame, height=20, width=50, font=("Arial", 12), state=tk.DISABLED)
        self.queue_display.pack()

        # 右边：已完成队列
        self.completed_label = tk.Label(self.right_frame, text="已完成进程队列", font=("Arial", 16, "bold"))
        self.completed_label.pack()
        self.completed_display = tk.Text(self.right_frame, height=20, width=50, font=("Arial", 12), state=tk.DISABLED)
        self.completed_display.pack()

        # 操作按钮
        self.schedule_button = ttk.Button(root, text="调度下一个进程", command=self.run_schedule, width=20, padding=10)
        self.schedule_button.grid(row=1, column=0, padx=20, pady=10)

        self.auto_schedule_button = ttk.Button(root, text="自动调度所有进程", command=self.run_auto_schedule, width=20, padding=10)
        self.auto_schedule_button.grid(row=1, column=1, padx=20, pady=10)

        self.reset_button = ttk.Button(root, text="重置", command=self.reset_scheduler, width=20, padding=10)
        self.reset_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

        self.status_label = tk.Label(root, text="", fg="blue", font=("Arial", 14))
        self.status_label.grid(row=3, column=0, columnspan=2)

        # 初始化显示
        self.update_displays()

    def init_processes(self):
        """初始化进程队列"""
        priorities = [1, 2, 3, 4, 5]
        random.shuffle(priorities)
        for i in range(5):
            name = f"P{i + 1}"
            priority = priorities[i]
            run_time = random.randint(1, 6)
            process = PCB(name, priority, run_time)
            self.scheduler.insert_process(process)

    def update_displays(self):
        """更新左侧和右侧的显示"""
        # 更新未完成队列
        self.queue_display.config(state=tk.NORMAL)
        self.queue_display.delete(1.0, tk.END)

        current = self.scheduler.queue
        if not current:
            self.queue_display.insert(tk.END, "队列为空。\n")
        else:
            self.queue_display.insert(tk.END, "当前队列状态:\n")
            while current:
                self.queue_display.insert(
                    tk.END, f"进程名: {current.name}, 优先数: {current.priority}, "
                            f"要求运行时间: {current.run_time}, 状态: {current.status}\n"
                )
                current = current.next

        self.queue_display.config(state=tk.DISABLED)

        # 更新已完成队列
        self.completed_display.config(state=tk.NORMAL)
        self.completed_display.delete(1.0, tk.END)

        if not self.scheduler.completed:
            self.completed_display.insert(tk.END, "暂无已完成进程。\n")
        else:
            self.completed_display.insert(tk.END, "已完成进程:\n")
            for process in self.scheduler.completed:
                self.completed_display.insert(
                    tk.END, f"进程名: {process.name}, 状态: {process.status}\n"
                )

        self.completed_display.config(state=tk.DISABLED)

    def run_schedule(self):
        """执行调度操作"""
        process = self.scheduler.schedule()
        if process:
            self.status_label.config(
                text=f"调度选择进程: {process.name} (优先数: {process.priority + 1}, 要求运行时间: {process.run_time + 1})"
            )
        else:
            self.status_label.config(text="所有进程已完成！")
        self.update_displays()

    def run_auto_schedule(self):
        """自动调度操作"""
        self.status_label.config(text="自动调度开始...")
        self.schedule_auto_step()

    def schedule_auto_step(self):
        """定时调度进程"""
        process = self.scheduler.schedule()
        if process:
            self.status_label.config(
                text=f"调度选择进程: {process.name} (优先数: {process.priority + 1}, 要求运行时间: {process.run_time + 1})"
            )
            self.update_displays()
            # 每1秒调度一次
            self.root.after(1000, self.schedule_auto_step)
        else:
            self.status_label.config(text="所有进程已完成！")
            self.update_displays()

    def reset_scheduler(self):
        """重置调度器"""
        self.scheduler = ProcessScheduler()
        self.init_processes()
        self.status_label.config(text="")
        self.update_displays()


# 启动程序
if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
