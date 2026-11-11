// Claude's answer becomes what the page shows: the message and, when Claude offers them, reply buttons.
const res = $input.first().json || {};
let body = res.body !== undefined ? res.body : res;
if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
if (!body || typeof body !== 'object') body = {};
const status = Number(res.statusCode) || 0;
const parts = Array.isArray(body.content) ? body.content : [];
let text = parts.filter(function (c) { return c && c.type === 'text'; }).map(function (c) { return String(c.text || ''); }).join('').trim();
if (status >= 300 || !text) {
  // The page gets a plain answer it can show; "problem" makes Problem? fail the run afterwards, so it shows up under failed executions.
  return [{ json: { status: 200, response: { error: 'unavailable' }, problem: 'Claude: HTTP ' + status + ' ' + String((body.error && body.error.message) || res.error || body.stop_reason || 'no text in the answer').slice(0, 300) } }];
}
// Claude answers as JSON {reply, buttons}; if that ever fails, the text itself is the reply.
let buttons = [];
let parsed = null;
try { parsed = JSON.parse(text); } catch (e) { parsed = null; }
if (parsed && typeof parsed === 'object' && typeof parsed.reply === 'string') {
  text = parsed.reply.trim();
  buttons = (Array.isArray(parsed.buttons) ? parsed.buttons : []).map(function (s) { return String(s || '').trim().slice(0, 24); }).filter(function (s) { return s.length > 0; }).slice(0, 3);
}
text = text.split('*').join('').trim();
if (!text && buttons.length) text = buttons.join(' / ');
if (!text) return [{ json: { status: 200, response: { error: 'unavailable' }, problem: 'Claude: empty reply' } }];
return [{ json: { status: 200, response: { reply: text.slice(0, 1500), buttons: buttons }, problem: '', usage: body.usage || null, model: String(body.model || '') } }];