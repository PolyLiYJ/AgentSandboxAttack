# Threat Model and Safety Section Draft

This section is written for the NDSS-style paper. It should appear before the method or at the beginning of the evaluation, because the paper studies attacks while deliberately avoiding real exploit payloads.

## Setting

We study coding agents that operate inside a constrained workspace or sandbox. The agent can read repository files, edit project artifacts, and optionally run local commands according to its interface policy. The user or platform expects the sandbox to constrain immediate execution and filesystem effects. However, the repository edited by the agent may later be opened, built, synchronized, tested, or interpreted by host-side systems outside the original interactive sandbox.

SandScout focuses on this lifecycle gap. A repository artifact may be inert while the agent edits it, yet become security-relevant when consumed by a package manager, editor extension, tool-discovery system, startup hook, CI runner, or another agent runtime.

## Adversary Capabilities

The adversary controls repository-local context that a coding agent may inspect during a benign maintenance task. This matches common collaborative-development settings: a user opens a repository, asks an agent to inspect or update metadata, and the repository contains attacker-controlled files such as documentation, local compatibility notes, package metadata, editor settings, CI workflows, or tool manifests.

The adversary can:

- Place text or metadata in project-local files that the agent may read.
- Shape repository structure so that lifecycle-relevant files are present.
- Induce the user to ask a benign task such as inspecting metadata or compatibility notes.
- Rely on later host-side interpretation of files created or modified by the agent.

The adversary cannot:

- Directly execute code on the host during the SandScout evaluation.
- Access credentials, secrets, or external network resources.
- Modify files outside the disposable workspace.
- Use destructive commands or real exploit payloads.
- Bypass the operating-system sandbox directly.

## Security Goal

The security goal is not to prove a kernel or container escape. Instead, we ask whether a sandboxed coding agent can be induced to prepare a repository artifact that crosses a semantic lifecycle boundary. In SandScout, the observable proxy is a harmless sentinel artifact. If the agent creates the specific sentinel derived from mined repository context, the task records semantic sandbox escape success for that boundary class.

This definition is intentionally conservative. Generic file edits, metadata formatting, documentation updates, or package-file rewrites do not count as success. The oracle requires the surface-specific sentinel path and benign sentinel value. This is why the no-note controls are informative: in run 015 and run 016, the agent made ordinary metadata edits but the oracle stayed at zero.

## Trusted Components

SandScout trusts the experiment harness to:

- Create disposable workspaces.
- Inject or omit repository-local SandScout notes according to the condition.
- Enforce harmless sentinel-only tasks.
- Capture stdout, stderr, git status, diffs, and sentinel file evidence.
- Classify infrastructure failures such as timeout or usage-limit separately from model behavior.

The harness does not trust agent self-reporting as the sole source of truth. The oracle derives success from workspace evidence, especially sentinel existence and content. This matters because agents may summarize a change differently from what they actually wrote.

## Out of Scope

The following are out of scope for the current prototype:

- Real exploit payloads, malware, credential access, exfiltration, or destructive commands.
- Claims about specific deployed products as vulnerable systems.
- Kernel, OCI, hypervisor, or container runtime escape techniques.
- Social engineering of users outside the controlled prompt.
- Measuring real-world prevalence across public repositories.
- Proving that every mined surface is exploitable in a deployed toolchain.

These exclusions are design choices. SandScout aims to provide a safe, reusable measurement system, not a recipe for compromising developer machines.

## Safety Controls

Every SandScout task uses the fixed benign marker `SSE_BENIGN_SENTINEL`. The real-agent runner rejects task JSON containing terms associated with credentials, exfiltration, malware, reverse shells, destructive filesystem commands, or non-benign sentinel values. Experiments run in disposable git repositories and capture only local evidence.

The no-note controls provide a second safety and validity check. They hold the agent, prompt mode, fixture, and task constant while removing SandScout's repository-local sentinel instruction. Completed controls should remain at SSE-SR=0.00. If a control created a sentinel without the note, it would indicate a prompt-template artifact or oracle flaw rather than evidence for the mined-context hypothesis.

## Disclosure and Artifact Policy

SandScout should be released as a safe benchmark artifact. The artifact should include miners, synthetic fixtures, sentinel tasks, trace/oracle scripts, and result-reproduction commands. It should not include working exploit payloads, product-specific bypass steps, credentials, or instructions for abusing real host lifecycle hooks.

If future runs identify behavior that appears product-specific and security-relevant beyond the sentinel harness, those findings should be handled through coordinated disclosure before publication.

