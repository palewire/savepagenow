```{include} _templates/nav.html
```

# Customizing the user agent

In an effort to be transparent and polite to the Internet Archive, all requests made by savepagenow carry a custom [user agent](https://en.wikipedia.org/wiki/User_agent) that identifies itself as ``"savepagenow (https://github.com/pastpages/savepagenow)"``.

You can further customize this setting by using the optional arguments to our API.

Here's how to do it in Python:

```python
savepagenow.capture("http://www.example.com/", user_agent="my user agent here")
```

And here's how to do it from the command line:

```bash
savepagenow http://www.example.com/ --user-agent "my user agent here"
```
