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

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => setUploadedImage(reader.result);
      reader.readAsDataURL(file);
    }
  };

  const processImage = async () => {
    if (!uploadedImage) {
      alert("Please upload an image.");
      return;
    }

    try {
      const response = await fetch("/api/image-to-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: uploadedImage })
      });

      const data = await response.json();
      setScenario(data.text);

      const storyResponse = await fetch("/api/story-generator", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scenario: data.text, modelChoice })
      });

      const storyData = await storyResponse.json();
      setStory(storyData.story);

      const audioResponse = await fetch("/api/text-to-speech", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: storyData.story })
      });

      const audioBlob = await audioResponse.blob();
      setAudioUrl(URL.createObjectURL(audioBlob));
    } catch (error) {
      console.error("Error processing image:", error);
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
          {uploadedImage && <img src={uploadedImage} alt="Uploaded" className="w-full h-auto mb-4" />}
          <Button onClick={processImage}>Generate Story</Button>
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
