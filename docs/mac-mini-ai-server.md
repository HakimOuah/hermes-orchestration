# Mac mini AI Server

## Target machine

- Mac mini M4 Pro
- 48 GB unified memory
- 512 GB internal storage

## Intended responsibilities

The Mac mini should become the primary local AI workstation/server:
- Hermes backend and agent runtime;
- MLX-based local inference where appropriate;
- local model storage and serving;
- browser/tool automation;
- research jobs that can run for hours;
- optional n8n and lightweight internal services;
- remote access from another machine if useful.

## Local model philosophy

Prefer models that leave enough free unified memory for macOS, Hermes, browser processes, and normal desktop work. A model that technically fits but leaves the system constantly under memory pressure is not a good production choice.

Initial model families should be re-evaluated when the hardware arrives. Current likely candidates are strong 20B–35B-class quantized models, especially efficient MoE architectures.

## MLX vs other runtimes

MLX should be tested first because it is designed for Apple Silicon. Ollama / llama.cpp remain useful for convenience and compatibility. The final choice should be based on measured:
- tokens/sec;
- memory use;
- context handling;
- tool-calling reliability;
- Hermes integration stability.

## Storage

512 GB may become restrictive once several model weights, caches, Docker images, repos, and datasets accumulate. Consider an external high-speed USB4/Thunderbolt NVMe SSD for model weights and archives while keeping frequently used system files on internal storage.

## Remote access

Optional architecture:

```text
MacBook / phone
      |
   Tailscale
      |
Mac mini at home
      |
Hermes + local LLMs + tools
```

The local system should start automatically after reboot and recover cleanly from crashes before being trusted for unattended jobs.

## Gaming coexistence

The Mac mini can also remain a normal desktop/gaming machine. Heavy local inference and GPU-heavy games may compete for unified memory/GPU resources, so large research jobs can be queued or throttled during active gaming sessions.