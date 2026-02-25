import { useState, useCallback, useEffect, useRef } from 'react';
import {
  ChevronRight,
  ChevronDown,
  Loader2,
  Database,
  Table2,
  Eye,
  Columns3,
  Box,
  FolderOpen,
  Braces,
} from 'lucide-react';
import { Checkbox } from '@/components/ui/checkbox';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useApi } from '@/hooks/use-api';
import type { BrowseNode } from '@/types/schema-import';

interface TreeNode extends BrowseNode {
  children?: TreeNode[];
  isExpanded: boolean;
  isLoading: boolean;
  level: number;
}

interface SchemaBrowserProps {
  connectionId: string | null;
  selectedPaths: Set<string>;
  onSelectionChange: (paths: Set<string>) => void;
}

const nodeIconMap: Record<string, typeof Database> = {
  catalog: Database,
  schema: FolderOpen,
  dataset: FolderOpen,
  database: Database,
  project: Database,
  table: Table2,
  view: Eye,
  column: Columns3,
  routine: Braces,
  model: Box,
};

function getNodeIcon(nodeType: string) {
  const Icon = nodeIconMap[nodeType.toLowerCase()] || Box;
  return <Icon className="h-4 w-4 shrink-0 text-muted-foreground" />;
}

export default function SchemaBrowser({
  connectionId,
  selectedPaths,
  onSelectionChange,
}: SchemaBrowserProps) {
  const { get: apiGet } = useApi();
  const [roots, setRoots] = useState<TreeNode[]>([]);
  const [isInitialLoading, setIsInitialLoading] = useState(false);
  const apiGetRef = useRef(apiGet);
  apiGetRef.current = apiGet;

  const loadChildren = useCallback(
    async (connId: string, path: string | null): Promise<TreeNode[]> => {
      const url = path
        ? `/api/schema-import/browse/${connId}?path=${encodeURIComponent(path)}`
        : `/api/schema-import/browse/${connId}`;
      const resp = await apiGetRef.current<{ nodes: BrowseNode[] }>(url);
      if (!resp.data?.nodes) return [];
      return resp.data.nodes.map((n) => ({
        ...n,
        children: undefined,
        isExpanded: false,
        isLoading: false,
        level: path ? path.split('.').length : 0,
      }));
    },
    [],
  );

  // Load root nodes when connectionId changes
  useEffect(() => {
    if (!connectionId) {
      setRoots([]);
      return;
    }
    let cancelled = false;
    setIsInitialLoading(true);
    loadChildren(connectionId, null)
      .then((nodes) => {
        if (!cancelled) setRoots(nodes);
      })
      .catch((err) => {
        if (!cancelled) console.error('Failed to load root nodes:', err);
      })
      .finally(() => {
        if (!cancelled) setIsInitialLoading(false);
      });
    return () => { cancelled = true; };
  }, [connectionId, loadChildren]);

  const toggleExpand = useCallback(
    async (path: string) => {
      if (!connectionId) return;

      const findNode = (nodes: TreeNode[]): TreeNode | undefined => {
        for (const n of nodes) {
          if (n.path === path) return n;
          if (n.children) {
            const found = findNode(n.children);
            if (found) return found;
          }
        }
        return undefined;
      };

      // Check if we need to load children before updating state
      setRoots((prev) => {
        const node = findNode(prev);
        if (!node) return prev;
        if (node.isExpanded) {
          // Collapse
          const collapse = (nodes: TreeNode[]): TreeNode[] =>
            nodes.map((n) => {
              if (n.path === path) return { ...n, isExpanded: false };
              if (n.children) return { ...n, children: collapse(n.children) };
              return n;
            });
          return collapse(prev);
        }
        if (node.children) {
          // Already loaded — just expand
          const expand = (nodes: TreeNode[]): TreeNode[] =>
            nodes.map((n) => {
              if (n.path === path) return { ...n, isExpanded: true };
              if (n.children) return { ...n, children: expand(n.children) };
              return n;
            });
          return expand(prev);
        }
        // Need to load — set loading flag
        const setLoading = (nodes: TreeNode[]): TreeNode[] =>
          nodes.map((n) => {
            if (n.path === path) return { ...n, isLoading: true };
            if (n.children) return { ...n, children: setLoading(n.children) };
            return n;
          });
        return setLoading(prev);
      });

      // Check current state to see if we need to fetch
      const currentNode = findNode(roots);
      if (currentNode && !currentNode.children && currentNode.has_children && !currentNode.isExpanded) {
        try {
          const children = await loadChildren(connectionId, path);
          const applyChildren = (nodes: TreeNode[]): TreeNode[] =>
            nodes.map((n) => {
              if (n.path === path) return { ...n, children, isExpanded: true, isLoading: false };
              if (n.children) return { ...n, children: applyChildren(n.children) };
              return n;
            });
          setRoots((prev) => applyChildren(prev));
        } catch {
          const clearLoading = (nodes: TreeNode[]): TreeNode[] =>
            nodes.map((n) => {
              if (n.path === path) return { ...n, isLoading: false };
              if (n.children) return { ...n, children: clearLoading(n.children) };
              return n;
            });
          setRoots((prev) => clearLoading(prev));
        }
      }
    },
    [connectionId, roots, loadChildren],
  );

  const toggleSelect = useCallback(
    (path: string) => {
      const next = new Set(selectedPaths);
      if (next.has(path)) {
        next.delete(path);
      } else {
        next.add(path);
      }
      onSelectionChange(next);
    },
    [selectedPaths, onSelectionChange],
  );

  const renderNode = (node: TreeNode) => {
    const indent = node.level * 20;
    const isSelected = selectedPaths.has(node.path);

    return (
      <div key={node.path}>
        <div
          className="flex items-center gap-1.5 py-1 px-2 hover:bg-muted/50 rounded-sm cursor-pointer group"
          style={{ paddingLeft: `${indent + 8}px` }}
        >
          {/* Expand/collapse toggle */}
          {node.has_children ? (
            <button
              onClick={() => toggleExpand(node.path)}
              className="p-0.5 hover:bg-muted rounded"
            >
              {node.isLoading ? (
                <Loader2 className="h-3.5 w-3.5 animate-spin text-muted-foreground" />
              ) : node.isExpanded ? (
                <ChevronDown className="h-3.5 w-3.5 text-muted-foreground" />
              ) : (
                <ChevronRight className="h-3.5 w-3.5 text-muted-foreground" />
              )}
            </button>
          ) : (
            <span className="w-[22px]" />
          )}

          {/* Checkbox */}
          <Checkbox
            checked={isSelected}
            onCheckedChange={() => toggleSelect(node.path)}
            className="shrink-0"
          />

          {/* Icon + label */}
          <div
            className="flex items-center gap-1.5 min-w-0 flex-1"
            onClick={() => node.has_children && toggleExpand(node.path)}
          >
            {getNodeIcon(node.node_type)}
            <span className="text-sm truncate">{node.name}</span>
            <span className="text-xs text-muted-foreground ml-1">{node.node_type}</span>
          </div>
        </div>

        {/* Children */}
        {node.isExpanded && node.children && (
          <div>{node.children.map(renderNode)}</div>
        )}
      </div>
    );
  };

  if (!connectionId) {
    return (
      <div className="flex items-center justify-center h-64 text-muted-foreground text-sm">
        Select a connection to browse its resources
      </div>
    );
  }

  if (isInitialLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-6 w-6 animate-spin text-primary" />
        <span className="ml-2 text-sm text-muted-foreground">Loading...</span>
      </div>
    );
  }

  if (roots.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-muted-foreground text-sm">
        No resources found for this connection
      </div>
    );
  }

  return (
    <ScrollArea className="h-[500px] border rounded-md">
      <div className="p-1">{roots.map(renderNode)}</div>
    </ScrollArea>
  );
}
