import { useEffect } from "react";
import {
  AlertTriangle,
  ArrowDown,
  ArrowRight,
  ArrowUp,
  Bell,
  ChevronDown,
  ChevronRight,
  FileText,
  Forward,
  LayoutDashboard,
  MapPin,
  Search,
  Settings,
  Shield,
  ShieldAlert,
} from "lucide-react";
import { ChartContainer, ChartTooltip } from "@/components/ui/chart";
import {
  CartesianGrid,
  Line,
  LineChart as RechartsLineChart,
  XAxis,
  YAxis,
} from "recharts";

export function Screen1() {
  return (
    <div>
      <div className="bg-zinc-950 text-neutral-50 w-full h-fit h-fit min-h-screen w-screen min-w-screen max-w-screen overflow-visible">
        <div className="bg-zinc-950 flex h-[956px]">
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
                className="rounded-2xl bg-red-600 text-white flex px-3 py-2.5 items-center gap-3"
              >
                <LayoutDashboard className="size-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Dashboard
                </span>
              </a>
              <a
                href="#"
                className="rounded-2xl text-[#9f9fa9] flex px-3 py-2.5 items-center gap-3"
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
                <span className="font-medium text-sm leading-[20px]">
                  Prateek
                </span>
                <span className="text-[#9f9fa9] text-xs leading-[16px]">
                  SOC Analyst
                </span>
              </div>
            </div>
          </aside>
          <div className="min-w-0 bg-zinc-950 flex flex-col flex-1">
            <header className="flex px-8 py-5 justify-between items-center gap-6 w-full">
              <h1 className="truncate font-semibold text-xl leading-[28px]">
                Threat Overview
              </h1>
              <div className="min-w-[420px] max-w-xl flex-1">
                <div className="relative">
                  <Search className="top-1/2 size-4 -translate-y-1/2 text-[#9f9fa9] absolute left-4" />
                  <input
                    type="text"
                    placeholder="Search threats, senders, IPs, domains..."
                    className="rounded-full bg-zinc-900 text-neutral-50 text-sm leading-[20px] border-white/15 border-1 border-solid pl-11 pr-4 w-full h-11"
                    defaultValue=""
                  />
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="rounded-full bg-zinc-900 border-white/15 border-1 border-solid flex px-4 py-2 items-center gap-2">
                  <span className="size-2 rounded-full bg-red-600" />
                  <span className="whitespace-nowrap font-medium text-sm leading-[20px]">
                    Threat Level: Elevated
                  </span>
                </div>
                <button className="relative size-10 rounded-full text-[#9f9fa9] flex justify-center items-center">
                  <Bell className="size-5" />
                  <span className="size-5 font-semibold rounded-full bg-red-600 text-white text-[10px] flex absolute -right-1 -top-1 justify-center items-center">
                    7
                  </span>
                </button>
                <button className="rounded-full flex pl-1 pr-2 py-1 items-center gap-2">
                  <span className="size-9 font-semibold rounded-full bg-red-600 text-white text-sm leading-[20px] flex justify-center items-center">
                    JM
                  </span>
                  <ChevronDown className="size-4 text-[#9f9fa9]" />
                </button>
              </div>
            </header>
            <main className="p-8 flex-1 overflow-auto">
              <div className="grid grid-cols-4 gap-6">
                <div className="rounded-2xl bg-zinc-900 border-red-600/15 border-1 border-solid flex p-6 flex-col gap-4">
                  <p className="text-[#9f9fa9] text-sm leading-[20px]">
                    Threats Blocked (24h)
                  </p>
                  <div className="flex justify-between items-end">
                    <span className="font-semibold text-3xl leading-[36px]">
                      1,284
                    </span>
                    <span className="font-medium text-emerald-400 text-sm leading-[20px] flex items-center gap-1">
                      <ArrowUp className="size-4" />
                      +12%
                    </span>
                  </div>
                </div>
                <div className="rounded-2xl bg-zinc-900 border-red-600/15 border-1 border-solid flex p-6 flex-col gap-4">
                  <p className="text-[#9f9fa9] text-sm leading-[20px]">
                    Phishing Attempts
                  </p>
                  <div className="flex justify-between items-end">
                    <span className="font-semibold text-3xl leading-[36px]">
                      342
                    </span>
                    <span className="font-medium text-emerald-400 text-sm leading-[20px] flex items-center gap-1">
                      <ArrowUp className="size-4" />
                      +8%
                    </span>
                  </div>
                </div>
                <div className="rounded-2xl bg-zinc-900 border-red-600/15 border-1 border-solid flex p-6 flex-col gap-4">
                  <p className="text-[#9f9fa9] text-sm leading-[20px]">
                    Active Investigations
                  </p>
                  <div className="flex justify-between items-end">
                    <span className="font-semibold text-3xl leading-[36px]">
                      19
                    </span>
                    <ArrowRight className="size-4 text-[#9f9fa9]" />
                  </div>
                </div>
                <div className="rounded-2xl bg-zinc-900 border-red-600/15 border-1 border-solid flex p-6 flex-col gap-4">
                  <p className="text-[#9f9fa9] text-sm leading-[20px]">
                    Avg. Detection Time
                  </p>
                  <div className="flex justify-between items-end">
                    <span className="font-semibold text-3xl leading-[36px]">
                      1.8s
                    </span>
                    <span className="font-medium text-emerald-400 text-sm leading-[20px] flex items-center gap-1">
                      <ArrowDown className="size-4" />
                      -0.3s
                    </span>
                  </div>
                </div>
              </div>
              <div className="grid grid-cols-3 mt-6 gap-6">
                <div className="col-span-2 flex flex-col gap-6">
                  <div className="rounded-2xl bg-zinc-900 border-red-600/15 border-1 border-solid flex p-8 flex-col gap-6">
                    <h2 className="font-semibold text-lg leading-[28px]">
                      Threat Volume — Last 7 Days
                    </h2>
                    <ChartContainer
                      config={{
                        malicious: { label: "Malicious", color: "#dc2626" },
                        suspicious: {
                          label: "Suspicious",
                          color: "oklch(0.769 0.188 70.08)",
                        },
                      }}
                      className="w-full h-[260px]"
                    >
                      <RechartsLineChart
                        data={[
                          { day: "Mon", malicious: 210, suspicious: 320 },
                          { day: "Tue", malicious: 280, suspicious: 260 },
                          { day: "Wed", malicious: 190, suspicious: 340 },
                          { day: "Thu", malicious: 360, suspicious: 300 },
                          { day: "Fri", malicious: 420, suspicious: 380 },
                          { day: "Sat", malicious: 260, suspicious: 240 },
                          { day: "Sun", malicious: 320, suspicious: 290 },
                        ]}
                      >
                        <CartesianGrid
                          strokeDasharray="3 3"
                          stroke="oklch(1 0 0 / 8%)"
                        />
                        <XAxis
                          dataKey="day"
                          stroke="oklch(0.705 0.015 286.067)"
                          tickLine={false}
                          axisLine={false}
                        />
                        <YAxis
                          domain={[0, 500]}
                          stroke="oklch(0.705 0.015 286.067)"
                          tickLine={false}
                          axisLine={false}
                        />
                        <ChartTooltip />
                        <Line
                          type="monotone"
                          dataKey="malicious"
                          stroke="#dc2626"
                          strokeWidth={2}
                          dot={false}
                        />
                        <Line
                          type="monotone"
                          dataKey="suspicious"
                          stroke="oklch(0.769 0.188 70.08)"
                          strokeWidth={2}
                          dot={false}
                        />
                      </RechartsLineChart>
                    </ChartContainer>
                    <div className="flex items-center gap-6">
                      <span className="text-[#9f9fa9] text-xs leading-[16px] flex items-center gap-2">
                        <span className="size-2 rounded-full bg-red-600" />
                        Malicious
                      </span>
                      <span className="text-[#9f9fa9] text-xs leading-[16px] flex items-center gap-2">
                        <span className="size-2 rounded-full bg-amber-400" />
                        Suspicious
                      </span>
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-900 border-red-600/15 border-1 border-solid flex p-8 flex-col gap-6">
                    <h2 className="font-semibold text-lg leading-[28px]">
                      Recent Threats
                    </h2>
                    <div className="grid grid-cols-[1.5fr_1.6fr_.65fr_.9fr_1fr_.7fr_auto] text-[#9f9fa9] text-xs leading-[16px] px-2 pb-3 gap-3">
                      <span>Sender</span>
                      <span>Subject</span>
                      <span>Risk Score</span>
                      <span>Origin</span>
                      <span>Status</span>
                      <span>Detected</span>
                      <span />
                    </div>
                    <div className="flex flex-col gap-1">
                      <div className="grid grid-cols-[1.5fr_1.6fr_.65fr_.9fr_1fr_.7fr_auto] rounded-xl bg-zinc-950 text-sm leading-[20px] px-2 py-4 items-center gap-3">
                        <span className="truncate">
                          billing@paypa1-secure.com
                        </span>
                        <span className="truncate text-[#9f9fa9]">
                          Urgent: Verify your account
                        </span>
                        <span className="font-semibold text-red-400">94</span>
                        <span className="text-[#9f9fa9]">Lagos, NG</span>
                        <span className="font-medium text-red-400">
                          Quarantined
                        </span>
                        <span className="text-[#9f9fa9] text-xs leading-[16px]">
                          2 min ago
                        </span>
                        <ChevronRight className="size-4 text-[#9f9fa9]" />
                      </div>
                      <div className="grid grid-cols-[1.5fr_1.6fr_.65fr_.9fr_1fr_.7fr_auto] text-sm leading-[20px] px-2 py-4 items-center gap-3">
                        <span className="truncate">
                          hr-noreply@corp-updates.net
                        </span>
                        <span className="truncate text-[#9f9fa9]">
                          Updated benefits enrollment
                        </span>
                        <span className="font-semibold text-amber-400">78</span>
                        <span className="text-[#9f9fa9]">Minsk, BY</span>
                        <span className="font-medium text-amber-400">
                          Under Review
                        </span>
                        <span className="text-[#9f9fa9] text-xs leading-[16px]">
                          14 min ago
                        </span>
                        <ChevronRight className="size-4 text-[#9f9fa9]" />
                      </div>
                      <div className="grid grid-cols-[1.5fr_1.6fr_.65fr_.9fr_1fr_.7fr_auto] rounded-xl bg-zinc-950 text-sm leading-[20px] px-2 py-4 items-center gap-3">
                        <span className="truncate">
                          it-support@cloud-verify.com
                        </span>
                        <span className="truncate text-[#9f9fa9]">
                          Password expiration notice
                        </span>
                        <span className="font-semibold text-red-400">88</span>
                        <span className="text-[#9f9fa9]">Bucharest, RO</span>
                        <span className="font-medium text-red-400">
                          Quarantined
                        </span>
                        <span className="text-[#9f9fa9] text-xs leading-[16px]">
                          31 min ago
                        </span>
                        <ChevronRight className="size-4 text-[#9f9fa9]" />
                      </div>
                      <div className="grid grid-cols-[1.5fr_1.6fr_.65fr_.9fr_1fr_.7fr_auto] text-sm leading-[20px] px-2 py-4 items-center gap-3">
                        <span className="truncate">
                          notifications@docusign-secure.co
                        </span>
                        <span className="truncate text-[#9f9fa9]">
                          Document awaiting signature
                        </span>
                        <span className="font-semibold text-amber-400">65</span>
                        <span className="text-[#9f9fa9]">Manila, PH</span>
                        <span className="font-medium text-emerald-400">
                          Cleared
                        </span>
                        <span className="text-[#9f9fa9] text-xs leading-[16px]">
                          1 hr ago
                        </span>
                        <ChevronRight className="size-4 text-[#9f9fa9]" />
                      </div>
                    </div>
                  </div>
                </div>
                <div className="col-span-1 flex flex-col gap-6">
                  <div className="rounded-2xl bg-zinc-900 border-red-600/15 border-1 border-solid flex p-8 flex-col gap-6">
                    <h2 className="font-semibold text-lg leading-[28px]">
                      Top Attack Origins
                    </h2>
                    <div className="relative rounded-xl h-32 overflow-hidden">
                      <img
                        src="https://screens-image-components-public.s3.eu-north-1.amazonaws.com/world-map-2d.png"
                        alt="World map of attack origins"
                        className="object-cover w-full h-full"
                      />
                      <span className="size-2.5 rounded-full bg-red-600 absolute left-[48%] top-[62%]" />
                      <span className="size-2.5 rounded-full bg-red-600 absolute left-[56%] top-[36%]" />
                      <span className="size-2.5 rounded-full bg-red-600 absolute left-[58%] top-[42%]" />
                      <span className="size-2.5 rounded-full bg-red-600 absolute left-[78%] top-[56%]" />
                    </div>
                    <div className="text-sm leading-[20px] flex flex-col gap-2">
                      <div className="flex justify-between">
                        <span>1. Maharashtra</span>
                        <span className="text-[#9f9fa9]">412 threats</span>
                      </div>
                      <div className="flex justify-between">
                        <span>2. Punjab</span>
                        <span className="text-[#9f9fa9]">289 threats</span>
                      </div>
                      <div className="flex justify-between">
                        <span>3. Kerala</span>
                        <span className="text-[#9f9fa9]">201 threats</span>
                      </div>
                      <div className="flex justify-between">
                        <span>4. Manipur</span>
                        <span className="text-[#9f9fa9]">156 threats</span>
                      </div>
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-900 border-red-600/15 border-1 border-solid flex p-8 flex-col gap-6">
                    <h2 className="font-semibold text-lg leading-[28px]">
                      Detection Model Confidence
                    </h2>
                    <div className="flex flex-col items-center gap-3">
                      <div className="size-40 bg-[conic-gradient(#10b981_0deg_347deg,oklch(0.274_0.006_286.033)_347deg_360deg)] rounded-full flex justify-center items-center">
                        <div className="size-28 rounded-full bg-zinc-900 flex justify-center items-center">
                          <span className="font-semibold text-2xl leading-[32px]">
                            96.4%
                          </span>
                        </div>
                      </div>
                      <p className="text-center text-[#9f9fa9] text-xs leading-[16px]">
                        AI classifier accuracy, last 30 days
                      </p>
                    </div>
                  </div>
                  <div className="rounded-2xl bg-zinc-900 border-red-600/15 border-1 border-solid flex p-8 flex-col gap-6">
                    <h2 className="font-semibold text-lg leading-[28px]">
                      Active Alerts
                    </h2>
                    <div className="flex flex-col gap-4">
                      <div className="flex items-start gap-3">
                        <div className="size-9 shrink-0 rounded-xl bg-red-400/15 flex justify-center items-center">
                          <ShieldAlert className="size-4 text-red-400" />
                        </div>
                        <div>
                          <p className="text-sm leading-[20px]">
                            Spoofed domain cluster detected
                          </p>
                          <p className="text-[#9f9fa9] text-xs leading-[16px]">
                            2 min ago
                          </p>
                        </div>
                      </div>
                      <div className="flex items-start gap-3">
                        <div className="size-9 shrink-0 rounded-xl bg-amber-400/15 flex justify-center items-center">
                          <MapPin className="size-4 text-amber-400" />
                        </div>
                        <div>
                          <p className="text-sm leading-[20px]">
                            Unusual login geolocation
                          </p>
                          <p className="text-[#9f9fa9] text-xs leading-[16px]">
                            18 min ago
                          </p>
                        </div>
                      </div>
                      <div className="flex items-start gap-3">
                        <div className="size-9 shrink-0 rounded-xl bg-amber-400/15 flex justify-center items-center">
                          <Forward className="size-4 text-amber-400" />
                        </div>
                        <div>
                          <p className="text-sm leading-[20px]">
                            Bulk forwarding rule created
                          </p>
                          <p className="text-[#9f9fa9] text-xs leading-[16px]">
                            40 min ago
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </main>
          </div>
        </div>
      </div>
    </div>
  );
}
