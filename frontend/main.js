// 当 HTML 文档完全加载并解析完成后执行
document.addEventListener('DOMContentLoaded', () => {

    const API_BASE_URL = 'http://localhost:8000/api';

    // === 1. 查找学生功能 ===
    document.getElementById('searchBtn').addEventListener('click', async () => {
        const stuId = document.getElementById('studentIdInput').value.trim();
        const resultBox = document.getElementById('searchResult');

        if (!stuId) {
            resultBox.innerHTML = '<span style="color: red;">请输入学号！</span>';
            return;
        }

        resultBox.innerHTML = '正在查询...';

        try {
            const response = await fetch(`${API_BASE_URL}/search?id=${stuId}`);
            const data = await response.json();

            // 【修复】双重校验：网络请求成功 且 后端明确返回了 success: true
            if (response.ok && data.success) {
                resultBox.innerHTML = `
                    <strong>姓名:</strong> ${data.name} <br>
                    <strong>性别:</strong> ${data.gender} <br>
                    <strong>班级:</strong> ${data.class_name} <br>
                    <strong>学院:</strong> ${data.college}
                `;
            } else {
                // 读取后端传来的 message
                resultBox.innerHTML = `<span style="color: red;">${data.message || '未找到该学生'}</span>`;
            }
        } catch (error) {
            resultBox.innerHTML = `<span style="color: red;">网络请求失败，请检查 Python 后端是否已启动。</span>`;
            console.error('Fetch error:', error);
        }
    });

    // === 2. 随机点名功能 ===
    document.getElementById('rollCallBtn').addEventListener('click', async () => {
        const count = document.getElementById('rollCallCount').value;
        const resultList = document.getElementById('rollCallResult');
        resultList.innerHTML = '';

        if (!count || count <= 0) {
            alert('请输入有效的人数！');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/rollcall`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ count: parseInt(count) })
            });
            const data = await response.json();

            // 【修复】校验 data.students 是否存在且为数组，防止 forEach 崩溃
            if (response.ok && Array.isArray(data.students)) {
                data.students.forEach((student, index) => {
                    const li = document.createElement('li');
                    li.textContent = `${index + 1}. ${student.name} (${student.id})`;
                    resultList.appendChild(li);
                });
            } else {
                alert(data.message || '点名失败或数量无效');
            }
        } catch (error) {
            alert('网络请求失败，请检查 Python 后端服务。');
        }
    });

    // === 3. 生成文件功能 ===
    const handleFileGeneration = async (endpoint, btnId, successMsg) => {
        const btn = document.getElementById(btnId);
        const statusBox = document.getElementById('fileSystemStatus');

        btn.disabled = true;
        statusBox.innerHTML = '正在处理文件，请稍候...';

        try {
            const response = await fetch(`${API_BASE_URL}/${endpoint}`, { method: 'POST' });
            const data = await response.json();

            // 【修复】根据后端返回的 status 字段严格判断是否真的成功
            if (response.ok && data.status === "success") {
                statusBox.innerHTML = `<span style="color: green;">✅ ${successMsg}</span>`;
            } else {
                statusBox.innerHTML = `<span style="color: red;">❌ 错误: ${data.message || '操作失败'}</span>`;
            }
        } catch (error) {
            statusBox.innerHTML = `<span style="color: red;">网络请求失败，请检查 Python 后端。</span>`;
        } finally {
            btn.disabled = false;
        }
    };

    document.getElementById('generateScheduleBtn').addEventListener('click', () => {
        handleFileGeneration('generate_schedule', 'generateScheduleBtn', '考场安排表.txt 已成功生成在根目录！');
    });

    document.getElementById('generateTicketsBtn').addEventListener('click', () => {
        handleFileGeneration('generate_tickets', 'generateTicketsBtn', '准考证文件已成功生成在目录中！');
    });
});