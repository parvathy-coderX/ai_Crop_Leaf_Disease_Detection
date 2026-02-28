import React, { useState } from 'react';
import { 
  CheckCircle, 
  AlertTriangle, 
  XCircle, 
  Info, 
  ChevronDown, 
  ChevronUp,
  Leaf,
  Flask,
  Pill
} from 'lucide-react';

const ResultCard = ({ result }) => {
  const [showDetails, setShowDetails] = useState(false);
  const [showTreatment, setShowTreatment] = useState(false);

  if (!result) return null;

  const {
    primary_disease,
    confidence,
    confidence_level,
    severity,
    predictions,
    disease_details,
    treatment,
    image_path,
    timestamp
  } = result;

  // Determine color based on disease and confidence
  const getStatusColor = () => {
    if (primary_disease === 'Healthy') return 'green';
    if (confidence > 80) return 'red';
    if (confidence > 60) return 'orange';
    return 'yellow';
  };

  const statusColor = getStatusColor();
  
  const getStatusIcon = () => {
    if (primary_disease === 'Healthy') {
      return <CheckCircle className="h-12 w-12 text-green-500" />;
    }
    if (confidence > 70) {
      return <XCircle className="h-12 w-12 text-red-500" />;
    }
    return <AlertTriangle className="h-12 w-12 text-yellow-500" />;
  };

  const getConfidenceColor = () => {
    if (confidence > 80) return 'text-red-600';
    if (confidence > 60) return 'text-orange-600';
    return 'text-yellow-600';
  };

  const getSeverityBadge = () => {
    const colors = {
      'CRITICAL': 'bg-red-100 text-red-800',
      'HIGH': 'bg-orange-100 text-orange-800',
      'MEDIUM': 'bg-yellow-100 text-yellow-800',
      'LOW': 'bg-blue-100 text-blue-800',
      'UNCERTAIN': 'bg-gray-100 text-gray-800'
    };
    return colors[severity] || 'bg-gray-100 text-gray-800';
  };

  const formatDate = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
      {/* Header */}
      <div className={`p-6 border-b ${
        statusColor === 'green' ? 'bg-green-50' :
        statusColor === 'red' ? 'bg-red-50' :
        statusColor === 'orange' ? 'bg-orange-50' :
        'bg-yellow-50'
      }`}>
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-4">
            {getStatusIcon()}
            <div>
              <h3 className="text-2xl font-bold text-gray-900">
                {primary_disease}
              </h3>
              <div className="flex items-center space-x-2 mt-2">
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getSeverityBadge()}`}>
                  {severity} SEVERITY
                </span>
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getConfidenceColor()} bg-white`}>
                  {confidence}% Confidence
                </span>
              </div>
            </div>
          </div>
          {image_path && (
            <img 
              src={`/static/uploads/${image_path}`} 
              alt="Uploaded crop"
              className="h-20 w-20 rounded-lg object-cover border-2 border-white shadow"
            />
          )}
        </div>
      </div>

      {/* Quick Info */}
      <div className="grid grid-cols-3 gap-4 p-6 bg-gray-50 border-b">
        <div className="text-center">
          <div className="text-sm text-gray-500">Disease Type</div>
          <div className="font-semibold text-gray-900">
            {disease_details?.type || 'Unknown'}
          </div>
        </div>
        <div className="text-center">
          <div className="text-sm text-gray-500">Scientific Name</div>
          <div className="font-semibold text-gray-900">
            {disease_details?.scientific_name || '-'}
          </div>
        </div>
        <div className="text-center">
          <div className="text-sm text-gray-500">Yield Loss</div>
          <div className="font-semibold text-gray-900">
            {disease_details?.yield_loss || 'Variable'}
          </div>
        </div>
      </div>

      {/* Description */}
      <div className="p-6 border-b">
        <p className="text-gray-700">
          {disease_details?.description || 'No description available.'}
        </p>
      </div>

      {/* Symptoms */}
      {disease_details?.symptoms && disease_details.symptoms.length > 0 && (
        <div className="p-6 border-b">
          <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
            <AlertTriangle className="h-5 w-5 text-red-500 mr-2" />
            Symptoms to Look For
          </h4>
          <ul className="space-y-2">
            {disease_details.symptoms.map((symptom, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-red-500 mt-1">•</span>
                <span className="text-gray-700">{symptom}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Causes */}
      {disease_details?.causes && disease_details.causes.length > 0 && (
        <div className="p-6 border-b">
          <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
            <Info className="h-5 w-5 text-blue-500 mr-2" />
            Common Causes
          </h4>
          <ul className="space-y-2">
            {disease_details.causes.map((cause, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span className="text-gray-700">{cause}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Treatment Section */}
      {treatment && (
        <div className="p-6 border-b">
          <button
            onClick={() => setShowTreatment(!showTreatment)}
            className="w-full flex items-center justify-between text-left"
          >
            <h4 className="font-semibold text-gray-900 flex items-center">
              <Pill className="h-5 w-5 text-green-500 mr-2" />
              Treatment Recommendations
            </h4>
            {showTreatment ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
          </button>
          
          {showTreatment && (
            <div className="mt-4 space-y-4">
              {/* Chemical Treatment */}
              {treatment.chemical && (
                <div>
                  <h5 className="font-medium text-gray-800 mb-2">Chemical Control:</h5>
                  <ul className="space-y-1">
                    {treatment.chemical.map((item, idx) => (
                      <li key={idx} className="text-sm text-gray-600 flex items-start">
                        <span className="text-green-600 mr-2">•</span>
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Organic Treatment */}
              {treatment.organic && (
                <div>
                  <h5 className="font-medium text-gray-800 mb-2">Organic/Biological Control:</h5>
                  <ul className="space-y-1">
                    {treatment.organic.map((item, idx) => (
                      <li key={idx} className="text-sm text-gray-600 flex items-start">
                        <span className="text-green-600 mr-2">•</span>
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Prevention */}
      {disease_details?.prevention && disease_details.prevention.length > 0 && (
        <div className="p-6 border-b">
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="w-full flex items-center justify-between text-left"
          >
            <h4 className="font-semibold text-gray-900 flex items-center">
              <Leaf className="h-5 w-5 text-green-500 mr-2" />
              Prevention Measures
            </h4>
            {showDetails ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
          </button>
          
          {showDetails && (
            <ul className="mt-4 space-y-2">
              {disease_details.prevention.map((item, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <span className="text-green-500 mt-1">•</span>
                  <span className="text-gray-700">{item}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* Alternative Predictions */}
      {predictions && predictions.length > 1 && (
        <div className="p-6 bg-gray-50">
          <h4 className="font-semibold text-gray-900 mb-3">Other Possible Diseases</h4>
          <div className="space-y-2">
            {predictions.slice(1).map((pred, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-gray-700">{pred.disease}</span>
                <span className="text-sm font-medium text-gray-600">
                  {pred.confidence_percentage}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Timestamp */}
      {timestamp && (
        <div className="px-6 py-3 text-xs text-gray-400 border-t">
          Analyzed on: {formatDate(timestamp)}
        </div>
      )}

      {/* Action Buttons */}
      <div className="p-6 bg-gray-50 border-t flex justify-end space-x-3">
        <button
          onClick={() => window.print()}
          className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-100"
        >
          Download Report
        </button>
        <button
          onClick={() => {
            // Share functionality
            if (navigator.share) {
              navigator.share({
                title: 'Crop Disease Analysis',
                text: `Detected: ${primary_disease} with ${confidence}% confidence`,
                url: window.location.href
              });
            }
          }}
          className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700"
        >
          Share Results
        </button>
      </div>
    </div>
  );
};

export default ResultCard;