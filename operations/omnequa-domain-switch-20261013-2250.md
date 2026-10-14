# OMNEQUA domain switch: continuation prerequisites

Written by Codex (AI), October 13, 2026, approximately 22:48–22:55 UTC.

**Cutover remains incomplete. No DNS changes or authenticated GoDaddy requests were made.** This supplements [the earlier handoff](omnequa-domain-switch-20261013-2230.md); it does not replace its rollback requirements.

## Fresh results

- The existing Sites project remains active at https://omnequa.solarghost3.chatgpt.site. No new site or domain attachment was created.
- Explicit Sites refreshes at 22:48:51 and 22:48:55 UTC returned `pending` ownership/provider state and `pending_validation` SSL for the apex and www, respectively. The A, CNAME and four non-null TXT targets are unchanged from the earlier handoff.
- Both configured GoDaddy bindings are present and nonempty. Only presence was checked. Their delivery types and secure destination configuration remain unverified; authentication was held pending that metadata as instructed.
- An unauthenticated GoDaddy API request returned HTTP 401, establishing HTTPS reachability only. It does not establish credential validity, scopes or account access.
- HTTPS requests through the environment's normal proxy to all three website hostnames failed with `CONNECT tunnel failed, response 403`. The same occurred for `dns.google`. No direct-routing bypass or network-policy change was attempted.
- A separate web reader returned the closure page at the apex, but could not read the replacement origin or www. This is limited observational evidence, not a certificate or cutover verification.

## Supported PAT route

GoDaddy's current [authentication documentation](https://developer.godaddy.com/en/docs/api-users/auth) specifies Bearer PAT authentication for Domains v3. Classic `sso-key` authentication belongs to v1/v2; do not assume the supplied PAT is a classic key/secret pair.

The [Domains v3 specification](https://developer.godaddy.com/openapi/domains-v3.json) provides `GET https://api.godaddy.com/v3/domains/zones/omnequa.org/dns-records`. Its response is paginated. A complete rollback export must collect every page, retain record IDs and record fields, and confirm completeness before any mutation. The authentication documentation lists `domains.dns:update` for DNS changes; actual token scope and account access remain untested.

The [environment documentation](https://learn.chatgpt.com/docs/environments/cloud-environments) distinguishes direct environment values from network-secret placeholders. Network secrets require an allowed HTTPS destination and unchanged placeholders for proxy substitution. Ownership of a binding does not establish its delivery type.

## Remaining dependencies and execution

1. Confirm the existing bindings' delivery type and allowed destination metadata with values hidden. Do not overwrite bindings, regenerate credentials, or expose values. Use the supported secure route once confirmed.
2. Provide permitted HTTPS verification access to `omnequa.org`, `www.omnequa.org`, `omnequa.solarghost3.chatgpt.site`, and a DNS resolver such as `dns.google`. The API host is already reachable. No persistent security settings were changed by this continuation.
3. Export all authenticated DNS records without credentials, compare a second fresh read, refresh Sites targets, and apply only necessary web/verification changes. Preserve email, unrelated services and shared TXT values. Resolve any forwarding or AAAA conflicts from authenticated evidence rather than public guesses.
4. Verify both ownership states, authoritative/public DNS, hostname-valid certificates, and replacement page identity/content. The earlier replacement title is an acceptance reference, not a fresh successful check. Historical September text is not itself a failure.
5. Record actual mutations and verification receipts when available. Until then the complete rollback export and cutover acceptance remain outstanding.

## Repository safeguards

The previous handoff was read at `da59872807d7f17b97a7458420c99d3c040f8f76`. The current repository and shared Git protocol were read. Default Git identities were unsuitable; explicit noreply author and committer are required for this record. An isolated checkout and command-scoped GitHub CLI credential helper were used without persistent credential configuration. An authenticated Git read succeeded; it alone is not proof of push or lease safety. Any publication receipt must separately establish the actual push and exact-lease result.

This is a hosting-operation record only. Existing sponsor-identity and external-publication restrictions remain in force.
