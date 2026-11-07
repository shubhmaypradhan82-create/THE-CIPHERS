import * as React from 'react';
export function ChartContainer({children,className,...p}:any){return <div className={className} {...p}>{children}</div>}
export function ChartTooltip({content}:any){return content||null}
