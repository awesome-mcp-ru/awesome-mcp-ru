# awesome-mcp-ru Standard

Version: `1.0.0-draft`

This standard describes the metadata expected for catalog entries and the badge levels shown in `README.md`.

## Required Metadata

Every file in `entries/` must include:

- `id`, `name`, `description`, and `category`
- `endpoint.url`, `endpoint.transport`, and `endpoint.auth`
- `maintainer.name` and `maintainer.contact`
- `tools`, `tools_count`, and `tools_lang`
- `hosting`, `license`, and `pricing`

`id` must be ASCII kebab-case and match the file name.

## Tier Rules

Tier 1 entries should have independently verifiable ownership or legal identity, public documentation, accurate tool metadata, and a reachable production endpoint.

Tier 2 entries are community entries with enough public metadata to compare and test, but without complete Tier 1 verification.

## Entry Quality

Good entries help users compare MCP servers quickly. Prefer factual descriptions, stable links, explicit auth modes, and focused example use cases. Avoid marketing copy, secrets, private implementation details, and unverified operational claims.
