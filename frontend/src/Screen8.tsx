import { useEffect } from "react";
import {
  AlertTriangle,
  Bell,
  ChevronDown,
  Download,
  FilePlus2,
  FileText,
  LayoutDashboard,
  MapPin,
  Search,
  Settings,
  Shield,
} from "lucide-react";

export function Screen8() {
  return (
    <div>
      <div className="bg-zinc-950 text-neutral-50 w-full h-fit h-fit min-h-screen w-screen min-w-screen max-w-screen overflow-visible">
        <div className="min-h-[956px] flex w-full">
          <aside className="bg-neutral-950 border-red-600/20 border-0 border-solid flex flex-col w-64 h-full">
            <div className="flex p-6 items-center gap-2">
              <Shield className="text-red-600 w-6 h-6" />
              <span className="font-semibold text-white text-lg leading-[28px]">
                The Ciphers
              </span>
            </div>
            <nav className="space-y-1 px-3 py-2 flex-1">
              <a
                href="#"
                className="rounded-2xl text-white/60 flex px-3 py-2.5 items-center gap-3"
              >
                <LayoutDashboard className="w-5 h-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Dashboard
                </span>
              </a>
              <a
                href="#"
                className="rounded-2xl text-white/60 flex px-3 py-2.5 items-center gap-3"
              >
                <AlertTriangle className="w-5 h-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Threats
                </span>
              </a>
              <a
                href="#"
                className="rounded-2xl text-white/60 flex px-3 py-2.5 items-center gap-3"
              >
                <MapPin className="w-5 h-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Geolocation
                </span>
              </a>
              <a
                href="#"
                className="rounded-2xl text-white/60 flex px-3 py-2.5 items-center gap-3"
              >
                <Search className="w-5 h-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Forensics
                </span>
              </a>
              <a
                href="#"
                className="rounded-2xl bg-red-600 text-white flex px-3 py-2.5 items-center gap-3"
              >
                <FileText className="w-5 h-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Reports
                </span>
              </a>
              <a
                href="#"
                className="rounded-2xl text-white/60 flex px-3 py-2.5 items-center gap-3"
              >
                <Settings className="w-5 h-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Settings
                </span>
              </a>
            </nav>
            <div className="rounded-2xl bg-white/5 flex mx-3 mb-3 p-4 items-center gap-3">
              <div className="font-semibold rounded-full bg-red-600 text-white text-sm leading-[20px] flex justify-center items-center w-10 h-10">
                P
              </div>
              <div className="flex flex-col">
                <span className="font-medium text-white text-sm leading-[20px]">
                  Prateek
                </span>
                <span className="text-white/50 text-xs leading-[16px]">
                  SOC Analyst
                </span>
              </div>
            </div>
          </aside>
          <div className="min-w-0 bg-neutral-950 flex flex-col flex-1">
            <header className="bg-neutral-950 border-red-600/20 border-t-0 border-r-0 border-b-1 border-l-0 border-solid flex px-6 py-4 justify-between items-center flex-1 gap-4">
              <div className="max-w-md rounded-2xl bg-white/5 flex px-4 py-2.5 items-center flex-1 gap-3">
                <Search className="text-white/40 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search threats, senders, IPs, domains..."
                  className="bg-transparent outline-none text-white text-sm leading-[20px] flex-1"
                />
              </div>
              <div className="flex items-center gap-4">
                <div className="rounded-2xl bg-red-600/15 flex px-4 py-2 items-center gap-2">
                  <AlertTriangle className="text-red-600 w-4 h-4" />
                  <span className="font-medium text-red-600 text-sm leading-[20px]">
                    Threat Level: Elevated
                  </span>
                </div>
                <button className="relative rounded-full bg-white/5 flex justify-center items-center w-10 h-10">
                  <Bell className="text-white/70 w-5 h-5" />
                  <span className="font-semibold rounded-full bg-red-600 text-white text-[10px] flex absolute -right-1 -top-1 justify-center items-center w-5 h-5">
                    7
                  </span>
                </button>
                <div className="rounded-2xl bg-white/5 flex px-3 py-2 items-center gap-2">
                  <div className="font-semibold rounded-full bg-red-600 text-white text-sm leading-[20px] flex justify-center items-center w-8 h-8">
                    JM
                  </div>
                  <ChevronDown className="text-white/50 w-4 h-4" />
                </div>
              </div>
            </header>
            <main className="p-8 flex-1 overflow-auto">
              <div className="flex justify-between items-start gap-6">
                <div className="flex flex-col gap-2">
                  <h1 className="font-semibold text-white text-3xl leading-[36px] tracking-tight">
                    Reports
                  </h1>
                  <p className="text-white/50 text-sm leading-[20px]">
                    Generate and download security summaries for stakeholders.
                  </p>
                </div>
                <button className="font-semibold rounded-2xl bg-red-600 text-white text-sm leading-[20px] flex px-5 py-3 items-center gap-2">
                  <FilePlus2 className="w-4 h-4" />
                  Generate Report
                </button>
              </div>
              <div className="grid grid-cols-4 mt-8 gap-4">
                <div className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-1 border-solid flex p-6 flex-col gap-3">
                  <span className="text-white/50 text-sm leading-[20px]">
                    Reports Generated (30d)
                  </span>
                  <span className="font-semibold text-white text-3xl leading-[36px]">
                    18
                  </span>
                </div>
                <div className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-1 border-solid flex p-6 flex-col gap-3">
                  <span className="text-white/50 text-sm leading-[20px]">
                    Scheduled Reports
                  </span>
                  <span className="font-semibold text-white text-3xl leading-[36px]">
                    3
                  </span>
                </div>
                <div className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-1 border-solid flex p-6 flex-col gap-3">
                  <span className="text-white/50 text-sm leading-[20px]">
                    Last Generated
                  </span>
                  <span className="font-semibold text-white text-2xl leading-[32px]">
                    2 hours ago
                  </span>
                </div>
                <div className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-1 border-solid flex p-6 flex-col gap-3">
                  <span className="text-white/50 text-sm leading-[20px]">
                    Avg. Generation Time
                  </span>
                  <span className="font-semibold text-white text-3xl leading-[36px]">
                    4.2s
                  </span>
                </div>
              </div>
              <section className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-1 border-solid mt-8 p-6">
                <h2 className="font-semibold text-white text-lg leading-[28px] mb-6">
                  Scheduled Reports
                </h2>
                <table className="text-left w-full">
                  <thead>
                    <tr className="font-medium uppercase text-white/40 text-xs leading-[16px] tracking-wide border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <th className="pb-4">Report Name</th>
                      <th className="pb-4">Frequency</th>
                      <th className="pb-4">Next Run</th>
                      <th className="pb-4">Recipients</th>
                      <th className="pb-4">Status</th>
                    </tr>
                  </thead>
                  <tbody className="text-sm leading-[20px]">
                    <tr className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <td className="font-medium text-white py-5">
                        Weekly Threat Summary
                      </td>
                      <td className="text-white/60 py-5">
                        Weekly, Mondays 9:00 UTC
                      </td>
                      <td className="text-white/60 py-5">2024-06-10</td>
                      <td className="text-white/60 py-5">3 recipients</td>
                      <td className="py-5">
                        <span className="font-medium rounded-full bg-emerald-500/15 text-emerald-400 text-xs leading-[16px] px-3 py-1">
                          Active
                        </span>
                      </td>
                    </tr>
                    <tr className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <td className="font-medium text-white py-5">
                        Monthly Executive Brief
                      </td>
                      <td className="text-white/60 py-5">Monthly, 1st</td>
                      <td className="text-white/60 py-5">2024-07-01</td>
                      <td className="text-white/60 py-5">5 recipients</td>
                      <td className="py-5">
                        <span className="font-medium rounded-full bg-emerald-500/15 text-emerald-400 text-xs leading-[16px] px-3 py-1">
                          Active
                        </span>
                      </td>
                    </tr>
                    <tr>
                      <td className="font-medium text-white pt-5">
                        Daily Phishing Digest
                      </td>
                      <td className="text-white/60 pt-5">Daily, 08:00 UTC</td>
                      <td className="text-white/60 pt-5">2024-06-04</td>
                      <td className="text-white/60 pt-5">2 recipients</td>
                      <td className="pt-5">
                        <span className="font-medium rounded-full bg-amber-500/15 text-amber-400 text-xs leading-[16px] px-3 py-1">
                          Paused
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </section>
              <section className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-1 border-solid mt-8 p-6">
                <h2 className="font-semibold text-white text-lg leading-[28px] mb-6">
                  Recent Reports
                </h2>
                <table className="text-left w-full">
                  <thead>
                    <tr className="font-medium uppercase text-white/40 text-xs leading-[16px] tracking-wide border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <th className="pb-4">Report Name</th>
                      <th className="pb-4">Type</th>
                      <th className="pb-4">Date Generated</th>
                      <th className="pb-4">Size</th>
                      <th className="text-right pb-4">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="text-sm leading-[20px]">
                    <tr className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <td className="font-medium text-white py-5">
                        Weekly Threat Summary — Jun 3
                      </td>
                      <td className="text-white/60 py-5">Weekly Summary</td>
                      <td className="text-white/60 py-5">2024-06-03</td>
                      <td className="text-white/60 py-5">1.2 MB</td>
                      <td className="text-right py-5">
                        <button className="inline-flex font-medium rounded-xl text-red-600 text-xs leading-[16px] border-red-600 border-1 border-solid px-3 py-2 items-center gap-2">
                          <Download className="w-4 h-4" />
                          Download
                        </button>
                      </td>
                    </tr>
                    <tr className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <td className="font-medium text-white py-5">
                        PayPal Phishing Cluster — Case Export
                      </td>
                      <td className="text-white/60 py-5">Case Report</td>
                      <td className="text-white/60 py-5">2024-06-03</td>
                      <td className="text-white/60 py-5">840 KB</td>
                      <td className="text-right py-5">
                        <button className="inline-flex font-medium rounded-xl text-red-600 text-xs leading-[16px] border-red-600 border-1 border-solid px-3 py-2 items-center gap-2">
                          <Download className="w-4 h-4" />
                          Download
                        </button>
                      </td>
                    </tr>
                    <tr className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <td className="font-medium text-white py-5">
                        Monthly Executive Brief — May
                      </td>
                      <td className="text-white/60 py-5">Executive Summary</td>
                      <td className="text-white/60 py-5">2024-06-01</td>
                      <td className="text-white/60 py-5">2.1 MB</td>
                      <td className="text-right py-5">
                        <button className="inline-flex font-medium rounded-xl text-red-600 text-xs leading-[16px] border-red-600 border-1 border-solid px-3 py-2 items-center gap-2">
                          <Download className="w-4 h-4" />
                          Download
                        </button>
                      </td>
                    </tr>
                    <tr className="border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                      <td className="font-medium text-white py-5">
                        Daily Phishing Digest — Jun 2
                      </td>
                      <td className="text-white/60 py-5">Daily Digest</td>
                      <td className="text-white/60 py-5">2024-06-02</td>
                      <td className="text-white/60 py-5">310 KB</td>
                      <td className="text-right py-5">
                        <button className="inline-flex font-medium rounded-xl text-red-600 text-xs leading-[16px] border-red-600 border-1 border-solid px-3 py-2 items-center gap-2">
                          <Download className="w-4 h-4" />
                          Download
                        </button>
                      </td>
                    </tr>
                    <tr>
                      <td className="font-medium text-white pt-5">
                        Geolocation Threat Analysis — Q2
                      </td>
                      <td className="text-white/60 pt-5">Custom Report</td>
                      <td className="text-white/60 pt-5">2024-05-29</td>
                      <td className="text-white/60 pt-5">1.8 MB</td>
                      <td className="text-right pt-5">
                        <button className="inline-flex font-medium rounded-xl text-red-600 text-xs leading-[16px] border-red-600 border-1 border-solid px-3 py-2 items-center gap-2">
                          <Download className="w-4 h-4" />
                          Download
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </section>
            </main>
          </div>
        </div>
      </div>
    </div>
  );
}
