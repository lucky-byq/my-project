import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# ========== 配置 ==========
MODEL_PATH = r'C:\Users\29137\zhongyao_model.h5'  # 改成你的模型路径
CLASS_NAMES = ['百合', '党参', '枸杞', '槐花', '金银花']  # 按你的实际顺序

# ========== 加载模型 ==========
print(f"正在加载模型: {MODEL_PATH}")
model = tf.keras.models.load_model(MODEL_PATH)
print("模型加载成功！")

# ========== 预测函数 ==========
def predict_image(image_path):
    """
    输入：图片路径（字符串）
    输出：字典 {'label': '中药名', 'confidence': 置信度(float)}
    """
    # 1. 加载图片并缩放到224x224
    img = load_img(image_path, target_size=(224, 224))
    
    # 2. 转成数组并做VGG16预处理
    img_array = img_to_array(img)
    img_array = tf.keras.applications.vgg16.preprocess_input(img_array)
    
    # 3. 增加批次维度
    img_array = np.expand_dims(img_array, axis=0)
    
    # 4. 预测
    predictions = model.predict(img_array, verbose=0)[0]
    predicted_idx = np.argmax(predictions)
    confidence = float(predictions[predicted_idx])
    
    return {
        'label': CLASS_NAMES[predicted_idx],
        'confidence': confidence
    }

# ========== 命令行测试入口 ==========
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        result = predict_image(sys.argv[1])
        print(f"识别结果: {result['label']}")
        print(f"置信度: {result['confidence']:.4f}")
    else:
        print("用法: python predict_service.py 图片路径.jpg")