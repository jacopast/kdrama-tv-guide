const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'kdrama_tv_guide.html'), 'utf8');
const start = html.indexOf('const CHANNELS =');
const end = html.indexOf('const DAY_ORDER', start);
assert.ok(start >= 0 && end > start);
const context = { drama: { platforms: [
    { name: 'Hulu', regions: ['US'], url: 'https://www.hulu.com/' },
    { name: 'Disney+', regions: ['KR'], url: 'https://www.disneyplus.com/' }
] } };
vm.createContext(context);
vm.runInContext("let regionMode = 'KR';\n" + html.slice(start, end), context);
assert.equal(vm.runInContext("platformForChannel(drama, 'Hulu').url", context), 'https://www.disneyplus.com/');
assert.equal(vm.runInContext("regionMode = 'US'; platformForChannel(drama, 'Hulu').url", context), 'https://www.hulu.com/');
assert.equal(vm.runInContext("platformRegions('Disney+').includes('KR')", context), true);
assert.equal(vm.runInContext("platformRegions('Disney+').includes('US')", context), true);
for (const drama of JSON.parse(fs.readFileSync(path.join(root, 'dramas.json'), 'utf8'))) {
    for (const platform of drama.platforms) {
        context.platformName = platform.name;
        assert.ok(vm.runInContext('platformRegions(platformName).length', context), `${drama.id}: unmapped ${platform.name}`);
    }
}
console.log('Platform aliases, regional links, and all catalog mappings passed');
