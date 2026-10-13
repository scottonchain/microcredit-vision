# OMNEQUA.org domain switch: verification and access blocker

Written by Codex (AI). Checked October 13, 2026, 22:27–22:33 UTC (16:27–16:33 America/Denver).

**Incomplete: no DNS records were changed.** The existing replacement Site is public and active, publication version 3. Both requested custom hostnames are already attached. No duplicate Site, domain attachment, or domain registration was created.

## Verified current state

| Check | Result |
| --- | --- |
| Replacement website | HTTPS 200; title “More ways to earn. Fewer barriers to start. \| Omnequa” |
| omnequa.org | HTTPS 200; title “Omnequa”; September 2026 initiative-closure notice |
| www.omnequa.org | Redirects to https://omnequa.org/ and returns the same closure-page HTML |
| Sites domain ownership | Both hostnames pending after explicit status refresh |
| Sites certificates | Both report pending_validation; replacement certificates are not verified |
| GoDaddy API transport | Unauthenticated GET to https://api.godaddy.com/v1/domains/omnequa.org/records returned HTTP 401 |
| GoDaddy credential | OMNEQUA_ORG_GD is absent or empty in this execution; only presence was checked |
| GoDaddy browser fallback | DNS-management URL redirects to Sign in; no authenticated session is available |
| Authenticated zone export | Blocked by unavailable credential |
| DNS writes | None |

Public HTTP response SHA-256:

- Old page, returned by both custom hostnames: `aa786723e196b3a42094fc01f9fbcd2a7d1be98dcb767c450b76ea041debb177`.
- Replacement origin: `0d228111d201daca31b2b45816f8be5d875459949981dde0b17887cc89fe3a1d`.

Replacement URL: https://omnequa.solarghost3.chatgpt.site

An initial default Python-client request to the replacement returned 403; a subsequent ordinary HTTP request succeeded with 200 and the replacement title above. Direct local DNS resolution failed, so public records were checked through Google Public DNS's HTTPS resolver. The HTTP client used its normal configured HTTPS path. Direct endpoint certificate inspection failed with local name-resolution errors; HTTP success alone is not recorded as independent certificate verification.

## Public DNS snapshot and rollback limits

The following public answers were returned by https://dns.google/resolve at approximately 22:30 UTC. TTL was 3600 seconds on each positive answer.

| Type | Name relative to omnequa.org | Observed value |
| --- | --- | --- |
| A | @ | 13.248.243.5 |
| A | @ | 76.223.105.230 |
| CNAME | www | omnequa.org. |
| MX | @ | priority 0, omnequa-org.mail.protection.outlook.com. |
| TXT | @ | v=spf1 include:secureserver.net -all |
| TXT | @ | NETORGFT20229360.onmicrosoft.com |
| NS | @ | ns65.domaincontrol.com. |
| NS | @ | ns66.domaincontrol.com. |

The apex AAAA and CAA queries had no answers. The www AAAA query returned only its CNAME, without an IPv6 address. All four validation TXT names listed below returned NXDOMAIN.

**This is a partial public snapshot, not a complete GoDaddy zone export or a complete rollback backup.** It preserves the observed web record sets, but does not enumerate every service, subdomain, DKIM selector, forwarding rule, or provider-managed setting. Do not replace an entire zone using this snapshot.

Before any mutation, obtain the complete authenticated GoDaddy record list, save a credential-free rollback copy, and compare it with a second current read. Preserve MX, SPF, DKIM, DMARC, NS, unrelated TXT/CNAME/SRV records, and unrelated services. Use record-set-level changes only, preserve unrelated values at shared TXT names, and reconcile any web AAAA or forwarding conflicts from the actual zone.

## Sites targets retrieved and refreshed

These values came from the existing Sites attachments, refreshed at 22:28:40 UTC for the apex and 22:28:43 UTC for www. Null validation entries were omitted. Refresh Sites again before applying them.

Names in this table are **relative to the omnequa.org zone**, suitable for interpreting GoDaddy's host/name field. Do not append the zone twice.

| Type | Relative name | Required value |
| --- | --- | --- |
| A | @ | 162.159.143.30 |
| A | @ | 172.66.3.26 |
| CNAME | www | custom-domains.chatgpt.site. |
| TXT | _openai-site-verification | openai-site-verification=emvbn-7TWSmpkcQneDKQTZMyHEG0tW2eaw5CekH8AN4 |
| TXT | _cf-custom-hostname | 0c320d16-c2bb-4eb2-92eb-98e71748b745 |
| TXT | _openai-site-verification.www | openai-site-verification=R2-X_lRl9c7IZHkHBF5ghOJKDuh1SgDHXbB_u44U-xc |
| TXT | _cf-custom-hostname.www | 2c0ad689-914f-4ec1-b288-3b0e16e341c5 |

The verification TXT values are intended public DNS records, not the GoDaddy credential.

## Exact configuration needed to unblock the API route

The current execution exposes neither OMNEQUA_ORG_GD nor a supported vault-retrieval/environment-edit operation. API transport is reachable; credential delivery is the immediate blocker. No conclusion about the stored token's validity, permissions, or API compatibility is possible until an authenticated request is made.

In **Settings → Codex Cloud → Environments → microcredit-vision → Edit**:

1. Configure a requested personal value named exactly `OMNEQUA_ORG_GD`, with the **same type** as its existing Personal vault entry: Environment variable or Network secret. Do not paste its value into a prompt or repository.
2. Ensure the existing Personal vault entry's **Applies to** includes this environment or All environments.
3. If it is a Network secret, permit `api.godaddy.com` as its destination. Keep the supplied placeholder unchanged when sending the authorized HTTPS request.
4. Enable internet access and allow `api.godaddy.com` over HTTPS port 443. Also allow `omnequa.org`, `www.omnequa.org`, and `omnequa.solarghost3.chatgpt.site` for verification. Allow `dns.google` if using the same HTTPS DNS checks.
5. Save, **Republish**, and start a **new task in that published environment**. Reopening this Work chat does not select that Codex Cloud environment.

Official configuration reference: https://learn.chatgpt.com/docs/environments/cloud-environments

## Remaining execution and acceptance

1. Verify credential presence without exposing it. Use the credential through GoDaddy's supported authentication method; authenticate and read the complete zone.
2. Preserve the full rollback export without credentials. Reconcile the current zone with freshly returned Sites targets.
3. Apply only the required web routing and ownership/certificate-validation records. Preserve email and unrelated services.
4. Refresh both existing Sites attachments until ownership and SSL are active; capture any additional certificate-validation records if returned.
5. Verify authoritative and public DNS, valid HTTPS certificates for each hostname, and replacement page content at both hostnames. The replacement has its own historical September reference, so identify it by current page title and content rather than by absence of the word “September.”
6. Commit the actual changes, rollback reference, and final verification results. Do not mark the cutover complete until these checks pass. Change canonical URLs to the custom domain only after the cutover is verified, as required by the Site's current README.

This record concerns hosting operations only and does not publish a new blog post or claim a completed cutover.
