function consume_comments(articleId, userId) {
  // Connect to the WebSocket

  const wsPath = `ws://${window.location.host}/ws/articles/${articleId}`;
  console.log("# WS Connecting to:", wsPath);

  const socket = new WebSocket(wsPath);

  socket.onopen = function (e) {
    console.log("# WebSocket connection established");
  };

  socket.onclose = function (e) {
    console.log("WebSocket connection closed");
    setTimeout(function () {
      console.log("Reconnecting...");
      //connect();
    }, 2000);
  };
  socket.onerror = function (err) {
    console.log("WebSocket encountered an error: " + err.message);
    console.log("Closing the socket.");
    socket.close();
  };

  socket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    // Append new comment to DOM or handle as needed
    console.log("# WS onmessage with:", data);

    if (data.comment !== null) {
      if (data.comment.author_id !== userId) {
        appendComment(data.comment.html);
      } else {
        console.log("Comment by current user. Ignoring.");
      }
    } else {
      console.log("No comment found in message:", data);
    }
  };

  function appendComment(commentHTML) {
    // Create a temporary element
    const tempDiv = document.createElement("div");

    // Set the innerHTML to the escaped HTML string
    tempDiv.innerHTML = JSON.parse(commentHTML);

    // Extract the parsed HTML content
    const unescapedHTML = tempDiv.firstChild;

    console.log("Appending comment:", unescapedHTML);
    const commentsContainer = document.getElementById("comments-container");
    commentsContainer.insertBefore(
      tempDiv.firstChild,
      commentsContainer.firstChild
    );
  }
}
