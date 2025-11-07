import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Progress } from './ui/progress';
import {
  Loader2, FileText, Shield, Users, Database, Clock,
  CheckCircle2, AlertTriangle, Download, Play, Copy,
  ChevronRight, Mail, Phone, TrendingUp, Target, Zap, Check
} from 'lucide-react';

const SEVERITY_COLORS = {
  critical: 'destructive',
  high: 'destructive',
  medium: 'warning',
  low: 'default'
};

const PHASE_ICONS = {
  "Preparation": Shield,
  "Detection and Analysis": Target,
  "Containment": AlertTriangle,
  "Eradication": Zap,
  "Recovery": TrendingUp,
  "Post-Incident Activity": FileText
};

export default function IRPlaybookGenerator() {
  const [templates, setTemplates] = useState([]);
  const [playbook, setPlaybook] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedIncidentType, setSelectedIncidentType] = useState('ransomware');
  const [selectedSeverity, setSelectedSeverity] = useState('high');
  const [selectedScope, setSelectedScope] = useState('single');
  const [automationLevel, setAutomationLevel] = useState('standard');
  const [currentPhase, setCurrentPhase] = useState(0);
  const [copiedText, setCopiedText] = useState('');

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/ir-playbooks/templates');
      setTemplates(response.data);
    } catch (error) {
      console.error('Error fetching templates:', error);
    }
  };

  const generatePlaybook = async () => {
    setLoading(true);
    try {
      const [playbookRes, metricsRes] = await Promise.all([
        axios.get('http://localhost:8000/api/ir-playbooks/generate', {
          params: {
            incident_type: selectedIncidentType,
            severity: selectedSeverity,
            scope: selectedScope,
            automation_level: automationLevel
          }
        }),
        axios.get(`http://localhost:8000/api/ir-playbooks/metrics/${selectedIncidentType}`)
      ]);
      
      setPlaybook(playbookRes.data);
      setMetrics(metricsRes.data);
      setCurrentPhase(0);
    } catch (error) {
      console.error('Error generating playbook:', error);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text, identifier) => {
    navigator.clipboard.writeText(text);
    setCopiedText(identifier);
    setTimeout(() => setCopiedText(''), 2000);
  };

  const exportPlaybook = () => {
    if (!playbook) return;
    
    const content = JSON.stringify(playbook, null, 2);
    const blob = new Blob([content], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${playbook.playbook_id}_incident_response_playbook.json`;
    a.click();
  };

  // Group steps by phase
  const stepsByPhase = playbook?.steps.reduce((acc, step) => {
    if (!acc[step.phase]) acc[step.phase] = [];
    acc[step.phase].push(step);
    return acc;
  }, {}) || {};

  const phases = Object.keys(stepsByPhase);

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-2xl">
            <FileText className="w-6 h-6" />
            Incident Response Playbook Generator
          </CardTitle>
          <p className="text-sm text-gray-500 mt-1">
            Generate customized IR playbooks based on incident type and organizational needs
          </p>
        </CardHeader>
      </Card>

      {/* Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Playbook Configuration</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
            <div>
              <label className="text-sm font-medium mb-2 block">Incident Type</label>
              <Select value={selectedIncidentType} onValueChange={setSelectedIncidentType}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {templates.map((template) => (
                    <SelectItem key={template.template_id} value={template.template_id}>
                      {template.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">Severity</label>
              <Select value={selectedSeverity} onValueChange={setSelectedSeverity}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="critical">Critical</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">Scope</label>
              <Select value={selectedScope} onValueChange={setSelectedScope}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="single">Single System</SelectItem>
                  <SelectItem value="multiple">Multiple Systems</SelectItem>
                  <SelectItem value="enterprise-wide">Enterprise-Wide</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">Automation</label>
              <Select value={automationLevel} onValueChange={setAutomationLevel}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="minimal">Minimal</SelectItem>
                  <SelectItem value="standard">Standard</SelectItem>
                  <SelectItem value="advanced">Advanced</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <Button onClick={generatePlaybook} disabled={loading} size="lg" className="w-full">
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin mr-2" />
            ) : (
              <Play className="w-4 h-4 mr-2" />
            )}
            Generate Playbook
          </Button>
        </CardContent>
      </Card>

      {/* Playbook Content */}
      {playbook && (
        <>
          {/* Playbook Overview */}
          <Card className="border-blue-200 bg-gradient-to-r from-blue-50 to-purple-50">
            <CardContent className="pt-6">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div>
                  <div className="text-sm text-gray-600 mb-1">Playbook ID</div>
                  <div className="text-lg font-bold">{playbook.playbook_id}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600 mb-1">Incident Type</div>
                  <Badge variant="outline" className="text-sm">{playbook.incident_type}</Badge>
                </div>
                <div>
                  <div className="text-sm text-gray-600 mb-1">Severity</div>
                  <Badge variant={SEVERITY_COLORS[playbook.severity]} className="text-sm">
                    {playbook.severity.toUpperCase()}
                  </Badge>
                </div>
                <div>
                  <div className="text-sm text-gray-600 mb-1">Estimated Duration</div>
                  <div className="text-lg font-bold">{playbook.estimated_duration}</div>
                </div>
              </div>

              <div className="mt-4 flex gap-3">
                <Button variant="outline" size="sm" onClick={exportPlaybook}>
                  <Download className="w-4 h-4 mr-2" />
                  Export Playbook
                </Button>
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={() => copyToClipboard(JSON.stringify(playbook, null, 2), 'playbook')}
                >
                  {copiedText === 'playbook' ? (
                    <Check className="w-4 h-4 mr-2" />
                  ) : (
                    <Copy className="w-4 h-4 mr-2" />
                  )}
                  Copy JSON
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Performance Metrics */}
          {metrics && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Clock className="w-5 h-5" />
                  Expected Performance Metrics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  <div className="text-center p-3 bg-blue-50 rounded-lg">
                    <div className="text-xs text-blue-600 mb-1">Time to Detect</div>
                    <div className="text-lg font-bold text-blue-700">{metrics.mean_time_to_detect}</div>
                  </div>
                  <div className="text-center p-3 bg-purple-50 rounded-lg">
                    <div className="text-xs text-purple-600 mb-1">Time to Respond</div>
                    <div className="text-lg font-bold text-purple-700">{metrics.mean_time_to_respond}</div>
                  </div>
                  <div className="text-center p-3 bg-orange-50 rounded-lg">
                    <div className="text-xs text-orange-600 mb-1">Time to Contain</div>
                    <div className="text-lg font-bold text-orange-700">{metrics.mean_time_to_contain}</div>
                  </div>
                  <div className="text-center p-3 bg-green-50 rounded-lg">
                    <div className="text-xs text-green-600 mb-1">Time to Recover</div>
                    <div className="text-lg font-bold text-green-700">{metrics.mean_time_to_recover}</div>
                  </div>
                  <div className="text-center p-3 bg-gray-100 rounded-lg">
                    <div className="text-xs text-gray-600 mb-1">Total Time</div>
                    <div className="text-lg font-bold text-gray-700">{metrics.total_estimated_time}</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Main Tabs */}
          <Tabs defaultValue="steps" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="steps">
                <FileText className="w-4 h-4 mr-2" />
                Response Steps
              </TabsTrigger>
              <TabsTrigger value="stakeholders">
                <Users className="w-4 h-4 mr-2" />
                Stakeholders
              </TabsTrigger>
              <TabsTrigger value="evidence">
                <Database className="w-4 h-4 mr-2" />
                Evidence
              </TabsTrigger>
              <TabsTrigger value="compliance">
                <Shield className="w-4 h-4 mr-2" />
                Compliance
              </TabsTrigger>
            </TabsList>

            {/* Response Steps Tab */}
            <TabsContent value="steps">
              <div className="space-y-6">
                {/* Phase Navigation */}
                <Card>
                  <CardContent className="pt-6">
                    <div className="flex items-center gap-2 mb-4 overflow-x-auto">
                      {phases.map((phase, idx) => {
                        const PhaseIcon = PHASE_ICONS[phase] || FileText;
                        return (
                          <React.Fragment key={phase}>
                            <button
                              onClick={() => setCurrentPhase(idx)}
                              className={`flex-1 p-3 rounded-lg border-2 transition-all min-w-[140px] ${
                                currentPhase === idx
                                  ? 'border-blue-600 bg-blue-50'
                                  : 'border-gray-200 hover:border-gray-300'
                              }`}
                            >
                              <PhaseIcon className={`w-5 h-5 mx-auto mb-1 ${
                                currentPhase === idx ? 'text-blue-600' : 'text-gray-400'
                              }`} />
                              <div className={`text-xs font-semibold ${
                                currentPhase === idx ? 'text-blue-600' : 'text-gray-600'
                              }`}>
                                {phase}
                              </div>
                              <div className="text-xs text-gray-500 mt-1">
                                {stepsByPhase[phase].length} steps
                              </div>
                            </button>
                            {idx < phases.length - 1 && (
                              <ChevronRight className="w-4 h-4 text-gray-400 flex-shrink-0" />
                            )}
                          </React.Fragment>
                        );
                      })}
                    </div>

                    <Progress value={((currentPhase + 1) / phases.length) * 100} className="h-2" />
                  </CardContent>
                </Card>

                {/* Current Phase Steps */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">
                      {phases[currentPhase]} - Detailed Steps
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {stepsByPhase[phases[currentPhase]]?.map((step, idx) => (
                        <div key={idx} className="p-4 border-2 rounded-lg">
                          <div className="flex items-start gap-4">
                            <div className="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold flex-shrink-0">
                              {step.step_number}
                            </div>
                            <div className="flex-1">
                              <div className="flex items-start justify-between mb-2">
                                <div>
                                  <h4 className="font-bold text-lg mb-1">{step.action}</h4>
                                  <p className="text-sm text-gray-600 mb-2">{step.description}</p>
                                </div>
                                {step.automation_available && (
                                  <Badge variant="default" className="ml-2">
                                    <Zap className="w-3 h-3 mr-1" />
                                    Automated
                                  </Badge>
                                )}
                              </div>

                              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3 text-sm">
                                <div>
                                  <span className="text-gray-600">Responsible:</span>
                                  <div className="font-semibold">{step.responsible_party}</div>
                                </div>
                                <div>
                                  <span className="text-gray-600">Estimated Time:</span>
                                  <div className="font-semibold flex items-center gap-1">
                                    <Clock className="w-3 h-3" />
                                    {step.estimated_time}
                                  </div>
                                </div>
                                <div>
                                  <span className="text-gray-600">Phase:</span>
                                  <Badge variant="outline" className="text-xs">{step.phase}</Badge>
                                </div>
                              </div>

                              <div className="space-y-2">
                                <div>
                                  <div className="text-xs font-semibold text-gray-700 mb-1">Required Tools:</div>
                                  <div className="flex gap-2 flex-wrap">
                                    {step.required_tools.map((tool, i) => (
                                      <Badge key={i} variant="secondary" className="text-xs">
                                        {tool}
                                      </Badge>
                                    ))}
                                  </div>
                                </div>

                                <div>
                                  <div className="text-xs font-semibold text-gray-700 mb-1">Success Criteria:</div>
                                  <ul className="text-xs space-y-1">
                                    {step.success_criteria.map((criteria, i) => (
                                      <li key={i} className="flex items-start gap-2">
                                        <CheckCircle2 className="w-3 h-3 text-green-600 mt-0.5 flex-shrink-0" />
                                        <span>{criteria}</span>
                                      </li>
                                    ))}
                                  </ul>
                                </div>

                                {step.escalation_triggers.length > 0 && (
                                  <div>
                                    <div className="text-xs font-semibold text-red-700 mb-1">Escalation Triggers:</div>
                                    <ul className="text-xs space-y-1">
                                      {step.escalation_triggers.map((trigger, i) => (
                                        <li key={i} className="flex items-start gap-2">
                                          <AlertTriangle className="w-3 h-3 text-red-600 mt-0.5 flex-shrink-0" />
                                          <span>{trigger}</span>
                                        </li>
                                      ))}
                                    </ul>
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="mt-4 flex gap-2">
                      <Button
                        variant="outline"
                        disabled={currentPhase === 0}
                        onClick={() => setCurrentPhase(Math.max(0, currentPhase - 1))}
                      >
                        Previous Phase
                      </Button>
                      <Button
                        disabled={currentPhase === phases.length - 1}
                        onClick={() => setCurrentPhase(Math.min(phases.length - 1, currentPhase + 1))}
                      >
                        Next Phase
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            {/* Stakeholders Tab */}
            <TabsContent value="stakeholders">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Stakeholder Notification Matrix</CardTitle>
                  <p className="text-sm text-gray-500">
                    Required communications and escalation procedures
                  </p>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {playbook.stakeholders.map((stakeholder, idx) => (
                      <div key={idx} className="p-4 border rounded-lg bg-purple-50">
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex items-center gap-2">
                            <Users className="w-5 h-5 text-purple-600" />
                            <h4 className="font-bold">{stakeholder.stakeholder_type}</h4>
                          </div>
                          <Badge variant="outline" className="text-xs">
                            {stakeholder.notification_method}
                          </Badge>
                        </div>

                        <div className="space-y-2 text-sm">
                          <div>
                            <span className="text-gray-600 font-semibold">Trigger:</span>
                            <p className="mt-1">{stakeholder.notification_trigger}</p>
                          </div>

                          <div>
                            <span className="text-gray-600 font-semibold">Escalation Threshold:</span>
                            <p className="mt-1 text-red-700">{stakeholder.escalation_threshold}</p>
                          </div>

                          <div>
                            <span className="text-gray-600 font-semibold">Communication Template:</span>
                            <div className="mt-2 p-3 bg-white rounded border font-mono text-xs whitespace-pre-wrap">
                              {stakeholder.communication_template}
                            </div>
                            <Button
                              variant="outline"
                              size="sm"
                              className="mt-2"
                              onClick={() => copyToClipboard(stakeholder.communication_template, `stakeholder-${idx}`)}
                            >
                              {copiedText === `stakeholder-${idx}` ? (
                                <Check className="w-3 h-3 mr-1" />
                              ) : (
                                <Copy className="w-3 h-3 mr-1" />
                              )}
                              Copy Template
                            </Button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Evidence Tab */}
            <TabsContent value="evidence">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Evidence Collection Requirements</CardTitle>
                  <p className="text-sm text-gray-500">
                    Critical evidence to preserve for investigation and legal proceedings
                  </p>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {playbook.evidence_collection.map((evidence, idx) => (
                      <div key={idx} className="p-4 border rounded-lg">
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex items-center gap-2">
                            <Database className="w-5 h-5 text-blue-600" />
                            <h4 className="font-bold">{evidence.evidence_type}</h4>
                          </div>
                          <div className="flex gap-2">
                            {evidence.chain_of_custody && (
                              <Badge variant="default" className="text-xs">
                                <Shield className="w-3 h-3 mr-1" />
                                Chain of Custody
                              </Badge>
                            )}
                            {evidence.legal_hold_required && (
                              <Badge variant="destructive" className="text-xs">
                                Legal Hold
                              </Badge>
                            )}
                          </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                          <div>
                            <span className="text-gray-600">Collection Method:</span>
                            <p className="font-semibold">{evidence.collection_method}</p>
                          </div>
                          <div>
                            <span className="text-gray-600">Retention Period:</span>
                            <p className="font-semibold">{evidence.retention_period}</p>
                          </div>
                          <div>
                            <span className="text-gray-600">Storage Location:</span>
                            <p className="font-semibold">{evidence.storage_location}</p>
                          </div>
                          <div>
                            <span className="text-gray-600">Legal Hold:</span>
                            <p className="font-semibold">
                              {evidence.legal_hold_required ? 'Required' : 'Not Required'}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  <Alert className="mt-4 border-orange-200 bg-orange-50">
                    <AlertTriangle className="h-4 w-4 text-orange-600" />
                    <AlertDescription className="text-sm text-orange-900">
                      <strong>Important:</strong> All evidence must be collected and preserved
                      according to forensic best practices. Maintain proper chain of custody
                      documentation for all items that may be used in legal proceedings.
                    </AlertDescription>
                  </Alert>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Compliance Tab */}
            <TabsContent value="compliance">
              <div className="space-y-6">
                {/* Compliance Requirements */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Regulatory Compliance Requirements</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {playbook.compliance_requirements.map((req, idx) => (
                        <div key={idx} className="flex items-start gap-3 p-3 border rounded-lg bg-blue-50">
                          <Shield className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                          <span className="text-sm">{req}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* MITRE ATT&CK Techniques */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Associated MITRE ATT&CK Techniques</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex gap-2 flex-wrap">
                      {playbook.mitre_techniques.map((technique, idx) => (
                        <Badge key={idx} variant="destructive" className="text-sm">
                          {technique}
                        </Badge>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Success Metrics */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Success Metrics & KPIs</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {Object.entries(playbook.success_metrics).map(([key, value], idx) => (
                        <div key={idx} className="p-4 border rounded-lg bg-green-50">
                          <div className="text-sm text-gray-600 capitalize mb-1">
                            {key.replace(/_/g, ' ')}
                          </div>
                          <div className="text-lg font-bold text-green-700">{value}</div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Post-Incident Actions */}
                <Card className="border-purple-200 bg-purple-50">
                  <CardHeader>
                    <CardTitle className="text-lg text-purple-900">
                      Post-Incident Follow-up Actions
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ol className="space-y-3">
                      <li className="flex items-start gap-3">
                        <Badge variant="default" className="w-6 h-6 flex items-center justify-center p-0">
                          1
                        </Badge>
                        <span className="text-sm text-purple-900">
                          Schedule post-incident review within 5 business days
                        </span>
                      </li>
                      <li className="flex items-start gap-3">
                        <Badge variant="default" className="w-6 h-6 flex items-center justify-center p-0">
                          2
                        </Badge>
                        <span className="text-sm text-purple-900">
                          Document all lessons learned and update playbooks accordingly
                        </span>
                      </li>
                      <li className="flex items-start gap-3">
                        <Badge variant="default" className="w-6 h-6 flex items-center justify-center p-0">
                          3
                        </Badge>
                        <span className="text-sm text-purple-900">
                          Implement approved security improvements within 30 days
                        </span>
                      </li>
                      <li className="flex items-start gap-3">
                        <Badge variant="default" className="w-6 h-6 flex items-center justify-center p-0">
                          4
                        </Badge>
                        <span className="text-sm text-purple-900">
                          Conduct tabletop exercise for similar scenario within 90 days
                        </span>
                      </li>
                      <li className="flex items-start gap-3">
                        <Badge variant="default" className="w-6 h-6 flex items-center justify-center p-0">
                          5
                        </Badge>
                        <span className="text-sm text-purple-900">
                          Update security awareness training based on incident findings
                        </span>
                      </li>
                    </ol>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </>
      )}

      {/* No Playbook Generated */}
      {!playbook && !loading && (
        <Card>
          <CardContent className="py-12">
            <div className="text-center text-gray-500">
              <FileText className="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <p className="text-lg mb-2">No Playbook Generated</p>
              <p className="text-sm">Configure your incident parameters above and click "Generate Playbook"</p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

