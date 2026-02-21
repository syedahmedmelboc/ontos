import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { ClipboardCheck, CheckCircle, Box, ArrowRight, TrendingUp, Database } from 'lucide-react';
import { RelativeDate } from '@/components/common/relative-date';

export default function StewardHome() {
  const [reviews, setReviews] = useState<any[]>([]);
  const [compliance, setCompliance] = useState<{ score?: number } | null>(null);
  const [assetCount, setAssetCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const didFetch = useRef(false);

  useEffect(() => {
    if (didFetch.current) return;
    didFetch.current = true;

    Promise.allSettled([
      fetch('/api/data-asset-reviews').then(r => r.ok ? r.json() : []),
      fetch('/api/compliance/trend').then(r => r.ok ? r.json() : []),
      fetch('/api/assets?limit=1').then(r => r.ok ? r.json() : {}),
    ]).then(([reviewsData, trendData, assetsData]) => {
      if (reviewsData.status === 'fulfilled') {
        const arr = Array.isArray(reviewsData.value) ? reviewsData.value : reviewsData.value?.items ?? [];
        setReviews(arr);
      }
      if (trendData.status === 'fulfilled') {
        const trend = Array.isArray(trendData.value) ? trendData.value : [];
        const latest = trend.length > 0 ? trend[trend.length - 1] : null;
        setCompliance(latest ? { score: latest.score } : null);
      }
      if (assetsData.status === 'fulfilled') {
        setAssetCount(assetsData.value?.total ?? assetsData.value?.length ?? 0);
      }
    })
    .catch(e => console.warn('StewardHome fetch error:', e))
    .finally(() => setLoading(false));
  }, []);

  const pendingReviews = reviews.filter((r) => r.status === 'queued' || r.status === 'in_review');
  const recentReviews = [...reviews].sort((a, b) =>
    new Date(b.created_at ?? 0).getTime() - new Date(a.created_at ?? 0).getTime()
  ).slice(0, 5);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-amber-500/10 p-2.5">
                <ClipboardCheck className="h-5 w-5 text-amber-600 dark:text-amber-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Pending Reviews</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : pendingReviews.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-blue-500/10 p-2.5">
                <ClipboardCheck className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total Reviews</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : reviews.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-purple-500/10 p-2.5">
                <TrendingUp className="h-5 w-5 text-purple-600 dark:text-purple-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Compliance Score</p>
                <p className="text-2xl font-bold">
                  {loading ? <Skeleton className="h-8 w-12" /> : compliance?.score != null ? `${Math.round(compliance.score)}%` : '—'}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-green-500/10 p-2.5">
                <Box className="h-5 w-5 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Managed Assets</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : assetCount}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">Recent Reviews</CardTitle>
              <Button variant="ghost" size="sm" asChild>
                <Link to="/steward/reviews">View all <ArrowRight className="h-4 w-4 ml-1" /></Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-2">{Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-10 w-full" />)}</div>
            ) : recentReviews.length === 0 ? (
              <p className="text-sm text-muted-foreground py-4 text-center">No reviews yet</p>
            ) : (
              <div className="space-y-3">
                {recentReviews.map((r) => (
                  <Link key={r.id} to={`/steward/reviews/${r.id}`} className="flex items-center justify-between hover:bg-muted/50 rounded-md px-3 py-2 -mx-3 transition-colors">
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium truncate">{r.title ?? r.id}</p>
                      <p className="text-xs text-muted-foreground">
                        {r.requester_email ?? 'Unknown requester'}
                        {r.created_at && <> &middot; <RelativeDate date={r.created_at} /></>}
                      </p>
                    </div>
                    <Badge variant={r.status === 'approved' ? 'default' : r.status === 'denied' ? 'destructive' : 'secondary'} className="capitalize">
                      {r.status?.replace('_', ' ')}
                    </Badge>
                  </Link>
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
              <Link to="/steward/reviews"><ClipboardCheck className="h-4 w-4 mr-2" />Review Assets</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/steward/assets"><Box className="h-4 w-4 mr-2" />Asset Explorer</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/steward/compliance"><CheckCircle className="h-4 w-4 mr-2" />Compliance Checks</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/steward/commander"><Database className="h-4 w-4 mr-2" />Catalog Commander</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
