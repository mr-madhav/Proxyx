def response(flow):
    if "jsonplaceholder.typicode.com/posts/1" in flow.request.pretty_url:
        flow.response.text = flow.response.text.replace("Good morning! lucifer morning star is here.")