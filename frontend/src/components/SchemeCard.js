import React, { useState } from 'react';
import {
  Award,
  Calendar,
  FileText,
  CheckCircle,
  ExternalLink,
  ChevronDown,
  ChevronUp,
  MapPin,
  Tag,
  Phone,
  Mail,
  Globe
} from 'lucide-react';

const SchemeCard = ({ scheme }) => {
  const [showDetails, setShowDetails] = useState(false);

  if (!scheme) return null;

  const {
    name,
    short_name,
    type,
    description,
    benefits,
    eligibility,
    documents_required,
    how_to_apply,
    application_deadline,
    contact,
    website,
    scheme_type,
    relevance,
    relevance_score,
    is_urgent,
    benefits_count
  } = scheme;

  const getTypeColor = () => {
    const colors = {
      'insurance': 'bg-blue-100 text-blue-800',
      'income_support': 'bg-green-100 text-green-800',
      'credit': 'bg-purple-100 text-purple-800',
      'subsidy': 'bg-orange-100 text-orange-800',
      'sustainable_farming': 'bg-emerald-100 text-emerald-800',
      'mechanization': 'bg-indigo-100 text-indigo-800',
      'crop_specific': 'bg-pink-100 text-pink-800',
      'emergency': 'bg-red-100 text-red-800',
      'comprehensive': 'bg-yellow-100 text-yellow-800'
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  const getTypeIcon = () => {
    const icons = {
      'insurance': '🛡️',
      'income_support': '💰',
      'credit': '💳',
      'subsidy': '🏷️',
      'sustainable_farming': '🌱',
      'mechanization': '🚜',
      'crop_specific': '🌾',
      'emergency': '🚨',
      'comprehensive': '📋'
    };
    return icons[type] || '📄';
  };

  const getRelevanceBadge = () => {
    if (is_urgent) {
      return {
        text: 'URGENT',
        color: 'bg-red-100 text-red-800'
      };
    }
    if (relevance_score >= 90) {
      return {
        text: 'HIGHLY RELEVANT',
        color: 'bg-green-100 text-green-800'
      };
    }
    if (relevance_score >= 70) {
      return {
        text: 'RELEVANT',
        color: 'bg-blue-100 text-blue-800'
      };
    }
    return null;
  };

  const relevanceBadge = getRelevanceBadge();

  return (
    <div className={`bg-white rounded-xl shadow-lg overflow-hidden border ${
      is_urgent ? 'border-red-300' : 'border-gray-200'
    } hover:shadow-xl transition-shadow duration-200`}>
      
      {/* Header */}
      <div className={`p-6 ${
        scheme_type === 'central' ? 'bg-gradient-to-r from-blue-50 to-indigo-50' :
        scheme_type === 'state' ? 'bg-gradient-to-r from-green-50 to-emerald-50' :
        scheme_type === 'crop_specific' ? 'bg-gradient-to-r from-orange-50 to-amber-50' :
        'bg-gray-50'
      }`}>
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-3">
            <div className="text-3xl">{getTypeIcon()}</div>
            <div>
              <h3 className="text-lg font-bold text-gray-900">
                {name}
                {short_name && <span className="ml-2 text-sm font-normal text-gray-500">({short_name})</span>}
              </h3>
              
              <div className="flex flex-wrap items-center gap-2 mt-2">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getTypeColor()}`}>
                  <Tag className="h-3 w-3 mr-1" />
                  {type?.replace('_', ' ').toUpperCase()}
                </span>
                
                {scheme_type && (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                    {scheme_type === 'central' ? '🇮🇳 CENTRAL' :
                     scheme_type === 'state' ? '🏛️ STATE' :
                     scheme_type === 'crop_specific' ? '🌾 CROP' : '📋 SCHEME'}
                  </span>
                )}
                
                {relevanceBadge && (
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${relevanceBadge.color}`}>
                    <Award className="h-3 w-3 mr-1" />
                    {relevanceBadge.text}
                  </span>
                )}
              </div>
            </div>
          </div>
          
          {relevance_score && (
            <div className="text-right">
              <div className="text-sm text-gray-500">Relevance</div>
              <div className="text-2xl font-bold text-green-600">{relevance_score}%</div>
            </div>
          )}
        </div>
      </div>

      {/* Description */}
      <div className="p-6 border-b">
        <p className="text-gray-700">{description}</p>
        {relevance && (
          <p className="mt-2 text-sm text-green-600 font-medium">{relevance}</p>
        )}
      </div>

      {/* Key Benefits */}
      {benefits && benefits.length > 0 && (
        <div className="p-6 border-b">
          <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
            <Award className="h-5 w-5 text-yellow-500 mr-2" />
            Key Benefits {benefits_count && `(${benefits_count})`}
          </h4>
          <ul className="space-y-2">
            {benefits.slice(0, showDetails ? benefits.length : 3).map((benefit, index) => (
              <li key={index} className="flex items-start space-x-2">
                <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
                <span className="text-gray-700">{benefit}</span>
              </li>
            ))}
          </ul>
          {benefits.length > 3 && (
            <button
              onClick={() => setShowDetails(!showDetails)}
              className="mt-2 text-sm text-green-600 hover:text-green-700 font-medium flex items-center"
            >
              {showDetails ? 'Show less' : `Show ${benefits.length - 3} more benefits`}
              {showDetails ? <ChevronUp className="h-4 w-4 ml-1" /> : <ChevronDown className="h-4 w-4 ml-1" />}
            </button>
          )}
        </div>
      )}

      {/* Eligibility */}
      {eligibility && eligibility.length > 0 && (
        <div className="p-6 border-b">
          <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
            <CheckCircle className="h-5 w-5 text-blue-500 mr-2" />
            Eligibility Criteria
          </h4>
          <ul className="space-y-1">
            {eligibility.map((item, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span className="text-gray-700">{item}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Documents Required */}
      {documents_required && documents_required.length > 0 && (
        <div className="p-6 border-b">
          <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
            <FileText className="h-5 w-5 text-orange-500 mr-2" />
            Documents Required
          </h4>
          <ul className="space-y-1">
            {documents_required.map((doc, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-orange-500 mt-1">•</span>
                <span className="text-gray-700">{doc}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* How to Apply */}
      {how_to_apply && (
        <div className="p-6 border-b">
          <h4 className="font-semibold text-gray-900 mb-2">How to Apply</h4>
          <p className="text-gray-700">{how_to_apply}</p>
        </div>
      )}

      {/* Deadline */}
      {application_deadline && (
        <div className="p-6 border-b">
          <div className="flex items-center text-orange-600">
            <Calendar className="h-5 w-5 mr-2" />
            <span className="font-medium">Deadline: {application_deadline}</span>
          </div>
        </div>
      )}

      {/* Contact Information */}
      {(contact || phone || email || website) && (
        <div className="p-6 bg-gray-50">
          <h4 className="font-semibold text-gray-900 mb-3">Contact Information</h4>
          <div className="space-y-2">
            {contact && (
              <div className="flex items-center text-gray-700">
                <Phone className="h-4 w-4 mr-2 text-gray-500" />
                {contact}
              </div>
            )}
            {phone && (
              <div className="flex items-center text-gray-700">
                <Phone className="h-4 w-4 mr-2 text-gray-500" />
                {phone}
              </div>
            )}
            {email && (
              <div className="flex items-center text-gray-700">
                <Mail className="h-4 w-4 mr-2 text-gray-500" />
                {email}
              </div>
            )}
            {website && (
              <div className="flex items-center text-blue-600 hover:text-blue-800">
                <Globe className="h-4 w-4 mr-2" />
                <a href={`https://${website}`} target="_blank" rel="noopener noreferrer" className="hover:underline">
                  {website}
                  <ExternalLink className="h-3 w-3 ml-1 inline" />
                </a>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="p-6 bg-gray-50 border-t flex justify-end space-x-3">
        <button
          onClick={() => {
            // Save scheme functionality
          }}
          className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-100"
        >
          Save for Later
        </button>
        <button
          onClick={() => {
            window.open(`https://${website || 'pmkisan.gov.in'}`, '_blank');
          }}
          className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700"
        >
          Apply Now
          <ExternalLink className="h-4 w-4 ml-1 inline" />
        </button>
      </div>
    </div>
  );
};

export default SchemeCard;