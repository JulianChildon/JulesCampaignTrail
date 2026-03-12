const { JSDOM } = require("jsdom");
const fs = require('fs');

const html = fs.readFileSync('campaign-trail/index.html', 'utf8');
const dom = new JSDOM(html, { runScripts: "dangerously", resources: "usable", url: "http://localhost/"});

dom.window.onerror = function (msg, url, lineNo, columnNo, error) {
  console.log('JSDOM Error: ', msg, lineNo, columnNo, error);
  return false;
};

setTimeout(() => {
    try {
        console.log("DOM loaded. Triggering game elements...");
        
        let win = dom.window;
        let doc = win.document;
        
        // Let's call the start function directly if we can
        // The game normally requires jQuery which is loaded via tag
        // so we wait a tick to ensure it parsed
    } catch(e) {
        console.error(e);
    }
}, 2000);
