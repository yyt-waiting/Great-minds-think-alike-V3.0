# ai_assistant/utils/config.py

import os
import numpy as np # [学术重构] 引入 Numpy 进行向量计算

# ==============================================================================
# 1. 基础服务配置 (API & Storage)
# ==============================================================================

# OSS (对象存储) 配置
OSS_ACCESS_KEY_ID = 'xxxxxxxxxxxxxxxxxx'
OSS_ACCESS_KEY_SECRET = 'xxxxxxxxxxxxxxxxxx'
OSS_ENDPOINT = 'xxxxxxxxxxxxxxxxxx'
OSS_BUCKET = 'xxxxxxxxxxxxxxxxxx'

# Deepseek API 配置 (大脑)
DEEPSEEK_API_KEY = 'xxxxxxxxxxxxxxxxxx'
DEEPSEEK_BASE_URL = 'xxxxxxxxxxxxxxxxxx'

# Qwen-VL API 配置 (视觉)
QWEN_API_KEY = "xxxxxxxxxxxxxxxxxx"
QWEN_BASE_URL = "xxxxxxxxxxxxxxxxxx"

# TTS & ASR 配置
TTS_MODEL = "xxxxxxxxxxxxxxxxxx"
TTS_VOICE = "xxxxxxxxxxxxxxxxxx"
ASR_MODEL_DIR = "xxxxxxxxxxxxxxxxxx"

# 音频录制参数
AUDIO_CHUNK = 1024
AUDIO_FORMAT = 16
AUDIO_CHANNELS = 1
AUDIO_RATE = 16000
AUDIO_WAVE_OUTPUT_FILENAME = "output.wav"

# ==============================================================================
# 2. Phase X: 情感计算数学模型 (Perception & Math Core)
# ==============================================================================

# 图像分析频率 (秒)
ANALYSIS_INTERVAL_SECONDS = 15

# Plutchik 8种基础情绪维度 (学术标准)
PLUTCHIK_EMOTIONS = [
    "喜悦", "信任", "恐惧", "惊讶", 
    "悲伤", "厌恶", "愤怒", "期待"
]

# 默认零向量
DEFAULT_EMOTION_VECTOR = {k: 0.0 for k in PLUTCHIK_EMOTIONS}

# --- [学术重构] 向量空间定义 ---

# 1. Plutchik 空间的基向量 (Basis Vectors, 8维正交基)
BASIS_VECTORS = {
    "喜悦": np.array([1, 0, 0, 0, 0, 0, 0, 0]),
    "信任": np.array([0, 1, 0, 0, 0, 0, 0, 0]),
    "恐惧": np.array([0, 0, 1, 0, 0, 0, 0, 0]),
    "惊讶": np.array([0, 0, 0, 1, 0, 0, 0, 0]),
    "悲伤": np.array([0, 0, 0, 0, 1, 0, 0, 0]),
    "厌恶": np.array([0, 0, 0, 0, 0, 1, 0, 0]),
    "愤怒": np.array([0, 0, 0, 0, 0, 0, 1, 0]),
    "期待": np.array([0, 0, 0, 0, 0, 0, 0, 1]),
}

# 2. UI 状态质心向量 (Centroids of UI States)
UI_CENTROIDS = {
    "开心": np.array([0.8, 0.2, 0, 0, 0, 0, 0, 0]),
    "惊讶": np.array([0, 0, 0.5, 0.8, 0, 0, 0, 0]),
    "沮丧": np.array([0, 0, 0, 0, 0.9, 0, 0, 0]),
    "生气": np.array([0, 0, 0, 0, 0, 0.4, 0.8, 0]),
    "专注": np.array([0, 0.1, 0, 0, 0, 0, 0, 0.9]),
    "平静": np.array([0, 0, 0, 0, 0, 0, 0, 0]),
}

# --- [Phase X.2 新增] 基于大五人格 (OCEAN) 的参数映射 ---

# 定义数字生命的人格特质 (0.0 - 1.0)
PERSONALITY_PROFILE = {
    "O": 0.5, # 开放性
    "C": 0.8, # 尽责性
    "E": 0.6, # 外向性
    "A": 0.9, # 宜人性
    "N": 0.4  # 神经质
}

# 动态计算惯性系数 (Inertia)
# N越高，情绪越容易波动(惯性小)
def get_derived_inertia():
    N = PERSONALITY_PROFILE["N"]
    return max(0.1, 0.8 - 0.5 * N)

EMOTION_INERTIA = get_derived_inertia()

# 动态计算稳态衰减率 (Homeostatic Decay Rate)
# 模拟能量耗散，E越高恢复越快
def get_derived_decay_rate():
    E = PERSONALITY_PROFILE["E"]
    return 0.05 + 0.05 * E

HOMEOSTATIC_DECAY = get_derived_decay_rate()

# -----------------------------------------------------

COMPOUND_THRESHOLD = 5.0    # 复合情绪激活阈值
FUZZY_SIGMOID_SLOPE = 2.0   # Sigmoid 斜率
FUZZY_SIGMOID_OFFSET = 5.0  # Sigmoid 中点

# 负面情绪列表 (用于兼容)
NEGATIVE_EMOTIONS = ["沮丧", "生气", "疲惫"] 
EMOTION_TRIGGER_THRESHOLD = 1

# ==============================================================================
# 3. Phase 2: 决策内核配置 (POMDP / Utility Function)
# ==============================================================================

class ACTIONS:
    WAIT = "静默观察"
    LIGHT_CARE = "轻度关怀"
    DEEP_INTERVENTION = "深度干预"

REWARD_CONFIG = {
    ("专注", ACTIONS.WAIT): 5.0,
    ("专注", ACTIONS.LIGHT_CARE): -5.0,
    ("专注", ACTIONS.DEEP_INTERVENTION): -20.0,

    ("焦虑", ACTIONS.WAIT): -10.0,
    ("焦虑", ACTIONS.LIGHT_CARE): 5.0,
    ("焦虑", ACTIONS.DEEP_INTERVENTION): 10.0,

    ("沮丧", ACTIONS.WAIT): -2.0,
    ("沮丧", ACTIONS.LIGHT_CARE): 8.0,
    ("沮丧", ACTIONS.DEEP_INTERVENTION): 2.0,

    ("开心", ACTIONS.WAIT): 2.0,
    ("开心", ACTIONS.LIGHT_CARE): 6.0,
    ("开心", ACTIONS.DEEP_INTERVENTION): -5.0
}

DEFAULT_REWARD = 0.0

# ==============================================================================
# 4. Phase 3: 认知行为疗法 (CBT) 与交互配置
# ==============================================================================

AROUSAL_THRESHOLD_HIGH = 7.5

CBT_SYSTEM_PROMPT = """
你现在不仅仅是婉晴，更是一位应用“认知行为疗法(CBT)”的心理辅助伙伴。
检测到用户当前处于【高强度负面情绪】状态。
请严格遵守以下干预步骤：
1. **接纳与共情**：确认用户情绪。
2. **苏格拉底式提问**：引导用户思考想法的真实性。
3. **认知重构**：寻找替代想法。
4. **行为着地**：建议深呼吸或喝水。
"""

SUMMARY_HOTKEY = "ctrl+shift+s"
LOG_FILE = "behavior_log.txt"

# [Phase 4 补全] 每日总结调度配置
DAILY_SUMMARY_HOUR = 17   # 下午 5 点
DAILY_SUMMARY_MINUTE = 30 # 30 分

# ==============================================================================
# 5. UI 与 字体配置
# ==============================================================================
try:
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    
    chinese_fonts = ['SimHei', 'Microsoft YaHei', 'SimSun', 'NSimSun', 'FangSong', 'KaiTi']
    chinese_font = None
    
    for font_name in chinese_fonts:
        try:
            font_path = fm.findfont(fm.FontProperties(family=font_name))
            if os.path.exists(font_path):
                chinese_font = font_name
                break
        except:
            continue
    
    if chinese_font:
        plt.rcParams['font.sans-serif'] = [chinese_font, 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
except Exception as e:
    print(f"Font loading error: {e}")