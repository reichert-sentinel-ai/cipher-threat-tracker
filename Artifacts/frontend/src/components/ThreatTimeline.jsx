import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { apiPath } from '../config/api.js';
import {
  ScatterChart, Scatter, LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  Cell, ZAxis
} from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import {
  Loader2, Shield, AlertTriangle, Clock, Users, Target,
  Activity, TrendingUp, Search, Filter, Eye, ChevronRight,
  FileText, Zap, Database
} from 'lucide-react';

const SEVERITY_COLORS = {
  critical: '#dc2626',
  high: '#ea580c',
  medium: '#f59e0b',
  low: '#3b82f6',
  info: '#6b7280'
};

const EVENT_TYPE_ICONS = {
  detection: Shield,
  attack: AlertTriangle,
  ioc: Target,
  mitigation: Zap,
  alert: Activity
};

const getSeverityBadge = (severity) => {
  const variants = {
    critical: 'destructive',
    high: 'destructive',
    medium: 'warning',
    low: 'default',
    info: 'secondary'
  };
  return variants[severity] || 'secondary';
};

export default function ThreatTimeline() {
  const [timelineData, setTimelineData] = useState(null);
  const [attackChain, setAttackChain] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [daysBack, setDaysBack] = useState(30);
  const [severityFilter, setSeverityFilter] = useState('all');
  const [eventTypeFilter, setEventTypeFilter] = useState('all');

  useEffect(() => {
    fetchTimelineData();
  }, [daysBack, severityFilter, eventTypeFilter]);

  const fetchTimelineData = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = {
        days_back: daysBack,
        ...(severityFilter !== 'all' && { severity: severityFilter }),
        ...(eventTypeFilter !== 'all' && { event_type: eventTypeFilter })
      };

      const response = await axios.get(apiPath('threat-timeline/events'), { params });
      if (response.data && response.data.events) {
        setTimelineData(response.data);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (error) {
      console.error('Error fetching timeline data:', error);
      setError(error.message || 'Failed to load timeline data');
      // Set empty data structure to prevent crashes
      setTimelineData({
        total_events: 0,
        date_range: { start: '', end: '' },
        events: [],
        campaigns: [],
        attack_pattern_insights: [],
        trending_threats: []
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchAttackChain = async (campaignId) => {
    try {
      const response = await axios.get(apiPath(`threat-timeline/attack-chain/${campaignId}`));
      setAttackChain(response.data);
    } catch (error) {
      console.error('Error fetching attack chain:', error);
    }
  };

  const viewEventDetails = async (eventId) => {
    try {
      const response = await axios.get(apiPath(`threat-timeline/event-details/${eventId}`));
      setSelectedEvent(response.data);
    } catch (error) {
      console.error('Error fetching event details:', error);
    }
  };

  // Prepare timeline scatter data (must be before conditional returns - Rules of Hooks)
  const timelineScatterData = React.useMemo(() => {
    if (!timelineData || !timelineData.events || !Array.isArray(timelineData.events)) {
      return [];
    }
    return timelineData.events.map((event, idx) => ({
      x: new Date(event.timestamp).getTime(),
      y: ['info', 'low', 'medium', 'high', 'critical'].indexOf(event.severity),
      severity: event.severity,
      title: event.title,
      type: event.event_type,
      status: event.status,
      ...event
    }));
  }, [timelineData]);

  // Prepare trending threats data
  const trendingData = timelineData?.trending_threats || [];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  if (error && !timelineData) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center max-w-md">
          <Alert className="border-red-200 bg-red-50">
            <AlertDescription className="text-red-800">
              <strong>Error:</strong> {error}<br />
              Please check if the backend server is running on port 8000.
            </AlertDescription>
          </Alert>
        </div>
      </div>
    );
  }

  if (!timelineData) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Controls */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2 text-2xl">
                <Activity className="w-6 h-6" />
                Threat Intelligence Timeline
              </CardTitle>
              <p className="text-sm text-gray-500 dark:text-[#a0a0a0] mt-1">
                Real-time visualization of cyber threats, attacks, and security events
              </p>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Time Range */}
            <div>
              <label className="text-sm font-medium mb-2 block">Time Range</label>
              <Select value={daysBack.toString()} onValueChange={(val) => setDaysBack(parseInt(val))}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="7">Last 7 Days</SelectItem>
                  <SelectItem value="30">Last 30 Days</SelectItem>
                  <SelectItem value="60">Last 60 Days</SelectItem>
                  <SelectItem value="90">Last 90 Days</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Severity Filter */}
            <div>
              <label className="text-sm font-medium mb-2 block">Severity</label>
              <Select value={severityFilter} onValueChange={setSeverityFilter}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Severities</SelectItem>
                  <SelectItem value="critical">Critical</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="low">Low</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Event Type Filter */}
            <div>
              <label className="text-sm font-medium mb-2 block">Event Type</label>
              <Select value={eventTypeFilter} onValueChange={setEventTypeFilter}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Types</SelectItem>
                  <SelectItem value="detection">Detections</SelectItem>
                  <SelectItem value="attack">Attacks</SelectItem>
                  <SelectItem value="ioc">IOCs</SelectItem>
                  <SelectItem value="mitigation">Mitigations</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Summary Stats */}
            <div className="flex flex-col justify-center">
              <div className="text-sm text-gray-600 dark:text-[#a0a0a0]">Total Events</div>
              <div className="text-3xl font-bold text-blue-600">
                {timelineData?.total_events}
              </div>
              <div className="text-xs text-gray-500 dark:text-[#a0a0a0]">
                {timelineData?.campaigns.length} campaigns
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Key Insights */}
      <Card className="border-blue-200 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-800">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-blue-900 dark:text-blue-200">
            <TrendingUp className="w-5 h-5" />
            Attack Pattern Insights
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {timelineData?.attack_pattern_insights.map((insight, idx) => (
              <div key={idx} className="flex items-start gap-2 text-sm">
                <div className="w-2 h-2 bg-blue-600 rounded-full mt-1.5" />
                <span className="text-blue-800 dark:text-blue-300">{insight}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Main Tabs */}
      <Tabs defaultValue="timeline" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="timeline">
            <Clock className="w-4 h-4 mr-2" />
            Timeline View
          </TabsTrigger>
          <TabsTrigger value="campaigns">
            <Users className="w-4 h-4 mr-2" />
            Campaigns
          </TabsTrigger>
          <TabsTrigger value="trending">
            <TrendingUp className="w-4 h-4 mr-2" />
            Trending Threats
          </TabsTrigger>
          <TabsTrigger value="killchain">
            <Target className="w-4 h-4 mr-2" />
            Kill Chain
          </TabsTrigger>
        </TabsList>

        {/* Timeline Visualization Tab */}
        <TabsContent value="timeline">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Threat Event Timeline</CardTitle>
              <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                Interactive scatter plot showing threats by time and severity
              </p>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <ScatterChart margin={{ top: 20, right: 20, bottom: 60, left: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="x"
                    type="number"
                    domain={['dataMin', 'dataMax']}
                    tickFormatter={(tick) => new Date(tick).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                    label={{ value: 'Date', position: 'bottom', offset: 40 }}
                  />
                  <YAxis
                    dataKey="y"
                    type="number"
                    domain={[0, 4]}
                    ticks={[0, 1, 2, 3, 4]}
                    tickFormatter={(tick) => ['Info', 'Low', 'Medium', 'High', 'Critical'][tick]}
                    label={{ value: 'Severity', angle: -90, position: 'insideLeft' }}
                  />
                  <ZAxis range={[50, 400]} />
                  <Tooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const data = payload[0].payload;
                        return (
                          <div className="bg-white dark:bg-[#1f1f1f] p-3 border rounded-lg shadow-lg max-w-xs">
                            <div className="flex items-center justify-between mb-2">
                              <Badge variant={getSeverityBadge(data.severity)}>
                                {data.severity.toUpperCase()}
                              </Badge>
                              <span className="text-xs text-gray-500 dark:text-[#a0a0a0]">
                                {new Date(data.timestamp).toLocaleString()}
                              </span>
                            </div>
                            <p className="font-semibold text-sm mb-1">{data.title}</p>
                            <p className="text-xs text-gray-600 dark:text-[#a0a0a0] mb-2">{data.description}</p>
                            {data.threat_actor && (
                              <div className="text-xs">
                                <span className="font-medium">Actor:</span> {data.threat_actor}
                              </div>
                            )}
                            <Button
                              size="sm"
                              variant="outline"
                              className="w-full mt-2"
                              onClick={() => viewEventDetails(data.event_id)}
                            >
                              View Details
                            </Button>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Scatter data={timelineScatterData}>
                    {timelineScatterData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={SEVERITY_COLORS[entry.severity]} />
                    ))}
                  </Scatter>
                </ScatterChart>
              </ResponsiveContainer>

              {/* Recent Events List */}
              <div className="mt-6">
                <h4 className="font-semibold text-sm mb-3">Recent Events</h4>
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {timelineData?.events.slice(0, 15).map((event) => {
                    const IconComponent = EVENT_TYPE_ICONS[event.event_type] || Activity;
                    return (
                      <div
                        key={event.event_id}
                        className="p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-[#1a1a1a] cursor-pointer transition-colors"
                        onClick={() => viewEventDetails(event.event_id)}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex items-start gap-3 flex-1">
                            <div className="p-2 rounded-lg bg-gray-100 dark:bg-[#1a1a1a]">
                              <IconComponent className="w-4 h-4" />
                            </div>
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="font-semibold text-sm">{event.title}</span>
                                <Badge variant={getSeverityBadge(event.severity)} className="text-xs">
                                  {event.severity}
                                </Badge>
                              </div>
                              <p className="text-xs text-gray-600 dark:text-[#a0a0a0] mb-2">{event.description}</p>
                              <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-[#a0a0a0]">
                                <span className="flex items-center gap-1">
                                  <Clock className="w-3 h-3" />
                                  {new Date(event.timestamp).toLocaleString()}
                                </span>
                                {event.threat_actor && (
                                  <span className="flex items-center gap-1">
                                    <Users className="w-3 h-3" />
                                    {event.threat_actor}
                                  </span>
                                )}
                                <Badge variant="outline" className="text-xs">
                                  {event.status}
                                </Badge>
                              </div>
                            </div>
                          </div>
                          <ChevronRight className="w-4 h-4 text-gray-400" />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Campaigns Tab */}
        <TabsContent value="campaigns">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Active Threat Campaigns</CardTitle>
              <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                Coordinated threat actor operations and attack campaigns
              </p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {timelineData?.campaigns.map((campaign) => (
                  <Card key={campaign.campaign_id} className="border-2">
                    <CardContent className="pt-6">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="text-lg font-bold mb-1">{campaign.name}</h3>
                          <div className="flex items-center gap-2">
                            <Badge variant="outline">{campaign.threat_actor}</Badge>
                            <Badge variant={getSeverityBadge(campaign.severity)}>
                              {campaign.severity.toUpperCase()}
                            </Badge>
                          </div>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => fetchAttackChain(campaign.campaign_id)}
                        >
                          View Kill Chain
                        </Button>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                        <div>
                          <div className="text-xs text-gray-600 dark:text-[#a0a0a0]">Start Date</div>
                          <div className="font-semibold">{campaign.start_date}</div>
                        </div>
                        <div>
                          <div className="text-xs text-gray-600 dark:text-[#a0a0a0]">Total Events</div>
                          <div className="font-semibold">{campaign.total_events}</div>
                        </div>
                        <div>
                          <div className="text-xs text-gray-600 dark:text-[#a0a0a0]">Success Rate</div>
                          <div className="font-semibold">{(campaign.success_rate * 100).toFixed(0)}%</div>
                        </div>
                        <div>
                          <div className="text-xs text-gray-600 dark:text-[#a0a0a0]">Status</div>
                          <Badge variant={campaign.end_date ? 'default' : 'destructive'}>
                            {campaign.end_date ? 'Concluded' : 'Ongoing'}
                          </Badge>
                        </div>
                      </div>

                      <div className="space-y-2">
                        <div>
                          <div className="text-xs text-gray-600 dark:text-[#a0a0a0] mb-1">Targeted Sectors</div>
                          <div className="flex gap-2 flex-wrap">
                            {campaign.targeted_sectors.map((sector, idx) => (
                              <Badge key={idx} variant="secondary" className="text-xs">
                                {sector}
                              </Badge>
                            ))}
                          </div>
                        </div>
                        <div>
                          <div className="text-xs text-gray-600 dark:text-[#a0a0a0] mb-1">Attack Vectors</div>
                          <div className="flex gap-2 flex-wrap">
                            {campaign.attack_vectors.map((vector, idx) => (
                              <Badge key={idx} variant="outline" className="text-xs">
                                {vector}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Trending Threats Tab */}
        <TabsContent value="trending">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Trending Threat Vectors</CardTitle>
              <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                Most active attack methods in the current period
              </p>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={trendingData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={120} />
                  <YAxis label={{ value: 'Event Count', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#8b5cf6" />
                </BarChart>
              </ResponsiveContainer>

              <div className="mt-6 space-y-4">
                {trendingData.map((threat, idx) => (
                  <div key={idx} className="p-4 border rounded-lg">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className="text-2xl font-bold text-purple-600">#{idx + 1}</div>
                        <div>
                          <h4 className="font-semibold">{threat.name}</h4>
                          <div className="text-sm text-gray-600 dark:text-[#a0a0a0]">{threat.count} events detected</div>
                        </div>
                      </div>
                      <Badge variant={threat.trend === 'increasing' ? 'destructive' : 'secondary'}>
                        {threat.trend}
                      </Badge>
                    </div>
                    <div className="grid grid-cols-3 gap-3">
                      <div className="text-center p-2 bg-red-50 dark:bg-red-900/20 rounded">
                        <div className="text-xs text-red-600 dark:text-red-400">Critical</div>
                        <div className="text-lg font-bold text-red-700 dark:text-red-300">
                          {threat.severity_distribution.critical}
                        </div>
                      </div>
                      <div className="text-center p-2 bg-orange-50 dark:bg-orange-900/20 rounded">
                        <div className="text-xs text-orange-600 dark:text-orange-400">High</div>
                        <div className="text-lg font-bold text-orange-700 dark:text-orange-300">
                          {threat.severity_distribution.high}
                        </div>
                      </div>
                      <div className="text-center p-2 bg-yellow-50 dark:bg-yellow-900/20 rounded">
                        <div className="text-xs text-yellow-600 dark:text-yellow-400">Medium</div>
                        <div className="text-lg font-bold text-yellow-700 dark:text-yellow-300">
                          {threat.severity_distribution.medium}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Kill Chain Tab */}
        <TabsContent value="killchain">
          {attackChain ? (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">{attackChain.campaign_name} - Attack Chain</CardTitle>
                <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                  Cyber Kill Chain progression: {attackChain.total_duration}
                </p>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {attackChain.stages.map((stage, idx) => (
                    <div key={idx} className="relative">
                      {idx < attackChain.stages.length - 1 && (
                        <div className="absolute left-6 top-12 bottom-0 w-0.5 bg-blue-200 dark:bg-blue-800" />
                      )}
                      <div className="flex items-start gap-4">
                        <div className="flex-shrink-0 w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold z-10">
                          {idx + 1}
                        </div>
                        <div className="flex-1 pb-6">
                          <div className="flex items-center gap-2 mb-2">
                            <h4 className="font-bold text-lg">{stage.stage}</h4>
                            <Badge variant="outline">{stage.mitre_technique}</Badge>
                          </div>
                          <p className="text-sm text-gray-600 dark:text-[#a0a0a0] mb-2">{stage.description}</p>
                          <div className="text-xs text-gray-500 dark:text-[#a0a0a0] mb-2">
                            {new Date(stage.timestamp).toLocaleString()}
                          </div>
                          <div className="space-y-1">
                            {stage.indicators.map((indicator, i) => (
                              <div key={i} className="flex items-center gap-2 text-xs">
                                <Target className="w-3 h-3 text-orange-600" />
                                <span className="text-gray-700 dark:text-[#a0a0a0]">{indicator}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="py-12">
                <div className="text-center text-gray-500 dark:text-[#a0a0a0]">
                  <Target className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                  <p>Select a campaign to view its attack chain progression</p>
                  <Button className="mt-4" onClick={() => fetchAttackChain('camp_001')}>
                    Load Example Campaign
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>

      {/* Event Details Modal (simplified for this example) */}
      {selectedEvent && (
        <Card className="border-2 border-blue-500">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Event Details: {selectedEvent.event_id}</CardTitle>
              <Button variant="outline" size="sm" onClick={() => setSelectedEvent(null)}>
                Close
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Alert>
                <FileText className="h-4 w-4" />
                <AlertDescription>
                  {selectedEvent.full_description}
                </AlertDescription>
              </Alert>
              
              <div>
                <h4 className="font-semibold mb-2">Technical Details</h4>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  {Object.entries(selectedEvent.technical_details).map(([key, value]) => (
                    <div key={key} className="flex justify-between p-2 bg-gray-50 dark:bg-[#1a1a1a] rounded">
                      <span className="text-gray-600 dark:text-[#a0a0a0] capitalize">{key}:</span>
                      <span className="font-semibold">{value}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-semibold mb-2">Response Timeline</h4>
                <div className="space-y-2">
                  {selectedEvent.response_actions.map((action, idx) => (
                    <div key={idx} className="flex items-center gap-3 text-sm">
                      <div className="w-2 h-2 rounded-full bg-green-600" />
                      <span className="text-gray-600 dark:text-[#a0a0a0]">
                        {new Date(action.timestamp).toLocaleTimeString()}
                      </span>
                      <span>{action.action}</span>
                      <Badge variant="outline" className="text-xs">{action.actor}</Badge>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

