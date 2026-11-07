import * as React from 'react'; import {cn} from '@/lib/utils';
export function Badge({className,...p}:React.HTMLAttributes<HTMLDivElement>){return <div className={cn('inline-flex items-center',className)} {...p}/>}
