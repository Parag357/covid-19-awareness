fetch("https://ac41bf31.ngrok.io/api/news"), {headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "*"
    }
  }
.then(function(resp){
    return resp.json();
})
.then(function(data){
    console.log(data.title);
});