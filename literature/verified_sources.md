# Verified Source Notes

Verification date: 2026-06-13.

This file records source metadata checked against primary pages. It is not a final BibTeX file. Before camera-ready submission, fetch BibTeX programmatically from arXiv DOI/CrossRef/Semantic Scholar and compare against this table.

## Peer-Reviewed or arXiv Academic Sources

| Key | Verified Title | Authors | Status | DOI / URL | SandScout Positioning |
|---|---|---|---|---|---|
| `agentdojo2024` | AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents | Edoardo Debenedetti, Jie Zhang, Mislav Balunovic, Luca Beurer-Kellner, Marc Fischer, Florian Tramer | arXiv v3, submitted 2024-06-19, last revised 2024-11-24 | https://doi.org/10.48550/arXiv.2406.13352 | Tool-using agent prompt-injection benchmark; closest benchmark-style precedent but not sandbox-lifecycle focused. |
| `wasp2025` | WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks | Ivan Evtimov, Arman Zharmagambetov, Aaron Grattafiori, Chuan Guo, Kamalika Chaudhuri | arXiv v3, submitted 2025-04-22, last revised 2025-05-16 | https://doi.org/10.48550/arXiv.2504.18575 | Realistic web-agent hijacking benchmark; useful for decomposed end-to-end attack metrics. |
| `agentharm2024` | AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents | Maksym Andriushchenko et al. | arXiv v3, accepted at ICLR 2025 | https://doi.org/10.48550/arXiv.2410.09024 | Harmful multi-step agent capability benchmark; supports the need to evaluate tool-using agents beyond chatbot refusals. |
| `sweagent2024` | SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering | John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, Ofir Press | arXiv v3, submitted 2024-05-06, last revised 2024-11-11 | https://doi.org/10.48550/arXiv.2405.15793 | Establishes that agent-computer interfaces shape coding-agent behavior; SandScout studies the security consequences of those interfaces. |
| `sandboxescapebench2026` | Quantifying Frontier LLM Capabilities for Container Sandbox Escape | Rahul Marchand, Art O Cathain, Jerome Wynne, Philippos Maximos Giavridis, Sam Deverett, John Wilkinson, Jason Gwartz, Harry Coppock | arXiv v1, submitted 2026-03-01 | https://doi.org/10.48550/arXiv.2603.02277 | Adjacent sandbox benchmark focused on container/OCI breakout capability; SandScout targets repository semantic boundaries instead. |
| `codingassistantinjection2026` | Prompt Injection Attacks on Agentic Coding Assistants: A Systematic Analysis of Vulnerabilities in Skills, Tools, and Protocol Ecosystems | Narek Maloyan, Dmitry Namiot | arXiv v1, submitted 2026-01-24 | https://doi.org/10.48550/arXiv.2601.17548 | SoK/taxonomy for coding-assistant prompt injection, skills, tools, and protocol ecosystems; useful threat-model background. |

## Non-Peer-Reviewed Motivation Sources

| Key | Source | Use | Caution |
|---|---|---|---|
| `cymulate_sandbox_escape` | Cymulate blog on configuration-based sandbox escape in AI coding tools | Motivation for semantic/configuration-based sandbox failure modes | Treat as industry report, not peer-reviewed evidence. Do not claim product vulnerabilities beyond what the source states. |
| `cymulate_codex_cli` | Cymulate blog on Codex CLI RCE/prompt-injection mitigations | Motivation for CLI-level prompt-injection and host-context risks | Use only for motivation and responsible-disclosure context. |

## Related-Work Gap Statement

The verified literature supports a clean gap statement:

Existing agent-security benchmarks measure prompt injection in tool/web agents, harmful agent tasks, coding-agent interface performance, or direct container sandbox escape. SandScout studies a different boundary: repository-local artifacts created inside a coding-agent sandbox that are later interpreted by host-side lifecycle systems such as package managers, editors, tool discovery, startup metadata, or CI.

