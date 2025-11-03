import streamlit as st

# --- 页面配置 (Apple风格) ---
# "centered" 布局能让内容居中，限制宽度，在宽屏上更像一个简洁的App
# "page_icon" 可以用emoji
st.set_page_config(
    page_title="AI 隐私政策生成器",
    page_icon="🛡️",
    layout="centered"
)

# --- 侧边栏 (可选，但很专业) ---
# 放置你的项目名称和目标，让主页更干净
with st.sidebar:
    st.image(
        "https://www.apple.com/ac/globalnav/7/zh_CN/images/be15095f-5a20-57d0-ad14-ca0c6df74a38/globalnav_apple_image__b5er5ngrzxqq_large.svg",
        width=50)
    st.header("AI隐私工程核查清单🧾")
    st.markdown("`august-privacy-engineer-mvp`")  # 替换成你的GitHub仓库名

    st.info("""
    **项目目标:** 一个面向深圳智能硬件创业者的AI隐私政策生成器，
    帮助他们快速生成符合GDPR的初步隐私政策文本。
    """)

# --- 主界面 ---

# 1. 标题和简介
st.title("AI 隐私政策生成器")
st.markdown("专为智能硬件创业者打造。请如实回答以下问题，AI 将为您生成合规的隐私政策初稿。")

# 用一个分隔符来增加“呼吸感”
st.divider()

# --- 问卷表单 ---
# 使用 st.form 可以让所有组件被“包裹”起来，
# 只有在点击表单内的"提交"按钮时，所有数据才会一次性提交
# 这可以防止用户每点一个选项就导致页面刷新，体验更好
with st.form(key="privacy_questionnaire"):
    # 问题1: PII
    st.subheader("1. 你的设备或App是否会要求用户提供“个人身份信息 (PII)”？")
    q1 = st.radio(
        "q1_pii",  # 每个组件都需要一个唯一的key
        options=["否", "是 (例如：姓名、邮箱、手机号、家庭住址、身份证号)"],
        label_visibility="collapsed",  # 隐藏 "q1_pii" 这个标签, 界面更干净
        horizontal=True  # 水平排列选项
    )

    # 问题2: 传感器数据
    st.subheader("2. 你的智能硬件设备会收集以下哪类“传感器数据”？")
    q2 = st.multiselect(
        "q2_sensors",
        options=[
            "GPS位置 (包括历史轨迹)",
            "摄像头影像 (视频或照片)",
            "麦克风音频 (录音或语音指令)",
            "健康与生物特征 (心率、血氧、睡眠、体重、指纹、面容ID)",
            "运动数据 (步数、姿态、速度)",
            "环境数据 (温度、湿度、空气质量)",
            "我的设备不收集任何传感器数据"
        ],
        label_visibility="collapsed"
    )

    # 问题3: 服务器位置
    st.subheader("3. 收集到的用户数据主要存储在哪个国家或地区的服务器上？")
    q3 = st.radio(
        "q3_location",
        options=["仅在中国大陆", "仅在欧盟 (EU) 境内", "仅在美国 (US) 境内", "存储在全球多个地区", "不确定 / 其他"],
        label_visibility="collapsed"
    )

    # 问题4: 收集目的
    st.subheader("4. 你收集这些数据的主要目的是什么？")
    q4 = st.multiselect(
        "q4_purpose",
        options=[
            "核心功能：实现产品承诺的核心功能 (如：运动App必须获取步数)",
            "体验优化：分析使用习惯，用于App迭代或Bug修复",
            "个性化服务：用于个性化推荐或定向广告",
            "算法训练：用于优化AI模型",
            "安全风控：用于保障账号和设备安全"
        ],
        label_visibility="collapsed"
    )

    # 问题5: 第三方共享
    st.subheader("5. 你是否会将收集到的用户数据“共享”或“传输”给第三方公司？")
    q5 = st.multiselect(
        "q5_sharing",
        options=[
            "是，会共享给广告或营销伙伴",
            "是，会共享给数据分析服务商 (如 谷歌分析、友盟等)",
            "是，数据会存储在云服务商 (如 阿里云、AWS、腾讯云等)",
            "否，完全不与任何第三方共享或传输"
        ],
        label_visibility="collapsed",
        help="第三方指你的公司和你用户之外的任何一方"
    )

    # 问题6: 行为或社交数据
    st.subheader("6. 你的配套App或服务是否会收集用户的“行为或社交”数据？")
    q6 = st.multiselect(
        "q6_behavioral",
        options=[
            "App操作日志 (用户点击了哪些按钮、停留时长)",
            "支付信息 (信用卡号、支付宝/微信账户)",
            "第三方账号信息 (如允许微信/Google/Apple登录)",
            "用户的联系人列表 (通讯录)",
            "完全不收集"
        ],
        label_visibility="collapsed"
    )

    # 问题7: 儿童
    st.subheader("7. 你的产品或服务是否主要面向“儿童”？")
    q7 = st.radio(
        "q7_children",
        options=["否，我的产品面向成人", "是，我的产品是为儿童设计的 (如：儿童手表、早教机)"],
        label_visibility="collapsed",
        horizontal=True,
        help="GDPR中对儿童有极其严格的特殊保护，通常指16岁以下"
    )

    # 问题8: 用户权限
    st.subheader("8. 用户是否有途径可以访问、修改或删除他们自己的个人数据？")
    q8 = st.radio(
        "q8_access",
        options=[
            "是，用户可以在App或设备内自行操作 (如“我的账户”里)",
            "是，但用户必须通过联系客服来申请处理",
            "否，目前没有提供此功能"
        ],
        label_visibility="collapsed"
    )

    # 问题9: 泄露应急
    st.subheader("9. 当发生数据泄露（例如黑客攻击）时，你是否有应急响应流程？")
    q9 = st.radio(
        "q9_breach",
        options=["否，目前还没有考虑过", "是，我们有内部的应急预案"],
        label_visibility="collapsed",
        horizontal=True
    )

    # 问题10: 联系方式
    st.subheader("10. 用户应该通过什么方式联系你（的公司）来咨询隐私问题？")
    q10 = st.radio(
        "q10_contact",
        options=[
            "提供一个专门的电子邮箱 (例如: privacy@yourcompany.com)",
            "用户可以通过App内的在线客服系统联系",
            "用户可以拨打公司客服电话",
            "尚未确定联系方式"
        ],
        label_visibility="collapsed",
        help="这是GDPR强制要求的，必须提供一个联系点"
    )

    # --- 提交按钮 ---
    st.divider()  # 最后的分隔符

    # 任务要求：一个"生成"按钮
    # st.form_submit_button 会自动触发表单提交
    submitted = st.form_submit_button(
        "开始生成隐私政策",
        type="primary",  # "primary" 类型会让按钮变成蓝色，更醒目
        use_container_width=True  # 让按钮和容器一样宽，更大气
    )

# --- 按钮点击后的逻辑 ---
# "if submitted:" 会在按钮被点击后变为 True
if submitted:
    # 任务要求：现在不需要AI功能，只需要让用户点击

    cross_border_prompt_template = """
       # 角色: 
你是一名精通GDPR的专业隐私顾问，特别擅长为智能硬件(IoT)创业公司起草清晰、合规的隐私政策。

# 任务:
基于用户提供的服务器位置和第三方共享情况，判断数据是否被传输至欧盟经济区(EEA)之外。如果是，请生成一段隐私政策条款，清晰地向用户解释其数据跨境传输的全部合规性基础。

# 事实背景 (由用户问卷提供):
1.  **设备收集的数据类型**: [组合Q1, Q2, Q6的答案, 例如：个人身份信息、GPS位置、App操作日志]
2.  **数据存储的服务器位置**: [来自Q3的答案, 例如：仅在中国大陆]
3.  **是否与EEA外的第三方共享**: [基于Q5答案的判断, 例如：是 (共享给美国的数据分析商)]

# 生成指示:
1.  **判断逻辑**: 
    仔细分析 [服务器位置] 和 [是否与EEA外的第三方共享]。

2.  **撰写条款 (请严格遵循以下逻辑)**:

    * **情况A：如果 [服务器位置] 是 "仅在欧盟 (EU) 境内" 并且 [是否与EEA外的第三方共享] 为 "否"**:
        (这是最简单的情况：数据不出境)
        请生成一段条款，向用户保证：他们的数据将严格在欧盟境内存储和处理，并受到GDPR的全面保护。

    * **情况B：如果 [服务器位置] 是 "EEA 境外" (例如 "仅在中国大陆", "仅在美国", 或 "存储在全球多个地区")**:
        (这是最主要的情况：主服务器在境外)
        请必须生成一段条款，包含以下三个关键点：
        a. **(透明度)** 明确告知用户，为了提供服务，他们的个人数据（[设备收集的数据类型]）将被传输并存储在位于 [服务器位置] 的服务器上。
        b. **(主要合规基础 - Art. 46)** 解释说明，由于该地区未获得欧盟委员会的“充分性认定”，我们将**主要依赖欧盟委员会批准的“标准合同条款 (Standard Contractual Clauses, SCCs)”** 作为数据传输的适当保障措施。
        c. **(次要合规基础 - Art. 49)** 补充说明，对于某些特定的、非必要的传输，我们也可能在征得您同意的情况下，依赖您的**“明确同意” (Explicit Consent)** 作为法律基础。
        d. **(用户保障)** 向用户承诺，无论数据在何处，公司都将采取一切合理的技术和组织措施（如数据加密）来确保其安全。

    * **情况C：如果 [服务器位置] 是 "仅在欧盟 (EU) 境内" 但是 [是否与EEA外的第三方共享] 为 "是"**:
        (这是“隐藏传输”：主服务器在境内，但共享出去了)
        请生成一段条款，说明：
        a. **(透明度)** "我们主要将您的数据存储在欧盟境内。但是，为了实现特定功能（例如数据分析、广告），您的部分数据（[设备收集的数据类型]）可能会被传输给位于EEA境外的第三方合作伙伴（例如位于[第三方国家，如美国]的服务商）。"
        b. **(合规基础)** "对于此类传输，我们将同样依赖 **“标准合同条款 (SCCs)”** 或在征得您 **“明确同意” (Explicit Consent)** 的前提下进行，以确保您的数据安全。"
        
        
        5.  **语言风格**: 必须专业、透明、易于理解。
      

    # 我们可以先给一个友好的提示，表示已收到
    with st.spinner("正在分析您的需求，请稍候..."):
        import time

        time.sleep(1)  # 模拟AI思考

    st.success("问卷提交成功！AI引擎正在启动... (下一步我们将实现AI逻辑)")

    # 作为验证，我们可以把用户的所有回答先打印出来（方便调试）
    with st.expander("查看我的回答摘要"):
        st.write("**1. 收集PII:**", q1)
        st.write("**2. 传感器数据:**", "、".join(q2) if q2 else "无")
        st.write("**3. 存储位置:**", q3)
        st.write("**4. 收集目的:**", "、".join(q4) if q4 else "无")
        st.write("**5. 第三方共享:**", "、".join(q5) if q5 else "无")
        st.write("**6. 行为数据:**", "、".join(q6) if q6 else "无")
        st.write("**7. 面向儿童:**", q7)
        st.write("**8. 用户数据权限:**", q8)
        st.write("**9. 泄露应急:**", q9)
        st.write("**10. 联系方式:**", q10)