function handleSocket() {
    const webSocketServerEndpoint = "wss://mock.com"
    const params = {user_id: 'unknown'};
    let socket = new WebSocket(`${webSocketServerEndpoint}?${new URLSearchParams(params).toString()}`);

    socket.onopen = function(e) {
      alert("[open] Connection established");
      alert("Sending to server");
      socket.send(JSON.stringify({"user_id": "unknown"}));
    };
    
    socket.onmessage = function(event) {
      alert(`[message] Data received from server: ${event.data}`);
    };
    
    socket.onclose = function(event) {
      if (event.wasClean) {
        alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
      } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        alert('[close] Connection died');
      }
    };
    
    socket.onerror = function(error) {
      alert(`[error]`);
    };
}