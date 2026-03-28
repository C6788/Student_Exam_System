import os
import random
import time
from core.student import Student

class ExamSystem:
    """考场与学生信息管理系统逻辑控制类"""

    def __init__(self, file_path):
        self.file_path = file_path
        self.students = []  # 用于存储Student对象的列表
        self.scheduled_students = []  # 用于存储打乱后的考场座位顺序
        self.load_data()

    @staticmethod
    def get_formatted_time():
        """
        静态方法：获取当前格式化时间
        符合作业要求：至少包含一个静态方法或类方法
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def load_data(self):
        """信息初始化：读取文本文件并解析为Student对象"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # 假设txt文件内以空格分隔：学号 姓名 性别 班级 学院
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        student = Student(parts[0], parts[1], parts[2], parts[3], parts[4])
                        self.students.append(student)
            print(f"✅ 系统初始化成功！共加载 {len(self.students)} 名学生信息。")
        except FileNotFoundError:
            # 异常处理：捕获文件丢失异常
            print(f"❌ 严重错误：未找到数据文件 '{self.file_path}'。请确保文件存在于根目录。")

    def search_student(self, target_id):
        """查找功能：根据学号打印学生完整信息"""
        for student in self.students:
            if student.stu_id == target_id:
                print("\n🔍 查找到学生信息：")
                print(student)
                return
        print(f"\n⚠️ 提示：未找到学号为 '{target_id}' 的学生，请检查输入是否正确。")

    def random_roll_call(self, count_str):
        """随机点名功能"""
        try:
            # 异常处理：尝试将用户输入的字符串转换为整数
            count = int(count_str)
            total_students = len(self.students)

            if count <= 0:
                print("\n⚠️ 错误：点名人数必须大于0。")
                return
            if count > total_students:
                print(f"\n⚠️ 错误：输入数量 ({count}) 超过了总人数 ({total_students})。")
                return

            # 使用 random.sample 获取不重复的随机样本
            selected_students = random.sample(self.students, count)
            print(f"\n🎲 随机点名 {count} 人，名单如下：")
            for i, s in enumerate(selected_students, 1):
                print(f"   {i}. {s.name} ({s.stu_id})")

        except ValueError:
            # 异常处理：捕获非数字字符转换异常
            print("\n❌ 错误：输入包含非数字字符，请输入有效的整数！")

    def generate_exam_schedule(self):
        """生成考场安排表"""
        if not self.students:
            print("\n⚠️ 系统中无学生数据，无法生成考场安排表。")
            return

        # 将学生列表复制一份并随机打乱
        self.scheduled_students = self.students.copy()
        random.shuffle(self.scheduled_students)

        try:
            with open("考场安排表.txt", 'w', encoding='utf-8') as f:
                # 写入带时间戳的表头
                f.write(f"生成时间：{self.get_formatted_time()}\n")
                f.write("=" * 40 + "\n")
                for index, student in enumerate(self.scheduled_students, start=1):
                    f.write(f"座位号: {index} | 姓名: {student.name} | 学号: {student.stu_id}\n")
            print("\n✅ 成功在根目录下生成 '考场安排表.txt'！")
        except Exception as e:
            print(f"\n❌ 生成考场安排表时发生未知错误: {e}")

    def generate_admission_tickets(self):
        """生成准考证目录与独立文件"""
        if not self.scheduled_students:
            print("\n⚠️ 请先执行 [3] 生成考场安排表，再生成准考证！")
            return

        dir_name = "准考证"
        # 如果目录不存在，则创建目录
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        try:
            for index, student in enumerate(self.scheduled_students, start=1):
                # 生成如 01.txt, 02.txt 的文件名
                file_name = f"{index:02d}.txt"
                file_path = os.path.join(dir_name, file_name)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"座位号: {index}\n")
                    f.write(f"姓名: {student.name}\n")
                    f.write(f"学号: {student.stu_id}\n")
            print(f"\n✅ 成功在 '{dir_name}' 文件夹下生成 {len(self.scheduled_students)} 份准考证文件！")
        except Exception as e:
            print(f"\n❌ 生成准考证文件时发生错误: {e}")
# ExamSystem 逻辑控制类
