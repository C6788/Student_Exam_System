石驭元-25318049 - 第二次人工智能编程作业
1. 任务拆解与 AI 协作策略
在本次开发中，我将任务拆解为三个阶段，分步向 AI 下达指令，以避免 AI 产生逻辑幻觉：

步骤 1： 首先要求 AI 构建 Student 类。我刻意限制 AI 不要在此阶段涉及任何文件操作，仅专注于数据结构的定义（__init__）和对象的序列化表达（__str__），确保系统拥有一个干净、标准的底层数据流。

步骤 2： 让 AI 编写 ExamSystem 类，接管所有业务逻辑。我要求 AI 将系统划分为“内存数据初始化 (load_data)”、“只读查询 (search_student, roll_call)”和“状态变更与 IO 写入 (generate_schedule)”三个逻辑层，确保数据的加载与消费相互独立。

步骤 3： 在核心逻辑跑通后，我专门针对系统的“脆弱点”进行了一轮强化 Prompt。要求 AI 在所有涉及本地存储交互的地方，必须加入 os.path 路径校验和 try-except 异常熔断机制，防止程序因环境问题崩溃。

2. 核心 Prompt 迭代记录
在开发“生成考场安排表与准考证”模块时，AI 初次生成的代码虽然能运行，但存在严重的工程隐患：

初代 Prompt (功能导向)：

“请在 ExamSystem 类中添加生成考场安排表和准考证的功能。要求打乱学生顺序，第一行附带生成时间，并且为每个人生成一个 01.txt 这样的准考证文件。只能用标准库。”

AI 生成的隐患/缺陷 (Code Smell)：

1：AI 直接对 self.students 执行了 random.shuffle()。这导致考场表生成后，系统内存中的原始名单顺序被永久破坏，引发了后续其他功能的逻辑混乱。

2：AI 简单粗暴地使用了 open("01.txt", "w")，导致几十个准考证文件直接像垃圾一样散落在项目的根目录下，严重污染了工程结构。

3：时间获取逻辑 (time.strftime) 被硬编码在了文件写入的循环内部，复用性极差。

优化后的 Prompt (架构约束与追问)：

“你刚才的代码有致命缺陷，请按以下要求重构：

1：在进行打乱操作前，必须使用 .copy() 将数据克隆到独立属性 self.scheduled_students 中，绝对禁止污染原始 self.students 名单！

2：引入 os 库，在生成准考证前，必须先检测并动态创建一个名为 准考证 的专属文件夹，通过 os.path.join 将所有碎片文件路由到该目录下。

3：将时间获取逻辑从循环中剥离，强制提纯为一个 @staticmethod 命名为 get_formatted_time()，专门负责吐出 YYYY-MM-DD HH:MM:SS 格式的时间字符串供外部调用。”

3. Debug 与异常处理记录
漏洞现象： 在测试“随机点名”功能时，如果输入的数字包含了隐藏的空白字符（，或者直接输入了英文字母 abc，控制台会直接抛出红色的 ValueError 堆栈错误，导致整个系统进程强行闪退。

解决过程： 我没有完全依赖 AI 来处理这个细节，而是自己通过阅读 Traceback 锁定了崩溃点发生在 int(count_str) 这一行。随后，我在该层外包裹了 try-except ValueError 拦截器。同时，为了防止输入数量大于实际名单人数导致 random.sample 越界崩溃，我手工补充了 if count > len(self.students): 的前置边界条件防御。不仅捕获了异常，还保障了交互的连贯性。

4. 人工代码审查 (Code Review)
以下是我针对 信息初始化加载 (load_data) 模块的人工审查与逐行批注。这部分代码涉及关键的文件 IO 和数据清洗，我已充分理解其底层机制：


    def load_data(self):
        """信息初始化：读取文本文件并解析为 Student 对象"""
        try:
            # 明确声明 encoding='utf-8'，避免在不同操作系统下产生中文乱码
            with open(self.file_path, 'r', encoding='utf-8') as f:
                # 采用迭代器按行读取文件，而非 readlines() 一次性吞入，这在处理超大名单时内存占用极低
                for line in f:
                    # strip() 剥离头尾换行符和不可见空格，split() 默认以任意空白字符为分隔符将字符串切片
                    parts = line.strip().split()
                    
                    # 过滤掉文末可能存在的空行或格式不全的脏数据，确保解包安全
                    if len(parts) >= 5:
                        # 严格按照列顺序，将清洗后的字符串实例化为 Student 数据模型
                        student = Student(parts[4], parts[1], parts[2], parts[3], parts[5])
                        # 装载入系统的持久化内存列表
                        self.students.append(student)
                        
            print(f"✅ 系统初始化成功！共加载 {len(self.students)} 名学生信息。")
            
        # 文件路径错误时，向用户抛出通俗易懂的 UI 提示，而不是在底层代码堆栈
        except FileNotFoundError:
            print(f"❌ 严重错误：未找到数据文件 '{self.file_path}'。请确保文件存在于根目录。")