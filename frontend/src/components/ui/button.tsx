import * as React from 'react';
import { cn } from '@/lib/utils';
export const Button=React.forwardRef<HTMLButtonElement,React.ButtonHTMLAttributes<HTMLButtonElement> & {variant?:string}>(({className,variant='default',...p},ref)=><button ref={ref} className={cn('inline-flex items-center justify-center whitespace-nowrap transition-colors disabled:pointer-events-none disabled:opacity-50',variant==='outline'?'border border-white/15 bg-transparent':'',className)} {...p}/>); Button.displayName='Button';
