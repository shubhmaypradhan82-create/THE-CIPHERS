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
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";

export function Screen9() {
  return (
    <div>
      <div className="bg-zinc-950 text-neutral-50 w-full h-fit h-fit min-h-screen w-screen min-w-screen max-w-screen overflow-visible">
        <div className="flex w-full h-full">
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
                className="rounded-2xl text-white/60 flex px-3 py-2.5 items-center gap-3"
              >
                <FileText className="w-5 h-5" />
                <span className="font-medium text-sm leading-[20px]">
                  Reports
                </span>
              </a>
              <a
                href="#"
                className="rounded-2xl bg-red-600 text-white border-white/80 border-t-0 border-r-0 border-b-0 border-l-4 border-solid flex px-3 py-2.5 items-center gap-3"
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
          <div className="min-h-screen bg-neutral-950 flex flex-col flex-1">
            <header className="bg-neutral-950 border-red-600/20 border-t-0 border-r-0 border-b-1 border-l-0 border-solid flex px-6 py-4 justify-between items-center flex-1 gap-4">
              <div className="max-w-md rounded-2xl bg-white/5 flex px-4 py-2.5 items-center flex-1 gap-3">
                <Search className="text-white/40 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search threats, senders, IPs, domains..."
                  className="bg-transparent outline-none text-white text-sm leading-[20px] flex-1"
                  defaultValue=""
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
            <main className="space-y-6 overflow-y-auto bg-neutral-950 p-8 flex-1">
              <div className="space-y-2">
                <h1 className="font-bold text-white text-3xl leading-[36px]">
                  Settings
                </h1>
                <p className="text-white/50 text-sm leading-[20px]">
                  Manage your account, team, and detection preferences.
                </p>
              </div>
              <div className="space-y-6">
                <div className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-1 border-solid p-6">
                  <div className="mb-6">
                    <h2 className="font-semibold text-white text-lg leading-[28px]">
                      Profile
                    </h2>
                  </div>
                  <div className="flex items-center gap-6">
                    <div className="shrink-0 font-semibold rounded-full bg-red-600 text-white text-2xl leading-[32px] flex justify-center items-center w-20 h-20">
                      P
                    </div>
                    <div className="grid grid-cols-3 flex-1 gap-4">
                      <div className="space-y-2">
                        <label className="text-white/50 text-xs leading-[16px]">
                          Full Name
                        </label>
                        <input
                          className="outline-none rounded-lg bg-[#111111] text-white text-sm leading-[20px] border-white/10 border-1 border-solid px-3 w-full h-10"
                          defaultValue="Prateek"
                        />
                      </div>
                      <div className="space-y-2">
                        <label className="text-white/50 text-xs leading-[16px]">
                          Role
                        </label>
                        <input
                          value="SOC Analyst"
                          readOnly={true}
                          className="outline-none rounded-lg bg-[#111111] text-white text-sm leading-[20px] border-white/10 border-1 border-solid px-3 w-full h-10"
                        />
                      </div>
                      <div className="space-y-2">
                        <label className="text-white/50 text-xs leading-[16px]">
                          Email
                        </label>
                        <input
                          className="outline-none rounded-lg bg-[#111111] text-white text-sm leading-[20px] border-white/10 border-1 border-solid px-3 w-full h-10"
                          defaultValue="prateek@theciphers.io"
                        />
                      </div>
                    </div>
                  </div>
                  <div className="flex pt-6 justify-end">
                    <Button className="rounded-lg bg-red-600 text-white px-5">
                      Save Changes
                    </Button>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-6">
                  <div className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-1 border-solid p-6">
                    <div className="mb-6">
                      <h2 className="font-semibold text-white text-lg leading-[28px]">
                        Notification Preferences
                      </h2>
                    </div>
                    <div className="space-y-5">
                      <div className="flex justify-between items-center">
                        <span className="text-white/80 text-sm leading-[20px]">
                          Critical threat alerts
                        </span>
                        <Switch defaultChecked={true} />
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-white/80 text-sm leading-[20px]">
                          Daily digest email
                        </span>
                        <Switch defaultChecked={true} />
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-white/80 text-sm leading-[20px]">
                          Weekly executive summary
                        </span>
                        <Switch defaultChecked={false} />
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-white/80 text-sm leading-[20px]">
                          SMS alerts for critical incidents
                        </span>
                        <Switch defaultChecked={false} />
                      </div>
                    </div>
                  </div>
                  <div className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-1 border-solid p-6">
                    <div className="mb-6">
                      <h2 className="font-semibold text-white text-lg leading-[28px]">
                        Detection Sensitivity
                      </h2>
                      <p className="text-white/50 text-sm leading-[20px] mt-2">
                        Adjust how aggressively the AI model flags suspicious
                        activity.
                      </p>
                    </div>
                    <div className="space-y-4">
                      <div className="text-white/60 text-sm leading-[20px] flex justify-between items-center">
                        <span>Conservative</span>
                        <span className="font-medium text-white">Balanced</span>
                        <span>Aggressive</span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="100"
                        className="accent-[#dc2626] w-full h-2"
                        defaultValue={50}
                      />
                      <p className="text-white/50 text-xs leading-[16px]">
                        Current threshold: 85/100 risk score triggers
                        auto-quarantine.
                      </p>
                    </div>
                  </div>
                </div>
                <div className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-1 border-solid p-6">
                  <div className="flex mb-6 justify-between items-center">
                    <h2 className="font-semibold text-white text-lg leading-[28px]">
                      Team Members
                    </h2>
                    <Button className="rounded-lg bg-red-600 text-white">
                      Invite Member
                    </Button>
                  </div>
                  <div className="grid grid-cols-3 font-medium uppercase text-white/40 text-xs leading-[16px] tracking-wide border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid pb-3">
                    <span>Name</span>
                    <span>Role</span>
                    <span>Access</span>
                  </div>
                  <div className="grid grid-cols-3 text-white/80 text-sm leading-[20px] border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid py-4">
                    <span>Prateek</span>
                    <span>SOC Analyst</span>
                    <span>Admin</span>
                  </div>
                  <div className="grid grid-cols-3 text-white/80 text-sm leading-[20px] border-white/10 border-t-0 border-r-0 border-b-1 border-l-0 border-solid py-4">
                    <span>J. Martinez</span>
                    <span>Security Lead</span>
                    <span>Admin</span>
                  </div>
                  <div className="grid grid-cols-3 text-white/80 text-sm leading-[20px] pt-4">
                    <span>S. Chen</span>
                    <span>Analyst</span>
                    <span>Viewer</span>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-6">
                  <div className="rounded-2xl bg-[#1a1a1a] border-red-600/20 border-1 border-solid p-6">
                    <h2 className="font-semibold text-white text-lg leading-[28px]">{`API & Integrations`}</h2>
                    <p className="text-white/50 text-sm leading-[20px] mt-3">
                      Manage API keys and connected tools from the API Access
                      page.
                    </p>
                    <Button
                      variant="outline"
                      className="rounded-lg text-white/70 border-white/15 border-0 border-solid mt-6"
                    >
                      Go to API Access
                    </Button>
                  </div>
                  <div className="rounded-2xl bg-[#1a1a1a] border-red-600/40 border-1 border-solid p-6">
                    <h2 className="font-semibold text-white text-lg leading-[28px]">
                      Danger Zone
                    </h2>
                    <p className="text-white/50 text-sm leading-[20px] mt-3">
                      Deactivate your account or transfer ownership.
                    </p>
                    <Button
                      variant="outline"
                      className="rounded-lg text-red-600 border-red-600 border-0 border-solid mt-6"
                    >
                      Deactivate Account
                    </Button>
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
