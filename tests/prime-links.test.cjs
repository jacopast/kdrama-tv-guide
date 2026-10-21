const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'kdrama_tv_guide.html'), 'utf8');
const start = html.indexOf('function getAppDeepLink(');
const end = html.indexOf('\nfunction launchPlatform(', start);
assert.ok(start >= 0 && end > start, 'App link function must be present');
const context = {};
vm.createContext(context);
vm.runInContext(html.slice(start, end), context);

// Global Prime title IDs are not 10-character Amazon ASINs. Preserve the HTTPS
// route rather than launching the app with a truncated, unrelated identifier.
const titleUrl = 'https://www.primevideo.com/detail/0INEYNSINLQC82ZUIFLK7VNV09';
assert.equal(context.getAppDeepLink(titleUrl, 'Prime Video'), null);
assert.equal(context.getAppDeepLink(titleUrl + '?ref=share', 'Prime Video'), null);
assert.equal(context.getAppDeepLink('https://www.primevideo.com', 'Prime Video'), null);
assert.equal(
    context.getAppDeepLink('https://www.amazon.com/gp/video/detail/B0HG5QDDF5', 'Prime Video'),
    'aiv://aiv/play?asin=B0HG5QDDF5'
);
assert.equal(
    context.getAppDeepLink('https://www.amazon.com/dp/B0HG5QDDF5?ref=share', 'Prime Video'),
    'aiv://aiv/play?asin=B0HG5QDDF5'
);
console.log('Prime link regressions passed (5 cases)');
