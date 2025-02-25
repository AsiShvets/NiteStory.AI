import React, { useState, useRef } from 'react';

const App = () => {
  const apiBaseUrl = 'http://127.0.0.1:8000/api';

  // State for "Generate Story from Image" workflow
  const [chainImageFile, setChainImageFile] = useState(null);
  const [chainPdfFile, setChainPdfFile] = useState(null); // Optional PDF file
  const [chainModelChoice, setChainModelChoice] = useState('OpenAI (GPT-3.5)');
  const [chainCaption, setChainCaption] = useState('');
  const [chainStory, setChainStory] = useState('');
  const [chainUploadedImage, setChainUploadedImage] = useState(''); // Base64 image data
  const [isLoading, setIsLoading] = useState(false);

  // State for file previews
  const [imagePreview, setImagePreview] = useState(null);
  const [pdfPreview, setPdfPreview] = useState(null);

  // Refs for file inputs
  const imageInputRef = useRef(null);
  const pdfInputRef = useRef(null);

  // Handler for generating story from image (with optional PDF)
  const handleChainSubmit = async (e) => {
    e.preventDefault();
    if (!chainImageFile) {
      alert('Please select an image file.');
      return;
    }
    const formData = new FormData();
    formData.append('image', chainImageFile);
    formData.append('model_choice', chainModelChoice);
    if (chainPdfFile) {
      formData.append('pdf', chainPdfFile);
    }
    setIsLoading(true);

    try {
      const response = await fetch(`${apiBaseUrl}/generate-story-from-image`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setChainCaption(data.caption);
      setChainStory(data.story);
      setChainUploadedImage(data.image);
    } catch (error) {
      console.error("Error generating story from image:", error);
    }
    setIsLoading(false);
  };

  // File change handlers with preview generation
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setChainImageFile(file);
    if (file) {
      setImagePreview(URL.createObjectURL(file));
    } else {
      setImagePreview(null);
    }
  };

  const handlePdfChange = (e) => {
    const file = e.target.files[0];
    setChainPdfFile(file);
    if (file) {
      setPdfPreview(URL.createObjectURL(file));
    } else {
      setPdfPreview(null);
    }
  };

  // Handlers to delete the selected files and clear previews
  const handleImageDelete = () => {
    setChainImageFile(null);
    setImagePreview(null);
    if (imageInputRef.current) {
      imageInputRef.current.value = '';
    }
  };

  const handlePdfDelete = () => {
    setChainPdfFile(null);
    setPdfPreview(null);
    if (pdfInputRef.current) {
      pdfInputRef.current.value = '';
    }
  };

  // Inline styling with a playful, kid-friendly theme
  const containerStyle = {
    maxWidth: '600px',
    margin: '20px auto',
    padding: '20px',
    background: '#f0f8ff', // Alice Blue
    borderRadius: '12px',
    fontFamily: '"Comic Sans MS", cursive, sans-serif',
    boxShadow: '0 0 10px rgba(0,0,0,0.1)'
  };
  const sectionStyle = {
    marginBottom: '40px',
    padding: '20px',
    background: '#fffacd', // LemonChiffon
    border: '2px dashed #ffb6c1', // LightPink dashed border
    borderRadius: '12px'
  };
  const resultStyle = {
    marginTop: '20px',
    padding: '15px',
    backgroundColor: '#e6ffe6', // light green background
    border: '1px solid #b3ffb3',
    borderRadius: '8px',
    whiteSpace: 'pre-wrap'
  };
  const previewStyle = {
    marginTop: '10px',
    maxWidth: '100%',
    borderRadius: '12px',
    border: '2px solid #ffb6c1'
  };
  const crossButtonStyle = {
    position: 'absolute',
    top: '5px',
    right: '5px',
    background: 'rgba(255,105,97,0.8)', // soft coral/red
    border: 'none',
    borderRadius: '50%',
    cursor: 'pointer',
    fontSize: '16px',
    color: 'white',
    width: '24px',
    height: '24px',
    textAlign: 'center',
    lineHeight: '22px'
  };
  const buttonStyle = {
    background: '#ffb6c1',
    color: 'white',
    border: 'none',
    borderRadius: '12px',
    padding: '10px 15px',
    cursor: 'pointer',
    marginTop: '16px',
    boxShadow: '0 2px 5px rgba(0,0,0,0.2)'
  };
  const inputStyle = {
    marginTop: '8px',
    padding: '6px',
    borderRadius: '6px',
    border: '1px solid #ccc'
  };

  return (
    <div style={containerStyle}>
      <h1 style={{ textAlign: 'center', color: '#ff6347' }}>AI Story Teller for Children - NiteStory.AI</h1>

      {/* Generate Story from Image Section */}
      <section style={sectionStyle}>
        <h2 style={{ color: '#ff6347' }}>Generate Story from Image and PDF</h2>
        <form onSubmit={handleChainSubmit}>
          <div>
            <label>Upload Image:</label>
            <br />
            <input 
              type="file" 
              accept="image/*" 
              ref={imageInputRef}
              onChange={handleImageChange}
              style={inputStyle}
            />
          </div>
          {/* Image Preview with Small Cross */}
          {imagePreview && (
            <div style={{ position: 'relative', display: 'inline-block', marginTop: '10px' }}>
              <img src={imagePreview} alt="Image Preview" style={previewStyle} />
              <button
                type="button"
                onClick={handleImageDelete}
                style={crossButtonStyle}
              >
                ×
              </button>
            </div>
          )}

          <div style={{ marginTop: '16px' }}>
            <label>Optional PDF for Story Enrichment:</label>
            <br />
            <input 
              type="file" 
              accept="application/pdf" 
              ref={pdfInputRef}
              onChange={handlePdfChange}
              style={inputStyle}
            />
          </div>
          {/* PDF Preview with Small Cross */}
          {pdfPreview && (
            <div style={{ position: 'relative', marginTop: '10px' }}>
              <embed 
                src={pdfPreview} 
                type="application/pdf" 
                width="100%" 
                height="400px" 
                style={{ border: '2px solid #ffb6c1', borderRadius: '12px' }}
              />
              <button
                type="button"
                onClick={handlePdfDelete}
                style={crossButtonStyle}
              >
                ×
              </button>
            </div>
          )}

          <div style={{ margin: '16px 0' }}>
            <label htmlFor="chainModelChoice">Model Choice:</label>
            <br />
            <select 
              id="chainModelChoice" 
              value={chainModelChoice}
              onChange={(e) => setChainModelChoice(e.target.value)}
              style={{ ...inputStyle, width: '100%' }}
            >
              <option value="OpenAI (GPT-3.5)">OpenAI (GPT-3.5)</option>
              <option value="Hugging Face (Alternative)">Hugging Face (Alternative)</option>
            </select>
          </div>
          <button type="submit" style={buttonStyle}>Generate Story</button>
        </form>

        {/* Progress Bar */}
        {isLoading && (
          <div style={{ marginTop: '20px', textAlign: 'center' }}>
            <progress style={{ width: '100%' }} />
            <p>Generating story, please wait...</p>
          </div>
        )}

        <div style={resultStyle}>
          <h3 style={{ color: '#ff6347' }}>Image Caption:</h3>
          <p>{chainCaption}</p>
          <h3 style={{ color: '#ff6347' }}>Story:</h3>
          <p>{chainStory}</p>
          {chainUploadedImage && (
            <div style={{ marginTop: '20px' }}>
              <h3 style={{ color: '#ff6347' }}>Uploaded Image:</h3>
              <img 
                src={chainUploadedImage} 
                alt="Uploaded" 
                style={{ maxWidth: '100%', border: '2px solid #ffb6c1', borderRadius: '12px' }} 
              />
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default App;
