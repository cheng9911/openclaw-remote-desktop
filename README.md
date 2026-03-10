# openclaw-remote-desktop
 本项目构建了一个通过飞书聊天即可控制本地电脑的 AI 自动化系统。默认情况下，OpenClaw 部署在宿主机上时，AI Agent 运行在受限的沙盒环境中，只能访问本机工作区和系统资源，自动化能力局限于宿主机本身，无法直接操作其他设备。通过引入 OpenClaw Node、Tailscale 私有网络以及 Windows 自动化桥接（desktopctl），我们将执行能力从单一主机扩展到多台设备。Agent 仍在沙盒中运行，但任务可以通过 Node 协议转发到远程节点执行，实现跨沙盒、跨设备的控制。最终，AI 不再只控制部署 OpenClaw 的机器，而是通过统一的 Gateway 调度多台 Windows、Linux 等设备，形成一个可扩展的 多设备 AI 自动化控制网络。
