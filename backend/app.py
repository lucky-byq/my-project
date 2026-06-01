from flask import Flask, request, jsonify
from flask_cors import CORS
from predict_service import predict_image  # 直接调用你写好的预测函数
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # 允许跨域请求，方便前后端联调

# 关键配置（与训练模型一致，这里和predict_service.py保持同步）
CLASS_NAMES = ["百合", "党参", "枸杞", "槐花", "金银花"]
CLASS_NAMES_EN = ["Lily", "Dangshen", "Goji Berry", "Sophora Flower", "Honeysuckle"]

# -------------------------- 核心识别接口 /predict --------------------------
@app.route("/predict", methods=["POST"])
def predict():
    # 1. 接收前端上传的图片文件
    if "file" not in request.files:
        return jsonify({"error": "未上传图片文件"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "请选择图片后上传"}), 400
    
    # 2. 验证图片格式
    allowed_extensions = {"jpg", "jpeg", "png"}
    if not file.filename.lower().endswith(tuple(allowed_extensions)):
        return jsonify({"error": "仅支持JPG、PNG格式图片"}), 400

    try:
        # 3. 读取图片并调用predict_service中的预测函数
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        result = predict_image(img)

        # 4. 解析预测结果，保持和你原来的字段名一致
        predicted_idx = CLASS_NAMES.index(result["label"])
        breed = CLASS_NAMES[predicted_idx]
        breed_english = CLASS_NAMES_EN[predicted_idx]
        confidence = result["confidence"]

        # 5. 返回结果给前端
        return jsonify({
            "breed": breed,
            "breed_english": breed_english,
            "confidence": confidence
        })

    except Exception as e:
        return jsonify({"error": f"图片处理失败：{str(e)}"}), 500


# -------------------------- 启动后端服务 --------------------------
if __name__ == "__main__":
    # 端口号固定为8000，和你原来的配置一致
    app.run(host="0.0.0.0", port=port, debug=False)
