// Synthetic browser-API fixture, not a browser run or delivered inquiry.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const keys = ['employer', 'source', 'task', 'eligibility', 'pay', 'payout', 'barrier'];
function fixture(invalid) {
  let click;
  const fields = Object.fromEntries(keys.map(k => [k, {
    value: k === 'task' ? 'Useful & paid work / café?\nReview honestly.' : `Public ${k}`,
    reportValidity: () => k !== invalid,
  }]));
  const button = {disabled: true, addEventListener: (name, fn) => {assert.equal(name, 'click'); click = fn;}};
  const fallback = {hidden: true};
  const status = {};
  const intake = {
    querySelectorAll: () => Object.values(fields),
    querySelector: selector => fields[selector.match(/name="([^"]+)"/)[1]],
  };
  const window = {location: {href: ''}};
  const nodes = {'#opportunity-intake': intake, '#prepare-draft': button, '#email-draft-link': fallback, '#draft-status': status};
  vm.runInNewContext(fs.readFileSync('assets/intake.js', 'utf8'), {document: {querySelector: key => nodes[key]}, window, encodeURIComponent});
  assert.equal(button.disabled, false);
  click();
  return {window, fallback, status};
}
for (const key of keys) {
  const f = fixture(key);
  assert.equal(f.window.location.href, '');
  assert.equal(f.fallback.hidden, true);
}
const good = fixture();
assert.match(good.window.location.href, /^mailto:/);
const query = new URLSearchParams(good.window.location.href.split('?')[1]);
assert.equal(query.get('subject'), 'Omnequa employer | source=website-intake');
assert.match(query.get('body'), /Useful & paid work \/ café\?\nReview honestly\./);
for (const label of ['Employer / payer', 'Original source', 'Eligibility and location', 'Pay and acceptance terms', 'Payment timing, method, costs and cashout', 'Access barrier and proposed next step']) assert.ok(query.get('body').includes(label));
assert.match(query.get('body'), /remove private worker records/);
assert.equal(good.fallback.href, good.window.location.href);
assert.equal(good.fallback.hidden, false);
assert.match(good.status.textContent, /Review it in your email app before sending/);
const script = fs.readFileSync('assets/intake.js', 'utf8');
assert.doesNotMatch(script, /fetch\(|XMLHttpRequest|localStorage|sessionStorage|\.submit\(/);
console.log('PASS: 7 invalid-field controls, encoded draft, fallback and no-send/storage source guard (synthetic only).');
