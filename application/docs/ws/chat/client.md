---
title: Websocket Chat Client
description: How the client interacts with something.
---


# Documentation header

This is some [documentation](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_client_applications#using_json_to_transmit_objects).

```javascript
function sendText() {
  const msg = {
    type: "message",
    text: document.getElementById("text").value,
    id:   clientID,
    date: Date.now()
  };
  exampleSocket.send(JSON.stringify(msg));
  document.getElementById("text").value = "";
}
```