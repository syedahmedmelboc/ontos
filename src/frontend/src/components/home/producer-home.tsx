import { useState, useEffect, useMemo, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Package, FileText, Plus, ArrowRight } from 'lucide-react';
import { RelativeDate } from '@/components/common/relative-date';
import type { DataProduct } from '@/types/data-product';

const STATUS_COLORS: Record<string, string> = {
  draft: 'bg-gray-500',
  active: 'bg-green-500',
  approved: 'bg-blue-500',
  deprecated: 'bg-amber-500',
  retired: 'bg-red-500',
};

export default function ProducerHome() {
  const [products, setProducts] = useState<DataProduct[]>([]);
  const [contracts, setContracts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const didFetch = useRef(false);

  useEffect(() => {
    if (didFetch.current) return;
    didFetch.current = true;

    Promise.all([
      fetch('/api/data-products').then(r => r.ok ? r.json() : []),
      fetch('/api/data-contracts').then(r => r.ok ? r.json() : []),
    ])
      .then(([prods, ctrs]) => {
        setProducts(Array.isArray(prods) ? prods : []);
        setContracts(Array.isArray(ctrs) ? ctrs : []);
      })
      .catch(e => console.warn('ProducerHome fetch error:', e))
      .finally(() => setLoading(false));
  }, []);

  const statusCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    products.forEach((p) => {
      const s = p.status ?? 'draft';
      counts[s] = (counts[s] ?? 0) + 1;
    });
    return counts;
  }, [products]);

  const recentProducts = useMemo(
    () => [...products].sort((a, b) =>
      new Date(b.productCreatedTs ?? 0).getTime() - new Date(a.productCreatedTs ?? 0).getTime()
    ).slice(0, 5),
    [products]
  );

  return (
    <div className="space-y-6">
      {/* Stat cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-emerald-500/10 p-2.5">
                <Package className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Data Products</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : products.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-blue-500/10 p-2.5">
                <FileText className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Data Contracts</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : contracts.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-amber-500/10 p-2.5">
                <Package className="h-5 w-5 text-amber-600 dark:text-amber-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Draft Products</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : (statusCounts['draft'] ?? 0)}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Products by status */}
        <Card className="lg:col-span-2">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">Products by Status</CardTitle>
              <Button variant="ghost" size="sm" asChild>
                <Link to="/producer/products">View all <ArrowRight className="h-4 w-4 ml-1" /></Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-2">{Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-8 w-full" />)}</div>
            ) : Object.keys(statusCounts).length === 0 ? (
              <p className="text-sm text-muted-foreground py-4 text-center">No products yet</p>
            ) : (
              <div className="space-y-3">
                {Object.entries(statusCounts).sort(([, a], [, b]) => b - a).map(([status, count]) => (
                  <div key={status} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className={`h-2.5 w-2.5 rounded-full ${STATUS_COLORS[status] ?? 'bg-gray-400'}`} />
                      <span className="text-sm font-medium capitalize">{status.replace('_', ' ')}</span>
                    </div>
                    <Badge variant="secondary">{count}</Badge>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Quick actions */}
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/producer/products"><Plus className="h-4 w-4 mr-2" />Create Data Product</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/producer/contracts"><Plus className="h-4 w-4 mr-2" />Define Data Contract</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/producer/datasets"><Package className="h-4 w-4 mr-2" />Browse Assets</Link>
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Recent products */}
      {!loading && recentProducts.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Recent Products</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {recentProducts.map((p) => (
                <Link key={p.id} to={`/producer/products/${p.id}`} className="flex items-center justify-between hover:bg-muted/50 rounded-md px-3 py-2 -mx-3 transition-colors">
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium truncate">{p.name ?? p.id}</p>
                    <p className="text-xs text-muted-foreground">{p.domain ?? 'No domain'}</p>
                  </div>
                  <div className="flex items-center gap-2 ml-3">
                    <Badge variant="outline" className="capitalize">{p.status}</Badge>
                    {p.productCreatedTs && <span className="text-xs text-muted-foreground"><RelativeDate date={p.productCreatedTs} /></span>}
                  </div>
                </Link>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
