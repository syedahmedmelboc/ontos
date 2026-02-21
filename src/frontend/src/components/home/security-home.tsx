import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Shield, Lock, RefreshCw, ArrowRight, ShieldCheck, Users } from 'lucide-react';
import { RelativeDate } from '@/components/common/relative-date';

export default function SecurityHome() {
  const [pendingRequests, setPendingRequests] = useState<any[]>([]);
  const [entitlements, setEntitlements] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const didFetch = useRef(false);

  useEffect(() => {
    if (didFetch.current) return;
    didFetch.current = true;

    Promise.allSettled([
      fetch('/api/access-grants/requests/pending').then(r => r.ok ? r.json() : []),
      fetch('/api/entitlements/personas').then(r => r.ok ? r.json() : []),
    ]).then(([requestsData, entitlementsData]) => {
      if (requestsData.status === 'fulfilled') {
        const arr = requestsData.value?.requests ?? (Array.isArray(requestsData.value) ? requestsData.value : []);
        setPendingRequests(arr);
      }
      if (entitlementsData.status === 'fulfilled') {
        setEntitlements(Array.isArray(entitlementsData.value) ? entitlementsData.value : []);
      }
    })
    .catch(e => console.warn('SecurityHome fetch error:', e))
    .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-red-500/10 p-2.5">
                <ShieldCheck className="h-5 w-5 text-red-600 dark:text-red-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Pending Access Requests</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : pendingRequests.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-blue-500/10 p-2.5">
                <Users className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Personas Configured</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : entitlements.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-amber-500/10 p-2.5">
                <Lock className="h-5 w-5 text-amber-600 dark:text-amber-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Security Features</p>
                <p className="text-2xl font-bold">—</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">Pending Access Requests</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-2">{Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-10 w-full" />)}</div>
            ) : pendingRequests.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
                <ShieldCheck className="h-8 w-8 mb-2 opacity-40" />
                <p className="text-sm">No pending access requests</p>
              </div>
            ) : (
              <div className="space-y-3">
                {pendingRequests.slice(0, 8).map((r: any) => (
                  <div key={r.id} className="flex items-center justify-between rounded-md px-3 py-2 -mx-3 border-b last:border-b-0">
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium truncate">{r.entity_name ?? r.entity_id}</p>
                      <p className="text-xs text-muted-foreground">
                        {r.requester_email} &middot; {r.permission_level} &middot; {r.requested_duration_days}d
                      </p>
                    </div>
                    {r.created_at && (
                      <span className="text-xs text-muted-foreground ml-2"><RelativeDate date={r.created_at} /></span>
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
              <Link to="/security/features"><Lock className="h-4 w-4 mr-2" />Security Features</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/security/entitlements"><Shield className="h-4 w-4 mr-2" />Entitlements</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/security/sync"><RefreshCw className="h-4 w-4 mr-2" />Entitlements Sync</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
