import React, { useState, useEffect } from 'react';
import axios from 'axios';
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
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import {
  Loader2, Search, Shield, AlertTriangle, Database, Globe,
  Hash, Mail, Link as LinkIcon, FileText, Copy, Check,
  TrendingUp, Activity, Eye, Download, Upload, Zap, Target
} from 'lucide-react';

const THREAT_LEVEL_COLORS = {
  critical: '#dc2626',
  high: '#ea580c',
  medium: '#f59e0b',
  low: '#3b82f6',
  clean: '#22c55e'
};

const IOC_TYPE_ICONS = {
  ip: Globe,
  domain: LinkIcon,
  hash: Hash,
  email: Mail,
  url: LinkIcon,
  file_path: FileText
};

const getThreatBadge = (level) => {
  const variants = {
    critical: 'destructive',
    high: 'destructive',
    medium: 'warning',
    low: 'default',
    clean: 'default'
  };
  return variants[level] || 'secondary';
};

export default function IOCSearch() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [enrichmentData, setEnrichmentData] = useState(null);
  const [correlationData, setCorrelationData] = useState(null);
  const [feeds, setFeeds] = useState([]);
  const [bulkIOCs, setBulkIOCs] = useState('');
  const [bulkResults, setBulkResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedIOC, setSelectedIOC] = useState(null);
  const [iocTypeFilter, setIocTypeFilter] = useState('all');
  const [threatLevelFilter, setThreatLevelFilter] = useState('all');
  const [copiedIOC, setCopiedIOC] = useState(null);

  useEffect(() => {
    fetchFeeds();
  }, []);

  const fetchFeeds = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/ioc/feeds');
      setFeeds(response.data);
    } catch (error) {
      console.error('Error fetching feeds:', error);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setLoading(true);
    setEnrichmentData(null);
    setCorrelationData(null);
    
    try {
      const params = {
        query: searchQuery,
        ...(iocTypeFilter !== 'all' && { ioc_type: iocTypeFilter }),
        ...(threatLevelFilter !== 'all' && { threat_level: threatLevelFilter })
      };

      const response = await axios.get('http://localhost:8000/api/ioc/search', { params });
      setSearchResults(response.data);
    } catch (error) {
      console.error('Error searching IOCs:', error);
    } finally {
      setLoading(false);
    }
  };

  // Auto-search when filters change (if there's already a search query and results)
  useEffect(() => {
    if (searchQuery.trim() && searchResults) {
      // Only search if we have existing results (avoid initial search)
      const timeoutId = setTimeout(() => {
        handleSearch();
      }, 300); // Debounce by 300ms
      return () => clearTimeout(timeoutId);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [iocTypeFilter, threatLevelFilter]);

  const enrichIOC = async (iocValue) => {
    setLoading(true);
    try {
      const [enrichRes, correlateRes] = await Promise.all([
        axios.get(`http://localhost:8000/api/ioc/enrich/${encodeURIComponent(iocValue)}`),
        axios.get(`http://localhost:8000/api/ioc/correlate/${encodeURIComponent(iocValue)}`)
      ]);
      
      setEnrichmentData(enrichRes.data);
      setCorrelationData(correlateRes.data);
      setSelectedIOC(iocValue);
    } catch (error) {
      console.error('Error enriching IOC:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBulkCheck = async () => {
    if (!bulkIOCs.trim()) return;
    
    setLoading(true);
    try {
      const iocList = bulkIOCs.split('\n').filter(line => line.trim());
      const response = await axios.post('http://localhost:8000/api/ioc/bulk-check', iocList);
      setBulkResults(response.data);
    } catch (error) {
      console.error('Error bulk checking IOCs:', error);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopiedIOC(text);
    setTimeout(() => setCopiedIOC(null), 2000);
  };

  // Prepare reputation chart data
  const reputationData = enrichmentData ? [
    { name: 'Malicious Votes', value: enrichmentData.threat_intelligence.community_votes.malicious, fill: '#dc2626' },
    { name: 'Harmless Votes', value: enrichmentData.threat_intelligence.community_votes.harmless, fill: '#22c55e' }
  ] : [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-2xl">
            <Search className="w-6 h-6" />
            IOC Search & Enrichment
          </CardTitle>
          <p className="text-sm text-gray-500 dark:text-[#a0a0a0] mt-1">
            Search, analyze, and correlate Indicators of Compromise across threat intelligence feeds
          </p>
        </CardHeader>
      </Card>

      {/* Search Interface */}
      <Card>
        <CardContent className="pt-6">
          <div className="space-y-4">
            <div className="flex gap-4">
              <div className="flex-1">
                <Input
                  placeholder="Enter IOC (IP, domain, hash, email, URL)..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  className="text-lg"
                />
              </div>
              <Button onClick={handleSearch} disabled={loading} size="lg">
                {loading ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Search className="w-4 h-4 mr-2" />}
                Search
              </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label className="text-sm">IOC Type</Label>
                <Select value={iocTypeFilter} onValueChange={setIocTypeFilter}>
                  <SelectTrigger className="mt-1">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    <SelectItem value="ip">IP Address</SelectItem>
                    <SelectItem value="domain">Domain</SelectItem>
                    <SelectItem value="hash">File Hash</SelectItem>
                    <SelectItem value="email">Email</SelectItem>
                    <SelectItem value="url">URL</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label className="text-sm">Threat Level</Label>
                <Select value={threatLevelFilter} onValueChange={setThreatLevelFilter}>
                  <SelectTrigger className="mt-1">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Levels</SelectItem>
                    <SelectItem value="critical">Critical</SelectItem>
                    <SelectItem value="high">High</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="low">Low</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Feed Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="w-5 h-5" />
            Threat Intelligence Feeds
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {feeds.map((feed, idx) => (
              <div key={idx} className="p-3 border rounded-lg bg-gray-50 dark:bg-[#1a1a1a]">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold text-sm">{feed.feed_name}</span>
                  <Badge variant="outline" className="text-xs">
                    {feed.feed_reliability}
                  </Badge>
                </div>
                <div className="text-xs text-gray-600 dark:text-[#a0a0a0] space-y-1">
                  <div>Total: {feed.total_iocs.toLocaleString()}</div>
                  <div className="flex items-center gap-1">
                    <Activity className="w-3 h-3 text-blue-600" />
                    New (24h): {feed.new_iocs_24h}
                  </div>
                  <div className="flex items-center gap-1">
                    <AlertTriangle className="w-3 h-3 text-red-600" />
                    Critical: {feed.critical_iocs}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Main Content Tabs */}
      <Tabs defaultValue="search" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="search">
            <Search className="w-4 h-4 mr-2" />
            Search Results
          </TabsTrigger>
          <TabsTrigger value="enrichment" disabled={!enrichmentData}>
            <Zap className="w-4 h-4 mr-2" />
            Enrichment
          </TabsTrigger>
          <TabsTrigger value="bulk">
            <Upload className="w-4 h-4 mr-2" />
            Bulk Check
          </TabsTrigger>
        </TabsList>

        {/* Search Results Tab */}
        <TabsContent value="search">
          {searchResults ? (
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-lg">Search Results</CardTitle>
                    <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                      Found {searchResults.total_results} IOCs in {searchResults.search_time_ms}ms
                    </p>
                  </div>
                  <Button variant="outline" size="sm">
                    <Download className="w-4 h-4 mr-2" />
                    Export
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {searchResults.iocs.map((ioc) => {
                    const IconComponent = IOC_TYPE_ICONS[ioc.type] || Target;
                    return (
                      <div
                        key={ioc.ioc_id}
                        className="p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-[#1a1a1a] cursor-pointer transition-colors"
                        onClick={() => enrichIOC(ioc.value)}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex items-start gap-3 flex-1">
                            <div className="p-2 rounded-lg bg-gray-100 dark:bg-[#2a2a2a]">
                              <IconComponent className="w-5 h-5" />
                            </div>
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-2">
                                <span className="font-mono font-semibold">{ioc.value}</span>
                                <Badge variant="outline" className="text-xs">
                                  {ioc.type}
                                </Badge>
                                <Badge variant={getThreatBadge(ioc.threat_level)}>
                                  {ioc.threat_level}
                                </Badge>
                                <div className="flex items-center gap-1 text-xs text-gray-600 dark:text-[#a0a0a0]">
                                  <Shield className="w-3 h-3" />
                                  {(ioc.confidence * 100).toFixed(0)}% confidence
                                </div>
                              </div>
                              
                              <p className="text-sm text-gray-600 dark:text-[#a0a0a0] mb-2">{ioc.description}</p>
                              
                              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                                <div>
                                  <span className="text-gray-500 dark:text-[#6a6a6a]">First Seen:</span>
                                  <div className="font-semibold">
                                    {new Date(ioc.first_seen).toLocaleDateString()}
                                  </div>
                                </div>
                                <div>
                                  <span className="text-gray-500 dark:text-[#6a6a6a]">Last Seen:</span>
                                  <div className="font-semibold">
                                    {new Date(ioc.last_seen).toLocaleDateString()}
                                  </div>
                                </div>
                                <div>
                                  <span className="text-gray-500 dark:text-[#6a6a6a]">Sources:</span>
                                  <div className="font-semibold">{ioc.sources.length}</div>
                                </div>
                                <div>
                                  <span className="text-gray-500 dark:text-[#6a6a6a]">Campaigns:</span>
                                  <div className="font-semibold">{ioc.campaigns.length}</div>
                                </div>
                              </div>

                              <div className="mt-3 flex gap-2 flex-wrap">
                                {ioc.tags.map((tag, idx) => (
                                  <Badge key={idx} variant="secondary" className="text-xs">
                                    {tag}
                                  </Badge>
                                ))}
                              </div>

                              {ioc.threat_actors.length > 0 && (
                                <div className="mt-2 text-xs">
                                  <span className="text-gray-600 dark:text-[#a0a0a0]">Threat Actors: </span>
                                  <span className="font-semibold">{ioc.threat_actors.join(', ')}</span>
                                </div>
                              )}

                              {ioc.malware_families.length > 0 && (
                                <div className="text-xs">
                                  <span className="text-gray-600 dark:text-[#a0a0a0]">Malware: </span>
                                  <span className="font-semibold">{ioc.malware_families.join(', ')}</span>
                                </div>
                              )}
                            </div>
                          </div>
                          
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={(e) => {
                              e.stopPropagation();
                              copyToClipboard(ioc.value);
                            }}
                          >
                            {copiedIOC === ioc.value ? (
                              <Check className="w-4 h-4" />
                            ) : (
                              <Copy className="w-4 h-4" />
                            )}
                          </Button>
                        </div>
                      </div>
                    );
                  })}
                </div>

                {searchResults.iocs.length === 0 && (
                  <div className="text-center py-12 text-gray-500 dark:text-[#a0a0a0]">
                    <Search className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                    <p>No IOCs found matching your search criteria</p>
                  </div>
                )}
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="py-12">
                <div className="text-center text-gray-500 dark:text-[#a0a0a0]">
                  <Search className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                  <p>Enter an IOC above to search threat intelligence feeds</p>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Enrichment Tab */}
        <TabsContent value="enrichment">
          {enrichmentData && (
            <div className="space-y-6">
              {/* IOC Overview */}
              <Card className="border-2" style={{ borderColor: THREAT_LEVEL_COLORS[enrichmentData.threat_intelligence.verdict === 'malicious' ? 'critical' : 'medium'] }}>
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h2 className="text-2xl font-bold font-mono">{selectedIOC}</h2>
                        <Badge variant="outline" className="text-sm">
                          {enrichmentData.ioc_type}
                        </Badge>
                      </div>
                      <div className="flex items-center gap-4">
                        <Badge 
                          variant={enrichmentData.threat_intelligence.verdict === 'malicious' ? 'destructive' : 'warning'}
                          className="text-lg px-4 py-1"
                        >
                          {enrichmentData.threat_intelligence.verdict.toUpperCase()}
                        </Badge>
                        <div className="text-sm">
                          <span className="text-gray-600 dark:text-[#a0a0a0]">Reputation Score: </span>
                          <span 
                            className="text-2xl font-bold"
                            style={{ color: enrichmentData.reputation_score < 30 ? '#dc2626' : '#f59e0b' }}
                          >
                            {enrichmentData.reputation_score}/100
                          </span>
                        </div>
                      </div>
                    </div>
                    <Button
                      variant="outline"
                      onClick={() => copyToClipboard(selectedIOC)}
                    >
                      {copiedIOC === selectedIOC ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                    </Button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-3 bg-gray-50 dark:bg-[#1a1a1a] rounded-lg">
                      <div className="text-sm text-gray-600 dark:text-[#a0a0a0] mb-1">Detection Rate</div>
                      <div className="text-2xl font-bold">
                        {enrichmentData.threat_intelligence.detections.positive_detections}/
                        {enrichmentData.threat_intelligence.detections.total_engines}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-[#6a6a6a]">
                        {enrichmentData.threat_intelligence.detections.detection_rate}
                      </div>
                    </div>
                    <div className="p-3 bg-gray-50 dark:bg-[#1a1a1a] rounded-lg">
                      <div className="text-sm text-gray-600 dark:text-[#a0a0a0] mb-1">Community Votes</div>
                      <div className="flex gap-2">
                        <div>
                          <div className="text-lg font-bold text-red-600">
                            {enrichmentData.threat_intelligence.community_votes.malicious}
                          </div>
                          <div className="text-xs text-gray-500 dark:text-[#6a6a6a]">Malicious</div>
                        </div>
                        <div className="text-2xl text-gray-300">/</div>
                        <div>
                          <div className="text-lg font-bold text-green-600">
                            {enrichmentData.threat_intelligence.community_votes.harmless}
                          </div>
                          <div className="text-xs text-gray-500 dark:text-[#6a6a6a]">Harmless</div>
                        </div>
                      </div>
                    </div>
                    <div className="p-3 bg-gray-50 dark:bg-[#1a1a1a] rounded-lg">
                      <div className="text-sm text-gray-600 dark:text-[#a0a0a0] mb-1">Last Analysis</div>
                      <div className="text-lg font-bold">
                        {new Date(enrichmentData.threat_intelligence.last_analysis_date).toLocaleString()}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Enrichment Details */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Community Votes Pie Chart */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Community Assessment</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={250}>
                      <PieChart>
                        <Pie
                          data={reputationData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, value }) => `${name}: ${value}`}
                          outerRadius={80}
                          dataKey="value"
                        >
                          {reputationData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.fill} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>

                {/* Geolocation */}
                {enrichmentData.geolocation && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg flex items-center gap-2">
                        <Globe className="w-5 h-5" />
                        Geolocation
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        {Object.entries(enrichmentData.geolocation).map(([key, value]) => (
                          <div key={key} className="flex justify-between p-2 bg-gray-50 dark:bg-[#1a1a1a] rounded">
                            <span className="text-gray-600 dark:text-[#a0a0a0] capitalize">{key.replace('_', ' ')}:</span>
                            <span className="font-semibold">{value}</span>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* WHOIS Data */}
                {enrichmentData.whois_data && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">WHOIS Information</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2 text-sm">
                        {Object.entries(enrichmentData.whois_data).map(([key, value]) => (
                          <div key={key} className="flex justify-between">
                            <span className="text-gray-600 dark:text-[#a0a0a0] capitalize">{key.replace('_', ' ')}:</span>
                            <span className="font-semibold">{Array.isArray(value) ? value.join(', ') : value}</span>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Malware Analysis */}
                {enrichmentData.malware_analysis && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Malware Analysis</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div className="grid grid-cols-2 gap-3 text-sm">
                          <div>
                            <span className="text-gray-600 dark:text-[#a0a0a0]">Family:</span>
                            <div className="font-semibold">{enrichmentData.malware_analysis.malware_family}</div>
                          </div>
                          <div>
                            <span className="text-gray-600 dark:text-[#a0a0a0]">File Type:</span>
                            <div className="font-semibold">{enrichmentData.malware_analysis.file_type}</div>
                          </div>
                        </div>

                        <div>
                          <div className="text-sm font-semibold mb-2">Observed Behaviors:</div>
                          <div className="space-y-1">
                            {enrichmentData.malware_analysis.behaviors.map((behavior, idx) => (
                              <div key={idx} className="flex items-center gap-2 text-sm">
                                <AlertTriangle className="w-3 h-3 text-red-600" />
                                <span>{behavior}</span>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div>
                          <div className="text-sm font-semibold mb-2">MITRE ATT&CK Techniques:</div>
                          <div className="flex gap-2 flex-wrap">
                            {enrichmentData.malware_analysis.mitre_techniques.map((technique, idx) => (
                              <Badge key={idx} variant="destructive" className="text-xs">
                                {technique}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>

              {/* Related IOCs */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Related IOCs</CardTitle>
                  <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                    Correlated indicators from the same threat infrastructure
                  </p>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {enrichmentData.related_iocs.map((relatedIOC, idx) => (
                      <div key={idx} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-[#1a1a1a]">
                        <span className="font-mono text-sm">{relatedIOC}</span>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => enrichIOC(relatedIOC.split(':')[1])}
                        >
                          <Eye className="w-4 h-4" />
                        </Button>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Correlation Analysis */}
              {correlationData && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <Target className="w-5 h-5" />
                      Correlation Analysis
                    </CardTitle>
                    <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                      Infrastructure and campaign relationships
                    </p>
                  </CardHeader>
                  <CardContent>
                    <div className="mb-4 p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-semibold">Overall Correlation Score</span>
                        <Badge variant="default" className="text-lg px-3">
                          {(correlationData.correlation_score * 100).toFixed(0)}%
                        </Badge>
                      </div>
                      <div className="text-sm text-purple-800 dark:text-purple-200">
                        Relationship Type: <span className="font-semibold capitalize">{correlationData.relationship_type.replace('_', ' ')}</span>
                      </div>
                    </div>

                    <div className="space-y-3">
                      {correlationData.related_iocs.map((related, idx) => (
                        <div key={idx} className="p-3 border rounded-lg">
                          <div className="flex items-center justify-between mb-2">
                            <span className="font-mono font-semibold">{related.ioc_value}</span>
                            <Badge variant="outline">{related.ioc_type}</Badge>
                          </div>
                          <div className="text-sm space-y-1">
                            <div className="flex items-center gap-2">
                              <span className="text-gray-600 dark:text-[#a0a0a0]">Relationship:</span>
                              <Badge variant="secondary" className="text-xs capitalize">
                                {related.relationship.replace('_', ' ')}
                              </Badge>
                            </div>
                            <div className="flex items-center gap-2">
                              <span className="text-gray-600 dark:text-[#a0a0a0]">Score:</span>
                              <span className="font-semibold">{(related.correlation_score * 100).toFixed(0)}%</span>
                            </div>
                            <div>
                              <span className="text-gray-600 dark:text-[#a0a0a0]">Shared Attributes:</span>
                              <div className="flex gap-2 mt-1">
                                {related.shared_attributes.map((attr, i) => (
                                  <Badge key={i} variant="outline" className="text-xs">
                                    {attr}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Detection Rules */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Detection Rules</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {enrichmentData.detection_rules.map((rule, idx) => (
                      <div key={idx} className="p-3 bg-gray-50 dark:bg-[#1a1a1a] rounded-lg font-mono text-xs">
                        {rule}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Recommendations */}
              <Card className="border-orange-200 dark:border-orange-800 bg-orange-50 dark:bg-orange-900/20">
                <CardHeader>
                  <CardTitle className="text-lg text-orange-900 dark:text-orange-200 flex items-center gap-2">
                    <Shield className="w-5 h-5" />
                    Security Recommendations
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {enrichmentData.recommendations.map((rec, idx) => (
                      <Alert key={idx} className="border-orange-200 dark:border-orange-800" variant="warning">
                        <AlertDescription className="text-sm text-orange-900 dark:text-orange-200">
                          {rec}
                        </AlertDescription>
                      </Alert>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </TabsContent>

        {/* Bulk Check Tab */}
        <TabsContent value="bulk">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Bulk IOC Check</CardTitle>
              <p className="text-sm text-gray-500 dark:text-[#a0a0a0]">
                Check multiple IOCs simultaneously (up to 100)
              </p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <Label className="text-sm">Enter IOCs (one per line)</Label>
                  <Textarea
                    placeholder="185.220.101.45&#10;malicious-domain.com&#10;a1b2c3d4e5f6..."
                    value={bulkIOCs}
                    onChange={(e) => setBulkIOCs(e.target.value)}
                    rows={10}
                    className="mt-2 font-mono"
                  />
                </div>

                <Button onClick={handleBulkCheck} disabled={loading} className="w-full">
                  {loading ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Upload className="w-4 h-4 mr-2" />}
                  Check All IOCs
                </Button>

                {bulkResults && (
                  <div className="mt-6 space-y-4">
                    <div className="grid grid-cols-4 gap-4">
                      <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg text-center">
                        <div className="text-2xl font-bold text-blue-600">{bulkResults.total_checked}</div>
                        <div className="text-sm text-blue-800 dark:text-blue-200">Total Checked</div>
                      </div>
                      <div className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg text-center">
                        <div className="text-2xl font-bold text-red-600">{bulkResults.malicious_count}</div>
                        <div className="text-sm text-red-800 dark:text-red-200">Malicious</div>
                      </div>
                      <div className="p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg text-center">
                        <div className="text-2xl font-bold text-orange-600">{bulkResults.suspicious_count}</div>
                        <div className="text-sm text-orange-800 dark:text-orange-200">Suspicious</div>
                      </div>
                      <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg text-center">
                        <div className="text-2xl font-bold text-green-600">{bulkResults.clean_count}</div>
                        <div className="text-sm text-green-800 dark:text-green-200">Clean</div>
                      </div>
                    </div>

                    <div>
                      <h4 className="font-semibold mb-3">Detailed Results</h4>
                      <div className="space-y-2 max-h-96 overflow-y-auto">
                        {bulkResults.results.map((result, idx) => (
                          <div key={idx} className="flex items-center justify-between p-3 border rounded-lg">
                            <div className="flex items-center gap-3 flex-1">
                              <Badge variant="outline">{result.type}</Badge>
                              <span className="font-mono text-sm">{result.ioc}</span>
                            </div>
                            <div className="flex items-center gap-3">
                              <Badge variant={getThreatBadge(result.threat_level)}>
                                {result.threat_level}
                              </Badge>
                              <span className="text-xs text-gray-600 dark:text-[#a0a0a0]">
                                {result.found_in_feeds} feeds
                              </span>
                              {result.confidence > 0 && (
                                <span className="text-xs text-gray-600 dark:text-[#a0a0a0]">
                                  {(result.confidence * 100).toFixed(0)}% conf.
                                </span>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

