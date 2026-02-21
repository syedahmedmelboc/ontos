import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Settings, ScrollText, Briefcase, ArrowRight, Shield, Users2, Search, Info } from 'lucide-react';
import { RelativeDate } from '@/components/common/relative-date';

export default function AdminHome() {
  const [roles, setRoles] = useState<any[]>([]);
  const [auditEntries, setAuditEntries] = useState<any[]>([]);
  const [jobCount, setJobCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const didFetch = useRef(false);

  useEffect(() => {
    if (didFetch.current) return;
    didFetch.current = true;

    Promise.allSettled([
      fetch('/api/settings/roles').then(r => r.ok ? r.json() : []),
      fetch('/api/audit?limit=5').then(r => r.ok ? r.json() : []),
      fetch('/api/settings/jobs').then(r => r.ok ? r.json() : []),
    ]).then(([rolesData, auditData, jobsData]) => {
      if (rolesData.status === 'fulfilled') {
        setRoles(Array.isArray(rolesData.value) ? rolesData.value : []);
      }
      if (auditData.status === 'fulfilled') {
        const entries = auditData.value?.items ?? (Array.isArray(auditData.value) ? auditData.value : []);
        setAuditEntries(entries.slice(0, 5));
      }
      if (jobsData.status === 'fulfilled') {
        const jobs = Array.isArray(jobsData.value) ? jobsData.value : jobsData.value?.jobs ?? [];
        setJobCount(jobs.length);
      }
    })
    .catch(e => console.warn('AdminHome fetch error:', e))
    .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-slate-500/10 p-2.5">
                <Shield className="h-5 w-5 text-slate-600 dark:text-slate-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">App Roles</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : roles.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-blue-500/10 p-2.5">
                <Briefcase className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Background Jobs</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : jobCount}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-amber-500/10 p-2.5">
                <ScrollText className="h-5 w-5 text-amber-600 dark:text-amber-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Audit Trail</p>
                <p className="text-2xl font-bold">
                  {loading ? <Skeleton className="h-8 w-12" /> : auditEntries.length > 0 ? 'Active' : '—'}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-green-500/10 p-2.5">
                <Settings className="h-5 w-5 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">System Status</p>
                <p className="text-2xl font-bold text-green-600 dark:text-green-400">OK</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">Recent Audit Activity</CardTitle>
              <Button variant="ghost" size="sm" asChild>
                <Link to="/admin/audit">View all <ArrowRight className="h-4 w-4 ml-1" /></Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-2">{Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-10 w-full" />)}</div>
            ) : auditEntries.length === 0 ? (
              <p className="text-sm text-muted-foreground py-4 text-center">No audit entries yet</p>
            ) : (
              <div className="space-y-3">
                {auditEntries.map((entry: any, idx: number) => (
                  <div key={entry.id ?? idx} className="flex items-center justify-between rounded-md px-3 py-2 -mx-3 border-b last:border-b-0">
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium truncate">{entry.action ?? entry.event_type ?? 'Event'}</p>
                      <p className="text-xs text-muted-foreground">
                        {entry.user_email ?? entry.actor ?? 'System'}
                        {entry.entity_type && <> &middot; {entry.entity_type}</>}
                      </p>
                    </div>
                    {entry.created_at && (
                      <span className="text-xs text-muted-foreground ml-2"><RelativeDate date={entry.created_at} /></span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/admin/general"><Settings className="h-4 w-4 mr-2" />General Settings</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/admin/roles"><Shield className="h-4 w-4 mr-2" />App Roles</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/admin/jobs"><Briefcase className="h-4 w-4 mr-2" />Background Jobs</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/admin/business-roles"><Users2 className="h-4 w-4 mr-2" />Business Roles</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/admin/search"><Search className="h-4 w-4 mr-2" />Search Settings</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/admin/about"><Info className="h-4 w-4 mr-2" />About</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
