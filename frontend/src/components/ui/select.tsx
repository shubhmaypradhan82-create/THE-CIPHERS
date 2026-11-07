import * as React from 'react'; import {cn} from '@/lib/utils';
const Ctx=React.createContext<{value?:string;setValue:(v:string)=>void}>({setValue:()=>{}});
export function Select({defaultValue,children}:any){const [value,setValue]=React.useState(defaultValue);return <Ctx.Provider value={{value,setValue}}><div className="relative inline-flex">{children}</div></Ctx.Provider>}
export function SelectTrigger({className,children,...p}:any){const {value}=React.useContext(Ctx);return <div className={cn('flex items-center justify-between px-3 py-2',className)} {...p}>{children}{value!==undefined&&null}</div>}
export function SelectValue({placeholder}:any){const {value}=React.useContext(Ctx);return <span>{value||placeholder||''}</span>}
export function SelectContent({children}:any){return <div className="absolute z-50 top-full left-0 mt-1 min-w-full rounded-xl bg-zinc-900 border border-white/10 p-1 shadow-xl">{children}</div>}
export function SelectItem({value,children}:any){const {setValue}=React.useContext(Ctx);return <button type="button" onClick={()=>setValue(value)} className="block w-full text-left px-3 py-2 rounded-lg hover:bg-white/10 text-sm">{children}</button>}
