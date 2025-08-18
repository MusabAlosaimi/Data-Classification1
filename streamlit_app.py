import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Shield, FileText, Globe, Building, Users, Leaf, Database } from 'lucide-react';

const DataClassificationApp = () => {
  const [selectedDataset, setSelectedDataset] = useState('');
  const [impactAssessment, setImpactAssessment] = useState({});
  const [showResults, setShowResults] = useState(false);

  // Example datasets
  const exampleDatasets = {
    'hr_employee': {
      name: 'HR Employee Content Dataset',
      description: 'Employee personal information, performance records, disciplinary actions',
      examples: ['Employee ID', 'Full Name', 'National ID', 'Home Address', 'Phone Number', 'Performance Reviews', 'Disciplinary Records', 'Training Records'],
      riskFactors: ['Personal identifiable information', 'Privacy concerns', 'Potential reputation damage']
    },
    'hr_payroll': {
      name: 'HR Payroll Dataset',
      description: 'Employee salary information, bank details, tax information',
      examples: ['Employee ID', 'Salary Amount', 'Bank Account Number', 'Tax Information', 'Benefits Details', 'Bonuses', 'Deductions'],
      riskFactors: ['Financial information', 'Privacy violations', 'Competitive intelligence']
    },
    'customer_data': {
      name: 'Customer Database',
      description: 'Customer contact information, purchase history, preferences',
      examples: ['Customer ID', 'Contact Details', 'Purchase History', 'Preferences', 'Support Tickets', 'Feedback'],
      riskFactors: ['Customer privacy', 'Business competitive advantage', 'GDPR compliance']
    },
    'financial_reports': {
      name: 'Financial Reports',
      description: 'Company financial statements, budget information, revenue data',
      examples: ['Revenue Data', 'Profit/Loss Statements', 'Budget Allocations', 'Cost Centers', 'Investment Information'],
      riskFactors: ['Market sensitive information', 'Competitive advantage', 'Investor relations']
    },
    'security_logs': {
      name: 'Security System Logs',
      description: 'Access logs, security incidents, system vulnerabilities',
      examples: ['Access Logs', 'Login Records', 'Security Incidents', 'Vulnerability Reports', 'System Configurations'],
      riskFactors: ['National security', 'Infrastructure protection', 'Operational security']
    },
    'research_data': {
      name: 'Research & Development Data',
      description: 'Product development, research findings, innovation plans',
      examples: ['Research Results', 'Product Specifications', 'Innovation Plans', 'Patent Applications', 'Test Results'],
      riskFactors: ['Competitive advantage', 'Intellectual property', 'Strategic planning']
    }
  };

  // Impact categories and questions
  const impactCategories = {
    'national_interest': {
      name: 'National Interest',
      icon: <Globe className="w-5 h-5" />,
      subcategories: {
        'reputation': {
          name: "Kingdom's Reputation",
          questions: [
            'Would this information be subject to national or international media interest?',
            'Would disclosure give a negative impression of the Kingdom?',
            'Could this affect diplomatic relationships with other countries?'
          ]
        },
        'diplomatic': {
          name: 'Diplomatic Relationships',
          questions: [
            'Would this information pose risk to relationships with friendly countries?',
            'Could it raise international tension?',
            'Could it lead to protests or sanctions from other countries?'
          ]
        },
        'security': {
          name: 'National Security/Public Order',
          questions: [
            'Would this information help with terrorist or serious crimes if released?',
            'Would it create public alarm?',
            'Could it compromise security or military operations?'
          ]
        },
        'economy': {
          name: 'National Economy',
          questions: [
            'Would disclosure cause economic losses at national level?',
            'Could it affect GDP, employment, or market rates?',
            'Would it impact multiple economic sectors?'
          ]
        },
        'infrastructure': {
          name: 'National Infrastructure',
          questions: [
            'Could this cause interruption to critical national infrastructure?',
            'Would it affect energy, transport, or health systems?',
            'Could it compromise cyber security of critical services?'
          ]
        },
        'government': {
          name: 'Government Functions',
          questions: [
            'Would this limit government entities ability to operate?',
            'Could it affect delivery of government services?',
            'Would it impact government decision-making processes?'
          ]
        }
      }
    },
    'entity_activities': {
      name: 'Entity Activities',
      icon: <Building className="w-5 h-5" />,
      subcategories: {
        'private_profits': {
          name: 'Profits of Private Entities',
          questions: [
            'Would disclosure lead to financial loss or bankruptcy?',
            'Could it enable fraud or illegal transfers of funds?',
            'Would it affect private entities operating public facilities?'
          ]
        },
        'private_functions': {
          name: 'Functions of Private Entities',
          questions: [
            'Would this cause damage to private entities operating public facilities?',
            'Could it lead to termination of significant employees?',
            'Would it affect competitiveness of private entities?'
          ]
        }
      }
    },
    'individuals': {
      name: 'Individuals',
      icon: <Users className="w-5 h-5" />,
      subcategories: {
        'health_safety': {
          name: 'Health/Safety of Individuals',
          questions: [
            'Would this lead to disclosure of names or locations of individuals?',
            'Could it expose undercover agents or people under protection?',
            'Would it cause physical harm or risk to individuals?'
          ]
        },
        'privacy': {
          name: 'Privacy',
          questions: [
            'Would this violate privacy of individuals?',
            'Would it infringe intellectual property rights?',
            'Could it expose personal identifiable information?'
          ]
        }
      }
    },
    'environment': {
      name: 'Environment',
      icon: <Leaf className="w-5 h-5" />,
      subcategories: {
        'resources': {
          name: 'Environmental Resources',
          questions: [
            'Could this information be used to develop services/products that destroy environmental resources?',
            'Would it cause long-term environmental damage?',
            'Could it affect natural resources of the country?'
          ]
        }
      }
    }
  };

  const classificationLevels = {
    'top_secret': {
      name: 'Top Secret',
      color: 'bg-red-100 border-red-500 text-red-800',
      impact: 'High',
      description: 'Exceptionally serious and irreparable effect on national interests, security, or safety',
      controls: [
        'Apply protective marking to all documents',
        'Restrict access to authorized personnel only',
        'Use only in specified secure locations',
        'Encrypt data using approved mechanisms',
        'No unattended storage permitted',
        'Secure disposal using electronic media disposal methods',
        'Maintain detailed access logs'
      ]
    },
    'secret': {
      name: 'Secret',
      color: 'bg-orange-100 border-orange-500 text-orange-800',
      impact: 'Medium',
      description: 'Serious effect on national interests, security, or safety',
      controls: [
        'Apply appropriate protective marking',
        'Implement access controls based on Need to Know',
        'Encrypt when stored or transmitted',
        'Restrict to authorized locations',
        'Regular access reviews required',
        'Secure disposal procedures',
        'Monitor and log access'
      ]
    },
    'restricted': {
      name: 'Restricted',
      color: 'bg-yellow-100 border-yellow-500 text-yellow-800',
      impact: 'Low',
      description: 'Limited negative effect on entities, individuals, or environment',
      controls: [
        'Apply protective marking as required',
        'Implement least privilege access',
        'Consider encryption for sensitive data',
        'Regular backup procedures',
        'Controlled sharing mechanisms',
        'Standard disposal procedures',
        'Access monitoring recommended'
      ]
    },
    'public': {
      name: 'Public',
      color: 'bg-green-100 border-green-500 text-green-800',
      impact: 'None',
      description: 'No impact on national interests, activities, individuals, or environment',
      controls: [
        'Standard information handling procedures',
        'Regular backup and maintenance',
        'Open sharing permitted after approval',
        'Standard retention policies apply',
        'Basic access logging',
        'Normal disposal procedures'
      ]
    }
  };

  const calculateClassification = () => {
    const allResponses = [];
    Object.values(impactAssessment).forEach(category => {
      Object.values(category).forEach(subcategory => {
        Object.values(subcategory).forEach(response => {
          allResponses.push(response);
        });
      });
    });

    const highCount = allResponses.filter(v => v === 'high').length;
    const mediumCount = allResponses.filter(v => v === 'medium').length;
    const lowCount = allResponses.filter(v => v === 'low').length;

    if (highCount > 0) {
      return 'top_secret';
    } else if (mediumCount > 0) {
      return 'secret';
    } else if (lowCount > 0) {
      return 'restricted';
    } else {
      return 'public';
    }
  };

  const getImpactSummary = () => {
    const allResponses = [];
    Object.values(impactAssessment).forEach(category => {
      Object.values(category).forEach(subcategory => {
        Object.values(subcategory).forEach(response => {
          allResponses.push(response);
        });
      });
    });

    return {
      high: allResponses.filter(v => v === 'high').length,
      medium: allResponses.filter(v => v === 'medium').length,
      low: allResponses.filter(v => v === 'low').length,
      none: allResponses.filter(v => v === 'none').length,
      total: allResponses.length
    };
  };

  const hasCompleteAssessment = () => {
    return Object.keys(impactAssessment).length > 0 && 
           Object.values(impactAssessment).some(category => 
             Object.values(category).some(subcategory => 
               Object.keys(subcategory).length > 0
             )
           );
  };

  return (
    <div className="max-w-6xl mx-auto p-6 bg-white">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          SDAIA Data Classification Tool
        </h1>
        <p className="text-gray-600">
          Assess impact and classify your data according to Saudi Data & AI Authority guidelines
        </p>
      </div>

      {!showResults ? (
        <div className="space-y-8">
          {/* Dataset Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="w-5 h-5" />
                Select Dataset Example (Optional)
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 mb-4">
                Choose an example dataset to help guide your impact assessment:
              </p>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Object.entries(exampleDatasets).map(([key, dataset]) => (
                  <div
                    key={key}
                    className={`p-4 border rounded-lg cursor-pointer transition-all ${
                      selectedDataset === key ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => setSelectedDataset(selectedDataset === key ? '' : key)}
                  >
                    <h3 className="font-semibold mb-2">{dataset.name}</h3>
                    <p className="text-sm text-gray-600 mb-2">{dataset.description}</p>
                    <div className="text-xs text-gray-500">
                      <strong>Examples:</strong> {dataset.examples.slice(0, 3).join(', ')}
                      {dataset.examples.length > 3 && '...'}
                    </div>
                  </div>
                ))}
              </div>

              {selectedDataset && (
                <Alert className="mt-4">
                  <AlertDescription>
                    <strong>Selected:</strong> {exampleDatasets[selectedDataset].name}
                    <br />
                    <strong>Key Risk Factors:</strong> {exampleDatasets[selectedDataset].riskFactors.join(', ')}
                  </AlertDescription>
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* Impact Assessment */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="w-5 h-5" />
                Impact Assessment
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 mb-6">
                Assess the potential impact of unauthorized access or disclosure in each category. 
                Consider what would happen if this data was compromised or made public.
              </p>

              <div className="space-y-8">
                {Object.entries(impactCategories).map(([categoryKey, category]) => (
                  <Card key={categoryKey} className="border-l-4 border-blue-500">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2 text-lg">
                        {category.icon}
                        {category.name}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      {Object.entries(category.subcategories).map(([subKey, subcategory]) => (
                        <div key={subKey} className="mb-6 p-4 bg-gray-50 rounded-lg">
                          <h4 className="font-semibold mb-4">{subcategory.name}</h4>
                          <div className="space-y-4">
                            {subcategory.questions.map((question, qIndex) => (
                              <div key={qIndex} className="space-y-3">
                                <p className="text-sm font-medium text-gray-700">{question}</p>
                                <div className="flex flex-wrap gap-3">
                                  {['high', 'medium', 'low', 'none'].map((level) => (
                                    <label key={level} className="flex items-center gap-2 cursor-pointer">
                                      <input
                                        type="radio"
                                        name={`${categoryKey}_${subKey}_${qIndex}`}
                                        value={level}
                                        onChange={(e) => {
                                          const newAssessment = { ...impactAssessment };
                                          if (!newAssessment[categoryKey]) newAssessment[categoryKey] = {};
                                          if (!newAssessment[categoryKey][subKey]) newAssessment[categoryKey][subKey] = {};
                                          newAssessment[categoryKey][subKey][qIndex] = e.target.value;
                                          setImpactAssessment(newAssessment);
                                        }}
                                        className="text-blue-600"
                                      />
                                      <span className={`text-xs px-3 py-1 rounded-full font-medium ${
                                        level === 'high' ? 'bg-red-100 text-red-800' :
                                        level === 'medium' ? 'bg-orange-100 text-orange-800' :
                                        level === 'low' ? 'bg-yellow-100 text-yellow-800' :
                                        'bg-green-100 text-green-800'
                                      }`}>
                                        {level.charAt(0).toUpperCase() + level.slice(1)}
                                      </span>
                                    </label>
                                  ))}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </CardContent>
                  </Card>
                ))}
              </div>

              <div className="mt-8 text-center">
                <button
                  onClick={() => setShowResults(true)}
                  disabled={!hasCompleteAssessment()}
                  className="px-8 py-3 bg-blue-600 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:bg-blue-700 transition-colors"
                >
                  Get Classification Result
                </button>
              </div>
            </CardContent>
          </Card>
        </div>
      ) : (
        /* Classification Results */
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-6 h-6" />
                Classification Result
              </CardTitle>
            </CardHeader>
            <CardContent>
              {(() => {
                const classification = calculateClassification();
                const level = classificationLevels[classification];
                const summary = getImpactSummary();

                return (
                  <div className="space-y-6">
                    {/* Main Classification Result */}
                    <div className={`p-6 rounded-lg border-2 ${level.color}`}>
                      <div className="flex items-center gap-4 mb-4">
                        <Shield className="w-12 h-12" />
                        <div>
                          <h2 className="text-3xl font-bold">{level.name}</h2>
                          <p className="text-lg opacity-75">Impact Level: {level.impact}</p>
                        </div>
                      </div>
                      <p className="text-base">{level.description}</p>
                    </div>

                    {/* Assessment Summary */}
                    <div className="grid md:grid-cols-2 gap-6">
                      <Card>
                        <CardHeader>
                          <CardTitle className="text-lg">Assessment Summary</CardTitle>
                        </CardHeader>
                        <CardContent>
                          {selectedDataset && (
                            <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                              <p className="font-semibold text-blue-900">{exampleDatasets[selectedDataset].name}</p>
                              <p className="text-sm text-blue-700">{exampleDatasets[selectedDataset].description}</p>
                            </div>
                          )}
                          
                          <div className="space-y-2">
                            <div className="flex justify-between items-center">
                              <span className="text-sm">High Impact Responses:</span>
                              <span className="px-2 py-1 bg-red-100 text-red-800 rounded text-sm font-medium">
                                {summary.high}
                              </span>
                            </div>
                            <div className="flex justify-between items-center">
                              <span className="text-sm">Medium Impact Responses:</span>
                              <span className="px-2 py-1 bg-orange-100 text-orange-800 rounded text-sm font-medium">
                                {summary.medium}
                              </span>
                            </div>
                            <div className="flex justify-between items-center">
                              <span className="text-sm">Low Impact Responses:</span>
                              <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-sm font-medium">
                                {summary.low}
                              </span>
                            </div>
                            <div className="flex justify-between items-center">
                              <span className="text-sm">No Impact Responses:</span>
                              <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-sm font-medium">
                                {summary.none}
                              </span>
                            </div>
                          </div>
                        </CardContent>
                      </Card>

                      <Card>
                        <CardHeader>
                          <CardTitle className="text-lg">Required Controls</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <ul className="space-y-2">
                            {level.controls.map((control, index) => (
                              <li key={index} className="flex items-start gap-2">
                                <span className="w-2 h-2 bg-blue-600 rounded-full mt-2 flex-shrink-0"></span>
                                <span className="text-sm">{control}</span>
                              </li>
                            ))}
                          </ul>
                        </CardContent>
                      </Card>
                    </div>

                    {/* Implementation Guidance */}
                    <Alert>
                      <AlertDescription>
                        <strong>Next Steps:</strong> This classification should be reviewed by a Data Classification Reviewer within one month. 
                        Implement the required controls and ensure all staff handling this data are trained on the appropriate procedures.
                      </AlertDescription>
                    </Alert>

                    {/* Action Buttons */}
                    <div className="flex gap-4 justify-center">
                      <button
                        onClick={() => {
                          setShowResults(false);
                          setImpactAssessment({});
                          setSelectedDataset('');
                        }}
                        className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
                      >
                        Start New Assessment
                      </button>
                      <button
                        onClick={() => setShowResults(false)}
                        className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        Modify Assessment
                      </button>
                    </div>
                  </div>
                );
              })()}
            </CardContent>
          </Card>
        </div>
      )}

      {/* Footer */}
      <div className="mt-8 pt-4 border-t text-center text-sm text-gray-500">
        Based on SDAIA National Data Governance Policies v1.0 (5/5/2020)
      </div>
    </div>
  );
};

export default DataClassificationApp;
