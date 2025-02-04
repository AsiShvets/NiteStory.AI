import React, { useState } from "react";
import { Card, CardContent } from "./components/ui/card";
import { Button } from "./components/ui/button";
import { Select, SelectTrigger, SelectContent, SelectItem } from "./components/ui/select";

export default function App() {
  const [modelChoice, setModelChoice] = useState("OpenAI (GPT-3.5)");
  const [uploadedImage, setUploadedImage] = useState(null);
  const [scenario, setScenario] = useState("");
  const [story, setStory] = useState("");
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);


  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setUploadedImage(file);
    }
  };
  const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
  console.log("API_BASE_URL:", process.env.REACT_APP_API_URL);


  const processImage = async () => {
    if (!uploadedImage) {
      alert("Please upload an image.");
      return;
    }
  
    setLoading(true);
    setScenario("");
    setStory("");
    setAudioUrl(null);
  
    try {
      // Convert image to FormData
      const formData = new FormData();
      formData.append("image", uploadedImage);
  
      console.log("Uploading image...");
  
      // Image to text request
      const imageResponse = await fetch(`${API_BASE_URL}/api/image-to-text`, { 
        method: "POST",
        body: formData
      });
  
      if (!imageResponse.ok) {
        const errorText = await imageResponse.text();
        console.error("Image-to-text API Error:", errorText);
        throw new Error(`Image processing failed: ${errorText}`);
      }
  
      const imageData = await imageResponse.json();
      console.log("Image-to-text response:", imageData);
      setScenario(imageData.text);
  
      // Generate story
      const storyResponse = await fetch(`${API_BASE_URL}/api/story-generator`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenario: imageData.text, modelChoice }),
      });
  
      if (!storyResponse.ok) {
        const errorText = await storyResponse.text();
        console.error("Story API Error:", errorText);
        throw new Error(`Story generation failed: ${errorText}`);
      }
  
      const storyData = await storyResponse.json();
      console.log("Story response:", storyData);
      setStory(storyData.story);
  
      // Generate speech
      const audioResponse = await fetch(`${API_BASE_URL}/api/text-to-speech`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: storyData.story }),
      });
  
      if (!audioResponse.ok) {
        const errorText = await audioResponse.text();
        console.error("Text-to-speech API Error:", errorText);
        throw new Error(`Audio generation failed: ${errorText}`);
      }
  
      const audioBlob = await audioResponse.blob();
      setAudioUrl(URL.createObjectURL(audioBlob));
  
    } catch (error) {
      console.error("Error:", error);
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">AI Story Teller</h1>

      <Card className="mb-4">
        <CardContent>
          <h2 className="text-lg font-semibold mb-2">Choose your language model:</h2>
          <Select onValueChange={(value) => setModelChoice(value)} defaultValue={modelChoice}>
            <SelectTrigger>
              <Button>{modelChoice}</Button>
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="OpenAI (GPT-3.5)">OpenAI (GPT-3.5)</SelectItem>
              <SelectItem value="Hugging Face (Alternative)">Hugging Face (Alternative)</SelectItem>
            </SelectContent>
          </Select>
        </CardContent>
      </Card>

      <Card className="mb-4">
        <CardContent>
          <h2 className="text-lg font-semibold mb-2">Upload an Image</h2>
          <input type="file" accept="image/*" onChange={handleImageUpload} className="mb-4" />
          {uploadedImage && <img src={URL.createObjectURL(uploadedImage)} alt="Uploaded" className="w-full h-auto mb-4" />}
          <Button onClick={processImage} disabled={loading}>
            {loading ? "Processing..." : "Generate Story"}
          </Button>
        </CardContent>
      </Card>

      {scenario && (
        <Card className="mb-4">
          <CardContent>
            <h2 className="text-lg font-semibold mb-2">Scenario</h2>
            <p>{scenario}</p>
          </CardContent>
        </Card>
      )}

      {story && (
        <Card className="mb-4">
          <CardContent>
            <h2 className="text-lg font-semibold mb-2">Story</h2>
            <p>{story}</p>
          </CardContent>
        </Card>
      )}

      {audioUrl && (
        <Card>
          <CardContent>
            <h2 className="text-lg font-semibold mb-2">Audio</h2>
            <audio controls src={audioUrl} />
          </CardContent>
        </Card>
      )}
    </div>
  );
}
