from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域问题（前端HTML直接打开时必须加）
import tensorflow as tf
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # 允许所有跨域请求（开发环境用，生产环境可限制域名）

# -------------------------- 关键配置（必须与训练模型一致） --------------------------
# 1. 模型路径：替换为你训练好的模型路径（如.h5文件）
MODEL_PATH = "C:\\Users\\29137\\zhongyao_model.h5"  # 与之前训练代码的保存路径一致
# 2. 类别映射：与前端 herbData 字典的中文名称完全对应（顺序必须和模型输出一致）
CLASS_NAMES = ["百合", "党参", "枸杞", "槐花", "金银花"]  # 模型输出索引对应的中文类别
CLASS_NAMES_EN = ["Lily", "Dangshen", "Goji Berry", "Sophora Flower", "Honeysuckle"]  # 英文名称（可选）
# 3. 图片尺寸：与训练模型的输入尺寸一致（之前代码是224x224）
IMG_SIZE = (224, 224)

# -------------------------- 加载模型（启动后端时加载，避免重复加载） --------------------------
try:
    # 加载训练好的模型（确保模型文件存在）
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"模型加载成功：{MODEL_PATH}")
except Exception as e:
    print(f"模型加载失败！错误：{str(e)}")
    print("请检查 MODEL_PATH 是否正确，或模型文件是否损坏")
    exit()  # 模型加载失败时，后端直接退出


# -------------------------- 核心识别接口（/predict） --------------------------
@app.route("/predict", methods=["POST"])
def predict():
    # 1. 接收前端上传的图片文件
    if "file" not in request.files:
        return jsonify({"error": "未上传图片文件"}), 400  # 前端会显示“识别失败：未上传图片文件”
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "请选择图片后上传"}), 400
    
    # 2. 验证图片格式
    allowed_extensions = {"jpg", "jpeg", "png"}
    if not file.filename.lower().endswith(tuple(allowed_extensions)):
        return jsonify({"error": "仅支持JPG、PNG格式图片"}), 400
    
    # 3. 处理图片（与训练时的预处理完全一致）
    try:
        # 读取图片并调整尺寸
        img = Image.open(file.stream).convert("RGB")  # 确保图片为RGB格式（避免透明通道问题）
        img = img.resize(IMG_SIZE)  # 缩放到模型输入尺寸（224x224）
        img_array = tf.keras.preprocessing.image.img_to_array(img)  # 转为数组
        img_array = tf.expand_dims(img_array, 0)  # 增加 batch 维度（模型要求输入为[batch, height, width, channel]）
        
        # 4. 模型预测（与训练时的预处理函数一致）
        img_array = tf.keras.applications.vgg16.preprocess_input(img_array)  # VGG16预处理（必须和训练一致）
        predictions = model.predict(img_array, verbose=0)  # 预测（verbose=0 不打印日志）
        
        # 5. 解析预测结果
        predicted_idx = np.argmax(predictions[0])  # 获取概率最大的类别索引
        confidence = float(predictions[0][predicted_idx])  # 获取该类别的置信度（0-1）
        breed = CLASS_NAMES[predicted_idx]  # 中文类别名称
        breed_english = CLASS_NAMES_EN[predicted_idx]  # 英文类别名称
        
        # 6. 返回结果给前端（格式必须和前端期望一致）
        return jsonify({
            "breed": breed,
            "breed_english": breed_english,
            "confidence": confidence  # 前端会转为百分比（如0.98 → 98%）
        })
    
    except Exception as e:
        # 捕获图片处理或预测过程中的错误
        return jsonify({"error": f"图片处理失败：{str(e)}"}), 500


# -------------------------- 启动后端服务 --------------------------
if __name__ == "__main__":
    # 注意：host="0.0.0.0" 允许局域网访问，port=8000 必须和前端一致
    app.run(host="0.0.0.0", port=8000, debug=True)