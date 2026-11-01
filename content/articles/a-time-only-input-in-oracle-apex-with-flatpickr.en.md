Sometimes a form needs a clear time-only input. Flatpickr can provide that interaction in an APEX page when its behavior suits the application. Thanks to **Ahmed Sherif**, whose contribution I acknowledged in the original post.

Start with a text item named P10_START_TIME. Load the chosen Flatpickr CSS through the page's CSS File URLs and its JavaScript through JavaScript File URLs. Use the official installation guidance to obtain the assets, and keep a tested version pinned for repeatable deployment. [Flatpickr: getting started](https://flatpickr.js.org/getting-started/).

After the library and item are available, initialize it in Execute when Page Loads:

```javascript
flatpickr("#P10_START_TIME", {
  enableTime: true,
  noCalendar: true,
  dateFormat: "H:i",
  time_24hr: true
});
```

This enables time selection, hides the calendar, and formats the value as hours and minutes using a 24-hour clock. The official examples include this time-only configuration. [Flatpickr: examples](https://flatpickr.js.org/examples/).

Test keyboard use, mobile behavior, and the dialog layout in the actual page. A widget that looks good in a demo still needs to fit the application's users. Avoid attaching a second date/time widget to an item that already manages its own picker.

The selected string also needs server-side validation and a clear storage rule. Decide whether the business value is a local time of day or part of a dated event; the picker alone does not define that meaning.

*Editorial correction: LinkedIn's extracted hashtag formatting broke the original selector. The valid selector is exactly `#P10_START_TIME`, without a newline or “hashtag” text.*