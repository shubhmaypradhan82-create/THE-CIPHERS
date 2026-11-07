import { useEffect } from "react";
import {
  AlertTriangle,
  Bell,
  ChevronDown,
  ChevronLeft,
  Download,
  FileText,
  LayoutDashboard,
  MapPin,
  Search,
  Settings,
  Shield,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";

export function Screen4() {
  return (
    <div>
      <div className="bg-zinc-950 text-neutral-50 w-full h-fit h-fit min-h-screen w-screen min-w-screen max-w-screen overflow-visible">
        <div className="min-h-[956px] bg-neutral-950 flex w-full">
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
                className="rounded-2xl bg-red-600 text-white flex px-3 py-2.5 items-center gap-3"
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
                className="rounded-2xl text-white/60 flex px-3 py-2.5 items-center gap-3"
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
            <header className="bg-neutral-950 flex px-8 py-5 justify-between items-center gap-6 w-full">
              <div className="min-w-0 flex items-center gap-3">
                <button className="transition-colors rounded-full text-white/60 flex justify-center items-center w-9 h-9">
                  <ChevronLeft className="w-5 h-5" />
                </button>
              </div>
              <div className="min-w-[420px] max-w-xl flex-1">
                <div className="relative">
                  <Search className="top-1/2 -translate-y-1/2 text-white/50 absolute left-4 w-4 h-4" />
                  <input
                    type="text"
                    placeholder="Search threats, senders, IPs, domains..."
                    className="transition-shadow rounded-full bg-[#1a1a1a] text-white text-sm leading-[20px] pl-11 pr-4 w-full h-11"
                    defaultValue=""
                  />
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="rounded-full bg-[#1a1a1a] flex px-4 py-2 items-center gap-2">
                  <span className="rounded-full bg-red-600 w-2 h-2" />
                  <span className="whitespace-nowrap font-medium text-white text-sm leading-[20px]">
                    Threat Level: Elevated
                  </span>
                </div>
                <button className="relative transition-colors rounded-full text-white/60 flex justify-center items-center w-10 h-10">
                  <Bell className="w-5 h-5" />
                  <span className="font-semibold rounded-full bg-red-600 text-white text-[10px] flex absolute -right-1 -top-1 justify-center items-center w-5 h-5">
                    7
                  </span>
                </button>
                <button className="transition-colors rounded-full flex pl-1 pr-2 py-1 items-center gap-2">
                  <span className="font-semibold rounded-full bg-red-600 text-white text-sm leading-[20px] flex justify-center items-center w-9 h-9">
                    JM
                  </span>
                  <ChevronDown className="text-white/60 w-4 h-4" />
                </button>
              </div>
            </header>
            <main className="bg-neutral-950 flex p-8 flex-col flex-1 gap-6 overflow-auto">
              <div className="flex justify-between items-center gap-6">
                <h1 className="font-semibold text-white text-2xl leading-[32px]">
                  Geolocation Intelligence
                </h1>
                <div className="flex items-center gap-3">
                  <Select defaultValue="Last 24 hours">
                    <SelectTrigger className="rounded-xl bg-[#1a1a1a] border-red-600/20 border-0 border-solid w-40">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Last 24 hours">
                        Last 24 hours
                      </SelectItem>
                    </SelectContent>
                  </Select>
                  <Select defaultValue="All Types">
                    <SelectTrigger className="rounded-xl bg-[#1a1a1a] border-red-600/20 border-0 border-solid w-36">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="All Types">All Types</SelectItem>
                    </SelectContent>
                  </Select>
                  <Tabs defaultValue="Pins">
                    <TabsList className="rounded-xl bg-[#1a1a1a]">
                      <TabsTrigger value="Heatmap">Heatmap</TabsTrigger>
                      <TabsTrigger value="Pins">Pins</TabsTrigger>
                    </TabsList>
                  </Tabs>
                  <Button className="rounded-xl bg-red-600 text-white gap-2">
                    <Download className="w-4 h-4" />
                    Export Map Data
                  </Button>
                </div>
              </div>
              <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-0 border-solid p-6 gap-4">
                <CardHeader className="p-0 gap-2">
                  <CardTitle className="text-white text-lg leading-[28px]">
                    Threat Origin Map
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-0">
                  <div className="relative rounded-xl bg-[#080d18] h-[390px] overflow-hidden">
                    <img
                      src="https://screens-image-components-public.s3.eu-north-1.amazonaws.com/world-map-2d.png"
                      alt="World map showing threat origins"
                      className="object-cover opacity-90 [filter:grayscale(1)_brightness(.45)_contrast(1.15)] w-full h-full"
                    />
                    <div className="bg-[#080d18]/50 absolute inset-0" />
                    <MapPin className="size-7 fill-[#dc2626] text-red-600 absolute left-[56%] top-[52%]" />
                    <MapPin className="size-7 fill-[#f97316] text-orange-500 absolute left-[55%] top-[30%]" />
                    <MapPin className="size-7 fill-[#f97316] text-orange-500 absolute left-[57%] top-[35%]" />
                    <MapPin className="size-7 fill-[#f97316] text-orange-500 absolute left-[82%] top-[66%]" />
                  </div>
                  <div className="text-white/60 text-sm leading-[20px] flex pt-4 items-center gap-6">
                    <span className="flex items-center gap-2">
                      <span className="size-3 rounded-full bg-red-600" />
                      High-risk origin
                    </span>
                    <span className="flex items-center gap-2">
                      <span className="size-3 rounded-full bg-orange-500" />
                      Suspicious origin
                    </span>
                    <span className="flex items-center gap-2">
                      <span className="size-3 rounded-full bg-yellow-400" />
                      Volume of threats
                    </span>
                  </div>
                </CardContent>
              </Card>
              <div className="grid grid-cols-2 gap-6">
                <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-0 border-solid p-6 gap-6">
                  <CardHeader className="p-0 gap-2">
                    <CardTitle className="text-white text-lg leading-[28px]">
                      Selected Region
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="flex p-0 flex-col gap-4">
                    <h2 className="font-semibold text-white text-xl leading-[28px]">
                      Mumbai, Maharashtra
                    </h2>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="rounded-xl bg-[#111111] p-4">
                        <span className="block text-white/50 text-sm leading-[20px]">
                          Threats originating here
                        </span>
                        <strong className="text-white text-2xl leading-[32px]">
                          412
                        </strong>
                      </div>
                      <div className="rounded-xl bg-[#111111] p-4">
                        <span className="block text-white/50 text-sm leading-[20px]">
                          Primary ASN
                        </span>
                        <strong className="text-white text-base leading-[24px]">
                          AS55836 Reliance Jio Maharashtra
                        </strong>
                      </div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-white/50 text-sm leading-[20px]">
                        Risk classification
                      </span>
                      <Badge className="rounded-full bg-red-600 text-white">
                        High
                      </Badge>
                    </div>
                    <div>
                      <h3 className="font-semibold text-white mb-3">
                        Top Sender Domains
                      </h3>
                      <div className="text-white/70 text-sm leading-[20px] flex flex-col gap-2">
                        <span>paypa1-secure.com</span>
                        <span>secure-verify.com</span>
                        <span>lagos-asn.net</span>
                      </div>
                    </div>
                    <Button
                      variant="outline"
                      className="rounded-xl text-white border-red-600/40 border-0 border-solid"
                    >
                      View All Threats From Region
                    </Button>
                  </CardContent>
                </Card>
                <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-0 border-solid p-6 gap-6">
                  <CardHeader className="p-0 gap-2">
                    <CardTitle className="text-white text-lg leading-[28px]">
                      Origin Breakdown
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="p-0">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Country</TableHead>
                          <TableHead>Threat Count</TableHead>
                          <TableHead>Dominant Attack Type</TableHead>
                          <TableHead>Trend (7d)</TableHead>
                          <TableHead>Risk Level</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        <TableRow>
                          <TableCell>Maharashtra</TableCell>
                          <TableCell>412</TableCell>
                          <TableCell>Phishing</TableCell>
                          <TableCell className="text-red-600">+18%</TableCell>
                          <TableCell className="text-red-600">High</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Punjab</TableCell>
                          <TableCell>186</TableCell>
                          <TableCell>Credential theft</TableCell>
                          <TableCell>+9%</TableCell>
                          <TableCell className="text-orange-500">
                            Medium
                          </TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Kerala</TableCell>
                          <TableCell>129</TableCell>
                          <TableCell>Malware</TableCell>
                          <TableCell>+4%</TableCell>
                          <TableCell className="text-orange-500">
                            Medium
                          </TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Manipur</TableCell>
                          <TableCell>94</TableCell>
                          <TableCell>Impersonation</TableCell>
                          <TableCell>+2%</TableCell>
                          <TableCell className="text-yellow-400">Low</TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
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
