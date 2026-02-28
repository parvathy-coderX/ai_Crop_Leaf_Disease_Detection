import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Camera, Upload, X, Image as ImageIcon, AlertCircle, Loader, CheckCircle } from 'lucide-react';
import { uploadImage } from '../services/api';
import ResultCard from './ResultCard';

const ImageUpload = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  // Handle file drop
  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    setError(null);
    setResult(null);
    setUploadProgress(0);

    // Handle rejected files
    if (rejectedFiles && rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0];
      if (rejection.errors[0].code === 'file-too-large') {
        setError('File is too large. Maximum size is 10MB.');
      } else if (rejection.errors[0].code === 'file-invalid-type') {
        setError('Invalid file type. Please upload JPG, PNG, or JPEG.');
      } else {
        setError('Invalid file. Please try again.');
      }
      return;
    }

    // Handle accepted files
    if (acceptedFiles && acceptedFiles.length > 0) {
      const selectedFile = acceptedFiles[0];
      setFile(selectedFile);
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(selectedFile);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp']
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    maxFiles: 1,
    noClick: true,
    noKeyboard: true
  });

  const handleUpload = async () => {
    if (!file) {
      setError('Please select an image first');
      return;
    }

    setUploading(true);
    setError(null);
    setResult(null);
    setUploadProgress(10);

    try {
      // Create form data
      const formData = new FormData();
      formData.append('image', file);
      
      // Add optional metadata
      const userId = localStorage.getItem('userId');
      if (userId) {
        formData.append('user_id', userId);
      }
      
      // You can add location and crop type if available
      // formData.append('location', 'Kerala');
      // formData.append('crop_type', 'tomato');

      setUploadProgress(30);

      // Call API
      console.log('Uploading image...', file.name);
      const response = await uploadImage(formData);
      
      setUploadProgress(100);

      if (response.success) {
        setResult(response);
        console.log('Upload successful:', response);
      } else {
        setError(response.error || 'Prediction failed');
      }
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.message || 'Failed to upload image. Please try again.');
    } finally {
      setUploading(false);
      setTimeout(() => setUploadProgress(0), 1000);
    }
  };

  const resetUpload = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
    setUploadProgress(0);
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Crop Disease Detection</h1>
        <p className="text-gray-600">
          Upload a photo of your crop leaf to detect diseases and get treatment recommendations
        </p>
      </div>

      {/* Upload Area */}
      {!result ? (
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          {/* Drop Zone */}
          <div
            {...getRootProps()}
            className={`relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200 ${
              isDragActive
                ? 'border-green-500 bg-green-50'
                : 'border-gray-300 hover:border-green-400 hover:bg-gray-50'
            } ${file ? 'bg-gray-50' : ''}`}
            onClick={open}
          >
            <input {...getInputProps()} />
            
            {!file ? (
              <div className="flex flex-col items-center space-y-4">
                <div className={`p-4 rounded-full transition-colors duration-200 ${
                  isDragActive ? 'bg-green-100' : 'bg-gray-100'
                }`}>
                  <Upload className={`h-12 w-12 transition-colors duration-200 ${
                    isDragActive ? 'text-green-600' : 'text-gray-500'
                  }`} />
                </div>
                
                <div>
                  <p className="text-lg font-medium text-gray-700">
                    {isDragActive
                      ? 'Drop your image here'
                      : 'Drag & drop your crop image here'}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">
                    or <span className="text-green-600 font-medium">click to browse</span>
                  </p>
                </div>

                <div className="flex items-center space-x-2 text-xs text-gray-400">
                  <ImageIcon className="h-4 w-4" />
                  <span>Supports: JPG, PNG, JPEG (Max: 10MB)</span>
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center space-x-2 text-green-600">
                <CheckCircle className="h-5 w-5" />
                <span className="font-medium">{file.name} selected</span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    resetUpload();
                  }}
                  className="ml-2 text-red-500 hover:text-red-600"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            )}
          </div>

          {/* Preview Area */}
          {preview && (
            <div className="mt-6">
              <div className="relative rounded-lg overflow-hidden border border-gray-200">
                <img
                  src={preview}
                  alt="Preview"
                  className="w-full h-auto max-h-96 object-contain bg-gray-100"
                />
                
                {/* Upload Progress Bar */}
                {uploading && (
                  <div className="absolute bottom-0 left-0 right-0 h-1 bg-gray-200">
                    <div 
                      className="h-full bg-green-500 transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    />
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              <div className="mt-4 flex justify-end space-x-3">
                <button
                  onClick={resetUpload}
                  disabled={uploading}
                  className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Cancel
                </button>
                <button
                  onClick={handleUpload}
                  disabled={uploading}
                  className="flex items-center px-6 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {uploading ? (
                    <>
                      <Loader className="h-4 w-4 mr-2 animate-spin" />
                      Processing... {uploadProgress}%
                    </>
                  ) : (
                    <>
                      <Camera className="h-4 w-4 mr-2" />
                      Analyze Image
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mt-4 flex items-center space-x-2 text-red-500 bg-red-50 px-4 py-3 rounded-lg">
              <AlertCircle className="h-5 w-5 flex-shrink-0" />
              <span className="text-sm">{error}</span>
              <button onClick={() => setError(null)} className="ml-auto">
                <X className="h-4 w-4" />
              </button>
            </div>
          )}

          {/* Tips Section */}
          <div className="mt-6 bg-blue-50 rounded-lg p-4">
            <h4 className="text-sm font-semibold text-blue-800 mb-2 flex items-center">
              <Camera className="h-4 w-4 mr-2" />
              Tips for best results:
            </h4>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• Take photo in natural lighting</li>
              <li>• Focus on the affected area of the leaf</li>
              <li>• Include both healthy and diseased parts</li>
              <li>• Avoid blurry or dark images</li>
              <li>• Ensure the leaf is clean and dry</li>
            </ul>
          </div>
        </div>
      ) : (
        /* Results Section */
        <div className="space-y-6">
          <ResultCard result={result} />
          
          <div className="flex justify-center">
            <button
              onClick={resetUpload}
              className="px-6 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition-colors"
            >
              Analyze Another Image
            </button>
          </div>
        </div>
      )}

      {/* Sample Images (Optional) */}
      {!result && !file && (
        <div className="mt-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">Sample Images</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {['tomato', 'potato', 'pepper', 'healthy'].map((sample, index) => (
              <div
                key={index}
                className="relative cursor-pointer group"
                onClick={() => {
                  // You can add sample images here
                  console.log(`Load sample: ${sample}`);
                }}
              >
                <div className="aspect-w-1 aspect-h-1 rounded-lg overflow-hidden bg-gray-200">
                  <div className="w-full h-full bg-gradient-to-br from-green-200 to-green-300 flex items-center justify-center">
                    <Camera className="h-8 w-8 text-green-600 opacity-50" />
                  </div>
                </div>
                <p className="mt-2 text-sm text-center text-gray-600 capitalize">{sample}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;