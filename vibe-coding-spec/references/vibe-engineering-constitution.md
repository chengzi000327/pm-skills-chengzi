# Vibe Engineering Constitution (Platform-Gateway Preset)

> **定位说明**：这是一个 **preset**，不是默认 constitution。它适用于"网关 + 多 client / 多 provider adapter"形态的平台型项目。其他项目类型（纯前端、CLI、数据管线、库等）应使用 `constitution-template.md` 引导生成自己的 constitution。建议安装位置：`.specify/presets/platform-gateway/`，或在生成项目 constitution 时引用其中适用的条款。
>
> 采用本 preset 时同样遵循 `constitution-template.md` 的版本治理规则（semver、Last Amended、修订程序、Constitution Check gate）。

## Directory Philosophy

Organize by responsibility boundary, not file type.

```text
src/                 product control: config, lifecycle, patchers, UI
platform/            core gateway, domain model, router, runtime config
platform/clients/    client adapters
platform/providers/  provider/back-end adapters
scripts/             operational scripts
scripts/certification/ release certification, reports, release gate
test/                fast and focused tests
quality/             versioned quality evidence
docs/                architecture, design, runtime, specs, decisions
```

## Layer Rules

### Product Control

Put CLI/UI, config store, lifecycle management, local patch/restore, and status verification in `src/` or `src/product-control/`.

Do not put provider protocol fields or core routing logic here.

### Platform Core

Put neutral domain models, gateway, router, runtime config, and shared error model in `platform/`.

Core code must not contain provider-specific name branches such as `if provider == "x"` when a capability can represent the behavior.

### Client Adapters

`platform/clients/` converts external client input into the neutral domain model and renders platform responses back to client format.

Client adapters must not directly call providers or read secrets.

### Provider Adapters

`platform/providers/` declares provider profile, defaults, capabilities, limits, request builder, response parser, and event parser.

Provider adapters must not handle UI, user config patching, or client-specific rendering.

### Governance

Configuration, secret references, logs, audit, health checks, certification, and release gates are governance concerns. Keep them separate from domain logic.

## Neutral Domain Contract

Use a neutral model before writing adapters:

```ts
type PlatformRequest = {
  tenantId?: string;
  userId?: string;
  operation: string;
  resource: string;
  payload: Record<string, unknown>;
  options?: Record<string, unknown>;
  capabilities?: string[];
  traceId: string;
};

type PlatformResponse = {
  status: 'ok' | 'error' | 'partial';
  data?: unknown;
  events?: PlatformEvent[];
  usage?: Record<string, unknown>;
  error?: PlatformError;
  traceId: string;
};
```

## Capability-driven Rule

Prefer:

```js
if (provider.capabilities.streaming) {
  body.stream = true;
}
```

Avoid:

```js
if (provider.id === 'provider-a') {
  body.stream = true;
}
```

## Adapter Contract

Client Adapter:

```ts
interface ClientAdapter<ClientInput, ClientOutput> {
  id: string;
  parse(input: ClientInput): PlatformRequest;
  render(response: PlatformResponse): ClientOutput;
  validate?(input: ClientInput): ValidationResult;
}
```

Provider Adapter:

```ts
interface ProviderAdapter {
  id: string;
  profile: ProviderProfile;
  buildRequest(request: PlatformRequest, config: ProviderConfig): ProviderHttpRequest;
  parseResponse(response: ProviderHttpResponse): PlatformResponse;
  parseEvent?(chunk: unknown): PlatformEvent[];
  health?(config: ProviderConfig): Promise<HealthStatus>;
}
```

## Minimum Project Skeleton

```text
src/
platform/
platform/clients/
platform/providers/
scripts/certification/
test/
quality/V0.1/
docs/architecture/
```
