import React, { useState } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 处理文件选择
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  // 处理识别
  const handlePredict = async () => {
    if (!selectedFile) {
      setError('请先选择图片');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || '识别失败');
      }
    } catch (err) {
      setError('网络错误，请确保后端服务已启动');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App" style={styles.container}>
      <h1 style={styles.title}>中药图像识别系统</h1>
      <p style={styles.subtitle}>上传中药图片，AI 自动识别种类</p>

      <div style={styles.uploadArea}>
        <input
          type="file"
          accept="image/jpeg,image/png,image/jpg"
          onChange={handleFileChange}
          style={styles.fileInput}
          id="fileInput"
        />
        <label htmlFor="fileInput" style={styles.uploadButton}>
          选择图片
        </label>

        {preview && (
          <div style={styles.previewContainer}>
            <img src={preview} alt="预览" style={styles.preview} />
          </div>
        )}

        <button
          onClick={handlePredict}
          disabled={!selectedFile || loading}
          style={{
            ...styles.predictButton,
            ...((!selectedFile || loading) ? styles.disabledButton : {})
          }}
        >
          {loading ? '识别中...' : '开始识别'}
        </button>

        {error && (
          <div style={styles.error}>
            ❌ {error}
          </div>
        )}

        {result && (
          <div style={styles.resultContainer}>
            <h2 style={styles.resultTitle}>识别结果</h2>
            <div style={styles.resultCard}>
              <p style={styles.herbName}>{result.breed}</p>
              <p style={styles.herbNameEn}>{result.breed_english}</p>
              <p style={styles.confidence}>
                置信度: {(result.confidence * 100).toFixed(2)}%
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    padding: '40px 20px',
  },
  title: {
    textAlign: 'center',
    color: 'white',
    fontSize: '2.5rem',
    marginBottom: '10px',
  },
  subtitle: {
    textAlign: 'center',
    color: 'rgba(255,255,255,0.9)',
    fontSize: '1.1rem',
    marginBottom: '40px',
  },
  uploadArea: {
    maxWidth: '500px',
    margin: '0 auto',
    background: 'white',
    borderRadius: '20px',
    padding: '30px',
    boxShadow: '0 10px 40px rgba(0,0,0,0.2)',
    textAlign: 'center',
  },
  fileInput: {
    display: 'none',
  },
  uploadButton: {
    display: 'inline-block',
    padding: '12px 30px',
    background: '#667eea',
    color: 'white',
    borderRadius: '25px',
    cursor: 'pointer',
    fontSize: '1rem',
    border: 'none',
    marginBottom: '20px',
  },
  previewContainer: {
    margin: '20px 0',
  },
  preview: {
    maxWidth: '100%',
    maxHeight: '250px',
    borderRadius: '10px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  },
  predictButton: {
    background: '#48bb78',
    color: 'white',
    border: 'none',
    padding: '12px 30px',
    borderRadius: '25px',
    fontSize: '1rem',
    cursor: 'pointer',
    marginTop: '10px',
    transition: 'all 0.3s',
  },
  disabledButton: {
    background: '#a0aec0',
    cursor: 'not-allowed',
  },
  error: {
    marginTop: '20px',
    padding: '10px',
    background: '#fed7d7',
    color: '#c53030',
    borderRadius: '10px',
  },
  resultContainer: {
    marginTop: '30px',
  },
  resultTitle: {
    fontSize: '1.3rem',
    color: '#2d3748',
    marginBottom: '15px',
  },
  resultCard: {
    background: '#f7fafc',
    padding: '20px',
    borderRadius: '15px',
  },
  herbName: {
    fontSize: '2rem',
    fontWeight: 'bold',
    color: '#553c9a',
    margin: '0 0 5px 0',
  },
  herbNameEn: {
    fontSize: '1rem',
    color: '#718096',
    margin: '0 0 15px 0',
  },
  confidence: {
    fontSize: '1.1rem',
    color: '#48bb78',
    fontWeight: 'bold',
    margin: 0,
  },
};

export default App;