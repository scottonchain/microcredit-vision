// Synthetic browser-API fixture, not a browser run or delivered inquiry.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const keys = ['employer', 'source', 'task', 'eligibility', 'pay', 'payout', 'barrier'];
function fixture(invalid, scriptSource = 'assets/intake.js') {
  let click, input;
  const fields = Object.fromEntries(keys.map(k => [k, {
    value: k === 'task' ? 'Useful & paid work / café?\nReview honestly.' : `Public ${k}`,
    reportValidity: () => k !== invalid,
  }]));
  const button = {disabled: true, addEventListener: (name, fn) => {assert.equal(name, 'click'); click = fn;}};
  const fallback = {hidden: true, removeAttribute: name => {assert.equal(name, 'href'); delete fallback.href;}};
  const plainPanel = {hidden: true};
  const plainDraft = {value: ''};
  const status = {};
  const intake = {
    addEventListener: (name, fn) => {assert.equal(name, 'input'); input = fn;},
    querySelectorAll: () => Object.values(fields),
    querySelector: selector => fields[selector.match(/name="([^"]+)"/)[1]],
  };
  const window = {location: {href: ''}};
  const nodes = {'#opportunity-intake': intake, '#prepare-draft': button, '#email-draft-link': fallback, '#draft-status': status, '#plain-draft-panel': plainPanel, '#plain-draft': plainDraft};
  vm.runInNewContext(fs.readFileSync(scriptSource, 'utf8'), {document: {querySelector: key => nodes[key]}, window, encodeURIComponent});
  assert.equal(button.disabled, false);
  click();
  return {window, fallback, status, plainPanel, plainDraft, fields, click, input};
}
for (const key of keys) {
  const f = fixture(key);
  assert.equal(f.window.location.href, '');
  assert.equal(f.fallback.hidden, true);
  assert.equal(f.plainPanel.hidden, true);
  assert.equal(f.plainDraft.value, '');
}
const good = fixture();
assert.equal(good.window.location.href, ''); // No protocol handler or app launch required.
assert.match(good.fallback.href, /^mailto:/);
assert.ok(good.fallback.href.startsWith('mailto:codex-microcredit@agentmail.to?'));
const query = new URLSearchParams(good.fallback.href.split('?')[1]);
assert.equal(query.get('subject'), 'Omnequa employer | source=website-intake');
assert.match(query.get('body'), /Useful & paid work \/ café\?\r\nReview honestly\./);
assert.ok(!query.get('body').replace(/\r\n/g, '').includes('\n'));
for (const label of ['Employer / payer', 'Original source', 'Eligibility and location', 'Pay and acceptance terms', 'Payment timing, method, costs and cashout', 'Access barrier and proposed next step']) assert.ok(query.get('body').includes(label));
assert.match(query.get('body'), /remove private worker records/);
assert.equal(good.plainDraft.value, query.get('body').replace(/\r\n/g, '\n'));
assert.equal(good.plainPanel.hidden, false);
assert.equal(good.fallback.hidden, false);
assert.match(good.status.textContent, /has not been sent/);
good.fields.task.value = '<script>not HTML</script> & revised task';
good.input();
assert.equal(good.plainDraft.value, '');
assert.equal(good.plainPanel.hidden, true);
assert.equal(good.fallback.hidden, true);
assert.equal(good.fallback.href, undefined);
assert.match(good.status.textContent, /Answers changed/);
good.click();
assert.match(good.plainDraft.value, /<script>not HTML<\/script> & revised task/);
assert.equal(good.plainDraft.value, new URLSearchParams(good.fallback.href.split('?')[1]).get('body').replace(/\r\n/g, '\n'));
assert.equal(good.plainPanel.hidden, false);
good.fields.pay.reportValidity = () => false;
good.click();
assert.equal(good.plainDraft.value, '');
assert.equal(good.plainPanel.hidden, true);
assert.equal(good.fallback.hidden, true);
assert.equal(good.fallback.href, undefined);
assert.match(good.status.textContent, /Check the required answers/);
// The generated script is tested too; stale delivery copies must fail.
const generated = fixture(undefined, 'dist/intake.js');
assert.equal(generated.plainDraft.value, query.get('body').replace(/\r\n/g, '\n'));
assert.equal(generated.window.location.href, '');
const large = fixture();
for (const [key, limit] of Object.entries({employer:200, source:600, task:800, eligibility:500, pay:600, payout:800, barrier:600})) large.fields[key].value = 'é'.repeat(limit);
large.click();
assert.equal(large.plainDraft.value, new URLSearchParams(large.fallback.href.split('?')[1]).get('body').replace(/\r\n/g, '\n'));
assert.ok(large.plainDraft.value.includes('é'.repeat(800)));
assert.equal(large.window.location.href, '');
const script = fs.readFileSync('assets/intake.js', 'utf8');
assert.doesNotMatch(script, /fetch\(|XMLHttpRequest|localStorage|sessionStorage|\.submit\(|innerHTML|clipboard|window\.location\s*[.=]/);
console.log('PASS: 7 invalid-field controls, exact plain-text/encoded-draft parity, no handler launch, edit invalidation, safe text, generated copy and no-send/storage guard (synthetic only).');
