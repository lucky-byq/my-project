import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image
import io

# ================== 配置 ==================
MODEL_PATH = r'C:\Users\29137\zhongyao_model.h5'  # 改成你的模型路径
CLASS_NAMES = ['百合', '党参', '枸杞', '槐花', '金银花']  # 按你的实际顺序

# ================== 加载模型 ==================
print(f"正在加载模型: {MODEL_PATH}")
model = tf.keras.models.load_model(MODEL_PATH)
print("模型加载成功！")

# ================== 核心预测函数（支持文件流） ==================
def predict_image(image_input):
    """
    统一预测函数，支持两种输入：
    1. 本地图片路径（字符串）
    2. PIL Image 对象 / 二进制文件流（Flask接口用）
    输出: 字典 {'label': '中药名', 'confidence': 置信度(float)}
    """
    # --- 处理输入，统一转为 PIL Image 对象 ---
    if isinstance(image_input, str):
        # 情况1：输入是本地路径
        img = load_img(image_input, target_size=(224, 224))
    else:
        # 情况2：输入是文件流 / PIL Image（给Flask接口用）
        if isinstance(image_input, bytes):
            img = Image.open(io.BytesIO(image_input)).convert("RGB")
        else:
            img = image_input.convert("RGB")
        img = img.resize((224, 224))

    # --- 预处理（保持你原来的VGG16方式不变） ---
    img_array = img_to_array(img)
    img_array = tf.keras.applications.vgg16.preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    # --- 预测 ---
    predictions = model.predict(img_array, verbose=0)[0]
    predicted_idx = np.argmax(predictions)
    confidence = float(predictions[predicted_idx])

    return {
        'label': CLASS_NAMES[predicted_idx],
        'confidence': confidence
    }

# ================== 命令行测试入口（保留你原来的用法） ==================
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        result = predict_image(sys.argv[1])
        print(f"识别结果: {result['label']}")
        print(f"置信度: {result['confidence']:.4f}")
    else:
        print("用法: python predict_service.py 图片路径")
