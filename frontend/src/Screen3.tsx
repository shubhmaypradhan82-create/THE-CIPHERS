import { useEffect } from "react";
import {
  AlertTriangle,
  Bell,
  ChevronDown,
  Clock,
  Download,
  FileText,
  Layers,
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
  CardDescription,
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

export function Screen3() {
  return (
    <div>
      <div className="bg-zinc-950 text-neutral-50 w-full h-fit h-fit min-h-screen w-screen min-w-screen max-w-screen overflow-visible">
        <div className="min-h-[956px] bg-zinc-950 flex w-full">
          <aside className="shrink-0 bg-zinc-950 flex flex-col w-64 h-full">
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
                className="rounded-2xl bg-red-600 text-white flex px-3 py-2.5 items-center gap-3"
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
          <div className="min-w-0 bg-zinc-950 flex flex-col flex-1">
            <header className="flex px-8 py-5 justify-between items-center gap-6 w-full">
              <div className="min-w-0 flex items-center gap-3">
                <h1 className="truncate font-semibold text-neutral-50 text-xl leading-[28px]">
                  Geolocation Intelligence
                </h1>
              </div>
              <div className="min-w-[420px] max-w-md flex-1">
                <div className="relative">
                  <Search className="top-1/2 -translate-y-1/2 size-4 text-[#9f9fa9] absolute left-4" />
                  <input
                    type="text"
                    placeholder="Search threats, senders, IPs, domains..."
                    className="rounded-full bg-zinc-900 text-neutral-50 text-sm leading-[20px] pl-11 pr-4 w-full h-11"
                    defaultValue=""
                  />
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="rounded-full bg-zinc-900 flex px-4 py-2 items-center gap-2">
                  <span className="size-2.5 rounded-full bg-green-500" />
                  <span className="whitespace-nowrap font-medium text-neutral-50 text-sm leading-[20px]">
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
            <main className="space-y-6 p-8 flex-1 overflow-auto">
              <div className="space-y-2">
                <h2 className="font-semibold text-neutral-50 text-2xl leading-[32px]">
                  Geolocation Intelligence
                </h2>
                <p className="text-[#9f9fa9] text-sm leading-[20px]">
                  Track threat origins and identify geographic patterns across
                  your security events.
                </p>
              </div>
              <div className="flex justify-between items-center gap-4">
                <div className="flex items-center gap-3">
                  <Select defaultValue="Last 24 hours">
                    <SelectTrigger className="rounded-xl bg-zinc-900 border-white/10 border-0 border-solid w-44">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Last 24 hours">
                        Last 24 hours
                      </SelectItem>
                      <SelectItem value="Last 7 days">Last 7 days</SelectItem>
                      <SelectItem value="Last 30 days">Last 30 days</SelectItem>
                    </SelectContent>
                  </Select>
                  <Select defaultValue="All Types">
                    <SelectTrigger className="rounded-xl bg-zinc-900 border-white/10 border-0 border-solid w-36">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="All Types">All Types</SelectItem>
                      <SelectItem value="Malware">Malware</SelectItem>
                      <SelectItem value="Phishing">Phishing</SelectItem>
                    </SelectContent>
                  </Select>
                  <Tabs defaultValue="pins">
                    <TabsList className="rounded-xl bg-zinc-900">
                      <TabsTrigger value="heatmap" className="rounded-lg gap-2">
                        <Layers className="size-4" />
                        Heatmap
                      </TabsTrigger>
                      <TabsTrigger value="pins" className="rounded-lg gap-2">
                        <MapPin className="size-4" />
                        Pins
                      </TabsTrigger>
                    </TabsList>
                  </Tabs>
                </div>
                <Button variant="outline" className="rounded-xl gap-2">
                  <Download className="size-4" />
                  Export Map Data
                </Button>
              </div>
              <Card className="rounded-2xl bg-zinc-900 border-white/10 border-0 border-solid p-6 gap-4">
                <CardHeader className="flex p-0 flex-row justify-between items-center gap-4">
                  <div>
                    <CardTitle className="text-neutral-50 text-lg leading-[28px]">
                      Threat Origin Map
                    </CardTitle>
                    <CardDescription className="text-[#9f9fa9] mt-1">
                      Geographic distribution of detected threats
                    </CardDescription>
                  </div>
                  <div className="text-[#9f9fa9] text-sm leading-[20px] flex items-center gap-2">
                    <Clock className="size-4" />
                    Updated just now
                  </div>
                </CardHeader>
                <CardContent className="p-0">
                  <div className="relative bg-[oklch(0.12_0.02_250)] rounded-xl h-[390px] overflow-hidden">
                    <img
                      src="https://screens-image-components-public.s3.eu-north-1.amazonaws.com/world-map-2d.png"
                      alt="Dark world map showing threat origins"
                      className="object-cover grayscale opacity-30 w-full h-full"
                    />
                    <div className="bg-[oklch(0.08_0.02_250/.52)] absolute inset-0" />
                    <div className="flex absolute left-[45%] top-[55%] flex-col items-center">
                      <MapPin className="fill-red-600 size-8 text-red-600" />
                      <span className="rounded-lg bg-zinc-950/80 text-neutral-50 text-xs leading-[16px] px-2 py-1">
                        Mumbai, Maharashtra
                      </span>
                    </div>
                    <MapPin className="fill-amber-500 size-7 text-amber-500 absolute left-[47%] top-[34%]" />
                    <MapPin className="fill-amber-500 size-7 text-amber-500 absolute left-[69%] top-[57%]" />
                    <div className="rounded-xl bg-zinc-950/80 absolute left-4 bottom-4 p-4">
                      <div className="text-[#9f9fa9] text-xs leading-[16px] flex items-center gap-6">
                        <span className="flex items-center gap-2">
                          <span className="size-2.5 rounded-full bg-red-600" />
                          High-risk origin
                        </span>
                        <span className="flex items-center gap-2">
                          <span className="size-2.5 rounded-full bg-amber-500" />
                          Suspicious origin
                        </span>
                        <span className="flex items-center gap-2">
                          <span className="size-2.5 rounded-full bg-yellow-400" />
                          Volume of threats
                        </span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
              <div className="grid grid-cols-3 gap-6">
                <Card className="rounded-2xl bg-zinc-900 border-white/10 border-0 border-solid p-6 gap-4">
                  <CardHeader className="p-0 gap-2">
                    <CardTitle className="text-neutral-50 text-lg leading-[28px]">
                      Selected Region
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="p-0 gap-4">
                    <div className="flex items-center gap-3">
                      <div className="rounded-xl bg-red-600/15 p-3">
                        <MapPin className="size-6 text-red-500" />
                      </div>
                      <div>
                        <p className="font-semibold text-neutral-50">
                          Mumbai, Maharashtra
                        </p>
                        <p className="text-[#9f9fa9] text-sm leading-[20px]">
                          High-risk origin
                        </p>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-[#9f9fa9] text-xs leading-[16px]">
                          Threats
                        </p>
                        <p className="font-semibold text-neutral-50 text-xl leading-[28px]">
                          1,284
                        </p>
                      </div>
                      <div>
                        <p className="text-[#9f9fa9] text-xs leading-[16px]">
                          Risk score
                        </p>
                        <p className="font-semibold text-red-500 text-xl leading-[28px]">
                          92%
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
                <Card className="col-span-2 rounded-2xl bg-zinc-900 border-white/10 border-0 border-solid p-6 gap-4">
                  <CardHeader className="p-0 gap-2">
                    <CardTitle className="text-neutral-50 text-lg leading-[28px]">
                      Origin Breakdown
                    </CardTitle>
                    <CardDescription className="text-[#9f9fa9]">
                      Threat activity by geographic origin
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="p-0">
                    <div className="grid grid-cols-[1.5fr_1fr_1fr] text-[#9f9fa9] text-xs leading-[16px] border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid pb-3">
                      <span>Region</span>
                      <span>Threats</span>
                      <span>Risk level</span>
                    </div>
                    <div className="grid grid-cols-[1.5fr_1fr_1fr] text-sm leading-[20px] border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid py-4">
                      <span className="text-neutral-50">
                        Mumbai, Maharashtra
                      </span>
                      <span className="text-neutral-50">1,284</span>
                      <span className="text-red-500">High risk</span>
                    </div>
                    <div className="grid grid-cols-[1.5fr_1fr_1fr] text-sm leading-[20px] border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid py-4">
                      <span className="text-neutral-50">Eastern Europe</span>
                      <span className="text-neutral-50">746</span>
                      <span className="text-amber-400">Suspicious</span>
                    </div>
                    <div className="grid grid-cols-[1.5fr_1fr_1fr] text-sm leading-[20px] pt-4">
                      <span className="text-neutral-50">South America</span>
                      <span className="text-neutral-50">391</span>
                      <span className="text-amber-400">Suspicious</span>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </main>
          </div>
        </div>
      </div>
    </div>
  );
}
