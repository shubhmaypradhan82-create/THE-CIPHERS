import { useEffect } from "react";
import {
  AlertTriangle,
  Ban,
  Bell,
  Check,
  ChevronDown,
  ChevronLeft,
  FileText,
  FolderPlus,
  LayoutDashboard,
  Map,
  MapPin,
  Search,
  Settings,
  Shield,
  ShieldX,
  Unlock,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export function Screen2() {
  return (
    <div>
      <div className="bg-zinc-950 text-neutral-50 w-full h-fit h-fit min-h-screen w-screen min-w-screen max-w-screen overflow-visible">
        <div className="bg-neutral-950 flex w-[1140px] h-[956px]">
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
                className="rounded-2xl bg-red-600 text-white flex px-3 py-2.5 items-center gap-3"
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
                <MapPin className="text-red-600 w-7 h-7" />
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
            <header className="flex px-8 py-5 justify-between items-center gap-6 w-full">
              <div className="min-w-0 flex items-center gap-3">
                <button className="rounded-full text-white/60 flex justify-center items-center w-8 h-8">
                  <ChevronLeft className="w-5 h-5" />
                </button>
                <h1 className="truncate font-semibold text-white text-xl leading-[28px]">
                  Threats
                </h1>
              </div>
              <div className="min-w-[360px] max-w-lg flex-1">
                <div className="relative">
                  <Search className="top-1/2 -translate-y-1/2 text-white/50 absolute left-4 w-4 h-4" />
                  <input
                    type="text"
                    placeholder="Search threats, senders, IPs, domains..."
                    className="rounded-full bg-[#1a1a1a] text-white text-sm leading-[20px] pl-11 pr-4 w-full h-11"
                    defaultValue=""
                  />
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="rounded-full bg-[#1a1a1a] flex px-4 py-2 items-center gap-2">
                  <span className="rounded-full bg-red-400 w-2.5 h-2.5" />
                  <span className="whitespace-nowrap font-medium text-white text-sm leading-[20px]">
                    Threat Level: Elevated
                  </span>
                </div>
                <button className="relative rounded-full text-white/60 flex justify-center items-center w-10 h-10">
                  <Bell className="w-5 h-5" />
                  <span className="font-semibold rounded-full bg-red-600 text-white text-[10px] flex absolute -right-1 -top-1 justify-center items-center w-5 h-5">
                    7
                  </span>
                </button>
                <button className="rounded-full flex pl-1 pr-2 py-1 items-center gap-2">
                  <span className="font-semibold rounded-full bg-red-600 text-white text-sm leading-[20px] flex justify-center items-center w-9 h-9">
                    JM
                  </span>
                  <ChevronDown className="text-white/60 w-4 h-4" />
                </button>
              </div>
            </header>
            <div className="p-8 flex-1 overflow-auto">
              <div className="flex mb-8 justify-between items-center gap-4">
                <div className="flex items-center gap-4">
                  <div className="rounded-2xl bg-red-600/10 border-red-600/30 border-1 border-solid flex px-5 py-3 flex-col items-center gap-1">
                    <span className="font-bold text-red-400 text-xl leading-[28px]">
                      94 / 100
                    </span>
                    <span className="font-bold text-red-400 text-xl leading-[28px]">
                      —
                    </span>
                    <span className="font-bold text-red-400 text-xl leading-[28px]">
                      Critical
                    </span>
                  </div>
                  <div className="rounded-full bg-red-600/10 border-red-600/30 border-1 border-solid flex px-4 py-2 items-center gap-2">
                    <ShieldX className="text-red-400 w-4 h-4" />
                    <span className="font-medium text-red-400 text-sm leading-[20px]">
                      Quarantined
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <Button className="rounded-xl bg-red-600 text-white gap-2">
                    <FolderPlus className="w-4 h-4" />
                    Escalate to Case
                  </Button>
                  <Button
                    variant="outline"
                    className="rounded-xl text-white border-red-600/30 border-0 border-solid gap-2"
                  >
                    <Unlock className="w-4 h-4" />
                    Release from Quarantine
                  </Button>
                  <Button className="rounded-xl bg-red-600 text-white gap-2">
                    <Ban className="w-4 h-4" />
                    Block Sender
                  </Button>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-6">
                <div className="col-span-2 flex flex-col gap-6">
                  <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/10 border-0 border-solid p-6 gap-5">
                    <CardHeader className="p-0 gap-1">
                      <CardTitle className="font-semibold text-base leading-[24px]">
                        Message Details
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm leading-[20px] flex p-0 flex-col gap-4">
                      <div className="flex gap-4">
                        <span className="shrink-0 text-white/50 w-24">
                          From
                        </span>
                        <span>{`PayPal Billing Team <billing@paypa1-secure.com>`}</span>
                      </div>
                      <div className="flex gap-4">
                        <span className="shrink-0 text-white/50 w-24">To</span>
                        <span>j.martinez@company.com</span>
                      </div>
                      <div className="flex gap-4">
                        <span className="shrink-0 text-white/50 w-24">
                          Subject
                        </span>
                        <span>Urgent: Verify your account</span>
                      </div>
                      <div className="flex gap-4">
                        <span className="shrink-0 text-white/50 w-24">
                          Date
                        </span>
                        <span>2024-06-03 09:41:12 UTC</span>
                      </div>
                      <div className="flex items-center gap-4">
                        <span className="shrink-0 text-white/50 w-24">
                          Reply-To
                        </span>
                        <span>support@paypa1-secure-verify.com</span>
                        <span className="font-medium rounded-full bg-red-600/10 text-red-400 text-[11px] border-red-600/30 border-1 border-solid px-2 py-0.5">
                          mismatched domain
                        </span>
                      </div>
                    </CardContent>
                  </Card>
                  <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/10 border-0 border-solid p-6 gap-5">
                    <CardHeader className="p-0 gap-1">
                      <CardTitle className="font-semibold text-base leading-[24px]">
                        AI Detection Signals
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm leading-[20px] flex p-0 flex-col gap-4">
                      <div className="flex justify-between">
                        <span className="flex items-center gap-2">
                          <span className="rounded-full bg-red-400 w-2.5 h-2.5" />
                          Lookalike domain (paypa1 vs paypal)
                        </span>
                        <span className="font-medium text-red-400">High</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="flex items-center gap-2">
                          <span className="rounded-full bg-red-400 w-2.5 h-2.5" />
                          Urgency language pattern detected
                        </span>
                        <span className="font-medium text-red-400">High</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="flex items-center gap-2">
                          <span className="rounded-full bg-amber-500 w-2.5 h-2.5" />
                          Sender reputation: first seen 3 days ago
                        </span>
                        <span className="font-medium text-amber-500">
                          Medium
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="flex items-center gap-2">
                          <span className="rounded-full bg-red-400 w-2.5 h-2.5" />
                          Embedded link mismatches display text
                        </span>
                        <span className="font-medium text-red-400">High</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="flex items-center gap-2">
                          <span className="rounded-full bg-blue-600 w-2.5 h-2.5" />
                          No DKIM/SPF alignment
                        </span>
                        <span className="font-medium text-red-400">High</span>
                      </div>
                    </CardContent>
                  </Card>
                  <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/10 border-0 border-solid p-6 gap-5">
                    <CardHeader className="p-0 gap-1">
                      <CardTitle className="font-semibold text-base leading-[24px]">
                        Email Body Preview
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="p-0">
                      <div className="rounded-xl bg-[#242424] flex p-5 flex-col gap-4">
                        <span className="font-bold text-sm leading-[20px]">
                          PayPal
                        </span>
                        <p className="text-sm leading-6">
                          We noticed unusual activity on your account. Click
                          below to verify your identity within 24 hours or your
                          account will be suspended.
                        </p>
                        <span className="underline text-red-400 text-sm leading-[20px]">
                          hxxp://paypa1-secure-verify.com/login
                        </span>
                      </div>
                    </CardContent>
                  </Card>
                  <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/10 border-0 border-solid p-6 gap-5">
                    <CardHeader className="p-0 gap-1">
                      <CardTitle className="font-semibold text-base leading-[24px]">
                        Embedded Links
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="p-0">
                      <table className="text-left text-sm leading-[20px] w-full">
                        <thead>
                          <tr className="text-white/50 border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid">
                            <th className="font-medium pr-3 py-3">URL</th>
                            <th className="font-medium pr-3 py-3">
                              Reputation
                            </th>
                            <th className="font-medium py-3">Redirect Chain</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td className="pr-3 py-4">
                              paypa1-secure-verify.com/login
                            </td>
                            <td className="pr-3 py-4">
                              <span className="font-medium rounded-full bg-red-600/10 text-red-400 text-[11px] border-red-600/30 border-1 border-solid px-2 py-1">
                                Malicious
                              </span>
                            </td>
                            <td className="py-4">
                              bit.ly/3xk9 → paypa1-secure-verify.com/login
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </CardContent>
                  </Card>
                </div>
                <div className="col-span-1 flex flex-col gap-6">
                  <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/10 border-0 border-solid p-6 gap-5">
                    <CardHeader className="p-0 gap-1">
                      <CardTitle className="font-semibold text-base leading-[24px]">{`Origin & Sender Geolocation`}</CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm leading-[20px] flex p-0 flex-col gap-4">
                      <div className="relative rounded-xl h-40 overflow-hidden">
                        <img
                          src="https://screens-image-components-public.s3.eu-north-1.amazonaws.com/city-map-2d.png"
                          alt="Mumbai, Maharashtra origin map"
                          className="object-cover w-full h-full"
                        />
                        <div className="left-1/2 top-1/2 -translate-x-1/2 -translate-y-full absolute">
                          <MapPin className="text-red-600 w-7 h-7" />
                        </div>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-white/50">IP</span>
                        <span>197.210.53.104</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-white/50">ISP</span>
                        <span className="text-right">Jio Communications</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-white/50">Coordinates</span>
                        <span className="text-right">6.5244° N, 3.3792° E</span>
                      </div>
                    </CardContent>
                    <CardFooter className="p-0">
                      <Button
                        variant="outline"
                        className="rounded-xl border-red-600/30 border-0 border-solid gap-2 w-full"
                      >
                        <Map className="w-4 h-4" />
                        View on Geolocation Map
                      </Button>
                    </CardFooter>
                  </Card>
                  <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/10 border-0 border-solid p-6 gap-5">
                    <CardHeader className="p-0 gap-1">
                      <CardTitle className="font-semibold text-base leading-[24px]">
                        Sender History
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm leading-[20px] flex p-0 flex-col gap-4">
                      <div className="flex justify-between">
                        <span className="text-white/50">First seen</span>
                        <span>3 days ago</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-white/50">
                          Total messages from sender
                        </span>
                        <span>6</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-white/50">Prior flags</span>
                        <span className="text-right">
                          4 malicious, 2 suspicious
                        </span>
                      </div>
                    </CardContent>
                  </Card>
                  <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/10 border-0 border-solid p-6 gap-5">
                    <CardHeader className="p-0 gap-1">
                      <CardTitle className="font-semibold text-base leading-[24px]">
                        Recommended Action
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="p-0">
                      <p className="text-sm leading-6">
                        High-confidence phishing attempt impersonating PayPal.
                        Recommend permanent block and user notification.
                      </p>
                    </CardContent>
                    <CardFooter className="p-0">
                      <Button className="rounded-xl bg-red-600 text-white gap-2 w-full">
                        <Check className="w-4 h-4" />
                        Apply Recommendation
                      </Button>
                    </CardFooter>
                  </Card>
                  <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/10 border-0 border-solid p-6 gap-5">
                    <CardHeader className="p-0 gap-1">
                      <CardTitle className="font-semibold text-base leading-[24px]">
                        Case Timeline
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm leading-[20px] flex p-0 flex-col gap-4">
                      <div className="flex gap-3">
                        <div className="flex flex-col items-center">
                          <span className="rounded-full bg-red-600 mt-1 w-2.5 h-2.5" />
                          <span className="bg-white/10 flex-1 w-px" />
                        </div>
                        <div>
                          <span>Detected</span>
                          <span className="block text-white/50 text-xs leading-[16px]">
                            09:41:12 UTC
                          </span>
                        </div>
                      </div>
                      <div className="flex gap-3">
                        <div className="flex flex-col items-center">
                          <span className="rounded-full bg-red-600 mt-1 w-2.5 h-2.5" />
                          <span className="bg-white/10 flex-1 w-px" />
                        </div>
                        <div>
                          <span>Auto-quarantined</span>
                          <span className="block text-white/50 text-xs leading-[16px]">
                            09:41:14 UTC
                          </span>
                        </div>
                      </div>
                      <div className="flex gap-3">
                        <div className="flex flex-col items-center">
                          <span className="rounded-full bg-red-600 mt-1 w-2.5 h-2.5" />
                          <span className="bg-white/10 flex-1 w-px" />
                        </div>
                        <div>
                          <span>Flagged for review</span>
                          <span className="block text-white/50 text-xs leading-[16px]">
                            09:44:02 UTC
                          </span>
                        </div>
                      </div>
                      <div className="flex gap-3">
                        <div className="flex flex-col items-center">
                          <span className="rounded-full bg-red-600 mt-1 w-2.5 h-2.5" />
                        </div>
                        <div>
                          <span>Assigned to A. Reyes</span>
                          <span className="block text-white/50 text-xs leading-[16px]">
                            09:50:31 UTC
                          </span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
