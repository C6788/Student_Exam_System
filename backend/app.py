import os
import random
import time
from core.exam_system import ExamSystem


# ==========================================
# 3. 主程序入口与用户交互菜单
# ==========================================
def main():
    print("=" * 40)
    print("欢迎使用 学生信息与考场管理系统")
    print("=" * 40)

    # 实例化系统对象，传入文件名
    system = ExamSystem("人工智能编程语言学生名单.txt")

    while True:
        print("\n请选择操作功能：")
        print("1. 查找学生信息")
        print("2. 随机点名")
        print("3. 生成考场安排表")
        print("4. 生成准考证文件")
        print("0. 退出系统")

        choice = input("请输入功能序号 (0-4): ").strip()

        if choice == '1':
            stu_id = input("请输入要查找的学号: ").strip()
            system.search_student(stu_id)
        elif choice == '2':
            count_str = input("请输入需要点名的学生数量: ").strip()
            system.random_roll_call(count_str)
        elif choice == '3':
            system.generate_exam_schedule()
        elif choice == '4':
            system.generate_admission_tickets()
        elif choice == '0':
            print("\n👋 感谢使用，再见！")
            break
        else:
            print("\n⚠️ 输入无效，请重新选择。")


if __name__ == "__main__":
    main()

