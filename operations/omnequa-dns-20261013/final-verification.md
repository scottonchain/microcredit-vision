# Omnequa domain switch: final verification receipt

Written by Codex (AI). Observation date: October 13, 2026; all times UTC.

**The website switch was verified successful by the parent verification session.** Both apex and www served the replacement site over secure HTTPS. The user was informed that the switch was resolved at 23:36:27. This additive receipt supersedes the outstanding acceptance status in [the earlier cutover record](README.md); that record, its failed TLS observations, rollback exports and original timestamps remain unchanged.

## Attributed verification evidence

The following observations were supplied by the parent verification session. They were not performed by this receipt writer's shell, and are not inferred from the older web-reader cache.

| Time | Verification path | Observed result |
| --- | --- | --- |
| 23:27:06–23:27:07 | Browser-based Dig Web Interface, direct queries to ns65.domaincontrol.com and ns66.domaincontrol.com | Both authorities returned AA/NOERROR: apex A 162.159.143.30 and 172.66.3.26; www CNAME custom-domains.chatgpt.site; TTL 3600. |
| 23:27:29 | Same authoritative browser query path | Both authorities returned no CAA. Resolver checks returned no DS and DNSSEC-requested A returned NOERROR, with no SERVFAIL; no separate resolver timestamp was supplied. |
| 23:33:59 | Sites refresh in parent session | Apex overall, provider and SSL status all active; www was already all active. |
| 23:34:38 | Dot cloud Chromium at https://www.omnequa.org/ | Matching replacement content loaded. |
| 23:34:59 | Same browser, www security indicator | Secure indicator verified. |
| 23:35:08 | [SSLShopper SSL Checker](https://www.sslshopper.com/ssl-checker.html#hostname=omnequa.org), inspected by parent | Trusted full chain and matching apex hostname at 172.66.3.26; issuer Google Trust Services WE1; certificate dates October 13, 2026–January 11, 2027. |
| 23:35:40 | Dot cloud Chromium at https://omnequa.org/ | Exact title: `More ways to earn. Fewer barriers to start. \u007c Omnequa`. Replacement hero, mission, opportunity/payment sections and October 13 journal entries loaded. |
| 23:36:15 | Same browser, apex connection panel | Explicitly showed `Connection is secure`; final URL remained https://omnequa.org/. |

## Preservation and limits

The earlier apex `ERR_SSL_VERSION_OR_CIPHER_MISMATCH` and pending-validation observations are historical failures that subsequently resolved. Their timestamps are not replaced by these successful observations. The old web-reader closure page was not used to determine final acceptance.

The pre/post exports already committed in draft PR #28 at `b09ef92cab8fac81f08791e48d285e71c3d87588` establish complete authenticated zone readback and preservation of all 15 unrelated records, including email services. This receipt adds no fresh authenticated DNS export and does not claim to have retested email delivery. All existing files from that commit are preserved byte-for-byte.

These are point-in-time observations from the stated browser, provider and certificate-checker paths, not proof of every resolver, edge address, client or future availability. The independent certificate checker result covers the apex at the stated address; www's secure acceptance is the parent browser observation plus Sites status. No raw browser capture or handshake transcript is added here. This writer independently verifies Git state, commit identities, repository checks and remote artifact bytes, not the browser observations themselves.

No DNS operation was replayed. This continuation changes only the GitHub evidence record and team handoff: no DNS, hosting, credential, security, site, schedule, blog or other publication action. Existing sponsor-naming, source-distribution and publication holds remain unchanged. PR #28 stays draft pending maintainer review; this receipt neither merges it nor claims maintainer endorsement.
