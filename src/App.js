import { useState } from 'react';
import './App.css';

// 药材百科信息
const HERB_INFO = {
  "百合": {
    "功效": "养阴润肺，清心安神",
    "用法": "煎服，6-12g；也可煮粥、煲汤",
    "注意事项": "风寒咳嗽、中寒便溏者忌服"
  },
  "党参": {
    "功效": "健脾益肺，养血生津",
    "用法": "煎服，9-30g",
    "注意事项": "不宜与藜芦同用"
  },
  "枸杞": {
    "功效": "滋补肝肾，益精明目",
    "用法": "煎服，6-12g；也可泡水、嚼服",
    "注意事项": "脾虚便溏者慎服"
  },
  "槐花": {
    "功效": "凉血止血，清肝泻火",
    "用法": "煎服，5-10g",
    "注意事项": "脾胃虚寒及阴虚发热而无实火者慎用"
  },
  "金银花": {
    "功效": "清热解毒，凉血消肿",
    "用法": "煎服，6-15g",
    "注意事项": "脾胃虚寒及气虚疮疡脓清者忌用"
  }
};

// 置信度颜色类
function getConfidenceClass(confidence) {
  if (confidence >= 0.9) return 'confidence-high';
  if (confidence >= 0.8) return 'confidence-medium';
  return 'confidence-low';
}

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setSelectedImage(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
  };

  const handleUpload = async () => {
    if (!selectedImage) {
      alert('请先选择一张图片');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      if (data.error) {
        alert(`识别失败：${data.error}`);
      } else {
        setResult(data);
      }
    } catch (error) {
      alert('请求失败，请检查后端服务是否正常运行');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>🌿 中药识别系统</h1>

      <div className="upload-area">
        <input 
          type="file" 
          accept="image/*" 
          onChange={handleImageChange} 
          id="file-input"
        />
        <label htmlFor="file-input" className="upload-btn">选择图片上传</label>

        {previewUrl && (
          <div className="preview">
            <img src={previewUrl} alt="预览图片" />
          </div>
        )}

        <button className="start-btn" onClick={handleUpload} disabled={loading}>
          {loading ? (
            <span className="loading-text">
              <span className="spinner"></span> 识别中...
            </span>
          ) : '开始识别'}
        </button>
      </div>

      {result && (
        <div className={`result ${getConfidenceClass(result.confidence)}`}>
          <h2>识别结果</h2>
          <p>药材名称：{result.breed}</p>
          <p>英文名称：{result.breed_english}</p>
          <p>置信度：{(result.confidence * 100).toFixed(2)}%</p>

          {HERB_INFO[result.breed] && (
            <div className="herb-info">
              <h3>药材百科</h3>
              <p>功效：{HERB_INFO[result.breed].功效}</p>
              <p>用法：{HERB_INFO[result.breed].用法}</p>
              <p>注意事项：{HERB_INFO[result.breed].注意事项}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
