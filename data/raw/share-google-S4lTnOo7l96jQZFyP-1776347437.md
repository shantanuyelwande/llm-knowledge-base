# Building with Modal and the OpenAI Agents SDK

**Source:** [https://share.google/S4lTnOo7l96jQZFyP](https://share.google/S4lTnOo7l96jQZFyP)
**Scraped:** 2026-04-16T13:50:37.535454

---

GLM-5.1 is available to try on Modal. [Get started](/glm-5-endpoint)

[ ![Modal logo](/_app/immutable/assets/logo.lottie.CgmMXf1s.png)](/)

Product 

Solutions 

Resources 

[Customers](/customers)[Pricing](/pricing)[Docs](/docs)

[Log In](/login?next=%2Fapps) [ Sign Up ](/signup?next=%2Fapps)

[ All posts](/blog)

[ Back](/blog)

Engineering

April 15, 2026•8 minute read

# Building with Modal and the OpenAI Agents SDK

![author](https://modal-cdn.com/cdnbot/erikbutterrzcow7hv_48afa478.webp)

[Erik Dunteman@erikdunteman](https://twitter.com/erikdunteman)

Member of the technical staff

Today, OpenAI [launches their Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/), a powerful tool for building agent harnesses for coding, deep research, and more.

Internal agents are a fresh topic, with companies such as [Ramp](https://ramp.com/) building out a fleet of [background coding agents on Modal](https://modal.com/blog/how-ramp-built-a-full-context-background-coding-agent-on-modal), which are now responsible for more than half of the PRs created.

While many businesses are becoming familiar with off-the-shelf agent harnesses such as Codex, Claude Code, and OpenCode, many are left wondering how to customize these agents and build them into powerful internal tools in the same way Ramp did.

We’re excited to see the OpenAI Agents SDK, because we believe it provides the right building blocks for teams to build their own agentic systems in-house. The SDK plugs neatly into Modal via a sandbox extension, giving agents a home computer to work on, and it comes with the right tools to truly take advantage of the scale Modal is known for.

Today we’ll show you how to build a custom agent harness, from scratch, on top of the OpenAI Agents SDK. We’ll integrate Modal Sandboxes, to give those agents computers (even GPUs) to run in. By the end, we’ll have a general-purpose coding harness with the ability to massively parallelize tasks in the background.

![](https://modal-cdn.com/cdnbot/openai agent sdk codegjz0od9k_24dba652.webp)

Our example will use OpenAI’s [Parameter Golf](https://openai.com/index/parameter-golf/) challenge, which prompts participants to cram a baseline threshold of intelligence into as few parameters as possible. Our agent harness will be able to tackle this task and parallelize it across many subagents running on GPUs, each coding and training with the goal of discovering new state-of-the-art approaches for efficiency.

Relevant code blocks will be shared as we go, for example, but you can always refer to the [complete project code here.](https://github.com/modal-labs/openai-agents-python-example)

## Starting with the most basic coding agent

First, we'll build a minimal coding agent with the OpenAI Agents SDK. This approach is unsafe and not recommended, but we start here for simplicity.

An `Agent` is a for-loop with an LLM running `tools` (functions) to task completion. The set of tools and state you build around the core `Agent` loop is often called a "Harness".

The simplest coding agent is an agent with an `exec(command)` function it may invoke to run an arbitrary shell command on the host:

While simple, this could quickly become a security disaster with a malicious prompt or low quality model.

## Moving the agent into a Sandbox

Sandboxes are isolated linux environments built on top of VMs or security-hardened containers. We can make the `exec` command safer by running it in this environment, effectively making the LLM _see_ the sandbox rather than our host.

The OpenAI Agents SDK gives us a handy `SandboxAgent` class, a superset of `Agent` which comes preloaded with the tools to attach to a remotely running sandbox. It also offers a `ShellTool` class which adds extra guardrails to our commands. Under the hood, it manages a `ModalSandboxSession` which is the client to the remote sandbox.

One primary distinction with these sandbox tools is they're now stateful, bound to that specific instance of a `ModalSandboxSession`, so we define a `Capability` which are ways to bind a set of tools to an instance.

We’ll also want to attach GPUs to our sandbox, which is a capability unique to Modal. We can request GPUs for our sandbox using `ModalSandboxClientOptions`.

### Training MNIST with a One-Shot prompt

Our agent harness, with a sandbox capability and a shell tool, is now fully capable of running a coding task end-to end. Let's have it train an image model on the MNIST dataset!

Out of the box, this should just work.

# Building the ultimate harness

The harness is everything around the agent loops that gives them the context and tools needed. Building a harness can feel like product engineering, because it's all totally in your control as a programmer. The OpenAI Agents SDK makes it easy to build up extra capabilities around a core agent loop.

Now, we'll just slowly chip away at adding new features to our harness until it reliably runs `Parameter Golf` experiments.

### Adding Memory with Sessions

By default, `Agents` are stateless. The run method takes string context in, and returns a string output. If you were to put a default agent on a loop with user-prompted input, the model _won't_ see the accumulated conversation.

`Sessions` are our solutions - they are objects you can pass across your agent runs to accumulate the context window, across multiple user prompts and even across agent instances if you'd like.

Let's add a session to the run:

In solving multi-turn memory, we introduce a new challenge: context management and [context rot](https://www.trychroma.com/research/context-rot). Now that memory accumulates indefinitely, we need to get smart about controlling and resetting it.

Most of the work we do next is focused on _protecting_ our primary thread of work from context bloat.

### Adding Subagents for higher-order planning and context delegation

Coding agents can be incredibly token-heavy as they explore and modify a codebase and ingest stdout/stderr. The effective lifetime of one of these agents is short.

To allow for long-horizon work, we split our agent into two agents: [An orchestrator](https://developers.openai.com/api/docs/guides/agents/orchestration), and a subagent.

![](https://modal-cdn.com/cdnbot/image \(4\)o0ddm_4o_c267737c.webp)

The orchestrator is our main chat agent, which accumulates memory for the entire task. It has a tool - `invoke_subagent` \- which is itself an agent with a completely fresh context window and `Session`. This allows work to get split into short bursts, the orchestrator concerned only for high-level details, and subagents spawned for brief focused tasks, with their session memory scrapped once the task is done.

The task description goes in, the subagent responds with a summary of work done, keeping orchestrator context tight and unconcerned with implementation details.

### Making it async and parallel with a Subagent Pool

Rather than our subagent runs being blocking, pausing the orchestrator, we can increase experiment throughput by allowing the orchestrator to manage _multiple_ parallel subagents, using a worker pool

We implement a `SubAgentPool` class, which is a key:value set of active subagents, and we attach it to the orchestrator instance. With this, we can modify the `invoke_subagent` to instead store an `asyncio.Future`, and expose new tools to allow the orchestrator to selectively wait for specific threads of work to finish:

Now that the orchestrator doesn't block by default, we need ways for the orchestrator to see what's going on in the subagents.

We implement this in two ways, using `Hooks` to track the current active tool for each subagent, and adding a `set_status` tool for the subagent to periodically update its status without fully exiting back to the orchestrator.

These subagent fields are made visible to the orchestrator via a list_subagents tool:

It took a great deal of ["encouragement"](https://github.com/modal-labs/openai-agents-python-example/blob/64a2b7badba13e111a92a23a6f1c70aabdaca763/orchestrator.py#L18) to keep the orchestrator from exiting before its async tasks finished. Future work, as an exercise for the reader, could included implementing a special "self thought" tool or subagent to give the orchestrator a productive outlet for thinking/planning rather than waiting for subagent results or exiting early.

### Limiting GPU spend with quotas

With async tasks, we're handing LLMs the potentially expensive ability to spin up unbounded amounts of GPU subagents. We can simply add a quota system to the subagent pool to ensure a fixed limit of expensive 8x H100s are in use.

### Now we can parallel train MNIST

Now that the orchestrator can manage parallel work, let's try parallelizing mnist across different backends with a prompt like:

The orchestrator, whose only access to a coding environments is via its async subagent spawn interface, will naturally spawn three parallel subagents for each of three ML frameworks.

### Using Filesystem Snapshots to deduplicate work

We can now start dumping context for `Parameter Golf` into the prompt.

But we quickly hit another challenge!

With subagents all starting from base sandboxes, they each waste precious GPU time doing the same setup work - pulling the repo and installing dependencies. Over longer-horizon tasks, you can imagine all sorts of "checkpoint" moments where you'd want to store the sandbox state to allow future fresh subagents to start from that point.

We add Filesystem Snapshots to freeze an active sandbox session into an ID, which the orchestrator may later refer too as a starting image for a new subagent, allowing it to branch work from known checkpoints.

In addition to the time savings, the added benefit of filesystem snapshots is `context management`. Filesystems can be used to offload memory!

Just like we keep context hot in `Session` state, the filesystem of a live sandbox also acts as an implicit form of memory when viewed via shell tools.

A stateful filesystem allows the artifacts produced by a prior agent be available to all future agents, even if the future agents don't have it explicitly put into their context `Sessions`. This on-disk memory can either be implemented explicitly, via writing skills/memory files, or implicitly by the nature of the codebase already having been put in a working state.

Now, the orchestrator can progress threads of work, snapshot that filesystem, and then drop fresh subagents into that snapshot with basic follow-up instructions and the subagent will quickly be able to get its bearings and resume work, without the context bloat of the work that led to this point.

### Adding a skills subsystem

Our final step for running `Parameter Golf` efficiently is prompting!

Currently it takes extensive prompting to get the orchestrator to use its async research tools effectively, and to understand the specific `Parameter Golf` challenge we're giving it. We could add those prompts into the core harness, but to keep the harness general purpose we instead give the orchestrator tools to selectively opt-into this context via a list of `Skills` plugins.

## We've now built parallel auto-research on GPUs!

We've started with a basic, locally-executing agent loop. Secured it with remote sandboxes. Scaled it with async workers. And given it pluggable skills to run `Parameter Golf` research, in parallel, autonomously.

Run it with:

If there's anything to take away from this blog, it's the understanding that you can _compose_ systems on top of your base agent loops to suit it for your task.

In our case, we built an harness that keeps context lean for an orchestrator, and takes full advantage of the parallelism of Modal's sandbox platform. All of this has been made incredibly simple and composable thanks to the OpenAI Agent SDK. It's been a blast to build with and we hope you take this project as an inspiration to build your own thing!

Remember to refer to the [full example repo](https://github.com/modal-labs/openai-agents-python-example) as you build, and when it’s time for sandboxes and GPUs, sign up for [Modal](https://modal.com) and get $30 free credits to start building on!

## Ship your first app in minutes. 

[Get Started ](/signup)

$30 / month free compute

[![Modal logo](data:image/svg+xml,%3csvg%20width='368'%20height='192'%20viewBox='0%200%20368%20192'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20d='M148.873%204L183.513%2064L111.922%20188C110.492%20190.47%20107.853%20192%20104.993%20192H40.3325C38.9025%20192%2037.5325%20191.62%2036.3325%20190.93C35.1325%20190.24%2034.1226%20189.24%2033.4026%20188L1.0725%20132C-0.3575%20129.53%20-0.3575%20126.48%201.0725%20124L70.3625%204C71.0725%202.76%2072.0925%201.76001%2073.2925%201.07001C74.4925%200.380007%2075.8625%200%2077.2925%200H141.952C144.812%200%20147.453%201.53%20148.883%204H148.873ZM365.963%20124L296.672%204C295.962%202.76%20294.943%201.76001%20293.743%201.07001C292.543%200.380007%20291.173%200%20289.743%200H225.083C222.223%200%20219.583%201.53%20218.153%204L183.513%2064L255.103%20188C256.533%20190.47%20259.173%20192%20262.033%20192H326.693C328.122%20192%20329.492%20191.62%20330.693%20190.93C331.893%20190.24%20332.902%20189.24%20333.622%20188L365.953%20132C367.383%20129.53%20367.383%20126.48%20365.953%20124H365.963Z'%20fill='%2362DE61'/%3e%3cpath%20d='M109.623%2064H183.523L148.883%204C147.453%201.53%20144.813%200%20141.953%200H77.2925C75.8625%200%2074.4925%200.380007%2073.2925%201.07001L109.623%2064Z'%20fill='url\(%23paint0_linear_342_139\)'/%3e%3cpath%20d='M109.623%2064L73.2925%201.07001C72.0925%201.76001%2071.0825%202.76%2070.3625%204L1.0725%20124C-0.3575%20126.48%20-0.3575%20129.52%201.0725%20132L33.4026%20188C34.1126%20189.24%2035.1325%20190.24%2036.3325%20190.93L109.613%2064H109.623Z'%20fill='url\(%23paint1_linear_342_139\)'/%3e%3cpath%20d='M183.513%2064H109.613L36.3325%20190.93C37.5325%20191.62%2038.9025%20192%2040.3325%20192H104.993C107.853%20192%20110.492%20190.47%20111.922%20188L183.513%2064Z'%20fill='%2309AF58'/%3e%3cpath%20d='M365.963%20132C366.673%20130.76%20367.033%20129.38%20367.033%20128H294.372L258.042%20190.93C259.242%20191.62%20260.612%20192%20262.042%20192H326.703C329.563%20192%20332.202%20190.47%20333.632%20188L365.963%20132Z'%20fill='%2309AF58'/%3e%3cpath%20d='M225.083%200C223.653%200%20222.283%200.380007%20221.083%201.07001L294.362%20128H367.023C367.023%20126.62%20366.663%20125.24%20365.953%20124L296.672%204C295.242%201.53%20292.603%200%20289.743%200H225.073H225.083Z'%20fill='url\(%23paint2_linear_342_139\)'/%3e%3cpath%20d='M258.033%20190.93L294.362%20128L221.083%201.07001C219.883%201.76001%20218.873%202.76%20218.153%204L183.513%2064L255.103%20188C255.813%20189.24%20256.833%20190.24%20258.033%20190.93Z'%20fill='url\(%23paint3_linear_342_139\)'/%3e%3cdefs%3e%3clinearGradient%20id='paint0_linear_342_139'%20x1='155.803'%20y1='80'%20x2='101.003'%20y2='-14.93'%20gradientUnits='userSpaceOnUse'%3e%3cstop%20stop-color='%23BFF9B4'/%3e%3cstop%20offset='1'%20stop-color='%2380EE64'/%3e%3c/linearGradient%3e%3clinearGradient%20id='paint1_linear_342_139'%20x1='8.62251'%20y1='174.93'%20x2='100.072'%20y2='16.54'%20gradientUnits='userSpaceOnUse'%3e%3cstop%20stop-color='%2380EE64'/%3e%3cstop%20offset='0.18'%20stop-color='%237BEB63'/%3e%3cstop%20offset='0.36'%20stop-color='%236FE562'/%3e%3cstop%20offset='0.55'%20stop-color='%235ADA60'/%3e%3cstop%20offset='0.74'%20stop-color='%233DCA5D'/%3e%3cstop%20offset='0.93'%20stop-color='%2318B759'/%3e%3cstop%20offset='1'%20stop-color='%2309AF58'/%3e%3c/linearGradient%3e%3clinearGradient%20id='paint2_linear_342_139'%20x1='340.243'%20y1='143.46'%20x2='248.793'%20y2='-14.93'%20gradientUnits='userSpaceOnUse'%3e%3cstop%20stop-color='%23BFF9B4'/%3e%3cstop%20offset='1'%20stop-color='%2380EE64'/%3e%3c/linearGradient%3e%3clinearGradient%20id='paint3_linear_342_139'%20x1='284.822'%20y1='175.47'%20x2='193.372'%20y2='17.0701'%20gradientUnits='userSpaceOnUse'%3e%3cstop%20stop-color='%2380EE64'/%3e%3cstop%20offset='0.18'%20stop-color='%237BEB63'/%3e%3cstop%20offset='0.36'%20stop-color='%236FE562'/%3e%3cstop%20offset='0.55'%20stop-color='%235ADA60'/%3e%3cstop%20offset='0.74'%20stop-color='%233DCA5D'/%3e%3cstop%20offset='0.93'%20stop-color='%2318B759'/%3e%3cstop%20offset='1'%20stop-color='%2309AF58'/%3e%3c/linearGradient%3e%3c/defs%3e%3c/svg%3e)](/)

[](https://x.com/modal) [](https://www.linkedin.com/company/modal-labs/) [](https://modal.com/slack) [](https://github.com/modal-labs) [](https://www.youtube.com/channel/UC477UdoLR2Js3RHhRWSXsQA)

© Modal 2026

Products

[Modal Inference](/products/inference)

[Modal Sandboxes](/products/sandboxes)

[Modal Training](/products/training)

[Modal Notebooks](/products/notebooks)

[Modal Batch](/products/batch)

[Modal Core Platform](/products/platform)

Resources

[Documentation](/docs/guide)

[Pricing](/pricing)

[Slack Community](/slack)

[Articles](/articles)

[GPU Glossary](/gpu-glossary)

[LLM Engine Advisor](/llm-almanac)

[Model Library](/library)

Popular Examples

[Serve your own LLM API](/docs/examples/llm_inference)

[Create custom art of your pet](/docs/examples/diffusers_lora_finetune)

[Analyze Parquet files from S3 with DuckDB](/docs/examples/s3_bucket_mount)

[Run hundreds of LoRAs from one app](/docs/examples/cloud_bucket_mount_loras)

[Finetune an LLM to replace your CEO](/docs/examples/llm-finetuning)

Company

[About](/company)

[Blog](/blog)

[Careers](/careers)

[Events](/events)

[Privacy Policy](/legal/privacy-policy)

[Security & Privacy](/docs/guide/security)

[Terms](/legal/terms)

[](https://x.com/modal) [](https://www.linkedin.com/company/modal-labs/) [](https://modal.com/slack) [](https://github.com/modal-labs) [](https://www.youtube.com/channel/UC477UdoLR2Js3RHhRWSXsQA)

© Modal 2026
