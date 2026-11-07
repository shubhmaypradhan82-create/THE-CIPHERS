import { useEffect } from "react";
import {
  AlertTriangle,
  Bell,
  ChevronDown,
  FileText,
  LayoutDashboard,
  MapPin,
  Search,
  Settings,
  Shield,
} from "lucide-react";

export function Screen6() {
  return (
    <div>
      <div className="bg-zinc-950 text-neutral-50 w-full h-fit h-fit min-h-screen w-screen min-w-screen max-w-screen overflow-visible">
        <div className="min-h-screen bg-zinc-950 flex">
          <aside className="bg-zinc-950 flex flex-col w-64 h-full">
            <div className="flex p-6 items-center gap-2">
              <Shield className="size-6 text-red-600" />
              <span className="font-semibold text-neutral-50 text-lg leading-[28px]">
                The Ciphers
              </span>
            </div>
            <nav className="space-y-1 px-3 py-2 flex-1">
              <a
                href="#"
                className="rounded-2xl text-[#9f9fa9] flex px-3 py-2.5 items-center gap-3"
              >
                <LayoutDashboard className="size-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Dashboard
                </span>
              </a>
              <a
                href="#"
                className="rounded-2xl bg-red-600 text-white flex px-3 py-2.5 items-center gap-3"
              >
                <AlertTriangle className="size-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Threats
                </span>
              </a>
              <a
                href="#"
                className="rounded-2xl text-[#9f9fa9] flex px-3 py-2.5 items-center gap-3"
              >
                <MapPin className="size-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Geolocation
                </span>
              </a>
              <a
                href="#"
                className="rounded-2xl text-[#9f9fa9] flex px-3 py-2.5 items-center gap-3"
              >
                <Search className="size-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Forensics
                </span>
              </a>
              <a
                href="#"
                className="rounded-2xl text-[#9f9fa9] flex px-3 py-2.5 items-center gap-3"
              >
                <FileText className="size-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Reports
                </span>
              </a>
              <a
                href="#"
                className="rounded-2xl text-[#9f9fa9] flex px-3 py-2.5 items-center gap-3"
              >
                <Settings className="size-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Settings
                </span>
              </a>
            </nav>
            <div className="rounded-2xl bg-zinc-900 flex mx-3 mb-3 p-4 items-center gap-3">
              <div className="size-10 font-semibold rounded-full bg-red-600 text-white text-sm leading-[20px] flex justify-center items-center">
                P
              </div>
              <div className="flex flex-col">
                <span className="font-medium text-neutral-50 text-sm leading-[20px]">
                  Prateek
                </span>
                <span className="text-[#9f9fa9] text-xs leading-[16px]">
                  SOC Analyst
                </span>
              </div>
            </div>
          </aside>
          <div className="min-w-0 flex-1">
            <header className="flex px-8 py-5 justify-between items-center gap-6">
              <h1 className="truncate font-semibold text-xl leading-[28px]">
                Case Details
              </h1>
              <div className="relative flex-none w-[400px]">
                <Search className="top-1/2 -translate-y-1/2 size-4 text-[#9f9fa9] absolute left-4" />
                <input
                  type="text"
                  placeholder="Search threats, senders, IPs, domains..."
                  className="rounded-full bg-zinc-900 text-neutral-50 text-sm leading-[20px] pl-11 pr-4 w-full h-11"
                  defaultValue=""
                />
              </div>
              <div className="flex items-center gap-4">
                <div className="rounded-full bg-zinc-900 flex px-4 py-2 items-center gap-2">
                  <span className="size-2.5 rounded-full bg-red-600" />
                  <span className="whitespace-nowrap font-medium text-sm leading-[20px]">
                    Threat Level: Elevated
                  </span>
                </div>
                <button
                  type="button"
                  className="relative size-10 rounded-full text-[#9f9fa9] flex justify-center items-center"
                >
                  <Bell className="size-5" />
                  <span className="size-5 font-semibold rounded-full bg-red-600 text-white text-[10px] flex absolute -right-1 -top-1 justify-center items-center">
                    7
                  </span>
                </button>
                <button
                  type="button"
                  className="rounded-full flex pl-1 pr-2 py-1 items-center gap-2"
                >
                  <span className="size-9 font-semibold rounded-full bg-red-600 text-white text-sm leading-[20px] flex justify-center items-center">
                    JM
                  </span>
                  <ChevronDown className="size-4 text-[#9f9fa9]" />
                </button>
              </div>
            </header>
            <main className="space-y-6 overflow-y-auto px-8 pt-4 pb-10">
              <div className="space-y-2">
                <h2 className="font-semibold text-3xl leading-[36px] tracking-tight">
                  Phishing Campaign — PayPal Impersonation Cluster
                </h2>
                <p className="text-[#9f9fa9] text-sm leading-[20px]">
                  Prateek<span className="px-2">•</span>Opened 2024-06-03
                </p>
              </div>
              <section className="space-y-4 rounded-2xl bg-zinc-900 border-red-600/20 border-1 border-solid p-6">
                <h3 className="font-semibold text-lg leading-[28px]">
                  Evidence Chain
                </h3>
                <div className="space-y-6 border-red-600/40 border-t-0 border-r-0 border-b-0 border-l-1 border-solid pl-6">
                  <div className="relative text-sm leading-5">
                    <span className="size-2 rounded-full bg-red-600 absolute -left-[29px] top-1.5" />
                    2024-06-03 09:41 UTC — Email received and quarantined by AI
                    filter
                  </div>
                  <div className="relative text-sm leading-5">
                    <span className="size-2 rounded-full bg-red-600 absolute -left-[29px] top-1.5" />
                    2024-06-03 09:42 UTC — Sender domain paypa1-secure.com
                    flagged as lookalike
                  </div>
                  <div className="relative text-sm leading-5">
                    <span className="size-2 rounded-full bg-red-600 absolute -left-[29px] top-1.5" />
                    2024-06-03 10:15 UTC — Reply-to domain
                    support@paypa1-secure-verify.com added to blocklist
                  </div>
                  <div className="relative text-sm leading-5">
                    <span className="size-2 rounded-full bg-red-600 absolute -left-[29px] top-1.5" />
                    2024-06-03 11:03 UTC — Case escalated by Prateek for manual
                    review
                  </div>
                </div>
              </section>
              <section className="space-y-4 rounded-2xl bg-zinc-900 border-red-600/20 border-1 border-solid p-6">
                <h3 className="font-semibold text-lg leading-[28px]">
                  Header Analysis
                </h3>
                <table className="text-left text-sm leading-[20px] w-full">
                  <tbody>
                    <tr className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <td className="w-1/3 text-[#9f9fa9] py-3">SPF</td>
                      <td className="font-medium text-red-400 py-3">Fail</td>
                    </tr>
                    <tr className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <td className="text-[#9f9fa9] py-3">DKIM</td>
                      <td className="font-medium text-red-400 py-3">Fail</td>
                    </tr>
                    <tr className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <td className="text-[#9f9fa9] py-3">DMARC</td>
                      <td className="font-medium text-red-400 py-3">Fail</td>
                    </tr>
                    <tr className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <td className="text-[#9f9fa9] py-3">
                        Return-Path mismatch
                      </td>
                      <td className="py-3">
                        billing@paypa1-secure.com vs paypal.com
                      </td>
                    </tr>
                    <tr>
                      <td className="text-[#9f9fa9] py-3">Originating IP</td>
                      <td className="py-3">
                        197.210.53.104
                        <span className="text-amber-400">
                          flagged as high-risk
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </section>
              <section className="space-y-4 rounded-2xl bg-zinc-900 border-red-600/20 border-1 border-solid p-6">
                <h3 className="font-semibold text-lg leading-[28px]">
                  Correlated Threats
                </h3>
                <table className="text-left text-sm leading-[20px] w-full">
                  <thead>
                    <tr className="text-[#9f9fa9] border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <th className="font-medium py-3">Sender</th>
                      <th className="font-medium py-3">Subject</th>
                      <th className="font-medium py-3">Risk Score</th>
                      <th className="font-medium py-3">Detected</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <td className="py-3">billing@paypa1-secure.com</td>
                      <td className="py-3">Urgent: Verify your account</td>
                      <td className="font-semibold text-red-400 py-3">94</td>
                      <td className="text-[#9f9fa9] py-3">2 min ago</td>
                    </tr>
                    <tr className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <td className="py-3">support@paypa1-secure-verify.com</td>
                      <td className="py-3">Your account will be suspended</td>
                      <td className="font-semibold text-red-400 py-3">91</td>
                      <td className="text-[#9f9fa9] py-3">18 min ago</td>
                    </tr>
                    <tr>
                      <td className="py-3">no-reply@paypa1-alerts.com</td>
                      <td className="py-3">Unusual login attempt detected</td>
                      <td className="font-semibold text-red-400 py-3">88</td>
                      <td className="text-[#9f9fa9] py-3">1 hr ago</td>
                    </tr>
                  </tbody>
                </table>
              </section>
              <section className="space-y-4 rounded-2xl bg-zinc-900 border-red-600/20 border-1 border-solid p-6">
                <h3 className="font-semibold text-lg leading-[28px]">
                  Infrastructure Graph
                </h3>
                <div className="space-y-6 rounded-xl bg-zinc-950 border-white/10 border-1 border-solid p-6">
                  <p className="text-[#9f9fa9] text-sm leading-[20px]">
                    Shared infrastructure cluster — 5 related indicators
                  </p>
                  <div className="flex flex-col items-center gap-4">
                    <div className="font-semibold rounded-full bg-red-600/20 text-sm leading-[20px] border-red-600 border-1 border-solid px-5 py-3">
                      paypa1-secure.com
                    </div>
                    <div className="grid grid-cols-5 items-center gap-3 w-full">
                      <div className="col-span-1 bg-red-600/50 h-px" />
                      <div className="col-span-1 bg-red-600/50 h-px" />
                      <div className="col-span-1 bg-red-600/50 h-px" />
                      <div className="col-span-1 bg-red-600/50 h-px" />
                      <div className="col-span-1 bg-red-600/50 h-px" />
                    </div>
                    <div className="grid grid-cols-5 text-center text-[#9f9fa9] text-xs leading-[16px] gap-3 w-full">
                      <span>billing@paypa1-secure.com</span>
                      <span>support@paypa1-secure-verify.com</span>
                      <span>no-reply@paypa1-alerts.com</span>
                      <span>197.210.53.104</span>
                      <span>197.210.53.107</span>
                    </div>
                  </div>
                </div>
              </section>
              <section className="space-y-4 rounded-2xl bg-zinc-900 border-red-600/20 border-1 border-solid p-6">
                <h3 className="font-semibold text-lg leading-[28px]">
                  AI Forensic Summary
                </h3>
                <p className="text-zinc-300 text-sm leading-6">
                  This cluster represents a coordinated phishing campaign
                  impersonating PayPal. The AI model identified a consistent
                  lookalike domain pattern (paypa1 substituting paypal), shared
                  hosting infrastructure across all three sender addresses, and
                  matching urgency-based social engineering language. All three
                  messages failed SPF, DKIM and DMARC checks and originated from
                  the same autonomous system in Mumbai, Maharashtra. Confidence:
                  96%
                </p>
                <div className="rounded-full bg-zinc-800 w-full h-3 overflow-hidden">
                  <div className="rounded-full bg-red-600 w-[96%] h-full" />
                </div>
              </section>
            </main>
          </div>
        </div>
      </div>
    </div>
  );
}
