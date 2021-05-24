var contextMenuItem = {
  id: "Clickbait",
  title: "Check if clickbait or not",
  contexts: ["link", "selection"]
};

chrome.contextMenus.create(contextMenuItem);

chrome.contextMenus.onClicked.addListener(function(clickData) {
  if (clickData.menuItemId == "Clickbait" && clickData.selectionText == null) {
    var request_contextlink = new XMLHttpRequest();
    request_contextlink.onreadystatechange = function() {
      if (request_contextlink.readyState == 4) {
        var data = JSON.parse(request_contextlink.responseText);
        displayAlert(data);
      }
    };

    request_contextlink.open(
      "GET",
      "http://localhost:5000/?url=" + clickData.linkUrl,
      false
    );
    request_contextlink.send();
  }
});

chrome.contextMenus.onClicked.addListener(function(clickData) {
  if (clickData.menuItemId == "Clickbait" && clickData.selectionText) {
    var request_contextselection = new XMLHttpRequest();
    request_contextselection.onreadystatechange = function() {
      if (request_contextselection.readyState == 4) {
        var data = JSON.parse(request_contextselection.responseText);
        displayAlert(data);
      }
    };

    request_contextselection.open(
      "GET",
      "http://localhost:5000/?headline=" + clickData.selectionText,
      false
    );
    request_contextselection.send();
  }
});

function displayAlert(data) {
  var alert_data = "";
  if (data.error !== undefined) {
    alert_data += "Error: " + data.error;
  } else {
    alert_data += "Headline: " + data.headline;
    alert_data += "\nPercentage: " + data.percentage.toString();
    if (data.percentage > 70.0) {
      alert_data += "\nResult: Clickbait.";
    } else if (data.percentage > 50.0) {
      similar = data.similarArticles.toString();
      similar = similar.charAt(0).toUpperCase() + similar.slice(1);
      alert_data += "\nSimilar articles found: " + similar;
      alert_data += "\nResult: Probably clickbait.";
    } else if (data.percentage > 30.0) {
      similar = data.similarArticles.toString();
      similar = similar.charAt(0).toUpperCase() + similar.slice(1);
      alert_data += "\nSimilar articles found: " + similar;
      alert_data += "\nResult: Probably not clickbait.";
    } else {
      alert_data += "\nResult: Not clickbait.";
    }
  }
  alert(alert_data);
}
