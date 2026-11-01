Custom HTML attributes can be a useful way to mark which controls should share a behavior. The attribute describes intent; your JavaScript implements the behavior.

For a text item, an illustrative marker is:

```html
data-auto-upper="Y"
```

A delegated listener can recognize marked text inputs:

```javascript
document.addEventListener('change', function (event) {
  const input = event.target;
  if (input instanceof HTMLInputElement &&
      input.matches('[data-auto-upper="Y"]')) {
    input.value = input.value.toUpperCase();
  }
});
```

Check the rendered markup of the specific APEX item type. The attribute must reach the element your code targets. Do not assume that every plug-in or composite item renders the same structure.

### Separate presentation from business rules

This example changes a browser value. It does not validate the value on the server, persist it, or automatically synchronize every APEX item implementation. If uppercase is a business requirement, normalize and validate it in the server-side write path too.

Prefer the native placeholder property when all you need is a placeholder. Use a small documented set of custom markers for behavior that is genuinely shared. Test keyboard use, screen readers, and partial refreshes.

*Editorial correction: data-* attributes do not activate APEX behavior by themselves. A server process changing session state on page load is also different from reacting to a user's later typing.*