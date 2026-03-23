import { Link } from 'react-router-dom';
import { Navigation } from './navigation';
import { UnityCatalogLogo } from '@/components/unity-catalog-logo';
import { cn } from '@/lib/utils';

interface SidebarProps {
  isCollapsed: boolean;
}

export function Sidebar({ isCollapsed }: SidebarProps) {
  return (
    <aside
      className={cn(
        'fixed inset-y-0 left-0 z-50 flex flex-col border-r border-sidebar-border bg-sidebar transition-all duration-300 ease-in-out overflow-x-hidden',
        isCollapsed ? 'w-14' : 'w-60' // Adjust width based on state
      )}
    >
      {/* Logo/Branding */}
      <div className="flex h-16 items-center justify-center px-2 shrink-0 overflow-hidden">
         <Link to="/" className="flex items-center justify-center gap-2 font-semibold">
            <UnityCatalogLogo className={cn(
              "transition-all duration-300",
              isCollapsed ? "h-8 w-8 object-contain" : "h-10 w-auto max-w-48 object-contain"
            )} />
         </Link>
      </div>
      <div className="intersection-device-bar" />

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto">
         <Navigation isCollapsed={isCollapsed} />
      </div>

      {/* Optional Footer (if needed) */}
      {/* <div className="mt-auto border-t p-4"> Footer Content </div> */}
    </aside>
  );
}
