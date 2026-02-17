import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import useBreadcrumbStore from '@/stores/breadcrumb-store';
import KGSearch from '@/components/search/kg-search';
import ConceptsSearch from '@/components/search/concepts-search';
import PropertiesSearch from '@/components/search/properties-search';

type OntologyMode = 'concepts' | 'properties' | 'kg';

function getModeFromPath(pathname: string): OntologyMode {
  const last = pathname.split('/').filter(Boolean).pop();
  if (last === 'properties') return 'properties';
  if (last === 'kg') return 'kg';
  return 'concepts';
}

const MODE_LABELS: Record<OntologyMode, string> = {
  concepts: 'Concepts',
  properties: 'Properties',
  kg: 'Knowledge Graph',
};

export default function OntologySearchView() {
  const { t } = useTranslation(['search', 'semantic-models', 'common']);
  const location = useLocation();
  const setStaticSegments = useBreadcrumbStore((state) => state.setStaticSegments);
  const setDynamicTitle = useBreadcrumbStore((state) => state.setDynamicTitle);

  const mode = getModeFromPath(location.pathname);
  const params = new URLSearchParams(location.search);

  useEffect(() => {
    setStaticSegments([
      { label: 'Ontology', path: '/ontology' },
    ]);
    setDynamicTitle(MODE_LABELS[mode]);
    return () => {
      setStaticSegments([]);
      setDynamicTitle(null);
    };
  }, [setStaticSegments, setDynamicTitle, mode, t]);

  if (mode === 'kg') {
    const kgPrefix = params.get('prefix') || '';
    const kgPath = params.get('path')?.split('|').filter(Boolean) || [];
    const kgSparql = params.get('sparql') || 'SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10';
    const kgDirection = (params.get('direction') as 'all' | 'incoming' | 'outgoing') || 'all';
    const kgConceptsOnly = params.get('concepts_only') === 'true';

    return (
      <div className="py-4 space-y-4">
        <KGSearch
          initialPrefix={kgPrefix}
          initialPath={kgPath}
          initialSparql={kgSparql}
          initialDirectionFilter={kgDirection}
          initialShowConceptsOnly={kgConceptsOnly}
        />
      </div>
    );
  }

  if (mode === 'properties') {
    const propertiesQuery = params.get('query') || '';
    const propertiesIri = params.get('iri');
    const initialProperty = propertiesIri ? {
      value: propertiesIri,
      label: propertiesIri.split('/').pop() || propertiesIri.split('#').pop() || propertiesIri,
      type: 'property' as const,
    } : null;

    return (
      <div className="py-4 space-y-4">
        <PropertiesSearch
          initialQuery={propertiesQuery}
          initialSelectedProperty={initialProperty}
        />
      </div>
    );
  }

  // Default: concepts
  const conceptsQuery = params.get('query') || '';
  const conceptsIri = params.get('iri');
  const initialConcept = conceptsIri ? {
    value: conceptsIri,
    label: conceptsIri.split('/').pop() || conceptsIri.split('#').pop() || conceptsIri,
    type: 'class' as const,
  } : null;

  return (
    <div className="py-4 space-y-4">
      <ConceptsSearch
        initialQuery={conceptsQuery}
        initialSelectedConcept={initialConcept}
      />
    </div>
  );
}
