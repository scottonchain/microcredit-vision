# OMNEQUA DNS cutover: applied, verification pending

Written by Codex (AI), October 13, 2026.

The authorized DNS changes were applied at approximately 23:13–23:14 UTC. **The website switch is not yet verified complete.** At 23:18 UTC www reached `active` for overall, provider and SSL status. At 23:19 UTC the apex provider remained `active`, but overall status was `pending` with SSL `pending_validation`. HTTPS checks from the execution environment were blocked by its proxy with CONNECT 403. No persistent access or credential configuration was changed.

This supersedes the credential-access blocker in the [earlier continuation](../omnequa-domain-switch-20261013-2250.md). Authentication succeeded through the existing network-secret proxy. The ordinary vault environment variable was not used, and no credentials are included here.

## Evidence

- `rollback.json`: full authenticated pre-change DNS export, all 17 records on one page, checked against the API's total count and unique record IDs.
- `preflight-second-read.json`: independent complete read matching the rollback records exactly before changes. A further immediate comparison also passed before execution.
- `sites-targets.json`: refreshed targets from the two existing Sites attachments.
- `change-plan.json`: intended record-level requests, without headers or credentials. The original www ID became stale during execution; this plan is historical, not a replay script.
- `write-results.json`: successful response records and the recovered 404.
- `after.json`: complete post-change zone, 22 records. All 15 records outside apex A and www CNAME are identical to the rollback records, including their IDs, TTLs and every returned field.
- `verification-read.json`: later complete authenticated read matching the 22-record post-change zone exactly.
- `sites-status.json`: latest Sites verification response for both existing attachments.

## Applied changes

| Record | Result |
| --- | --- |
| A @ | Replaced WebsiteBuilder Site entry with 162.159.143.30; HTTP 200 |
| A @ | Added 172.66.3.26; HTTP 201 |
| CNAME www | Changed to custom-domains.chatgpt.site.; HTTP 200 after resolving changed record ID |
| TXT _openai-site-verification | Added exact Sites value; HTTP 201 |
| TXT _cf-custom-hostname | Added exact Sites value; HTTP 201 |
| TXT _openai-site-verification.www | Added exact Sites value; HTTP 201 |
| TXT _cf-custom-hostname.www | Added exact Sites value; HTTP 201 |

Web records retain TTL 3600; new verification records use TTL 600. No AAAA records were present. Existing MX, SPF, DMARC, Microsoft service records, NS, SOA and domain-connect records were preserved. There were no preexisting values at the new verification TXT names to replace. No duplicate site, domain attachment, registration or schedule was created.

The apex update caused the www CNAME's provider-assigned ID to change while preserving its old value. The first www request therefore returned 404. Execution stopped, read the full current zone, verified unchanged unrelated records, then performed a second matching current read before updating the newly returned www ID. Successful apex writes were not replayed.

## Rollback guidance

The export preserves the original provider representation, including `WebsiteBuilder Site` at the apex. That string is not an IPv4 address and must not be blindly submitted as a normal A record. Restoring the managed WebsiteBuilder association may require GoDaddy's supported website/domain connection workflow. The earlier public DNS snapshot recorded 13.248.243.5 and 76.223.105.230, but those historical addresses are not a substitute for restoring the managed association.

For a rollback, first read the current zone and reconcile against these receipts. Restore the original www CNAME value using its current record ID; remove only the newly created verification records and second apex record identified by the successful receipts; restore the apex through the appropriate supported provider workflow. Preserve concurrent and unrelated changes. This is guidance, not an instruction to execute a rollback now.

## Outstanding acceptance

The operator reported `ERR_SSL_VERSION_OR_CIPHER_MISMATCH` at the apex at approximately 23:16 UTC. DNS was already changed while the apex certificate was still awaiting validation; this is consistent with reaching the new endpoint before certificate issuance. This diagnosis is based on the reported browser error and Sites state, not a direct TLS handshake from this environment. By 23:18 www's certificate and domain were active, so the two hostnames differed. Sites returned no error and no additional non-null certificate-validation record for the apex. Preserve the correct DNS and allow certificate provisioning/propagation to continue, refreshing the existing attachment. Do not disable certificate checks or remove/recreate attachments as a workaround.

The complete API readback confirms the intended zone configuration, not global DNS propagation. Still required: active Sites ownership and certificates for both hostnames, authoritative/public DNS resolution, valid hostname certificates, and replacement page identity/content at both HTTPS URLs. The replacement origin is https://omnequa.solarghost3.chatgpt.site. The prior replacement title was “More ways to earn. Fewer barriers to start. | Omnequa”; historical September text is not itself a failure.

The environment currently rejects HTTPS verification requests to the apex, www, replacement origin and dns.google with CONNECT 403. A separate web reader still returned the closure-page text at the apex and could not read the other URLs; its cached/freshness ambiguity prevents a propagation conclusion. Do not mark the switch complete from these observations. The exact access dependency is an already-permitted verification path to those hosts; no settings were broadened by this task.

The existing publication, sponsor-identity and distribution restrictions remain unchanged. This record is operational evidence and does not publish a new blog post.
