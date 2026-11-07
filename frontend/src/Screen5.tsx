import { useEffect } from "react";
import {
  AlertTriangle,
  Bell,
  ChevronDown,
  Download,
  FileText,
  LayoutDashboard,
  MapPin,
  Search,
  Settings,
  Shield,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";

export function Screen5() {
  return (
    <div>
      <div className="bg-zinc-950 text-neutral-50 w-full h-fit h-fit min-h-screen w-screen min-w-screen max-w-screen overflow-visible">
        <div className="bg-zinc-950 flex w-[1140px] h-[956px] overflow-hidden">
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
                className="rounded-2xl text-[#9f9fa9] flex px-3 py-2.5 items-center gap-3"
              >
                <AlertTriangle className="size-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Threats
                </span>
              </a>
              <a
                href="#"
                className="rounded-2xl bg-[#155dfc] text-[#1c398e] flex px-3 py-2.5 items-center gap-3"
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
              <div className="size-10 font-semibold rounded-full bg-[#155dfc] text-[#1c398e] text-sm leading-[20px] flex justify-center items-center">
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
          <div className="min-w-0 bg-zinc-950 flex flex-col flex-1">
            <header className="bg-zinc-950 flex px-8 py-5 justify-between items-center gap-6 w-full">
              <div className="min-w-0 flex items-center gap-3">
                <h1 className="truncate font-semibold text-neutral-50 text-xl leading-[28px]">
                  Geolocation
                </h1>
              </div>
              <div className="min-w-[420px] max-w-lg flex-1">
                <div className="relative">
                  <Search className="top-1/2 -translate-y-1/2 size-4 text-[#9f9fa9] absolute left-4" />
                  <input
                    type="text"
                    placeholder="Search threats, senders, IPs, domains..."
                    className="outline-none rounded-full bg-zinc-800 text-neutral-50 text-sm leading-[20px] pl-11 pr-4 w-full h-11"
                    defaultValue=""
                  />
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="rounded-full bg-zinc-800 flex px-4 py-2 items-center gap-2">
                  <span className="size-2 rounded-full bg-red-600" />
                  <span className="whitespace-nowrap font-medium text-neutral-50 text-sm leading-[20px]">
                    Threat Level: Elevated
                  </span>
                </div>
                <button className="relative size-10 rounded-full text-[#9f9fa9] flex justify-center items-center">
                  <Bell className="size-5" />
                  <span className="size-5 font-semibold rounded-full bg-[#155dfc] text-[#1c398e] text-[10px] flex absolute -right-1 -top-1 justify-center items-center">
                    7
                  </span>
                </button>
                <button className="rounded-full flex pl-1 pr-2 py-1 items-center gap-2">
                  <span className="size-9 font-semibold rounded-full bg-[#155dfc] text-[#1c398e] text-sm leading-[20px] flex justify-center items-center">
                    JM
                  </span>
                  <ChevronDown className="size-4 text-[#9f9fa9]" />
                </button>
              </div>
            </header>
            <main className="overflow-y-auto p-8 flex-1">
              <div className="flex flex-col gap-6">
                <div className="flex justify-between items-end gap-6">
                  <div className="flex flex-col gap-2">
                    <h2 className="font-semibold text-neutral-50 text-2xl leading-[32px]">
                      Threat Origin Map
                    </h2>
                    <p className="text-[#9f9fa9] text-sm leading-[20px]">
                      Geographic distribution of detected threats
                    </p>
                  </div>
                  <div className="flex items-center gap-3">
                    <Select defaultValue="Last 24 hours">
                      <SelectTrigger className="rounded-xl bg-zinc-900 border-white/10 border-0 border-solid w-40">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Last 24 hours">
                          Last 24 hours
                        </SelectItem>
                        <SelectItem value="Last 7 days">Last 7 days</SelectItem>
                        <SelectItem value="Last 30 days">
                          Last 30 days
                        </SelectItem>
                      </SelectContent>
                    </Select>
                    <Select defaultValue="All Types">
                      <SelectTrigger className="rounded-xl bg-zinc-900 border-white/10 border-0 border-solid w-36">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="All Types">All Types</SelectItem>
                        <SelectItem value="Phishing">Phishing</SelectItem>
                        <SelectItem value="Malware">Malware</SelectItem>
                      </SelectContent>
                    </Select>
                    <Button
                      variant="outline"
                      className="bg-transparent rounded-xl border-white/10 border-0 border-solid"
                    >
                      <Download className="size-4" />
                      Export Map Data
                    </Button>
                  </div>
                </div>
                <Card className="rounded-2xl bg-zinc-900 border-white/10 border-0 border-solid p-6 gap-4">
                  <CardHeader className="p-0 flex-row justify-between items-center gap-3">
                    <CardTitle className="text-neutral-50 text-lg leading-[28px]">
                      Threat Origin Map
                    </CardTitle>
                    <Tabs defaultValue="pins">
                      <TabsList className="rounded-xl bg-zinc-800">
                        <TabsTrigger value="heatmap">Heatmap</TabsTrigger>
                        <TabsTrigger value="pins">Pins</TabsTrigger>
                      </TabsList>
                    </Tabs>
                  </CardHeader>
                  <CardContent className="p-0">
                    <div className="relative rounded-xl bg-neutral-950 h-[390px] overflow-hidden">
                      <img
                        src="https://screens-image-components-public.s3.eu-north-1.amazonaws.com/world-map-2d.png"
                        alt="Dark world map showing threat origins"
                        className="object-cover grayscale contrast-125 brightness-[0.35] opacity-80 w-full h-full"
                      />
                      <div className="bg-neutral-950/35 absolute inset-0" />
                      <div className="flex absolute left-[30%] top-[57%] flex-col items-center gap-1">
                        <MapPin className="fill-red-600 size-7 text-red-600" />
                        <span className="rounded-lg bg-zinc-950/80 text-neutral-50 text-xs leading-[16px] px-2 py-1">
                          High-risk origin
                        </span>
                      </div>
                      <div className="absolute left-[34%] top-[51%]">
                        <MapPin className="fill-amber-500 size-6 text-amber-500" />
                      </div>
                      <div className="absolute left-[78%] top-[67%]">
                        <MapPin className="fill-amber-500 size-6 text-amber-500" />
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter className="px-0 pt-2 pb-0 gap-6">
                    <div className="text-[#9f9fa9] text-sm leading-[20px] flex items-center gap-2">
                      <span className="size-3 rounded-full bg-red-600" />
                      High-risk origin
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-[20px] flex items-center gap-2">
                      <span className="size-3 rounded-full bg-amber-500" />
                      Suspicious origin
                    </div>
                    <div className="text-[#9f9fa9] text-sm leading-[20px] flex items-center gap-2">
                      <span className="size-3 rounded-full bg-yellow-400" />
                      Volume of threats
                    </div>
                  </CardFooter>
                </Card>
                <div className="grid grid-cols-2 gap-6">
                  <Card className="rounded-2xl bg-zinc-900 border-white/10 border-0 border-solid p-6 gap-4">
                    <CardHeader className="p-0 gap-1">
                      <CardTitle className="text-neutral-50 text-lg leading-[28px]">
                        Selected Region
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="flex p-0 flex-col gap-4">
                      <div>
                        <div className="font-semibold text-neutral-50 text-xl leading-[28px]">
                          Mumbai, Maharashtra
                        </div>
                        <div className="text-[#9f9fa9] text-sm leading-[20px]">
                          412 threats
                        </div>
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <div className="text-[#9f9fa9] text-xs leading-[16px]">
                            Network
                          </div>
                          <div className="text-neutral-50 text-sm leading-[20px]">
                            AS29465 MTN Nigeria
                          </div>
                        </div>
                        <div>
                          <div className="text-[#9f9fa9] text-xs leading-[16px]">
                            Classification
                          </div>
                          <div className="font-medium text-red-500 text-sm leading-[20px]">
                            High risk
                          </div>
                        </div>
                      </div>
                      <div>
                        <div className="text-[#9f9fa9] text-xs leading-[16px]">
                          Top sender domains
                        </div>
                        <div className="text-neutral-50 text-sm leading-[20px]">
                          paypa1-secure.com
                        </div>
                        <div className="text-neutral-50 text-sm leading-[20px]">
                          paypal-verification.net
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                  <Card className="rounded-2xl bg-zinc-900 border-white/10 border-0 border-solid p-6 gap-4">
                    <CardHeader className="p-0 gap-1">
                      <CardTitle className="text-neutral-50 text-lg leading-[28px]">
                        Origin Breakdown
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="p-0">
                      <div className="grid grid-cols-3 text-[#9f9fa9] text-xs leading-[16px] border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid pb-3">
                        <span>Origin</span>
                        <span>Threats</span>
                        <span>Risk</span>
                      </div>
                      <div className="text-sm leading-[20px] flex pt-4 flex-col gap-4">
                        <div className="grid grid-cols-3">
                          <span className="text-neutral-50">
                            Mumbai, Maharashtra
                          </span>
                          <span className="text-neutral-50">412</span>
                          <span className="text-red-500">High</span>
                        </div>
                        <div className="grid grid-cols-3">
                          <span className="text-neutral-50">West Africa</span>
                          <span className="text-neutral-50">186</span>
                          <span className="text-amber-500">Suspicious</span>
                        </div>
                        <div className="grid grid-cols-3">
                          <span className="text-neutral-50">Australia</span>
                          <span className="text-neutral-50">94</span>
                          <span className="text-amber-500">Suspicious</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>
            </main>
          </div>
        </div>
      </div>
    </div>
  );
}
