import { useState, useEffect, useMemo, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Package, Users, CheckCircle, ArrowRight, TrendingUp } from 'lucide-react';
import type { DataProduct } from '@/types/data-product';

export default function OwnerHome() {
  const [products, setProducts] = useState<DataProduct[]>([]);
  const [subscriberCounts, setSubscriberCounts] = useState<Record<string, number>>({});
  const [compliance, setCompliance] = useState<{ score?: number } | null>(null);
  const [loading, setLoading] = useState(true);
  const didFetch = useRef(false);

  useEffect(() => {
    if (didFetch.current) return;
    didFetch.current = true;

    (async () => {
      try {
        const prodsResp = await fetch('/api/data-products');
        const productList: DataProduct[] = prodsResp.ok ? await prodsResp.json() : [];
        setProducts(Array.isArray(productList) ? productList : []);

        const counts: Record<string, number> = {};
        await Promise.all(
          (Array.isArray(productList) ? productList : []).slice(0, 20).map(async (p) => {
            try {
              const resp = await fetch(`/api/data-products/${p.id}/subscriber-count`);
              const data = resp.ok ? await resp.json() : {};
              counts[p.id] = data?.subscriber_count ?? 0;
            } catch { counts[p.id] = 0; }
          })
        );
        setSubscriberCounts(counts);

        try {
          const trendResp = await fetch('/api/compliance/trend');
          const trend = trendResp.ok ? await trendResp.json() : [];
          const latest = Array.isArray(trend) && trend.length > 0 ? trend[trend.length - 1] : null;
          setCompliance(latest ? { score: latest.score } : null);
        } catch { /* compliance optional */ }
      } catch (e) {
        console.warn('OwnerHome fetch error:', e);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const totalSubscribers = useMemo(
    () => Object.values(subscriberCounts).reduce((s, c) => s + c, 0),
    [subscriberCounts]
  );

  const activeProducts = products.filter((p) => ['active', 'approved', 'certified'].includes(p.status));

  const topProducts = useMemo(
    () => [...products].sort((a, b) => (subscriberCounts[b.id] ?? 0) - (subscriberCounts[a.id] ?? 0)).slice(0, 5),
    [products, subscriberCounts]
  );

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-orange-500/10 p-2.5">
                <Package className="h-5 w-5 text-orange-600 dark:text-orange-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">My Products</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : products.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-green-500/10 p-2.5">
                <CheckCircle className="h-5 w-5 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Active</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : activeProducts.length}</p>
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
                <p className="text-sm text-muted-foreground">Total Subscribers</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : totalSubscribers}</p>
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
                <p className="text-sm text-muted-foreground">Compliance</p>
                <p className="text-2xl font-bold">
                  {loading ? <Skeleton className="h-8 w-12" /> : compliance?.score != null ? `${Math.round(compliance.score)}%` : '—'}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">Top Products by Subscribers</CardTitle>
              <Button variant="ghost" size="sm" asChild>
                <Link to="/owner/consumers">View all <ArrowRight className="h-4 w-4 ml-1" /></Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-2">{Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-10 w-full" />)}</div>
            ) : topProducts.length === 0 ? (
              <p className="text-sm text-muted-foreground py-4 text-center">No products yet</p>
            ) : (
              <div className="space-y-3">
                {topProducts.map((p) => (
                  <Link key={p.id} to={`/owner/products/${p.id}`} className="flex items-center justify-between hover:bg-muted/50 rounded-md px-3 py-2 -mx-3 transition-colors">
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium truncate">{p.name ?? p.id}</p>
                      <p className="text-xs text-muted-foreground">{p.domain ?? 'No domain'}</p>
                    </div>
                    <Badge variant="secondary">
                      <Users className="h-3 w-3 mr-1" />
                      {subscriberCounts[p.id] ?? 0}
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
              <Link to="/owner/products"><Package className="h-4 w-4 mr-2" />Manage Products</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/owner/contracts"><Package className="h-4 w-4 mr-2" />View Contracts</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/owner/consumers"><Users className="h-4 w-4 mr-2" />View Consumers</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/owner/health"><CheckCircle className="h-4 w-4 mr-2" />Product Health</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
