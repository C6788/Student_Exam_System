import os
import random
import time

class Student:
    """学生数据类"""

    def __init__(self, stu_id, name, gender, class_name, college):
        # 初始化属性，符合硬性要求
        self.stu_id = stu_id
        self.name = name
        self.gender = gender
        self.class_name = class_name
        self.college = college

    def __str__(self):
        # 友好的字符串表达，用于打印对象信息
        return f"学号: {self.stu_id} | 姓名: {self.name} | 性别: {self.gender} | 班级: {self.class_name} | 学院: {self.college}"