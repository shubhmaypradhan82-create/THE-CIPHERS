const API = 'https://the-ciphers.onrender.com';

export type User = { id:number; name:string; email:string; role:string; created_at:string };
export type Email = { id:number; sender:string; recipient:string; subject:string|null; body:string|null; threat_level:string; investigation_id:number|null; created_at:string };
export type Investigation = { id:number; title:string; description:string|null; user_id:number|null; status:string; created_at:string };
export type AIResult = { id:number; email_id:number; prediction:string; confidence_score:number|null; explanation:string|null; created_at:string };
export type Forensic = { id:number; email_id:number|null; investigation_id:number|null; case_id:string; analysis_type:string; result_json:string; created_at:string };

let auth = '';
export function setAuth(value:string){ auth=value; }
export function getAuth(){ return auth || localStorage.getItem('basicAuth') || sessionStorage.getItem('basicAuth') || ''; }

async function request<T>(path:string, options:RequestInit={}) : Promise<T> {
  const headers = new Headers(options.headers || {});
  const token = getAuth();
  if(token) headers.set('Authorization', `Basic ${token}`);
  if(options.body && !(options.body instanceof FormData) && !headers.has('Content-Type')) headers.set('Content-Type','application/json');
  const response = await fetch(`${API}${path}`, {...options, headers});
  let data:any = null;
  const type = response.headers.get('content-type') || '';
  if(type.includes('application/json')) data = await response.json(); else data = await response.text();
  if(!response.ok) throw new Error(data?.detail || data?.message || data || `Request failed (${response.status})`);
  return data as T;
}

export const api = {
  url: API,
  me:()=>request<User>('/auth/me'),
  register:(payload:any)=>request<User>('/auth/register',{method:'POST',body:JSON.stringify(payload)}),
  login:(payload:any)=>request<User>('/auth/login',{method:'POST',body:JSON.stringify(payload)}),
  adminLogin:(payload:any)=>request<User>('/auth/admin-login',{method:'POST',body:JSON.stringify(payload)}),
  adminUsers:()=>request<any[]>('/admin/users'),
  adminAuditLogs:(limit=200)=>request<any[]>(`/admin/audit-logs?limit=${limit}`),
  adminResetPassword:(id:number)=>request<any>(`/admin/users/${id}/reset-password`,{method:'POST'}),
  adminDeleteUser:(id:number)=>request<any>(`/admin/users/${id}`,{method:'DELETE'}),
  adminBanUser:(id:number)=>request<any>(`/admin/users/${id}/ban`,{method:'POST'}),
  adminUnbanUser:(id:number)=>request<any>(`/admin/users/${id}/unban`,{method:'POST'}),
  adminIpIntel:(ip:string)=>request<any>(`/admin/ip-intel?ip=${encodeURIComponent(ip)}`),
  changePassword:(payload:any)=>request<any>('/auth/change-password',{method:'POST',body:JSON.stringify(payload)}),
  updateMe:(payload:any)=>request<User>('/auth/me',{method:'PUT',body:JSON.stringify(payload)}),
  health:()=>request<any>('/health'),
  dashboard:()=>request<any>('/dashboard/summary'),
  emails:(q='')=>request<Email[]>(`/emails${q?`?q=${encodeURIComponent(q)}`:''}`),
  email:(id:number)=>request<any>(`/emails/${id}`),
  threats:(params:Record<string,string|number|undefined>={})=>{const s=new URLSearchParams();Object.entries(params).forEach(([k,v])=>{if(v!==undefined&&v!=='')s.set(k,String(v))});return request<any[]>(`/threats?${s}`)},
  geolocation:()=>request<any>('/geolocation'),
  investigations:()=>request<Investigation[]>('/investigations'),
  createInvestigation:(payload:any)=>request<Investigation>('/investigations',{method:'POST',body:JSON.stringify(payload)}),
  updateInvestigation:(id:number,payload:any)=>request<Investigation>(`/investigations/${id}`,{method:'PATCH',body:JSON.stringify(payload)}),
  forensics:(q='')=>request<Forensic[]>(`/forensics${q?`?q=${encodeURIComponent(q)}`:''}`),
  aiResults:()=>request<AIResult[]>('/ai-results'),
  analyze:(payload:any)=>request<any>('/analyze',{method:'POST',body:JSON.stringify(payload)}),
  forensicUrl:(url:string)=>request<any>('/forensics/url',{method:'POST',body:JSON.stringify({url})}),
  forensicEmail:(file:File)=>{const fd=new FormData();fd.append('file',file);return request<any>('/forensics/email',{method:'POST',body:fd});},
  reports:()=>request<any[]>('/reports'),
  reportFromForensic:(id:number)=>request<any>(`/reports/from-forensic/${id}`,{method:'POST'}),
};
