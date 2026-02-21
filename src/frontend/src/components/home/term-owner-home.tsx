import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { BookOpen, ClipboardCheck, ArrowRight, Layers } from 'lucide-react';

export default function TermOwnerHome() {
  const [collections, setCollections] = useState<any[]>([]);
  const [reviews, setReviews] = useState<any[]>([]);
  const [conceptCount, setConceptCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const didFetch = useRef(false);

  useEffect(() => {
    if (didFetch.current) return;
    didFetch.current = true;

    Promise.allSettled([
      fetch('/api/knowledge/collections?hierarchical=true').then(r => r.ok ? r.json() : []),
      fetch('/api/data-asset-reviews').then(r => r.ok ? r.json() : []),
      fetch('/api/semantic-models/stats').then(r => r.ok ? r.json() : {}),
    ]).then(([collectionsData, reviewsData, statsData]) => {
      if (collectionsData.status === 'fulfilled') {
        setCollections(Array.isArray(collectionsData.value) ? collectionsData.value : []);
      }
      if (reviewsData.status === 'fulfilled') {
        const arr = Array.isArray(reviewsData.value) ? reviewsData.value : reviewsData.value?.items ?? [];
        setReviews(arr);
      }
      if (statsData.status === 'fulfilled') {
        setConceptCount(statsData.value?.totalTerms ?? statsData.value?.total_terms ?? 0);
      }
    })
    .catch(e => console.warn('TermOwnerHome fetch error:', e))
    .finally(() => setLoading(false));
  }, []);

  const pendingReviews = reviews.filter((r) => r.status === 'queued' || r.status === 'in_review');

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-pink-500/10 p-2.5">
                <Layers className="h-5 w-5 text-pink-600 dark:text-pink-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Glossaries</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : collections.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-blue-500/10 p-2.5">
                <BookOpen className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total Terms</p>
                <p className="text-2xl font-bold">{loading ? <Skeleton className="h-8 w-12" /> : conceptCount}</p>
              </div>
            </div>
          </CardContent>
        </Card>
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
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">Glossaries</CardTitle>
              <Button variant="ghost" size="sm" asChild>
                <Link to="/terms/glossary">View all <ArrowRight className="h-4 w-4 ml-1" /></Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-2">{Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-10 w-full" />)}</div>
            ) : collections.length === 0 ? (
              <p className="text-sm text-muted-foreground py-4 text-center">No glossaries defined yet</p>
            ) : (
              <div className="space-y-3">
                {collections.slice(0, 6).map((c: any) => (
                  <div key={c.id} className="flex items-center justify-between rounded-md px-3 py-2 -mx-3 hover:bg-muted/50 transition-colors">
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium truncate">{c.name ?? c.id}</p>
                      <p className="text-xs text-muted-foreground">{c.source ?? ''}</p>
                    </div>
                    {c.concept_count != null && (
                      <Badge variant="secondary">{c.concept_count} terms</Badge>
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
              <Link to="/terms/glossary"><BookOpen className="h-4 w-4 mr-2" />Browse Terms</Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link to="/terms/requests"><ClipboardCheck className="h-4 w-4 mr-2" />Review Requests</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
