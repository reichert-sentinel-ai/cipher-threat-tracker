import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { apiPath } from '../config/api.js';
import {
  BarChart, Bar, PieChart, Pie, Cell, RadarChart, Radar,
  PolarGrid, PolarAngleAxis, PolarRadiusAxis, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Progress } from './ui/progress';
import {
  Loader2, Shield, Target, AlertTriangle, CheckCircle2,
  XCircle, Search, TrendingUp, Users, FileText, Layers,
  Activity, Eye, ChevronRight, Database, Zap
} from 'lucide-react';

const COVERAGE_COLORS = {
  none: '#dc2626',
  partial: '#f59e0b',
  good: '#3b82f6',
  excellent: '#22c55e'
};

const getCoverageIcon = (coverage) => {
  switch(coverage) {
    case 'excellent': return <CheckCircle2 className="w-4 h-4 text-green-600" />;
    case 'good': return <CheckCircle2 className="w-4 h-4 text-blue-600" />;
    case 'partial': return <AlertTriangle className="w-4 h-4 text-orange-600" />;
    case 'none': return <XCircle className="w-4 h-4 text-red-600" />;
    default: return null;
  }
};

export default function MitreAttackMap() {
  const [matrix, setMatrix] = useState(null);
  const [gapAnalysis, setGapAnalysis] = useState(null);
  const [actorTTPs, setActorTTPs] = useState(null);
  const [selectedTechnique, setSelectedTechnique] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTactic, setSelectedTactic] = useState(null);
  const [threatActor, setThreatActor] = useState('APT28');

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const [matrixRes, gapRes] = await Promise.all([
        axios.get(apiPath('mitre/coverage-matrix')),
        axios.get(apiPath('mitre/gap-analysis'))
      ]);
      
      setMatrix(matrixRes.data);
      setGapAnalysis(gapRes.data);
    } catch (error) {
      console.error('Error fetching MITRE data:', error);
    } finally {
      setLoading(false);
    }
  }, []); // Empty deps - only fetch on mount

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const fetchThreatActorTTPs = async (actor) => {
    try {
      const response = await axios.get(apiPath(`mitre/threat-actor-ttps/${actor}`));
      setActorTTPs(response.data);
    } catch (error) {
      console.error('Error fetching threat actor TTPs:', error);
    }
  };

  const viewTechniqueDetails = async (techniqueId) => {
    try {
      const response = await axios.get(apiPath(`mitre/technique-details/${techniqueId}`));
      setSelectedTechnique(response.data);
    } catch (error) {
      console.error('Error fetching technique details:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  // Filter techniques by search query
  const filteredTechniques = matrix?.techniques.filter(tech =>
    tech.technique_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    tech.technique_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    tech.tactic.toLowerCase().includes(searchQuery.toLowerCase())
  ) || [];

  // Prepare coverage distribution data
  const coverageDistribution = matrix ? [
    { name: 'Excellent', value: matrix.techniques.filter(t => t.detection_coverage === 'excellent').length, fill: COVERAGE_COLORS.excellent },
    { name: 'Good', value: matrix.techniques.filter(t => t.detection_coverage === 'good').length, fill: COVERAGE_COLORS.good },
    { name: 'Partial', value: matrix.techniques.filter(t => t.detection_coverage === 'partial').length, fill: COVERAGE_COLORS.partial },
    { name: 'None', value: matrix.techniques.filter(t => t.detection_coverage === 'none').length, fill: COVERAGE_COLORS.none }
  ] : [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2 text-2xl">
                <Target className="w-6 h-6" />
                MITRE ATT&CK Coverage Map
              </CardTitle>
              <p className="text-sm text-gray-500 dark:text-[#a0a0a0] mt-1">
                Detection coverage across the MITRE ATT&CK framework
              </p>
            </div>
            <Button variant="outline" onClick={fetchData}>
              <Activity className="w-4 h-4 mr-2" />
              Refresh
            </Button>
          </div>
        </CardHeader>
      </Card>

      {/* Overall Coverage Summary */}
      <Card className="border-blue-200 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 dark:border-blue-800">
        <CardContent className="pt-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="col-span-2">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700 dark:text-[#a0a0a0]">
                  Overall Detection Coverage
                </span>
                <span className="text-3xl font-bold text-blue-600 dark:text-blue-400">
                  {matrix?.overall_coverage}%
                </span>
              </div>
              <Progress value={matrix?.overall_coverage} className="h-3" />
              <div className="flex items-center gap-2 mt-2 text-xs text-gray-600 dark:text-[#a0a0a0]">
                <Shield className="w-4 h-4" />
                Last updated: {new Date(matrix?.last_updated).toLocaleString()}
              </div>
            </div>

            <div>
              <div className="text-sm text-gray-600 dark:text-[#a0a0a0] mb-1">Total Techniques</div>
              <div className="text-3xl font-bold">{matrix?.total_techniques}</div>
              <div className="text-xs text-gray-500 dark:text-[#6a6a6a] mt-1">
                Covered: {matrix?.covered_techniques}
              </div>
            </div>

            <div>
              <div className="text-sm text-gray-600 dark:text-[#a0a0a0] mb-1">Coverage Gaps</div>
              <div className="text-3xl font-bold text-red-600 dark:text-red-400">{matrix?.gap_techniques}</div>
              <div className="text-xs text-gray-500 dark:text-[#6a6a6a] mt-1">
                Require attention
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Tabs */}
      <Tabs defaultValue="matrix" className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="matrix">
            <Layers className="w-4 h-4 mr-2" />
            Coverage Matrix
          </TabsTrigger>
          <TabsTrigger value="tactics">
            <Target className="w-4 h-4 mr-2" />
            Tactics
          </TabsTrigger>
          <TabsTrigger value="gaps">
            <AlertTriangle className="w-4 h-4 mr-2" />
            Gap Analysis
          </TabsTrigger>
          <TabsTrigger value="threat-actors">
            <Users className="w-4 h-4 mr-2" />
            Threat Actors
          </TabsTrigger>
          <TabsTrigger value="overview">
            <TrendingUp className="w-4 h-4 mr-2" />
            Overview
          </TabsTrigger>
        </TabsList>

        {/* Coverage Matrix Tab */}
        <TabsContent value="matrix">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">Technique Coverage Matrix</CardTitle>
                <Input
                  placeholder="Search techniques..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-64"
                />
              </div>
            </CardHeader>
            <CardContent>
              {/* Coverage Legend */}
              <div className="flex gap-4 mb-6 p-4 bg-gray-50 dark:bg-[#1a1a1a] rounded-lg">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded" style={{ backgroundColor: COVERAGE_COLORS.excellent }} />
                  <span className="text-sm">Excellent (90%+)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded" style={{ backgroundColor: COVERAGE_COLORS.good }} />
                  <span className="text-sm">Good (70-90%)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded" style={{ backgroundColor: COVERAGE_COLORS.partial }} />
                  <span className="text-sm">Partial (40-70%)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded" style={{ backgroundColor: COVERAGE_COLORS.none }} />
                  <span className="text-sm">None (&lt;40%)</span>
                </div>
              </div>

              {/* Techniques Grid */}
              <div className="space-y-2 max-h-[600px] overflow-y-auto">
                {filteredTechniques.map((technique) => (
                  <div
                    key={technique.technique_id}
                    className="p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-[#1a1a1a] cursor-pointer transition-colors"
                    onClick={() => viewTechniqueDetails(technique.technique_id)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-start gap-3 flex-1">
                        <div
                          className="w-12 h-12 rounded flex items-center justify-center flex-shrink-0"
                          style={{ backgroundColor: COVERAGE_COLORS[technique.detection_coverage] }}
                        >
                          <span className="text-white font-bold text-xs">
                            {(technique.detection_score * 100).toFixed(0)}%
                          </span>
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="font-mono font-semibold">{technique.technique_id}</span>
                            <span className="font-semibold">{technique.technique_name}</span>
                            {getCoverageIcon(technique.detection_coverage)}
                          </div>
                          
                          <div className="flex items-center gap-3 text-sm text-gray-600 dark:text-[#a0a0a0] mb-2">
                            <Badge variant="outline">{technique.tactic}</Badge>
                            {technique.recent_detections > 0 && (
                              <span className="flex items-center gap-1">
                                <Activity className="w-3 h-3" />
                                {technique.recent_detections} recent detections
                              </span>
                            )}
                            {technique.mitigation_implemented && (
                              <Badge variant="default" className="text-xs">
                                <Shield className="w-3 h-3 mr-1" />
                                Mitigated
                              </Badge>
                            )}
                          </div>

                          <p className="text-sm text-gray-600 dark:text-[#a0a0a0] mb-2">{technique.description}</p>

                          <div className="flex items-center gap-4 text-xs">
                            <div>
                              <span className="text-gray-500 dark:text-[#6a6a6a]">Platforms: </span>
                              <span className="font-semibold">{technique.platforms.join(', ')}</span>
                            </div>
                            <div>
                              <span className="text-gray-500 dark:text-[#6a6a6a]">Data Sources: </span>
                              <span className="font-semibold">{technique.data_sources.length}</span>
                            </div>
                          </div>

                          {technique.threat_actors_using.length > 0 && (
                            <div className="mt-2">
                              <span className="text-xs text-gray-600 dark:text-[#a0a0a0]">Threat Actors: </span>
                              {technique.threat_actors_using.map((actor, idx) => (
                                <Badge key={idx} variant="destructive" className="text-xs mr-1">
                                  {actor}
                                </Badge>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-gray-400 flex-shrink-0" />
                    </div>
                  </div>
                ))}
              </div>

              {filteredTechniques.length === 0 && (
                <div className="text-center py-12 text-gray-500 dark:text-[#a0a0a0]">
                  <Search className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                  <p>No techniques found matching your search</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Tactics Tab */}
        <TabsContent value="tactics">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Tactic-Level Coverage</CardTitle>
              <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                Detection coverage organized by MITRE ATT&CK tactics
              </p>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={matrix?.tactics}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="tactic_name" angle={-45} textAnchor="end" height={150} />
                  <YAxis label={{ value: 'Coverage %', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="coverage_percentage" fill="#3b82f6" name="Coverage %" />
                </BarChart>
              </ResponsiveContainer>

              <div className="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {matrix?.tactics.map((tactic) => (
                  <Card key={tactic.tactic_id} className="border-2">
                    <CardContent className="pt-6">
                      <div className="mb-3">
                        <div className="flex items-center justify-between mb-1">
                          <h3 className="font-bold">{tactic.tactic_name}</h3>
                          <Badge variant="outline">{tactic.tactic_id}</Badge>
                        </div>
                        <Progress value={tactic.coverage_percentage} className="h-2" />
                        <div className="text-xs text-gray-500 dark:text-[#6a6a6a] mt-1">
                          {tactic.coverage_percentage.toFixed(1)}% coverage
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-3 text-sm mb-3">
                        <div>
                          <div className="text-gray-600 dark:text-[#a0a0a0]">Total</div>
                          <div className="font-bold text-lg">{tactic.total_techniques}</div>
                        </div>
                        <div>
                          <div className="text-gray-600 dark:text-[#a0a0a0]">Covered</div>
                          <div className="font-bold text-lg text-green-600 dark:text-green-400">{tactic.covered_techniques}</div>
                        </div>
                      </div>

                      {tactic.gap_count > 0 && (
                        <div>
                          <div className="flex items-center gap-2 text-sm text-red-600 dark:text-red-400 mb-1">
                            <AlertTriangle className="w-4 h-4" />
                            <span className="font-semibold">{tactic.gap_count} Gaps</span>
                          </div>
                          <div className="text-xs text-gray-600 dark:text-[#a0a0a0]">
                            Priority: {tactic.priority_gaps.slice(0, 2).join(', ')}
                          </div>
                        </div>
                      )}

                      <Button
                        variant="outline"
                        size="sm"
                        className="w-full mt-3"
                        onClick={() => setSelectedTactic(tactic.tactic_name)}
                      >
                        View Details
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Gap Analysis Tab */}
        <TabsContent value="gaps">
          <div className="space-y-6">
            {/* Risk Score */}
            <Card className="border-red-200 bg-red-50 dark:bg-red-900/20 dark:border-red-800">
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm text-red-800 dark:text-red-300 mb-1">Overall Risk Score</div>
                    <div className="text-4xl font-bold text-red-600 dark:text-red-400">
                      {gapAnalysis?.risk_score}/100
                    </div>
                  </div>
                  <AlertTriangle className="w-16 h-16 text-red-600 dark:text-red-400" />
                </div>
              </CardContent>
            </Card>

            {/* Critical Gaps */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-red-600" />
                  Critical Detection Gaps
                </CardTitle>
                <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                  High-priority techniques requiring immediate attention
                </p>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {gapAnalysis?.critical_gaps.map((gap, idx) => (
                    <div key={idx} className="p-4 border rounded-lg">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <Badge variant="outline">{gap.technique_id}</Badge>
                          <span className="font-semibold">{gap.technique_name}</span>
                        </div>
                        <Badge 
                          variant={
                            gap.risk_level === 'critical' ? 'destructive' :
                            gap.risk_level === 'high' ? 'destructive' :
                            'warning'
                          }
                        >
                          {gap.risk_level.toUpperCase()}
                        </Badge>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                        <div>
                          <div className="text-gray-600 dark:text-[#a0a0a0]">Tactic</div>
                          <Badge variant="secondary" className="text-xs">{gap.tactic}</Badge>
                        </div>
                        <div>
                          <div className="text-gray-600 dark:text-[#a0a0a0]">Threat Actors</div>
                          <div className="font-semibold">{gap.threat_actors_using}</div>
                        </div>
                        <div>
                          <div className="text-gray-600 dark:text-[#a0a0a0]">Recent Campaigns</div>
                          <div className="font-semibold">{gap.recent_campaigns}</div>
                        </div>
                        <div>
                          <div className="text-gray-600 dark:text-[#a0a0a0]">Implementation</div>
                          <div className="font-semibold">{gap.estimated_time}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Recommended Detections */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Zap className="w-5 h-5 text-blue-600" />
                  Recommended Detections
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {gapAnalysis?.recommended_detections.map((rec, idx) => (
                    <div key={idx} className="p-4 border rounded-lg bg-blue-50 dark:bg-blue-900/20">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <div className="flex items-center gap-2 mb-1">
                            <Badge variant="outline">{rec.technique_id}</Badge>
                            <span className="font-semibold">{rec.technique_name}</span>
                          </div>
                          <div className="text-sm text-gray-600 dark:text-[#a0a0a0]">{rec.detection_method}</div>
                        </div>
                        <Badge variant={
                          rec.implementation_priority === 'critical' ? 'destructive' :
                          rec.implementation_priority === 'high' ? 'destructive' :
                          'default'
                        }>
                          {rec.implementation_priority}
                        </Badge>
                      </div>

                      <div className="grid grid-cols-2 gap-3 text-sm mt-3">
                        <div>
                          <span className="text-gray-600 dark:text-[#a0a0a0]">Data Source: </span>
                          <span className="font-semibold">{rec.recommended_data_source}</span>
                        </div>
                        <div>
                          <span className="text-gray-600 dark:text-[#a0a0a0]">False Positive Rate: </span>
                          <span className="font-semibold">{rec.expected_false_positive_rate}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Priority Implementation Order */}
            <Card className="border-purple-200 bg-purple-50 dark:bg-purple-900/20 dark:border-purple-800">
              <CardHeader>
                <CardTitle className="text-lg text-purple-900 dark:text-purple-200">
                  Recommended Implementation Priority
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ol className="space-y-2">
                  {gapAnalysis?.priority_order.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <Badge variant="default" className="w-6 h-6 flex items-center justify-center p-0">
                        {idx + 1}
                      </Badge>
                      <span className="text-sm text-purple-900 dark:text-purple-200">{item}</span>
                    </li>
                  ))}
                </ol>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Threat Actors Tab */}
        <TabsContent value="threat-actors">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">Threat Actor TTPs Analysis</CardTitle>
                <div className="flex items-center gap-3">
                  <Input
                    placeholder="Enter threat actor..."
                    value={threatActor}
                    onChange={(e) => setThreatActor(e.target.value)}
                    className="w-48"
                  />
                  <Button onClick={() => fetchThreatActorTTPs(threatActor)}>
                    <Search className="w-4 h-4 mr-2" />
                    Analyze
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              {actorTTPs ? (
                <div className="space-y-6">
                  {/* Actor Overview */}
                  <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
                    <h3 className="text-lg font-bold mb-3">{actorTTPs.threat_actor}</h3>
                    <div className="grid grid-cols-3 gap-4">
                      <div>
                        <div className="text-sm text-gray-600 dark:text-[#a0a0a0]">Techniques Used</div>
                        <div className="text-2xl font-bold">{actorTTPs.techniques_used.length}</div>
                      </div>
                      <div>
                        <div className="text-sm text-gray-600 dark:text-[#a0a0a0]">Detection Coverage</div>
                        <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                          {(actorTTPs.detection_coverage * 100).toFixed(0)}%
                        </div>
                      </div>
                      <div>
                        <div className="text-sm text-gray-600 dark:text-[#a0a0a0]">High Risk Gaps</div>
                        <div className="text-2xl font-bold text-red-600 dark:text-red-400">
                          {actorTTPs.high_risk_techniques.length}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Tactics Distribution */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Tactics Distribution</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={Object.entries(actorTTPs.tactics_distribution).map(([name, value]) => ({ name, value }))}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                          <YAxis />
                          <Tooltip />
                          <Bar dataKey="value" fill="#8b5cf6" />
                        </BarChart>
                      </ResponsiveContainer>
                    </CardContent>
                  </Card>

                  {/* High Risk Techniques */}
                  {actorTTPs.high_risk_techniques.length > 0 && (
                    <Alert className="border-red-200 bg-red-50 dark:bg-red-900/20 dark:border-red-800">
                      <AlertTriangle className="h-4 w-4 text-red-600 dark:text-red-400" />
                      <AlertDescription>
                        <div className="text-sm text-red-900 dark:text-red-300">
                          <strong className="block mb-2">Critical Detection Gaps for {actorTTPs.threat_actor}:</strong>
                          <ul className="space-y-1 list-disc list-inside">
                            {actorTTPs.high_risk_techniques.map((tech, idx) => (
                              <li key={idx}>{tech}</li>
                            ))}
                          </ul>
                        </div>
                      </AlertDescription>
                    </Alert>
                  )}

                  {/* Techniques List */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Techniques Timeline</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3 max-h-96 overflow-y-auto">
                        {actorTTPs.techniques_used.map((tech, idx) => (
                          <div key={idx} className="p-3 border rounded-lg">
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center gap-2">
                                <Badge variant="outline">{tech.technique_id}</Badge>
                                <span className="font-semibold text-sm">{tech.technique_name}</span>
                                {tech.detection_coverage ? (
                                  <CheckCircle2 className="w-4 h-4 text-green-600" />
                                ) : (
                                  <XCircle className="w-4 h-4 text-red-600" />
                                )}
                              </div>
                              <Badge variant={tech.severity === 'critical' ? 'destructive' : 'warning'}>
                                {tech.severity}
                              </Badge>
                            </div>
                            <div className="grid grid-cols-3 gap-3 text-xs">
                              <div>
                                <span className="text-gray-600 dark:text-[#a0a0a0]">Tactic:</span>
                                <Badge variant="secondary" className="ml-1 text-xs">{tech.tactic}</Badge>
                              </div>
                              <div>
                                <span className="text-gray-600 dark:text-[#a0a0a0]">Frequency:</span>
                                <span className="font-semibold ml-1 capitalize">{tech.frequency}</span>
                              </div>
                              <div>
                                <span className="text-gray-600 dark:text-[#a0a0a0]">Last Seen:</span>
                                <span className="font-semibold ml-1">{tech.last_observed}</span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500 dark:text-[#a0a0a0]">
                  <Users className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                  <p>Enter a threat actor name and click Analyze to view their TTPs</p>
                  <p className="text-sm mt-2">Examples: APT28, APT29, Lazarus Group, FIN7</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Overview Tab */}
        <TabsContent value="overview">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Coverage Distribution Pie */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Coverage Distribution</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={coverageDistribution}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, value }) => `${name}: ${value}`}
                      outerRadius={100}
                      dataKey="value"
                    >
                      {coverageDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Key Metrics */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Key Metrics</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                    <div>
                      <div className="text-sm text-green-800 dark:text-green-300">Excellent Coverage</div>
                      <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                        {coverageDistribution.find(d => d.name === 'Excellent')?.value || 0}
                      </div>
                    </div>
                    <CheckCircle2 className="w-8 h-8 text-green-600 dark:text-green-400" />
                  </div>

                  <div className="flex items-center justify-between p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <div>
                      <div className="text-sm text-blue-800 dark:text-blue-300">Good Coverage</div>
                      <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                        {coverageDistribution.find(d => d.name === 'Good')?.value || 0}
                      </div>
                    </div>
                    <CheckCircle2 className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                  </div>

                  <div className="flex items-center justify-between p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                    <div>
                      <div className="text-sm text-orange-800 dark:text-orange-300">Partial Coverage</div>
                      <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                        {coverageDistribution.find(d => d.name === 'Partial')?.value || 0}
                      </div>
                    </div>
                    <AlertTriangle className="w-8 h-8 text-orange-600 dark:text-orange-400" />
                  </div>

                  <div className="flex items-center justify-between p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                    <div>
                      <div className="text-sm text-red-800 dark:text-red-300">No Coverage</div>
                      <div className="text-2xl font-bold text-red-600 dark:text-red-400">
                        {coverageDistribution.find(d => d.name === 'None')?.value || 0}
                      </div>
                    </div>
                    <XCircle className="w-8 h-8 text-red-600 dark:text-red-400" />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Top Data Sources */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Common Data Sources</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {[
                    "Process Monitoring",
                    "File Monitoring",
                    "Network Traffic Analysis",
                    "Windows Event Logs",
                    "Authentication Logs",
                    "Command Execution"
                  ].map((source, idx) => (
                    <div key={idx} className="flex items-center justify-between p-2 bg-gray-50 dark:bg-[#1a1a1a] rounded">
                      <span className="text-sm">{source}</span>
                      <Badge variant="outline">
                        {matrix?.techniques.filter(t => 
                          t.data_sources.some(ds => ds.toLowerCase().includes(source.toLowerCase()))
                        ).length}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Action Items */}
            <Card className="border-blue-200 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-800">
              <CardHeader>
                <CardTitle className="text-lg text-blue-900 dark:text-blue-200">Recommended Actions</CardTitle>
              </CardHeader>
              <CardContent>
                <ol className="space-y-3">
                  <li className="flex items-start gap-2">
                    <Badge variant="default" className="w-6 h-6 flex items-center justify-center p-0">1</Badge>
                    <span className="text-sm text-blue-900 dark:text-blue-200">
                      Address {gapAnalysis?.critical_gaps.filter(g => g.risk_level === 'critical').length} critical gaps immediately
                    </span>
                  </li>
                  <li className="flex items-start gap-2">
                    <Badge variant="default" className="w-6 h-6 flex items-center justify-center p-0">2</Badge>
                    <span className="text-sm text-blue-900 dark:text-blue-200">
                      Implement recommended detection rules for high-priority techniques
                    </span>
                  </li>
                  <li className="flex items-start gap-2">
                    <Badge variant="default" className="w-6 h-6 flex items-center justify-center p-0">3</Badge>
                    <span className="text-sm text-blue-900 dark:text-blue-200">
                      Enhance data source coverage for Defense Evasion and Credential Access tactics
                    </span>
                  </li>
                  <li className="flex items-start gap-2">
                    <Badge variant="default" className="w-6 h-6 flex items-center justify-center p-0">4</Badge>
                    <span className="text-sm text-blue-900 dark:text-blue-200">
                      Conduct threat hunting exercises for undetected APT techniques
                    </span>
                  </li>
                </ol>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
