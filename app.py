
# app.py (V3 - 极简和原生主题版)
# 
# 移除了所有CSS注入。
# 风格现在 100% 由 .streamlit/config.toml 控制。
# 
import streamlit as st
import time
from openai import OpenAI
import re

# --- 页面配置 ---
# (注意：不再有CSS注入)
st.set_page_config(
    page_title="AI 隐私政策生成器 (V3)",
    page_icon="🛡️",
    layout="centered" # "centered" 布局对表单最友好
)

# --- 侧边栏 ---
with st.sidebar:
    st.image("https://www.apple.com/ac/globalnav/7/zh_CN/images/be15095f-5a20-57d0-ad14-ca0c6df74a38/globalnav_apple_image__b5er5ngrzxqq_large.svg", width=50)
    st.header("项目：兵工厂 (V3)")
    st.markdown("`zhangwei-privacy-engineer-mvp`")
    st.info("""
    **V3 更新:** 采用原生主题，修复所有UI BUG。
    """)
    st.divider()
    try:
        st.secrets["DEEPSEEK_API_KEY"]
        st.success("API 密钥已通过 st.secrets 安全加载。")
    except KeyError:
        st.error("API Key 未配置！请检查 .streamlit/secrets.toml 文件。")
    except FileNotFoundError:
        st.error("未找到 secrets.toml 文件！")


# --- 黄金标准 (Gold Standard) 加载函数 (未改变) ---
@st.cache_data
def load_gold_standards(file_path="gold_standards.md"):
    standards = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        sections = re.split(r'### (CASE_[ABC])\n', content)
        if len(sections) < 2: return {"Error": "gold_standards.md 文件格式不正确"}
        for i in range(1, len(sections), 2):
            key = sections[i].strip()
            value = sections[i+1].strip()
            standards[key] = value
        if "CASE_A" not in standards or "CASE_B" not in standards or "CASE_C" not in standards:
            return {"Error": "gold_standards.md 文件不完整, 必须包含 CASE_A, B, C"}
        return standards
    except FileNotFoundError:
        return {"Error": f"关键文件 '{file_path}' 未找到！"}
    except Exception as e:
        return {"Error": f"读取 gold_standards.md 时出错: {e}"}

# --- API 调用函数 (未改变) ---
def get_deepseek_response(api_key, prompt_text):
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt_text}]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"调用AI时出错：{e}")
        return None

# --- 主界面 ---
st.title("AI 隐私政策生成器")
st.markdown("请回答问卷，AI 将生成初稿，并**自动进行“质检”**。")

# --- 问卷表单 (格式已全面更新为原生组件) ---
with st.form(key="privacy_questionnaire"):

    # (--- 问卷模块一 ---)
    st.header("模块一：数据收集清单 (What & Why)")
    
    # [STYLE] Q1 (原生 st.subheader + st.radio)
    st.subheader("1. 你的设备是否收集“个人身份信息 (PII)”？")
    q1_pii = st.radio(
        "q1_pii_key", # Key
        options=["否", "是 (例如：姓名、邮箱、手机号)"], 
        horizontal=True,
        label_visibility="collapsed" # 隐藏默认标签, 只显示 subheader
    )
    
    # [STYLE] Q2 (原生 st.subheader + st.checkbox)
    st.subheader("2. 你的智能硬件设备会收集以下哪类“传感器数据”？")
    q2_sensor_labels = [
        "GPS位置 (包括历史轨迹)", "摄像头影像 (视频或照片)", "麦克风音频 (录音或语音指令)",
        "健康与生物特征 (心率、血氧、指纹)", "运动数据 (步数、姿态)", "环境数据 (温度、湿度)",
        "我的设备不收集任何传感器数据"
    ]
    q2_sensor_checks = [st.checkbox(label, key=f"q2_{i}") for i, label in enumerate(q2_sensor_labels)]

    # [STYLE] Q3 
    st.subheader("3. 你的配套App或服务是否会收集用户的“行为或社交”数据？")
    q3_behavioral_labels = ["App操作日志 (点击、停留时长)", "支付信息", "第三方账号信息 (微信/Google登录)", "用户的联系人列表 (通讯录)", "完全不收集"]
    q3_behavioral_checks = [st.checkbox(label, key=f"q3_{i}") for i, label in enumerate(q3_behavioral_labels)]

    # [STYLE] Q4
    st.subheader("4. 你收集这些数据的主要目的是什么？ (此项用于未来功能)")
    q4_purpose_labels = ["核心功能", "体验优化", "个性化服务/广告", "算法训练", "安全风控"]
    q4_purpose_checks = [st.checkbox(label, key=f"q4_{i}") for i, label in enumerate(q4_purpose_labels)]

    # (--- 问卷模块二 ---)
    st.header("模块二：数据流转与跨境 (Where & Who)")
    
    # [STYLE] Q5
    st.subheader("5. 你的主服务器存储在哪个国家或地区？")
    q5_location = st.radio(
        "q5_location_key",
        options=["仅在中国大陆", "仅在欧盟 (EU) 境内", "仅在美国 (US) 境内", "存储在全球多个地区", "不确定 / 其他"],
        label_visibility="collapsed"
    )
    
    # [STYLE] Q6
    st.subheader("6. 你是否会将数据“共享”给第三方公司？")
    q6_sharing_labels = ["广告或营销伙伴", "数据分析服务商 (如 谷歌分析)", "云服务商 (如 阿里云, AWS)", "否，完全不与任何第三方共享"]
    q6_sharing_checks = [st.checkbox(label, key=f"q6_{i}") for i, label in enumerate(q6_sharing_labels)]

    # [STYLE] Q7
    st.subheader("7. [关键] 你 Q6 中的第三方服务商是否在欧盟(EU)以外的国家？")
    q7_third_party_location = st.radio(
        "q7_third_party_location_key",
        options=[
            "是，他们中至少有一个在欧盟以外 (例如 Google, AWS, OpenAI, 阿里云等)",
            "否，我确认我所有的服务商都在欧盟境内",
            "我不确定 (法律上视同'是')"
        ],
        label_visibility="collapsed"
    )

    # (--- 问卷模块三 ---)
    st.header("模块三：合规与安全 (How) (此项用于未来功能)")
    
    # [STYLE] Q8
    st.subheader("8. 你的产品是否主要面向“儿童”？")
    q8_children = st.radio("q8_children_key", options=["否", "是"], horizontal=True, label_visibility="collapsed")
    
    # [STYLE] Q9
    st.subheader("9. 用户是否可以访问、修改或删除他们的数据？")
    q9_access = st.radio("q9_access_key", options=["是，可自助", "是，需联系客服", "否"], label_visibility="collapsed")
    
    # [STYLE] Q10
    st.subheader("10. 你是否有数据泄露应急流程？")
    q10_breach = st.radio("q10_breach_key", options=["否", "是"], horizontal=True, label_visibility="collapsed")
    
    # [STYLE] Q11
    st.subheader("11. 用户通过什么方式联系你？")
    q11_contact = st.radio("q11_contact_key", options=["电子邮箱", "在线客服", "电话", "尚未确定"], label_visibility="collapsed")

    # (--- 提交按钮 ---)
    st.divider()
    submitted = st.form_submit_button(
        "生成条款并进行AI质检",
        type="primary", # 将使用 config.toml 中的 primaryColor
        use_container_width=True
    )

# --- 按钮点击后的逻辑 (未改变) ---
if submitted:
    
    # 1. 加载黄金标准
    gold_standards = load_gold_standards()
    if "Error" in gold_standards:
        st.error(f"黄金标准文件加载失败: {gold_standards['Error']}")
        st.stop()

    # 2. 收集输入 & 检查 Key
    with st.spinner("正在收集您的回答..."):
        time.sleep(0.5)
        try:
            api_key = st.secrets["DEEPSEEK_API_KEY"]
        except KeyError:
            st.error("未找到 API Key！请确保你已创建 .streamlit/secrets.toml 文件。")
            st.stop()
        
        # 收集 Checkbox 结果
        q2_selected = [q2_sensor_labels[i] for i, checked in enumerate(q2_sensor_checks) if checked]
        q2_sensors_str = ", ".join(q2_selected) if q2_selected else "无"
        q3_selected = [q3_behavioral_labels[i] for i, checked in enumerate(q3_behavioral_checks) if checked]
        q3_behavioral_str = ", ".join(q3_selected) if q3_selected else "无"
        q6_selected = [q6_sharing_labels[i] for i, checked in enumerate(q6_sharing_checks) if checked]
        q6_sharing_str = ", ".join(q6_selected) if q6_selected else "无"
        
    # 3. 决定场景 (A, B, or C)
    case_key = ""
    if (q5_location == "仅在欧盟 (EU) 境内" and 
        q7_third_party_location == "否，我确认我所有的服务商都在欧盟境内"):
        case_key = "CASE_A"
    elif q5_location in ["仅在中国大陆", "仅在美国 (US) 境内", "存储在全球多个地区", "不确定 / 其他"]:
        case_key = "CASE_B"
    elif (q5_location == "仅在欧盟 (EU) 境内" and 
          q7_third_party_location in ["是，他们中至少有一个在欧盟以外 (例如 Google, AWS, OpenAI, 阿里云等)", "我不确定 (法律上视同'是')"]):
        case_key = "CASE_C"
    else:
        st.warning("未能匹配到标准场景，将默认使用 CASE_A (无跨境传输) 逻辑。")
        case_key = "CASE_A"

    st.info(f"已匹配到场景: **{case_key}**")

    # 4. 构建“初稿”的 Prompt (未改变)
    with st.spinner("正在参数化“初稿”弹药..."):
        draft_prompt = f"""
# 角色: 
你是一名精通GDPR的专业隐私顾问，特别擅长为智能硬件(IoT)创业公司起草清晰、合规的隐私政策。

# 任务:
基于用户提供的服务器位置和第三方共享情况，判断数据是否被传输至欧盟经济区(EEA)之外。如果是，请生成一段隐私政策条款，清晰地向用户解释其数据跨境传输的全部合K规性基础。

# 事实背景 (由用户问卷提供):
1.  设备收集的PII: {q1_pii}
2.  设备收集的传感器数据: {q2_sensors_str}
3.  设备收集的行为数据: {q3_behavioral_str}
4.  数据存储的服务器位置: {q5_location}
5.  第三方服务商位置: {q7_third_party_location}
6.  共享的第三方类型: {q6_sharing_str}

# 生成指示:
1.  **判断逻辑**: 
    仔细分析 [数据存储的服务器位置] 和 [第三方服务商位置]。

2.  **撰写条款 (请严格遵循以下逻辑)**:

    * **情况A：(数据完全不出境)**
        * **触发条件**: 
            * [数据存储的服务器位置] 是 "仅在欧盟 (EU) 境内" 
            * **并且** [第三方服务商位置] 是 "否，我确认我所有的服务商都在欧盟境内"
        * **生成内容**:
            请生成一段条款，向用户保证：他们的数据将严格在欧盟境内存储和处理，并受到GDPR的全面保护。

    * **情况B：(主服务器在境外)**
        * **触发条件**: 
            * [数据存储的服务器位置] 是 "仅在中国大陆", "仅在美国 (US) 境内", "存储在全球多个地区", 或 "不确定 / 其他" 
        * **生成内容**:
            请必须生成一段条款，包含以下三个关键点：
            a. **(透明度)** 明确告知用户，为了提供服务，他们的个人数据（包括 {q1_pii}、{q2_sensors_str}、{q3_behavioral_str}）将被传输并存储在位于 [{q5_location}] 的服务器上。
            b. **(主要合规基础 - Art. 46)** 解释说明，由于该地区未获得欧盟委员会的“充分性认定”，我们将主要依赖欧盟委员会批准的“标准合同条款 (Standard Contractual Clauses, SCCs)” 作为数据传输的适当保障措施。
            c. **(次要合规基础 - Art. 49)** 补充说明，对于某些特定的、非必要的传输（例如共享给 [{q6_sharing_str}]），我们也可能在征得您同意的情况下，依赖您的“明确同意” (Explicit Consent) 作为法律基础。
            d. **(用户保障)** 向用户承诺，无论数据在何处，公司都将采取一切合理的技术和组织措施（如数据加密）来确保其安全。

    * **情况C：(主服务器在境内，但第三方在境外)**
        * **触发条件**: 
            * [数据存储的服务器位置] 是 "仅在欧盟 (EU) 境内" 
            * **并且** [第三方服务商位置] 是 "是，他们中至少有一个在欧盟以外..." 或 "我不确定 (法律上视同'是')"
        * **生成内容**:
            请生成一段条款，说明：
            a. **(透明度)** "我们主要将您的数据存储在欧盟境内。但是，为了实现特定功能（例如 {q6_sharing_str}），您的部分数据（包括 {q1_pii}、{q2_sensors_str}、{q3_behavioral_str}）可能会被传输给位于EEA境外的第三方合作伙伴。"
            b. **(合规基础)** "对于此类传输，我们将同样依赖 “标准合同条款 (SCCs)” 或在征得您 “明确同意” (Explicit Consent) 的前提下进行，以确保您的数据安全。"
"""

    # 5. [步骤1 - 初稿] 第一次API调用 (未改变)
    with st.spinner("AI“大脑”正在生成初稿..."):
        draft_text = get_deepseek_response(api_key, draft_prompt)
    
    if not draft_text:
        st.error("AI 初稿生成失败，流程中止。")
        st.stop()
        
    # 6. [步骤2 - 批判] 第二次API调用 (未改变)
    with st.spinner("AI“质检员”正在批判初稿..."):
        gold_text = gold_standards.get(case_key, "错误：未找到对应的黄金标准。")
        
        critique_prompt = f"""
# 角色:
你是一名严格、吹毛K疵的法律合规官（QA）。你的唯一任务是对比 "AI初稿" 和 "黄金标准"。
# 任务:
请对比这两者，然后以列表形式清晰地指出 "AI初稿" 中：
1.  **遗漏的关键信息**: 遗漏了哪些 "黄金标准" 中提到的关键法律术语或承诺？ (例如：是否遗漏了 'SCCs' 或 '明确同意'?)
2.  **模糊的表述**: 存在哪些模糊不清、不准确或有潜在法律风险的表述？
3.  **(可选) 优点**: 有哪些 "AI初稿" 比 "黄金标准" 做得好的地方 (如果有)？
如果 "AI初稿" 质量很高，请明确表扬。如果 "AI初稿" 严重遗漏了关键信息，请严厉指出。
---
# [黄金标准 (专家范本 - 你必须以此为准)]
{gold_text}
---
# [AI初稿 (待质检)]
{draft_text}
---
# [你的质检报告 (请用 Markdown 列表格式化)]
"""
        
        critique_text = get_deepseek_response(api_key, critique_prompt)

    if not critique_text:
        st.error("AI 质检报告生成失败。")
        st.stop()

    # 7. (产出) 显示所有结果
    st.success("AI 生成及质检完成！")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 AI 生成的初稿：")
        st.markdown(draft_text)
        
    with col2:
        st.subheader("🧐 AI 质检员的批判报告：")
        st.markdown(critique_text)

    st.divider()
    
    with st.expander("点击查看本次对比使用的“黄金标准”原文 (来自 gold_standards.md)"):
        st.markdown(f"**匹配场景: {case_key}**")
        st.markdown(gold_text)