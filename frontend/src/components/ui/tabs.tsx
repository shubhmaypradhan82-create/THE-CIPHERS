import * as React from 'react'; import {cn} from '@/lib/utils';
const Ctx=React.createContext<{value?:string;setValue:(v:string)=>void}>({setValue:()=>{}});
export function Tabs({defaultValue,children}:any){const [value,setValue]=React.useState(defaultValue);return <Ctx.Provider value={{value,setValue}}><div>{children}</div></Ctx.Provider>}
export function TabsList({className,...p}:any){return <div className={cn('flex p-1 gap-1',className)} {...p}/>}
export function TabsTrigger({value,children,className,...p}:any){const c=React.useContext(Ctx);return <button type="button" onClick={()=>c.setValue(value)} className={cn('px-3 py-2 text-sm rounded-lg',c.value===value?'bg-red-600 text-white':'text-white/60',className)} {...p}>{children}</button>}
