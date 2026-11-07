import * as React from 'react'; import {cn} from '@/lib/utils';
export function Card({className,...p}:React.HTMLAttributes<HTMLDivElement>){return <div className={cn('flex flex-col',className)} {...p}/>}
export function CardHeader({className,...p}:React.HTMLAttributes<HTMLDivElement>){return <div className={cn('flex flex-col',className)} {...p}/>}
export function CardContent({className,...p}:React.HTMLAttributes<HTMLDivElement>){return <div className={cn(className)} {...p}/>}
export function CardFooter({className,...p}:React.HTMLAttributes<HTMLDivElement>){return <div className={cn('flex items-center',className)} {...p}/>}
export function CardTitle({className,...p}:React.HTMLAttributes<HTMLHeadingElement>){return <h3 className={cn(className)} {...p}/>}
export function CardDescription({className,...p}:React.HTMLAttributes<HTMLParagraphElement>){return <p className={cn(className)} {...p}/>}
