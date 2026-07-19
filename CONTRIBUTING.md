# Contributing

Thanks for improving `awesome-mcp-ru`. Keep submissions small, verifiable, and aligned with the catalog schema.

## Add Or Update An Entry

1. Add or edit one file in `entries/<id>.yaml`.
2. Keep `id` equal to the file name without `.yaml`.
3. Use an HTTPS endpoint URL and the closest schema category.
4. Set `tools_count` to the public total. The `tools` list can include a representative subset when the server exposes many tools.
5. Add or update a focused test in `tests/` when the entry needs invariants beyond the shared schema.
6. Regenerate `README.md` with:

```bash
python3 -m generator.build --output README.md
```

## Validate

Run the catalog checks before opening a pull request:

```bash
python3 -m pytest
```

Do not include credentials, private endpoints, or unverified claims in entries.
