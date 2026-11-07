import { useEffect } from "react";
import {
  AlertTriangle,
  ArrowRight,
  Bell,
  ChevronDown,
  FileText,
  LayoutDashboard,
  MapPin,
  Plus,
  Search,
  Settings,
  Shield,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export function Screen7() {
  return (
    <div>
      <div className="bg-zinc-950 text-neutral-50 w-full h-fit h-fit min-h-screen w-screen min-w-screen max-w-screen overflow-visible">
        <div className="min-h-screen flex w-full h-full">
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
                className="rounded-2xl bg-red-600 text-white flex px-3 py-2.5 items-center gap-3"
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
            <main className="flex p-8 flex-col flex-1 gap-6 overflow-auto">
              <div className="flex justify-between items-end gap-4">
                <div className="flex flex-col gap-2">
                  <h1 className="font-semibold text-white text-3xl leading-[36px] tracking-tight">
                    Forensics
                  </h1>
                  <p className="text-white/50 text-sm leading-[20px]">
                    Investigate and build evidence for confirmed threat
                    clusters.
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Select defaultValue="all">
                  <SelectTrigger className="rounded-2xl bg-[#1a1a1a] text-white border-white/10 border-0 border-solid w-44">
                    <SelectValue placeholder="All Statuses" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Statuses</SelectItem>
                    <SelectItem value="open">Open</SelectItem>
                    <SelectItem value="review">Under Review</SelectItem>
                    <SelectItem value="closed">Closed</SelectItem>
                  </SelectContent>
                </Select>
                <Select defaultValue="all">
                  <SelectTrigger className="rounded-2xl bg-[#1a1a1a] text-white border-white/10 border-0 border-solid w-44">
                    <SelectValue placeholder="All Severities" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Severities</SelectItem>
                    <SelectItem value="critical">Critical</SelectItem>
                    <SelectItem value="high">High</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                  </SelectContent>
                </Select>
                <div className="rounded-2xl bg-[#1a1a1a] border-white/10 border-1 border-solid flex px-4 py-2.5 items-center gap-2 w-64">
                  <Search className="size-4 text-white/40" />
                  <input
                    type="text"
                    placeholder="Search cases..."
                    className="min-w-0 bg-transparent outline-none text-white text-sm leading-[20px] flex-1"
                    defaultValue=""
                  />
                </div>
                <Button className="rounded-2xl bg-red-600 text-white ml-auto px-5">
                  <Plus className="size-4 mr-2" />
                  New Case
                </Button>
              </div>
              <div className="flex flex-col gap-4">
                <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-0 border-solid p-6 gap-4">
                  <CardContent className="flex p-0 justify-between items-center gap-6">
                    <div className="min-w-0 flex flex-col flex-1 gap-3">
                      <div className="flex items-center gap-3">
                        <h2 className="font-semibold text-white text-base leading-[24px]">
                          Phishing Campaign — PayPal Impersonation Cluster
                        </h2>
                        <Badge className="rounded-full bg-red-600/20 text-red-400">
                          Open
                        </Badge>
                      </div>
                      <div className="text-white/50 text-xs leading-[16px] flex items-center gap-6">
                        <span>
                          Severity
                          <strong className="font-medium text-red-400 ml-1">
                            Critical
                          </strong>
                        </span>
                        <span>
                          Owner
                          <strong className="font-medium text-white/80 ml-1">
                            Prateek
                          </strong>
                        </span>
                        <span>
                          Opened
                          <strong className="font-medium text-white/80 ml-1">
                            2024-06-03
                          </strong>
                        </span>
                      </div>
                      <p className="text-white/60 text-sm leading-[20px]">
                        Coordinated lookalike-domain phishing impersonating
                        PayPal, 3 correlated senders, shared infrastructure.
                      </p>
                      <div className="flex items-center gap-3">
                        <span className="text-white/50 text-xs leading-[16px]">
                          Confidence
                        </span>
                        <div className="rounded-full bg-white/10 w-40 h-2">
                          <div className="rounded-full bg-red-600 w-[96%] h-2" />
                        </div>
                        <span className="font-semibold text-white text-sm leading-[20px]">
                          96%
                        </span>
                      </div>
                    </div>
                    <Button
                      variant="outline"
                      className="rounded-2xl bg-white/5 text-white border-white/10 border-0 border-solid"
                    >
                      View Case
                      <ArrowRight className="size-4 ml-2" />
                    </Button>
                  </CardContent>
                </Card>
                <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-0 border-solid p-6 gap-4">
                  <CardContent className="flex p-0 justify-between items-center gap-6">
                    <div className="min-w-0 flex flex-col flex-1 gap-3">
                      <div className="flex items-center gap-3">
                        <h2 className="font-semibold text-white text-base leading-[24px]">
                          Business Email Compromise — Vendor Invoice Fraud
                        </h2>
                        <Badge className="rounded-full bg-red-600/20 text-red-400">
                          Open
                        </Badge>
                      </div>
                      <div className="text-white/50 text-xs leading-[16px] flex items-center gap-6">
                        <span>
                          Severity
                          <strong className="font-medium text-red-400 ml-1">
                            High
                          </strong>
                        </span>
                        <span>
                          Owner
                          <strong className="font-medium text-white/80 ml-1">
                            Prateek
                          </strong>
                        </span>
                        <span>
                          Opened
                          <strong className="font-medium text-white/80 ml-1">
                            2024-06-01
                          </strong>
                        </span>
                      </div>
                      <p className="text-white/60 text-sm leading-[20px]">
                        Spoofed vendor invoice requesting urgent wire transfer,
                        mismatched reply-to domain, 2 correlated senders.
                      </p>
                      <div className="flex items-center gap-3">
                        <span className="text-white/50 text-xs leading-[16px]">
                          Confidence
                        </span>
                        <div className="rounded-full bg-white/10 w-40 h-2">
                          <div className="rounded-full bg-red-600 w-[91%] h-2" />
                        </div>
                        <span className="font-semibold text-white text-sm leading-[20px]">
                          91%
                        </span>
                      </div>
                    </div>
                    <Button
                      variant="outline"
                      className="rounded-2xl bg-white/5 text-white border-white/10 border-0 border-solid"
                    >
                      View Case
                      <ArrowRight className="size-4 ml-2" />
                    </Button>
                  </CardContent>
                </Card>
                <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-0 border-solid p-6 gap-4">
                  <CardContent className="flex p-0 justify-between items-center gap-6">
                    <div className="min-w-0 flex flex-col flex-1 gap-3">
                      <div className="flex items-center gap-3">
                        <h2 className="font-semibold text-white text-base leading-[24px]">
                          Credential Harvesting — Microsoft 365 Lookalike
                        </h2>
                        <Badge className="rounded-full bg-amber-500/20 text-amber-400">
                          Under Review
                        </Badge>
                      </div>
                      <div className="text-white/50 text-xs leading-[16px] flex items-center gap-6">
                        <span>
                          Severity
                          <strong className="font-medium text-red-400 ml-1">
                            High
                          </strong>
                        </span>
                        <span>
                          Owner
                          <strong className="font-medium text-white/80 ml-1">
                            Prateek
                          </strong>
                        </span>
                        <span>
                          Opened
                          <strong className="font-medium text-white/80 ml-1">
                            2024-05-28
                          </strong>
                        </span>
                      </div>
                      <p className="text-white/60 text-sm leading-[20px]">
                        Fake Microsoft login page distributed via email, hosted
                        on newly registered domain.
                      </p>
                      <div className="flex items-center gap-3">
                        <span className="text-white/50 text-xs leading-[16px]">
                          Confidence
                        </span>
                        <div className="rounded-full bg-white/10 w-40 h-2">
                          <div className="rounded-full bg-red-600 w-[88%] h-2" />
                        </div>
                        <span className="font-semibold text-white text-sm leading-[20px]">
                          88%
                        </span>
                      </div>
                    </div>
                    <Button
                      variant="outline"
                      className="rounded-2xl bg-white/5 text-white border-white/10 border-0 border-solid"
                    >
                      View Case
                      <ArrowRight className="size-4 ml-2" />
                    </Button>
                  </CardContent>
                </Card>
                <Card className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-0 border-solid p-6 gap-4">
                  <CardContent className="flex p-0 justify-between items-center gap-6">
                    <div className="min-w-0 flex flex-col flex-1 gap-3">
                      <div className="flex items-center gap-3">
                        <h2 className="font-semibold text-white text-base leading-[24px]">
                          Malware Delivery — Invoice Attachment Campaign
                        </h2>
                        <Badge className="rounded-full bg-white/10 text-white/50">
                          Closed
                        </Badge>
                      </div>
                      <div className="text-white/50 text-xs leading-[16px] flex items-center gap-6">
                        <span>
                          Severity
                          <strong className="font-medium text-amber-400 ml-1">
                            Medium
                          </strong>
                        </span>
                        <span>
                          Owner
                          <strong className="font-medium text-white/80 ml-1">
                            Prateek
                          </strong>
                        </span>
                        <span>
                          Opened
                          <strong className="font-medium text-white/80 ml-1">
                            2024-05-20
                          </strong>
                        </span>
                      </div>
                      <p className="text-white/60 text-sm leading-[20px]">
                        Malicious macro-enabled attachment distributed to
                        finance team, contained and remediated.
                      </p>
                      <div className="flex items-center gap-3">
                        <span className="text-white/50 text-xs leading-[16px]">
                          Confidence
                        </span>
                        <div className="rounded-full bg-white/10 w-40 h-2">
                          <div className="rounded-full bg-red-600 w-[94%] h-2" />
                        </div>
                        <span className="font-semibold text-white text-sm leading-[20px]">
                          94%
                        </span>
                      </div>
                    </div>
                    <Button
                      variant="outline"
                      className="rounded-2xl bg-white/5 text-white border-white/10 border-0 border-solid"
                    >
                      View Case
                      <ArrowRight className="size-4 ml-2" />
                    </Button>
                  </CardContent>
                </Card>
              </div>
              <div className="text-white/50 text-sm leading-[20px] border-white/10 border-t-1 border-r-0 border-b-0 border-l-0 border-solid flex pt-5 justify-between items-center">
                <span>Showing 4 of 4 cases</span>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    disabled={true}
                    className="rounded-xl bg-white/5 text-white/40 border-white/10 border-0 border-solid"
                  >
                    Previous
                  </Button>
                  <Button
                    variant="outline"
                    className="rounded-xl bg-red-600/15 text-red-400 border-red-600/30 border-0 border-solid"
                  >
                    1
                  </Button>
                  <Button
                    variant="outline"
                    disabled={true}
                    className="rounded-xl bg-white/5 text-white/40 border-white/10 border-0 border-solid"
                  >
                    Next
                  </Button>
                </div>
              </div>
            </main>
          </div>
        </div>
      </div>
    </div>
  );
}
